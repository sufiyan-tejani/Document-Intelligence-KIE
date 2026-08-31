# 📄 Document Intelligence & Key Information Extraction System

### Deep Learning-Based Document Classification, OCR & Automated Information Extraction

An end-to-end document intelligence system that automatically classifies document images, extracts text using OCR, identifies key information from relevant documents, validates extracted fields, and stores structured results in a SQLite database.

The system combines **ResNet50 transfer learning**, **EasyOCR**, **rule-based Key Information Extraction (KIE)**, and **SQLite** within an interactive **Streamlit** application.

---

## 🚀 Features

- Deep learning-based document classification
- ResNet50 transfer learning with ImageNet pretrained weights
- Classification across **16 document categories**
- High-resolution **336 × 336** image input
- Confidence score for document predictions
- OCR-based text extraction using EasyOCR
- Rule-based Key Information Extraction (KIE)
- Invoice / Job Number extraction
- Total Expenses extraction
- Basic extraction validation
- SQLite database storage
- Interactive Streamlit interface
- End-to-end document processing pipeline

---

## 🧠 System Workflow

```text
Document Image
      ↓
Image Preprocessing
      ↓
ResNet50 Document Classifier
      ↓
Document Type + Confidence
      ↓
EasyOCR Text Extraction
      ↓
Rule-Based Key Information Extraction
      ↓
Field Validation
      ↓
SQLite Database

