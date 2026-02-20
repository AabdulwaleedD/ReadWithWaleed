import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import secrets
import uuid
import random
import time
import re
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ReadWithWaleed",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --cream:     #F8F4EF;
    --warm:      #EDE5D8;
    --tan:       #C9B99A;
    --brown:     #6B4F3A;
    --espresso:  #2C1A0E;
    --gold:      #C9A84C;
    --gold-lt:   #E8D5A3;
    --gold-dk:   #A07830;
    --sage:      #7A9E7E;
    --rust:      #B85C3A;
    --ink:       #1A1208;
    --muted:     #9a8070;
    --white:     #FFFFFF;
    --card-shad: 0 2px 16px rgba(44,26,14,0.07);
    --card-shad-hover: 0 8px 32px rgba(44,26,14,0.14);
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: var(--cream) !important;
    color: var(--espresso) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1280px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--espresso) !important;
    border-right: 1px solid #3d2a18;
    min-width: 260px !important;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(201,184,154,0.3) !important;
    color: var(--cream) !important;
    border-radius: 8px;
    font-size: 0.9rem !important;
}
[data-testid="stSidebar"] label {
    color: var(--gold-lt) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio label {
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
}
[data-testid="stSidebar"] .stRadio > div { gap: 0.2rem; }
[data-testid="stSidebar"] p { color: rgba(247,243,238,0.65) !important; font-size: 0.82rem !important; }

/* ── AVATAR ── */
.avatar-circle {
    width: 52px; height: 52px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    font-weight: 600;
    color: white;
    flex-shrink: 0;
    border: 2px solid var(--gold);
}

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, var(--espresso) 0%, #4a2e1a 55%, #7a5238 100%);
    border-radius: 18px;
    padding: 2.8rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '❝';
    font-family: 'Cormorant Garamond', serif;
    font-size: 22rem;
    color: rgba(201,168,76,0.06);
    position: absolute;
    top: -5rem; right: 1rem;
    line-height: 1;
    pointer-events: none;
}
.hero .pill {
    display: inline-block;
    background: rgba(201,168,76,0.18);
    border: 1px solid rgba(201,168,76,0.5);
    color: var(--gold) !important;
    padding: 0.22rem 0.85rem;
    border-radius: 100px;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
    font-weight: 500;
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--cream) !important;
    margin: 0 0 0.5rem 0;
    line-height: 1.15;
}
.hero p {
    color: rgba(232,213,163,0.8) !important;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* ── SECTION HEADS ── */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--brown);
    font-weight: 600;
    margin-bottom: 0.2rem;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--espresso);
    margin: 0 0 1.4rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--warm);
}

/* ── STAT CARDS ── */
.stat-card {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 14px;
    padding: 1.6rem 1.2rem;
    text-align: center;
    box-shadow: var(--card-shad);
    transition: box-shadow 0.2s, transform 0.2s;
    height: 100%;
}
.stat-card:hover {
    box-shadow: var(--card-shad-hover);
    transform: translateY(-2px);
}
.stat-card .stat-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.stat-card .stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--brown);
    line-height: 1;
}
.stat-card .stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.4rem;
    font-weight: 500;
}
.stat-card .stat-sub {
    font-size: 0.75rem;
    color: var(--sage);
    margin-top: 0.2rem;
}

/* ── BOOK CARDS ── */
.book-card {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 14px;
    padding: 1.4rem;
    box-shadow: var(--card-shad);
    transition: box-shadow 0.2s, transform 0.2s;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.book-card:hover {
    box-shadow: var(--card-shad-hover);
    transform: translateY(-3px);
}
.book-cover {
    background: linear-gradient(135deg, var(--espresso), var(--brown));
    border-radius: 8px;
    padding: 1.5rem 1rem;
    text-align: center;
    margin-bottom: 1rem;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.book-cover .book-emoji { font-size: 2.5rem; margin-bottom: 0.3rem; }
.book-cover .cover-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--gold-lt) !important;
    line-height: 1.3;
    text-align: center;
}
.book-card .book-author {
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 0.5rem;
    letter-spacing: 0.04em;
}
.book-card .book-desc {
    font-size: 0.82rem;
    color: var(--brown);
    flex: 1;
    line-height: 1.55;
}
.book-tag {
    display: inline-block;
    background: var(--warm);
    color: var(--brown) !important;
    font-size: 0.65rem;
    padding: 0.15rem 0.55rem;
    border-radius: 100px;
    margin: 0.1rem;
    font-weight: 500;
    letter-spacing: 0.05em;
}

/* ── READING VIEW ── */
.reading-view {
    background: #FDFAF6;
    border: 1px solid var(--warm);
    border-radius: 14px;
    padding: 3rem 4rem;
    max-width: 720px;
    margin: 0 auto;
    box-shadow: var(--card-shad);
    line-height: 1.85;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: var(--ink);
}
.reading-view h2 {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: var(--espresso);
}
.reading-view .reading-author {
    font-size: 0.85rem;
    color: var(--muted);
    font-family: 'Outfit', sans-serif;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--warm);
}
.chapter-progress {
    height: 4px;
    background: var(--warm);
    border-radius: 100px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.chapter-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--gold), var(--rust));
    border-radius: 100px;
    transition: width 0.5s ease;
}

/* ── FORM CARD ── */
.form-card {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: var(--card-shad);
}

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox select {
    border: 1px solid var(--warm) !important;
    border-radius: 9px !important;
    background: var(--cream) !important;
    color: var(--espresso) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
    outline: none !important;
}
label {
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--brown) !important;
    font-weight: 600 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: var(--espresso) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.55rem 1.5rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 2px 8px rgba(44,26,14,0.15) !important;
}
.stButton > button:hover {
    background: var(--brown) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(44,26,14,0.2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── PROGRESS ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--gold), var(--rust)) !important;
    border-radius: 100px !important;
}
.stProgress > div > div {
    background: var(--warm) !important;
    border-radius: 100px !important;
    height: 8px !important;
}

/* ── BADGES ── */
.badge-row {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: var(--card-shad);
    margin-bottom: 0.6rem;
    transition: box-shadow 0.2s;
}
.badge-row:hover { box-shadow: var(--card-shad-hover); }
.badge-row .badge-icon { font-size: 2rem; }
.badge-row .badge-earned { color: var(--gold) !important; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-left: auto; }

/* ── LEADERBOARD ── */
.lb-row {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
    transition: box-shadow 0.2s;
}
.lb-row:hover { box-shadow: var(--card-shad-hover); }
.lb-row.gold-row { background: linear-gradient(90deg, #fffdf5, white); border-color: var(--gold-lt); }
.lb-rank { font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; font-weight: 700; width: 2.2rem; color: var(--gold); }
.lb-name { font-weight: 500; flex: 1; }
.lb-pages { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-weight: 700; color: var(--brown); }
.lb-pts { font-size: 0.78rem; color: var(--gold-dk); font-weight: 600; margin-left: 0.5rem; }

/* ── YOU BADGE ── */
.you-badge {
    background: var(--gold);
    color: var(--espresso) !important;
    font-size: 0.6rem;
    padding: 0.12rem 0.45rem;
    border-radius: 100px;
    margin-left: 0.4rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    vertical-align: middle;
}

/* ── POINTS BADGE ── */
.pts-chip {
    display: inline-block;
    background: linear-gradient(135deg, var(--gold), var(--gold-dk));
    color: var(--espresso) !important;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.2rem 0.7rem;
    border-radius: 100px;
    letter-spacing: 0.05em;
}

/* ── INVITE CARD ── */
.invite-card {
    background: linear-gradient(135deg, var(--espresso), #4a2e1a);
    border-radius: 14px;
    padding: 2rem;
    color: var(--cream);
    border: 1px solid rgba(201,168,76,0.2);
}
.invite-code {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--gold) !important;
    letter-spacing: 0.25em;
    text-align: center;
    padding: 1rem;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    border: 1px dashed rgba(201,168,76,0.4);
    margin: 1rem 0;
}

/* ── PROFILE CARD ── */
.profile-card {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: var(--card-shad);
    text-align: center;
}

/* ── AUTH FORM ── */
.auth-wrapper {
    max-width: 420px;
    margin: 2rem auto;
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 18px;
    padding: 2.5rem;
    box-shadow: 0 8px 40px rgba(44,26,14,0.12);
}
.auth-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--espresso);
    text-align: center;
    margin-bottom: 0.2rem;
}
.auth-sub {
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.06em;
    margin-bottom: 2rem;
}

/* ── TIMER ── */
.timer-face {
    background: var(--white);
    border: 1px solid var(--warm);
    border-radius: 50%;
    width: 200px; height: 200px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    margin: 1.5rem auto;
    box-shadow: 0 4px 32px rgba(44,26,14,0.1);
}
.timer-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--brown);
    line-height: 1;
}
.timer-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── DIVIDER ── */
.fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--tan), transparent);
    margin: 2rem 0;
}

/* ── ALERTS ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--warm);
    border-radius: 10px;
    padding: 0.3rem;
    gap: 0.2rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--brown) !important;
    padding: 0.45rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--espresso) !important;
    box-shadow: 0 1px 6px rgba(44,26,14,0.1);
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--brown) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--warm) !important;
    border-radius: 10px !important;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════
conn = sqlite3.connect("readwithwaleed.db", check_same_thread=False)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id         TEXT PRIMARY KEY,
    email      TEXT UNIQUE NOT NULL,
    nickname   TEXT NOT NULL,
    avatar_color TEXT DEFAULT '#6B4F3A',
    password_hash TEXT NOT NULL,
    salt       TEXT NOT NULL,
    invite_code TEXT UNIQUE,
    points     INTEGER DEFAULT 0,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS invites (
    code       TEXT PRIMARY KEY,
    owner_id   TEXT,
    used_by    TEXT,
    used_at    TEXT
);

CREATE TABLE IF NOT EXISTS reading_logs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    TEXT,
    book_title TEXT,
    gutenberg_id TEXT,
    pages      INTEGER,
    minutes    INTEGER DEFAULT 0,
    date       TEXT,
    notes      TEXT
);

CREATE TABLE IF NOT EXISTS reading_sessions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    TEXT,
    book_title TEXT,
    gutenberg_id TEXT,
    start_time TEXT,
    duration_minutes INTEGER,
    completed  INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS book_progress (
    user_id    TEXT,
    gutenberg_id TEXT,
    last_chunk INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    started_at TEXT,
    PRIMARY KEY (user_id, gutenberg_id)
);
""")
conn.commit()

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
QUOTES = [
    "A reader lives a thousand lives before he dies.",
    "Not all those who wander are lost — but all who read, find.",
    "Today a reader, tomorrow a leader.",
    "One page at a time builds a library of the soul.",
    "Reading is to the mind what exercise is to the body.",
    "Books are a uniquely portable magic.",
    "There is no friend as loyal as a book.",
]

AVATAR_COLORS = [
    "#6B4F3A","#4A6741","#3A5167","#6B3A5A",
    "#7A6B3A","#3A4F6B","#6B4A3A","#3A6B5A",
]

POINTS_TABLE = {
    "log_pages_per_10": 5,
    "complete_session": 20,
    "streak_day": 10,
    "invite_friend": 50,
    "finish_book": 100,
}

# ── Password hashing ──
def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    return key.hex(), salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    computed, _ = hash_password(password, salt)
    return secrets.compare_digest(computed, stored_hash)

def validate_email(email: str) -> bool:
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email))

# ── Streak computation ──
def compute_streak(user_id):
    rows = c.execute(
        "SELECT DISTINCT date FROM reading_logs WHERE user_id=? ORDER BY date DESC", (user_id,)
    ).fetchall()
    if not rows:
        return 0
    dates = [datetime.strptime(r[0], "%Y-%m-%d").date() for r in rows]
    today = datetime.today().date()
    streak = 0
    expected = today
    for d in dates:
        if d == expected or d == expected - timedelta(days=1):
            streak += 1
            expected = d - timedelta(days=1)
        else:
            break
    return streak

# ── Points award ──
def award_points(user_id, pts, reason=""):
    c.execute("UPDATE users SET points = points + ? WHERE id = ?", (pts, user_id))
    conn.commit()

# ── Invite code generator ──
def generate_invite_code():
    return secrets.token_hex(3).upper()

# ═══════════════════════════════════════════════════════════
# GUTENBERG BOOK CATALOG (curated classics)
# ═══════════════════════════════════════════════════════════
BOOKS = [
    {
        "id": "1342",
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "emoji": "💌",
        "tags": ["Romance", "Classic", "19th Century"],
        "desc": "The story of the Bennet sisters navigating love, class, and society in Regency England.",
        "color": "#5a3a6b"
    },
    {
        "id": "11",
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "emoji": "🐇",
        "tags": ["Fantasy", "Children", "Adventure"],
        "desc": "Young Alice falls through a rabbit hole into a whimsical world of impossible creatures.",
        "color": "#3a5a6b"
    },
    {
        "id": "1661",
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "emoji": "🔍",
        "tags": ["Mystery", "Classic", "Detective"],
        "desc": "Twelve extraordinary tales featuring the world's most famous consulting detective.",
        "color": "#3a4a2e"
    },
    {
        "id": "2701",
        "title": "Moby Dick",
        "author": "Herman Melville",
        "emoji": "🐋",
        "tags": ["Adventure", "Classic", "Sea"],
        "desc": "Captain Ahab's obsessive quest to hunt the white whale across the vast ocean.",
        "color": "#3a5a6b"
    }