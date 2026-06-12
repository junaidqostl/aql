"""
AQL Inspection Calculator
Based on ISO 2859-1 / ANSI/ASQ Z1.4 standard tables
"""

import streamlit as st

# ─────────────────────────────────────────────
# ISO 2859-1 DATA TABLES
# ─────────────────────────────────────────────

# Lot size ranges → Code Letter per Inspection Level
# Format: (min, max) → {level: code_letter}
LOT_SIZE_CODE_LETTER = [
    ((2,        8),       {"I": "A", "II": "A", "III": "B", "S-1": "A", "S-2": "A", "S-3": "A", "S-4": "A"}),
    ((9,        15),      {"I": "A", "II": "B", "III": "C", "S-1": "A", "S-2": "A", "S-3": "A", "S-4": "A"}),
    ((16,       25),      {"I": "B", "II": "C", "III": "D", "S-1": "A", "S-2": "A", "S-3": "B", "S-4": "B"}),
    ((26,       50),      {"I": "C", "II": "D", "III": "E", "S-1": "A", "S-2": "B", "S-3": "B", "S-4": "C"}),
    ((51,       90),      {"I": "C", "II": "E", "III": "F", "S-1": "B", "S-2": "B", "S-3": "C", "S-4": "C"}),
    ((91,       150),     {"I": "D", "II": "F", "III": "G", "S-1": "B", "S-2": "B", "S-3": "C", "S-4": "D"}),
    ((151,      280),     {"I": "E", "II": "G", "III": "H", "S-1": "B", "S-2": "C", "S-3": "D", "S-4": "E"}),
    ((281,      500),     {"I": "F", "II": "H", "III": "J", "S-1": "B", "S-2": "C", "S-3": "D", "S-4": "E"}),
    ((501,      1200),    {"I": "G", "II": "J", "III": "K", "S-1": "C", "S-2": "C", "S-3": "E", "S-4": "F"}),
    ((1201,     3200),    {"I": "H", "II": "K", "III": "L", "S-1": "C", "S-2": "D", "S-3": "E", "S-4": "G"}),
    ((3201,     10000),   {"I": "J", "II": "L", "III": "M", "S-1": "C", "S-2": "D", "S-3": "F", "S-4": "H"}),
    ((10001,    35000),   {"I": "K", "II": "M", "III": "N", "S-1": "C", "S-2": "D", "S-3": "F", "S-4": "J"}),
    ((35001,    150000),  {"I": "L", "II": "N", "III": "P", "S-1": "D", "S-2": "E", "S-3": "G", "S-4": "J"}),
    ((150001,   500000),  {"I": "M", "II": "P", "III": "Q", "S-1": "D", "S-2": "E", "S-3": "G", "S-4": "K"}),
    ((500001,   9999999), {"I": "N", "II": "Q", "III": "R", "S-1": "D", "S-2": "E", "S-3": "H", "S-4": "K"}),
]

# Sample sizes by code letter
SAMPLE_SIZES = {
    "A": 2,  "B": 3,  "C": 5,  "D": 8,   "E": 13,
    "F": 20, "G": 32, "H": 50, "J": 80,  "K": 125,
    "L": 200,"M": 315,"N": 500,"P": 800, "Q": 1250, "R": 2000,
}

# AQL acceptance/rejection numbers per code letter and AQL level
# Format: code_letter → {aql_str: (Ac, Re)}
# Ac = Acceptance Number, Re = Rejection Number
# None = "use next larger sample size code" (arrow in standard)
AQL_TABLE = {
    # ── A ──
    "A": {
        "0.010": None, "0.015": None, "0.025": None, "0.040": None,
        "0.065": (0, 1), "0.10": (0, 1), "0.15": (0, 1),
        "0.25": (0, 1),  "0.40": (0, 1), "0.65": (0, 1),
        "1.0": (0, 1),   "1.5": (0, 1),  "2.5": (0, 1),
        "4.0": (0, 1),   "6.5": (0, 1),  "10": (0, 1),
        "15": (0, 1),    "25": (0, 1),   "40": (0, 1), "65": (0, 1),
    },
    # ── B ──
    "B": {
        "0.010": None, "0.015": None, "0.025": None,
        "0.040": None, "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (0, 1),
        "0.40": (0, 1), "0.65": (0, 1), "1.0": (0, 1),
        "1.5": (0, 1),  "2.5": (0, 1),  "4.0": (0, 1),
        "6.5": (0, 1),  "10": (1, 2),   "15": (1, 2),
        "25": (2, 3),   "40": (3, 4),   "65": (5, 6),
    },
    # ── C ──
    "C": {
        "0.010": None, "0.015": None, "0.025": None,
        "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (0, 1),
        "0.40": (0, 1), "0.65": (0, 1), "1.0": (0, 1),
        "1.5": (0, 1),  "2.5": (0, 1),  "4.0": (1, 2),
        "6.5": (1, 2),  "10": (1, 2),   "15": (2, 3),
        "25": (3, 4),   "40": (5, 6),   "65": (7, 8),
    },
    # ── D ──
    "D": {
        "0.010": None, "0.015": None,
        "0.025": (0, 1), "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (0, 1),
        "0.40": (0, 1), "0.65": (0, 1), "1.0": (0, 1),
        "1.5": (0, 1),  "2.5": (1, 2),  "4.0": (1, 2),
        "6.5": (2, 3),  "10": (2, 3),   "15": (3, 4),
        "25": (5, 6),   "40": (7, 8),   "65": (10, 11),
    },
    # ── E ──
    "E": {
        "0.010": None,
        "0.015": (0, 1), "0.025": (0, 1), "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (0, 1),
        "0.40": (0, 1), "0.65": (0, 1), "1.0": (0, 1),
        "1.5": (1, 2),  "2.5": (1, 2),  "4.0": (2, 3),
        "6.5": (3, 4),  "10": (3, 4),   "15": (5, 6),
        "25": (7, 8),   "40": (10, 11), "65": (14, 15),
    },
    # ── F ──
    "F": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (0, 1),
        "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (0, 1),
        "0.40": (0, 1), "0.65": (1, 2), "1.0": (1, 2),
        "1.5": (1, 2),  "2.5": (2, 3),  "4.0": (3, 4),
        "6.5": (5, 6),  "10": (5, 6),   "15": (7, 8),
        "25": (10, 11), "40": (14, 15), "65": (21, 22),
    },
    # ── G ──
    "G": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (0, 1),
        "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (0, 1), "0.25": (1, 2),
        "0.40": (1, 2), "0.65": (1, 2), "1.0": (2, 3),
        "1.5": (2, 3),  "2.5": (3, 4),  "4.0": (5, 6),
        "6.5": (7, 8),  "10": (7, 8),   "15": (10, 11),
        "25": (14, 15), "40": (21, 22), "65": None,
    },
    # ── H ──
    "H": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (0, 1),
        "0.040": (0, 1), "0.065": (0, 1),
        "0.10": (0, 1), "0.15": (1, 2), "0.25": (1, 2),
        "0.40": (2, 3), "0.65": (2, 3), "1.0": (3, 4),
        "1.5": (3, 4),  "2.5": (5, 6),  "4.0": (7, 8),
        "6.5": (10, 11),"10": (10, 11), "15": (14, 15),
        "25": (21, 22), "40": None,     "65": None,
    },
    # ── J ──
    "J": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (0, 1),
        "0.040": (0, 1), "0.065": (1, 2),
        "0.10": (1, 2), "0.15": (1, 2), "0.25": (2, 3),
        "0.40": (3, 4), "0.65": (3, 4), "1.0": (5, 6),
        "1.5": (5, 6),  "2.5": (7, 8),  "4.0": (10, 11),
        "6.5": (14, 15),"10": (14, 15), "15": (21, 22),
        "25": None,     "40": None,     "65": None,
    },
    # ── K ──
    "K": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (0, 1),
        "0.040": (1, 2), "0.065": (1, 2),
        "0.10": (1, 2), "0.15": (2, 3), "0.25": (3, 4),
        "0.40": (5, 6), "0.65": (5, 6), "1.0": (7, 8),
        "1.5": (7, 8),  "2.5": (10, 11),"4.0": (14, 15),
        "6.5": (21, 22),"10": (21, 22), "15": None,
        "25": None,     "40": None,     "65": None,
    },
    # ── L ──
    "L": {
        "0.010": (0, 1), "0.015": (0, 1), "0.025": (1, 2),
        "0.040": (1, 2), "0.065": (2, 3),
        "0.10": (2, 3), "0.15": (3, 4), "0.25": (5, 6),
        "0.40": (7, 8), "0.65": (7, 8), "1.0": (10, 11),
        "1.5": (10, 11),"2.5": (14, 15),"4.0": (21, 22),
        "6.5": None,    "10": None,     "15": None,
        "25": None,     "40": None,     "65": None,
    },
    # ── M ──
    "M": {
        "0.010": (0, 1), "0.015": (1, 2), "0.025": (1, 2),
        "0.040": (2, 3), "0.065": (3, 4),
        "0.10": (3, 4), "0.15": (5, 6), "0.25": (7, 8),
        "0.40": (10, 11),"0.65": (10, 11),"1.0": (14, 15),
        "1.5": (14, 15),"2.5": (21, 22),"4.0": None,
        "6.5": None,   "10": None,      "15": None,
        "25": None,    "40": None,      "65": None,
    },
    # ── N ──
    "N": {
        "0.010": (1, 2), "0.015": (1, 2), "0.025": (2, 3),
        "0.040": (3, 4), "0.065": (5, 6),
        "0.10": (5, 6), "0.15": (7, 8), "0.25": (10, 11),
        "0.40": (14, 15),"0.65": (14, 15),"1.0": (21, 22),
        "1.5": (21, 22),"2.5": None,    "4.0": None,
        "6.5": None,   "10": None,      "15": None,
        "25": None,    "40": None,      "65": None,
    },
    # ── P ──
    "P": {
        "0.010": (1, 2), "0.015": (2, 3), "0.025": (3, 4),
        "0.040": (5, 6), "0.065": (7, 8),
        "0.10": (7, 8), "0.15": (10, 11),"0.25": (14, 15),
        "0.40": (21, 22),"0.65": (21, 22),"1.0": None,
        "1.5": None,   "2.5": None,     "4.0": None,
        "6.5": None,   "10": None,      "15": None,
        "25": None,    "40": None,      "65": None,
    },
    # ── Q ──
    "Q": {
        "0.010": (2, 3), "0.015": (3, 4), "0.025": (5, 6),
        "0.040": (7, 8), "0.065": (10, 11),
        "0.10": (10, 11),"0.15": (14, 15),"0.25": (21, 22),
        "0.40": None,  "0.65": None,    "1.0": None,
        "1.5": None,   "2.5": None,     "4.0": None,
        "6.5": None,   "10": None,      "15": None,
        "25": None,    "40": None,      "65": None,
    },
    # ── R ──
    "R": {
        "0.010": (3, 4), "0.015": (5, 6), "0.025": (7, 8),
        "0.040": (10, 11),"0.065": (14, 15),
        "0.10": (14, 15),"0.15": (21, 22),"0.25": None,
        "0.40": None,  "0.65": None,    "1.0": None,
        "1.5": None,   "2.5": None,     "4.0": None,
        "6.5": None,   "10": None,      "15": None,
        "25": None,    "40": None,      "65": None,
    },
}

# Standard AQL levels available
AQL_OPTIONS = [
    "0.010", "0.015", "0.025", "0.040", "0.065",
    "0.10",  "0.15",  "0.25",  "0.40",  "0.65",
    "1.0",   "1.5",   "2.5",   "4.0",   "6.5",
    "10",    "15",    "25",    "40",    "65",
]

INSPECTION_LEVELS = ["S-1", "S-2", "S-3", "S-4", "I", "II", "III"]

# ─────────────────────────────────────────────
# LOOKUP FUNCTIONS
# ─────────────────────────────────────────────

def get_code_letter(lot_size: int, level: str) -> str | None:
    for (lo, hi), level_map in LOT_SIZE_CODE_LETTER:
        if lo <= lot_size <= hi:
            return level_map.get(level)
    return None


def get_aql_limits(code_letter: str, aql_str: str):
    """
    Returns (Ac, Re) tuple or None (arrow — use next code letter).
    Walks up the code letters if an arrow is encountered.
    """
    letter_order = list(SAMPLE_SIZES.keys())  # A … R
    letter = code_letter

    for _ in range(len(letter_order)):
        row = AQL_TABLE.get(letter, {})
        result = row.get(aql_str)
        if result is not None:
            return result, letter  # (Ac, Re), effective_letter
        # Move to the next larger letter (down-arrow in standard)
        idx = letter_order.index(letter)
        if idx + 1 >= len(letter_order):
            return None, letter
        letter = letter_order[idx + 1]

    return None, code_letter


# ─────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AQL Inspection Calculator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── App background ── */
    .stApp {
        background: #0f1117;
    }

    /* ── Page header ── */
    .page-header {
        display: flex;
        align-items: baseline;
        gap: 16px;
        padding: 28px 0 6px 0;
        border-bottom: 1px solid #2a2d36;
        margin-bottom: 28px;
    }
    .page-header h1 {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.45rem;
        font-weight: 600;
        color: #e8eaf0;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .page-header .standard-tag {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        font-weight: 600;
        color: #5b6578;
        border: 1px solid #2a2d36;
        padding: 2px 8px;
        border-radius: 3px;
        letter-spacing: 0.5px;
    }

    /* ── Section labels ── */
    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        color: #5b6578;
        text-transform: uppercase;
        margin-bottom: 12px;
        margin-top: 4px;
    }

    /* ── Code letter badge ── */
    .code-letter-card {
        background: #161922;
        border: 1px solid #2a2d36;
        border-radius: 8px;
        padding: 20px 24px;
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 6px;
    }
    .code-letter-big {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 3.2rem;
        font-weight: 600;
        color: #4d9de0;
        line-height: 1;
    }
    .code-letter-meta {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .code-letter-meta .meta-label {
        font-size: 0.72rem;
        color: #5b6578;
        font-weight: 500;
        letter-spacing: 0.3px;
    }
    .code-letter-meta .meta-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.1rem;
        font-weight: 600;
        color: #c8ccd8;
    }

    /* ── Defect class cards ── */
    .defect-card {
        background: #161922;
        border: 1px solid #2a2d36;
        border-radius: 8px;
        padding: 18px 20px 14px 20px;
        margin-bottom: 10px;
        position: relative;
    }
    .defect-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .defect-class-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.8px;
        color: #8b92a5;
        text-transform: uppercase;
    }
    .defect-class-label.critical { color: #e05c5c; }
    .defect-class-label.major    { color: #e09d4d; }
    .defect-class-label.minor    { color: #4d9de0; }

    /* ── Result badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 12px;
        border-radius: 4px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .badge-pass {
        background: rgba(52, 168, 83, 0.15);
        border: 1px solid rgba(52, 168, 83, 0.4);
        color: #34a853;
    }
    .badge-fail {
        background: rgba(220, 53, 69, 0.15);
        border: 1px solid rgba(220, 53, 69, 0.4);
        color: #dc3545;
    }
    .badge-na {
        background: rgba(91, 101, 120, 0.2);
        border: 1px solid rgba(91, 101, 120, 0.3);
        color: #5b6578;
    }

    /* ── Ac/Re row ── */
    .acre-row {
        display: flex;
        gap: 10px;
        margin-top: 8px;
    }
    .acre-chip {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        color: #5b6578;
        background: #1e2230;
        border: 1px solid #2a2d36;
        border-radius: 4px;
        padding: 3px 10px;
    }
    .acre-chip span { color: #c8ccd8; font-weight: 600; }

    /* ── Overall verdict ── */
    .verdict-box {
        border-radius: 10px;
        padding: 28px 32px;
        display: flex;
        align-items: center;
        gap: 18px;
        margin-top: 10px;
    }
    .verdict-pass {
        background: rgba(52, 168, 83, 0.08);
        border: 2px solid rgba(52, 168, 83, 0.4);
    }
    .verdict-fail {
        background: rgba(220, 53, 69, 0.08);
        border: 2px solid rgba(220, 53, 69, 0.4);
    }
    .verdict-pending {
        background: rgba(91, 101, 120, 0.08);
        border: 2px solid rgba(91, 101, 120, 0.2);
    }
    .verdict-icon { font-size: 2.6rem; line-height: 1; }
    .verdict-text-main {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.6rem;
        font-weight: 600;
        line-height: 1.1;
    }
    .verdict-text-main.pass { color: #34a853; }
    .verdict-text-main.fail { color: #dc3545; }
    .verdict-text-main.pending { color: #5b6578; }
    .verdict-text-sub {
        font-size: 0.82rem;
        color: #5b6578;
        margin-top: 3px;
    }

    /* ── Streamlit overrides ── */
    .stNumberInput input, .stSelectbox > div > div {
        background: #161922 !important;
        border: 1px solid #2a2d36 !important;
        color: #e8eaf0 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        border-radius: 6px !important;
    }
    .stNumberInput input:focus, .stSelectbox > div > div:focus {
        border-color: #4d9de0 !important;
        box-shadow: 0 0 0 2px rgba(77, 157, 224, 0.2) !important;
    }
    label, .stSelectbox label {
        color: #8b92a5 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    .stSelectbox svg { color: #5b6578 !important; }
    div[data-testid="stHorizontalBlock"] { gap: 20px; }
    .stDivider { border-color: #2a2d36 !important; }

    /* ── Info box ── */
    .info-strip {
        background: rgba(77, 157, 224, 0.07);
        border-left: 3px solid #4d9de0;
        border-radius: 0 6px 6px 0;
        padding: 10px 14px;
        font-size: 0.8rem;
        color: #8b92a5;
        margin-top: 6px;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .info-strip strong { color: #c8ccd8; }

    /* ── Metrics row ── */
    .metrics-row {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .metric-chip {
        background: #161922;
        border: 1px solid #2a2d36;
        border-radius: 6px;
        padding: 10px 16px;
        display: flex;
        flex-direction: column;
        gap: 2px;
        min-width: 100px;
    }
    .metric-chip .mc-label {
        font-size: 0.68rem;
        color: #5b6578;
        letter-spacing: 0.5px;
        font-weight: 500;
        text-transform: uppercase;
    }
    .metric-chip .mc-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.15rem;
        font-weight: 600;
        color: #e8eaf0;
    }
    .metric-chip .mc-value.accent { color: #4d9de0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class="page-header">
    <h1>🔬 AQL Inspection Calculator</h1>
    <span class="standard-tag">ISO 2859-1 / ANSI ASQ Z1.4</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LAYOUT: two columns — inputs left, results right
# ─────────────────────────────────────────────

col_input, col_result = st.columns([1, 1.05], gap="large")

# ══════════════════════════════════════════════
# LEFT COLUMN — INPUTS
# ══════════════════════════════════════════════
with col_input:
    st.markdown('<div class="section-label">Lot Parameters</div>', unsafe_allow_html=True)

    lot_size = st.number_input(
        "Total Lot / Batch Size",
        min_value=2,
        max_value=9_999_999,
        value=1000,
        step=1,
        help="Total number of units in the lot or batch being inspected.",
    )

    inspection_level = st.selectbox(
        "Inspection Level",
        options=INSPECTION_LEVELS,
        index=INSPECTION_LEVELS.index("II"),
        help="General II is the default for most inspections. General I is less discriminating; General III is more. S levels are special/small-sample levels.",
    )

    st.markdown('<div class="section-label" style="margin-top:22px;">AQL Limits</div>', unsafe_allow_html=True)

    aql_col1, aql_col2, aql_col3 = st.columns(3)
    with aql_col1:
        aql_critical = st.selectbox(
            "🔴 Critical",
            options=AQL_OPTIONS,
            index=AQL_OPTIONS.index("0.065"),
            help="Defects that could harm users. Typically 0.065 or lower.",
        )
    with aql_col2:
        aql_major = st.selectbox(
            "🟠 Major",
            options=AQL_OPTIONS,
            index=AQL_OPTIONS.index("2.5"),
            help="Defects that affect functionality or appearance significantly. Typically 2.5.",
        )
    with aql_col3:
        aql_minor = st.selectbox(
            "🔵 Minor",
            options=AQL_OPTIONS,
            index=AQL_OPTIONS.index("4.0"),
            help="Cosmetic or minor defects. Typically 4.0.",
        )

    # ── Lookup code letter & sample size ──────
    code_letter = get_code_letter(lot_size, inspection_level)

    st.markdown('<div class="section-label" style="margin-top:22px;">Sample Plan</div>', unsafe_allow_html=True)

    if code_letter:
        sample_size = SAMPLE_SIZES.get(code_letter, "—")
        st.markdown(f"""
        <div class="code-letter-card">
            <div class="code-letter-big">{code_letter}</div>
            <div class="code-letter-meta">
                <div>
                    <div class="meta-label">Sample Size Code Letter</div>
                    <div class="meta-value" style="font-size:0.85rem;color:#5b6578;">per ISO 2859-1 Table I</div>
                </div>
                <div style="margin-top:10px;">
                    <div class="meta-label">Required Sample Size</div>
                    <div class="meta-value">{sample_size:,} units</div>
                </div>
            </div>
        </div>
        <div class="info-strip">
            Inspect exactly <strong>{sample_size:,} units</strong> drawn randomly from the lot of
            <strong>{lot_size:,}</strong>. If the sample size exceeds the lot size, inspect 100%.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Lot size is outside the standard table range.")

    # ── Actual defects found ───────────────────
    st.markdown('<div class="section-label" style="margin-top:26px;">Defects Found</div>', unsafe_allow_html=True)

    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        found_critical = st.number_input("🔴 Critical", min_value=0, value=0, step=1, key="fc")
    with dcol2:
        found_major = st.number_input("🟠 Major", min_value=0, value=0, step=1, key="fm")
    with dcol3:
        found_minor = st.number_input("🔵 Minor", min_value=0, value=0, step=1, key="fn")


# ══════════════════════════════════════════════
# RIGHT COLUMN — RESULTS
# ══════════════════════════════════════════════
with col_result:
    st.markdown('<div class="section-label">Inspection Results</div>', unsafe_allow_html=True)

    if not code_letter:
        st.error("Cannot compute results — lot size out of range.")
    else:
        # ── Lookup Ac/Re for each class ───────
        defect_classes = [
            ("CRITICAL", "critical", aql_critical, found_critical, "🔴"),
            ("MAJOR",    "major",    aql_major,    found_major,    "🟠"),
            ("MINOR",    "minor",    aql_minor,    found_minor,    "🔵"),
        ]

        results = []
        for label, css_class, aql_str, found, icon in defect_classes:
            limits, eff_letter = get_aql_limits(code_letter, aql_str)
            eff_sample = SAMPLE_SIZES.get(eff_letter, SAMPLE_SIZES.get(code_letter, "?"))

            if limits is None:
                ac, re = None, None
                passed = None
                badge_html = '<span class="badge badge-na">N/A — see standard</span>'
            else:
                ac, re = limits
                passed = found <= ac
                if passed:
                    badge_html = '<span class="badge badge-pass">✓ PASS</span>'
                else:
                    badge_html = '<span class="badge badge-fail">✗ REJECT</span>'

            results.append((label, css_class, aql_str, found, ac, re, passed, eff_letter, eff_sample))

            arrow_note = ""
            if eff_letter != code_letter:
                arrow_note = f' <span style="color:#5b6578;font-size:0.7rem;">(↑ arrow → use {eff_letter}, n={eff_sample})</span>'

            ac_text = str(ac) if ac is not None else "—"
            re_text = str(re) if re is not None else "—"

            st.markdown(f"""
            <div class="defect-card">
                <div class="defect-card-header">
                    <span class="defect-class-label {css_class}">{icon} {label} &nbsp;·&nbsp; AQL {aql_str}%</span>
                    {badge_html}
                </div>
                <div class="acre-row">
                    <div class="acre-chip">Ac &nbsp;<span>{ac_text}</span></div>
                    <div class="acre-chip">Re &nbsp;<span>{re_text}</span></div>
                    <div class="acre-chip">Found &nbsp;<span>{found}</span></div>
                </div>
                <div style="font-size:0.73rem;color:#5b6578;margin-top:8px;font-family:'IBM Plex Mono',monospace;">
                    Code {eff_letter} · n = {eff_sample}{arrow_note}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Summary metrics ───────────────────
        total_found = found_critical + found_major + found_minor
        sample_size = SAMPLE_SIZES.get(code_letter, 0)
        defect_rate = (total_found / sample_size * 100) if sample_size else 0

        st.markdown(f"""
        <div class="metrics-row" style="margin-top:18px;">
            <div class="metric-chip">
                <span class="mc-label">Sample Size</span>
                <span class="mc-value accent">{sample_size:,}</span>
            </div>
            <div class="metric-chip">
                <span class="mc-label">Total Defects</span>
                <span class="mc-value">{total_found}</span>
            </div>
            <div class="metric-chip">
                <span class="mc-label">Defect Rate</span>
                <span class="mc-value">{defect_rate:.2f}%</span>
            </div>
            <div class="metric-chip">
                <span class="mc-label">Code Letter</span>
                <span class="mc-value accent">{code_letter}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Overall verdict ───────────────────
        has_unknown = any(r[6] is None for r in results)
        all_passed  = all(r[6] is True  for r in results)
        any_failed  = any(r[6] is False for r in results)

        if any_failed:
            verdict_class = "fail"
            verdict_box_class = "verdict-fail"
            verdict_icon = "❌"
            verdict_main = "BATCH REJECTED"
            verdict_sub = "One or more defect classes exceeded the rejection number."
        elif all_passed:
            verdict_class = "pass"
            verdict_box_class = "verdict-pass"
            verdict_icon = "✅"
            verdict_main = "BATCH ACCEPTED"
            verdict_sub = "All defect classes are within acceptable limits."
        else:
            verdict_class = "pending"
            verdict_box_class = "verdict-pending"
            verdict_icon = "⚠️"
            verdict_main = "REVIEW REQUIRED"
            verdict_sub = "Some AQL limits could not be resolved from the table."

        st.markdown(f"""
        <div class="verdict-box {verdict_box_class}">
            <div class="verdict-icon">{verdict_icon}</div>
            <div>
                <div class="verdict-text-main {verdict_class}">{verdict_main}</div>
                <div class="verdict-text-sub">{verdict_sub}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Footnote ─────────────────────────
        st.markdown("""
        <div style="margin-top:18px;font-size:0.72rem;color:#3a3f4e;font-family:'IBM Plex Mono',monospace;border-top:1px solid #1e2230;padding-top:12px;">
            Normal inspection · Single sampling · ISO 2859-1:1999 (ANSI/ASQ Z1.4)<br>
            ↑ = use next larger sample size code letter &nbsp;|&nbsp; Ac = Accept if ≤ &nbsp;|&nbsp; Re = Reject if ≥
        </div>
        """, unsafe_allow_html=True)
