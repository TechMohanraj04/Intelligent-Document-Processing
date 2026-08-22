
import streamlit as st
import cv2
import numpy as np
import easyocr
import re
import json


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Intelligent Document Processing",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# LOAD OCR MODEL
# ============================================================

@st.cache_resource
def load_ocr_reader():

    return easyocr.Reader(
        ["en"],
        gpu=True,
        verbose=False
    )


reader = load_ocr_reader()


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    height, width = gray.shape

    # Resize only small images
    if width < 1500:

        scale = 1500 / width

        gray = cv2.resize(
            gray,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_CUBIC
        )

    # Light denoising
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Otsu thresholding
    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return processed


# ============================================================
# OCR
# ============================================================

def extract_text(image):

    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    text_parts = []

    for result in results:

        if len(result) >= 2:

            text_parts.append(
                str(result[1])
            )

    return "\n".join(
        text_parts
    )


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    return text.strip()


# ============================================================
# INVOICE NUMBER
# ============================================================

def extract_invoice_number(text):

    patterns = [

        r"(?:invoice\s*(?:no|number|#)"
        r"\s*[:\-]?\s*)"
        r"([A-Z0-9\/\-_]+)",

        r"(?:inv\s*(?:no|number|#)"
        r"\s*[:\-]?\s*)"
        r"([A-Z0-9\/\-_]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return match.group(1).strip()

    return None


# ============================================================
# GSTIN
# ============================================================

def extract_gstin(text):

    pattern = (
        r"\b"
        r"\d{2}"
        r"[A-Z]{5}"
        r"\d{4}"
        r"[A-Z]"
        r"\d"
        r"[A-Z0-9]"
        r"\b"
    )

    matches = re.findall(
        pattern,
        text.upper()
    )

    return list(
        dict.fromkeys(matches)
    )


# ============================================================
# DATE
# ============================================================

def extract_dates(text):

    pattern = (
        r"\b(?:"
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
        r"|"
        r"\d{1,2}[/-][A-Za-z]{3,9}[/-]?\d{2,4}"
        r"|"
        r"[A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4}"
        r")\b"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    return list(
        dict.fromkeys(matches)
    )


# ============================================================
# AMOUNTS
# ============================================================

def extract_amounts(text):

    pattern = (
        r"(?:₹|Rs\.?|INR|\$|€|£)\s*"
        r"\d+(?:,\d{3})*(?:\.\d{1,2})?"
    )

    matches = re.findall(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    return list(
        dict.fromkeys(matches)
    )


# ============================================================
# EMAIL
# ============================================================

def extract_emails(text):

    pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}\b"
    )

    matches = re.findall(
        pattern,
        text
    )

    return list(
        dict.fromkeys(matches)
    )


# ============================================================
# PHONE NUMBER
# ============================================================

def extract_phone_numbers(text):

    pattern = (
        r"(?<!\d)"
        r"(?:\+91[\s-]?)?"
        r"[6-9]\d{9}"
        r"(?!\d)"
    )

    matches = re.findall(
        pattern,
        text
    )

    return list(
        dict.fromkeys(matches)
    )


# ============================================================
# INVOICE ENTITY EXTRACTION
# ============================================================

def extract_invoice_entities(text):

    return {

        "invoice_number":
            extract_invoice_number(text),

        "invoice_dates":
            extract_dates(text),

        "gstin":
            extract_gstin(text),

        "amounts":
            extract_amounts(text),

        "emails":
            extract_emails(text),

        "phone_numbers":
            extract_phone_numbers(text)
    }


# ============================================================
# APPLICATION UI
# ============================================================

st.title(
    "📄 Intelligent Document Processing"
)

st.caption(
    "Invoice OCR and Structured Information Extraction"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Document Configuration"
)

document_type = st.sidebar.selectbox(
    "Document Type",
    ["Invoice"]
)


# ============================================================
# UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload an Invoice",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# ============================================================
# PROCESS
# ============================================================

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    image_array = np.frombuffer(
        file_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        st.error(
            "Unable to read the uploaded image."
        )

        st.stop()


    # --------------------------------------------------------
    # Display uploaded image
    # --------------------------------------------------------

    st.subheader(
        "Uploaded Invoice"
    )

    st.image(
        cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        ),
        caption=uploaded_file.name,
        use_container_width=True
    )


    process_button = st.button(
        "🚀 Process Invoice",
        type="primary"
    )


    if process_button:

        with st.spinner(
            "Processing invoice..."
        ):

            # ------------------------------------------------
            # Preprocessing
            # ------------------------------------------------

            processed_image = (
                preprocess_image(image)
            )


            # ------------------------------------------------
            # OCR
            # ------------------------------------------------

            extracted_text = (
                extract_text(
                    processed_image
                )
            )


            # ------------------------------------------------
            # Cleaning
            # ------------------------------------------------

            cleaned_text = (
                clean_text(
                    extracted_text
                )
            )


            # ------------------------------------------------
            # Entity Extraction
            # ------------------------------------------------

            entities = (
                extract_invoice_entities(
                    cleaned_text
                )
            )


        # ====================================================
        # RESULTS
        # ====================================================

        st.success(
            "Invoice processed successfully!"
        )


        # ----------------------------------------------------
        # OCR TEXT
        # ----------------------------------------------------

        st.subheader(
            "🔍 Extracted OCR Text"
        )

        st.text_area(
            "OCR Result",
            extracted_text,
            height=250
        )


        # ----------------------------------------------------
        # STRUCTURED INFORMATION
        # ----------------------------------------------------

        st.subheader(
            "📊 Extracted Invoice Information"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                "**Invoice Number**"
            )

            st.info(
                entities["invoice_number"]
                or "Not detected"
            )


            st.write(
                "**GSTIN**"
            )

            st.info(
                ", ".join(
                    entities["gstin"]
                )
                if entities["gstin"]
                else "Not detected"
            )


            st.write(
                "**Invoice Date(s)**"
            )

            st.info(
                ", ".join(
                    entities["invoice_dates"]
                )
                if entities["invoice_dates"]
                else "Not detected"
            )


        with col2:

            st.write(
                "**Amount(s)**"
            )

            st.info(
                ", ".join(
                    entities["amounts"]
                )
                if entities["amounts"]
                else "Not detected"
            )


            st.write(
                "**Email(s)**"
            )

            st.info(
                ", ".join(
                    entities["emails"]
                )
                if entities["emails"]
                else "Not detected"
            )


            st.write(
                "**Phone Number(s)**"
            )

            st.info(
                ", ".join(
                    entities["phone_numbers"]
                )
                if entities["phone_numbers"]
                else "Not detected"
            )


        # ----------------------------------------------------
        # JSON OUTPUT
        # ----------------------------------------------------

        st.subheader(
            "📦 Structured JSON"
        )

        json_output = json.dumps(
            entities,
            indent=4,
            ensure_ascii=False
        )


        st.code(
            json_output,
            language="json"
        )


        st.download_button(
            label="⬇️ Download JSON",
            data=json_output,
            file_name="invoice_entities.json",
            mime="application/json"
        )
