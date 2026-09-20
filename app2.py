import folium
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
import joblib


# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="MyDecouple AI | Balancing Tourism Footprint Across Malaysia",
    page_icon="🇲🇾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for SDG Badges, Cards, Layout UI, Hero, and Footer
st.markdown("""
<style>

/* =========================================================
   MYDECOUPLE AI — FIXED LIGHT MODE
   ========================================================= */

/* =========================================================
   1. GLOBAL LIGHT MODE
   ========================================================= */

html,
body {
    background-color: #ffffff !important;
    color: #222222 !important;
}

/* Main Streamlit application */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    color: #222222 !important;
}

/* Main content area */
[data-testid="stMain"] {
    background-color: #F7F9FC !important;
    color: #222222 !important;
}

/* Main block */
[data-testid="stMainBlockContainer"] {
    background-color: #F7F9FC !important;
}

/* Streamlit header */
[data-testid="stHeader"] {
    background-color: #ffffff !important;
}

/* Prevent transparent/dark containers */
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    color: #222222;
}


/* =========================================================
   2. SIDEBAR — FIXED LIGHT
   ========================================================= */

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    color: #333333 !important;
}

section[data-testid="stSidebar"] > div {
    background-color: #ffffff !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #333333;
}

/* Sidebar navigation buttons */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;

    border: none !important;
    background-color: transparent !important;

    padding: 12px 15px;
    border-radius: 8px;

    font-size: 15px;
    font-weight: 500;

    color: #333333 !important;

    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #EAF2F8 !important;
    color: #1F77B4 !important;
    border: none !important;
}


/* =========================================================
   3. SIDEBAR BRANDING
   ========================================================= */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 18px 4px;
}

.sidebar-logo {
    width: 52px;
    height: 52px;

    object-fit: contain;
    border-radius: 50%;

    flex-shrink: 0;

    box-shadow: 0 2px 6px rgba(0,0,0,0.15);

    border: 2px solid #E0E0E0;
}

.sidebar-brand-text {
    flex: 1;
    min-width: 0;
}

.sidebar-title {
    font-size: 18px;
    font-weight: 700;

    color: #1F4E79 !important;

    line-height: 1.2;
    white-space: nowrap;
}

.sidebar-subtitle {
    font-size: 10px;

    color: #777777 !important;

    line-height: 1.3;
    margin-top: 4px;
}


/* =========================================================
   4. SIDEBAR INPUTS / SELECTBOXES
   ========================================================= */

/* Selectbox */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #222222 !important;

    border-color: #D1D5DB !important;
}

/* Selectbox text */
section[data-testid="stSidebar"]
div[data-baseweb="select"] span {
    color: #222222 !important;
}

/* Number input */
section[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #222222 !important;

    border-color: #D1D5DB !important;
}

/* Slider labels */
section[data-testid="stSidebar"] [data-testid="stSlider"] {
    color: #222222 !important;
}


/* =========================================================
   5. SDG BADGES
   ========================================================= */

.sdg-badge {
    display: inline-block;

    padding: 4px 12px;
    margin-right: 8px;

    border-radius: 15px;

    font-weight: 600;
    font-size: 0.85rem;

    color: #ffffff !important;
}

.sdg-8 {
    background-color: #A21942;
}

.sdg-12 {
    background-color: #BF8B2E;
}


/* =========================================================
   6. HERO BANNER
   ========================================================= */

.hero-container {
    position: relative;

    border-radius: 12px;

    padding: 40px 32px;
    margin: 10px 0 25px 0;

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    color: #ffffff !important;

    box-shadow: 0 10px 25px rgba(0,0,0,0.15);

    overflow: hidden;
}

.hero-overlay {
    position: absolute;

    top: 0;
    left: 0;
    right: 0;
    bottom: 0;

    background: linear-gradient(
        135deg,
        rgba(0,0,0,0.75) 0%,
        rgba(0,0,0,0.45) 100%
    );

    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;

    color: #ffffff !important;

    margin-top: 15px;
    margin-bottom: 8px;

    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 600;

    color: #60A5FA !important;

    margin-bottom: 20px;
}

.hero-quote {
    background: rgba(255,255,255,0.12);

    backdrop-filter: blur(4px);

    border-left: 4px solid #3B82F6;

    padding: 14px 18px;

    border-radius: 6px;

    font-size: 0.95rem;

    color: #F1F5F9 !important;

    line-height: 1.5;
}


/* =========================================================
   7. GENERAL CARDS
   ========================================================= */

.metric-card {
    background-color: #FFFFFF !important;

    border-left: 5px solid #1F77B4;

    padding: 15px;

    border-radius: 5px;

    margin-bottom: 10px;

    color: #222222 !important;
}

.engine-card {
    background-color: #FFFFFF !important;

    border: 1px solid #E0E0E0;

    border-radius: 8px;

    padding: 20px;

    box-shadow: 0 2px 4px rgba(0,0,0,0.05);

    color: #222222 !important;
}


/* =========================================================
   8. HOME PAGE — FORMAL SECTIONS
   ========================================================= */

.section-label {
    color: #1F77B4 !important;

    font-size: 0.85rem;
    font-weight: 700;

    letter-spacing: 1.5px;

    text-transform: uppercase;

    margin-bottom: 8px;
}

.section-heading {
    font-size: 2rem;
    font-weight: 800;

    color: #1F2937 !important;

    margin-bottom: 12px;
}

.section-text {
    font-size: 1rem;
    line-height: 1.8;

    color: #4B5563 !important;
}

.home-info-card {
    background: #FFFFFF !important;

    border: 1px solid #E5E7EB;

    border-radius: 12px;

    padding: 24px;

    height: 100%;

    box-shadow: 0 3px 12px rgba(0,0,0,0.04);

    color: #222222 !important;
}

.home-info-card h3 {
    color: #1F4E79 !important;

    font-size: 1.15rem;

    margin-bottom: 10px;
}

.home-info-card p {
    color: #4B5563 !important;

    font-size: 0.95rem;

    line-height: 1.7;
}

.challenge-card {
    background: #F8FAFC !important;

    border-radius: 10px;

    padding: 22px;

    border-top: 4px solid #1F77B4;

    height: 100%;

    color: #222222 !important;
}

.challenge-card h4 {
    color: #1F4E79 !important;

    font-size: 1rem;

    margin-bottom: 8px;
}

.challenge-card p {
    color: #6B7280 !important;

    font-size: 0.9rem;

    line-height: 1.6;
}

.solution-box {
    background: linear-gradient(
        135deg,
        #EFF6FF,
        #F8FAFC
    ) !important;

    border: 1px solid #DBEAFE;

    border-radius: 14px;

    padding: 30px;

    margin-top: 10px;

    color: #222222 !important;
}


/* =========================================================
   9. VISION / MISSION
   ========================================================= */

.vision-box,
.mission-box {
    height: 220px;

    padding: 28px;

    border-radius: 12px;

    box-sizing: border-box;

    display: flex;
    flex-direction: column;

    justify-content: center;
}

.vision-box {
    background-color: #1F4E79 !important;
    color: #FFFFFF !important;
}

.mission-box {
    background-color: #F8FAFC !important;

    border: 1px solid #E5E7EB;

    color: #222222 !important;
}

.vision-box h3,
.mission-box h3 {
    margin-top: 0;
    margin-bottom: 15px;

    font-size: 1.25rem;
}

.vision-box p,
.mission-box p {
    margin-bottom: 0;

    line-height: 1.8;

    font-size: 0.95rem;
}

.vision-box h3,
.vision-box p {
    color: #FFFFFF !important;
}

.mission-box h3 {
    color: #1F4E79 !important;
}

.mission-box p {
    color: #4B5563 !important;
}


/* =========================================================
   10. EXPLORE PLATFORM BUTTONS
   ========================================================= */

[data-testid="stMain"] div.stButton > button {
    width: 100%;

    height: 150px;

    background-color: #F8FAFC !important;

    color: #1F4E79 !important;

    border: 1px solid #E5E7EB !important;

    border-radius: 12px;

    font-weight: 600;

    text-align: center;

    transition: all 0.2s ease;

    box-sizing: border-box;
}

[data-testid="stMain"] div.stButton > button:hover {
    background-color: #1F4E79 !important;

    color: #FFFFFF !important;

    border-color: #1F4E79 !important;

    transform: translateY(-3px);

    box-shadow: 0 6px 15px rgba(0,0,0,0.12);
}

[data-testid="stMain"] div.stButton > button p {
    font-size: 1rem !important;

    font-weight: 600 !important;

    margin: 0 !important;

    color: inherit !important;
}


/* =========================================================
   11. STEPS / IMPACT
   ========================================================= */

.step-number {
    background: #1F77B4 !important;

    color: #FFFFFF !important;

    width: 42px;
    height: 42px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    font-weight: 700;

    margin-bottom: 12px;
}

.impact-card {
    background: #FFFFFF !important;

    border: 1px solid #E5E7EB;

    border-radius: 10px;

    padding: 20px;

    text-align: center;

    height: 100%;

    color: #222222 !important;
}

.impact-card h4 {
    color: #1F4E79 !important;

    margin-bottom: 8px;
}

.impact-card p {
    font-size: 0.9rem;

    color: #6B7280 !important;

    line-height: 1.6;
}


/* =========================================================
   12. HOME CTA
   ========================================================= */

.home-cta {
    background: #B9D5EB !important;

    border: 1px solid #84AFD1;

    border-radius: 16px;

    padding: 35px;

    text-align: center;

    margin-top: 20px;

    color: #222222 !important;
}

.home-cta h2 {
    color: #1F4E79 !important;

    font-size: 1.6rem;

    font-weight: 700;

    margin-top: 0;

    margin-bottom: 12px;
}

.home-cta p {
    color: #4B5563 !important;

    font-size: 0.95rem;

    line-height: 1.7;

    max-width: 850px;

    margin: 0 auto;
}


/* =========================================================
   13. OVERVIEW PAGE
   ========================================================= */

.overview-title {
    font-size: 36px;

    font-weight: 800;

    color: #12355B !important;

    margin-bottom: 4px;
}

.overview-subtitle {
    font-size: 15px;

    color: #64748B !important;

    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;

    font-weight: 750;

    color: #12355B !important;

    margin-top: 20px;

    margin-bottom: 15px;
}

.section-description {
    font-size: 14px;

    color: #64748B !important;

    margin-bottom: 18px;
}


/* =========================================================
   14. OVERVIEW KPI CARDS
   ========================================================= */

.metric-card {
    background: #FFFFFF !important;

    border-radius: 16px;

    padding: 22px;

    min-height: 135px;

    border: 1px solid #E2E8F0;

    box-shadow: 0 4px 14px rgba(15,23,42,0.05);

    transition: 0.2s ease;

    color: #222222 !important;
}

.metric-card:hover {
    transform: translateY(-3px);

    box-shadow: 0 8px 20px rgba(15,23,42,0.10);
}

.metric-label {
    font-size: 13px;

    color: #64748B !important;

    font-weight: 600;

    margin-bottom: 10px;
}

.metric-value {
    font-size: 27px;

    font-weight: 800;

    color: #12355B !important;

    line-height: 1.2;
}

.metric-icon {
    font-size: 25px;

    margin-bottom: 8px;
}


/* =========================================================
   15. CHART CARDS
   ========================================================= */

.chart-card {
    background: #FFFFFF !important;

    border-radius: 16px;

    padding: 10px 18px 12px 18px;

    border: 1px solid #E2E8F0;

    box-shadow: 0 3px 12px rgba(15,23,42,0.04);

    color: #222222 !important;
}


/* =========================================================
   16. FILTER BOX
   ========================================================= */

.filter-box {
    background: #EAF2F8 !important;

    border-left: 5px solid #2E86AB;

    border-radius: 12px;

    padding: 15px 20px 5px 20px;

    margin-bottom: 25px;

    color: #222222 !important;
}


/* =========================================================
   17. INFO BANNER
   ========================================================= */

.info-banner {
    background: linear-gradient(
        135deg,
        #12355B,
        #1D6A96
    ) !important;

    color: #FFFFFF !important;

    border-radius: 18px;

    padding: 24px 28px;

    margin-bottom: 28px;
}

.info-banner h3 {
    color: #FFFFFF !important;

    margin-bottom: 8px;
}

.info-banner p {
    color: #E2E8F0 !important;

    margin-bottom: 0;
}


/* =========================================================
   18. POWER BI
   ========================================================= */

.powerbi-container {
    width: 100%;

    margin: 20px 0 30px 0;

    border-radius: 12px;

    overflow: hidden;

    background-color: #F8FAFC !important;

    border: 1px solid #E5E7EB;
}

.powerbi-container iframe {
    width: 100%;

    height: 700px;

    border: none;

    display: block;
}


/* =========================================================
   19. DATASET PREVIEW
   ========================================================= */

.dataset-card {
    background: #FFFFFF !important;

    border-radius: 16px;

    padding: 18px;

    border: 1px solid #E2E8F0;

    color: #222222 !important;
}


/* =========================================================
   20. MANAGEMENT / MEMBERSHIP CARDS
   ========================================================= */

.member-card {
    display: flex;

    align-items: center;

    gap: 28px;

    padding: 24px 16px;

    margin-bottom: 12px;

    background: #FFFFFF !important;

    border-bottom: 1px solid #F0F0F0;

    transition: all 0.3s ease;

    color: #222222 !important;
}

.member-avatar {
    width: 110px;
    height: 110px;

    border-radius: 50%;

    object-fit: cover;

    box-shadow: 0 4px 10px rgba(0,0,0,0.15);

    border: 3px solid #FFFFFF;

    flex-shrink: 0;
}

.member-name {
    font-size: 22px;

    font-weight: 700;

    color: #222222 !important;

    margin-bottom: 4px;
}

.member-role {
    font-size: 13px;

    font-weight: 600;

    color: #7F8C8D !important;

    text-transform: uppercase;

    letter-spacing: 0.8px;

    margin-bottom: 10px;
}

.member-contact {
    font-size: 14px;

    color: #555555 !important;

    line-height: 1.6;
}

.member-contact a {
    color: #1F77B4 !important;

    text-decoration: none;
}

.member-contact a:hover {
    text-decoration: underline;
}


/* =========================================================
   21. OFFICIAL FOOTER
   ========================================================= */

.custom-footer-container {
    margin-top: 50px;

    width: 100%;

    border-radius: 8px;

    overflow: hidden;

    box-sizing: border-box;
}

.custom-footer-top {
    background-color: #333333 !important;

    color: #FFFFFF !important;

    padding: 30px 40px;

    display: flex;

    flex-wrap: wrap;

    justify-content: space-between;

    align-items: center;

    gap: 20px;

    font-family:
        'Segoe UI',
        Tahoma,
        Geneva,
        Verdana,
        sans-serif;
}

.footer-col-logo {
    display: flex;

    align-items: center;

    gap: 15px;
}

.footer-col-logo img {
    width: 60px;
    height: 60px;

    object-fit: contain;

    border-radius: 50%;

    border: 2px solid rgba(255,255,255,0.2);
}

.footer-logo-title {
    font-size: 20px;

    font-weight: 700;

    color: #FFFFFF !important;
}

.footer-logo-sub {
    font-size: 12px;

    color: #AAAAAA !important;
}

.footer-col-address {
    max-width: 300px;

    font-size: 13px;

    line-height: 1.5;

    color: #DDDDDD !important;
}

.footer-col-address strong {
    font-size: 14px;

    color: #FFFFFF !important;

    display: block;

    margin-bottom: 4px;
}

.footer-col-contact {
    font-size: 13px;

    line-height: 1.6;

    color: #DDDDDD !important;
}

.footer-col-contact strong {
    color: #FFFFFF !important;
}

.footer-col-hotline {
    display: flex;

    align-items: center;

    gap: 12px;
}

.hotline-icon {
    font-size: 28px;

    line-height: 1;
}

.hotline-details {
    display: flex;

    flex-direction: column;
}

.hotline-title {
    font-size: 11px;

    font-weight: 700;

    color: #FF5252 !important;

    text-transform: uppercase;
}

.hotline-number {
    font-size: 22px;

    font-weight: 800;

    color: #FF5252 !important;

    line-height: 1.1;
}

.hotline-hours {
    font-size: 10px;

    color: #FF8A8A !important;
}

.custom-footer-bottom {
    background-color: #1A1A1A !important;

    color: #888888 !important;

    text-align: center;

    padding: 15px 20px;

    font-size: 12px;

    border-top: 1px solid #2A2A2A;
}

.custom-footer-bottom a {
    color: #CCCCCC !important;

    text-decoration: none;

    margin: 0 8px;
}

.custom-footer-bottom a:hover {
    color: #FFFFFF !important;

    text-decoration: underline;
}


/* =========================================================
   22. DIVIDER
   ========================================================= */

hr {
    border: none;

    border-top: 1px solid #E2E8F0;

    margin: 35px 0;
}


/* =========================================================
   23. STREAMLIT NATIVE TEXT INPUTS
   ========================================================= */

[data-testid="stMain"] input,
[data-testid="stMain"] textarea {
    background-color: #FFFFFF !important;

    color: #222222 !important;

    border-color: #D1D5DB !important;
}


/* =========================================================
   24. STREAMLIT NATIVE SELECTBOX
   ========================================================= */

[data-testid="stMain"] div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;

    color: #222222 !important;

    border-color: #D1D5DB !important;
}

[data-testid="stMain"] div[data-baseweb="select"] span {
    color: #222222 !important;
}


/* =========================================================
   25. STREAMLIT NATIVE NUMBER INPUT
   ========================================================= */

[data-testid="stMain"] [data-testid="stNumberInput"] input {
    background-color: #FFFFFF !important;

    color: #222222 !important;
}


/* =========================================================
   26. STREAMLIT EXPANDER
   ========================================================= */

[data-testid="stExpander"] {
    background-color: #FFFFFF !important;

    border: 1px solid #E2E8F0 !important;

    color: #222222 !important;
}

[data-testid="stExpander"] summary {
    color: #222222 !important;
}


/* =========================================================
   27. STREAMLIT DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}


/* =========================================================
   28. MOBILE RESPONSIVE
   ========================================================= */

@media (max-width: 768px) {

    .hero-container {
        padding: 30px 20px;
    }

    .hero-title {
        font-size: 1.8rem;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .member-card {
        flex-direction: column;

        align-items: flex-start;

        gap: 15px;
    }

    .custom-footer-top {
        padding: 25px 20px;

        flex-direction: column;

        align-items: flex-start;
    }

}

/* =========================================================
   END — FIXED LIGHT MODE
   ========================================================= */

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Shared Data Loaders
# ---------------------------------------------------------
# Tourism Dataset
TOURISM_FILE = "TOURISM DATASET.xlsx"


POI_FILE = "POI_WEBSITE_CLEANED.xlsx"
# ML DATA

ML_FILE = "ML Full Dataset.xlsx"
SHAP_GLOBAL_FILE = "SHAP GLOBAL.xlsx"
SHAP_STATE_FILE = "SHAP STATE.xlsx"

ML_FEATURES = {
    "X1": "X1_interstate transit hub density",
    "X2": "X2_Top5 Digital Polarization Index (HHI)",
    "X3": "X3_Yearly_Average_Score_by_State",
    "X4": "X4_Accommodation_Capacity_Density",
    "X5": "X5_GDP per Capita"
}

TARGET = "Y_Tourist Density"

# ============================================================
# TRAINED ML MODEL
# ============================================================

MODEL_FILE = "champion_gbr.joblib"

@st.cache_resource
def load_gbr_model():
    return joblib.load(MODEL_FILE)

gbr_model = load_gbr_model()

STATE_MAPPING = {
    "Kuala Lumpur": "Kuala Lumpur",
    "W.P. Kuala Lumpur": "Kuala Lumpur",
    "WP Kuala Lumpur": "Kuala Lumpur",
    "W.P. KL": "Kuala Lumpur",
    "KL": "Kuala Lumpur",

    "Putrajaya": "Putrajaya",
    "W.P. Putrajaya": "Putrajaya",
    "WP Putrajaya": "Putrajaya",

    "W.P. Labuan": "Labuan",

    "Penang": "Penang",
    "Pulau Pinang": "Penang",

    "Malacca": "Melaka",
    "Melaka": "Melaka",

    "Johor": "Johor",
    "Kedah": "Kedah",
    "Kelantan": "Kelantan",
    "Negeri Sembilan": "Negeri Sembilan",
    "Pahang": "Pahang",
    "Perak": "Perak",
    "Perlis": "Perlis",
    "Sabah": "Sabah",
    "Sarawak": "Sarawak",
    "Selangor": "Selangor",
    "Terengganu": "Terengganu",
}

def standardize_state(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # Direct matching
    if value in STATE_MAPPING:
        return STATE_MAPPING[value]

    # Case-insensitive matching
    for original, standard in STATE_MAPPING.items():
        if value.lower() == original.lower():
            return standard

    # Return original if no mapping is needed
    return value

# ============================================================
# Tourism Dataset
# ============================================================
@st.cache_data
def load_tourism_data():
    excel_file = pd.ExcelFile(TOURISM_FILE)

    tourism_data = {
        sheet: pd.read_excel(TOURISM_FILE, sheet_name=sheet)
        for sheet in excel_file.sheet_names
    }

    return tourism_data
tourism_data = load_tourism_data()

# ============================================================
# ML DATA
# ============================================================

@st.cache_data
def load_ml_data():

    df = pd.read_excel(ML_FILE)

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Clean state names
    if "State" in df.columns:
        df["State"] = (
            df["State"]
            .astype(str)
            .str.strip()
        )

    # Clean numeric columns
    numeric_cols = [
        "Year",
        "Area",
        "Domestic Visitor('000)",
        "Domestic Visitor",
        "Y_Tourist Density",
        "Airport count",
        "ktmb station",
        "Count of Bus station",
        "Total public transport station",
        "X1_Interstate transit hub density",
        "X2_Top5 Digital Polarization Index (HHI)",
        "X3_Yearly_Average_Score_by_State",
        "No of hotel room",
        "No of homestay",
        "Total number of accommodation",
        "X4_Accommodation_Capacity_Density",
        "GDP_by_State (RM Million)",
        "population",
        "X5_GDP_per_Capita"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df_ml = load_ml_data()
df_ml["State"] = df_ml["State"].apply(
    standardize_state
)

# ============================================================
# POLICY SIMULATOR MODEL DATA
# ============================================================

TRAIN_FILE = "train_2018_2022.csv"
TEST_FILE = "test_2023_2025.csv"


@st.cache_data
def load_policy_model_data():

    train = pd.read_csv(TRAIN_FILE)
    test = pd.read_csv(TEST_FILE)

    df = pd.concat(
        [train, test],
        ignore_index=True
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "state" in df.columns:

        df["state"] = (
            df["state"]
            .astype(str)
            .str.strip()
        )

        df["state_std"] = (
            df["state"]
            .apply(standardize_state)
        )

    if "year" in df.columns:

        df["year"] = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

    policy_features = [
        "x1_transit_density_log",
        "x2_digital_index",
        "x3_state_score",
        "x4_accommodation_density_log",
        "x5_gdp_per_capita_log",
        "y_tourist_density"
    ]

    for col in policy_features:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df_policy_model = load_policy_model_data()

@st.cache_data
def load_shap_global():

    shap_df = pd.read_excel(SHAP_GLOBAL_FILE)

    shap_df.columns = (
        shap_df.columns
        .astype(str)
        .str.strip()
    )

    return shap_df


df_shap_global = load_shap_global()

# ============================================================
# SHAP STATE DATA
# ============================================================

@st.cache_data
def load_shap_state():

    shap_df = pd.read_excel(SHAP_STATE_FILE)

    shap_df.columns = (
        shap_df.columns
        .astype(str)
        .str.strip()
    )

    # Standardize state names
    if "state" in shap_df.columns:
        shap_df["state_std"] = (
            shap_df["state"]
            .apply(standardize_state)
        )

    # Clean year
    if "year" in shap_df.columns:
        shap_df["year"] = pd.to_numeric(
            shap_df["year"],
            errors="coerce"
        )

    # Clean numeric SHAP / prediction columns
    numeric_cols = [
        "actual_tourist_density_real",
        "predicted_tourist_density_real",
        "national_baseline_real",
        "X1_transit_impact_real",
        "X2_digital_impact_real",
        "X3_score_impact_real",
        "X4_accommodation_impact_real",
        "X5_gdp_impact_real"
    ]

    for col in numeric_cols:

        if col in shap_df.columns:

            shap_df[col] = pd.to_numeric(
                shap_df[col],
                errors="coerce"
            )

    return shap_df


df_shap_state = load_shap_state()


@st.cache_data
def load_poi_data():

    df = pd.read_excel(POI_FILE)

    # -----------------------------------------------------
    # Basic cleaning
    # -----------------------------------------------------

    df = df.dropna(
        subset=["name", "latitude", "longitude"]
    ).copy()

    # Text cleaning
    for col in [
        "name",
        "category",
        "subtypes",
        "type",
        "city",
        "state_std",
        "business_status"
    ]:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # Numeric columns
    for col in [
        "latitude",
        "longitude",
        "rating",
        "reviews",
        "photos_count",
        "digital_visibility_score"
    ]:
        if col in df.columns:
            df[col] = (
                df[col]
                    .astype(str)
                    .str.strip()
                    .str.replace(",", "", regex=False))
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # -----------------------------------------------------
    # Create Tourism Theme
    # -----------------------------------------------------

    def assign_theme(row):

        text = " ".join([
            str(row.get("category", "")),
            str(row.get("subtypes", "")),
            str(row.get("type", "")),
            str(row.get("name", ""))
        ]).lower()

        # Theme Park
        if any(x in text for x in [
            "theme park",
            "water park",
            "amusement",
            "adventure park"
        ]):
            return "Theme Park"

        # Historical
        if any(x in text for x in [
            "museum",
            "historical",
            "heritage",
            "monument",
            "fort",
            "historic",
            "memorial"
        ]):
            return "Historical"

        # Nature
        if any(x in text for x in [
            "zoo",
            "park",
            "nature",
            "forest",
            "waterfall",
            "beach",
            "island",
            "botanical",
            "garden",
            "wildlife",
            "national park"
        ]):
            return "Nature"

        # Shopping
        if any(x in text for x in [
            "shopping",
            "mall",
            "market",
            "outlet",
            "bazaar"
        ]):
            return "Shopping"

        # Culture
        if any(x in text for x in [
            "culture",
            "cultural",
            "temple",
            "mosque",
            "church",
            "shrine",
            "gallery",
            "art"
        ]):
            return "Culture"

        return "Other"

    df["Theme"] = df.apply(assign_theme, axis=1)

    return df


df_poi = load_poi_data()
df_poi["state_std"]=(df_poi["state_std"].apply(standardize_state))

# ---------------------------------------------------------
# 3. Dynamic Logo Load & Sidebar
# ---------------------------------------------------------
logo_filename = None
for fname in ["logo.png", "logo.jpg", "LOGO.jpg", "LOGO.PNG", "logo.jpeg"]:
    if os.path.exists(fname):
        logo_filename = fname
        break

if logo_filename:
    with open(logo_filename, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()
    mime_type = "image/png" if logo_filename.endswith(".png") else "image/jpeg"
    logo_src = f"data:{mime_type};base64,{logo_base64}"
else:
    logo_src = "https://via.placeholder.com/50?text=ML"

st.sidebar.markdown(
    f"""
    <div class="sidebar-brand">
        <img src="{logo_src}" class="sidebar-logo">
        <div class="sidebar-brand-text">
            <div class="sidebar-title">MyDecouple AI</div>
            <div class="sidebar-subtitle">Smart Tourism Intelligence Platform</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

if "app_mode" not in st.session_state:
    st.session_state.app_mode = "HOME"

# 替换 use_container_width 为 width="stretch"
if st.sidebar.button("HOME", width="stretch"):
    st.session_state.app_mode = "HOME"

if st.sidebar.button("OVERVIEW", width="stretch"):
    st.session_state.app_mode = "OVERVIEW"

if st.sidebar.button("🔥SMART TRIP PLANNER", width="stretch"):
    st.session_state.app_mode = "🔥SMART TRIP PLANNER"

if st.sidebar.button(" WHAT-IF SCENARIO", width="stretch"):
    st.session_state.app_mode = " WHAT-IF SCENARIO"

if st.sidebar.button("ABOUT", width="stretch"):
    st.session_state.app_mode = "ABOUT"

app_mode = st.session_state.app_mode
st.sidebar.markdown("---")
st.sidebar.info("💡 **Data Scope:** The data presented on this platform are derived from official Malaysian government sources and authoritative public-sector datasets.")

# -----------------------------------------------------------------------------
# Part 1: Home Page
# -----------------------------------------------------------------------------
if app_mode == "HOME":
    bg_path = "home_bg.jpg"
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as f:
            bg_base64 = base64.b64encode(f.read()).decode()
        ext = bg_path.split('.')[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        hero_bg_style = f"background-image: url('data:{mime};base64,{bg_base64}');"
    else:
        hero_bg_style = "background-image: url('https://images.unsplash.com/photo-1596422846543-75c6fc197f07?q=80&w=1600&auto=format&fit=crop');"

    st.markdown(f"""
    <div class="hero-container" style="{hero_bg_style}">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div>
                <span class="sdg-badge sdg-8">SDG 8: Decent Work & Economic Growth</span>
                <span class="sdg-badge sdg-12">SDG 12: Responsible Consumption</span>
            </div>
            <div class="hero-title">Leveraging AI Recommender Systems and Spatial Analytics </div>
            <div class="hero-subtitle">To Reduce Tourism Concentration in Malaysia</div>
            <div class="hero-quote">
                How can Malaysia achieve tourism growth without concentrating too much tourism in the same destinations?
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    # =====================================================
    # 1. ABOUT MALAYSIA TOURISM
    # =====================================================

    col_text, col_stats = st.columns([2, 1])
    with col_text:
        st.markdown(
            '<div class="section-label">01 — About Malaysia Tourism</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-heading">Welcome to Malaysia</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <p class="section-text">
            Malaysia is a multicultural nation that blends the traditions and cultures of Malay, Chinese, Indian, and various indigenous communities. Its rich cultural heritage, tropical rainforests, islands and beaches, and vibrant cities offer visitors a diverse range of travel experiences.
            </p>
            <p class="section-text">
            Malaysia is also a culinary paradise, bringing together the unique flavors and cuisines of its various ethnic groups. Beyond exploring its multicultural landscape and natural scenery, visitors can venture into Sabah and Sarawak to experience the cultures of indigenous peoples such as the Kadazan-Dusun and the Iban.
            </p>
            """,
            unsafe_allow_html=True
        )
    with col_stats:
        # =================================================
        # TOURISM IMAGE SLIDESHOW
        # =================================================
        images = [
            "Melaka.jpeg",
            "Sabah Kundasang.jpeg",
            "port dickson.jpeg",
            "penang-hill.jpg",
            "mosque.jpeg"
        ]
        slides_html = ""
        for i, img_path in enumerate(images):
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    img_base64 = base64.b64encode(f.read()).decode()
                    ext = img_path.split(".")[-1].lower()
                if ext in ["jpg", "jpeg"]:
                    mime = "image/jpeg"
                elif ext == "png":
                    mime = "image/png"
                else:
                    mime = "image/jpeg"
                slides_html += f"""
                <img
                    class="tourism-slide slide-{i}"
                    src="data:{mime};base64,{img_base64}"
                >
                """ 
            else:
                st.warning(f"Image not found: {img_path}")
        # =================================================
        # DISPLAY SLIDESHOW
        # =================================================
        if slides_html:
            st.markdown(
                f"""
                <style>
                .tourism-slideshow {{
                    position: relative;
                    width: 100%;
                    aspect-ratio: 16 / 10;
                    overflow: hidden;
                    border-radius: 18px;
                    margin-top: 10px;
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
                }}
                .tourism-slide {{
                    position: absolute;
                    inset: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    border-radius: 18px;
                    opacity: 0;
                    animation: tourismFade 15s infinite;
                }}
                .slide-0 {{
                    animation-delay: 0s;
                }}
                .slide-1 {{
                    animation-delay: 3s;
                }}
                .slide-2 {{
                    animation-delay: 6s;
                }}
                .slide-3 {{
                    animation-delay: 9s;
                }}
                .slide-4 {{
                    animation-delay: 12s;
                }}
                @keyframes tourismFade {{
                    0% {{
                        opacity: 0;
                    }}
                    6% {{
                        opacity: 1;
                    }}
                    20% {{
                        opacity: 1;
                    }}
                    26% {{
                        opacity: 0;
                    }}
                    100% {{
                        opacity: 0;
                    }}
                }}
                </style>
                <div class="tourism-slideshow">
                    {slides_html}
                </div>
                """,
                unsafe_allow_html=True
            )
    # =====================================================
    # 2. WHAT IS MYDECOUPLE AI?
    # =====================================================

    st.markdown(
        '<div class="section-label">02 — Our Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">What Is MyDecouple AI?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="solution-box">
            <p class="section-text">
            <p>MyDecouple AI is an AI-powered Sustainable Tourism Intelligence Platform designed to support more balanced tourism development across Malaysia.</p>
            <p>The platform integrates tourism, economic, environmental, social,and mobility-related data to identify tourism patterns, understand destination pressure, and generate actionable insights for different stakeholders.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.divider()

    # =====================================================
    # 3. VISION AND MISSION
    # =====================================================

    st.markdown(
        '<div class="section-label">03 — Our Direction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Our Vision & Mission</div>',
        unsafe_allow_html=True
    )

    vision_col, mission_col = st.columns(2)

    with vision_col:
        st.markdown(
            """
            <div class="vision-box">
                <h3>Our Vision</h3>
                <p>
                To create a smarter, more balanced, and sustainable tourism ecosystem across Malaysia.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mission_col:
        st.markdown(
            """
            <div class="mission-box">
                <h3>Our Mission</h3>
                <p>
                To leverage data, artificial intelligence, and tourism intelligence to support responsible travel, distribute tourism benefits more evenly, and empower stakeholders to make informed decisions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # =====================================================
    # 4. EXPLORE THE PLATFORM
    # =====================================================

    st.markdown(
        '<div class="section-label">04 — Explore MyDecouple AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-heading">Explore the Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="section-text">
        Discover tourism insights, explore smarter travel options, and understand how data and artificial intelligence can support a more sustainable tourism future for Malaysia.
        </p>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # EXPLORE PLATFORM
    # =========================================================

    p1, p2, p3 = st.columns(3)

    # =========================================================
    # TOURISM OVERVIEW
    # =========================================================
    with p1:
        if st.button(
            "Tourism Overview",
            key="btn_title_overview",
            width="stretch"
        ):
            st.session_state.app_mode = "OVERVIEW"
            st.rerun()

        st.markdown(
            """
            <p style="
                font-size: 0.9rem;
                color: #666;
                text-align: center;
                margin-top: 12px;
            ">
            Explore tourism trends, destination patterns, and spatial tourism diagnostics across Malaysia.
            </p>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # SMART TRIP PLANNER
    # =========================================================
    with p2:
        if st.button(
            "Smart Trip Planner",
            key="btn_title_planner",
            width="stretch"
        ):
            st.session_state.app_mode = "🔥SMART TRIP PLANNER"
            st.rerun()

        st.markdown(
            """
            <p style="
                font-size: 0.9rem;
                color: #666;
                text-align: center;
                margin-top: 12px;
            ">
            Discover personalized travel recommendations and alternative destinations based on your preferences.
            </p>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # WHAT-IF SCENARIO
    # =========================================================
    with p3:
        if st.button(
            "What-If Scenario",
            key="btn_title_simulator",
            width="stretch"
        ):
            st.session_state.app_mode = " WHAT-IF SCENARIO"
            st.rerun()

        st.markdown(
            """
            <p style="
                font-size: 0.9rem;
                color: #666;
                text-align: center;
                margin-top: 12px;
            ">
            Explore tourism policy scenarios and their potential impact on destination distribution and sustainability.
            </p>
            """,
            unsafe_allow_html=True
        )

    
    st.markdown("---")
    st.markdown(
        """
        <div class="home-cta">
            <h2>Building a Smarter Tourism Future for Malaysia</h2>
            <p>MyDecouple AI connects data, artificial intelligence, and sustainable tourism intelligence to support better decisions for travelers, communities, and policymakers.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

# -----------------------------------------------------------------------------
# Part 2: Overview Page
# -----------------------------------------------------------------------------
elif app_mode == "OVERVIEW":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        "<h1 style='text-align:center;'>Tourism Overview</h1>",
        unsafe_allow_html=True
        )
    st.markdown(
        """
        <p style='text-align:center; font-size:17px;'>
        Explore Malaysia's domestic tourism activity,
        visitor behaviour, tourism receipts, destinations
        and accommodation distribution.
        </p>
        """,
        unsafe_allow_html=True)

    # -----------------------------------------------------
    # LOAD DATASETS
    # -----------------------------------------------------

    hotel_rating = tourism_data.get(
        "Hotel Rating", pd.DataFrame()
    )

    hotel_type = tourism_data.get(
        "Hotel Type", pd.DataFrame()
    )

    transportation = tourism_data.get(
        "Transportation", pd.DataFrame()
    )

    accommodation = tourism_data.get(
        "Accommodation", pd.DataFrame()
    )

    top_destination = tourism_data.get(
        "Top 5 Destination", pd.DataFrame()
    )

    tourism_purpose = tourism_data.get(
        "Tourism Purpose", pd.DataFrame()
    )

    receipt = tourism_data.get(
        "Receipt", pd.DataFrame()
    )

    domestic_visitor = tourism_data.get(
        "Domestic Visitor", pd.DataFrame()
    )

    domestic_trip = tourism_data.get(
        "Domestic Trip", pd.DataFrame()
    )


    # -----------------------------------------------------
    # STANDARDISE COLUMN NAMES
    # -----------------------------------------------------

    def clean_columns(df):

        df = df.copy()

        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        return df


    hotel_rating = clean_columns(hotel_rating)
    hotel_type = clean_columns(hotel_type)
    transportation = clean_columns(transportation)
    accommodation = clean_columns(accommodation)
    top_destination = clean_columns(top_destination)
    tourism_purpose = clean_columns(tourism_purpose)
    receipt = clean_columns(receipt)
    domestic_visitor = clean_columns(domestic_visitor)
    domestic_trip = clean_columns(domestic_trip)


    # -----------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------

    def find_column(df, keywords):

        if df.empty:
            return None

        for col in df.columns:

            col_clean = str(col).lower().strip()

            for keyword in keywords:

                if keyword.lower() in col_clean:
                    return col

        return None


    def format_number(value):
        try:
            if pd.isna(value):
                return "0"
            value = str(value).replace(",", "").strip()
            value = pd.to_numeric(value, errors="coerce")

            if pd.isna(value):
                return "0"

            return f"{float(value):,.2f}"
        except (ValueError, TypeError):
            return "0"


    def apply_chart_style(fig):

        fig.update_layout(
            template="plotly_white",
            font=dict(
                family="Arial",
                size=13,
                color="#334155"
            ),
            title_font=dict(
                size=17,
                color="#12355B"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=40,
                r=25,
                t=55,
                b=45
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            )
        )

        fig.update_xaxes(
            showgrid=False,
            linecolor="#CBD5E1"
        )

        fig.update_yaxes(
            gridcolor="#E2E8F0",
            zeroline=False
        )

        return fig


    # -----------------------------------------------------
    # PREPARE COLUMNS
    # -----------------------------------------------------

    visitor_year = find_column(
        domestic_visitor,
        ["year"]
    )

    visitor_state = find_column(
        domestic_visitor,
        ["state"]
    )

    visitor_type = find_column(
        domestic_visitor,
        ["type"]
    )

    visitor_value = find_column(
        domestic_visitor,
        ["number", "visitor"]
    )


    trip_year = find_column(
        domestic_trip,
        ["year"]
    )

    trip_state = find_column(
        domestic_trip,
        ["state"]
    )

    trip_type = find_column(
        domestic_trip,
        ["type"]
    )

    trip_value = find_column(
        domestic_trip,
        ["number", "trip"]
    )


    receipt_year = find_column(
        receipt,
        ["year"]
    )

    receipt_state = find_column(
        receipt,
        ["state"]
    )

    receipt_type = "Type of Receipts"

    receipt_value = "Receipts"


    purpose_year = find_column(
        tourism_purpose,
        ["year"]
    )

    purpose_state = find_column(
        tourism_purpose,
        ["state"]
    )

    purpose_visitor_type = find_column(
        tourism_purpose,
        ["type"]
    )

    purpose_category = find_column(
        tourism_purpose,
        ["purpose"]
    )

    purpose_value = find_column(
        tourism_purpose,
        ["percentage"]
    )


    destination_year = find_column(
        top_destination,
        ["year"]
    )

    destination_state = find_column(
        top_destination,
        ["state"]
    )

    destination_type_visitor = find_column(
        top_destination,
        ["type"]
    )

    destination_name = find_column(
        top_destination,
        ["destination"]
    )


    hotel_year = find_column(
        hotel_rating,
        ["year"]
    )

    hotel_state = find_column(
        hotel_rating,
        ["state"]
    )

    hotel_rating_category = find_column(
        hotel_rating,
        ["star rating", "rating", "gred"]
    )

    hotel_number = find_column(
        hotel_rating,
        ["hotel"]
    )

    hotel_room_number = find_column(
        hotel_rating,
        ["room"]
    )

    transport_year = find_column(
        transportation,
        ["year"]
    )

    transport_state = find_column(
        transportation,
        ["state"]
    )

    transport_type = find_column(
        transportation,
        ["type of tourist", "type"]
    )

    transport_category = find_column(
        transportation,
        ["transportation"]
    )

    transport_value = find_column(
        transportation,
        ["percentage", "%"]
    )

    accommodation_year = find_column(
        accommodation,
        ["year"]
    )

    accommodation_state = find_column(
        accommodation,
        ["state"]
    )

    accommodation_category = find_column(
        accommodation,
        ["accommodation"]
    )

    accommodation_value = find_column(
        accommodation,
        ["percentage", "%"]
    )


    # -----------------------------------------------------
    # AVAILABLE YEARS AND STATES
    # -----------------------------------------------------

    all_years = set()

    for df in tourism_data.values():

        year_col = find_column(df, ["year"])

        if year_col:

            years = pd.to_numeric(
                df[year_col],
                errors="coerce"
            ).dropna().astype(int)

            all_years.update(years.tolist())


    all_years = sorted(all_years)


    all_states = set()

    for df in tourism_data.values():

        state_col = find_column(df, ["state"])

        if state_col:

            states = (
                df[state_col]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
            )

            all_states.update(states.tolist())


    all_states = sorted(all_states)


    # -----------------------------------------------------
    # FILTER SECTION
    # -----------------------------------------------------

    st.markdown("""
    <div class="section-title">A. Tourism Data Explorer</div>
    <div class="section-description">
        Select a year and location to explore tourism activity.
    </div>
    """, unsafe_allow_html=True)

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        selected_year = st.selectbox(
            "Select Year",
            ["All Years"] + all_years,
            key="overview_year_filter"
        )

    with filter_col2:

        selected_state = st.selectbox(
            "Select State",
            ["Malaysia"] + all_states,
            key="overview_state_filter"
        )


    # -----------------------------------------------------
    # FILTER FUNCTION
    # -----------------------------------------------------

    def filter_dataframe(
        df,
        year_col=None,
        state_col=None
    ):

        df = df.copy()

        if df.empty:
            return df

        if (
            selected_year != "All Years"
            and year_col
            and year_col in df.columns
        ):

            df = df[
                pd.to_numeric(
                    df[year_col],
                    errors="coerce"
                ) == int(selected_year)
            ]


        if (
            selected_state != "Malaysia"
            and state_col
            and state_col in df.columns
        ):

            df = df[
                df[state_col].astype(str).str.strip()
                == selected_state
            ]

        return df


    # -----------------------------------------------------
    # PREPARE FILTERED DATA
    # -----------------------------------------------------

    visitor_filtered = filter_dataframe(
        domestic_visitor,
        visitor_year,
        visitor_state
    )

    trip_filtered = filter_dataframe(
        domestic_trip,
        trip_year,
        trip_state
    )

    receipt_filtered = filter_dataframe(
        receipt,
        receipt_year,
        receipt_state
    )

    purpose_filtered = filter_dataframe(
        tourism_purpose,
        purpose_year,
        purpose_state
    )

    destination_filtered = filter_dataframe(
        top_destination,
        destination_year,
        destination_state
    )

    hotel_filtered = filter_dataframe(
        hotel_rating,
        hotel_year,
        hotel_state
    )

    transport_filtered = filter_dataframe(
        transportation,
        transport_year,
        transport_state)

    accommodation_filtered = filter_dataframe(
        accommodation,
        accommodation_year,
        accommodation_state
    )
    
    # -----------------------------------------------------
    # SECTION 1: KEY TOURISM INDICATORS
    # -----------------------------------------------------

    st.markdown("""
    <div class="section-title">Key Tourism Indicators</div>
    <div class="section-description">
        A snapshot of Malaysia's domestic tourism activity
        and economic contribution.
    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # 1. TOTAL DOMESTIC VISITORS
    # -----------------------------------------------------

    total_visitors = 0

    if not visitor_filtered.empty and visitor_value:

        visitor_total = visitor_filtered[
            visitor_filtered[visitor_type].astype(str).str.lower()
            == "total"
        ]

        if not visitor_total.empty:

            total_visitors = visitor_total[visitor_value].sum()

        else:

            total_visitors = visitor_filtered[visitor_value].sum()


    # -----------------------------------------------------
    # 2. TOTAL DOMESTIC TRIPS
    # -----------------------------------------------------
    total_trips = 0

    if not trip_filtered.empty and trip_value:

        trip_total = trip_filtered[
            trip_filtered[trip_type].astype(str).str.lower()
            == "total"
        ]

        if not trip_total.empty:

            total_trips = trip_total[trip_value].sum()

        else:

            total_trips = trip_filtered[trip_value].sum()


    # -----------------------------------------------------
    # 3. TOTAL DOMESTIC RECEIPTS
    # -----------------------------------------------------
    total_receipt = 0

    if not receipt_filtered.empty and receipt_value:

        receipt_total = receipt_filtered[
            receipt_filtered["Type of Receipts"].astype(str).str.lower()
            == "total receipts (rm million)"
        ]

        if not receipt_total.empty:
            total_receipt = pd.to_numeric(receipt_total["Receipts"],
                                          errors="coerce"
                                         ).sum()

        else:
            total_receipt = pd.to_numeric(receipt_total["Receipts"],
                                          errors="coerce"
                                         )

    # -----------------------------------------------------
    # 4. SELECTED YEAR
    # -----------------------------------------------------
    selected_year_display = (
            "All Years"
            if selected_year == "All Years"
            else str(selected_year)
        )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-label">Total Domestic Visitors</div>
            <div class="metric-value">
                {format_number(total_visitors)}K
            </div>
        </div>
        """, unsafe_allow_html=True)


    with col2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">✈️</div>
            <div class="metric-label">Total Domestic Trips</div>
            <div class="metric-value">
                {format_number(total_trips)}K
            </div>
        </div>
        """, unsafe_allow_html=True)


    with col3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-label">Total Tourism Receipt</div>
            <div class="metric-value">
                RM {format_number(total_receipt)} million
            </div>
        </div>
        """, unsafe_allow_html=True)


    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📅</div>
            <div class="metric-label">Selected Year</div>
            <div class="metric-value">
                {selected_year_display}
            </div>
        </div>
        """, unsafe_allow_html=True)


    st.divider()

    # =====================================================
    # SECTION 2: DOMESTIC TOURISM DEMAND
    # =====================================================

    st.markdown("""
    <div class="section-title">Domestic Tourism Demand</div>
    <div class="section-description">
        Domestic visitors and domestic tourism trips by visitor category.
    </div>
    """, unsafe_allow_html=True)


    left_col, right_col = st.columns(2)


    # =====================================================
    # DOMESTIC VISITOR TREND
    # =====================================================

    with left_col:

        if not domestic_visitor.empty:

            df = domestic_visitor.copy()

            if selected_state != "Malaysia":

                df = df[
                    df[visitor_state]
                    .astype(str)
                    .str.strip()
                    == selected_state
                ]

            if visitor_year and visitor_type and visitor_value:

                df[visitor_year] = pd.to_numeric(
                    df[visitor_year],
                    errors="coerce"
                )

                df[visitor_value] = pd.to_numeric(
                    df[visitor_value],
                    errors="coerce"
                )

                df = df.dropna(
                    subset=[
                        visitor_year,
                        visitor_value
                    ]
                )

                visitor_pivot = df.pivot_table(
                    index=visitor_year,
                    columns=visitor_type,
                    values=visitor_value,
                    aggfunc="sum"
                ).reset_index()

                visitor_pivot = visitor_pivot.sort_values(
                    visitor_year
                )

                visitor_categories = [
                    col for col in
                    ["Total", "Tourist", "Excursionist"]
                    if col in visitor_pivot.columns
                ]

                if visitor_categories:
                    st.markdown(
                        f"""
                        <div style="
                        font-size: 15px;
                        font-weight: 600;
                        color: #475569;
                        margin-bottom: 8px;
                        ">
                        📍 State: <span style="color:#12355B;
                        ">{selected_state}</span>
                        </div>
                        """,
                        unsafe_allow_html=True)

                    fig_visitors = px.line(
                        visitor_pivot,
                        x=visitor_year,
                        y=visitor_categories,
                        markers=True,
                        title="Domestic Visitor Trend",
                        labels={
                            "variable": ".",
                            "value": "Visitors ('000)"
                        }
                    )

                    fig_visitors = apply_chart_style(
                        fig_visitors
                    )

                    fig_visitors.update_layout(
                        yaxis_title="Visitors ('000)",
                        xaxis_title="Year"
                    )

                    st.plotly_chart(
                        fig_visitors,
                        width="stretch"
                    )

                else:

                    st.info(
                        "No visitor categories available "
                        "for the selected state."
                    )

            else:

                st.info(
                    "Domestic Visitor columns could not "
                    "be identified."
                )

        else:

            st.info(
                "Domestic Visitor data is not available."
            )


    # =====================================================
    # DOMESTIC TRIP TREND
    # =====================================================

    with right_col:

        if not domestic_trip.empty:

            df = domestic_trip.copy()

            if selected_state != "Malaysia":

                df = df[
                    df[trip_state]
                    .astype(str)
                    .str.strip()
                    == selected_state
                ]

            if trip_year and trip_type and trip_value:

                df[trip_year] = pd.to_numeric(
                    df[trip_year],
                    errors="coerce"
                )

                df[trip_value] = pd.to_numeric(
                    df[trip_value],
                    errors="coerce"
                )

                df = df.dropna(
                    subset=[
                        trip_year,
                        trip_value
                    ]
                )

                trip_pivot = df.pivot_table(
                    index=trip_year,
                    columns=trip_type,
                    values=trip_value,
                    aggfunc="sum"
                ).reset_index()

                trip_pivot = trip_pivot.sort_values(
                    trip_year
                )

                trip_categories = [
                    col for col in
                    ["Total", "Same Day", "Overnight"]
                    if col in trip_pivot.columns
                ]

                if trip_categories:

                    st.markdown(
                        f"""
                        <div style="
                        font-size: 15px;
                        font-weight: 600;
                        color: #475569;
                        margin-bottom: 8px;
                        ">
                        📍 State: <span style="color:#12355B;
                        ">{selected_state}</span>
                        </div>
                        """,
                        unsafe_allow_html=True)

                    fig_trips = px.line(
                        trip_pivot,
                        x=trip_year,
                        y=trip_categories,
                        markers=True,
                        title="Domestic Trip Trend",
                        labels={
                            "variable": ".",
                            "value": "Trips ('000)"}
                    )

                    fig_trips = apply_chart_style(
                        fig_trips
                    )

                    fig_trips.update_layout(
                        yaxis_title="Trips ('000)",
                        xaxis_title="Year"
                    )

                    st.plotly_chart(
                        fig_trips,
                        width="stretch"
                    )

                else:

                    st.info(
                        "No trip categories available "
                        "for the selected state."
                    )

            else:

                st.info(
                    "Domestic Trip columns could not "
                    "be identified."
                )

        else:

            st.info(
                "Domestic Trip data is not available."
            )

    # =====================================================
    # SECTION 3: TOURISM RECEIPTS
    # =====================================================

    st.markdown("""
    <div class="section-title">Tourism Receipts</div>
    <div class="section-description">
        Domestic tourism receipts by type of trip.
    </div>
    """, unsafe_allow_html=True)


    if not receipt.empty:

        df = receipt.copy()

        if selected_state != "Malaysia":
            df = df[
                df[receipt_state].astype(str).str.strip()
                == selected_state
            ]

        if receipt_year and receipt_type and receipt_value:

            df[receipt_year] = pd.to_numeric(
                df[receipt_year],
                errors="coerce"
            )

            df[receipt_value] = pd.to_numeric(
                df[receipt_value],
                errors="coerce"
            )

            receipt_pivot = df.pivot_table(
                index=receipt_year,
                columns=receipt_type,
                values=receipt_value,
                aggfunc="sum"
            ).reset_index()

             # -----------------------------------------
             # Sort by Year
             # -----------------------------------------
            receipt_pivot = receipt_pivot.sort_values(
                receipt_year
            )

            receipt_columns = [
                col for col in
                [
                    "Same Day Receipts (RM million)",
                    "Overnight Receipts (RM million)",
                    "Total Receipts (RM million)"
                ]
                if col in receipt_pivot.columns
            ]

            if receipt_columns:
                # -----------------------------------------
                # State Label
                # -----------------------------------------
                st.markdown(
                    f"""
                    <div style="
                    font-size: 15px;
                    font-weight: 600;
                    color: #475569;
                    margin-bottom: 8px;
                    ">
                    📍 State:
                    <span style="color:#12355B;
                    ">
                    {selected_state}
                    </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # -----------------------------------------
                # Receipt Chart
                # -----------------------------------------

                fig_receipt = px.bar(
                    receipt_pivot,
                    x=receipt_year,
                    y=receipt_columns,
                    barmode="group",
                    title="Domestic Tourism Receipt Trend"
                )

                fig_receipt = apply_chart_style(
                    fig_receipt
                )

                fig_receipt.update_layout(
                    xaxis_title="Year",
                    yaxis_title="RM Million",
                    legend_title_text=""
                )

                st.plotly_chart(
                   fig_receipt,
                   width="stretch")


    st.divider()


    # =====================================================
    # SECTION 4: TOURISM PURPOSE
    # =====================================================

    st.markdown("""
    <div class="section-title">B. Tourism Purpose</div>
    <div class="section-description">
        Explore the main purposes of domestic travel among
        domestic visitors and tourists.
    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # 4.1 INDEPENDENT FILTERS
    # -----------------------------------------------------

    if not tourism_purpose.empty:

        # Make sure year column is numeric
        tourism_purpose[purpose_year] = pd.to_numeric(
            tourism_purpose[purpose_year],
            errors="coerce"
        )

        # Clean state names
        tourism_purpose[purpose_state] = (
            tourism_purpose[purpose_state]
            .astype(str)
            .str.strip()
        )

        # -------------------------------------------------
        # Available years
        # -------------------------------------------------

        purpose_years = sorted(
            tourism_purpose[purpose_year]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )

        # -------------------------------------------------
        # Available states
        # -------------------------------------------------

        purpose_states = sorted(
            tourism_purpose[purpose_state]
            .dropna()
            .unique()
            .tolist()
        )

        # -------------------------------------------------
        # Filter layout
        # -------------------------------------------------

        purpose_filter_col1, purpose_filter_col2 = st.columns(2)

        with purpose_filter_col1:

            purpose_selected_year = st.selectbox(
                "Select Year",
                purpose_years,
                key="purpose_year_filter",
                width="stretch"
            )

        with purpose_filter_col2:

            purpose_selected_state = st.selectbox(
                "Select State",
                purpose_states,
                key="purpose_state_filter",
                width="stretch"
            )


        # -------------------------------------------------
        # 4.2 FILTER DATA
        # -------------------------------------------------

        purpose_df = tourism_purpose.copy()

        purpose_df[purpose_year] = pd.to_numeric(
            purpose_df[purpose_year],
            errors="coerce"
        )

        purpose_df[purpose_state] = (
            purpose_df[purpose_state]
            .astype(str)
            .str.strip()
        )

        # Filter selected year
        purpose_df = purpose_df[
            purpose_df[purpose_year]
            == purpose_selected_year
        ]

        # Filter selected state
        purpose_df = purpose_df[
            purpose_df[purpose_state]
            == purpose_selected_state
        ]


        # -------------------------------------------------
        # 4.3 CLEAN PURPOSE DATA
        # -------------------------------------------------

        if not purpose_df.empty:

            purpose_df[purpose_value] = pd.to_numeric(
                purpose_df[purpose_value],
                errors="coerce"
            )

            purpose_df = purpose_df.dropna(
                subset=[purpose_value]
            )

            # Remove unnecessary spaces
            purpose_df[purpose_category] = (
                purpose_df[purpose_category]
                .astype(str)
                .str.strip()
            )

            purpose_df[purpose_visitor_type] = (
                purpose_df[purpose_visitor_type]
                .astype(str)
                .str.strip()
            )


        # -------------------------------------------------
        # 4.4 DISPLAY CURRENT SELECTION
        # -------------------------------------------------

        st.markdown(
            f"""
            <div style="
            margin-top: 10px;
            margin-bottom: 18px;
            padding: 12px 16px;
            background: #F8FAFC;
            border-left: 4px solid #12355B;
            border-radius: 6px;
            font-size: 14px;
            color: #475569;
            ">
            <b>Current View</b>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            Year:
            <span style="
            color:#12355B;
            font-weight:600;
            ">
            {purpose_selected_year}
            </span>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            State:
            <span style="
            color:#12355B;z
                    font-weight:600;
                ">
                    {purpose_selected_state}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 4.5 CHECK DATA
        # -------------------------------------------------

        if purpose_df.empty:

            st.warning(
                f"No tourism purpose data available for "
                f"{purpose_selected_state} in "
                f"{purpose_selected_year}."
            )

        else:

            # -------------------------------------------------
            # 4.6 CREATE TWO DATASETS
            # -------------------------------------------------

            visitor_df = purpose_df[
                purpose_df[purpose_visitor_type]
                .str.lower()
                == "domestic visitor"
            ].copy()

            tourist_df = purpose_df[
                purpose_df[purpose_visitor_type]
                .str.lower()
                == "tourist"
            ].copy()


            # -------------------------------------------------
            # 4.7 CREATE DONUT FUNCTION
            # -------------------------------------------------

            def create_purpose_donut(
                df,
                chart_title
            ):

                if df.empty:

                    return None, None

                # Group by purpose
                purpose_chart_df = (
                    df.groupby(
                        purpose_category,
                        as_index=False
                    )[purpose_value]
                    .sum()
                )

                # Sort descending
                purpose_chart_df = (
                    purpose_chart_df
                    .sort_values(
                        purpose_value,
                        ascending=False
                    )
                )

                # Create donut chart
                fig = px.pie(
                    purpose_chart_df,
                    names=purpose_category,
                    values=purpose_value,
                    hole=0.58,
                    title=chart_title
                )

                # -------------------------------------------------
                # Chart styling
                # -------------------------------------------------

                fig.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Share: %{value:.2f}%"
                        "<extra></extra>"
                    ),
                    marker=dict(
                        line=dict(
                            color="white",
                            width=2
                        )
                    )
                )

                fig.update_layout(
                    template="plotly_white",
                    font=dict(
                        family="Arial",
                        size=12,
                        color="#334155"
                    ),
                    title=dict(
                        text=chart_title,
                        font=dict(
                            size=17,
                            color="#12355B"
                        ),
                        x=0.5,
                        xanchor="center"
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(
                        l=20,
                        r=20,
                        t=60,
                        b=20
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.05,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11)
                    ),
                    showlegend=True
                )

                # Center text
                fig.add_annotation(
                    text=(
                        "<b>100%</b><br>"
                        "<span style='font-size:11px'>"
                        "Total Share"
                        "</span>"
                    ),
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=20,
                        color="#12355B"
                    ),
                    align="center"
                )

                # Apply your existing chart style
                fig = apply_chart_style(fig)

                # Restore donut-specific layout
                fig.update_layout(
                    title=dict(
                        text=chart_title,
                        font=dict(
                            size=17,
                            color="#12355B"
                        ),
                        x=0.5,
                        xanchor="center"
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.05,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11)
                    ),
                    margin=dict(
                        l=20,
                        r=20,
                        t=60,
                        b=80
                    )
                )

                # Largest purpose
                largest_row = (
                    purpose_chart_df
                    .iloc[0]
                )

                largest_purpose = (
                    largest_row[purpose_category]
                )

                largest_percentage = float(
                    largest_row[purpose_value]
                )

                return (
                    fig,
                    (
                        largest_purpose,
                        largest_percentage
                    )
                )


            # -------------------------------------------------
            # 4.8 CREATE CHARTS
            # -------------------------------------------------

            fig_visitor, visitor_insight = (
                create_purpose_donut(
                    visitor_df,
                    "Domestic Visitor"
                )
            )

            fig_tourist, tourist_insight = (
                create_purpose_donut(
                    tourist_df,
                    "Tourist"
                )
            )


            # -------------------------------------------------
            # 4.9 DISPLAY SIDE-BY-SIDE DONUT CHARTS
            # -------------------------------------------------

            chart_col1, chart_col2 = st.columns(
                2,
                gap="large"
            )


            # =================================================
            # DOMESTIC VISITOR
            # =================================================

            with chart_col1:

                st.markdown(
                    """
                    <div style="
                        background:#FFFFFF;
                        border:1px solid #E2E8F0;
                        border-radius:12px;
                        padding:10px 12px 5px 12px;
                        box-shadow:
                            0 2px 8px rgba(15,23,42,0.05);
                    ">
                    """,
                    unsafe_allow_html=True
                )

                if fig_visitor is not None:

                    st.plotly_chart(
                        fig_visitor,
                        width="stretch",
                        config={
                            "displayModeBar": False
                        }
                    )

                    if visitor_insight is not None:

                        visitor_purpose = (
                            visitor_insight[0]
                        )

                        visitor_percentage = (
                            visitor_insight[1]
                        )

                        st.markdown(
                            f"""
                            <div style="
                                margin: 0 8px 12px 8px;
                                padding: 11px 13px;
                                background:#F8FAFC;
                                border-radius:8px;
                                font-size:13px;
                                color:#475569;
                            ">
                                <b style="color:#12355B;">
                                    Main Purpose
                                </b>
                                <br>
                                {visitor_purpose}
                                <b>
                                    ({visitor_percentage:.2f}%)
                                </b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No Domestic Visitor data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # =================================================
            # TOURIST
            # =================================================

            with chart_col2:

                st.markdown(
                    """
                    <div style="
                        background:#FFFFFF;
                        border:1px solid #E2E8F0;
                        border-radius:12px;
                        padding:10px 12px 5px 12px;
                        box-shadow:
                            0 2px 8px rgba(15,23,42,0.05);
                    ">
                    """,
                    unsafe_allow_html=True
                )

                if fig_tourist is not None:

                    st.plotly_chart(
                        fig_tourist,
                        width="stretch",
                        config={
                            "displayModeBar": False
                        }
                    )

                    if tourist_insight is not None:

                        tourist_purpose = (
                            tourist_insight[0]
                        )

                        tourist_percentage = (
                            tourist_insight[1]
                        )

                        st.markdown(
                            f"""
                            <div style="
                                margin: 0 8px 12px 8px;
                                padding: 11px 13px;
                                background:#F8FAFC;
                                border-radius:8px;
                                font-size:13px;
                                color:#475569;
                            ">
                                <b style="color:#12355B;">
                                    Main Purpose
                                </b>
                                <br>
                                {tourist_purpose}
                                <b>
                                    ({tourist_percentage:.2f}%)
                                </b>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No Tourist data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


        # -----------------------------------------------------
        # SECTION DIVIDER
        # -----------------------------------------------------

        st.divider()

    else:

        st.info(
            "Tourism purpose data is not available."
        )


    # =====================================================
    # SECTION 5: TRANSPORTATION
    # =====================================================

    st.markdown("""
    <div class="section-title">C. Transportation</div>
    <div class="section-description">
        Explore how domestic visitors and excursionists travel,
        including the main modes of transport and land
        transportation choices.
    </div>
    """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # 5.1 CHECK DATA
    # -----------------------------------------------------

    if not transportation.empty:

        # -------------------------------------------------
        # CLEAN DATA
        # -------------------------------------------------

        transport_data = transportation.copy()

        # Clean year
        transport_data[transport_year] = pd.to_numeric(
            transport_data[transport_year],
            errors="coerce"
        )

        # Clean state
        transport_data[transport_state] = (
            transport_data[transport_state]
            .astype(str)
            .str.strip()
        )

        # Clean visitor type
        transport_data[transport_type] = (
            transport_data[transport_type]
            .astype(str)
            .str.strip()
        )

        # Clean transportation category
        transport_data[transport_category] = (
            transport_data[transport_category]
            .astype(str)
            .str.strip()
        )

        # Clean percentage
        transport_data[transport_value] = pd.to_numeric(
            transport_data[transport_value],
            errors="coerce"
        )


        # -------------------------------------------------
        # 5.2 AVAILABLE YEARS
        # -------------------------------------------------

        transport_years = sorted(
            transport_data[transport_year]
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )


        # -------------------------------------------------
        # 5.3 AVAILABLE STATES
        # -------------------------------------------------

        transport_states = sorted(
            transport_data[transport_state]
            .dropna()
            .unique()
            .tolist()
        )


        # -------------------------------------------------
        # 5.4 INDEPENDENT FILTERS
        # -------------------------------------------------

        transport_filter_col1, transport_filter_col2 = st.columns(
            2,
            gap="medium"
        )

        with transport_filter_col1:

            transport_selected_year = st.selectbox(
                "Select Year",
                transport_years,
                key="transport_year_filter",
                width="stretch"
            )

        with transport_filter_col2:

            transport_selected_state = st.selectbox(
                "Select State",
                transport_states,
                key="transport_state_filter",
                width="stretch"
            )


        # -------------------------------------------------
        # 5.5 FILTER DATA
        # -------------------------------------------------

        transport_df = transport_data[
            transport_data[transport_year]
            == transport_selected_year
        ].copy()

        transport_df = transport_df[
            transport_df[transport_state]
            == transport_selected_state
        ].copy()


        # -------------------------------------------------
        # 5.6 CURRENT VIEW
        # -------------------------------------------------

        st.markdown(
            f"""
            <div style="
            margin-top: 10px;
            margin-bottom: 18px;
            padding: 12px 16px;
            background: #F8FAFC;
            border-left: 4px solid #12355B;
            border-radius: 6px;
            font-size: 14px;
            color: #475569;
            ">
            <b>Current View</b>
            <span style="margin-left: 18px;">
            Year:
            <b style="color:#12355B;">
            {transport_selected_year}
            </b>
            </span>
            <span style="margin-left: 18px;">
            State:
            <b style="color:#12355B;">
            {transport_selected_state}
            </b>
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 5.7 CHECK FILTERED DATA
        # -------------------------------------------------

        if transport_df.empty:

            st.info(
                f"No transportation data available for "
                f"{transport_selected_state} in "
                f"{transport_selected_year}."
            )

        else:

            # -------------------------------------------------
            # 5.8 SEPARATE VISITOR TYPES
            # -------------------------------------------------

            visitors_transport = transport_df[
                transport_df[transport_type]
                .str.lower()
                == "visitors"
            ].copy()

            excursionist_transport = transport_df[
                transport_df[transport_type]
                .str.lower()
                == "excursionist"
            ].copy()


            # -------------------------------------------------
            # 5.9 MAIN TRANSPORTATION FUNCTION
            # -------------------------------------------------

            def build_main_transport_chart(
                df,
                title,
                chart_key
            ):

                if df.empty:
                    return None

                # Only use main transport modes
                main_modes = [
                    "Air",
                    "Water",
                    "Land"
                ]

                chart_df = df[
                    df[transport_category]
                    .isin(main_modes)
                ].copy()

                if chart_df.empty:
                    return None

                # Remove duplicates if any
                chart_df = (
                    chart_df
                    .groupby(
                        transport_category,
                        as_index=False
                    )[transport_value]
                    .sum()
                )

                # Keep desired order
                chart_df[
                    transport_category
                ] = pd.Categorical(
                    chart_df[transport_category],
                    categories=main_modes,
                    ordered=True
                )

                chart_df = chart_df.sort_values(
                    transport_category
                )

                # Create donut
                fig = px.pie(
                    chart_df,
                    names=transport_category,
                    values=transport_value,
                    hole=0.58
                )

                fig.update_traces(

                    textposition="inside",

                    textinfo="percent",

                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Share: %{value:.2f}%"
                        "<extra></extra>"
                    ),

                    marker=dict(
                        line=dict(
                            color="white",
                            width=2
                        )
                    )
                )

                fig.update_layout(

                    height=380,

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        family="Arial",
                        size=12,
                        color="#334155"
                    ),

                    margin=dict(
                        l=15,
                        r=15,
                        t=25,
                        b=70
                    ),

                    showlegend=True,

                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.05,
                        xanchor="center",
                        x=0.5,
                        font=dict(
                            size=11
                        )
                    )
                )

                fig.add_annotation(

                    x=0.5,
                    y=0.5,

                    text=(
                        "<b>Transport</b><br>"
                        "<span style="
                        "'font-size:11px;color:#64748B;'>"
                        "Mode Share"
                        "</span>"
                    ),

                    showarrow=False,

                    align="center",

                    font=dict(
                        size=16,
                        color="#12355B"
                    )
                )

                return fig


            # -------------------------------------------------
            # 5.10 LAND TRANSPORTATION FUNCTION
            # -------------------------------------------------

            def build_land_transport_chart(
                df,
                title
            ):

                if df.empty:
                    return None, None

                land_modes = [
                    "Private Vehicles",
                    "Bus",
                    "Taxi",
                    "Train"
                ]

                chart_df = df[
                    df[transport_category]
                    .isin(land_modes)
                ].copy()

                if chart_df.empty:
                    return None, None

                chart_df = (
                    chart_df
                    .groupby(
                        transport_category,
                        as_index=False
                    )[transport_value]
                    .sum()
                )

                # Keep desired order
                chart_df[
                    transport_category
                ] = pd.Categorical(
                    chart_df[transport_category],
                    categories=land_modes,
                    ordered=True
                )

                chart_df = chart_df.sort_values(
                    transport_category
                )

                # Create horizontal bar
                fig = px.bar(
                    chart_df,
                    x=transport_value,
                    y=transport_category,
                    orientation="h",
                    text=transport_value
                )

                fig.update_traces(
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Share: %{x:.2f}%"
                        "<extra></extra>"
                    )
                )

                fig.update_layout(

                    height=300,

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        family="Arial",
                        size=12,
                        color="#334155"
                    ),

                    margin=dict(
                        l=20,
                        r=45,
                        t=25,
                        b=40
                    ),

                    xaxis=dict(
                        title="Percentage Share (%)",
                        range=[
                            0,
                            max(
                                100,
                                chart_df[
                                    transport_value
                                ].max() * 1.15
                            )
                        ],
                        showgrid=True,
                        gridcolor="#E2E8F0",
                        zeroline=False
                    ),

                    yaxis=dict(
                        title="",
                        categoryorder="array",
                        categoryarray=land_modes
                    ),

                    showlegend=False
                )

                return fig, chart_df


            # -------------------------------------------------
            # 5.11 BUILD MAIN MODE CHARTS
            # -------------------------------------------------

            visitors_main_fig = build_main_transport_chart(
                visitors_transport,
                "Visitors",
                "transport_visitors_main"
            )

            excursionist_main_fig = build_main_transport_chart(
                excursionist_transport,
                "Excursionist",
                "transport_excursionist_main"
            )


            # -------------------------------------------------
            # 5.12 MAIN TRANSPORTATION TITLE
            # -------------------------------------------------

            st.markdown("""
            <div style="
                margin-top: 8px;
                margin-bottom: 12px;
                font-size: 18px;
                font-weight: 700;
                color: #12355B;
            ">
                Main Transportation Mode
            </div>
            """, unsafe_allow_html=True)


            # -------------------------------------------------
            # 5.13 MAIN TRANSPORTATION CARDS
            # -------------------------------------------------

            main_col1, main_col2 = st.columns(
                2,
                gap="large"
            )


            # =================================================
            # VISITORS MAIN MODE
            # =================================================

            with main_col1:

                st.markdown(
                    """
                    <div style="
                        background:#FFFFFF;
                        border:1px solid #E2E8F0;
                        border-radius:12px;
                        padding:10px 12px;
                        box-shadow:
                            0 2px 8px rgba(15,23,42,0.05);
                    ">
                    """,
                    unsafe_allow_html=True
                )

                if visitors_main_fig is not None:

                    st.plotly_chart(
                        visitors_main_fig,
                        width="stretch",
                        key="transport_visitors_main_chart",
                        on_select="ignore",
                        config={
                            "displayModeBar": False
                        }
                    )

                else:

                    st.info(
                        "No visitor transportation data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # =================================================
            # EXCURSIONIST MAIN MODE
            # =================================================

            with main_col2:

                st.markdown(
                    """
                    <div style="
                        background:#FFFFFF;
                        border:1px solid #E2E8F0;
                        border-radius:12px;
                        padding:10px 12px;
                        box-shadow:
                            0 2px 8px rgba(15,23,42,0.05);
                    ">
                    """,
                    unsafe_allow_html=True
                )

                if excursionist_main_fig is not None:

                    st.plotly_chart(
                        excursionist_main_fig,
                        width="stretch",
                        key="transport_excursionist_main_chart",
                        on_select="ignore",
                        config={
                            "displayModeBar": False
                        }
                    )

                else:

                    st.info(
                        "No excursionist transportation data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # 5.14 LAND TRANSPORTATION
            # -------------------------------------------------

            st.markdown(
                """
                <div style="
                    margin-top: 25px;
                    margin-bottom: 12px;
                    font-size: 18px;
                    font-weight: 700;
                    color: #12355B;
                ">
                    Land Transportation
                </div>

                <div style="
                    margin-bottom: 15px;
                    font-size: 13px;
                    color: #64748B;
                ">
                    Breakdown of land transportation choices
                    among visitors and excursionists.
                </div>
                """,
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # 5.15 BUILD LAND CHARTS
            # -------------------------------------------------

            visitors_land_fig, visitors_land_df = (
                build_land_transport_chart(
                    visitors_transport,
                    "Visitors"
                )
            )

            excursionist_land_fig, excursionist_land_df = (
                build_land_transport_chart(
                    excursionist_transport,
                    "Excursionist"
                )
            )


            # -------------------------------------------------
            # 5.16 LAND TRANSPORTATION CARDS
            # -------------------------------------------------

            land_col1, land_col2 = st.columns(
                2,
                gap="large"
            )


            # =================================================
            # VISITORS LAND TRANSPORT
            # =================================================

            with land_col1:

                st.markdown(
                    """
                    <div style="
                        background:#FFFFFF;
                        border:1px solid #E2E8F0;
                        border-radius:12px;
                        padding:16px 16px 10px 16px;
                        box-shadow:
                            0 2px 8px rgba(15,23,42,0.05);
                    ">

                    <div style="
                        font-size:15px;
                        font-weight:600;
                        color:#12355B;
                        margin-bottom:4px;
                    ">
                        Visitors
                    </div>

                    """,
                    unsafe_allow_html=True
                )

                if visitors_land_fig is not None:

                    st.plotly_chart(
                        visitors_land_fig,
                        width="stretch",
                        key="transport_visitors_land_chart",
                        on_select="ignore",
                        config={
                            "displayModeBar": False
                        }
                    )

                else:

                    st.info(
                        "No land transportation data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # =================================================
            # EXCURSIONIST LAND TRANSPORT
            # =================================================

            with land_col2:

                st.markdown(
                    """
                    <div style="
                    background:#FFFFFF;
                    border:1px solid #E2E8F0;
                    border-radius:12px;
                    padding:16px 16px 10px 16px;
                    box-shadow:
                    0 2px 8px rgba(15,23,42,0.05);
                    ">
                    <div style="
                    font-size:15px;
                    font-weight:600;
                    color:#12355B;
                    margin-bottom:4px;
                    ">
                    Excursionist
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if excursionist_land_fig is not None:

                    st.plotly_chart(
                        excursionist_land_fig,
                        width="stretch",
                        key="transport_excursionist_land_chart",
                        on_select="ignore",
                        config={
                            "displayModeBar": False
                        }
                    )

                else:

                    st.info(
                        "No land transportation data available."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


        # -----------------------------------------------------
        # SECTION DIVIDER
        # -----------------------------------------------------

        st.divider()


    else:

        st.info(
            "Transportation data is not available."
        )

    # =====================================================
    # SECTION 6: TOURISM DESTINATION & HOTEL DISTRIBUTION
    # =====================================================

    st.markdown("""
    <div class="section-title">
        D. Tourism Destination & Hotel Distribution
    </div>

    <div class="section-description">
        Explore Malaysia's top domestic tourism destinations
        and hotel accommodation capacity across states.
    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # MAP COORDINATES
    # =====================================================

    state_coordinates = {

        "Malaysia": [4.2105, 101.9758],

        "Johor": [1.4927, 103.7414],
        "Kedah": [6.1184, 100.3685],
        "Kelantan": [6.1254, 102.2381],
        "Melaka": [2.1896, 102.2501],
        "Negeri Sembilan": [2.7258, 101.9424],
        "Pahang": [3.8126, 103.3256],
        "Penang": [5.4141, 100.3288],
        "Perak": [4.5975, 101.0901],
        "Perlis": [6.4449, 100.2048],
        "Sabah": [5.9788, 116.0753],
        "Sarawak": [1.5533, 110.3592],
        "Selangor": [3.0738, 101.5183],
        "Terengganu": [5.3117, 103.1324],
        "Kuala Lumpur": [3.1390, 101.6869],
        "Putrajaya": [2.9264, 101.6964],
        "Labuan": [5.2831, 115.2308]
    }


    # =====================================================
    # DESTINATION COORDINATES
    # =====================================================

    destination_coordinates = {

        # -------------------------------------------------
        # JOHOR
        # -------------------------------------------------

        "Nusajaya": [1.4620, 103.7644],
        "Kulai": [1.6561, 103.6032],
        "Kulaijaya": [1.6561, 103.6032],
        "Pantai Air Papan": [2.5286, 103.8420],
        "Bandaraya Johor Bahru": [1.4927, 103.7414],
        "Johor Bahru": [1.4927, 103.7414],
        "Pekan Tangkak": [2.2673, 102.5456],
        "Batu Pahat": [1.8548, 102.9325],
        "Kluang": [2.0305, 103.3169],
        "Pulau Besar": [2.1200, 102.3460],
        "Mersing": [2.4312, 103.8405],
        "Muar": [2.0442, 102.5689],
        "Kota Tinggi": [1.7381, 103.8999],
        "Danga Bay": [1.4655, 103.7212],
        "Bandar Indahpura": [1.6467, 103.6067],
        "Desaru": [1.5630, 104.2330],
        "Bazaar Karat JB": [1.4561, 103.7610],
        "Angsana Johor Bahru Mall": [1.5198, 103.7102],
        "Johor Premium Outlet": [1.6126, 103.6117],
        "KSL City": [1.4848, 103.7610],
        "Air Terjun Kota Tinggi": [1.8588, 103.8527],
        "Pantai Tanjung Balau": [1.5910, 104.2450],
        "Telok Gorek": [2.4870, 103.8390],
        "Pantai Minyak Beku": [1.8150, 102.8560],
        "Sedili Besar": [1.7550, 104.1230],
        "Paradigm Mall Johor Bahru": [1.5006, 103.6823],
        "Pantai Desaru": [1.5710, 104.2400],
        "Kota Tinggi Firefly Park": [1.7330, 103.8990],
        "The Mall, Mid Valley Southkey": [1.4785, 103.7390],
        "Batu Pahat Mall": [1.8508, 102.9320],
        "Skyscape @ Menara Jland": [1.4620, 103.7640],
        "Pantai Batu Layar": [1.5630, 104.2300],
        "Legoland Malaysia": [1.4250, 103.6299],
        "Toppen Shopping Centre": [1.4936, 103.7975],
        "Square One Shopping Mall": [1.8490, 102.9320],
        "Air Terjun Gunung Ledang": [2.3710, 102.6250],
        "Adventure Waterpark Desaru Coast": [1.5660, 104.2380],

        # -------------------------------------------------
        # KEDAH
        # -------------------------------------------------

        "Bandar Alor Star": [6.1184, 100.3685],
        "Alor Star": [6.1184, 100.3685],
        "Jitra": [6.2680, 100.4210],
        "Langkawi": [6.3500, 99.8000],
        "Pulau Langkawi": [6.3500, 99.8000],
        "Pantai Merdeka": [5.7100, 100.3800],
        "Pendang": [5.9900, 100.4800],
        "Tanjung Dawai": [5.6200, 100.3800],
        "Bandar Sg. Petani": [5.6470, 100.4870],
        "Kolam Air Panas Ulu Legong": [5.7500, 100.7500],
        "Pantai Murni": [5.6500, 100.3900],
        "Hutan Lipur Lata Lembu": [5.7700, 100.7000],
        "Gunung Jerai": [5.8000, 100.4300],
        "Bandar Amanjaya": [5.6400, 100.5000],
        "Pekan Rabu": [6.1200, 100.3650],
        "Ulu Legong": [5.7500, 100.7500],
        "Menara Alor Setar": [6.1180, 100.3690],
        "Gunung Keriang": [6.1300, 100.3500],
        "Aman Central Mall": [6.1160, 100.3700],
        "Puncak Janing": [5.8500, 100.6500],
        "Makam Mahsuri": [6.3500, 99.8000],
        "Perniagaan Haji Ismail Group": [6.3200, 99.8200],
        "Pantai Cenang": [6.2900, 99.7300],
        "Langkawi Cable Car": [6.3700, 99.6700],
        "Padang Matsirat": [6.3500, 99.7400],
        "Air Terjun Telaga Tujuh": [6.3800, 99.6800],
        "Tasik Dayang Bunting": [6.1900, 99.8200],
        "Panorama Langkawi": [6.3700, 99.6700],
        "Amanjaya Mall": [5.6500, 100.4900],
        "Dataran Lang": [6.3100, 99.8500],
        "Pantai Tanjung Dawai": [5.6200, 100.3800],
        "Underwater World Langkawi": [6.2880, 99.7270],
        "National Art Gallery": [6.1200, 100.3700],

        # -------------------------------------------------
        # KELANTAN
        # -------------------------------------------------

        "Pasar Siti Khadijah": [6.1330, 102.2380],
        "Pasar Malam Wakaf Che Yeh": [6.0700, 102.2200],
        "Kawasan Membeli Belah Bebas Cukai Rantau Panjang": [6.0200, 101.9700],
        "Kawasan Membeli Belah Pengkalan Kubor": [6.2000, 102.1000],
        "Pantai Tok Bali": [5.8700, 102.4000],
        "Bandar Kota Bharu": [6.1254, 102.2381],
        "Wakaf Che Yeh": [6.0700, 102.2200],
        "Rantau Panjang": [6.0200, 101.9700],
        "Pengkalan Kubor": [6.2000, 102.1000],
        "Pantai Cahaya Bulan": [6.1800, 102.2700],
        "Lembah Sireh": [6.1200, 102.2200],
        "Masjid Bandar Pasir Mas": [6.0500, 102.1400],
        "Pantai Irama": [6.1000, 102.4000],
        "AEON Lembah Sireh": [6.1200, 102.2200],
        "KB Mall": [6.1150, 102.2250],
        "AEON Mall Kota Bharu": [6.1200, 102.2200],
        "Bazar Tengku Anis": [6.1300, 102.2400],
        "Zon Bebas Cukai Rantau Panjang": [6.0200, 101.9700],
        "Pantai Melawi": [6.0000, 102.4000],

        # -------------------------------------------------
        # MELAKA
        # -------------------------------------------------

        "Banda Hilir": [2.1944, 102.2491],
        "Klebang": [2.2180, 102.2060],
        "Pantai Puteri": [2.2400, 102.1800],
        "Jonker Street": [2.1944, 102.2489],
        "Jonker Walk": [2.1944, 102.2489],
        "Zoo Melaka & Night Safari": [2.2640, 102.3100],
        "Simpang Ampat": [2.4800, 102.2300],
        "Pantai Emas Klebang": [2.2100, 102.2000],
        "Pantai Pengkalan Balak": [2.3600, 102.1000],
        "Umbai": [2.1500, 102.3400],
        "Melaka International Trade Centre(MITC)": [2.2700, 102.2800],
        "Dataran Pahlawan": [2.1900, 102.2500],
        "Makam Hang Tuah": [2.2700, 102.2000],
        "Melaka River Cruise": [2.1950, 102.2480],
        "Muzium Adat Istadat": [2.2000, 102.2500],
        "Taman Rama-Rama dan Reptilia": [2.2700, 102.3100],
        "Porta De Santiago(A'Famosa)": [2.1920, 102.2500],
        "Pantai Klebang": [2.2100, 102.2000],
        "Mahkota Parade": [2.1900, 102.2500],
        "Dataran Pahlawan Melaka Megamall": [2.1900, 102.2500],
        "Taman Botanikal Melaka": [2.3000, 102.3000],
        "Menara Taming Sari": [2.1900, 102.2500],
        "A'Famosa Resort": [2.4300, 102.2100],
        "Freeport A'Famosa Outlet": [2.4300, 102.2100],

        # -------------------------------------------------
        # NEGERI SEMBILAN
        # -------------------------------------------------

        "Pantai Port Dickson": [2.5220, 101.7950],
        "Port Dickson": [2.5220, 101.7950],
        "Nilai": [2.8200, 101.8000],
        "Rumah Undang Sg. Ujong": [2.7250, 101.9400],
        "Hutam Simpan Sg.Menyala": [2.5700, 101.8700],
        "Kompleks Kraf N.Sembilan": [2.7300, 101.9400],
        "Bandar Seremban 2": [2.6900, 101.9300],
        "Hutan Lipur & Rekreasi Ulu Bendul": [2.7000, 102.0500],
        "Hutan Lipur Gunung Datuk": [2.5800, 102.1800],
        "Bandar Seremban": [2.7258, 101.9424],
        "Kuala Pilah": [2.7400, 102.2500],
        "Tampin": [2.4700, 102.2300],
        "Hutan Lipur Jeram Tengkek": [2.6500, 102.2000],
        "Bandar Gemas": [2.5800, 102.6200],
        "Pedas": [2.6000, 102.0000],
        "Nilai 3 Wholesale Centre": [2.8100, 101.8100],
        "Palm Mall Seremban": [2.7100, 101.9400],
        "Kompleks Sejarah Pengkalan Kempas": [2.6000, 102.4300],
        "Dataran Tampin": [2.4700, 102.2300],
        "Alive 3D Art Gallery": [2.5200, 101.8000],
        "Nilai Square": [2.8100, 101.8000],
        "PD Ostrich Farm": [2.5600, 101.8300],
        "Pantai Teluk Kemang": [2.4800, 101.8000],
        "Muzium Tentera Darat": [2.5200, 101.8000],
        "Rantau Eco Park": [2.5800, 101.9400],
        "City Park Seremban 2": [2.6900, 101.9300],
        "Pantai Cahaya Negeri": [2.5000, 101.7900],
        "Pantai Saujana": [2.5100, 101.7900],
        "Dataran Nilai": [2.8200, 101.8000],
        "Taman Eko-Rimba Ulu Bendul": [2.7000, 102.0500],
        "Taman Eko-Rimba Ulu Datuk": [2.6500, 102.1000],

        # -------------------------------------------------
        # PAHANG
        # -------------------------------------------------

        "Bandar Kuantan": [3.8126, 103.3256],
        "Cameron Highlands": [4.4700, 101.3800],
        "Pantai Telok Chempedak": [3.8100, 103.3700],
        "Genting Highlands": [3.4250, 101.7900],
        "Hutan Lipur Lentang": [3.3500, 101.8700],
        "Pantai Cherating": [4.1300, 103.4000],
        "Tanjung Lumpur": [3.7900, 103.3200],
        "Temerloh": [3.4500, 102.4200],
        "Bukit Panorama": [3.9000, 103.3000],
        "Bukit Gambang Resort City": [3.7200, 103.1200],
        "Genting Premium Outlets": [3.4200, 101.7900],
        "East Cost Mall": [3.8100, 103.3300],
        "Bukit Fraser": [3.7100, 101.7400],
        "Beseraj": [3.8000, 103.3300],
        "Pantai Teluk Cempedek": [3.8100, 103.3700],
        "Janda Baik": [3.3200, 101.8700],
        "Strawberry Farm": [4.4700, 101.3800],
        "Ladang The Boh Sg. Palas": [4.5200, 101.4100],
        "Kuantan City Mall": [3.8100, 103.3300],
        "Kuantan Parade": [3.8100, 103.3300],
        "Dataran Kuantan": [3.8100, 103.3300],

        # -------------------------------------------------
        # PERLIS
        # -------------------------------------------------

        "Padang Besar": [6.6600, 100.3200],
        "Kuala Perlis": [6.4000, 100.1300],
        "Pantai Sg. Berembang": [6.4300, 100.1600],
        "Mata Air Forest Reserve State Park": [6.5000, 100.2500],
        "Hutan Lipur Bukit Air": [6.4500, 100.2500],
        "Bandar Kangar": [6.4449, 100.2048],
        "Kangar": [6.4449, 100.2048],
        "Gua Kelam": [6.5500, 100.2000],
        "Taman Negeri Perlis": [6.5500, 100.2000],
        "Pusat Pelancongan Agro,Bukit Temiang": [6.5000, 100.2500],
        "Taman Ular & Reptilia & Taman Burung": [6.4500, 100.2500],
        "Arked Niaga Padang Besar": [6.6600, 100.3200],
        "Tasik Timah Tasoh": [6.5000, 100.2000],
        "Hutan Lipur Bukit Ayer": [6.4500, 100.2500],
        "Taman Rekreasi Pengkalan Asam": [6.4500, 100.2000],
        "Taman Rekreasi Sungai Jernih": [6.5000, 100.2000],
        "Taman Rekreasi Tasik Melati": [6.4500, 100.2500],
        "Padang Waremart": [6.6600, 100.3200],
        "Medan Ikan Bakar Kuala Perlis": [6.4000, 100.1300],
        "Masjid Al-Hussain": [6.4000, 100.1300],
        "Taman Awam Bukit Lagi": [6.4500, 100.2000],
        "Pantai Peranginan Sg. Berembang": [6.4300, 100.1600],
        "Menara Pandang Wang Kelian": [6.6000, 100.1700],
        "Ladang Nipah Kipli": [6.4500, 100.2500],

        # -------------------------------------------------
        # PERAK
        # -------------------------------------------------

        "Taiping": [4.8500, 100.7400],
        "Bandaraya Ipoh": [4.5975, 101.0901],
        "Ipoh": [4.5975, 101.0901],
        "Pulau Pangkor": [4.2300, 100.5500],
        "Teluk Batik": [4.2000, 100.6000],
        "Kolam Air Panas Sungai Klah": [4.1000, 101.4000],
        "Zoo Taiping": [4.8600, 100.7400],
        "Bukit Merah": [4.7500, 100.6700],
        "Batu Gajah": [4.4700, 101.0400],
        "Taman Tasik Taiping": [4.8600, 100.7300],
        "Teluk Intan": [4.0250, 101.0200],
        "Lumut": [4.2300, 100.6300],
        "Tambun": [4.6300, 101.1600],
        "Taman Rekreasi Gunung Lang": [4.6300, 101.0800],
        "Sungai Klah": [4.1000, 101.4000],
        "Durio Tourism Mardi": [4.6000, 101.1000],
        "Pantai Teluk Nipah": [4.2200, 100.5500],
        "Marina Island": [4.2200, 100.6200],
        "Ipoh Town Hall": [4.5950, 101.0750],
        "Air Terjun Ulu Kinta(Air Terjun Tanjung Rambutan)": [4.6800, 101.1800],
        "Ipoh Parade Shopping Centre": [4.6000, 101.0900],
        "Lost World of Tambun": [4.6200, 101.1500],
        "Lumut Waterfront": [4.2300, 100.6300],
        "Teluk Senangin": [4.2000, 100.5800],
        "Bukit Merah Laketown Resort": [4.7500, 100.6700],
        "Ipoh Night Market": [4.6000, 101.0900],

        # -------------------------------------------------
        # PENANG
        # -------------------------------------------------

        "Bayan Lepas": [5.2970, 100.2700],
        "George Town": [5.4141, 100.3288],
        "Seberang Jaya": [5.4000, 100.4000],
        "Pulau Aman": [5.5500, 100.3500],
        "Balik Pulau": [5.3500, 100.2300],
        "Bukit Bendera": [5.4200, 100.2700],
        "Pantai Batu Ferringhi": [5.4700, 100.2450],
        "Monkey Beach": [5.4700, 100.2000],
        "Padang Kota Lama": [5.4200, 100.3400],
        "Pantai Teluk Bahang": [5.4600, 100.2150],
        "KOMTAR": [5.4140, 100.3290],
        "Batu Kawan": [5.2200, 100.4300],
        "Fort Cornwallis,Padang Kota Lama": [5.4180, 100.3400],
        "Queensbay Mall": [5.3330, 100.3050],
        "Gurney Plaza": [5.4370, 100.3090],
        "Prangin Mall": [5.4120, 100.3290],
        "Pantai Tanjung Bungah": [5.4700, 100.2800],
        "Bukit Jambul Complex": [5.3300, 100.3100],
        "Butterworth Art Wal": [5.4000, 100.3700],
        "Gurney Paragon Mall": [5.4400, 100.3100],
        "1st Avenue Mall": [5.4130, 100.3290],
        "Sunway Carnival Mall": [5.4000, 100.4000],
        "ESCAPE": [5.4600, 100.2100],
        "Thean Hou Kong Temple": [5.4000, 100.3200],
        "Taman Negara Pulau Pinang": [5.4600, 100.2000],

        # -------------------------------------------------
        # SABAH
        # -------------------------------------------------

        "Pulau Mataking": [4.5500, 118.9500],
        "Bandar Kota Kinabalu": [5.9804, 116.0735],
        "Bandaraya Kota Kinabalu": [5.9804, 116.0735],
        "Pulau Sapi": [6.0000, 116.0000],
        "Pulau Sulug": [5.9700, 116.0000],
        "Kulambia Wildfire Reserve": [5.9000, 116.0000],
        "Taman Kinabalu": [6.0750, 116.5600],
        "Lok Kawi Wildfire Park": [5.8500, 115.9500],
        "Tawau": [4.2500, 117.8900],
        "Beaufort": [5.3500, 115.7500],
        "Kunak": [4.6800, 118.2500],
        "Lahad Datu": [5.0300, 118.3200],
        "Ranau": [5.9500, 116.6700],
        "Pulau Gaya": [6.0200, 116.0400],
        "Pulau Manukan": [5.9700, 116.0000],
        "Kundasang": [6.0100, 116.5800],
        "Sandakan": [5.8400, 118.1100],
        "Pantai Tanjung Aru": [5.9500, 116.0400],
        "Imago Shopping Mall": [5.9750, 116.0670],
        "Suria Sabah Shopping Mall": [5.9850, 116.0750],
        "Desa Dairy Farm": [6.0200, 116.5800],
        "Pulau Bohey Dulang": [4.7400, 117.9200],
        "Sungai Melangkap(Polumpung Malangkap Camp Site)": [6.0000, 116.7000],
        "Culvert View": [6.0000, 116.6000],
        "One Borneo Hypermall": [6.0400, 116.1600],
        "Pasar Tanjung Tawau": [4.2500, 117.8900],
        "Karamunsing Shopping Mall": [5.9700, 116.0700],
        "Sutera Habour Golf & Country Club": [5.9500, 116.0400],
        "Pekan Kundasang & Pekan Nabalu": [6.0200, 116.5800],
        "Jesselton Point Waterfront": [5.9900, 116.0800],
        "Air Panas Poring": [6.0400, 116.7000],
        "Centre Point Sabah": [5.9800, 116.0700],
        "Tunku Abdul Rahman Marine Park": [6.0000, 116.0000],

        # -------------------------------------------------
        # SARAWAK
        # -------------------------------------------------

        "Bandaraya Kuching": [1.5533, 110.3592],
        "Bandar Bintulu": [3.1667, 113.0333],
        "Bandaraya Miri": [4.3995, 113.9914],
        "Ranchan Waterfall,Serian": [1.1800, 110.5500],
        "Pasar Serikin": [1.1500, 110.2000],
        "Serian": [1.1700, 110.5700],
        "Lundu": [1.6700, 109.8500],
        "Sri Aman": [1.2400, 111.4600],
        "Sibu": [2.2900, 111.8300],
        "Samarahan": [1.4600, 110.5000],
        "Borneo Highlands": [1.1600, 110.2500],
        "Kuching Waterfront": [1.5580, 110.3450],
        "Wisma Sanyan": [2.2900, 111.8300],
        "Pantai Tanjung Batu": [3.1800, 113.0400],
        "Padawan": [1.4500, 110.3000],
        "Pantai Damai": [1.7500, 110.3200],
        "Pasar Sentral Sibu": [2.2900, 111.8300],
        "Daesco Star Mega Mall": [3.1700, 113.0400],
        "Vivacity Megamall": [1.5300, 110.3600],
        "Park City Mall": [3.1700, 113.0400],
        "The Spring Mall Bintulu": [3.1700, 113.0400],
        "Buntal Esplanade,Kampung Buntal": [1.7000, 110.3500],
        "Grand Old Lady Canada Hill": [4.4000, 113.9900],
        "Boulevard Shopping Mall": [4.4000, 113.9900],
        "Marina Bay": [4.4000, 113.9900],
        "AEON Mall Kuching Central": [1.5300, 110.3500],
        "Sibu Night Market": [2.2900, 111.8300],

        # -------------------------------------------------
        # SELANGOR
        # -------------------------------------------------

        "Bandar Sunway": [3.0730, 101.6070],
        "Damansara": [3.1500, 101.6100],
        "Kuala Selangor": [3.3300, 101.2500],
        "Batu Caves": [3.2370, 101.6840],
        "Klang": [3.0440, 101.4450],
        "Shah Alam": [3.0738, 101.5183],
        "Bandar Klang": [3.0440, 101.4450],
        "Pantai Morib": [2.7500, 101.4500],
        "Hulu Selangor": [3.5500, 101.6000],
        "Petaling Jaya": [3.1073, 101.6067],
        "Sepang": [2.6900, 101.7500],
        "Gombak": [3.3000, 101.7000],
        "Hulu Langat": [3.1300, 101.7900],
        "Morib": [2.7500, 101.4500],
        "Sabak Bernam": [3.7600, 100.9900],
        "Bagan Lalang": [2.6200, 101.7000],
        "Bandaraya Shah Alam": [3.0738, 101.5183],
        "Bandar Botanic": [3.0000, 101.4300],
        "Subang Jaya": [3.0500, 101.5800],
        "The Curve": [3.1580, 101.6100],
        "Sunway Pyramid Shopping Mall": [3.0730, 101.6070],
        "Zoo Negara": [3.2100, 101.7500],
        "1 Utama Shopping Centre": [3.1480, 101.6160],
        "Sunway Lagoon": [3.0670, 101.6070],
        "Pantai Bagan Lalang": [2.6200, 101.7000],
        "IOI City Mall": [2.9700, 101.7200],
        "Ideal Convention Centre (IDCC) Shah Alam": [3.0800, 101.5200],
        "GM Klang Wholesale City": [3.0000, 101.4400],
        "Kuil Batu Caves": [3.2370, 101.6840],
        "Air Terjun Sungai Gabai": [3.1700, 101.8500],
        "Taman Metropolitan Kepong": [3.2100, 101.6400],
        "i-City, Shah Alam": [3.0700, 101.4800],
        "IKEA Damansara": [3.1580, 101.6100],
        "Gold Coast Marib": [2.7500, 101.4500],
        "AEON Mall Shah Alam": [3.0800, 101.5300],
        "Mitsui Outlet Park": [2.7200, 101.7000],
        "Pantai Rhu Sepuluh": [5.4000, 103.1000],

        # -------------------------------------------------
        # TERENGGANU
        # -------------------------------------------------

        "Pantai Batu Buruk": [5.3250, 103.1450],
        "Pasar Payang": [5.3300, 103.1350],
        "Kemaman": [4.2300, 103.4400],
        "Pulau Warisan": [5.3300, 103.1350],
        "Taman Tema Tamadun Islam": [5.3500, 103.1400],
        "Kuala Ibai": [5.3000, 103.1500],
        "Pantai Kelulut": [5.0500, 102.9300],
        "Kuala Terengganu": [5.3300, 103.1350],
        "Dungun": [4.7600, 103.4200],
        "Besut": [5.8300, 102.5500],
        "Bandar Kemaman": [4.2300, 103.4400],
        "Pantai Teluk Lipat": [4.7600, 103.4200],
        "Kemasik": [4.3200, 103.4400],
        "Pasar Besar Kedai Payang": [5.3300, 103.1350],
        "Pulau Redang": [5.7800, 103.0000],
        "Pulau Perhentian": [5.9000, 102.7300],
        "Terengganu Drawbridge": [5.3350, 103.1450],
        "KTCC Mall": [5.3350, 103.1450],
        "Bazaar Warisan": [5.3300, 103.1350],
        "Balai Ukiran Negeri Terengganu": [5.3300, 103.1350],
        "Chendering Craft Centre": [5.2800, 103.1700],
        "Kuala Terengganu Waterfront": [5.3300, 103.1350],
        "Kenyir Water Park": [5.0500, 102.8000],
        "Masjid Kristal": [5.3400, 103.1400],
        "Pantai Miami Terengganu": [5.3300, 103.1500],
        "Pesisir Pantai Sebarang Takir": [5.3600, 103.1300],

        # -------------------------------------------------
        # KUALA LUMPUR
        # -------------------------------------------------

        "Mid Valley Megamall": [3.1180, 101.6770],
        "Jalan TAR": [3.1550, 101.6960],
        "Jalan Ampang": [3.1600, 101.7200],
        "Bukit Bintang": [3.1478, 101.7130],
        "Cheras": [3.1000, 101.7400],
        "Jalan Tunku Abdul Rahman": [3.1550, 101.6960],
        "Mid Valley City": [3.1180, 101.6770],
        "Istana Negara": [3.1050, 101.6900],
        "Mid Valley": [3.1180, 101.6770],
        "SOGO": [3.1580, 101.6960],
        "KLCC": [3.1579, 101.7116],
        "Pavilion Kuala Lumpur": [3.1490, 101.7130],
        "Jalan Imbi": [3.1420, 101.7110],
        "Jalan Masjid India": [3.1540, 101.6950],
        "Kampung Baru": [3.1630, 101.7070],
        "Sunway Putra Mall": [3.1660, 101.6920],
        "Pasar Seni": [3.1420, 101.6960],
        "Berjaya Time Square": [3.1420, 101.7110],
        "Putra World Trade Centre (PWTC)": [3.1660, 101.6920],
        "Bintang Walk": [3.1478, 101.7130],
        "Mid Valley Exhibition Centre": [3.1180, 101.6770],
        "Setapak Central": [3.2000, 101.7100],
        "Lalaport Bukit Bintang City Centre (BBCC)": [3.1410, 101.7080],
        "Menara Kuala Lumpur": [3.1520, 101.7030],
        "Suria KLCC": [3.1579, 101.7116],
        "Petaling Street Market": [3.1420, 101.6960],

        # -------------------------------------------------
        # LABUAN
        # -------------------------------------------------

        "Kompleks Sukan Laut Antarabangsa Labuan": [5.2800, 115.2400],
        "Pantai Pancur Hitam": [5.3000, 115.2500],
        "Pasar Minggu Labuan": [5.2800, 115.2400],
        "Pantai Sg. Miri": [5.3000, 115.2500],
        "Taman Burung Labuan": [5.3200, 115.2500],
        "Pantai Pohon Batu": [5.3100, 115.2300],
        "Memorial Perang Dunia Kedua": [5.2800, 115.2400],
        "Kampung Patau-Patau": [5.2700, 115.2400],
        "Dataran Labuan": [5.2800, 115.2400],
        "Taman Marin Laut": [5.2800, 115.2300],
        "Pantai Tanjung Batu": [5.2900, 115.2400],
        "Pantai Layang-Layang": [5.3000, 115.2500],
        "Kompleks Ujana Kewangan": [5.2800, 115.2400],
        "Muzium Marin Labuan": [5.2800, 115.2400],

        # -------------------------------------------------
        # PUTRAJAYA
        # -------------------------------------------------

        "Presint 1": [2.9300, 101.6900],
        "Presint 2": [2.9300, 101.6900],
        "Presint 3": [2.9300, 101.6900],
        "Presint 4": [2.9300, 101.6900],
        "Presint 5": [2.9300, 101.6900],
        "Dataran Putrajaya": [2.9264, 101.6964],
        "Dataran Putra": [2.9360, 101.6960],
        "Taman Botani": [2.9100, 101.6900],
        "Pusat Konvensyen Antarabangsa Putrajaya(PICC)": [2.9300, 101.6800],
        "Putrajaya International Convention Centre": [2.9300, 101.6800],
        "Alamanda": [2.9200, 101.6800],
        "Alamanda Shopping Centre": [2.9200, 101.6800],
        "Masjid Putra": [2.9360, 101.6960],
        "Taman Saujana Hijau": [2.9400, 101.6600],
        "Cruise Tasik Putrajaya": [2.9300, 101.6900],
        "Masjid Sultan Mizan Zainal Abidin": [2.9300, 101.6900],
        "Masjid Tuanku Mizan Zainal Abidin": [2.9300, 101.6900],
        "Kelab Tasik Putrajaya,Presint 8": [2.9300, 101.7000],
        "Galeria PJH": [2.9300, 101.6900],
        "Taman Cabaran": [2.9400, 101.6700],
        "Tamab Botani": [2.9100, 101.6900],
        "Taman Wetland": [2.9700, 101.6800],
        "Dataran Putrajaya,Presint 3": [2.9300, 101.6900]
    }


    # =====================================================
    # MAP LAYER SELECTION
    # =====================================================

    map_option = st.radio(
        "Select Map Layer",
        [
            "🏆 Top 5 Destinations",
            "🏨 Hotels"
        ],
        horizontal=True,
        key="tourism_map_option"
    )


    # =====================================================
    # TOP 5 DESTINATIONS
    # =====================================================

    if map_option == "🏆 Top 5 Destinations":

        st.markdown("""
        <div style="
            margin-top: 18px;
            margin-bottom: 15px;
            font-size: 20px;
            font-weight: 700;
            color: #12355B;
        ">
            🏆 Top 5 Destinations
        </div>
        """, unsafe_allow_html=True)


        if not top_destination.empty:

            destination_data = top_destination.copy()

            # -------------------------------------------------
            # CLEAN COLUMNS
            # -------------------------------------------------

            destination_data.columns = [
                str(col).strip()
                for col in destination_data.columns
            ]

            destination_data[destination_year] = pd.to_numeric(
                destination_data[destination_year],
                errors="coerce"
            )

            destination_data[destination_state] = (
                destination_data[destination_state]
                .astype(str)
                .str.strip()
            )

            destination_data[destination_type_visitor] = (
                destination_data[destination_type_visitor]
                .astype(str)
                .str.strip()
            )

            destination_data[destination_name] = (
                destination_data[destination_name]
                .astype(str)
                .str.strip()
            )


            # -------------------------------------------------
            # REMOVE COMMON TEXT ERRORS
            # -------------------------------------------------

            destination_data[destination_name] = (
                destination_data[destination_name]
                .str.replace(
                    "\u00a0",
                    " ",
                    regex=False
                )
                .str.replace(
                    r"\s+",
                    " ",
                    regex=True
                )
                .str.strip()
            )


            # -------------------------------------------------
            # INDEPENDENT FILTERS
            # -------------------------------------------------

            destination_years = sorted(
                destination_data[destination_year]
                .dropna()
                .astype(int)
                .unique()
                .tolist()
            )

            destination_states = sorted(
                destination_data[destination_state]
                .dropna()
                .unique()
                .tolist()
            )

            destination_visitor_types = [
                x for x in
                ["Domestic Visitor", "Tourists"]
                if x in
                destination_data[
                    destination_type_visitor
                ].unique()
            ]

            # Add any unexpected type if present
            existing_types = (
                destination_data[
                    destination_type_visitor
                ]
                .dropna()
                .unique()
                .tolist()
            )

            for x in existing_types:
                if x not in destination_visitor_types:
                    destination_visitor_types.append(x)


            filter_col1, filter_col2, filter_col3 = st.columns(
                3,
                gap="medium"
            )


            with filter_col1:

                destination_selected_year = st.selectbox(
                    "Year",
                    destination_years,
                    key="destination_year_filter",
                    width="stretch"
                )


            with filter_col2:

                destination_selected_state = st.selectbox(
                    "State",
                    destination_states,
                    key="destination_state_filter",
                    width="stretch"
                )


            with filter_col3:

                destination_selected_type = st.selectbox(
                    "Visitor Type",
                    destination_visitor_types,
                    key="destination_type_filter",
                    width="stretch"
                )


            # -------------------------------------------------
            # FILTER DATA
            # -------------------------------------------------

            destination_df = destination_data[
                destination_data[destination_year]
                == destination_selected_year
            ].copy()

            destination_df = destination_df[
                destination_df[destination_state]
                == destination_selected_state
            ].copy()

            destination_df = destination_df[
                destination_df[destination_type_visitor]
                .str.lower()
                ==
                destination_selected_type.lower()
            ].copy()


            # -------------------------------------------------
            # REMOVE DUPLICATE DESTINATIONS
            # -------------------------------------------------

            destination_df = destination_df.drop_duplicates(
                subset=[destination_name],
                keep="first"
            )


            # -------------------------------------------------
            # TOP 5
            # -------------------------------------------------

            destination_df = destination_df.head(5).copy()


            # -------------------------------------------------
            # CURRENT VIEW
            # -------------------------------------------------

            st.markdown(
                f"""
                <div style="
                margin-top: 10px;
                margin-bottom: 16px;
                padding: 11px 15px;
                background: #F8FAFC;
                border-left: 4px solid #12355B;
                border-radius: 6px;
                font-size: 14px;
                color: #475569;
                ">
                <b>Current View</b>
                <span style="margin-left:18px;">
                Year:
                <b style="color:#12355B;">
                {destination_selected_year}
                </b>
                </span>
                <span style="margin-left:18px;">
                State:
                <b style="color:#12355B;">
                {destination_selected_state}
                </b>
                </span>
                <span style="margin-left:18px;">
                Visitor Type:
                <b style="color:#12355B;">
                {destination_selected_type}
                </b>
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )


            # -------------------------------------------------
            # MAP + RANKING
            # -------------------------------------------------

            map_col, ranking_col = st.columns(
                [7, 3],
                gap="large"
            )


            # =================================================
            # MAP
            # =================================================

            with map_col:

                if not destination_df.empty:

                    first_destination = str(
                        destination_df.iloc[0][destination_name]
                    ).strip()

                    first_coordinates = (
                        destination_coordinates.get(
                            first_destination
                        )
                    )

                    if first_coordinates:

                        map_center = first_coordinates

                    else:

                        map_center = state_coordinates.get(
                            destination_selected_state,
                            state_coordinates["Malaysia"]
                        )


                    tourism_map = folium.Map(
                        location=map_center,
                        zoom_start=10,
                        tiles="OpenStreetMap",
                        control_scale=True
                    )


                    # -------------------------------------------------
                    # ADD NUMBERED MARKERS
                    # -------------------------------------------------

                    mapped_count = 0

                    for rank, (_, row) in enumerate(
                        destination_df.iterrows(),
                        start=1
                    ):

                        place = str(
                            row[destination_name]
                        ).strip()

                        coordinates = (
                            destination_coordinates.get(
                                place
                            )
                        )

                        # Do not create fake/random locations
                        if coordinates is None:
                            continue

                        mapped_count += 1

                        lat, lon = coordinates


                        # Numbered circular marker
                        marker_html = f"""
                        <div style="
                        width: 34px;
                        height: 34px;
                        background: #12355B;
                        border: 3px solid white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 15px;
                        font-weight: 700;
                        box-shadow:
                        0 2px 6px rgba(0,0,0,0.35);
                        ">
                        {rank}
                        </div>
                        """


                        popup_html = f"""
                        <div style="
                        width: 230px;
                        font-family: Arial;
                        ">
                        <div style="
                        font-size: 17px;
                        font-weight: 700;
                        color: #12355B;
                        margin-bottom: 8px;
                        ">
                        🏆 Rank #{rank}
                        </div>
                        <div style="
                        font-size: 14px;
                        margin-bottom: 5px;
                        ">
                        📍 <b>{place}</b>
                        </div>
                        <div style="
                        font-size: 13px;
                        color: #475569;
                        margin-bottom: 4px;
                        ">
                        📌 {destination_selected_state}
                        </div>
                        <div style="
                        font-size: 13px;
                        color: #475569;
                        margin-bottom: 4px;
                        ">
                        📅 {destination_selected_year}
                        </div>
                        <div style="
                        font-size: 13px;
                        color: #475569;
                        ">
                        👥 {destination_selected_type}
                        </div>
                        </div>
                        """


                        folium.Marker(
                            location=[lat, lon],
                            popup=folium.Popup(
                                popup_html,
                                max_width=280
                            ),
                            tooltip=folium.Tooltip(
                                f"<b>#{rank} {place}</b>"
                            ),
                            icon=folium.DivIcon(
                                html=marker_html,
                                icon_size=(34, 34),
                                icon_anchor=(17, 17)
                            )
                        ).add_to(tourism_map)


                    # -------------------------------------------------
                    # FIT MAP TO MARKERS
                    # -------------------------------------------------

                    if mapped_count > 1:

                        marker_locations = []

                        for _, row in destination_df.iterrows():

                            place = str(
                                row[destination_name]
                            ).strip()

                            coordinates = (
                                destination_coordinates.get(
                                    place
                                )
                            )

                            if coordinates:
                                marker_locations.append(
                                    coordinates
                                )

                        if marker_locations:

                            tourism_map.fit_bounds(
                                marker_locations,
                                padding=(30, 30)
                            )


                    st_folium(
                        tourism_map,
                        width=None,
                        height=540,
                        key="top5_destination_map"
                    )


                    # -------------------------------------------------
                    # LOCATION WARNING
                    # -------------------------------------------------

                    unmapped_places = []

                    for _, row in destination_df.iterrows():

                        place = str(
                            row[destination_name]
                        ).strip()

                        if (
                            place
                            not in destination_coordinates
                        ):
                            unmapped_places.append(place)


                    if unmapped_places:

                        st.caption(
                            "⚠️ Location coordinates are not yet "
                            "available for: "
                            + ", ".join(unmapped_places)
                        )


                else:

                    st.info(
                        "No destination data available for "
                        f"{destination_selected_state} "
                        f"in {destination_selected_year}."
                    )


            # =================================================
            # TOP 5 RANKING PANEL
            # =================================================

            with ranking_col:

                st.markdown(
                    """
                    <div style="
                        font-size: 17px;
                        font-weight: 700;
                        color: #12355B;
                        margin-bottom: 12px;
                    ">
                        🏆 TOP 5 DESTINATIONS
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                if not destination_df.empty:

                    for rank, (_, row) in enumerate(
                        destination_df.iterrows(),
                        start=1
                    ):

                        place = str(
                            row[destination_name]
                        ).strip()

                        has_location = (
                            place
                            in destination_coordinates
                        )

                        location_status = (
                            "📍 Mapped"
                            if has_location
                            else "⚠️ Location unavailable"
                        )


                        st.markdown(
                            f"""
                            <div style="
                            background: #FFFFFF;
                            border: 1px solid #E2E8F0;
                            border-radius: 10px;
                            padding: 13px 14px;
                            margin-bottom: 10px;
                            box-shadow:
                            0 2px 6px
                            rgba(15,23,42,0.04);
                            ">
                            <div style="
                            display:flex;
                            align-items:center;
                            gap:10px;
                            ">
                            <div style="
                            width:30px;
                            height:30px;
                            min-width:30px;
                            background:#12355B;
                            color:white;
                            border-radius:50%;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-weight:700;
                            font-size:13px;
                            ">
                            {rank}
                            </div>
                            <div style="
                            flex:1;
                            font-size:14px;
                            font-weight:600;
                            color:#1E293B;
                            line-height:1.35;
                            ">
                            {place}
                            </div>
                            </div>
                            <div style="
                            margin-left:40px;
                            margin-top:5px;
                            font-size:11px;
                            color:#64748B;
                            ">
                            {location_status}
                            </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                else:

                    st.info("No Top 5 destinations available.")


        else:

            st.info(
                "Top destination data is not available."
            )

    # =====================================================
    # HOTEL MAP + ANALYTICS
    # =====================================================
    elif map_option == "🏨 Hotels":
        st.markdown("""
        <div style="
        margin-top: 18px;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: 700;
        color: #12355B;
        ">
        🏨 Hotel Distribution
        </div>
        """, unsafe_allow_html=True)


        if not hotel_rating.empty:
            hotel_data = hotel_rating.copy()
            hotel_data.columns = [
                str(col).strip()
                for col in hotel_data.columns
            ]

            # =================================================
            # CLEAN DATA
            # =================================================
            hotel_data[hotel_year] = pd.to_numeric(
                hotel_data[hotel_year],
                errors="coerce"
            )

            hotel_data[hotel_state] = (
                hotel_data[hotel_state]
                .astype(str)
                .str.replace("\xa0", " ", regex=False)
                .str.strip()
            )

            hotel_data[hotel_rating_category] = (
                hotel_data[hotel_rating_category]
                .astype(str)
                .str.replace("\xa0", " ", regex=False)
                .str.strip()
            )

            hotel_data[hotel_number] = pd.to_numeric(
                hotel_data[hotel_number],
                errors="coerce"
            ).fillna(0)

            hotel_data[hotel_room_number] = pd.to_numeric(
                hotel_data[hotel_room_number],
                errors="coerce"
            ).fillna(0)

            # =================================================
            # HOTEL FILTERS
            # =================================================
            hotel_years = sorted(
                hotel_data[hotel_year]
                .dropna()
                .astype(int)
                .unique()
                .tolist()
            )

            hotel_states = sorted(
                hotel_data[hotel_state]
                .dropna()
                .unique()
               .tolist()
            )

            hotel_filter_col1, hotel_filter_col2 = st.columns(
                2,gap="medium")

            with hotel_filter_col1:
                hotel_selected_year = st.selectbox(
                    "Year",
                    hotel_years,
                    key="hotel_year_filter",
                    width="stretch"
            )

            with hotel_filter_col2:
                hotel_selected_state = st.selectbox(
                    "State",
                    ["Malaysia"] + hotel_states,
                    key="hotel_state_filter",
                    width="stretch"
                )

            # =================================================
            # HOTEL DATA FILTER
            # =================================================
            hotel_df = hotel_data[
                hotel_data[hotel_year]
                == hotel_selected_year
            ].copy()
            if hotel_selected_state != "Malaysia":
                hotel_df = hotel_df[
                hotel_df[hotel_state]
                == hotel_selected_state
                    ].copy()

            # =================================================
            # DISPLAY TOGGLE
            # =================================================

            hotel_metric = st.radio(
                "Map Metric",
                [
                    "🏨 Hotels",
                    "🛏️ Rooms"
                ],
                horizontal=True,
                key="hotel_map_metric")


            # =================================================
            # MAP + ANALYTICS LAYOUT
            # =================================================
            map_col, analytics_col = st.columns(
                [6.8, 3.2],
                gap="medium"
            )

            # =================================================
            # LEFT COLUMN: HOTEL MAP
            # =================================================
            with map_col:
                if not hotel_df.empty:
                    # -------------------------------------------------
                    # HOTEL SUMMARY BY STATE
                    # -------------------------------------------------

                    hotel_summary = (
                        hotel_df
                       .groupby(
                           hotel_state,
                           as_index=False
                       )
                            .agg(
                                Hotels=(hotel_number, "sum"),
                                Rooms=(hotel_room_number, "sum")
                            )
                    )


                    hotel_summary["Hotels"] = pd.to_numeric(
                        hotel_summary["Hotels"],
                        errors="coerce"
                    ).fillna(0)

                    hotel_summary["Rooms"] = pd.to_numeric(
                        hotel_summary["Rooms"],
                        errors="coerce"
                    ).fillna(0)

                    # -------------------------------------------------
                    # MAP CENTER
                    # -------------------------------------------------
                    if (
                        hotel_selected_state != "Malaysia"
                        and hotel_selected_state
                        in state_coordinates
                    ):
                        hotel_map_center = (
                            state_coordinates[
                                hotel_selected_state
                                ]
                        )
                        hotel_zoom = 8
                    else:
                        hotel_map_center = (
                            state_coordinates["Malaysia"]
                        )
                        hotel_zoom = 6

                    # -------------------------------------------------
                    # CREATE MAP
                    # -------------------------------------------------
                    hotel_map = folium.Map(
                        location=hotel_map_center,
                        zoom_start=hotel_zoom,
                        tiles="OpenStreetMap",
                        control_scale=True)


                    # =================================================
                    # ONE ARROW PER STATE
                    #
                    # IMPORTANT:
                    # Only ONE marker is created for each state.
                    # This keeps the map fast.
                    # =================================================
                    marker_locations = []
                    for _, row in hotel_summary.iterrows():
                        state_name = str(
                            row[hotel_state]
                        ).strip()

                        # Skip states without coordinates
                        if state_name not in state_coordinates:
                            continue
                        # -------------------------------------------------
                        # STATE COORDINATES
                        # -------------------------------------------------
                        center_lat, center_lon = (
                            state_coordinates[state_name]
                        )


                        # -------------------------------------------------
                        # HOTEL / ROOM VALUES
                        # -------------------------------------------------
                        hotel_count = int(
                            round(row["Hotels"]))

                        room_count = int(
                            round(row["Rooms"])
                        )

                        # -------------------------------------------------
                        # CURRENT MAP METRIC
                        # -------------------------------------------------
                        if hotel_metric == "🏨 Hotels":
                            metric_label = "Hotels"
                            metric_value = hotel_count
                        else:
                            metric_label = "Rooms"
                            metric_value = room_count

                        marker_lat = center_lat
                        marker_lon = center_lon

                        marker_locations.append(
                            [
                                marker_lat,
                                marker_lon
                            ]
                        )

                        # =================================================
                        # POPUP
                        # =================================================
                        popup_html = f"""
                        <div style="
                        width:220px;
                        font-family:Arial,sans-serif;
                        ">
                        <div style="
                        font-size:17px;
                        font-weight:700;
                        color:#12355B;
                        margin-bottom:8px;
                        ">
                        {state_name}
                        </div>
                        <div style="
                        font-size:13px;
                        color:#64748B;
                        margin-bottom:5px;
                        ">
                        Year: {hotel_selected_year}
                        </div>
                        <div style="
                        font-size:14px;
                        color:#334155;
                        margin-bottom:3px;
                        ">
                        Hotels:
                        <b>{hotel_count:,}</b>
                        </div>
                        <div style="
                        font-size:14px;
                        color:#334155;
                        ">
                        Rooms:
                        <b>{room_count:,}</b>
                        </div>
                        </div>
                        """
                        # =================================================
                        # SIMPLE BLUE ARROW
                        # =================================================
                        arrow_html = """
                        <div style="
                        width:30px;
                        height:30px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        filter:drop-shadow(
                        0px 2px 3px rgba(0,0,0,0.30)
                        );
                        ">
                        <div style="
                        width:0;
                        height:0;
                        border-left:10px solid transparent;
                        border-right:10px solid transparent;
                        border-bottom:23px solid #1463E8;
                        transform:rotate(45deg);
                        "></div>
                        </div>
                        """

                        # =================================================
                        # ONE MARKER
                        # =================================================
                        folium.Marker(
                            location=[
                                marker_lat,
                                marker_lon
                            ],
                            popup=folium.Popup(
                                popup_html,
                                max_width=280
                            ),

                            tooltip=(
                                f"{state_name} | "
                                f"{metric_label}: "
                                f"{metric_value:,}"
                            ),
                            icon=folium.DivIcon(
                                html=arrow_html,
                                icon_size=(30, 30),
                                icon_anchor=(15, 15)
                            )

                        ).add_to(hotel_map)

                    # =================================================
                    # AUTO FIT MAP
                    # =================================================

                    if len(marker_locations) > 1:
                        hotel_map.fit_bounds(
                            marker_locations,
                            padding=(20, 20)
                        )

                    # =================================================
                    # MAP TITLE
                    # =================================================
                    st.markdown(
                        f"""
                        <div style="
                        font-size:17px;
                        font-weight:700;
                        color:#12355B;
                        margin-bottom:8px;
                        ">
                        📍 {hotel_metric} Distribution Map
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =================================================
                    # DISPLAY MAP
                    # =================================================
                    st_folium(
                        hotel_map,
                        width=None,
                        height=540,
                        key="hotel_distribution_map"
                    )

                else:
                    st.info(
                        "No hotel data available for "
                        f"{hotel_selected_state} "
                        f"in {hotel_selected_year}."
                    )

            # =================================================
            # RIGHT COLUMN: HOTEL ANALYTICS
            # =================================================
            with analytics_col:

                # =================================================
                # TOTAL HOTEL / ROOM KPI
                # =================================================
                total_hotel_count = hotel_df[hotel_number].sum()

                total_room_count = hotel_df[hotel_room_number].sum()


                # =================================================
                # RATING SUMMARY
                # =================================================
                rating_summary = (
                    hotel_df
                    .groupby(
                        hotel_rating_category,
                        as_index=False
                    )[hotel_number]
                    .sum()
                )

                rating_summary = rating_summary[
                    rating_summary[hotel_number] > 0
                ].copy()


                # =================================================
                # RATING ORDER
                # =================================================
                def rating_order_value(x):
                    text = str(x).lower().strip()

                    if "5" in text and (
                        "star" in text or
                        "bintang" in text
                    ):
                        return 1

                    if "4" in text and (
                        "star" in text or
                        "bintang" in text
                    ):
                        return 2

                    if "3" in text and (
                        "star" in text or
                        "bintang" in text
                    ):
                        return 3

                    if "2" in text and (
                        "star" in text or
                        "bintang" in text
                    ):
                        return 4

                    if "1" in text and (
                        "star" in text or
                        "bintang" in text
                    ):
                        return 5

                    if "orchid" in text:
                        return 6

                    if "unrated" in text:
                        return 99

                    return 50


                rating_summary["_order"] = (
                    rating_summary[
                        hotel_rating_category
                    ].apply(rating_order_value)
                )

                rating_summary = (
                    rating_summary
                    .sort_values("_order")
                    .drop(columns="_order")
                )


                # =================================================
                # HOTEL / ROOM GRADE DISTRIBUTION
                # =================================================
                if hotel_metric == "🏨 Hotels":

                    st.markdown(
                        """
                        <div style="
                        font-size:17px;
                        font-weight:700;
                        color:#12355B;
                        margin-bottom:5px;
                        ">
                        ⭐ Hotel Grade Distribution
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if not rating_summary.empty:

                        fig_hotel_rating = px.bar(
                            rating_summary,
                            x=hotel_number,
                            y=hotel_rating_category,
                            orientation="h",
                            title="Hotels by Grade"
                        )

                        rating_chart_height = max(
                            250,
                            min(
                                430,
                                90 + len(rating_summary) * 48
                            )
                        )

                        fig_hotel_rating.update_layout(
                            template="plotly_white",
                            height=rating_chart_height,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(
                                family="Arial",
                                size=11,
                                color="#334155"
                            ),
                            title_font=dict(
                                size=15,
                                color="#12355B"
                            ),
                            margin=dict(
                                l=5,
                                r=25,
                                t=45,
                                b=25
                            ),
                            xaxis_title="Number of Hotels",
                            yaxis_title="",
                            showlegend=False
                        )

                        fig_hotel_rating.update_traces(
                            marker_color="#287BE8",
                            texttemplate="%{x:,.0f}",
                            textposition="outside",
                            cliponaxis=False,
                            hovertemplate=(
                                "<b>%{y}</b><br>"
                                "Hotels: %{x:,.0f}"
                                "<extra></extra>"
                            )
                        )

                        fig_hotel_rating.update_xaxes(
                            showgrid=True,
                            gridcolor="#E2E8F0"
                        )

                        fig_hotel_rating.update_yaxes(
                            showgrid=False
                        )

                        st.plotly_chart(
                            fig_hotel_rating,
                            width="stretch",
                            key="hotel_grade_distribution",
                            on_select="ignore",
                            config={
                                "displayModeBar": False,
                                "scrollZoom": False
                            }
                        )

                    else:
                        st.info(
                            "No hotel grade data available."
                        )


                elif hotel_metric == "🛏️ Rooms":
                    st.markdown(
                        """
                        <div style="
                        font-size:17px;
                        font-weight:700;
                        color:#12355B;
                        margin-bottom:5px;
                        ">
                        ⭐ Hotel Grade Distribution
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =================================================
                    # ROOM SUMMARY
                    # =================================================
                    room_summary = (
                        hotel_df
                        .groupby(
                            hotel_rating_category,
                            as_index=False
                        )[hotel_room_number]
                        .sum()
                    )

                    room_summary = room_summary[
                        room_summary[hotel_room_number] > 0
                    ].copy()

                    room_summary["_order"] = (
                        room_summary[
                            hotel_rating_category
                        ].apply(rating_order_value)
                    )

                    room_summary = (
                        room_summary
                        .sort_values("_order")
                        .drop(columns="_order")
                    )


                    # =================================================
                    # ROOM CHART
                    # =================================================
                    if not room_summary.empty:

                        fig_room_rating = px.bar(
                            room_summary,
                            x=hotel_room_number,
                            y=hotel_rating_category,
                            orientation="h",
                            title="Rooms by Grade"
                        )

                        room_chart_height = max(
                            230,
                            min(
                                360,
                                80 + len(room_summary) * 42
                            )
                        )

                        fig_room_rating.update_layout(
                            template="plotly_white",
                            height=room_chart_height,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(
                                family="Arial",
                                size=11,
                                color="#334155"
                            ),
                            title_font=dict(
                                size=15,
                                color="#12355B"
                            ),
                            margin=dict(
                                l=5,
                                r=25,
                                t=45,
                                b=25
                            ),
                            xaxis_title="Number of Rooms",
                            yaxis_title="",
                            showlegend=False
                        )

                        fig_room_rating.update_traces(
                            marker_color="#7657D9",
                            texttemplate="%{x:,.0f}",
                            textposition="outside",
                            cliponaxis=False,
                            hovertemplate=(
                                "<b>%{y}</b><br>"
                                "Rooms: %{x:,.0f}"
                                "<extra></extra>"
                            )
                        )

                        fig_room_rating.update_xaxes(
                            showgrid=True,
                            gridcolor="#E2E8F0"
                        )

                        fig_room_rating.update_yaxes(
                            showgrid=False
                        )

                        st.plotly_chart(
                            fig_room_rating,
                            width="stretch",
                            key="hotel_room_distribution",
                            on_select="ignore",
                            config={
                                "displayModeBar": False,
                                "scrollZoom": False
                            }
                        )

                    else:
                        st.info(
                            "No room data available."
                        )

                else:
                    st.info(
                        "No hotel information available.")


                # =================================================
                # ACCOMMODATION CAPACITY
                # =================================================
                st.markdown(
                    """
                    <div style="
                    margin-top:8px;
                    margin-bottom:8px;
                    font-size:16px;
                    font-weight:700;
                    color:#12355B;
                    ">
                    🛏️ Accommodation Capacity
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # ROOM KPI CARDS
                # -------------------------------------------------
                total_hotel_count = hotel_df[
                    hotel_number
                ].sum()

                total_room_count = hotel_df[
                    hotel_room_number
                ].sum()

                kpi1, kpi2 = st.columns(2)

                with kpi1:
                    st.markdown(
                        f"""
                        <div style="
                        background:#F8FAFC;
                        border:1px solid #E2E8F0;
                        border-radius:10px;
                        padding:13px;
                        text-align:center;
                        ">
                        <div style="
                        font-size:11px;
                        color:#64748B;
                        font-weight:600;
                        ">
                        TOTAL HOTELS
                        </div>
                        <div style="
                        margin-top:4px;
                        font-size:22px;
                        font-weight:700;
                        color:#12355B;
                        ">
                        {total_hotel_count:,.0f}
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with kpi2:
                    st.markdown(
                        f"""
                        <div style="
                        background:#F8FAFC;
                        border:1px solid #E2E8F0;
                        border-radius:10px;
                        padding:13px;
                        text-align:center;
                        ">
                        <div style="
                        font-size:11px;
                        color:#64748B;
                        font-weight:600;
                        ">
                        TOTAL ROOMS
                        </div>
                        <div style="
                        margin-top:4px;
                        font-size:22px;
                        font-weight:700;
                        color:#12355B;
                        ">
                        {total_room_count:,.0f}
                        </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    "<div style='height:10px;'></div>",
                    unsafe_allow_html=True
                )
    # =========================================================
    # POWER BI DASHBOARD
    # =========================================================
    st.markdown(
        '<div class="section-heading">Interactive Tourism Dashboard</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p class="section-text">
        Explore additional tourism insights through an interactive Power BI dashboard.
        </p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="powerbi-container">
            <iframe
                title="4SIGHT_Datathon2026_Dashboard"
                src="https://app.powerbi.com/view?r=eyJrIjoiZjdiMjljYjItY2I5Yi00ZjFlLTgyOWYtNjZjMjQyNGM3NTQzIiwidCI6IjFmNTUxYWViLTdlYTEtNDcyYy05YWMwLTA5ZGU5YmYzMzA1MSIsImMiOjEwfQ%3D%3D&pageName=5e820162677e1acd80bc"
                frameborder="0"
                allowFullScreen="true">
            </iframe>
        </div>
        """,
        unsafe_allow_html=True
   )

    

    # =====================================================
    # SECTION DIVIDER
    # =====================================================
    st.divider()


# -----------------------------------------------------------------------------
# Part 3: Smart Trip Planner
# -----------------------------------------------------------------------------
elif app_mode == "🔥SMART TRIP PLANNER":

    # =========================================================
    # RECEIPT DATA FOR BUDGET REFERENCE
    # =========================================================

    receipt = tourism_data.get(
        "Receipt",
        pd.DataFrame()
    )

    receipt_year = "Year"
    receipt_state = "State"
    receipt_type = "Type of Receipts"
    receipt_value = "Receipts"

    # =========================================================
    # PAGE HEADER
    # =========================================================

    st.markdown(
        "<h1 style='text-align:center;'>🗺️ Smart Trip Planner</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style='text-align:center; font-size:17px;'>
            Find destinations that match your travel preferences while supporting a more balanced tourism distribution across Malaysia.
        </p>
        """,
        unsafe_allow_html=True
        )
    
    st.markdown("### Plan Your Trip")

    # =========================================================
    # STATE + TOURISM THEME
    # =========================================================

    col1, col2 = st.columns(2)

    with col1:

        state_options = [
            "Smart Recommendation"
        ] + sorted(
            df_poi["state_std"]
            .dropna()
            .unique()
            .tolist()
        )

        user_state = st.selectbox(
            "Preferred State",
            state_options,
            help=(
                "Choose a specific state, or let MyDecouple AI "
                "prioritize destinations in relatively lower-pressure areas."
            )
        )

    with col2:

        theme_options = [
            "All Themes",
            "Historical",
            "Nature",
            "Theme Park",
            "Shopping",
            "Culture"
        ]

        user_theme = st.selectbox(
            "Tourism Theme",
            theme_options
        )

    # =========================================================
    # CROWD + NUMBER OF RECOMMENDATIONS
    # =========================================================

    col3, col4 = st.columns(2)

    with col3:

        user_crowd_tol = st.select_slider(
            "Crowd Preference",
            options=[
                "Low",
                "Medium",
                "High"
            ],
            value="Medium",
            help=(
                "Low = prefer less digitally popular destinations | "
                "Medium = prefer moderately popular destinations | "
                "High = prefer more digitally popular destinations."
            )
        )

    with col4:

        top_n = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5,
            help = (
                "Choose how many destinations you would like "
                "MyDecouple AI to recommend.")
            )

    # =========================================================
    # BUDGET PREFERENCE
    # =========================================================

    st.markdown("### 💰 Budget Preference")

    budget_col1, budget_col2 = st.columns(2)

    with budget_col1:

        travel_type = st.selectbox(
            "Travel Type",
            [
                "Same-Day Trip",
                "Overnight Trip"
            ],
            help=(
                "Choose whether your trip is a same-day visit "
                "or an overnight trip."
            )
        )

    with budget_col2:

        user_budget = st.number_input(
            "Budget per Visitor (RM)",
            min_value=0.0,
            value=300.0,
            step=50.0,
            help=(
                "Enter your approximate tourism expenditure "
                "budget per visitor."
            )
        )
    # =========================================================
    # BUDGET STATUS EXPLANATION
    # =========================================================
    st.markdown(
        """
        🟢 **Within Budget**  
        *State average expenditure is within your selected budget.*

        🟡 **Above Budget**  
        *State average expenditure is above your selected budget.*
        """
)

    st.divider()

    # =========================================================
    # LATEST ML PREDICTION YEAR
    # =========================================================

    available_years = sorted(
        df_shap_state["year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    if not available_years:

        st.error(
            "No valid ML prediction year is available."
        )

        st.stop()

    latest_year = available_years[-1]

    state_df = df_shap_state[
        df_shap_state["year"] == latest_year
    ].copy()

    state_df = state_df.dropna(
        subset=[
            "state_std",
            "actual_tourist_density_real"
        ]
    ).copy()

    if state_df.empty:

        st.error(
            "No valid ML prediction data is available."
        )

        st.stop()

    # =========================================================
    # TOURIST DENSITY POLICY REFERENCE
    # =========================================================
    national_baseline = 9346.28
    gov_overtourism_ceiling = 10467.83
    gov_underutilized_floor = 8224.73

    # =========================================================
    # TOURIST DENSITY CLASSIFICATION
    # =========================================================
    def classify_tourist_density(value):
        # Below the underutilized floor
        if value < gov_underutilized_floor:
            return "Low"
        # Between floor and national baseline
        elif value <= national_baseline:
            return "Medium"
        # Between baseline and overtourism ceiling
        elif value <= gov_overtourism_ceiling:
            return "High"
        # Above overtourism ceiling
        else:
            return 0
    state_df["Tourism_Density"] = (
        state_df["actual_tourist_density_real"])
    state_df["Tourism_Density_Category"] = (
        state_df["Tourism_Density"]
            .apply(classify_tourist_density))
    # =========================================================
    # TOURIST DENSITY SUITABILITY
    # =========================================================
    def calculate_density_suitability(value):
        # Below the underutilized floor
        if value < gov_underutilized_floor:
            return max(
                0,
                value / gov_underutilized_floor
            )
        # Between floor and national baseline
        elif value <= national_baseline:
            return (
                value / national_baseline
            )
        # Between baseline and overtourism ceiling
        elif value <= gov_overtourism_ceiling:
            return max(
                0,1 - ((value - national_baseline)/ (gov_overtourism_ceiling- national_baseline)))
        # Above overtourism ceiling
        else:
            return 0
    state_df["Tourism_Density_Suitability"] = (
        state_df["actual_tourist_density_real"]
            .apply(calculate_density_suitability))
    # =========================================================
    # STATE SELECTION
    # =========================================================
    if user_state == "Smart Recommendation":
        recommended_states = (
            state_df
                .sort_values(
                    "Tourism_Density_Suitability",
                    ascending=False
                ).copy())
        candidate_states = (recommended_states.head(8).copy())
    else:
        candidate_states = state_df[
            state_df["state_std"]
            == user_state
            ].copy()

    # =========================================================
    # STATE PRESSURE MESSAGE
    # =========================================================
    if user_state != "Smart Recommendation":
        selected_state_ml = state_df[
            state_df["state_std"]
            == user_state
            ]
        
        if not selected_state_ml.empty:
            density_category = (
                selected_state_ml[
                    "Tourism_Density_Category"
                    ].iloc[0]
            )
            actual_density = (
                selected_state_ml[
                    "Tourism_Density"
                    ].iloc[0]
            )
            density_score = (
                selected_state_ml[
                    "Tourism_Density_Suitability"
                    ].iloc[0]
            )
            if density_category == "Low":
                st.success(
                    f"🟢 **{user_state} — "
                    "Low Tourist Density**\n\n"
                    f"Actual tourist density: "
                    f"{actual_density:,.2f}\n\n"
                    "The state has relatively low tourist density based on the defined reference range.")     
            
            elif density_category == "Medium":
                st.info(
                    f"🟡 **{user_state} — "
                    "Medium Tourist Density**\n\n"
                    f"Actual tourist density: "
                    f"{actual_density:,.2f}\n\n"
                    "The state falls within the defined tourist density reference range."
                )
            else:
                st.warning(
                    f"🔴 **{user_state} — "
                    "High Tourist Density**\n\n"
                    f"Actual tourist density: "
                    f"{actual_density:,.2f}\n\n"
                    "The state has relatively high tourist density based on the defined reference range."
                )
    else:
        st.info(
            "🤖 **Smart Recommendation Mode**\n\n"
            "The planner ranks states using Tourist Density "
            "Suitability, then matches destinations with "
            "your travel preferences."
        )

    # =========================================================
    # INITIAL POI FILTER
    # =========================================================

    filtered_df = df_poi.copy()

    selected_states = (
        candidate_states[
            "state_std"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    filtered_df = filtered_df[
        filtered_df["state_std"]
        .isin(selected_states)
    ].copy()

    # =========================================================
    # TOURISM THEME FILTER
    # =========================================================

    if user_theme != "All Themes":

        filtered_df = filtered_df[
            filtered_df["Theme"]
            == user_theme
        ].copy()

    if filtered_df.empty:

        st.warning(
            "No attractions match your selected preferences. "
            "Please try another tourism theme or state."
        )

        st.stop()

    # =========================================================
    # MERGE ML TOURISM PRESSURE
    # =========================================================

    filtered_df = filtered_df.merge(
        candidate_states[
            [
                "state_std",
                "Tourism_Density",
                "Tourism_Density_Category",
                "Tourism_Density_Suitability"
            ]
        ],
        on="state_std",
        how="left"
    )

    # =========================================================
    # DIGITAL VISIBILITY
    # =========================================================

    if "digital_visibility_score" in filtered_df.columns:

        filtered_df[
            "Digital_Visibility"
        ] = pd.to_numeric(
            filtered_df[
                "digital_visibility_score"
            ],
            errors="coerce"
        ).fillna(50)

    else:

        filtered_df[
            "Digital_Visibility"
        ] = 50

    filtered_df[
        "Digital_Visibility"
    ] = (
        filtered_df[
            "Digital_Visibility"
        ]
        .clip(0, 100)
        / 100
    )

    # =========================================================
    # CROWD PREFERENCE
    # =========================================================

    if user_crowd_tol == "Low":

        filtered_df[
            "Crowd_Suitability"
        ] = (
            1
            - filtered_df[
                "Digital_Visibility"
            ]
        )

    elif user_crowd_tol == "Medium":

        filtered_df[
            "Crowd_Suitability"
        ] = (
            1
            - abs(
                filtered_df[
                    "Digital_Visibility"
                ]
                - 0.5
            )
        )

    else:

        filtered_df[
            "Crowd_Suitability"
        ] = (
            filtered_df[
                "Digital_Visibility"
            ]
        )

    # =========================================================
    # RATING SCORE
    # =========================================================

    if "rating" in filtered_df.columns:

        filtered_df[
            "Rating_Score"
        ] = pd.to_numeric(
            filtered_df[
                "rating"
            ],
            errors="coerce"
        )

        median_rating = (
            filtered_df[
                "Rating_Score"
            ].median()
        )

        if pd.isna(median_rating):

            median_rating = 3.0

        filtered_df[
            "Rating_Score"
        ] = (
            filtered_df[
                "Rating_Score"
            ]
            .fillna(median_rating)
            / 5
        ).clip(0, 1)

    else:

        filtered_df[
            "Rating_Score"
        ] = 0.5

    # =========================================================
    # RECOMMENDATION SCORE
    #
    # ORIGINAL LOGIC — UNCHANGED
    # =========================================================

    filtered_df[
        "Recommendation_Score"
    ] = (
        0.60
        * filtered_df[
            "Tourism_Density_Suitability"
        ]

        + 0.30
        * filtered_df[
            "Crowd_Suitability"
        ]

        + 0.10
        * filtered_df[
            "Rating_Score"
        ]
    )

    # =========================================================
    # SORT RECOMMENDATIONS
    # =========================================================

    filtered_df = (
        filtered_df
        .sort_values(
            "Recommendation_Score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # =========================================================
    # BUDGET REFERENCE
    # =========================================================

    receipt_budget = receipt.copy()

    if not receipt_budget.empty:

        # -----------------------------------------------------
        # Clean receipt data
        # -----------------------------------------------------

        receipt_budget[
            receipt_year
        ] = pd.to_numeric(
            receipt_budget[
                receipt_year
            ],
            errors="coerce"
        )

        receipt_budget[
            receipt_value
        ] = pd.to_numeric(
            receipt_budget[
                receipt_value
            ],
            errors="coerce"
        )

        # -----------------------------------------------------
        # Latest available receipt year
        # -----------------------------------------------------

        valid_receipt_years = (
            receipt_budget[
                receipt_budget[
                    receipt_year
                ].notna()
            ]
        )

        if not valid_receipt_years.empty:

            latest_receipt_year = (
                valid_receipt_years[
                    receipt_year
                ].max()
            )

            receipt_budget = (
                receipt_budget[
                    receipt_budget[
                        receipt_year
                    ]
                    == latest_receipt_year
                ]
                .copy()
            )

        # -----------------------------------------------------
        # Select expenditure type
        # -----------------------------------------------------

        if travel_type == "Same-Day Trip":

            selected_receipt_type = (
                "Average Same Day Receipts per Trip (RM)"
            )

        else:

            selected_receipt_type = (
                "Average Overnight Receipts per Trip (RM)"
            )

        receipt_budget = (
            receipt_budget[
                receipt_budget[
                    receipt_type
                ]
                .astype(str)
                .str.strip()
                == selected_receipt_type
            ]
            .copy()
        )

        # -----------------------------------------------------
        # Keep State + Expenditure
        # -----------------------------------------------------

        if not receipt_budget.empty:

            receipt_budget = (
                receipt_budget[
                    [
                        receipt_state,
                        receipt_value
                    ]
                ]
                .rename(
                    columns={
                        receipt_state:
                            "state_std",

                        receipt_value:
                            "Average_Travel_Expenditure"
                    }
                )
            )

            receipt_budget[
                "state_std"
            ] = (
                receipt_budget[
                    "state_std"
                ]
                .astype(str)
                .str.strip()
            )

            # -------------------------------------------------
            # Merge expenditure into recommendations
            # -------------------------------------------------

            filtered_df = filtered_df.merge(
                receipt_budget,
                on="state_std",
                how="left"
            )

        else:

            filtered_df[
                "Average_Travel_Expenditure"
            ] = np.nan

    else:

        filtered_df[
            "Average_Travel_Expenditure"
        ] = np.nan

    # =========================================================
    # BUDGET STATUS
    #
    # Budget does NOT affect recommendation score.
    # It is only an affordability reference.
    # =========================================================

    def budget_status(value):

        if pd.isna(value):

            return "ℹ️ Benchmark unavailable"

        elif value <= user_budget:

            return "🟢 Within Budget"

        else:

            return "🟡 Above Budget"

    filtered_df[
        "Budget_Status"
    ] = filtered_df[
        "Average_Travel_Expenditure"
    ].apply(
        budget_status
    )

    # =========================================================
    # TOP N RECOMMENDATIONS
    # =========================================================

    top_n_df = (
        filtered_df
        .head(top_n)
        .copy()
    )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    st.divider()

    st.subheader(
        "🌱 Your Recommended Destinations"
    )

    st.caption(
        "Recommendations combine tourism density suitability, "
        "destination popularity, your preferences, and visitor ratings."
    )
    # =========================================================
    # RECOMMENDATION CARDS
    # =========================================================

    for i, (_, r) in enumerate(
        top_n_df.iterrows(),
        1
    ):

        with st.container(border=True):

            left, middle, right = st.columns(
                [2.2, 2, 1]
            )

            # -------------------------------------------------
            # LEFT COLUMN
            # -------------------------------------------------

            with left:

                st.markdown(
                    f"### {i}. {r['name']}"
                )

                st.write(
                    f"📍 {r['city']}, "
                    f"{r['state_std']}"
                )

                st.write(
                    f"🎨 {r['Theme']}"
                )

                st.write(
                    "🌱 Recommended based on "
                    "your selected preferences"
                )

            # -------------------------------------------------
            # MIDDLE COLUMN
            # -------------------------------------------------

            with middle:

                rating_value = (
                    float(r["rating"])
                    if pd.notna(r["rating"])
                    else 0
                )

                reviews_value = (
                    int(r["reviews"])
                    if pd.notna(r["reviews"])
                    else 0
                )

                st.write(
                    f"⭐ **Rating:** "
                    f"{rating_value:.1f}/5"
                )

                st.write(
                    f"💬 **Reviews:** "
                    f"{reviews_value:,}"
                )

                st.write(
                    f"🏙️ **Tourist Density:** "
                    f"{r['Tourism_Density_Category']}"
                )

                if (
                    pd.notna(
                        r[
                            "Average_Travel_Expenditure"
                        ]
                    )
                ):

                    expenditure_value = float(
                        r[
                            "Average_Travel_Expenditure"
                        ]
                    )

                    st.write(
                        f"💰 **Avg. Travel Expenditure:** "
                        f"RM {expenditure_value:,.0f}"
                    )

                    st.write(
                        f"**Budget Status:** "
                        f"{r['Budget_Status']}"
                    )

                else:

                    st.write(
                        "💰 **Avg. Travel Expenditure:** "
                        "Benchmark unavailable"
                    )

            # -------------------------------------------------
            # RIGHT COLUMN
            # -------------------------------------------------

            with right:

                st.metric(
                    "Match Score",
                    f"{r['Recommendation_Score']:.2f}"
                )

            # -------------------------------------------------
            # GOOGLE MAPS LINK
            # -------------------------------------------------

            if (
                "location_link" in r.index
                and pd.notna(
                    r["location_link"]
                )
                and str(
                    r["location_link"]
                ).strip()
            ):

                st.markdown(
                    f"[📍 Open in Google Maps]"
                    f"({r['location_link']})"
                )

    # =========================================================
    # MAP
    # =========================================================

    st.divider()

    st.subheader(
        "🗺️ Recommended Destination Map"
    )

    valid_map_df = (
        top_n_df
        .dropna(
            subset=[
                "latitude",
                "longitude"
            ]
        )
        .copy()
    )

    if not valid_map_df.empty:

        center_lat = (
            valid_map_df[
                "latitude"
            ].mean()
        )

        center_lon = (
            valid_map_df[
                "longitude"
            ].mean()
        )

        m = folium.Map(
            location=[
                center_lat,
                center_lon
            ],
            zoom_start=7
        )

        for _, r in valid_map_df.iterrows():

            rating_for_map = (
                float(r["rating"])
                if pd.notna(r["rating"])
                else 0
            )

            popup_html = f"""
            <b>{r['name']}</b><br>
            📍 {r['city']}, {r['state_std']}<br>
            🎨 Theme: {r['Theme']}<br>
            ⭐ Rating: {rating_for_map:.1f}/5<br>
            🏙️  Tourist Density:
            {r['Tourism_Density_Category']}<br>
            🤖 Match Score:
            {r['Recommendation_Score']:.2f}
            """

            folium.Marker(
                location=[
                    r["latitude"],
                    r["longitude"]
                ],
                popup=folium.Popup(
                    popup_html,
                    max_width=300
                ),
                tooltip=r["name"]
            ).add_to(m)

        st_folium(
            m,
            width="stretch",
            height=550
        )

    else:

        st.warning(
            "Map coordinates are not available "
            "for the recommended attractions."
        )

    # =========================================================
    # SOLUTION BOX
    # =========================================================

    st.markdown(
        """
        <div class="solution-box">
        <h4>🌱 From Accessibility to Opportunity</h4>
        <p>
        MyDecouple AI helps travellers discover alternative
        destinations that match their preferences while supporting
        a more balanced distribution of tourism activity across
        Malaysia.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )
# -----------------------------------------------------------------------------
# Part 4: B2G Government Policy What-If Simulator
# -----------------------------------------------------------------------------
elif app_mode == " WHAT-IF SCENARIO":
   # =========================================================
    # PAGE HEADER
    # =========================================================

    st.markdown(
        "<h1 style='text-align:center;'>🏛️ What-If Simulator</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center; font-size:18px;'>
        Explore how hypothetical changes in tourism-related
        development indicators may affect predicted tourist density.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # =========================================================
    # 2. SELECT STATE
    # =========================================================

    st.markdown("## 1️. Select State")

    available_states = sorted(
        df_policy_model["state_std"]
        .dropna()
        .unique()
    )

    selected_state = st.selectbox(
        "Choose a state for the policy scenario:",
        available_states
    )


    # ---------------------------------------------------------
    # Get selected state data
    # ---------------------------------------------------------

    state_data = df_policy_model[
        df_policy_model["state_std"] == selected_state
    ].copy()

    if state_data.empty:

        st.warning(
            "No policy model data available for the selected state."
        )

        st.stop()


    # ---------------------------------------------------------
    # Latest available year
    # ---------------------------------------------------------

    latest_year = state_data["year"].max()

    current_row = state_data[
        state_data["year"] == latest_year
    ].iloc[0]


    # =========================================================
    # 3. CURRENT CONDITION
    # =========================================================

    st.markdown("## 2️. Current Condition")

    st.caption(
        f"Latest available model year: {int(latest_year)}"
    )


    # ---------------------------------------------------------
    # Current RAW values
    #
    # These are reconstructed from the processed model
    # features and are used as the baseline for scenarios.
    # ---------------------------------------------------------

    raw_current_values = {

        "X1": float(
            np.expm1(
                current_row[
                    "x1_transit_density_log"
                ]
            )
        ),

        "X2": float(
            current_row[
                "x2_digital_index"
            ]
        ),

        "X3": float(
            current_row[
                "x3_state_score"
            ]
        ),

        "X4": float(
            np.expm1(
                current_row[
                    "x4_accommodation_density_log"
                ]
            )
        ),

        "X5": float(
            np.expm1(
                current_row[
                    "x5_gdp_per_capita_log"
                ]
            )
        )
    }


    # ---------------------------------------------------------
    # Display current indicators
    # ---------------------------------------------------------

    current_col1, current_col2, current_col3 = st.columns(3)

    with current_col1:

        st.metric(
            "Transit Hub Density",
            f"{raw_current_values['X1']:,.4f}"
        )

        st.metric(
            "Digital Polarization Index",
            f"{raw_current_values['X2']:,.4f}"
        )


    with current_col2:

        st.metric(
            "State Average Score",
            f"{raw_current_values['X3']:,.4f}"
        )

        st.metric(
            "Accommodation Capacity Density",
            f"{raw_current_values['X4']:,.4f}"
        )


    with current_col3:

        st.metric(
            "GDP per Capita",
            f"RM {raw_current_values['X5']:,.2f}"
        )


    st.markdown("---")


    # =========================================================
    # 4. POLICY SCENARIO
    # =========================================================

    st.markdown("## 3️. What-If Scenario")

    st.caption(
        "Adjust each indicator to simulate a hypothetical "
        "policy or development scenario."
    )


    scenario_col1, scenario_col2 = st.columns(2)


    # ---------------------------------------------------------
    # X1
    # ---------------------------------------------------------

    with scenario_col1:

        x1_change = st.slider(
            "X1 • Interstate Transit Hub Density",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            format="%d%%"
        )


    # ---------------------------------------------------------
    # X2
    # ---------------------------------------------------------

    with scenario_col2:

        x2_change = st.slider(
            "X2 • Top 5 Digital Polarization Index",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            format="%d%%"
        )


    scenario_col3, scenario_col4 = st.columns(2)


    # ---------------------------------------------------------
    # X3
    # ---------------------------------------------------------

    with scenario_col3:

        x3_change = st.slider(
            "X3 • Yearly Average Score",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            format="%d%%"
        )


    # ---------------------------------------------------------
    # X4
    # ---------------------------------------------------------

    with scenario_col4:

        x4_change = st.slider(
            "X4 • Accommodation Capacity Density",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            format="%d%%"
        )


    # ---------------------------------------------------------
    # X5
    # ---------------------------------------------------------

    x5_change = st.slider(
        "X5 • GDP per Capita",
        min_value=-100,
        max_value=100,
        value=0,
        step=5,
        format="%d%%"
    )


    # =========================================================
    # 5. CALCULATE SCENARIO RAW VALUES
    # =========================================================

    scenario_x1_raw = (
        raw_current_values["X1"]
        * (1 + x1_change / 100)
    )

    scenario_x2_raw = (
        raw_current_values["X2"]
        * (1 + x2_change / 100)
    )

    scenario_x3_raw = (
        raw_current_values["X3"]
        * (1 + x3_change / 100)
    )

    scenario_x4_raw = (
        raw_current_values["X4"]
        * (1 + x4_change / 100)
    )

    scenario_x5_raw = (
        raw_current_values["X5"]
        * (1 + x5_change / 100)
    )


    # Prevent negative values
    scenario_x1_raw = max(
        scenario_x1_raw,
        0
    )

    scenario_x2_raw = max(
        scenario_x2_raw,
        0
    )

    scenario_x3_raw = max(
        scenario_x3_raw,
        0
    )

    scenario_x4_raw = max(
        scenario_x4_raw,
        0
    )

    scenario_x5_raw = max(
        scenario_x5_raw,
        0
    )


    # =========================================================
    # 6. CONVERT SCENARIO TO MODEL FEATURES
    # =========================================================
    current_model_input = pd.DataFrame([{
    "x1_transit_density_log":
        current_row["x1_transit_density_log"],

    "x2_digital_index":
        current_row["x2_digital_index"],

    "x3_state_score":
        current_row["x3_state_score"],

    "x4_accommodation_density_log":
        current_row["x4_accommodation_density_log"],

    "x5_gdp_per_capita_log":
        current_row["x5_gdp_per_capita_log"]
}])


    # =========================================================
    # 6. CONVERT SCENARIO TO MODEL FEATURES
    # =========================================================
    scenario_model_input = pd.DataFrame([{
        # X1: Raw value → log(1 + X1)
        "x1_transit_density_log":
            np.log1p(
                max(scenario_x1_raw, 0)
            ),

        # X2: No log transformation
        "x2_digital_index":
            scenario_x2_raw,

        # X3: No log transformation
        "x3_state_score":
            scenario_x3_raw,

        # X4: Raw value → log(1 + X4)
        "x4_accommodation_density_log":
            np.log1p(
                max(scenario_x4_raw, 0)
            ),

        # X5: Raw value → log(1 + X5)
        "x5_gdp_per_capita_log":
            np.log1p(
                max(scenario_x5_raw, 0)
            )
    }])


    # =========================================================
    # 7. RUN SIMULATION
    # =========================================================

    st.markdown("## 4️. Simulation Results")

    run_simulation = st.button(
        "🚀 Run What-If Simulation",
        use_container_width=True
    )


    if run_simulation:

        # -----------------------------------------------------
        # Current prediction
        # -----------------------------------------------------
        current_prediction = float(
            current_row["y_tourist_density"]
        )


        # -----------------------------------------------------
        # Scenario prediction
        # -----------------------------------------------------

        scenario_prediction_log = gbr_model.predict(
            scenario_model_input
        )[0]

        scenario_prediction = np.expm1(
            scenario_prediction_log
        )

        # -----------------------------------------------------
        # Scenario Tourism Density Classification
        # -----------------------------------------------------
        if scenario_prediction < 8224.73:
            scenario_tourism_level = "Low"
        elif scenario_prediction <= 10467.83:
            scenario_tourism_level = "Moderate"
        else:
            scenario_tourism_level = "High"


        # -----------------------------------------------------
        # Percentage change
        # -----------------------------------------------------

        if current_prediction != 0:

            prediction_change_pct = (
                (
                    scenario_prediction
                    - current_prediction
                )
                / current_prediction
            ) * 100

        else:

            prediction_change_pct = np.nan


        # =====================================================
        # 8. KPI RESULTS
        # =====================================================
        result_col1, result_col2, result_col3, result_col4 = st.columns(4)
        # =========================================================
        # ACTUAL TOURIST DENSITY
        # =========================================================
        with result_col1:
            st.markdown(
                "<div style='font-size:14px; color:gray;'>"
                "Actual Tourist Density"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="
                font-size:28px;
                font-weight:600;
                margin-top:5px;
                ">
                {current_prediction:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
        # =========================================================
        # SCENARIO PREDICTED TOURIST DENSITY
        # =========================================================
        with result_col2:
            st.markdown(
                "<div style='font-size:14px; color:gray;'>"
                "Scenario Predicted Tourist Density"
                "</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div style="
                font-size:28px;
                font-weight:600;
                margin-top:5px;
                ">
                {scenario_prediction:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )
        # =========================================================
        # CHANGE IN TOURIST DENSITY
        # =========================================================
        with result_col3:
            st.markdown(
                "<div style='font-size:14px; color:gray;'>"
                "Change in Tourist Density"
                "</div>",
                unsafe_allow_html=True
            )
            if pd.notna(prediction_change_pct):
                if prediction_change_pct > 0:
                    change_color = "#d62728"      # Red
                elif prediction_change_pct < 0:
                    change_color = "#2ca02c"      # Green
                else:
                    change_color = "#808080"      # Grey
                st.markdown(
                    f"""
                    <div style="
                    font-size:28px;
                    font-weight:600;
                    color:{change_color};
                    margin-top:5px;
                    ">
                    {prediction_change_pct:+.2f}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style="
                    font-size:28px;
                    color:#808080;
                    margin-top:5px;
                    ">
                    N/A
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        # =========================================================
        # SCENARIO TOURISM LEVEL
        # =========================================================
        with result_col4:
            st.markdown(
                "<div style='font-size:14px; color:gray;'>"
                "Scenario Tourism Level"
                "</div>",
                unsafe_allow_html=True
            )
            
            if scenario_tourism_level == "High":
                level_color = "#d62728"      # Red
            elif scenario_tourism_level == "Moderate":
                level_color = "#e6a700"      # Yellow
            else:
                level_color = "#2ca02c"      # Green
            st.markdown(
                f"""
                <div style="
                font-size:28px;
                font-weight:600;
                color:{level_color};
                margin-top:5px;
                ">
                {scenario_tourism_level}
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # 10. SCENARIO INTERPRETATION
        # =====================================================
        st.markdown("### 📊 Scenario Interpretation")
        if pd.notna(prediction_change_pct):
            if prediction_change_pct > 0:
                st.warning(
                    f"The policy scenario is associated with a "
                    f"{prediction_change_pct:.2f}% increase in predicted "
                    f"tourist density compared with the current condition."
                )
            
            elif prediction_change_pct < 0:
                st.success(
                    f"The policy scenario is associated with a "
                    f"{abs(prediction_change_pct):.2f}% decrease in predicted "
                    f"tourist density compared with the current condition."
                )
            
            else:
                st.info(
                    "The policy scenario produces no change in predicted "
                    "tourist density compared with the current condition."
                )
        # ---------------------------------------------------------
        # Tourism Density Level Interpretation
        # ---------------------------------------------------------
        if scenario_tourism_level == "High":
            st.error(
                "🔴 High: The scenario indicates a high concentration "
                "of tourist activity."
            )
        elif scenario_tourism_level == "Moderate":
            st.warning(
                "🟡 Moderate: The scenario indicates a moderate level "
                "of tourist activity."
            )
        else:
            st.success(
                "🟢 Low: The scenario indicates a relatively low "
                "concentration of tourist activity."
            )
        # ---------------------------------------------------------
        # Threshold Reference
        # ---------------------------------------------------------
        st.caption(
            "Tourism Density Classification: "
            "Low: Tourist density < 8,224.73 | "
            "Moderate = Tourist density between 8,224.73 and 10,467.83 | "
            "High:Tourist density > 10,467.83"
        )
        st.caption(
            "The simulation represents a model-based what-if scenario. "
            "It does not establish a causal policy effect or guarantee "
            "a real-world change in tourist density."
        )


        # =====================================================
        # 11. SCENARIO VARIABLE COMPARISON
        # =====================================================
        st.markdown("### 🔍 Scenario Variable Comparison")
        st.caption(
            "Comparison of the current and simulated values for each "
            "tourism-related indicator. Values are shown in their original scale."
        )
        input_comparison = pd.DataFrame({
            "Feature": [
                "X1 • Transit Hub Density",
                "X2 • Digital Polarization Index",
                "X3 • State Average Score",
                "X4 • Accommodation Capacity Density",
                "X5 • GDP per Capita"
            ],
            "Current": [
                raw_current_values["X1"],
                raw_current_values["X2"],
                raw_current_values["X3"],
                raw_current_values["X4"],
                raw_current_values["X5"]
            ],
            "Scenario": [
                scenario_x1_raw,
                scenario_x2_raw,
                scenario_x3_raw,
                scenario_x4_raw,
                scenario_x5_raw
            ]
        })
        st.dataframe(
            input_comparison,
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------------------------------------------
# Part 5: About (Team Member Information)
# -----------------------------------------------------------------------------
elif app_mode == "ABOUT":
    st.title("Management Team")
    st.caption("Key Leadership & Platform Contributors for MyDecouple AI Platform")
    st.write("")

    # 辅助函数：自动读取本地 JPG/PNG 图片并转为 Base64 格式
    def get_image_base64(image_path):
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            # 根据后缀识别类型
            ext = image_path.split('.')[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
            return f"data:{mime};base64,{encoded}"
        else:
            # 如果找不到本地图片，自动用占位图兜底，防止报错
            return "https://via.placeholder.com/150"

    # 1. 在这里填写你的本地 JPG 图片文件名/路径
    team_members = [
        {
            "name": "Ge Zi Jenn",
            "role": "PROJECT LEAD & MACHINE LEARNING SPECIALIST",
            "phone": "+6011-10557980",
            "email": "zijenn@gmail.com",
            "image_path": "zijenn.png"  # 👈 替换为你的本地 JPG 文件名
        },
        {
            "name": "Lai Rui Ni",
            "role": "DASHBOARD DEVELOPER",
            "phone": "+6018-9828573",
            "email": "ruini@gmail.com",
            "image_path": "ruini.jpeg"  # 👈 替换为你的本地 JPG 文件名
        },
        {
            "name": "Loo Hui Qian",
            "role": "WEBSITE DEVELOPER",
            "phone": "+6011-23173009",
            "email": "huiqian@gmail.com",
            "image_path": "huiqian.png"  # 👈 替换为你的本地 JPG 文件名
        },
        {
            "name": "Loo Zu Yi",
            "role": "DATA ANALYTICS & RESEARCH SPECIALIST",
            "phone": "+6018-3172448",
            "email": "zuyi@gmail.com",
            "image_path": "zuyi.png"  # 👈 替换为你的本地 JPG 文件名
        }
    ]

    # 2. 渲染成员卡片
    for member in team_members:
        # 将本地图片路径转换为 Base64 编码字符串
        img_src = get_image_base64(member["image_path"])

        card_html = f"""<div class="member-card">
<img src="{img_src}" class="member-avatar">
<div>
<div class="member-name">{member['name']}</div>
<div class="member-role">{member['role']}</div>
<div class="member-contact">
📞 <b>Phone:</b> {member['phone']} <br>
✉️ <b>Email:</b> <a href="mailto:{member['email']}">{member['email']}</a>
</div>
</div>
</div>"""
        st.markdown(card_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Part 6: Official Website Footer Component
# -----------------------------------------------------------------------------
footer_html = f"""<div class="custom-footer-container">
<div class="custom-footer-top">
<div class="footer-col-logo">
<img src="{logo_src}">
<div>
<div class="footer-logo-title">MyDecouple AI</div>
<div class="footer-logo-sub">Smart Tourism Intelligence Platform</div>
</div>
</div>
<div class="footer-col-address">
<strong>MYDECOUPLE AI HEADQUARTERS</strong>
Universiti Putra Malaysia (UPM)<br>
43400 UPM Serdang, Selangor Darul Ehsan,<br>
Malaysia
</div>
<div class="footer-col-contact">
<strong>Phone:</strong> +601x-xxxxxxxx<br>
<strong>Email:</strong> 4sight@gmail.com
</div>
</div>
</div>
<div class="custom-footer-bottom">
© 2026 MyDecouple AI Platform (UPM). All rights reserved. <br style="margin-bottom:4px;">
<a href="#">Privacy Policy</a> | <a href="#">Sitemap</a> | <span>Last updated: 20 September 2026</span>
</div>
</div>"""

st.markdown(footer_html, unsafe_allow_html=True)
