# 📄 Intelligent Document Processing

An AI-powered **Intelligent Document Processing (IDP)** application that automatically extracts meaningful and structured information from **Invoices, Resumes, and ID Cards** using Computer Vision, Optical Character Recognition (OCR), Text Processing, and Natural Language Processing (NLP).

## 🌐 Live Demo

🤗 **Hugging Face Deployment:**

👉 https://huggingface.co/spaces/Mohanrajdeena/Intelligent-document-processing

The application is deployed on Hugging Face using Gradio and provides AI-powered document processing for invoices, resumes, and ID cards.

---

🚀 **Deployed Streamlit Application:**

👉 https://intelligent-document-processing-jphfscl8pyay96uaxsadc6.streamlit.app/

The application allows users to upload documents and view extracted text and structured information through an interactive Streamlit dashboard.

---

# 📌 Project Overview

Manual document processing can be time-consuming and error-prone, especially when organizations handle large volumes of invoices, resumes, and identification documents.

This project automates the document processing workflow by combining:

- Image preprocessing
- Optical Character Recognition (OCR)
- Text cleaning
- Named Entity Recognition (NER)
- Structured information extraction
- Model evaluation
- Interactive Streamlit dashboard

The system accepts document images, improves their quality through preprocessing, extracts text using EasyOCR, cleans the extracted text, identifies important entities, and presents the results in a structured format.

---

# 🎯 Project Objectives

The main objectives of this project are:

- Automate document information extraction.
- Improve OCR performance using image preprocessing.
- Extract text from document images using EasyOCR.
- Clean and normalize OCR-generated text.
- Extract meaningful entities from different document types.
- Process invoices, resumes, and ID cards using a unified application.
- Evaluate information extraction using Precision, Recall, and F1-score.
- Provide an interactive web-based dashboard.
- Deploy the application using Streamlit Community Cloud.

---

# 📂 Supported Documents

The application supports three major document categories.

## 🧾 1. Invoice

The system extracts important invoice information such as:

- Invoice Number
- Invoice Date
- Vendor Information
- Customer Information
- GSTIN
- Total Amount
- Tax Amount
- Other available invoice details

---

## 📄 2. Resume

The system extracts relevant candidate information such as:

- Candidate Name
- Email
- Phone Number
- Skills
- Education
- Experience
- Location
- Other available information

---

## 🪪 3. ID Card

The system extracts available identification information such as:

- Name
- ID Number
- Date of Birth
- Gender
- Address
- Other available identification fields

> The exact fields extracted depend on the document quality and the information detected by OCR.

---

# 🔄 End-to-End Project Pipeline

```text
                    ┌─────────────────────┐
                    │   Document Upload   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Image Preprocessing │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        OCR          │
                    │      EasyOCR        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Cleaning     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       NER           │
                    │ Entity Extraction   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Structured Fields   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    JSON Output      │
                    └─────────────────────┘
