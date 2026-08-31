# 📄 Document Intelligence & Key Information Extraction System

### Deep Learning-Based Document Classification, OCR & Automated Information Extraction

An end-to-end **Document AI** system that processes document images, identifies their document type using a deep learning classifier, extracts text using OCR, retrieves important fields from relevant documents, validates the extracted information, and stores structured results in a SQLite database.

The project combines **ResNet50 transfer learning, TensorFlow/Keras, EasyOCR, rule-based Key Information Extraction (KIE), regular expressions, and SQLite** into an interactive **Streamlit** application.

---

## 🎯 Project Objective

Organizations often receive large volumes of documents such as invoices, forms, letters, reports, resumes, and emails. Manually identifying document types and extracting important information from these documents is time-consuming and error-prone.

This project demonstrates how a document-processing workflow can be partially automated using machine learning and OCR.

Given a document image, the system can:

* Identify the document category.
* Provide a prediction confidence score.
* Extract readable text from the document.
* Identify relevant structured information from the extracted text.
* Validate whether the required information was successfully extracted.
* Store validated information in a database.

The project focuses on building a **complete and understandable Document AI pipeline** rather than only developing an image classification model.

---

## 🧠 Document Classification

The first component of the system is a deep learning-based document image classifier.

A **ResNet50** architecture pretrained on **ImageNet** was used as the foundation for the classifier. Transfer learning was used to leverage the visual representations learned from the large ImageNet dataset and adapt them to document-image classification.

The model processes document images at a relatively high resolution of **336 × 336 pixels**, allowing more visual information from document layouts and text regions to be retained compared with lower-resolution inputs.

### Model Configuration

| Parameter                | Configuration                       |
| ------------------------ | ----------------------------------- |
| Architecture             | ResNet50                            |
| Pretrained weights       | ImageNet                            |
| Task                     | Multi-class document classification |
| Number of classes        | 16                                  |
| Input resolution         | 336 × 336                           |
| Framework                | TensorFlow / Keras                  |
| Best validation accuracy | 62.03%                              |

The model was trained and fine-tuned through multiple experiments, with the final high-resolution model selected based on validation performance.

The trained model is approximately **285 MB**, so it is intentionally excluded from this GitHub repository.

---

## 📂 Document Categories

The classifier recognizes the following 16 document categories:

* Advertisement
* Budget
* Email
* File Folder
* Form
* Handwritten
* Invoice
* Letter
* Memo
* News Article
* Presentation
* Questionnaire
* Resume
* Scientific Publication
* Scientific Report
* Specification

These categories represent different types of documents with substantially different visual structures and layouts.

---

## 🔎 OCR-Based Text Extraction

After document classification, the uploaded document is processed using **EasyOCR**.

OCR (Optical Character Recognition) converts visible text in the document image into machine-readable text.

The application:

1. Converts the uploaded image into an RGB image.
2. Processes the image using EasyOCR.
3. Collects the detected text regions.
4. Combines the detected text into a single text representation.
5. Displays the extracted text to the user.

This extracted text becomes the input for the subsequent information-extraction stage.

---

## 🧩 Key Information Extraction (KIE)

The project implements a lightweight, rule-based approach to **Key Information Extraction**.

Instead of applying a separate complex NLP model, regular expressions are used to identify specific fields from the OCR output.

For relevant invoice-style documents, the system extracts:

### Invoice / Job Number

The application searches the OCR text for supported invoice or job-number patterns, including formats such as:

* `INV123`
* `INV-123`
* `INV 123`
* `TI1234-5678`

### Total Expenses

The system searches for the **TOTAL EXPENSES** field and extracts the associated numeric amount.

The extracted value is converted into a numeric representation before being stored.

This approach keeps the KIE component **simple, interpretable, and easy to extend** with additional document-specific extraction rules.

---

## ✅ Information Validation

Extracted information is checked before being stored.

For the implemented invoice extraction workflow, validation requires both:

* A valid invoice / job number to be identified.
* A total-expenses value to be successfully extracted.

If both fields are available, the application reports:

**Validation: PASSED**

If one or more required fields cannot be extracted, the application warns the user that some information could not be identified.

This provides a basic validation layer between OCR/KIE and database storage.

---

## 🗄️ SQLite Database

Validated extracted information is stored using **SQLite**, providing a lightweight relational database without requiring an external database server.

The database stores:

| Column           | Description                  |
| ---------------- | ---------------------------- |
| `id`             | Unique record identifier     |
| `invoice_number` | Extracted invoice/job number |
| `total_expenses` | Extracted expense amount     |

The database is created automatically when the application runs.

The generated `.db` file is excluded from the GitHub repository through `.gitignore`.

---

## 🖥️ Streamlit Application

The complete pipeline is exposed through an interactive **Streamlit** application.

The user can upload a document image and view:

* The uploaded document.
* Predicted document category.
* Classification confidence.
* OCR-extracted text.
* Extracted invoice/job number.
* Extracted total expenses.
* Validation status.
* Database storage confirmation.

The application loads the trained classification model and performs inference on newly uploaded documents.

---

## 📊 Development & Experiments

The complete development process is documented in:

`Document_Intelligence_KIE_DL_Project.ipynb`

The notebook contains the project's experimental and development work, including the deep learning model development and evaluation process.

The final application logic is separated into:

`app.py`

This separation keeps the experimental work and the deployable application code distinct.

---

## 🛠️ Technology Stack

### Programming

* Python

### Deep Learning

* TensorFlow
* Keras
* ResNet50
* Transfer Learning

### Data Processing

* NumPy
* Pandas

### Computer Vision & OCR

* EasyOCR
* Pillow

### Information Extraction

* Python Regular Expressions

### Database

* SQLite

### Application

* Streamlit

### Development Tools

* Jupyter Notebook
* Google Colab
* Git
* GitHub

---

## 📁 Project Structure

```text
Document-Intelligence-KIE/
│
├── Document_Intelligence_KIE_DL_Project.ipynb
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── database/
    └── .gitkeep
```

The trained `.keras` model and generated SQLite database are intentionally not included in the repository.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sufiyan-tejani/Document-Intelligence-KIE.git
cd Document-Intelligence-KIE
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the trained model

Because the trained model is approximately 285 MB, it is not stored in this repository.

Place the trained model at:

```text
model/document_classifier_v3_high_res.keras
```

The application expects the model at this location.

### 4. Run the application

```bash
streamlit run app.py
```

---

## ⚠️ Current Limitations

The current implementation intentionally uses a simple and interpretable KIE approach.

* KIE is currently focused on invoice/job-number and total-expenses extraction.
* OCR accuracy depends on document image quality.
* The document classifier achieves 62.03% best validation accuracy and can be improved with more training data and further fine-tuning.
* The trained model is not included in the repository because of its large file size.
* The current validation logic checks whether required fields were successfully extracted rather than performing advanced semantic validation.

---

## 🔮 Future Improvements

Potential extensions include:

* Improve document classification using a larger training dataset.
* Add document-specific KIE for resumes, forms, reports, and other categories.
* Introduce OCR preprocessing for noisy or low-quality documents.
* Add confidence scores for extracted fields.
* Implement more robust field validation.
* Add a database viewer and document history to the Streamlit interface.
* Store document metadata and timestamps.
* Deploy the trained model through a cloud-based inference service.

---

## 👤 Author

**Sufiyan Tejani**

M.Sc. Mathematics, IIT Kharagpur

GitHub: https://github.com/sufiyan-tejani

LinkedIn: https://www.linkedin.com/in/sufiyan-tejani/
