
import streamlit as st
import cv2
import numpy as np
import easyocr
import re
import json
import time
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Document Processing",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS - MODERN AI DASHBOARD
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background: linear-gradient(
            135deg,
            #f8faff 0%,
            #f3f0ff 50%,
            #eef7ff 100%
        );
    }

    .main {
        padding-top: 1rem;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .main-header {
        background: linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

        color: white;

        padding: 1.5rem 2rem;

        border-radius: 18px;

        margin-bottom: 0.5rem;

        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.20);
    }

    .main-header-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .main-header-subtitle {
        font-size: 1rem;
        margin-top: 0.4rem;
        opacity: 0.9;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #1e1b4b 100%
            );

    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        font-weight: 700;
    }


    /* =====================================================
       DOCUMENT TYPE BADGE
       ===================================================== */

    .document-badge {

        display: inline-block;

        padding: 0.45rem 1rem;

        border-radius: 50px;

        background: linear-gradient(
            135deg,
            #dbeafe,
            #ede9fe
        );

        color: #4338ca;

        font-weight: 700;

        font-size: 0.9rem;

        margin-bottom: 1rem;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    .metric-card {

        padding: 1.2rem;

        border-radius: 16px;

        background: rgba(
            255,
            255,
            255,
            0.90
        );

        border: 1px solid #e5e7eb;

        box-shadow:
            0 6px 20px rgba(
                15,
                23,
                42,
                0.08
            );

        text-align: center;

        min-height: 115px;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .metric-card:hover {

        transform: translateY(
            -4px
        );

        box-shadow:
            0 12px 28px rgba(
                37,
                99,
                235,
                0.15
            );
    }

    .metric-title {

        font-size: 0.82rem;

        color: #64748b;

        font-weight: 600;

        text-transform: uppercase;

        letter-spacing: 0.5px;
    }

    .metric-value {

        font-size: 1.45rem;

        font-weight: 800;

        color: #1e293b;

        margin-top: 0.45rem;
    }


    /* =====================================================
       SECTION HEADERS
       ===================================================== */

    .section-title {

        font-size: 1.25rem;

        font-weight: 800;

        color: #1e293b;

        margin-top: 1rem;

        margin-bottom: 0.8rem;

        border-left:
            5px solid #6366f1;

        padding-left: 0.7rem;
    }


    /* =====================================================
       ENTITY CARDS
       ===================================================== */

    .entity-card {

        border-radius: 14px;

        padding: 1rem;

        margin-bottom: 12px;

        background: white;

        border:
            1px solid #e5e7eb;

        border-left:
            5px solid #6366f1;

        box-shadow:
            0 5px 15px rgba(
                15,
                23,
                42,
                0.06
            );

        transition:
            transform 0.2s ease;
    }

    .entity-card:hover {

        transform:
            translateX(4px);

        border-left-color:
            #2563eb;
    }

    .entity-label {

        font-size: 0.75rem;

        color: #64748b;

        text-transform:
            uppercase;

        font-weight: 700;

        letter-spacing:
            0.5px;
    }

    .entity-value {

        font-size: 1rem;

        color: #111827;

        font-weight: 700;

        margin-top: 5px;
    }


    /* =====================================================
       SUCCESS BOX
       ===================================================== */

    .success-box {

        padding: 1rem 1.2rem;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #ecfdf5,
                #d1fae5
            );

        border:
            1px solid #86efac;

        color: #166534;

        font-weight: 700;

        margin: 1rem 0;
    }


    /* =====================================================
       INFO BOX
       ===================================================== */

    .info-box {

        padding: 1rem 1.2rem;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #eff6ff,
                #dbeafe
            );

        border:
            1px solid #93c5fd;

        color: #1e40af;

        font-weight: 600;
    }


    /* =====================================================
       UPLOAD AREA
       ===================================================== */

    [data-testid="stFileUploader"] {

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #f8faff
            );

        border:
            2px dashed #818cf8;

        border-radius: 16px;

        padding: 1rem;

        box-shadow:
            0 5px 20px rgba(
                99,
                102,
                241,
                0.08
            );
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed
            );

        color: white;

        border: none;

        border-radius: 12px;

        padding:
            0.7rem 1rem;

        font-weight: 700;

        font-size: 1rem;

        box-shadow:
            0 6px 15px rgba(
                79,
                70,
                229,
                0.25
            );

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 10px 25px rgba(
                79,
                70,
                229,
                0.35
            );
    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    .stDownloadButton > button {

        background:
            linear-gradient(
                135deg,
                #059669,
                #10b981
            );

        color: white;

        border: none;

        border-radius: 12px;

        font-weight: 700;

        padding:
            0.7rem 1rem;
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {

        font-weight: 700;

        color: #64748b;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        color: #4f46e5;
    }


    /* =====================================================
       IMAGE CONTAINERS
       ===================================================== */

    [data-testid="stImage"] {

        border-radius: 14px;

        overflow: hidden;

        box-shadow:
            0 6px 20px rgba(
                15,
                23,
                42,
                0.10
            );
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {

        border: none;

        border-top:
            1px solid #e2e8f0;

        margin:
            1.5rem 0;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        text-align: center;

        color: #64748b;

        font-size: 0.85rem;

        padding: 1rem;

        margin-top: 2rem;
    }


    /* =====================================================
       HIDE STREAMLIT DEFAULT ELEMENTS
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

SUPPORTED_TYPES = [
    "Invoice",
    "Resume",
    "ID Card"
]


# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource(show_spinner="Loading OCR model...")
def load_ocr_reader():

    reader = easyocr.Reader(
        ["en"],
        gpu=False,
        verbose=False
    )

    return reader


reader = load_ocr_reader()


# ============================================================
# IMAGE UTILITIES
# ============================================================

def decode_uploaded_image(file_bytes):

    image_array = np.frombuffer(
        file_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    return image


def resize_image(image, max_width=1600):

    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    new_height = int(height * scale)

    resized = cv2.resize(
        image,
        (max_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    return resized


# ============================================================
# DOCUMENT PREPROCESSING
# ============================================================

def preprocess_document(image):

    image = resize_image(
        image,
        max_width=1600
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # CLAHE improves local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Mild denoising
    denoised = cv2.GaussianBlur(
        enhanced,
        (3, 3),
        0
    )

    # Otsu thresholding
    thresholded = cv2.threshold(
        denoised,
        0,
        255,
        cv2.THRESH_BINARY +
        cv2.THRESH_OTSU
    )[1]

    return thresholded


# ============================================================
# OCR
# ============================================================

def perform_ocr(image):

    results = reader.readtext(
        image,
        detail=1,
        paragraph=False
    )

    text_lines = []

    confidence_scores = []

    for result in results:

        if len(result) >= 3:

            text = str(result[1])
            confidence = float(result[2])

            text_lines.append(text)

            confidence_scores.append(
                confidence
            )

    full_text = "\n".join(
        text_lines
    )

    if confidence_scores:

        average_confidence = (
            sum(confidence_scores)
            /
            len(confidence_scores)
        )

    else:

        average_confidence = 0.0

    return {
        "text": full_text,
        "confidence": average_confidence,
        "results": results
    }


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
        r"\n{2,}",
        "\n",
        text
    )

    return text.strip()


# ============================================================
# GENERIC ENTITY EXTRACTION
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
        dict.fromkeys(
            matches
        )
    )


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
        dict.fromkeys(
            matches
        )
    )


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
        dict.fromkeys(
            matches
        )
    )


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
        dict.fromkeys(
            matches
        )
    )


# ============================================================
# INVOICE EXTRACTION
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
        dict.fromkeys(
            matches
        )
    )


def extract_invoice_entities(text):

    return {

        "Invoice Number":
            extract_invoice_number(text),

        "Invoice Date":
            extract_dates(text),

        "GSTIN":
            extract_gstin(text),

        "Amounts":
            extract_amounts(text),

        "Email":
            extract_emails(text),

        "Phone Number":
            extract_phone_numbers(text)
    }


# ============================================================
# RESUME EXTRACTION
# ============================================================

def extract_name_from_resume(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    # Usually the first meaningful line is the candidate name
    if lines:

        candidate = lines[0]

        if (
            len(candidate.split()) <= 5
            and len(candidate) <= 60
        ):

            return candidate

    return None


def extract_skills(text):

    skill_dictionary = [

        "Python",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "Power BI",
        "Excel",
        "Power Query",
        "Tableau",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Streamlit",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Java",
        "C++",
        "C",
        "AWS",
        "Azure",
        "Git",
        "GitHub",
        "SAP",
        "Oracle"
    ]

    found_skills = []

    text_lower = text.lower()

    for skill in skill_dictionary:

        if skill.lower() in text_lower:

            found_skills.append(
                skill
            )

    return found_skills


def extract_resume_entities(text):

    return {

        "Name":
            extract_name_from_resume(text),

        "Email":
            extract_emails(text),

        "Phone Number":
            extract_phone_numbers(text),

        "Skills":
            extract_skills(text),

        "Dates":
            extract_dates(text)
    }


# ============================================================
# ID CARD EXTRACTION
# ============================================================

def extract_aadhaar_numbers(text):

    pattern = (
        r"\b"
        r"\d{4}\s\d{4}\s\d{4}"
        r"\b"
    )

    return list(
        dict.fromkeys(
            re.findall(
                pattern,
                text
            )
        )
    )


def extract_id_card_entities(text):

    return {

        "Name":
            extract_name_from_resume(text),

        "ID Number":
            extract_aadhaar_numbers(text),

        "Date":
            extract_dates(text),

        "Phone Number":
            extract_phone_numbers(text)
    }


# ============================================================
# DOCUMENT ROUTER
# ============================================================

def extract_entities(
    text,
    document_type
):

    if document_type == "Invoice":

        return extract_invoice_entities(
            text
        )

    elif document_type == "Resume":

        return extract_resume_entities(
            text
        )

    elif document_type == "ID Card":

        return extract_id_card_entities(
            text
        )

    return {}


# ============================================================
# DISPLAY HELPERS
# ============================================================

def format_value(value):

    if value is None:

        return "Not detected"

    if isinstance(
        value,
        list
    ):

        if not value:

            return "Not detected"

        return ", ".join(
            str(item)
            for item in value
        )

    return str(value)


def count_detected_entities(entities):

    count = 0

    for value in entities.values():

        if value is None:
            continue

        if isinstance(
            value,
            list
        ):

            if len(value) > 0:

                count += len(value)

        else:

            if str(value).strip():

                count += 1

    return count


def confidence_label(score):

    percentage = score * 100

    if percentage >= 85:

        return "High"

    elif percentage >= 60:

        return "Medium"

    return "Low"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 📄 IDP Dashboard"
    )

    st.markdown(
        "Intelligent Document Processing"
    )

    st.divider()

    document_type = st.selectbox(
        "Document Type",
        SUPPORTED_TYPES
    )

    st.divider()

    st.markdown(
        "### Supported Documents"
    )

    st.write(
        "🧾 Invoice"
    )

    st.write(
        "📄 Resume"
    )

    st.write(
        "🪪 ID Card"
    )

    st.divider()

    st.caption(
        "OCR: EasyOCR"
    )

    st.caption(
        "Processing: OpenCV"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-header">'
    '📄 Intelligent Document Processing'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">'
    'AI-powered OCR and structured information extraction'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOP METRICS
# ============================================================

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">
                Document Type
            </div>
            <div class="metric-value">
                📄
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric2:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">
                OCR Engine
            </div>
            <div class="metric-value">
                EasyOCR
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric3:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">
                Processing
            </div>
            <div class="metric-value">
                AI + OCR
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric4:

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">
                Export
            </div>
            <div class="metric-value">
                JSON
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# UPLOAD SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📤 Upload Document'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    f"Upload {document_type}",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    help=(
        "Upload a clear JPG or PNG document "
        "for better OCR accuracy."
    )
)


# ============================================================
# DOCUMENT PROCESSING
# ============================================================

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    image = decode_uploaded_image(
        file_bytes
    )

    if image is None:

        st.error(
            "Unable to read the uploaded image."
        )

        st.stop()


    # --------------------------------------------------------
    # FILE INFORMATION
    # --------------------------------------------------------

    height, width = image.shape[:2]

    file_size_kb = (
        len(file_bytes) / 1024
    )


    # --------------------------------------------------------
    # PREVIEW
    # --------------------------------------------------------

    preview_col, info_col = st.columns(
        [2, 1]
    )

    with preview_col:

        st.markdown(
            '<div class="section-title">'
            '👁️ Document Preview'
            '</div>',
            unsafe_allow_html=True
        )

        st.image(
            cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            ),
            caption=uploaded_file.name,
            use_container_width=True
        )


    with info_col:

        st.markdown(
            '<div class="section-title">'
            '📋 Document Information'
            '</div>',
            unsafe_allow_html=True
        )

        st.metric(
            "Document Type",
            document_type
        )

        st.metric(
            "Image Width",
            f"{width}px"
        )

        st.metric(
            "Image Height",
            f"{height}px"
        )

        st.metric(
            "File Size",
            f"{file_size_kb:.1f} KB"
        )


    st.divider()


    # --------------------------------------------------------
    # PROCESS BUTTON
    # --------------------------------------------------------

    process = st.button(
        f"🚀 Process {document_type}",
        type="primary",
        use_container_width=True
    )


    if process:

        start_time = time.time()


        progress = st.progress(
            0
        )

        status = st.empty()


        # ====================================================
        # STEP 1 - PREPROCESSING
        # ====================================================

        status.info(
            "Step 1/3 — Preprocessing document..."
        )

        processed_image = (
            preprocess_document(
                image
            )
        )

        progress.progress(
            33
        )


        # ====================================================
        # STEP 2 - OCR
        # ====================================================

        status.info(
            "Step 2/3 — Extracting text with OCR..."
        )

        ocr_output = perform_ocr(
            processed_image
        )

        raw_text = ocr_output[
            "text"
        ]

        ocr_confidence = ocr_output[
            "confidence"
        ]

        progress.progress(
            66
        )


        # ====================================================
        # STEP 3 - ENTITY EXTRACTION
        # ====================================================

        status.info(
            "Step 3/3 — Extracting structured fields..."
        )

        cleaned_text = clean_text(
            raw_text
        )

        entities = extract_entities(
            cleaned_text,
            document_type
        )

        progress.progress(
            100
        )

        processing_time = (
            time.time()
            -
            start_time
        )

        status.success(
            "Document processing completed."
        )


        # ====================================================
        # RESULT METRICS
        # ====================================================

        st.markdown(
            '<div class="section-title">'
            '📊 Processing Summary'
            '</div>',
            unsafe_allow_html=True
        )

        m1, m2, m3, m4 = st.columns(4)

        detected_count = (
            count_detected_entities(
                entities
            )
        )

        confidence_percent = (
            ocr_confidence * 100
        )

        with m1:

            st.metric(
                "OCR Confidence",
                f"{confidence_percent:.1f}%"
            )

        with m2:

            st.metric(
                "Detected Fields",
                detected_count
            )

        with m3:

            st.metric(
                "OCR Text Length",
                len(raw_text)
            )

        with m4:

            st.metric(
                "Processing Time",
                f"{processing_time:.2f}s"
            )


        st.divider()


        # ====================================================
        # TABS
        # ====================================================

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📊 Structured Data",
                "🔍 OCR Text",
                "🖼️ Preprocessed Image",
                "📦 JSON Output"
            ]
        )


        # ====================================================
        # TAB 1 - STRUCTURED DATA
        # ====================================================

        with tab1:

            st.markdown(
                '<div class="section-title">'
                'Extracted Information'
                '</div>',
                unsafe_allow_html=True
            )


            if entities:

                columns = st.columns(2)

                for index, (
                    field,
                    value
                ) in enumerate(
                    entities.items()
                ):

                    column = columns[
                        index % 2
                    ]

                    formatted = (
                        format_value(
                            value
                        )
                    )

                    with column:

                        st.markdown(
                            f"""
                            <div class="entity-card">

                                <div class="entity-label">
                                    {field}
                                </div>

                                <div class="entity-value">
                                    {formatted}
                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.warning(
                    "No structured fields detected."
                )


        # ====================================================
        # TAB 2 - OCR TEXT
        # ====================================================

        with tab2:

            st.markdown(
                '<div class="section-title">'
                'Raw OCR Output'
                '</div>',
                unsafe_allow_html=True
            )

            st.text_area(
                "Extracted Text",
                raw_text,
                height=400,
                label_visibility="collapsed"
            )


            st.markdown(
                '<div class="section-title">'
                'Cleaned Text'
                '</div>',
                unsafe_allow_html=True
            )

            st.text_area(
                "Cleaned Text",
                cleaned_text,
                height=300,
                label_visibility="collapsed"
            )


        # ====================================================
        # TAB 3 - PREPROCESSED IMAGE
        # ====================================================

        with tab3:

            st.markdown(
                '<div class="section-title">'
                'Preprocessed Document'
                '</div>',
                unsafe_allow_html=True
            )

            st.image(
                processed_image,
                caption="Processed image used for OCR",
                use_container_width=True
            )


        # ====================================================
        # TAB 4 - JSON
        # ====================================================

        with tab4:

            st.markdown(
                '<div class="section-title">'
                'Structured JSON'
                '</div>',
                unsafe_allow_html=True
            )


            final_output = {

                "document_type":
                    document_type,

                "file_name":
                    uploaded_file.name,

                "processing_timestamp":
                    datetime.now().isoformat(),

                "ocr_confidence":
                    round(
                        ocr_confidence,
                        4
                    ),

                "processing_time_seconds":
                    round(
                        processing_time,
                        3
                    ),

                "entities":
                    entities,

                "ocr_text":
                    raw_text
            }


            json_output = json.dumps(
                final_output,
                indent=4,
                ensure_ascii=False
            )


            st.code(
                json_output,
                language="json"
            )


            st.download_button(
                label="⬇️ Download Structured JSON",
                data=json_output,
                file_name=(
                    f"{document_type.lower().replace(' ', '_')}"
                    "_results.json"
                ),
                mime="application/json",
                use_container_width=True
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Intelligent Document Processing | "
    "OCR + NLP + Structured Information Extraction"
)
