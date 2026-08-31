
import streamlit as st
import tensorflow as tf
import easyocr
import numpy as np
import re
import sqlite3
from pathlib import Path
from PIL import Image


# ====================================================
# PATHS
# ====================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model" / "document_classifier_v3_high_res.keras"
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "documents.db"


# ====================================================
# PAGE
# ====================================================

st.set_page_config(
    page_title="Document Intelligence System",
    page_icon="📄",
    layout="centered"
)

st.title("Document Intelligence System")


# ====================================================
# LOAD MODEL
# ====================================================

model = tf.keras.models.load_model(MODEL_PATH)

reader = easyocr.Reader(["en"])


# ====================================================
# CLASS NAMES
# ====================================================

class_names = [
    "advertisement", "budget", "email", "file_folder",
    "form", "handwritten", "invoice", "letter",
    "memo", "news_article", "presentation", "questionnaire",
    "resume", "scientific_publication", "scientific_report",
    "specification"
]


# ====================================================
# UPLOAD DOCUMENT
# ====================================================

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Document"
    )


    # ====================================================
    # DOCUMENT CLASSIFICATION
    # ====================================================

    image_array = np.array(image)

    resized = tf.image.resize(
        image_array,
        (336, 336)
    )

    resized = tf.expand_dims(
        resized,
        0
    )

    prediction = model.predict(
        resized,
        verbose=0
    )

    class_id = np.argmax(
        prediction[0]
    )

    confidence = (
        prediction[0][class_id] * 100
    )


    st.subheader(
        "Document Classification"
    )

    st.write(
        f"**Type:** {class_names[class_id]}"
    )

    st.write(
        f"**Confidence:** {confidence:.2f}%"
    )


    # ====================================================
    # OCR
    # ====================================================

    text = reader.readtext(
        image_array
    )

    extracted_text = "\n".join(
        item[1] for item in text
    )


    st.subheader(
        "Extracted Text"
    )


    if extracted_text:

        st.text(
            extracted_text
        )

    else:

        st.write(
            "No text detected."
        )


    # ====================================================
    # KEY INFORMATION EXTRACTION
    # ====================================================

    invoice_number = None
    total_expenses = None


    number_match = re.search(
        r"(?:TI\d{4}-\d{4}|INV[-\s]?\d+)",
        extracted_text,
        re.IGNORECASE
    )


    amount_match = re.search(
        r"TOTAL EXPENSES\s*[:\-]?\s*(\d+\.\d{2})",
        extracted_text,
        re.IGNORECASE
    )


    if number_match:

        invoice_number = (
            number_match.group(0)
        )


    if amount_match:

        total_expenses = float(
            amount_match.group(1)
        )


    # ====================================================
    # KEY INFORMATION
    # ====================================================

    st.subheader(
        "Key Information"
    )


    st.write(
        f"**Invoice / Job Number:** "
        f"{invoice_number if invoice_number else 'Not found'}"
    )


    st.write(
        f"**Total Expenses:** "
        f"{total_expenses if total_expenses is not None else 'Not found'}"
    )


    # ====================================================
    # VALIDATION
    # ====================================================

    st.subheader(
        "Validation"
    )


    if (
        invoice_number
        and total_expenses is not None
    ):

        st.success(
            "Validation: PASSED"
        )

    else:

        st.warning(
            "Some information could not be extracted."
        )


    # ====================================================
    # SQLITE DATABASE
    # ====================================================

    DATABASE_DIR.mkdir(
        exist_ok=True
    )


    conn = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = conn.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT,
            total_expenses REAL
        )
    """)


    if (
        invoice_number
        and total_expenses is not None
    ):

        cursor.execute(
            """
            INSERT INTO documents
            (invoice_number, total_expenses)
            VALUES (?, ?)
            """,
            (
                invoice_number,
                total_expenses
            )
        )

        conn.commit()

        st.success(
            "Document saved to database."
        )


    conn.close()
