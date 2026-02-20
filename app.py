import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import random
import time
import hashlib
import requests
import json
import urllib.parse
import base64

# ═══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ReadWithWaleed",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
#  GLOBAL CSS  ─  Dark Navy + White  +  DIN font
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
/* DIN-like via Google Fonts (Barlow Condensed is the closest free DIN) */
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;600;700&family=Barlow+Semi+Condensed:wght@300;400;500;600&display=swap');

:root {
  /* ── Navy / Blue Palette ── */
  --navy:       #0A1628;
  --navy-mid:   #0F2044;
  --navy-lt:    #1A3060;
  --blue:       #1E4FC2;
  --blue-md:    #2E63E8;
  --blue-lt:    #4B7FFF;
  --sky:        #A8C4FF;
  --ice:        #E8EFFE;

  /* ── Whites / Neutrals ── */
  --white:      #FFFFFF;
  --off-white:  #F4F6FB;
  --ghost:      #EEF1F9;
  --mist:       #D0D8EE;
  --slate:      #8896B3;
  --dark-slate: #4A5568;

  /* ── Accent ── */
  --gold:       #F0C060;
  --gold-dk:    #C89A30;
  --green:      #3DD68C;
  --red:        #F04E5A;
}

/* ── Base ── */
html, body, [class*="css"] {
  font-family: 'Barlow', sans-serif !important;
  background-color: var(--off-white) !important;
  color: var(--navy) !important;
}
* { font-family: 'Barlow', sans-serif !important; }
h1,h2,h3 { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1340px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--navy) !important;
  border-right: 1px solid var(--navy-lt);
}
[data-testid="stSidebar"] * { color: var(--white) !important; font-family: 'Barlow', sans-serif !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] [type="password"] {
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(78,127,255,0.4) !important;
  color: var(--white) !important;
  border-radius: 6px;
  font-family: 'Barlow', sans-serif !important;
}
[data-testid="stSidebar"] label {
  color: var(--sky) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio label {
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-size: 0.9rem !important;
  font-family: 'Barlow', sans-serif !important;
  font-weight: 400 !important;
  color: rgba(255,255,255,0.82) !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label {
  color: var(--white) !important;
  font-weight: 600 !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: rgba(46,99,232,0.25) !important;
  border: 1px solid rgba(78,127,255,0.5) !important;
  color: var(--sky) !important;
  width: 100%;
  font-size: 0.82rem !important;
  border-radius: 6px !important;
  margin-top: 0.3rem;
  font-family: 'Barlow', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(46,99,232,0.45) !important;
  color: var(--white) !important;
}

/* ── Hero Banner ── */
.hero {
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 50%, var(--navy-lt) 100%);
  border-radius: 14px;
  padding: 2.8rem 3.2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(78,127,255,0.2);
}
.hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(46,99,232,0.25) 0%, transparent 70%);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  bottom: -40px; left: 40%;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(75,127,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero h1 {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 2.8rem !important;
  color: var(--white) !important;
  margin: 0 0 0.5rem 0;
  line-height: 1.1;
  letter-spacing: -0.01em;
}
.hero p { color: var(--sky) !important; font-size: 1rem; font-weight: 400; margin: 0; }
.pill {
  display: inline-block;
  background: rgba(78,127,255,0.2);
  border: 1px solid var(--blue-lt);
  color: var(--blue-lt) !important;
  padding: 0.22rem 0.8rem;
  border-radius: 100px;
  font-size: 0.68rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 1rem;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 600;
}

/* ── Section Labels ── */
.section-label {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 0.68rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--blue-md);
  font-weight: 600;
  margin-bottom: 0.2rem;
}
.section-title {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1.6rem !important;
  font-weight: 700 !important;
  color: var(--navy);
  margin: 0.2rem 0 1.2rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--mist);
  letter-spacing: -0.01em;
}
.fancy-divider {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--mist), transparent);
  margin: 2rem 0;
}

/* ── Stat Cards ── */
.stat-card {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 12px;
  padding: 1.4rem;
  text-align: center;
  box-shadow: 0 2px 16px rgba(10,22,40,0.06);
  transition: all 0.2s;
}
.stat-card:hover {
  box-shadow: 0 8px 32px rgba(10,22,40,0.1);
  transform: translateY(-2px);
  border-color: var(--blue-lt);
}
.stat-num {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--blue);
  line-height: 1;
}
.stat-label {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--slate);
  margin-top: 0.3rem;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 600;
}
.stat-icon { font-size: 1.4rem; margin-bottom: 0.4rem; }

/* ── Cards ── */
.form-card {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 16px rgba(10,22,40,0.06);
}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
input[type="text"], input[type="password"], input[type="email"] {
  border: 1.5px solid var(--mist) !important;
  border-radius: 8px !important;
  background: var(--off-white) !important;
  color: var(--navy) !important;
  padding: 0.65rem 0.95rem !important;
  font-family: 'Barlow', sans-serif !important;
  font-size: 0.92rem !important;
  transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color: var(--blue-md) !important;
  box-shadow: 0 0 0 3px rgba(46,99,232,0.12) !important;
  background: var(--white) !important;
}
label {
  font-size: 0.7rem !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: var(--dark-slate) !important;
  font-weight: 600 !important;
  font-family: 'Barlow Condensed', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--blue) !important;
  color: var(--white) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 0.65rem 1.8rem !important;
  font-family: 'Barlow', sans-serif !important;
  font-size: 0.88rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.04em !important;
  cursor: pointer !important;
  transition: all 0.18s !important;
}
.stButton > button:hover {
  background: var(--blue-md) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 16px rgba(30,79,194,0.35) !important;
}

/* ── Progress ── */
.stProgress > div > div > div {
  background: linear-gradient(90deg, var(--blue), var(--blue-lt)) !important;
  border-radius: 100px !important;
}
.stProgress > div > div {
  background: var(--ghost) !important;
  border-radius: 100px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: transparent; gap: 0.4rem; }
.stTabs [data-baseweb="tab"] {
  background: var(--ghost);
  border-radius: 8px;
  color: var(--dark-slate) !important;
  font-size: 0.84rem;
  font-weight: 600;
  padding: 0.5rem 1.2rem;
  border: 1px solid var(--mist) !important;
  font-family: 'Barlow', sans-serif !important;
}
.stTabs [aria-selected="true"] {
  background: var(--navy) !important;
  color: var(--white) !important;
  border-color: var(--navy) !important;
}

/* ── Badge ── */
.badge {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 10px;
  padding: 1rem 1.3rem;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  box-shadow: 0 2px 8px rgba(10,22,40,0.05);
  margin-bottom: 0.6rem;
}
.badge-icon { font-size: 1.8rem; }
.badge-title {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1rem;
  font-weight: 700;
  color: var(--navy);
  letter-spacing: -0.01em;
}
.badge-desc { font-size: 0.8rem; color: var(--slate); }

/* ── Leaderboard ── */
.lb-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.85rem 1.1rem; border-radius: 10px; margin-bottom: 0.4rem;
  background: var(--white); border: 1px solid var(--mist);
  transition: transform 0.15s, border-color 0.15s;
}
.lb-row:hover { transform: translateX(4px); border-color: var(--blue-lt); }
.lb-row.top { background: linear-gradient(90deg, #EEF3FF, var(--white)); border-color: var(--sky); }
.lb-rank { font-family: 'Barlow Condensed', sans-serif !important; font-size: 1.2rem; font-weight: 700; color: var(--blue); width: 2.5rem; }
.lb-name { font-weight: 500; flex: 1; color: var(--navy); }
.lb-pages { font-family: 'Barlow Condensed', sans-serif !important; font-size: 1.1rem; font-weight: 700; color: var(--blue-md); }

/* ── Book Cards ── */
.book-card {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 12px;
  padding: 1.4rem;
  box-shadow: 0 2px 10px rgba(10,22,40,0.05);
  transition: all 0.22s;
  position: relative;
  overflow: hidden;
  min-height: 230px;
}
.book-card:hover {
  box-shadow: 0 10px 36px rgba(10,22,40,0.12);
  transform: translateY(-4px);
  border-color: var(--blue-lt);
}
.book-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 4px; height: 100%;
  background: linear-gradient(180deg, var(--blue), var(--blue-lt));
}
.book-title {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 0.25rem;
  line-height: 1.25;
  letter-spacing: -0.01em;
}
.book-author { font-size: 0.8rem; color: var(--slate); margin-bottom: 0.6rem; }
.book-genre {
  display: inline-block;
  background: var(--ice);
  color: var(--blue);
  font-size: 0.62rem;
  padding: 0.15rem 0.6rem;
  border-radius: 4px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  font-family: 'Barlow Condensed', sans-serif !important;
}

/* ── Reading View ── */
.reading-container {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 16px;
  padding: 3rem 4rem;
  box-shadow: 0 4px 24px rgba(10,22,40,0.07);
  font-family: 'Barlow Semi Condensed', sans-serif !important;
  font-size: 1.05rem;
  line-height: 1.85;
  color: var(--navy);
}
.reading-chapter {
  font-size: 0.68rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--blue-md);
  margin-bottom: 0.4rem;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 700;
}
.reading-title {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 2rem !important;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--mist);
  letter-spacing: -0.02em;
}

/* ── Invite ── */
.invite-card {
  background: linear-gradient(135deg, #EEF3FF, var(--white));
  border: 1px solid var(--sky);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 16px rgba(30,79,194,0.08);
}
.invite-code {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--blue);
  letter-spacing: 0.22em;
  background: var(--ice);
  padding: 0.8rem 2rem;
  border-radius: 8px;
  display: inline-block;
  margin: 0.8rem 0;
  border: 1px dashed var(--blue-lt);
}

/* ── Points Badge ── */
.points-badge {
  background: linear-gradient(135deg, var(--blue), var(--blue-lt));
  color: white !important;
  padding: 0.3rem 0.85rem;
  border-radius: 100px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  display: inline-block;
  font-family: 'Barlow Condensed', sans-serif !important;
}

/* ── Daily Card ── */
.daily-card {
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-lt) 100%);
  border-radius: 14px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  height: 100%;
  border: 1px solid rgba(78,127,255,0.25);
}
.daily-card::after {
  content: '📖';
  font-size: 8rem;
  position: absolute;
  right: 0.5rem; bottom: -1.5rem;
  opacity: 0.08;
}

/* ── Profile Header ── */
.profile-header {
  background: var(--white);
  border: 1px solid var(--mist);
  border-radius: 14px;
  padding: 2.5rem;
  text-align: center;
  box-shadow: 0 2px 16px rgba(10,22,40,0.06);
}
.avatar-xl {
  width: 88px; height: 88px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 2.3rem; margin: 0 auto 1rem auto;
  border: 3px solid var(--blue-lt);
  background: var(--ice);
}
.avatar-circle {
  width: 68px; height: 68px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem; margin: 0 auto 0.75rem auto;
  border: 2px solid var(--blue-lt);
  background: var(--ice);
}

/* ── Bookmark card ── */
.bookmark-card {
  background: var(--white);
  border: 1px solid var(--mist);
  border-left: 4px solid var(--blue);
  border-radius: 10px;
  padding: 1.1rem 1.3rem;
  margin-bottom: 0.7rem;
  box-shadow: 0 2px 8px rgba(10,22,40,0.04);
  transition: all 0.18s;
}
.bookmark-card:hover { border-left-color: var(--blue-lt); box-shadow: 0 4px 18px rgba(10,22,40,0.09); }
.bookmark-book { font-family: 'Barlow Condensed', sans-serif !important; font-size: 1rem; font-weight: 700; color: var(--navy); }
.bookmark-note { font-size: 0.86rem; color: var(--dark-slate); margin-top: 0.3rem; font-style: italic; }
.bookmark-meta { font-size: 0.72rem; color: var(--slate); margin-top: 0.4rem; }

/* ── Download link ── */
.dl-link {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: var(--ice); border: 1px solid var(--sky);
  color: var(--blue) !important; padding: 0.35rem 0.85rem;
  border-radius: 6px; font-size: 0.78rem; font-weight: 600;
  text-decoration: none !important; transition: all 0.15s;
  font-family: 'Barlow', sans-serif !important;
}
.dl-link:hover { background: var(--blue); color: var(--white) !important; border-color: var(--blue); }

/* ── Feedback ── */
.feedback-card {
  background: linear-gradient(135deg, #EEF3FF, var(--white));
  border: 1px solid var(--sky);
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 2px 16px rgba(30,79,194,0.07);
}

/* ── AI summary ── */
.ai-card {
  background: linear-gradient(135deg, var(--navy-mid), var(--navy-lt));
  border: 1px solid rgba(78,127,255,0.3);
  border-radius: 12px;
  padding: 1.5rem;
  color: var(--white);
  position: relative;
}
.ai-badge {
  display: inline-flex; align-items: center; gap: 0.3rem;
  background: rgba(78,127,255,0.25); border: 1px solid rgba(78,127,255,0.5);
  color: var(--sky); padding: 0.2rem 0.7rem;
  border-radius: 100px; font-size: 0.65rem;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 0.8rem;
}

/* ── Alert overrides ── */
div[data-testid="stAlert"] { border-radius: 8px !important; font-family: 'Barlow', sans-serif !important; }

/* ── Selectbox ── */
[data-baseweb="select"] * { font-family: 'Barlow', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  DATABASE
# ═══════════════════════════════════════════════════════════
conn = sqlite3.connect("readwithwaleed.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, nickname TEXT, email TEXT,
    password_hash TEXT, avatar TEXT DEFAULT '📚',
    points INTEGER DEFAULT 0, invite_code TEXT UNIQUE,
    invited_by TEXT, joined_date TEXT, bio TEXT DEFAULT '', avatar_img TEXT DEFAULT '')""")

# ── Migration: safely add 'bio' column to any existing database ──
existing_cols = [row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()]
if "bio" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN bio TEXT DEFAULT ''")
    conn.commit()
if "avatar_img" not in existing_cols:
    c.execute("ALTER TABLE users ADD COLUMN avatar_img TEXT DEFAULT ''")
    conn.commit()

c.execute("""CREATE TABLE IF NOT EXISTS reading_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, book TEXT, pages INTEGER, date TEXT, notes TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, book TEXT, page_ref TEXT,
    note TEXT, created_date TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, category TEXT, message TEXT,
    rating INTEGER, created_date TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS points_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, points INTEGER, reason TEXT, date TEXT)""")

conn.commit()

# ═══════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════
QUOTES = [
    "A reader lives a thousand lives before he dies.",
    "Not all those who wander are lost — but all who read, find.",
    "Today a reader, tomorrow a leader.",
    "One page at a time builds a library of the soul.",
    "The more that you read, the more things you will know.",
    "A book is a dream that you hold in your hands.",
    "Reading is the passport to countless extraordinary journeys.",
]

AVATARS = ["📚","🦁","🌙","🌿","🔮","🦉","⚡","🌊","🏔","🌸","🎯","🦋","🧭","🌺","🐉","🦅","💎","🌌"]

BOOKS = [
    {"id":"1342","title":"Pride and Prejudice","author":"Jane Austen","genre":"Classic Romance","emoji":"💕","year":1813,
     "description":"A witty story of love, society, and the Bennet family's five daughters in Regency-era England.",
     "gutenberg_id":"1342","pages_est":432},
    {"id":"11","title":"Alice's Adventures in Wonderland","author":"Lewis Carroll","genre":"Fantasy","emoji":"🐇","year":1865,
     "description":"A young girl falls into a rabbit hole and discovers a fantastical world of peculiar creatures.",
     "gutenberg_id":"11","pages_est":176},
    {"id":"1661","title":"The Adventures of Sherlock Holmes","author":"Arthur Conan Doyle","genre":"Mystery","emoji":"🔍","year":1892,
     "description":"Twelve stories featuring the legendary detective Sherlock Holmes and Dr. Watson.",
     "gutenberg_id":"1661","pages_est":307},
    {"id":"84","title":"Frankenstein","author":"Mary Shelley","genre":"Gothic Horror","emoji":"⚡","year":1818,
     "description":"A scientist creates a sentient creature in an unorthodox experiment with terrifying consequences.",
     "gutenberg_id":"84","pages_est":280},
    {"id":"1260","title":"Jane Eyre","author":"Charlotte Brontë","genre":"Classic Romance","emoji":"🕯","year":1847,
     "description":"An orphaned girl becomes a governess and falls in love with the mysterious Mr. Rochester.",
     "gutenberg_id":"1260","pages_est":532},
    {"id":"2701","title":"Moby-Dick","author":"Herman Melville","genre":"Adventure","emoji":"🐋","year":1851,
     "description":"Captain Ahab's obsessive quest to hunt the white whale that bit off his leg.",
     "gutenberg_id":"2701","pages_est":720},
    {"id":"74","title":"The Adventures of Tom Sawyer","author":"Mark Twain","genre":"Adventure","emoji":"🛶","year":1876,
     "description":"The mischievous adventures of a young boy growing up along the Mississippi River.",
     "gutenberg_id":"74","pages_est":274},
    {"id":"345","title":"Dracula","author":"Bram Stoker","genre":"Gothic Horror","emoji":"🧛","year":1897,
     "description":"Jonathan Harker travels to Transylvania and encounters the terrifying Count Dracula.",
     "gutenberg_id":"345","pages_est":418},
    {"id":"1232","title":"The Prince","author":"Niccolò Machiavelli","genre":"Philosophy","emoji":"👑","year":1532,
     "description":"A political treatise on the acquisition, maintenance, and use of political power.",
     "gutenberg_id":"1232","pages_est":140},
    {"id":"2542","title":"A Doll's House","author":"Henrik Ibsen","genre":"Drama","emoji":"🏠","year":1879,
     "description":"Nora Helmer discovers her true position in her seemingly perfect marriage.",
     "gutenberg_id":"2542","pages_est":112},
    {"id":"16328","title":"Beowulf","author":"Anonymous","genre":"Epic Poetry","emoji":"⚔️","year":700,
     "description":"The oldest surviving Old English epic poem about the hero Beowulf.",
     "gutenberg_id":"16328","pages_est":96},
    {"id":"4300","title":"Ulysses","author":"James Joyce","genre":"Modernist","emoji":"🌊","year":1922,
     "description":"A day in the life of Leopold Bloom wandering through Dublin on 16 June 1904.",
     "gutenberg_id":"4300","pages_est":730},
    {"id":"1400","title":"Great Expectations","author":"Charles Dickens","genre":"Classic Fiction","emoji":"🎩","year":1861,
     "description":"Young Pip's journey from humble origins to London society, love, and self-discovery.",
     "gutenberg_id":"1400","pages_est":544},
    {"id":"2600","title":"War and Peace","author":"Leo Tolstoy","genre":"Historical Fiction","emoji":"⚔️","year":1869,
     "description":"An epic portrayal of Russian society during the Napoleonic era.",
     "gutenberg_id":"2600","pages_est":1296},
    {"id":"174","title":"The Picture of Dorian Gray","author":"Oscar Wilde","genre":"Gothic Fiction","emoji":"🖼","year":1890,
     "description":"A young man sells his soul for eternal youth while his portrait ages in his place.",
     "gutenberg_id":"174","pages_est":254},
]

AI_SUMMARIES = {
    "1342": "Pride and Prejudice follows Elizabeth Bennet as she navigates issues of manners, upbringing, and marriage in Georgian England. The novel's central romance between Elizabeth and the proud Mr. Darcy is a study in overcoming first impressions. Austen's sharp wit illuminates the social constraints on women and the absurdity of class-obsessed society.",
    "11": "Alice follows a young girl's surreal journey through Wonderland after tumbling down a rabbit hole. Carroll uses fantasy and wordplay to explore themes of identity, logic, and the often arbitrary nature of adult rules. Each encounter — from the Mad Hatter's tea party to the Queen's croquet game — challenges Alice's sense of reality.",
    "1661": "The Adventures of Sherlock Holmes collects twelve cases solved by the brilliant consulting detective. Holmes's legendary deductive method — observing minute details others overlook — makes each mystery feel both thrilling and logical. Dr. Watson's narration humanises Holmes while grounding the reader in Victorian London's fog-filled streets.",
    "84": "Frankenstein explores what happens when human ambition overreaches ethical limits. Victor Frankenstein's creation of life leads to catastrophic loneliness and violence — not because the creature is evil, but because he is abandoned. Shelley asks whether the true monster is the scientist or the society that rejects what it cannot understand.",
    "1260": "Jane Eyre charts one woman's journey from orphaned childhood to independent womanhood. Jane's moral strength and refusal to sacrifice her integrity for love or security make her a revolutionary heroine. The novel's Gothic atmosphere and psychological depth transformed Victorian fiction.",
    "2701": "Moby-Dick is both a thrilling adventure and a profound meditation on obsession, fate, and humanity's place in nature. Captain Ahab's monomania drives the Pequod toward doom, but it is Ishmael's curiosity about everything — whaling, philosophy, friendship — that gives the novel its astonishing breadth.",
    "345": "Dracula, told through letters and journal entries, follows a group of heroes as they try to stop the vampire Count from conquering England. Stoker uses the epistolary format to build dread gradually, and the novel's anxieties about foreign invasion, sexuality, and modernity still resonate. Van Helsing's team represents tradition battling the ancient and monstrous.",
    "174": "The Picture of Dorian Gray is Wilde's only novel — a dark fable about beauty, corruption, and consequence. Dorian, gifted with eternal youth while his portrait bears his sins, descends into hedonism and cruelty. Wilde embeds a razor-sharp critique of aestheticism and Victorian hypocrisy beneath the story's Gothic surface.",
    "1400": "Great Expectations follows Pip from a blacksmith's forge to London's elite, driven by the mysterious benefactor who funds his ambitions. Dickens uses Pip's journey to critique social class, the emptiness of wealth, and the danger of discarding genuine love for social ambition. Miss Havisham and Magwitch are among literature's most unforgettable characters.",
}

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def encode_image(uploaded_file):
    """Convert uploaded file to base64 data URI for storage and display."""
    ext = uploaded_file.name.split('.')[-1].lower()
    mime = {'jpg':'jpeg','jpeg':'jpeg','png':'png','gif':'gif','webp':'webp'}.get(ext,'jpeg')
    b64 = base64.b64encode(uploaded_file.read()).decode()
    return f"data:image/{mime};base64,{b64}"

def render_avatar_xl(avatar_img, avatar_emoji, extra_style=""):
    """Render profile photo if uploaded, else emoji fallback."""
    if avatar_img:
        return f"<div style='width:96px;height:96px;border-radius:50%;margin:0 auto 1rem auto;border:3px solid #4B7FFF;overflow:hidden;background:#EEF1F9;{extra_style}'><img src='{avatar_img}' style='width:100%;height:100%;object-fit:cover;' /></div>"
    return f"<div class='avatar-xl' style='{extra_style}'>{avatar_emoji}</div>"

def render_avatar_sm(avatar_img, avatar_emoji):
    """Render small sidebar avatar."""
    if avatar_img:
        return f"<div style='width:68px;height:68px;border-radius:50%;margin:0 auto 0.75rem auto;border:2px solid #4B7FFF;overflow:hidden;background:#EEF1F9;'><img src='{avatar_img}' style='width:100%;height:100%;object-fit:cover;' /></div>"
    return f"<div class='avatar-circle'>{avatar_emoji}</div>" 
def gen_invite(u): return hashlib.md5(u.encode()).hexdigest()[:8].upper()

def add_points(uname, pts, reason):
    c.execute("UPDATE users SET points=points+? WHERE username=?", (pts, uname))
    c.execute("INSERT INTO points_log VALUES (NULL,?,?,?,?)", (uname, pts, reason, datetime.today().strftime("%Y-%m-%d")))
    conn.commit()

def compute_streak(df):
    if df.empty: return 0
    dates = sorted(df["date"].dt.date.unique(), reverse=True)
    streak = 0; expected = datetime.today().date()
    for d in dates:
        if d == expected or d == expected - timedelta(days=1): streak += 1; expected = d - timedelta(days=1)
        else: break
    return streak

def fetch_book_text(book_id, max_chars=10000):
    for url in [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
    ]:
        try:
            r = requests.get(url, timeout=14)
            if r.status_code == 200:
                t = r.text
                s = t.find("*** START OF")
                t = t[s+60:] if s != -1 else t
                e = t.find("*** END OF")
                t = t[:e] if e != -1 else t
                return t[:max_chars].strip()
        except: continue
    return None

def get_download_links(book):
    bid = book["gutenberg_id"]
    title_q = urllib.parse.quote(book["title"] + " " + book["author"])
    return {
        "Project Gutenberg": f"https://www.gutenberg.org/ebooks/{bid}",
        "Standard Ebooks": f"https://standardebooks.org/search?q={urllib.parse.quote(book['title'])}",
        "Open Library": f"https://openlibrary.org/search?q={title_q}",
        "PDF Drive": f"https://www.pdfdrive.com/search?q={title_q}",
        "Z-Library": f"https://z-lib.id/s/{title_q}",
    }

# ═══════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════
for k, v in [("logged_in",False),("current_user",None),("reading_book",None),("book_cache",{})]:
    if k not in st.session_state: st.session_state[k] = v

# ═══════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:1.3rem 0 1rem 0;'>
      <div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:700;color:#FFFFFF;letter-spacing:-0.01em;'>
        ReadWith<span style='color:#4B7FFF;'>Waleed</span>
      </div>
      <div style='font-size:0.62rem;letter-spacing:0.18em;text-transform:uppercase;color:#8896B3;margin-top:0.2rem;font-family:Barlow Condensed,sans-serif;font-weight:600;'>
        Your Reading Companion
      </div>
    </div>
    <hr style='border:none;height:1px;background:rgba(78,127,255,0.2);margin-bottom:1.2rem;'>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        ur = c.execute("SELECT * FROM users WHERE username=?", (st.session_state.current_user,)).fetchone()
        if ur:
            uname,nickname,email,_,avatar,points,invite_code,invited_by,joined_date,bio,avatar_img = ur
            dn = nickname if nickname else uname
            sidebar_av = render_avatar_sm(avatar_img, avatar)
            st.markdown(f"""
            <div style='text-align:center;padding:0.3rem 0 1rem 0;'>
              {sidebar_av}
              <div style='font-family:Barlow Condensed,sans-serif;font-size:1.1rem;font-weight:700;color:#FFFFFF;'>{dn}</div>
              <div style='font-size:0.72rem;color:#8896B3;margin-top:0.1rem;'>@{uname}</div>
              <div style='margin-top:0.5rem;'><span class='points-badge'>✦ {points:,} pts</span></div>
            </div>
            <hr style='border:none;height:1px;background:rgba(78,127,255,0.15);margin-bottom:0.8rem;'>
            """, unsafe_allow_html=True)

        page = st.radio("", [
            "📊  Dashboard", "👤  My Profile", "📖  Log Reading",
            "📚  Book Library", "🔖  Bookmarks", "⏱  Timer",
            "🤝  Invite Friends", "💬  Feedback", "🏆  Leaderboard"
        ], label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.reading_book = None
            st.rerun()
    else:
        page = "auth"
        st.markdown("""
        <div style='color:rgba(255,255,255,0.35);font-size:0.8rem;text-align:center;padding:1.2rem 0;line-height:1.6;'>
          Sign in to access your<br>personal reading dashboard.
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='position:absolute;bottom:1rem;left:1rem;right:1rem;font-size:0.6rem;color:#1A3060;letter-spacing:0.05em;text-align:center;font-family:Barlow Condensed,sans-serif;'>
      ReadWithWaleed &nbsp;·&nbsp; Built with ♥
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  AUTH PAGE
# ═══════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div class='hero'>
      <div class='pill'>Welcome to ReadWithWaleed</div>
      <h1>Read More.<br>Track Everything.<br><span style='color:#4B7FFF;'>Grow Together.</span></h1>
      <p>Your personal reading tracker, book library, and reading community — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    tab_li, tab_su = st.tabs(["  ✦  Sign In  ", "  ✦  Create Account  "])

    with tab_li:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='max-width:480px;margin:0 auto;'>
        <div class='form-card'>
        <div style='text-align:center;margin-bottom:1.5rem;'>
          <div style='font-size:2rem;margin-bottom:0.4rem;'>📖</div>
          <div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:700;color:#0A1628;'>Welcome Back</div>
          <div style='font-size:0.85rem;color:#8896B3;'>Enter your credentials to continue reading</div>
        </div>
        """, unsafe_allow_html=True)
        li_u = st.text_input("Username", key="li_u", placeholder="your_username")
        li_p = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In →", use_container_width=True, key="btn_li"):
            row = c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (li_u, hash_pw(li_p))).fetchone()
            if row:
                st.session_state.logged_in = True
                st.session_state.current_user = li_u
                add_points(li_u, 2, "Daily login")
                st.rerun()
            else:
                st.error("Incorrect username or password. Please try again.")
        st.markdown("""
        <div style='text-align:center;margin-top:1rem;font-size:0.82rem;color:#8896B3;'>
          Don't have an account? Switch to the <strong>Create Account</strong> tab above.
        </div>
        </div></div>
        """, unsafe_allow_html=True)

    with tab_su:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='form-card'>
        <div style='margin-bottom:1.5rem;'>
          <div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:700;color:#0A1628;'>Create Your Account</div>
          <div style='font-size:0.85rem;color:#8896B3;'>Join thousands of readers on ReadWithWaleed</div>
        </div>
        """, unsafe_allow_html=True)

        # Account details section
        st.markdown("""<div style='font-family:Barlow Condensed,sans-serif;font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#1E4FC2;margin-bottom:0.8rem;border-bottom:1px solid #EEF1F9;padding-bottom:0.4rem;'>Account Details</div>""", unsafe_allow_html=True)
        ac1, ac2 = st.columns(2)
        with ac1:
            su_u = st.text_input("Username *", key="su_u", placeholder="john_reads", help="Your unique login name. Cannot be changed later.")
            su_e = st.text_input("Email *", key="su_e", placeholder="you@email.com", help="Used for account recovery.")
        with ac2:
            su_p = st.text_input("Password *", type="password", key="su_p", placeholder="Min. 6 characters")
            su_p2 = st.text_input("Confirm Password *", type="password", key="su_p2", placeholder="Repeat password")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:Barlow Condensed,sans-serif;font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#1E4FC2;margin-bottom:0.8rem;border-bottom:1px solid #EEF1F9;padding-bottom:0.4rem;'>Profile Details</div>""", unsafe_allow_html=True)
        pc1, pc2 = st.columns(2)
        with pc1:
            su_n = st.text_input("Nickname / Display Name", key="su_n", placeholder="How others see you", help="Can be your real name or a fun reading alias.")
        with pc2:
            su_av = st.selectbox("Choose Your Avatar", AVATARS, key="su_av")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style='font-family:Barlow Condensed,sans-serif;font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#1E4FC2;margin-bottom:0.8rem;border-bottom:1px solid #EEF1F9;padding-bottom:0.4rem;'>Optional</div>""", unsafe_allow_html=True)
        su_inv = st.text_input("Invite Code", key="su_inv", placeholder="Enter a friend's code to earn +50 bonus points")
        su_bio = st.text_area("Short Bio", key="su_bio", placeholder="Tell the community about your reading interests...", height=70)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style='font-size:0.78rem;color:#8896B3;margin-bottom:0.8rem;'>By creating an account you agree to read more books and share the love of reading. 📚</div>""", unsafe_allow_html=True)

        if st.button("Create My Account →", use_container_width=True, key="btn_su"):
            if not su_u or not su_e or not su_p:
                st.warning("Please fill in all required fields (marked with *).")
            elif len(su_p) < 6:
                st.error("Password must be at least 6 characters.")
            elif su_p != su_p2:
                st.error("Passwords do not match.")
            elif c.execute("SELECT 1 FROM users WHERE username=?", (su_u,)).fetchone():
                st.error("Username already taken. Please choose another.")
            elif c.execute("SELECT 1 FROM users WHERE email=?", (su_e,)).fetchone():
                st.error("Email already registered.")
            else:
                inv_code = gen_invite(su_u)
                inv_by = None
                bonus = 0
                if su_inv:
                    ir = c.execute("SELECT username FROM users WHERE invite_code=?", (su_inv.strip().upper(),)).fetchone()
                    if ir:
                        inv_by = ir[0]
                        bonus = 50
                        add_points(ir[0], 100, f"Invited {su_u}")
                    else:
                        st.warning("Invite code not found — creating account anyway.")
                c.execute("""
                    INSERT INTO users
                        (username, nickname, email, password_hash, avatar,
                         points, invite_code, invited_by, joined_date, bio, avatar_img)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    su_u, su_n or su_u, su_e, hash_pw(su_p),
                    su_av, bonus, inv_code, inv_by,
                    datetime.today().strftime("%Y-%m-%d"), su_bio or "", ""
                ))
                conn.commit()
                st.session_state.logged_in = True
                st.session_state.current_user = su_u
                st.balloons()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    for col, icon, t, d in [
        (fc1,"📚","Free Book Library","12+ classics readable in-app from Project Gutenberg"),
        (fc2,"🔥","Streaks & Points","Earn points every session, build unbroken reading streaks"),
        (fc3,"🔖","Bookmarks & Notes","Save your spot and annotate insights across any book"),
        (fc4,"🤝","Invite & Earn","Get 100 pts per friend you bring into the community"),
    ]:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
              <div class='stat-icon'>{icon}</div>
              <div style='font-family:Barlow Condensed,sans-serif;font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.3rem;'>{t}</div>
              <div style='font-size:0.8rem;color:#8896B3;line-height:1.5;'>{d}</div>
            </div>""", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════
#  LOAD USER DATA  (logged in)
# ═══════════════════════════════════════════════════════════
username = st.session_state.current_user
ur = c.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
uname, nickname, email, _, avatar, points, invite_code, invited_by, joined_date, bio, avatar_img = ur
display_name = nickname if nickname else uname

df_all = pd.read_sql_query("SELECT * FROM reading_logs WHERE username=?", conn, params=(username,))
if not df_all.empty: df_all["date"] = pd.to_datetime(df_all["date"])

total_pages = int(df_all["pages"].sum()) if not df_all.empty else 0
streak = compute_streak(df_all) if not df_all.empty else 0
books_count = df_all["book"].nunique() if not df_all.empty else 0

# ═══════════════════════════════════════════════════════════
#  IN-APP READER  (shown when a book is open)
# ═══════════════════════════════════════════════════════════
if st.session_state.reading_book is not None:
    bk = st.session_state.reading_book
    bid = bk["id"]

    # Download links bar
    dl_links = get_download_links(bk)
    dl_html = " ".join([f'<a href="{url}" target="_blank" class="dl-link">⬇ {name}</a>' for name, url in dl_links.items()])

    st.markdown(f"""
    <div class='hero' style='padding:1.5rem 2rem;'>
      <div class='pill'>Now Reading</div>
      <h1 style='font-size:2rem;'>{bk['emoji']} {bk['title']}</h1>
      <p>by {bk['author']} &nbsp;·&nbsp; {bk['genre']} &nbsp;·&nbsp; ~{bk.get('pages_est',300)} pages</p>
      <div style='margin-top:1rem;display:flex;gap:0.5rem;flex-wrap:wrap;'>{dl_html}</div>
    </div>
    """, unsafe_allow_html=True)

    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Library"): st.session_state.reading_book = None; st.rerun()

    # AI Summary
    ai_sum = AI_SUMMARIES.get(bid)
    if ai_sum:
        st.markdown(f"""
        <div class='ai-card'>
          <div class='ai-badge'>🤖 AI Summary</div>
          <div style='font-size:0.92rem;color:#A8C4FF;line-height:1.7;'>{ai_sum}</div>
        </div>
        """, unsafe_allow_html=True)
        # AI Voice toggle
        with st.expander("🔊 AI Voice — Listen to the Summary"):
            st.markdown("""
            <div style='background:rgba(78,127,255,0.1);border:1px solid rgba(78,127,255,0.3);border-radius:10px;padding:1.2rem;'>
              <div style='font-family:Barlow Condensed,sans-serif;font-size:1rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;'>🔊 Text-to-Speech</div>
              <div style='font-size:0.85rem;color:#4A5568;margin-bottom:0.8rem;'>Click play below to hear the AI summary read aloud using your browser's built-in text-to-speech.</div>
            """, unsafe_allow_html=True)
            safe_text = ai_sum.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
            st.markdown(f"""
            <button onclick="
              var u = new SpeechSynthesisUtterance('{safe_text}');
              u.rate = 0.92; u.pitch = 1.0;
              var voices = speechSynthesis.getVoices();
              var eng = voices.find(v => v.lang.startsWith('en'));
              if(eng) u.voice = eng;
              speechSynthesis.speak(u);
            " style='background:#1E4FC2;color:white;border:none;padding:0.6rem 1.6rem;border-radius:8px;font-family:Barlow,sans-serif;font-size:0.88rem;font-weight:600;cursor:pointer;margin-right:0.5rem;'>
              ▶ Play Summary
            </button>
            <button onclick="speechSynthesis.cancel();"
              style='background:#EEF1F9;color:#0A1628;border:1px solid #D0D8EE;padding:0.6rem 1.2rem;border-radius:8px;font-family:Barlow,sans-serif;font-size:0.88rem;font-weight:600;cursor:pointer;'>
              ⏹ Stop
            </button>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch text
    if bid not in st.session_state.book_cache:
        with st.spinner("Fetching from Project Gutenberg..."):
            st.session_state.book_cache[bid] = fetch_book_text(bid)

    text = st.session_state.book_cache.get(bid)

    if text:
        words = text.split()
        chunk_size = 700
        total_chunks = max(1, len(words) // chunk_size)

        r_col, s_col = st.columns([3, 1])

        with s_col:
            st.markdown("<div class='form-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Navigation</div>", unsafe_allow_html=True)
            chunk_num = st.number_input("Section", min_value=1, max_value=total_chunks, value=1, step=1)
            st.progress(chunk_num / total_chunks)
            st.markdown(f"<div style='font-size:0.72rem;color:#8896B3;margin-bottom:1rem;'>Section {chunk_num} of {total_chunks}</div>", unsafe_allow_html=True)
            st.markdown("</div><br>", unsafe_allow_html=True)

            # Log session
            st.markdown("<div class='form-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Log This Session</div>", unsafe_allow_html=True)
            with st.form("rl"):
                mr = st.number_input("Minutes read", min_value=1, max_value=180, value=15)
                pr = st.number_input("Pages read", min_value=1, value=5)
                if st.form_submit_button("✦ Log & Earn Points", use_container_width=True):
                    c.execute("INSERT INTO reading_logs VALUES (NULL,?,?,?,?,?)",
                              (username, bk['title'], pr, datetime.today().strftime("%Y-%m-%d"), "In-app session"))
                    conn.commit()
                    earned = (pr // 5) * 5 + mr
                    add_points(username, earned, f"Read: {bk['title']}")
                    st.success(f"+{earned} pts!")
                    st.balloons()
            st.markdown("</div><br>", unsafe_allow_html=True)

            # Add bookmark
            st.markdown("<div class='form-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Add Bookmark</div>", unsafe_allow_html=True)
            with st.form("bm_form"):
                bm_note = st.text_area("Note / Insight", placeholder="What struck you here?", height=80)
                if st.form_submit_button("🔖 Save Bookmark", use_container_width=True):
                    c.execute("INSERT INTO bookmarks VALUES (NULL,?,?,?,?,?)",
                              (username, bk['title'], f"Section {chunk_num}", bm_note, datetime.today().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    st.success("Bookmark saved!")
            st.markdown("</div>", unsafe_allow_html=True)

        with r_col:
            start_w = (chunk_num - 1) * chunk_size
            excerpt = " ".join(words[start_w: start_w + chunk_size])
            paras = [p.strip() for p in excerpt.replace("\r\n", "\n").split("\n\n") if p.strip()]
            formatted = "".join([f"<p style='margin-bottom:1.2em;text-indent:2em;'>{p}</p>" for p in paras])
            st.markdown(f"""
            <div class='reading-container'>
              <div class='reading-chapter'>{bk['genre']} · Section {chunk_num} of {total_chunks}</div>
              <div class='reading-title'>{bk['title']}</div>
              {formatted}
            </div>
            """, unsafe_allow_html=True)

            # Voice for reading text
            first_para = paras[0] if paras else ""
            safe_para = first_para[:300].replace("'", "\\'").replace('"', '\\"')
            st.markdown(f"""
            <div style='margin-top:1rem;display:flex;gap:0.5rem;align-items:center;'>
              <button onclick="
                var u = new SpeechSynthesisUtterance('{safe_para}...');
                u.rate=0.88; speechSynthesis.speak(u);
              " style='background:#0F2044;color:#A8C4FF;border:1px solid rgba(78,127,255,0.4);padding:0.45rem 1rem;border-radius:6px;font-family:Barlow,sans-serif;font-size:0.8rem;font-weight:600;cursor:pointer;'>
                🔊 Listen to excerpt
              </button>
              <button onclick="speechSynthesis.cancel();"
                style='background:#EEF1F9;color:#0A1628;border:1px solid #D0D8EE;padding:0.45rem 0.85rem;border-radius:6px;font-family:Barlow,sans-serif;font-size:0.8rem;font-weight:600;cursor:pointer;'>
                ⏹ Stop
              </button>
              <span style='font-size:0.72rem;color:#8896B3;'>Browser TTS · First paragraph only</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Could not load text from Project Gutenberg. Try the download links above to read offline.")
    st.stop()

# ═══════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════
if page == "📊  Dashboard":
    st.markdown(f"""
    <div class='hero'>
      <div class='pill'>Welcome back</div>
      <div style='display:flex;align-items:center;gap:1.4rem;margin-bottom:0.4rem;'>
        {render_avatar_xl(avatar_img, avatar, "width:72px;height:72px;font-size:1.6rem;border-width:3px;flex-shrink:0;margin:0;")}
        <h1 style='margin:0;'>Hello, {display_name}.</h1>
      </div>
      <p>Here's a snapshot of your reading life on ReadWithWaleed.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, num, label in [
        (c1,"📄",f"{total_pages:,}","Total Pages"),
        (c2,"🔥",str(streak),"Day Streak"),
        (c3,"📚",str(books_count),"Books Logged"),
        (c4,"✦",f"{points:,}","Points Earned"),
    ]:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
              <div class='stat-icon'>{icon}</div>
              <div class='stat-num'>{num}</div>
              <div class='stat-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    daily_bk = BOOKS[datetime.today().timetuple().tm_yday % len(BOOKS)]
    dc1, dc2 = st.columns([2, 1])
    with dc1:
        st.markdown(f"""
        <div class='daily-card'>
          <div style='font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;color:rgba(168,196,255,0.6);margin-bottom:0.4rem;font-family:Barlow Condensed,sans-serif;font-weight:700;'>Today's Reading Pick</div>
          <div style='font-family:Barlow Condensed,sans-serif;font-size:1.7rem;font-weight:700;color:#FFFFFF;margin-bottom:0.3rem;letter-spacing:-0.01em;'>{daily_bk['emoji']} {daily_bk['title']}</div>
          <div style='font-size:0.85rem;color:#A8C4FF;margin-bottom:0.8rem;'>by {daily_bk['author']} · {daily_bk['year']}</div>
          <div style='font-size:0.9rem;color:rgba(255,255,255,0.75);line-height:1.6;'>{daily_bk['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    with dc2:
        st.markdown(f"""
        <div class='stat-card' style='height:100%;display:flex;flex-direction:column;justify-content:center;padding:1.5rem;'>
          <div style='font-size:2rem;margin-bottom:0.6rem;'>💬</div>
          <div style='font-family:Barlow Semi Condensed,sans-serif;font-style:italic;font-size:0.92rem;color:#4A5568;line-height:1.65;'>&ldquo;{random.choice(QUOTES)}&rdquo;</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    # Weekly challenge
    df_week = df_all[df_all["date"] >= pd.Timestamp(datetime.today() - timedelta(days=7))] if not df_all.empty else pd.DataFrame()
    weekly = int(df_week["pages"].sum()) if not df_week.empty else 0
    st.markdown("<div class='section-label'>Weekly Challenge</div><div class='section-title'>100 Pages This Week</div>", unsafe_allow_html=True)
    st.progress(min(weekly / 100, 1.0))
    wc1, wc2 = st.columns([3, 1])
    with wc1: st.markdown(f"<span style='font-size:0.85rem;color:#4A5568;'>{weekly} of 100 pages this week</span>", unsafe_allow_html=True)
    with wc2: st.markdown(f"<span style='font-size:0.85rem;color:#1E4FC2;font-weight:700;'>{min(int(weekly/100*100),100)}%</span>", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

    if not df_all.empty:
        st.markdown("<div class='section-label'>Reading History</div><div class='section-title'>All Sessions</div>", unsafe_allow_html=True)
        disp = df_all[["date","book","pages","notes"]].sort_values("date",ascending=False).copy()
        disp["date"] = disp["date"].dt.strftime("%b %d, %Y")
        disp.columns = ["Date","Book","Pages","Notes"]
        st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.info("No sessions yet. Head to **Book Library** to start reading, or **Log Reading** to track a book.")

    # Badges
    st.markdown("<div class='fancy-divider'></div><div class='section-label'>Achievements</div><div class='section-title'>Your Milestones</div>", unsafe_allow_html=True)
    badges = [
        (total_pages>=50,"🌱","First Sprout","50 pages — the journey begins."),
        (total_pages>=100,"🎖","Century Reader","100 pages — a solid start!"),
        (total_pages>=200,"🥇","Dedicated Reader","200 pages — you mean business."),
        (total_pages>=500,"🏆","Page Legend","500 pages — absolute legend."),
        (streak>=7,"🔥","Week Warrior","7-day streak — unbroken!"),
        (books_count>=5,"📚","Bibliophile","5 books tracked — a true lover of books."),
        (points>=500,"✦","Point Collector","500 points earned — keep going!"),
    ]
    earned_b = [(i,t,d) for (u,i,t,d) in badges if u]
    locked_b = [(i,t,d) for (u,i,t,d) in badges if not u]
    if earned_b:
        bc1, bc2 = st.columns(2)
        for idx, (icon,title,desc) in enumerate(earned_b):
            with (bc1 if idx%2==0 else bc2):
                st.markdown(f"""<div class='badge'><div class='badge-icon'>{icon}</div><div><div class='badge-title'>{title}</div><div class='badge-desc'>{desc}</div></div><span style='color:#1E4FC2;font-size:0.7rem;font-weight:700;margin-left:auto;font-family:Barlow Condensed,sans-serif;'>EARNED ✓</span></div>""", unsafe_allow_html=True)
    if locked_b:
        with st.expander(f"🔒 {len(locked_b)} badges still to unlock"):
            for icon,title,desc in locked_b:
                st.markdown(f"""<div class='badge' style='opacity:0.38;'><div class='badge-icon' style='filter:grayscale(1);'>{icon}</div><div><div class='badge-title'>{title}</div><div class='badge-desc'>{desc}</div></div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  MY PROFILE
# ═══════════════════════════════════════════════════════════
elif page == "👤  My Profile":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Your Identity</div><h1 style='font-size:2.2rem;'>My Profile</h1><p>Manage your account, avatar, bio, and password.</p></div>""", unsafe_allow_html=True)

    pc1, pc2 = st.columns([1, 2])
    with pc1:
        pts_rank = "🥇 Legend" if points>=1000 else ("🥈 Veteran" if points>=500 else ("🥉 Reader" if points>=100 else "🌱 Newcomer"))
        st.markdown(f"""
        <div class='profile-header'>
          <div class='avatar-xl'>{avatar}</div>
          <div style='font-family:Barlow Condensed,sans-serif;font-size:1.6rem;font-weight:700;color:#0A1628;'>{display_name}</div>
          <div style='font-size:0.8rem;color:#8896B3;margin:0.15rem 0;'>@{uname}</div>
          <div style='font-size:0.78rem;color:#8896B3;margin-bottom:0.5rem;'>{email}</div>
          {"<div style='font-size:0.82rem;color:#4A5568;font-style:italic;margin-bottom:0.7rem;line-height:1.4;'>" + bio + "</div>" if bio else ""}
          <span class='points-badge'>✦ {points:,} points</span>
          <div style='font-size:0.85rem;color:#1E4FC2;margin-top:0.6rem;font-weight:700;font-family:Barlow Condensed,sans-serif;'>{pts_rank}</div>
          <div style='font-size:0.72rem;color:#8896B3;margin-top:0.3rem;'>Member since {joined_date}</div>
          {"<div style='font-size:0.72rem;color:#3DD68C;margin-top:0.3rem;'>Invited by @" + str(invited_by) + " ✓</div>" if invited_by else ""}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Reading Stats</div>", unsafe_allow_html=True)
        for icon,val,lab in [("📄",f"{total_pages:,}","Pages Read"),("🔥",str(streak),"Day Streak"),("📚",str(books_count),"Books Tracked")]:
            st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;padding:0.65rem 0;border-bottom:1px solid #EEF1F9;'><span style='font-size:0.88rem;color:#4A5568;'>{icon} {lab}</span><span style='font-family:Barlow Condensed,sans-serif;font-size:1.15rem;font-weight:700;color:#0A1628;'>{val}</span></div>""", unsafe_allow_html=True)

    with pc2:
        st.markdown("<div class='section-label'>Edit Profile</div><div class='section-title'>Update Your Details</div>", unsafe_allow_html=True)
        # ── Profile Photo Upload ──
        st.markdown("<div class='section-label'>Profile Photo</div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:white;border:1px solid #D0D8EE;border-radius:12px;"
            "padding:1.4rem;box-shadow:0 2px 10px rgba(10,22,40,0.05);margin-bottom:1rem;'>",
            unsafe_allow_html=True
        )
        ph1, ph2 = st.columns([1, 2])
        with ph1:
            if avatar_img:
                st.markdown(
                    f"<img src='{avatar_img}' style='width:90px;height:90px;border-radius:50%;"
                    "object-fit:cover;border:3px solid #4B7FFF;display:block;margin:0 auto;' />",
                    unsafe_allow_html=True
                )
                st.markdown("<div style='font-size:0.72rem;color:#8896B3;text-align:center;margin-top:0.4rem;'>Current photo</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='width:90px;height:90px;border-radius:50%;background:#EEF1F9;"
                    f"border:3px solid #4B7FFF;display:flex;align-items:center;justify-content:center;"
                    f"font-size:2rem;margin:0 auto;'>{avatar}</div>",
                    unsafe_allow_html=True
                )
                st.markdown("<div style='font-size:0.72rem;color:#8896B3;text-align:center;margin-top:0.4rem;'>No photo yet — emoji used</div>", unsafe_allow_html=True)

        with ph2:
            st.markdown(
                "<div style='font-size:0.82rem;color:#4A5568;margin-bottom:0.6rem;line-height:1.55;'>"
                "Upload a photo from your phone or computer.<br>"
                "<span style='color:#8896B3;font-size:0.75rem;'>JPG, PNG, GIF or WEBP · Max 5 MB</span></div>",
                unsafe_allow_html=True
            )
            uploaded_photo = st.file_uploader(
                "Choose a photo",
                type=["jpg","jpeg","png","gif","webp"],
                key="photo_upload",
                label_visibility="collapsed"
            )
            if uploaded_photo is not None:
                if uploaded_photo.size > 5 * 1024 * 1024:
                    st.error("File is over 5 MB. Please choose a smaller image.")
                else:
                    img_data = encode_image(uploaded_photo)
                    c.execute("UPDATE users SET avatar_img=? WHERE username=?", (img_data, username))
                    conn.commit()
                    st.success("Profile photo saved!")
                    st.rerun()
            if avatar_img:
                if st.button("Remove Photo", key="rm_photo"):
                    c.execute("UPDATE users SET avatar_img='' WHERE username=?", (username,))
                    conn.commit()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-label' style='margin-top:1rem;'>Edit Details</div>", unsafe_allow_html=True)
        with st.form("ep"):
            ep1, ep2 = st.columns(2)
            with ep1: new_nick = st.text_input("Nickname", value=nickname or "")
            with ep2: new_av = st.selectbox("Emoji (fallback avatar)", AVATARS, index=AVATARS.index(avatar) if avatar in AVATARS else 0)
            new_bio = st.text_area("Bio", value=bio or "", placeholder="Tell the community about yourself...", height=80)
            st.markdown("**Change Password** *(leave blank to keep current)*")
            np1, np2 = st.columns(2)
            with np1: new_pw = st.text_input("New Password", type="password")
            with np2: conf_pw = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Save Changes →", use_container_width=True):
                if new_pw and new_pw != conf_pw:
                    st.error("Passwords don't match.")
                else:
                    upd = ["avatar=?","bio=?"]; pms = [new_av, new_bio]
                    if new_nick: upd.append("nickname=?"); pms.append(new_nick)
                    if new_pw: upd.append("password_hash=?"); pms.append(hash_pw(new_pw))
                    pms.append(username)
                    c.execute(f"UPDATE users SET {','.join(upd)} WHERE username=?", pms)
                    conn.commit()
                    st.success("Details saved!")

        st.markdown("<br><div class='section-label'>Points History</div><div class='section-title'>How You Earned Points</div>", unsafe_allow_html=True)
        pts_df = pd.read_sql_query("SELECT date,reason,points FROM points_log WHERE username=? ORDER BY id DESC LIMIT 20", conn, params=(username,))
        if not pts_df.empty:
            pts_df.columns = ["Date","Reason","Points"]
            st.dataframe(pts_df, use_container_width=True, hide_index=True)
        else:
            st.info("No points history yet. Start reading!")

# ═══════════════════════════════════════════════════════════
#  LOG READING
# ═══════════════════════════════════════════════════════════
elif page == "📖  Log Reading":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>New Entry</div><h1 style='font-size:2.2rem;'>Log a Reading Session</h1><p>Record what you read today and keep your streak alive.</p></div>""", unsafe_allow_html=True)

    with st.form("lf", clear_on_submit=True):
        lc1, lc2 = st.columns([2, 1])
        with lc1: book_t = st.text_input("Book Title", placeholder="e.g. Atomic Habits by James Clear")
        with lc2: pages_l = st.number_input("Pages Read Today", min_value=0, step=1, value=0)
        log_date = st.date_input("Date", value=datetime.today())
        notes_l = st.text_area("Session Notes (optional)", placeholder="Key insights, quotes, or reflections from today's reading...", height=90)
        if st.form_submit_button("✦ Log Reading Session", use_container_width=True):
            if not book_t: st.warning("Please enter a book title.")
            elif pages_l == 0: st.warning("Please enter at least 1 page.")
            else:
                c.execute("INSERT INTO reading_logs VALUES (NULL,?,?,?,?,?)", (username, book_t, pages_l, str(log_date), notes_l))
                conn.commit()
                earned = (pages_l // 5) * 5 + 10
                add_points(username, earned, f"Logged: {book_t}")
                st.balloons()
                st.success(f"✦ Logged **{pages_l} pages** of *{book_t}* · +{earned} points earned!")

    if not df_all.empty:
        st.markdown("<br><div class='section-label'>Recent Sessions</div><div class='section-title'>Last 5 Entries</div>", unsafe_allow_html=True)
        rec = df_all.sort_values("date", ascending=False).head(5)[["date","book","pages"]].copy()
        rec["date"] = rec["date"].dt.strftime("%b %d, %Y")
        rec.columns = ["Date","Book","Pages"]
        st.dataframe(rec, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════
#  BOOK LIBRARY
# ═══════════════════════════════════════════════════════════
elif page == "📚  Book Library":
    st.markdown("""
    <div class='hero' style='padding:2rem 2.5rem;'>
      <div class='pill'>Project Gutenberg · 70,000+ Free Books</div>
      <h1 style='font-size:2.2rem;'>Book Library</h1>
      <p>Read classic literature directly in this app — or download to any device for free.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search + filter
    s1, s2 = st.columns([2, 1])
    with s1: search_q = st.text_input("Search books", placeholder="Title, author, or genre...", label_visibility="collapsed")
    with s2:
        all_genres = ["All"] + sorted(set(b["genre"] for b in BOOKS))
        genre_f = st.selectbox("Genre", all_genres, label_visibility="collapsed")

    filtered = BOOKS
    if search_q: filtered = [b for b in filtered if search_q.lower() in b["title"].lower() or search_q.lower() in b["author"].lower() or search_q.lower() in b["genre"].lower()]
    if genre_f != "All": filtered = [b for b in filtered if b["genre"] == genre_f]

    st.markdown(f"<div style='font-size:0.8rem;color:#8896B3;margin-bottom:1.2rem;'>{len(filtered)} books matching your filter</div>", unsafe_allow_html=True)

    # Grid
    for rs in range(0, len(filtered), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            idx = rs + i
            if idx < len(filtered):
                bk = filtered[idx]
                dl = get_download_links(bk)
                with col:
                    st.markdown(f"""
                    <div class='book-card'>
                      <div style='font-size:2.3rem;margin-bottom:0.5rem;'>{bk['emoji']}</div>
                      <div class='book-title'>{bk['title']}</div>
                      <div class='book-author'>by {bk['author']} · {bk['year']}</div>
                      <div class='book-genre'>{bk['genre']}</div>
                      <div style='font-size:0.8rem;color:#8896B3;margin-top:0.7rem;line-height:1.5;'>{bk['description']}</div>
                      <div style='margin-top:0.9rem;display:flex;flex-wrap:wrap;gap:0.3rem;'>
                        {"".join([f'<a href="{url}" target="_blank" class="dl-link">⬇ {name}</a>' for name,url in list(dl.items())[:3]])}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("📖 Read In-App", key=f"o_{bk['id']}", use_container_width=True):
                        st.session_state.reading_book = bk
                        st.rerun()

    st.markdown("""
    <div class='fancy-divider'></div>
    <div style='text-align:center;padding:1rem 0;'>
      <div style='font-family:Barlow Condensed,sans-serif;font-size:1.1rem;font-weight:700;color:#0A1628;margin-bottom:0.5rem;'>Want even more books?</div>
      <div style='font-size:0.85rem;color:#8896B3;margin-bottom:1rem;'>Access millions of titles across these free platforms:</div>
      <div style='display:flex;gap:0.6rem;justify-content:center;flex-wrap:wrap;'>
        <a href='https://www.gutenberg.org' target='_blank' class='dl-link'>📚 Project Gutenberg (70K books)</a>
        <a href='https://standardebooks.org' target='_blank' class='dl-link'>✨ Standard Ebooks (beautifully formatted)</a>
        <a href='https://openlibrary.org' target='_blank' class='dl-link'>🌐 Open Library (borrowing)</a>
        <a href='https://www.pdfdrive.com' target='_blank' class='dl-link'>📄 PDF Drive</a>
        <a href='https://z-lib.id' target='_blank' class='dl-link'>🔍 Z-Library</a>
        <a href='https://archive.org/details/texts' target='_blank' class='dl-link'>🏛 Internet Archive</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  BOOKMARKS
# ═══════════════════════════════════════════════════════════
elif page == "🔖  Bookmarks":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Your Reading Notes</div><h1 style='font-size:2.2rem;'>Bookmarks & Notes</h1><p>All your saved passages, insights, and annotations in one place.</p></div>""", unsafe_allow_html=True)

    bm_tab1, bm_tab2 = st.tabs(["🔖  My Bookmarks", "  ✦  Add New Bookmark"])

    with bm_tab1:
        bm_df = pd.read_sql_query("SELECT * FROM bookmarks WHERE username=? ORDER BY id DESC", conn, params=(username,))
        if bm_df.empty:
            st.info("No bookmarks yet. Open any book in the Library and save a note while reading.")
        else:
            # Filter by book
            all_books_bm = ["All Books"] + sorted(bm_df["book"].unique().tolist())
            filter_book = st.selectbox("Filter by book", all_books_bm)
            filtered_bm = bm_df if filter_book == "All Books" else bm_df[bm_df["book"] == filter_book]
            st.markdown(f"<div style='font-size:0.8rem;color:#8896B3;margin-bottom:1rem;'>{len(filtered_bm)} bookmark(s)</div>", unsafe_allow_html=True)
            for _, row in filtered_bm.iterrows():
                st.markdown(f"""
                <div class='bookmark-card'>
                  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                      <div class='bookmark-book'>📚 {row['book']}</div>
                      <div class='bookmark-meta'>📍 {row['page_ref']} &nbsp;·&nbsp; 🗓 {row['created_date']}</div>
                    </div>
                  </div>
                  {"<div class='bookmark-note'>" + str(row['note']) + "</div>" if row['note'] else ""}
                </div>
                """, unsafe_allow_html=True)

    with bm_tab2:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Add a New Bookmark</div>", unsafe_allow_html=True)
        with st.form("new_bm", clear_on_submit=True):
            bm_book = st.text_input("Book Title", placeholder="Which book are you noting?")
            bm_page = st.text_input("Page / Section Reference", placeholder="e.g. Page 127, Chapter 4, Section 3...")
            bm_note_new = st.text_area("Your Note / Insight", placeholder="Write your thought, quote, or reflection here...", height=120)
            if st.form_submit_button("🔖 Save Bookmark", use_container_width=True):
                if not bm_book: st.warning("Please enter a book title.")
                else:
                    c.execute("INSERT INTO bookmarks VALUES (NULL,?,?,?,?,?)",
                              (username, bm_book, bm_page or "—", bm_note_new, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    add_points(username, 3, f"Added bookmark: {bm_book}")
                    st.success("Bookmark saved! +3 points earned.")
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  TIMER
# ═══════════════════════════════════════════════════════════
elif page == "⏱  Timer":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Focus Mode</div><h1 style='font-size:2.2rem;'>Reading Timer</h1><p>Set a focused session. Earn 1 point per minute you commit to reading.</p></div>""", unsafe_allow_html=True)

    tl, tr = st.columns([1, 1])
    with tl:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)
        preset = st.radio("Quick Presets", ["5 min","15 min","25 min — Pomodoro","45 min","Custom"])
        pmap = {"5 min":5,"15 min":15,"25 min — Pomodoro":25,"45 min":45}
        minutes = pmap[preset] if preset != "Custom" else st.number_input("Custom duration (minutes)", 1, 180, 20, 5)
        st.markdown(f"""
        <div style='background:rgba(30,79,194,0.08);border:1px solid rgba(30,79,194,0.2);border-radius:8px;padding:0.8rem 1rem;margin-top:0.8rem;'>
          <div style='font-size:0.8rem;color:#1E4FC2;font-weight:600;'>✦ You'll earn {minutes} points on completion</div>
          <div style='font-size:0.75rem;color:#8896B3;margin-top:0.2rem;'>Plus bonus points if you log pages afterward.</div>
        </div>
        """, unsafe_allow_html=True)
        start_t = st.button("▶ Start Reading Session", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tr:
        tph = st.empty(); pph = st.empty(); mph = st.empty()
        tph.markdown(f"""
        <div class='stat-card' style='padding:3rem;'>
          <div class='stat-icon'>⏱</div>
          <div class='stat-num'>{minutes:02d}:00</div>
          <div class='stat-label'>Ready to begin</div>
        </div>""", unsafe_allow_html=True)
        if start_t:
            total_s = minutes * 60
            for rem in range(total_s, -1, -1):
                m, s = divmod(rem, 60)
                tph.markdown(f"""
                <div class='stat-card' style='padding:3rem;'>
                  <div class='stat-icon'>🔥</div>
                  <div class='stat-num'>{m:02d}:{s:02d}</div>
                  <div class='stat-label'>Stay focused</div>
                </div>""", unsafe_allow_html=True)
                pph.progress(rem / total_s if total_s else 0)
                time.sleep(1)
            add_points(username, minutes, f"{minutes}-min reading session")
            mph.success(f"🎉 Session complete! +{minutes} points earned. Now log your pages!")
            st.balloons()

# ═══════════════════════════════════════════════════════════
#  INVITE FRIENDS
# ═══════════════════════════════════════════════════════════
elif page == "🤝  Invite Friends":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Grow the Community</div><h1 style='font-size:2.2rem;'>Invite Friends</h1><p>Share your code. They earn 50 bonus points. You earn 100.</p></div>""", unsafe_allow_html=True)

    inv1, inv2 = st.columns([1, 1])
    with inv1:
        st.markdown("<div class='section-label'>Your Invite Code</div><div class='section-title'>Share & Earn</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='invite-card'>
          <div style='font-size:0.72rem;letter-spacing:0.14em;text-transform:uppercase;color:#8896B3;margin-bottom:0.3rem;font-family:Barlow Condensed,sans-serif;font-weight:700;'>Your Personal Code</div>
          <div class='invite-code'>{invite_code}</div>
          <div style='font-size:0.85rem;color:#4A5568;'>Share this when friends sign up to ReadWithWaleed</div>
          <div style='background:var(--ice);border-radius:8px;padding:1rem;margin-top:1rem;text-align:left;'>
            <div style='display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #D0D8EE;'>
              <span style='font-size:0.85rem;color:#4A5568;'>You earn per referral</span>
              <span style='font-family:Barlow Condensed,sans-serif;color:#1E4FC2;font-size:1.1rem;font-weight:700;'>+100 pts</span>
            </div>
            <div style='display:flex;justify-content:space-between;padding:0.4rem 0;'>
              <span style='font-size:0.85rem;color:#4A5568;'>Friend's welcome bonus</span>
              <span style='font-family:Barlow Condensed,sans-serif;color:#3DD68C;font-size:1.1rem;font-weight:700;'>+50 pts</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with inv2:
        st.markdown("<div class='section-label'>How It Works</div><div class='section-title'>Three Simple Steps</div>", unsafe_allow_html=True)
        for num, title, desc in [
            ("1","Copy your code","Share your unique 8-character code via WhatsApp, text, or email."),
            ("2","Friend creates account","They sign up and enter your code in the 'Invite Code' field."),
            ("3","Both earn points","You get 100 pts credited instantly. They start with 50 bonus pts."),
        ]:
            st.markdown(f"""
            <div style='display:flex;gap:1rem;align-items:flex-start;margin-bottom:1.3rem;'>
              <div style='min-width:38px;height:38px;border-radius:50%;background:#0A1628;color:#4B7FFF;display:flex;align-items:center;justify-content:center;font-family:Barlow Condensed,sans-serif;font-size:1.1rem;font-weight:700;flex-shrink:0;'>{num}</div>
              <div><div style='font-weight:700;color:#0A1628;margin-bottom:0.2rem;font-family:Barlow,sans-serif;'>{title}</div><div style='font-size:0.84rem;color:#8896B3;line-height:1.5;'>{desc}</div></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='fancy-divider'></div><div class='section-label'>Your Referrals</div><div class='section-title'>Friends You've Brought In</div>", unsafe_allow_html=True)
    refs = pd.read_sql_query("SELECT username,nickname,avatar,avatar_img,points,joined_date FROM users WHERE invited_by=?", conn, params=(username,))
    if not refs.empty:
        for _, row in refs.iterrows():
            rn = row["nickname"] if row["nickname"] else row["username"]
            ref_av = row.get('avatar_img','')
            ref_emoji = row.get('avatar','📚')
            ref_av_html = (f"<img src='{ref_av}' style='width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid #4B7FFF;flex-shrink:0;' />"
                          if ref_av else f"<span style='font-size:1.6rem;'>{ref_emoji}</span>")
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:1rem;padding:0.85rem 1.1rem;background:white;border:1px solid #D0D8EE;border-radius:10px;margin-bottom:0.5rem;transition:all 0.15s;'>
              {ref_av_html}
              <div style='flex:1;'><div style='font-weight:600;color:#0A1628;'>{rn}</div><div style='font-size:0.75rem;color:#8896B3;'>Joined {row['joined_date']}</div></div>
              <span class='points-badge'>✦ {int(row['points']):,} pts</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No referrals yet. Share your code to start earning!")

# ═══════════════════════════════════════════════════════════
#  FEEDBACK
# ═══════════════════════════════════════════════════════════
elif page == "💬  Feedback":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Your Voice Matters</div><h1 style='font-size:2.2rem;'>Send Feedback</h1><p>Help us make ReadWithWaleed better. Every message is read by the team.</p></div>""", unsafe_allow_html=True)

    fb1, fb2 = st.columns([3, 2])

    with fb1:
        st.markdown("<div class='feedback-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Share Your Thoughts</div>", unsafe_allow_html=True)
        with st.form("fb_form", clear_on_submit=True):
            fb_cat = st.selectbox("Category", ["💡 Feature Request","🐛 Bug Report","👍 General Praise","📚 Book Request","🤔 Question / Help","💬 Other"])
            fb_rating = st.slider("Overall App Rating", min_value=1, max_value=5, value=5,
                                  format="%d ⭐")
            fb_msg = st.text_area("Your Message", placeholder="Tell us what you think, what's missing, what you love, or what broke...", height=140)
            if st.form_submit_button("📨 Submit Feedback", use_container_width=True):
                if not fb_msg.strip():
                    st.warning("Please write a message before submitting.")
                else:
                    c.execute("INSERT INTO feedback VALUES (NULL,?,?,?,?,?)",
                              (username, fb_cat, fb_msg, fb_rating, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    add_points(username, 10, "Submitted feedback")
                    st.success("✦ Thank you! Your feedback has been received. +10 points for helping us improve!")
                    st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)

    with fb2:
        st.markdown(f"""
        <div class='daily-card' style='margin-bottom:1rem;'>
          <div style='font-size:0.65rem;letter-spacing:0.18em;text-transform:uppercase;color:rgba(168,196,255,0.6);margin-bottom:0.6rem;font-family:Barlow Condensed,sans-serif;font-weight:700;'>Why Feedback Matters</div>
          <div style='font-family:Barlow Condensed,sans-serif;font-size:1.3rem;font-weight:700;color:#FFFFFF;margin-bottom:0.8rem;'>You shape this app.</div>
          <div style='font-size:0.88rem;color:#A8C4FF;line-height:1.65;'>Every feature request, bug report, and idea goes directly to the team. We read every message and use them to decide what to build next.</div>
          <div style='margin-top:1rem;font-family:Barlow Condensed,sans-serif;font-size:1rem;color:#4B7FFF;font-weight:700;'>✦ +10 points per submission</div>
        </div>
        """, unsafe_allow_html=True)

        # Show user's past feedback
        my_fb = pd.read_sql_query("SELECT created_date,category,rating,message FROM feedback WHERE username=? ORDER BY id DESC LIMIT 5", conn, params=(username,))
        if not my_fb.empty:
            st.markdown("<div class='section-label'>Your Previous Feedback</div>", unsafe_allow_html=True)
            for _, row in my_fb.iterrows():
                stars = "⭐" * int(row["rating"])
                st.markdown(f"""
                <div class='bookmark-card'>
                  <div class='bookmark-book'>{row['category']}</div>
                  <div style='font-size:0.75rem;color:#8896B3;margin-top:0.15rem;'>{row['created_date']} · {stars}</div>
                  <div class='bookmark-note'>{str(row['message'])[:120]}{"..." if len(str(row['message']))>120 else ""}</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  LEADERBOARD
# ═══════════════════════════════════════════════════════════
elif page == "🏆  Leaderboard":
    st.markdown("""<div class='hero' style='padding:2rem 2.5rem;'><div class='pill'>Community Rankings</div><h1 style='font-size:2.2rem;'>The Leaderboard</h1><p>See how your reading stacks up across the ReadWithWaleed community.</p></div>""", unsafe_allow_html=True)

    tab_pg, tab_pts = st.tabs(["📄  By Pages Read", "  ✦  By Points"])
    rank_icons = {1:"🥇",2:"🥈",3:"🥉"}

    def render_lb(query, val_key, val_lbl):
        lb = pd.read_sql_query(query, conn)
        if lb.empty: st.info("No data yet — be the first to log some reading!"); return
        for i, row in lb.iterrows():
            rank = i + 1
            ri = rank_icons.get(rank, f"#{rank}")
            is_top = rank <= 3
            is_me = row["username"] == username
            av_emoji = row.get("avatar","📚")
            av_photo = row.get("avatar_img","")
            nick = row.get("nickname") or row["username"]
            me_b = "<span style='background:#1E4FC2;color:white;font-size:0.62rem;padding:0.12rem 0.5rem;border-radius:100px;margin-left:0.4rem;font-family:Barlow Condensed,sans-serif;font-weight:700;'>YOU</span>" if is_me else ""
            val = int(row.get(val_key, 0))
            # Avatar: photo if uploaded, else emoji
            if av_photo:
                av_html = f"<img src='{av_photo}' style='width:36px;height:36px;border-radius:50%;object-fit:cover;border:2px solid #4B7FFF;margin-right:0.6rem;vertical-align:middle;flex-shrink:0;' />"
            else:
                av_html = f"<span style='font-size:1.1rem;margin-right:0.6rem;'>{av_emoji}</span>"
            st.markdown(f"""
            <div class='lb-row {"top" if is_top else ""}'>
              <span class='lb-rank'>{ri}</span>
              {av_html}
              <span class='lb-name'>{nick}{me_b}</span>
              <span style='font-size:0.72rem;color:#8896B3;margin-right:1rem;'>{int(row.get("books",0))} books</span>
              <span class='lb-pages'>{val:,} <span style='font-size:0.68rem;color:#8896B3;font-weight:400;'>{val_lbl}</span></span>
            </div>""", unsafe_allow_html=True)

    with tab_pg:
        render_lb("""SELECT u.username,u.nickname,u.avatar,u.avatar_img,
            COALESCE(SUM(r.pages),0) as total_pages,
            COUNT(DISTINCT r.book) as books
            FROM users u LEFT JOIN reading_logs r ON u.username=r.username
            GROUP BY u.username ORDER BY total_pages DESC LIMIT 10""", "total_pages", "pages")

    with tab_pts:
        render_lb("""SELECT username,nickname,avatar,avatar_img,points as total_points,0 as books
            FROM users ORDER BY points DESC LIMIT 10""", "total_points", "pts")
