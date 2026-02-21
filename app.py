import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import random
import time
import hashlib
import requests
import urllib.parse
import base64

st.set_page_config(page_title="ReadWithWaleed", page_icon="📖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
:root{
  --bg:#F8F8F8;--white:#FFFFFF;--border:#E5E5E5;--border2:#CFCFCF;
  --text:#1C1C1C;--text2:#555;--text3:#999;
  --green:#2F6B4F;--green-lt:#EBF4EF;--green-dk:#1E4A35;
  --orange:#E8763A;--red:#D94F4F;
  --shadow:0 1px 3px rgba(0,0,0,0.07);--shadow2:0 4px 14px rgba(0,0,0,0.09);
  --r:10px;
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[class*="css"]{font-family:'Plus Jakarta Sans',sans-serif!important;background:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.5rem 1.5rem 3rem!important;max-width:1080px;}

/* Sidebar */
[data-testid="stSidebar"]{background:var(--white)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{font-family:'Plus Jakarta Sans',sans-serif!important;color:var(--text)!important;}
[data-testid="stSidebar"] .stTextInput input,[data-testid="stSidebar"] [type="password"]{background:var(--bg)!important;border:1.5px solid var(--border)!important;color:var(--text)!important;border-radius:8px!important;}
[data-testid="stSidebar"] label{color:var(--text3)!important;font-size:0.7rem!important;letter-spacing:0.06em!important;text-transform:uppercase!important;font-weight:600!important;}
[data-testid="stSidebar"] .stRadio label{text-transform:none!important;letter-spacing:0!important;font-size:0.88rem!important;font-weight:500!important;color:var(--text2)!important;padding:0.1rem 0!important;}
[data-testid="stSidebar"] .stButton>button{background:var(--bg)!important;border:1.5px solid var(--border)!important;color:var(--text2)!important;width:100%;font-size:0.85rem!important;border-radius:8px!important;font-weight:500!important;}
[data-testid="stSidebar"] .stButton>button:hover{border-color:var(--green)!important;color:var(--green)!important;background:var(--green-lt)!important;}

/* Typography */
.ph{margin-bottom:1.4rem;padding-bottom:1rem;border-bottom:1px solid var(--border);}
.ph h1{font-size:1.55rem!important;font-weight:700!important;color:var(--text)!important;margin:0 0 0.2rem!important;line-height:1.2;}
.ph p{color:var(--text3);font-size:0.88rem;margin:0;}
.sec-lbl{font-size:0.68rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--text3);margin-bottom:0.3rem;}
.sec-ttl{font-size:1.1rem;font-weight:700;color:var(--text);margin:0 0 1rem;}

/* Cards */
.card{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1.3rem;box-shadow:var(--shadow);}
.card-lg{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1.75rem;box-shadow:var(--shadow);}
.card-green{background:var(--green-lt);border:1px solid #BDD9CA;border-radius:var(--r);padding:1.3rem;}

/* Stats */
.sc{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1rem 1.2rem;box-shadow:var(--shadow);transition:box-shadow 0.18s;}
.sc:hover{box-shadow:var(--shadow2);}
.sn{font-size:1.8rem;font-weight:700;color:var(--text);line-height:1;margin-bottom:0.2rem;}
.sl{font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);}
.si{font-size:1.1rem;margin-bottom:0.35rem;}

/* Inputs */
.stTextInput input,.stNumberInput input,.stTextArea textarea{border:1.5px solid var(--border)!important;border-radius:8px!important;background:var(--white)!important;color:var(--text)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:0.9rem!important;padding:0.6rem 0.85rem!important;}
.stTextInput input:focus,.stNumberInput input:focus,.stTextArea textarea:focus{border-color:var(--green)!important;box-shadow:0 0 0 3px rgba(47,107,79,0.1)!important;}
label{font-size:0.7rem!important;font-weight:600!important;letter-spacing:0.06em!important;text-transform:uppercase!important;color:var(--text3)!important;font-family:'Plus Jakarta Sans',sans-serif!important;}

/* Buttons */
.stButton>button{background:var(--green)!important;color:#fff!important;border:none!important;border-radius:8px!important;padding:0.6rem 1.5rem!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:0.88rem!important;font-weight:600!important;transition:all 0.15s!important;}
.stButton>button:hover{background:var(--green-dk)!important;box-shadow:0 4px 12px rgba(47,107,79,0.28)!important;}

/* Progress */
.stProgress>div>div>div{background:var(--green)!important;border-radius:100px!important;}
.stProgress>div>div{background:var(--border)!important;border-radius:100px!important;height:5px!important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:transparent;gap:0;border-bottom:1px solid var(--border);margin-bottom:1rem;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--text3)!important;font-size:0.88rem;font-weight:600;padding:0.55rem 1rem;border:none!important;border-bottom:2px solid transparent!important;border-radius:0!important;font-family:'Plus Jakarta Sans',sans-serif!important;}
.stTabs [aria-selected="true"]{color:var(--green)!important;border-bottom-color:var(--green)!important;}

/* Tags */
.tag{display:inline-block;background:var(--green-lt);color:var(--green);border-radius:4px;font-size:0.65rem;font-weight:700;padding:0.15rem 0.5rem;letter-spacing:0.05em;text-transform:uppercase;}
.tag-gray{display:inline-block;background:#F0F0F0;color:var(--text3);border-radius:4px;font-size:0.65rem;font-weight:700;padding:0.15rem 0.5rem;letter-spacing:0.05em;text-transform:uppercase;}
.pts{display:inline-block;background:var(--green);color:#fff;border-radius:20px;font-size:0.72rem;font-weight:700;padding:0.18rem 0.65rem;}

/* Avatars */
.av-lg{width:76px;height:76px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.9rem;background:var(--green-lt);border:2px solid var(--border);margin:0 auto 0.7rem;}
.av-sm{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;background:var(--green-lt);border:2px solid var(--border);margin:0 auto 0.45rem;}

/* Book cards */
.bkc{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1.1rem;box-shadow:var(--shadow);transition:all 0.18s;min-height:220px;}
.bkc:hover{box-shadow:var(--shadow2);border-color:var(--green);transform:translateY(-2px);}
.bk-title{font-size:0.92rem;font-weight:700;color:var(--text);margin-bottom:0.2rem;line-height:1.3;}
.bk-auth{font-size:0.78rem;color:var(--text3);margin-bottom:0.45rem;}

/* Download links */
.dl{display:inline-block;background:var(--bg);border:1px solid var(--border);color:var(--text2)!important;border-radius:5px;padding:0.2rem 0.55rem;font-size:0.72rem;font-weight:500;text-decoration:none!important;margin:0.15rem 0.15rem 0 0;transition:all 0.15s;}
.dl:hover{border-color:var(--green);color:var(--green)!important;background:var(--green-lt);}

/* Reading area */
.read-area{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:2rem 2.4rem;box-shadow:var(--shadow);font-size:1rem;line-height:1.85;color:var(--text);}
.read-meta{font-size:0.7rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--text3);margin-bottom:0.4rem;}
.read-title{font-size:1.25rem;font-weight:700;color:var(--text);margin-bottom:1.4rem;padding-bottom:0.7rem;border-bottom:1px solid var(--border);}

/* Leaderboard */
.lbr{display:flex;align-items:center;padding:0.7rem 0.9rem;border-radius:8px;margin-bottom:0.3rem;background:var(--white);border:1px solid var(--border);transition:border-color 0.15s;}
.lbr:hover{border-color:var(--green);}
.lbr.top{border-left:3px solid var(--green);}
.lb-rank{font-size:0.9rem;font-weight:700;width:1.8rem;color:var(--text3);flex-shrink:0;}
.lb-name{font-size:0.88rem;font-weight:600;flex:1;color:var(--text);}
.lb-val{font-size:0.88rem;font-weight:700;color:var(--text);}

/* Bookmark */
.bmc{background:var(--white);border:1px solid var(--border);border-left:3px solid var(--green);border-radius:8px;padding:0.85rem 1rem;margin-bottom:0.45rem;}
.bm-title{font-size:0.88rem;font-weight:700;color:var(--text);}
.bm-note{font-size:0.83rem;color:var(--text2);margin-top:0.2rem;font-style:italic;}
.bm-meta{font-size:0.7rem;color:var(--text3);margin-top:0.3rem;}

/* Invite code */
.inv-code{font-size:1.7rem;font-weight:700;letter-spacing:0.22em;color:var(--green);background:var(--green-lt);border:1px dashed var(--green);border-radius:8px;padding:0.65rem 1.3rem;display:inline-block;margin:0.65rem 0;}

/* AI */
.ai-box{background:#F3FAF6;border:1px solid #C2DDD1;border-radius:var(--r);padding:1.1rem 1.3rem;margin-bottom:0.9rem;}
.ai-lbl{font-size:0.65rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--green);margin-bottom:0.45rem;}

/* Divider */
hr.div{border:none;height:1px;background:var(--border);margin:1.4rem 0;}

/* Alerts */
div[data-testid="stAlert"]{border-radius:8px!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:0.87rem!important;}
[data-baseweb="select"] *{font-family:'Plus Jakarta Sans',sans-serif!important;}

@media(max-width:640px){
  .block-container{padding:1rem 0.7rem 3rem!important;}
  .read-area{padding:1.1rem 0.9rem;font-size:0.93rem;}
  .ph h1{font-size:1.25rem!important;}
}
</style>
""", unsafe_allow_html=True)

# ── DB ──────────────────────────────────────────────────────
conn = sqlite3.connect("readwithwaleed.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY, nickname TEXT, email TEXT,
    password_hash TEXT, avatar TEXT DEFAULT '📚',
    points INTEGER DEFAULT 0, invite_code TEXT UNIQUE,
    invited_by TEXT, joined_date TEXT, bio TEXT DEFAULT '', avatar_img TEXT DEFAULT '')""")
existing_cols = [r[1] for r in c.execute("PRAGMA table_info(users)").fetchall()]
for col, defval in [("bio","''"),("avatar_img","''")]:
    if col not in existing_cols:
        c.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT {defval}")
        conn.commit()
c.execute("""CREATE TABLE IF NOT EXISTS reading_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, book TEXT, pages INTEGER, date TEXT, notes TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, book TEXT, page_ref TEXT, note TEXT, created_date TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, category TEXT, message TEXT, rating INTEGER, created_date TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS points_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, points INTEGER, reason TEXT, date TEXT)""")
conn.commit()

# ── Constants ───────────────────────────────────────────────
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
    {"id":"1342","title":"Pride and Prejudice","author":"Jane Austen","genre":"Classic Romance","emoji":"💕","year":1813,"description":"A witty story of love and society through the Bennet family's five daughters.","gutenberg_id":"1342","pages_est":432},
    {"id":"11","title":"Alice's Adventures in Wonderland","author":"Lewis Carroll","genre":"Fantasy","emoji":"🐇","year":1865,"description":"A young girl falls into a rabbit hole and discovers a fantastical world.","gutenberg_id":"11","pages_est":176},
    {"id":"1661","title":"The Adventures of Sherlock Holmes","author":"Arthur Conan Doyle","genre":"Mystery","emoji":"🔍","year":1892,"description":"Twelve stories featuring the legendary detective Sherlock Holmes.","gutenberg_id":"1661","pages_est":307},
    {"id":"84","title":"Frankenstein","author":"Mary Shelley","genre":"Gothic Horror","emoji":"⚡","year":1818,"description":"A scientist creates a sentient creature with terrifying consequences.","gutenberg_id":"84","pages_est":280},
    {"id":"1260","title":"Jane Eyre","author":"Charlotte Brontë","genre":"Classic Romance","emoji":"🕯","year":1847,"description":"An orphaned governess falls for the mysterious Mr. Rochester.","gutenberg_id":"1260","pages_est":532},
    {"id":"2701","title":"Moby-Dick","author":"Herman Melville","genre":"Adventure","emoji":"🐋","year":1851,"description":"Captain Ahab's obsessive quest to hunt the great white whale.","gutenberg_id":"2701","pages_est":720},
    {"id":"74","title":"The Adventures of Tom Sawyer","author":"Mark Twain","genre":"Adventure","emoji":"🛶","year":1876,"description":"The mischievous adventures of a boy along the Mississippi River.","gutenberg_id":"74","pages_est":274},
    {"id":"345","title":"Dracula","author":"Bram Stoker","genre":"Gothic Horror","emoji":"🧛","year":1897,"description":"Jonathan Harker encounters the terrifying Count Dracula in Transylvania.","gutenberg_id":"345","pages_est":418},
    {"id":"1232","title":"The Prince","author":"Niccolò Machiavelli","genre":"Philosophy","emoji":"👑","year":1532,"description":"A political treatise on the acquisition and use of power.","gutenberg_id":"1232","pages_est":140},
    {"id":"2542","title":"A Doll's House","author":"Henrik Ibsen","genre":"Drama","emoji":"🏠","year":1879,"description":"Nora Helmer discovers her true position in her seemingly perfect marriage.","gutenberg_id":"2542","pages_est":112},
    {"id":"16328","title":"Beowulf","author":"Anonymous","genre":"Epic Poetry","emoji":"⚔️","year":700,"description":"The oldest surviving Old English epic poem about the hero Beowulf.","gutenberg_id":"16328","pages_est":96},
    {"id":"4300","title":"Ulysses","author":"James Joyce","genre":"Modernist","emoji":"🌊","year":1922,"description":"A day in the life of Leopold Bloom wandering through Dublin.","gutenberg_id":"4300","pages_est":730},
    {"id":"1400","title":"Great Expectations","author":"Charles Dickens","genre":"Classic Fiction","emoji":"🎩","year":1861,"description":"Young Pip's journey from humble origins to London society.","gutenberg_id":"1400","pages_est":544},
    {"id":"2600","title":"War and Peace","author":"Leo Tolstoy","genre":"Historical Fiction","emoji":"⚔️","year":1869,"description":"An epic portrayal of Russian society during the Napoleonic era.","gutenberg_id":"2600","pages_est":1296},
    {"id":"174","title":"The Picture of Dorian Gray","author":"Oscar Wilde","genre":"Gothic Fiction","emoji":"🖼","year":1890,"description":"A young man sells his soul for eternal youth while his portrait ages.","gutenberg_id":"174","pages_est":254},
]
AI_SUMMARIES = {
    "1342":"Pride and Prejudice follows Elizabeth Bennet as she navigates issues of manners, upbringing, and marriage in Georgian England. The novel's central romance between Elizabeth and the proud Mr. Darcy is a study in overcoming first impressions. Austen's sharp wit illuminates the social constraints on women and the absurdity of class-obsessed society.",
    "11":"Alice follows a young girl's surreal journey through Wonderland after tumbling down a rabbit hole. Carroll uses fantasy and wordplay to explore themes of identity, logic, and the often arbitrary nature of adult rules. Each encounter — from the Mad Hatter's tea party to the Queen's croquet game — challenges Alice's sense of reality.",
    "1661":"The Adventures of Sherlock Holmes collects twelve cases solved by the brilliant consulting detective. Holmes's legendary deductive method makes each mystery feel both thrilling and logical. Dr. Watson's narration humanises Holmes while grounding the reader in Victorian London's fog-filled streets.",
    "84":"Frankenstein explores what happens when human ambition overreaches ethical limits. Victor Frankenstein's creation of life leads to catastrophic loneliness and violence — not because the creature is evil, but because he is abandoned. Shelley asks whether the true monster is the scientist or the society that rejects what it cannot understand.",
    "1260":"Jane Eyre charts one woman's journey from orphaned childhood to independent womanhood. Jane's moral strength and refusal to sacrifice her integrity for love or security make her a revolutionary heroine. The novel's Gothic atmosphere and psychological depth transformed Victorian fiction.",
    "2701":"Moby-Dick is both a thrilling adventure and a profound meditation on obsession, fate, and humanity's place in nature. Captain Ahab's monomania drives the Pequod toward doom, but it is Ishmael's curiosity about everything that gives the novel its astonishing breadth.",
    "345":"Dracula, told through letters and journal entries, follows a group of heroes trying to stop the vampire Count from conquering England. Stoker uses the epistolary format to build dread gradually, and the novel's anxieties about foreign invasion and modernity still resonate today.",
    "174":"The Picture of Dorian Gray is Wilde's only novel — a dark fable about beauty, corruption, and consequence. Dorian, gifted with eternal youth while his portrait bears his sins, descends into hedonism and cruelty. Wilde embeds a sharp critique of aestheticism and Victorian hypocrisy beneath the Gothic surface.",
    "1400":"Great Expectations follows Pip from a blacksmith's forge to London's elite, driven by a mysterious benefactor. Dickens uses Pip's journey to critique social class, the emptiness of wealth, and the danger of discarding genuine love for ambition. Miss Havisham and Magwitch are among literature's most unforgettable characters.",
}

# ── Helpers ─────────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def gen_invite(u): return hashlib.md5(u.encode()).hexdigest()[:8].upper()

def encode_image(f):
    ext = f.name.split('.')[-1].lower()
    mime = {'jpg':'jpeg','jpeg':'jpeg','png':'png','gif':'gif','webp':'webp'}.get(ext,'jpeg')
    return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"

def av_lg_html(img, emoji):
    if img:
        return f"<div style='width:76px;height:76px;border-radius:50%;overflow:hidden;border:2px solid #E5E5E5;margin:0 auto 0.7rem;'><img src='{img}' style='width:100%;height:100%;object-fit:cover;'/></div>"
    return f"<div class='av-lg'>{emoji}</div>"

def av_sm_html(img, emoji):
    if img:
        return f"<div style='width:48px;height:48px;border-radius:50%;overflow:hidden;border:2px solid #E5E5E5;margin:0 auto 0.45rem;'><img src='{img}' style='width:100%;height:100%;object-fit:cover;'/></div>"
    return f"<div class='av-sm'>{emoji}</div>"

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
    for url in [f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
                f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"]:
        try:
            r = requests.get(url, timeout=14)
            if r.status_code == 200:
                t = r.text
                s = t.find("*** START OF"); t = t[s+60:] if s != -1 else t
                e = t.find("*** END OF"); t = t[:e] if e != -1 else t
                return t[:max_chars].strip()
        except: continue
    return None

def get_dl(book):
    bid = book["gutenberg_id"]; q = urllib.parse.quote(book["title"]+" "+book["author"])
    return {"Project Gutenberg":f"https://www.gutenberg.org/ebooks/{bid}",
            "Standard Ebooks":f"https://standardebooks.org/search?q={urllib.parse.quote(book['title'])}",
            "Open Library":f"https://openlibrary.org/search?q={q}",
            "PDF Drive":f"https://www.pdfdrive.com/search?q={q}",
            "Z-Library":f"https://z-lib.id/s/{q}"}

# ── Session state ────────────────────────────────────────────
for k,v in [("logged_in",False),("current_user",None),("reading_book",None),("book_cache",{})]:
    if k not in st.session_state: st.session_state[k]=v

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.1rem 0 0.9rem;'>
      <div style='font-size:1.15rem;font-weight:700;color:#1C1C1C;'>📖 ReadWithWaleed</div>
      <div style='font-size:0.72rem;color:#999;margin-top:0.15rem;letter-spacing:0.03em;'>Your reading companion</div>
    </div>
    <hr style='border:none;height:1px;background:#E5E5E5;margin-bottom:1rem;'>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        ur = c.execute("SELECT * FROM users WHERE username=?", (st.session_state.current_user,)).fetchone()
        if ur:
            _u,_nick,_em,_,_av,_pts,_ic,_ib,_jd,_bio,_aimg = ur
            _dn = _nick if _nick else _u
            st.markdown(f"""
            <div style='text-align:center;padding:0.2rem 0 0.9rem;'>
              {av_sm_html(_aimg,_av)}
              <div style='font-size:0.95rem;font-weight:700;color:#1C1C1C;'>{_dn}</div>
              <div style='font-size:0.72rem;color:#999;'>@{_u}</div>
              <div style='margin-top:0.45rem;'><span class='pts'>{_pts:,} pts</span></div>
            </div>
            <hr style='border:none;height:1px;background:#E5E5E5;margin-bottom:0.7rem;'>
            """, unsafe_allow_html=True)

        page = st.radio("Navigation", [
            "Dashboard", "My Profile", "Log Reading",
            "Book Library", "Bookmarks", "Timer",
            "Invite Friends", "Feedback", "Leaderboard"
        ], label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.reading_book = None
            st.rerun()
    else:
        page = "auth"

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem;color:#CCC;text-align:center;'>ReadWithWaleed · Built with ♥</div>", unsafe_allow_html=True)

# ── AUTH ─────────────────────────────────────────────────────
if not st.session_state.logged_in:
    # Landing
    st.markdown("""
    <div style='background:#fff;border:1px solid #E5E5E5;border-radius:12px;padding:2.5rem 2rem;margin-bottom:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.06);'>
      <div style='display:flex;align-items:center;gap:0.6rem;margin-bottom:0.9rem;'>
        <span style='font-size:1.8rem;'>📖</span>
        <span style='font-size:1.5rem;font-weight:700;color:#1C1C1C;'>ReadWithWaleed</span>
      </div>
      <div style='font-size:1.05rem;color:#555;line-height:1.6;max-width:520px;'>
        Track your reading. Explore free books. Build streaks. Share with friends.
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_li, tab_su = st.tabs(["Sign In", "Create Account"])

    with tab_li:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:1.1rem;font-weight:700;margin-bottom:0.2rem;'>Welcome back</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:0.85rem;color:#999;margin-bottom:1.2rem;'>Enter your details to continue</div>", unsafe_allow_html=True)
            li_u = st.text_input("Username", key="li_u", placeholder="your_username")
            li_p = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True, key="btn_li"):
                row = c.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (li_u, hash_pw(li_p))).fetchone()
                if row:
                    st.session_state.logged_in = True
                    st.session_state.current_user = li_u
                    add_points(li_u, 2, "Daily login")
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_su:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:1.1rem;font-weight:700;margin-bottom:0.2rem;'>Create your account</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.85rem;color:#999;margin-bottom:1.3rem;'>Join the ReadWithWaleed community</div>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#999;margin-bottom:0.6rem;border-bottom:1px solid #E5E5E5;padding-bottom:0.4rem;'>Account Details</div>", unsafe_allow_html=True)
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            su_u = st.text_input("Username *", key="su_u", placeholder="john_reads")
            su_e = st.text_input("Email *", key="su_e", placeholder="you@email.com")
        with r1c2:
            su_p = st.text_input("Password *", type="password", key="su_p", placeholder="Min. 6 characters")
            su_p2 = st.text_input("Confirm Password *", type="password", key="su_p2", placeholder="Repeat password")

        st.markdown("<br><div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#999;margin-bottom:0.6rem;border-bottom:1px solid #E5E5E5;padding-bottom:0.4rem;'>Profile Details</div>", unsafe_allow_html=True)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            su_n = st.text_input("Display Name", key="su_n", placeholder="What others see")
        with r2c2:
            su_av = st.selectbox("Avatar Emoji", AVATARS, key="su_av")

        st.markdown("<br><div style='font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#999;margin-bottom:0.6rem;border-bottom:1px solid #E5E5E5;padding-bottom:0.4rem;'>Optional</div>", unsafe_allow_html=True)
        su_inv = st.text_input("Invite Code", key="su_inv", placeholder="Friend's code — earn +50 bonus points")
        su_bio = st.text_area("Short Bio", key="su_bio", placeholder="Tell others about your reading interests...", height=65)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Create Account", use_container_width=True, key="btn_su"):
            if not su_u or not su_e or not su_p:
                st.warning("Please fill in all required fields.")
            elif len(su_p) < 6:
                st.error("Password must be at least 6 characters.")
            elif su_p != su_p2:
                st.error("Passwords do not match.")
            elif c.execute("SELECT 1 FROM users WHERE username=?", (su_u,)).fetchone():
                st.error("Username already taken.")
            elif c.execute("SELECT 1 FROM users WHERE email=?", (su_e,)).fetchone():
                st.error("Email already registered.")
            else:
                inv_code = gen_invite(su_u); inv_by = None; bonus = 0
                if su_inv:
                    ir = c.execute("SELECT username FROM users WHERE invite_code=?", (su_inv.strip().upper(),)).fetchone()
                    if ir: inv_by = ir[0]; bonus = 50; add_points(ir[0], 100, f"Invited {su_u}")
                    else: st.warning("Invite code not found — proceeding anyway.")
                c.execute("""INSERT INTO users (username,nickname,email,password_hash,avatar,points,invite_code,invited_by,joined_date,bio,avatar_img) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                    (su_u, su_n or su_u, su_e, hash_pw(su_p), su_av, bonus, inv_code, inv_by, datetime.today().strftime("%Y-%m-%d"), su_bio or "", ""))
                conn.commit()
                st.session_state.logged_in = True
                st.session_state.current_user = su_u
                st.balloons(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    f1,f2,f3,f4 = st.columns(4)
    for col,ic,t,d in [(f1,"📚","Free Library","15+ classics, readable in-app"),(f2,"🔥","Streaks","Build daily reading habits"),(f3,"🔖","Bookmarks","Save notes across any book"),(f4,"🤝","Invite & Earn","100 pts per friend you invite")]:
        with col:
            st.markdown(f"<div class='sc'><div class='si'>{ic}</div><div style='font-size:0.88rem;font-weight:700;color:#1C1C1C;margin-bottom:0.2rem;'>{t}</div><div style='font-size:0.78rem;color:#999;line-height:1.4;'>{d}</div></div>", unsafe_allow_html=True)
    st.stop()

# ── LOAD USER ────────────────────────────────────────────────
username = st.session_state.current_user
ur = c.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
uname,nickname,email,_,avatar,points,invite_code,invited_by,joined_date,bio,avatar_img = ur
display_name = nickname if nickname else uname
df_all = pd.read_sql_query("SELECT * FROM reading_logs WHERE username=?", conn, params=(username,))
if not df_all.empty: df_all["date"] = pd.to_datetime(df_all["date"])
total_pages = int(df_all["pages"].sum()) if not df_all.empty else 0
streak = compute_streak(df_all) if not df_all.empty else 0
books_count = df_all["book"].nunique() if not df_all.empty else 0

# ── IN-APP READER ────────────────────────────────────────────
if st.session_state.reading_book is not None:
    bk = st.session_state.reading_book; bid = bk["id"]
    dl_links = get_dl(bk)
    dl_html = " ".join([f'<a href="{u}" target="_blank" class="dl">⬇ {n}</a>' for n,u in dl_links.items()])

    st.markdown(f"""
    <div class='ph'>
      <div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;'>
        <span class='tag-gray'>Now Reading</span>
      </div>
      <h1 style='font-size:1.35rem;font-weight:700;margin:0 0 0.25rem;'>{bk['emoji']} {bk['title']}</h1>
      <div style='font-size:0.85rem;color:#999;margin-bottom:0.6rem;'>by {bk['author']} · {bk['genre']} · ~{bk.get('pages_est',300)} pages</div>
      <div>{dl_html}</div>
    </div>
    """, unsafe_allow_html=True)

    col_back, _ = st.columns([1,6])
    with col_back:
        if st.button("← Back to Library"): st.session_state.reading_book=None; st.rerun()

    ai_sum = AI_SUMMARIES.get(bid)
    if ai_sum:
        st.markdown(f"<div class='ai-box'><div class='ai-lbl'>🤖 AI Book Summary</div><div style='font-size:0.88rem;color:#444;line-height:1.7;'>{ai_sum}</div></div>", unsafe_allow_html=True)
        with st.expander("🔊 Listen to Summary (AI Voice)"):
            safe = ai_sum.replace("'","\\'").replace('"','\\"').replace('\n',' ')
            st.markdown(f"""
            <div style='padding:0.5rem 0;'>
              <button class='voice-btn primary' onclick="var u=new SpeechSynthesisUtterance('{safe}');u.rate=0.9;var vs=speechSynthesis.getVoices();var e=vs.find(v=>v.lang.startsWith('en'));if(e)u.voice=e;speechSynthesis.speak(u);">▶ Play</button>
              <button class='voice-btn' onclick="speechSynthesis.cancel();">⏹ Stop</button>
              <span style='font-size:0.75rem;color:#999;margin-left:0.5rem;'>Uses browser text-to-speech</span>
            </div>""", unsafe_allow_html=True)

    if bid not in st.session_state.book_cache:
        with st.spinner("Loading book from Project Gutenberg..."):
            st.session_state.book_cache[bid] = fetch_book_text(bid)
    text = st.session_state.book_cache.get(bid)

    if text:
        words = text.split(); chunk_size = 700
        total_chunks = max(1, len(words)//chunk_size)
        r_col, s_col = st.columns([3,1])

        with s_col:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='sec-lbl'>Navigation</div>", unsafe_allow_html=True)
            chunk_num = st.number_input("Section", min_value=1, max_value=total_chunks, value=1)
            st.progress(chunk_num/total_chunks)
            st.caption(f"Section {chunk_num} of {total_chunks}")
            st.markdown("</div><br>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='sec-lbl'>Log Session</div>", unsafe_allow_html=True)
            with st.form("rl"):
                mr = st.number_input("Minutes", min_value=1, max_value=180, value=15)
                pr = st.number_input("Pages", min_value=1, value=5)
                if st.form_submit_button("Log & Earn Points", use_container_width=True):
                    c.execute("INSERT INTO reading_logs VALUES (NULL,?,?,?,?,?)",(username,bk['title'],pr,datetime.today().strftime("%Y-%m-%d"),"In-app"))
                    conn.commit(); earned=(pr//5)*5+mr; add_points(username,earned,f"Read: {bk['title']}")
                    st.success(f"+{earned} pts!"); st.balloons()
            st.markdown("</div><br>", unsafe_allow_html=True)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='sec-lbl'>Bookmark</div>", unsafe_allow_html=True)
            with st.form("bmf"):
                bm_note = st.text_area("Note", placeholder="What stood out?", height=70)
                if st.form_submit_button("Save Bookmark", use_container_width=True):
                    c.execute("INSERT INTO bookmarks VALUES (NULL,?,?,?,?,?)",(username,bk['title'],f"Section {chunk_num}",bm_note,datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit(); st.success("Saved!")
            st.markdown("</div>", unsafe_allow_html=True)

        with r_col:
            start_w = (chunk_num-1)*chunk_size
            excerpt = " ".join(words[start_w:start_w+chunk_size])
            paras = [p.strip() for p in excerpt.replace("\r\n","\n").split("\n\n") if p.strip()]
            fmt = "".join([f"<p style='margin-bottom:1.15em;text-indent:1.8em;'>{p}</p>" for p in paras])
            st.markdown(f"<div class='read-area'><div class='read-meta'>{bk['genre']} · Section {chunk_num}/{total_chunks}</div><div class='read-title'>{bk['title']}</div>{fmt}</div>", unsafe_allow_html=True)
            first_p = (paras[0] if paras else "")[:300].replace("'","\\'").replace('"','\\"')
            st.markdown(f"""
            <div style='margin-top:0.75rem;display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;'>
              <button class='voice-btn' onclick="var u=new SpeechSynthesisUtterance('{first_p}');u.rate=0.88;speechSynthesis.speak(u);">🔊 Listen</button>
              <button class='voice-btn' onclick="speechSynthesis.cancel();">⏹ Stop</button>
              <span style='font-size:0.72rem;color:#999;'>First paragraph · browser TTS</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.warning("Couldn't load the book text. Use the download links above to read offline.")
    st.stop()

# ── DASHBOARD ────────────────────────────────────────────────
if page == "Dashboard":
    st.markdown(f"""
    <div class='ph'>
      <div style='display:flex;align-items:center;gap:0.9rem;'>
        {av_lg_html(avatar_img,avatar).replace('margin:0 auto 0.7rem','margin:0 0 0 0;flex-shrink:0')}
        <div>
          <h1>Hello, {display_name} 👋</h1>
          <p>Here's your reading overview for today.</p>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,ic,num,lbl in [(c1,"📄",f"{total_pages:,}","Total Pages"),(c2,"🔥",str(streak),"Day Streak"),(c3,"📚",str(books_count),"Books"),(c4,"⭐",f"{points:,}","Points")]:
        with col:
            st.markdown(f"<div class='sc'><div class='si'>{ic}</div><div class='sn'>{num}</div><div class='sl'>{lbl}</div></div>", unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    d1, d2 = st.columns([3,2])
    with d1:
        daily_bk = BOOKS[datetime.today().timetuple().tm_yday % len(BOOKS)]
        st.markdown("<div class='sec-lbl'>Today's Pick</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card' style='border-left:3px solid #2F6B4F;'>
          <div style='display:flex;gap:0.9rem;align-items:flex-start;'>
            <span style='font-size:2rem;flex-shrink:0;'>{daily_bk['emoji']}</span>
            <div>
              <div style='font-size:0.95rem;font-weight:700;color:#1C1C1C;margin-bottom:0.1rem;'>{daily_bk['title']}</div>
              <div style='font-size:0.78rem;color:#999;margin-bottom:0.5rem;'>by {daily_bk['author']} · {daily_bk['year']}</div>
              <div style='font-size:0.83rem;color:#555;line-height:1.5;'>{daily_bk['description']}</div>
              <div style='margin-top:0.6rem;'><span class='tag'>{daily_bk['genre']}</span></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("<div class='sec-lbl'>Quote of the Day</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card' style='height:calc(100% - 1.4rem);'>
          <div style='font-size:0.92rem;color:#555;font-style:italic;line-height:1.65;'>"{random.choice(QUOTES)}"</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='div'>", unsafe_allow_html=True)

    df_week = df_all[df_all["date"]>=pd.Timestamp(datetime.today()-timedelta(days=7))] if not df_all.empty else pd.DataFrame()
    weekly = int(df_week["pages"].sum()) if not df_week.empty else 0
    st.markdown(f"<div class='sec-lbl'>Weekly Challenge</div><div class='sec-ttl'>100 Pages This Week &nbsp; <span style='font-size:0.85rem;color:#2F6B4F;font-weight:600;'>{weekly}/100</span></div>", unsafe_allow_html=True)
    st.progress(min(weekly/100,1.0))

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    if not df_all.empty:
        st.markdown("<div class='sec-lbl'>Recent Sessions</div><div class='sec-ttl'>Reading History</div>", unsafe_allow_html=True)
        disp = df_all[["date","book","pages","notes"]].sort_values("date",ascending=False).copy()
        disp["date"] = disp["date"].dt.strftime("%b %d, %Y"); disp.columns=["Date","Book","Pages","Notes"]
        st.dataframe(disp, use_container_width=True, hide_index=True)
    else:
        st.info("No reading sessions yet. Go to Book Library to start reading, or Log Reading to track a book.")

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-lbl'>Achievements</div><div class='sec-ttl'>Badges</div>", unsafe_allow_html=True)
    badges = [(total_pages>=50,"🌱","First 50 Pages","You started the journey."),(total_pages>=200,"📘","200 Pages","Solid reading habits."),(total_pages>=500,"🏆","500 Pages","You're dedicated!"),(streak>=7,"🔥","Week Streak","7 days in a row!"),(books_count>=5,"📚","Bibliophile","5 books tracked."),(points>=500,"⭐","500 Points","Keep earning!")]
    earned_b=[x for x in badges if x[0]]; locked_b=[x for x in badges if not x[0]]
    if earned_b:
        bc1,bc2=st.columns(2)
        for i,(u,ic,t,d) in enumerate(earned_b):
            with (bc1 if i%2==0 else bc2):
                st.markdown(f"<div class='card-accent'><div style='display:flex;align-items:center;gap:0.75rem;'><span style='font-size:1.5rem;'>{ic}</span><div><div style='font-size:0.88rem;font-weight:700;'>{t}</div><div style='font-size:0.78rem;color:#999;'>{d}</div></div><span class='tag' style='margin-left:auto;'>Earned</span></div></div>", unsafe_allow_html=True)
    if locked_b:
        with st.expander(f"{len(locked_b)} badges to unlock"):
            for _,ic,t,d in locked_b:
                st.markdown(f"<div style='display:flex;align-items:center;gap:0.75rem;padding:0.6rem 0;border-bottom:1px solid #F0F0F0;opacity:0.4;'><span style='font-size:1.5rem;filter:grayscale(1);'>{ic}</span><div><div style='font-size:0.88rem;font-weight:700;'>{t}</div><div style='font-size:0.78rem;color:#999;'>{d}</div></div><span class='tag-gray' style='margin-left:auto;'>Locked</span></div>", unsafe_allow_html=True)

# ── MY PROFILE ───────────────────────────────────────────────
elif page == "My Profile":
    st.markdown("<div class='ph'><h1>My Profile</h1><p>Manage your account, photo, and preferences.</p></div>", unsafe_allow_html=True)
    pc1,pc2 = st.columns([1,2])

    with pc1:
        pts_rank = "Legend 🥇" if points>=1000 else ("Veteran 🥈" if points>=500 else ("Reader 🥉" if points>=100 else "Newcomer 🌱"))
        st.markdown(f"""
        <div class='card-lg' style='text-align:center;'>
          {av_lg_html(avatar_img,avatar)}
          <div style='font-size:1.05rem;font-weight:700;color:#1C1C1C;'>{display_name}</div>
          <div style='font-size:0.78rem;color:#999;margin:0.1rem 0 0.3rem;'>@{uname}</div>
          <div style='font-size:0.75rem;color:#999;margin-bottom:0.5rem;'>{email}</div>
          {"<div style='font-size:0.83rem;color:#555;font-style:italic;margin-bottom:0.6rem;line-height:1.4;'>" + bio + "</div>" if bio else ""}
          <span class='pts'>{points:,} pts</span>
          <div style='font-size:0.82rem;color:#2F6B4F;font-weight:600;margin-top:0.5rem;'>{pts_rank}</div>
          <div style='font-size:0.72rem;color:#999;margin-top:0.2rem;'>Member since {joined_date}</div>
          {"<div style='font-size:0.72rem;color:#2F6B4F;margin-top:0.2rem;'>Referred by @"+str(invited_by)+"</div>" if invited_by else ""}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for ic,val,lbl in [("📄",f"{total_pages:,}","Pages Read"),("🔥",str(streak),"Day Streak"),("📚",str(books_count),"Books")]:
            st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center;padding:0.55rem 0;border-bottom:1px solid #F0F0F0;'><span style='font-size:0.85rem;color:#555;'>{ic} {lbl}</span><span style='font-size:0.95rem;font-weight:700;'>{val}</span></div>", unsafe_allow_html=True)

    with pc2:
        # Photo upload
        st.markdown("<div class='sec-lbl'>Profile Photo</div><div class='sec-ttl'>Upload from Phone or Computer</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        ph1,ph2 = st.columns([1,2])
        with ph1:
            if avatar_img:
                st.markdown(f"<img src='{avatar_img}' style='width:80px;height:80px;border-radius:50%;object-fit:cover;border:2px solid #E5E5E5;display:block;margin:0 auto;'/>", unsafe_allow_html=True)
                st.caption("Current photo")
            else:
                st.markdown(f"<div class='av-lg' style='width:80px;height:80px;font-size:2rem;'>{avatar}</div>", unsafe_allow_html=True)
                st.caption("No photo yet")
        with ph2:
            st.markdown("<div style='font-size:0.82rem;color:#555;margin-bottom:0.5rem;'>JPG, PNG, GIF or WEBP · Max 5 MB</div>", unsafe_allow_html=True)
            uploaded = st.file_uploader("Photo", type=["jpg","jpeg","png","gif","webp"], key="photo_upload", label_visibility="collapsed")
            if uploaded is not None:
                if uploaded.size > 5*1024*1024:
                    st.error("File is over 5 MB.")
                else:
                    img_data = encode_image(uploaded)
                    c.execute("UPDATE users SET avatar_img=? WHERE username=?", (img_data, username))
                    conn.commit(); st.success("Photo updated!"); st.rerun()
            if avatar_img:
                if st.button("Remove Photo", key="rm"):
                    c.execute("UPDATE users SET avatar_img='' WHERE username=?", (username,))
                    conn.commit(); st.rerun()
        st.markdown("</div><br>", unsafe_allow_html=True)

        st.markdown("<div class='sec-lbl'>Edit Details</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        with st.form("ep"):
            e1,e2 = st.columns(2)
            with e1: new_nick = st.text_input("Display Name", value=nickname or "")
            with e2: new_av = st.selectbox("Emoji Avatar", AVATARS, index=AVATARS.index(avatar) if avatar in AVATARS else 0)
            new_bio = st.text_area("Bio", value=bio or "", placeholder="Tell others about yourself...", height=75)
            st.markdown("**Change Password** *(leave blank to keep current)*")
            p1,p2 = st.columns(2)
            with p1: new_pw = st.text_input("New Password", type="password")
            with p2: conf_pw = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Save Changes", use_container_width=True):
                if new_pw and new_pw != conf_pw: st.error("Passwords don't match.")
                else:
                    upd=["avatar=?","bio=?"]; pms=[new_av,new_bio]
                    if new_nick: upd.append("nickname=?"); pms.append(new_nick)
                    if new_pw: upd.append("password_hash=?"); pms.append(hash_pw(new_pw))
                    pms.append(username)
                    c.execute(f"UPDATE users SET {','.join(upd)} WHERE username=?", pms)
                    conn.commit(); st.success("Saved!")
        st.markdown("</div><br>", unsafe_allow_html=True)

        st.markdown("<div class='sec-lbl'>Points History</div>", unsafe_allow_html=True)
        pts_df = pd.read_sql_query("SELECT date,reason,points FROM points_log WHERE username=? ORDER BY id DESC LIMIT 20", conn, params=(username,))
        if not pts_df.empty:
            pts_df.columns=["Date","Reason","Points"]
            st.dataframe(pts_df, use_container_width=True, hide_index=True)
        else:
            st.info("No points history yet.")

# ── LOG READING ──────────────────────────────────────────────
elif page == "Log Reading":
    st.markdown("<div class='ph'><h1>Log a Reading Session</h1><p>Record what you read today to keep your streak alive.</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
    with st.form("lf", clear_on_submit=True):
        lc1,lc2 = st.columns([3,1])
        with lc1: book_t = st.text_input("Book Title", placeholder="e.g. Atomic Habits by James Clear")
        with lc2: pages_l = st.number_input("Pages Read", min_value=0, value=0)
        log_date = st.date_input("Date", value=datetime.today())
        notes_l = st.text_area("Notes (optional)", placeholder="Key insights from today's session...", height=80)
        if st.form_submit_button("Log Session", use_container_width=True):
            if not book_t: st.warning("Please enter a book title.")
            elif pages_l==0: st.warning("Please enter at least 1 page.")
            else:
                c.execute("INSERT INTO reading_logs VALUES (NULL,?,?,?,?,?)",(username,book_t,pages_l,str(log_date),notes_l))
                conn.commit(); earned=(pages_l//5)*5+10; add_points(username,earned,f"Logged: {book_t}")
                st.balloons(); st.success(f"Logged {pages_l} pages of {book_t} · +{earned} points earned!")
    st.markdown("</div>", unsafe_allow_html=True)
    if not df_all.empty:
        st.markdown("<br><div class='sec-lbl'>Recent Sessions</div>", unsafe_allow_html=True)
        rec = df_all.sort_values("date",ascending=False).head(5)[["date","book","pages"]].copy()
        rec["date"]=rec["date"].dt.strftime("%b %d, %Y"); rec.columns=["Date","Book","Pages"]
        st.dataframe(rec, use_container_width=True, hide_index=True)

# ── BOOK LIBRARY ─────────────────────────────────────────────
elif page == "Book Library":
    st.markdown("<div class='ph'><h1>Book Library</h1><p>Free classics from Project Gutenberg — read in-app or download.</p></div>", unsafe_allow_html=True)

    s1,s2 = st.columns([3,1])
    with s1: search_q = st.text_input("Search", placeholder="Title, author, genre...", label_visibility="collapsed")
    with s2:
        genre_f = st.selectbox("Genre", ["All genres"]+sorted(set(b["genre"] for b in BOOKS)), label_visibility="collapsed")

    filtered = BOOKS
    if search_q: filtered=[b for b in filtered if search_q.lower() in (b["title"]+b["author"]+b["genre"]).lower()]
    if genre_f!="All genres": filtered=[b for b in filtered if b["genre"]==genre_f]

    st.markdown(f"<div style='font-size:0.78rem;color:#999;margin-bottom:1rem;'>{len(filtered)} book(s)</div>", unsafe_allow_html=True)

    for rs in range(0,len(filtered),3):
        cols=st.columns(3)
        for i,col in enumerate(cols):
            idx=rs+i
            if idx<len(filtered):
                bk=filtered[idx]; dl=get_dl(bk)
                with col:
                    st.markdown(f"""
                    <div class='bkc'>
                      <div style='font-size:2rem;margin-bottom:0.4rem;'>{bk['emoji']}</div>
                      <div class='bk-title'>{bk['title']}</div>
                      <div class='bk-auth'>by {bk['author']} · {bk['year']}</div>
                      <span class='tag-gray'>{bk['genre']}</span>
                      <div style='font-size:0.78rem;color:#777;margin-top:0.5rem;line-height:1.45;'>{bk['description']}</div>
                      <div style='margin-top:0.75rem;'>{"".join([f'<a href="{u}" target="_blank" class="dl">⬇ {n}</a>' for n,u in list(dl.items())[:3]])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Read In-App", key=f"o_{bk['id']}", use_container_width=True):
                        st.session_state.reading_book=bk; st.rerun()

    st.markdown("<hr class='div'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-lbl'>More Free Book Sources</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display:flex;flex-wrap:wrap;gap:0.4rem;'>
      <a href='https://www.gutenberg.org' target='_blank' class='dl'>📚 Project Gutenberg (70,000+ books)</a>
      <a href='https://standardebooks.org' target='_blank' class='dl'>✨ Standard Ebooks</a>
      <a href='https://openlibrary.org' target='_blank' class='dl'>🌐 Open Library</a>
      <a href='https://www.pdfdrive.com' target='_blank' class='dl'>📄 PDF Drive</a>
      <a href='https://z-lib.id' target='_blank' class='dl'>🔍 Z-Library</a>
      <a href='https://archive.org/details/texts' target='_blank' class='dl'>🏛 Internet Archive</a>
    </div>
    """, unsafe_allow_html=True)

# ── BOOKMARKS ────────────────────────────────────────────────
elif page == "Bookmarks":
    st.markdown("<div class='ph'><h1>Bookmarks & Notes</h1><p>All your saved insights and annotations.</p></div>", unsafe_allow_html=True)
    t1,t2 = st.tabs(["My Bookmarks","Add New"])

    with t1:
        bm_df = pd.read_sql_query("SELECT * FROM bookmarks WHERE username=? ORDER BY id DESC", conn, params=(username,))
        if bm_df.empty:
            st.info("No bookmarks yet. Open a book in the Library and save notes while reading.")
        else:
            books_bm = ["All Books"]+sorted(bm_df["book"].unique().tolist())
            fb = st.selectbox("Filter by book", books_bm)
            filtered_bm = bm_df if fb=="All Books" else bm_df[bm_df["book"]==fb]
            st.markdown(f"<div style='font-size:0.78rem;color:#999;margin-bottom:0.8rem;'>{len(filtered_bm)} bookmark(s)</div>", unsafe_allow_html=True)
            for _,row in filtered_bm.iterrows():
                st.markdown(f"""
                <div class='bmc'>
                  <div class='bm-title'>📚 {row['book']}</div>
                  <div class='bm-meta'>📍 {row['page_ref']} · {row['created_date']}</div>
                  {"<div class='bm-note'>" + str(row['note']) + "</div>" if row['note'] else ""}
                </div>""", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
        with st.form("nbm", clear_on_submit=True):
            nb1,nb2 = st.columns(2)
            with nb1: bm_book = st.text_input("Book Title", placeholder="Which book?")
            with nb2: bm_page = st.text_input("Page / Section", placeholder="e.g. Page 127 or Chapter 4")
            bm_note_new = st.text_area("Your Note", placeholder="Write your thought or insight here...", height=110)
            if st.form_submit_button("Save Bookmark", use_container_width=True):
                if not bm_book: st.warning("Enter a book title.")
                else:
                    c.execute("INSERT INTO bookmarks VALUES (NULL,?,?,?,?,?)",(username,bm_book,bm_page or "—",bm_note_new,datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit(); add_points(username,3,f"Bookmark: {bm_book}"); st.success("Saved! +3 points.")
        st.markdown("</div>", unsafe_allow_html=True)

# ── TIMER ────────────────────────────────────────────────────
elif page == "Timer":
    st.markdown("<div class='ph'><h1>Reading Timer</h1><p>Focus on reading. Earn 1 point per minute.</p></div>", unsafe_allow_html=True)
    tl,tr = st.columns(2)
    with tl:
        st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
        preset = st.radio("Duration", ["5 min","15 min","25 min (Pomodoro)","45 min","Custom"])
        pmap = {"5 min":5,"15 min":15,"25 min (Pomodoro)":25,"45 min":45}
        minutes = pmap[preset] if preset!="Custom" else st.number_input("Minutes", 1, 180, 20)
        st.markdown(f"<div style='margin-top:0.8rem;padding:0.8rem;background:var(--green-lt);border-radius:8px;'><span style='font-size:0.85rem;color:#2F6B4F;font-weight:600;'>You'll earn {minutes} points on completion</span></div>", unsafe_allow_html=True)
        start_t = st.button("Start Timer", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with tr:
        tph=st.empty(); pph=st.empty(); mph=st.empty()
        tph.markdown(f"<div class='sc' style='padding:2.5rem;text-align:center;'><div style='font-size:3rem;margin-bottom:0.3rem;'>⏱</div><div class='sn' style='font-size:3rem;'>{minutes:02d}:00</div><div class='sl'>Ready</div></div>", unsafe_allow_html=True)
        if start_t:
            total_s = minutes*60
            for rem in range(total_s,-1,-1):
                m,s=divmod(rem,60)
                tph.markdown(f"<div class='sc' style='padding:2.5rem;text-align:center;'><div style='font-size:3rem;margin-bottom:0.3rem;'>🔥</div><div class='sn' style='font-size:3rem;'>{m:02d}:{s:02d}</div><div class='sl'>Stay focused</div></div>", unsafe_allow_html=True)
                pph.progress(rem/total_s if total_s else 0)
                time.sleep(1)
            add_points(username,minutes,f"{minutes}-min session")
            mph.success(f"Done! +{minutes} points earned. Log your pages now.")
            st.balloons()

# ── INVITE FRIENDS ───────────────────────────────────────────
elif page == "Invite Friends":
    st.markdown("<div class='ph'><h1>Invite Friends</h1><p>Share your code and earn 100 points per friend who joins.</p></div>", unsafe_allow_html=True)
    i1,i2 = st.columns(2)
    with i1:
        st.markdown("<div class='sec-lbl'>Your Invite Code</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-lg' style='text-align:center;'>
          <div style='font-size:0.78rem;color:#999;margin-bottom:0.3rem;'>Share this with friends when they sign up</div>
          <div class='inv-code'>{invite_code}</div>
          <div style='margin-top:0.9rem;background:#F8F8F8;border:1px solid #E5E5E5;border-radius:8px;padding:0.8rem;text-align:left;'>
            <div style='display:flex;justify-content:space-between;padding:0.35rem 0;border-bottom:1px solid #F0F0F0;'>
              <span style='font-size:0.83rem;color:#555;'>You earn per referral</span>
              <span style='font-size:0.9rem;font-weight:700;color:#2F6B4F;'>+100 pts</span>
            </div>
            <div style='display:flex;justify-content:space-between;padding:0.35rem 0;'>
              <span style='font-size:0.83rem;color:#555;'>Friend's welcome bonus</span>
              <span style='font-size:0.9rem;font-weight:700;color:#2F6B4F;'>+50 pts</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown("<div class='sec-lbl'>How It Works</div>", unsafe_allow_html=True)
        for num,t,d in [("1","Copy your code","Share it via WhatsApp, text, or email."),("2","Friend signs up","They enter your code when creating an account."),("3","Both earn points","You get 100 pts. They start with 50 bonus pts.")]:
            st.markdown(f"""
            <div style='display:flex;gap:0.85rem;margin-bottom:1.1rem;'>
              <div style='min-width:30px;height:30px;border-radius:50%;background:#2F6B4F;color:#fff;display:flex;align-items:center;justify-content:center;font-size:0.82rem;font-weight:700;flex-shrink:0;'>{num}</div>
              <div><div style='font-size:0.88rem;font-weight:700;margin-bottom:0.15rem;'>{t}</div><div style='font-size:0.8rem;color:#999;line-height:1.45;'>{d}</div></div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div'><div class='sec-lbl'>Your Referrals</div>", unsafe_allow_html=True)
    refs = pd.read_sql_query("SELECT username,nickname,avatar,avatar_img,points,joined_date FROM users WHERE invited_by=?", conn, params=(username,))
    if not refs.empty:
        for _,row in refs.iterrows():
            rn=row["nickname"] if row["nickname"] else row["username"]
            rav=row.get("avatar_img",""); rem=row.get("avatar","📚")
            av_h=(f"<img src='{rav}' style='width:36px;height:36px;border-radius:50%;object-fit:cover;border:1px solid #E5E5E5;flex-shrink:0;'/>" if rav else f"<span style='font-size:1.3rem;'>{rem}</span>")
            st.markdown(f"<div style='display:flex;align-items:center;gap:0.85rem;padding:0.65rem 0.9rem;background:#fff;border:1px solid #E5E5E5;border-radius:8px;margin-bottom:0.35rem;'>{av_h}<div style='flex:1;'><div style='font-size:0.88rem;font-weight:600;'>{rn}</div><div style='font-size:0.72rem;color:#999;'>Joined {row['joined_date']}</div></div><span class='pts'>{int(row['points']):,} pts</span></div>", unsafe_allow_html=True)
    else:
        st.info("No referrals yet. Share your code to start earning!")

# ── FEEDBACK ─────────────────────────────────────────────────
elif page == "Feedback":
    st.markdown("<div class='ph'><h1>Send Feedback</h1><p>Help us improve ReadWithWaleed. Every message is read.</p></div>", unsafe_allow_html=True)
    fb1,fb2 = st.columns([3,2])
    with fb1:
        st.markdown("<div class='card-lg'>", unsafe_allow_html=True)
        with st.form("fbf", clear_on_submit=True):
            fb_cat = st.selectbox("Category", ["💡 Feature Request","🐛 Bug Report","👍 Praise","📚 Book Request","🤔 Question","💬 Other"])
            fb_rating = st.slider("Rating", 1, 5, 5)
            fb_msg = st.text_area("Your Message", placeholder="What's on your mind?", height=130)
            if st.form_submit_button("Submit Feedback", use_container_width=True):
                if not fb_msg.strip(): st.warning("Please write a message.")
                else:
                    c.execute("INSERT INTO feedback VALUES (NULL,?,?,?,?,?)",(username,fb_cat,fb_msg,fb_rating,datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit(); add_points(username,10,"Submitted feedback")
                    st.success("Thank you! +10 points for your feedback."); st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)
    with fb2:
        st.markdown(f"""
        <div class='card-green' style='margin-bottom:1rem;'>
          <div style='font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;color:#2F6B4F;margin-bottom:0.4rem;'>Why it matters</div>
          <div style='font-size:0.95rem;font-weight:700;margin-bottom:0.4rem;'>You shape this app</div>
          <div style='font-size:0.83rem;color:#555;line-height:1.55;'>Every request and idea goes to the team. We use your feedback to decide what to build next.</div>
          <div style='margin-top:0.7rem;font-size:0.83rem;color:#2F6B4F;font-weight:600;'>+10 points per submission</div>
        </div>
        """, unsafe_allow_html=True)
        my_fb = pd.read_sql_query("SELECT created_date,category,rating,message FROM feedback WHERE username=? ORDER BY id DESC LIMIT 5",conn,params=(username,))
        if not my_fb.empty:
            st.markdown("<div class='sec-lbl'>Your Previous Feedback</div>", unsafe_allow_html=True)
            for _,row in my_fb.iterrows():
                stars="⭐"*int(row["rating"])
                st.markdown(f"<div class='bmc'><div class='bm-title'>{row['category']}</div><div class='bm-meta'>{row['created_date']} · {stars}</div><div class='bm-note'>{str(row['message'])[:110]}{'...' if len(str(row['message']))>110 else ''}</div></div>", unsafe_allow_html=True)

# ── LEADERBOARD ──────────────────────────────────────────────
elif page == "Leaderboard":
    st.markdown("<div class='ph'><h1>Leaderboard</h1><p>See how your reading compares across the community.</p></div>", unsafe_allow_html=True)
    tab_pg,tab_pts = st.tabs(["By Pages Read","By Points"])
    rank_icons={1:"🥇",2:"🥈",3:"🥉"}

    def render_lb(query, val_key, val_lbl):
        lb=pd.read_sql_query(query,conn)
        if lb.empty: st.info("No data yet."); return
        for i,row in lb.iterrows():
            rank=i+1; ri=rank_icons.get(rank,f"#{rank}"); is_top=rank<=3
            is_me=row["username"]==username
            av_e=row.get("avatar","📚"); av_p=row.get("avatar_img","")
            nick=row.get("nickname") or row["username"]
            me_b="<span class='tag' style='margin-left:0.4rem;font-size:0.6rem;'>YOU</span>" if is_me else ""
            val=int(row.get(val_key,0))
            av_h=(f"<img src='{av_p}' style='width:32px;height:32px;border-radius:50%;object-fit:cover;border:1px solid #E5E5E5;margin-right:0.6rem;vertical-align:middle;flex-shrink:0;'/>" if av_p else f"<span style='font-size:1rem;margin-right:0.6rem;'>{av_e}</span>")
            st.markdown(f"""
            <div class='lbr {"top" if is_top else ""}'>
              <span class='lb-rank'>{ri}</span>
              {av_h}
              <span class='lb-name'>{nick}{me_b}</span>
              <span style='font-size:0.72rem;color:#999;margin-right:0.8rem;'>{int(row.get("books",0))} books</span>
              <span class='lb-val'>{val:,} <span style='font-size:0.7rem;color:#999;font-weight:400;'>{val_lbl}</span></span>
            </div>""", unsafe_allow_html=True)

    with tab_pg:
        render_lb("""SELECT u.username,u.nickname,u.avatar,u.avatar_img,
            COALESCE(SUM(r.pages),0) as total_pages,COUNT(DISTINCT r.book) as books
            FROM users u LEFT JOIN reading_logs r ON u.username=r.username
            GROUP BY u.username ORDER BY total_pages DESC LIMIT 10""","total_pages","pages")
    with tab_pts:
        render_lb("""SELECT username,nickname,avatar,avatar_img,points as total_points,0 as books
            FROM users ORDER BY points DESC LIMIT 10""","total_points","pts")
