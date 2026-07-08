import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json
import hashlib
import base64
import threading
import uuid
from urllib.parse import urljoin
from datetime import datetime
from duckduckgo_search import DDGS

# ==========================================
# PAGE CONFIGURATION & STYLING (RTL SUPPORT)
# ==========================================
st.set_page_config(
    page_title="סוכן הורדת מאמרים אקדמאיים",
    page_icon="📑",
    layout="wide" # Wide layout looks more premium
)

# Custom CSS for Premium Glassmorphic Theme with Hebrew RTL Alignment
st.markdown(
    """
    <style>
    /* 1. Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&family=Rubik:wght@400;500;700&display=swap');

    /* 2. Global Page Styling & Typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Assistant', 'Rubik', 'Segoe UI', sans-serif !important;
        direction: RTL;
        text-align: right;
        background-color: #0b0f19; /* Sleek Dark Slate */
    }

    /* 3. RTL Adjustments for Streamlit Components */
    .stMarkdown p, .stMarkdown li, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
        text-align: right !important;
        direction: RTL !important;
        font-family: 'Rubik', sans-serif;
    }
    
    input, textarea, select, [data-testid="stHeader"] {
        direction: RTL !important;
        text-align: right !important;
    }
    
    div[data-testid="column"] {
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* Adjust list item margins for Hebrew bullet points */
    .stMarkdown ul {
        padding-right: 20px !important;
        padding-left: 0px !important;
        direction: RTL !important;
    }

    /* 4. Elegant Glassmorphism Cards */
    .premium-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .premium-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }

    /* 5. Custom Button Styling */
    .stButton button {
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    
    /* Primary Button Style (Gradient & Glow) */
    .stButton button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #14b8a6 100%) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
    }
    .stButton button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #0d9488 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    }
    
    /* Secondary Button Style (Glassmorphic dark with borders) */
    .stButton button[data-testid="baseButton-secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e5e7eb !important;
    }
    .stButton button[data-testid="baseButton-secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(20, 184, 166, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton button:active {
        transform: translateY(1px) !important;
    }

    /* 6. Form Field Enhancements */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f3f4f6 !important;
        font-size: 15px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* 7. Sidebar Recent Searches Item Styling */
    .history-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 8px;
        transition: background 0.2s ease;
        text-align: right;
    }
    .history-item:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(20, 184, 166, 0.3);
    }
    
    /* 8. Elegant Status Notifications */
    .success-alert {
        border-right: 4px solid #10b981;
        background: rgba(16, 185, 129, 0.1);
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 15px;
        text-align: right;
        direction: RTL;
    }
    .warning-alert {
        border-right: 4px solid #f59e0b;
        background: rgba(245, 158, 11, 0.1);
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 15px;
        text-align: right;
        direction: RTL;
    }
    
    /* 9. Scrollable Iframe Wrapper */
    .pdf-preview-wrapper {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
# Template variables for internal police networks (as per forensic-rd-env-context rules)
POLICE_INTERNAL_SERVER_IP = "10.x.x.x"  # Swap with internal police server IP if routing via intranet proxy
INTERNAL_LOGGING_SERVER = "http://10.x.x.x:5000/log"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
CROSSREF_MAILTO = "mop.agent@gmail.com"
DEFAULT_GAS_URL = "https://script.google.com/macros/s/AKfycbxrbYur_N9a_Fb_70GxIbOdMdwvIxymfeFhUhgK1i6Y3CjaN_Q253EonyizxWb3Ktccgw/exec"

# Directories for caching & logging
CACHE_DIR = "pdf_cache"
HISTORY_FILE = "search_history.json"
os.makedirs(CACHE_DIR, exist_ok=True)

# DOI Regex
DOI_REGEX = r"(10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+)"

# Sci-Hub mirrors
SCIHUB_MIRRORS = [
    "https://sci-hub.se",
    "https://sci-hub.st",
    "https://sci-hub.ru"
]

# Thread lock for thread-safe writing to the history log
history_lock = threading.RLock()

# ==========================================
# SECURITY & AUTHENTICATION (PASSWORD CHECK)
# ==========================================
def check_password():
    """Returns True if the user has entered the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets.get("password", "123456"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password in session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Render a premium glassmorphic login card
    st.markdown(
        """
        <div style="max-width: 500px; margin: 80px auto 20px auto; padding: 30px; 
                    background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(16px);
                    -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.07); 
                    border-radius: 14px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                    text-align: center; direction: RTL;">
            <h2 style="font-family: 'Rubik', sans-serif; font-size: 1.8rem; font-weight: 700; 
                       background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 50%, #2dd4bf 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">
                כניסה למערכת 🔐
            </h2>
            <p style="color: #9ca3af; font-size: 1rem; margin-bottom: 20px; font-family: 'Assistant', sans-serif;">
                סוכן הורדת מאמרים אקדמאיים - מדור מו"פ, חטיבת מז"פ
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "סיסמה חטיבתית:",
            type="password",
            on_change=password_entered,
            key="password",
            placeholder="הזן סיסמת גישה..."
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.markdown(
                """
                <div class="warning-alert" style="margin-top: 10px; text-align: center;">
                    😕 הסיסמה שהוזנה אינה נכונה. אנא נסה שנית.
                </div>
                """,
                unsafe_allow_html=True
            )
    return False

# ==========================================
# USER IDENTIFICATION & HISTORY FUNCTIONS
# ==========================================
def get_user_id():
    """Generate a unique, persistent hash for the device based on IP and Browser."""
    try:
        headers = st.context.headers
        ip = headers.get("X-Forwarded-For", "local_user")
        ua = headers.get("User-Agent", "unknown_browser")
        user_hash = hashlib.md5(f"{ip}_{ua}".encode()).hexdigest()
        return user_hash[:12]
    except Exception:
        if "session_user_uuid" not in st.session_state:
            st.session_state["session_user_uuid"] = f"session_{uuid.uuid4().hex[:8]}"
        return st.session_state["session_user_uuid"]

def post_to_google_sheets(gas_url, payload):
    """Fire-and-forget logging to Google Sheets without blocking the main UI thread."""
    try:
        requests.post(gas_url, json=payload, timeout=8)
    except Exception:
        pass

def log_search(user_id, query, resolved_title, doi, status, link_found, gas_url=""):
    """Logs the search details locally (thread-safe JSON) and sends to Google Sheets in background."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "query": query,
        "resolved_title": resolved_title or query,
        "doi": doi or "N/A",
        "status": status,
        "link_found": link_found or "N/A"
    }
    
    # 1. Thread-safe Local JSON Logging with Size Truncation
    with history_lock:
        history = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                pass
                
        history.insert(0, log_entry)
        history = history[:200]  # Cap history size at 200 items to prevent bloating
        
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    # 2. Asynchronous Google Sheets Apps Script Logging
    if gas_url:
        payload = {
            "userId": user_id,
            "query": query,
            "resolvedTitle": resolved_title or query,
            "doi": doi or "N/A",
            "status": status,
            "linkFound": link_found or "N/A"
        }
        threading.Thread(target=post_to_google_sheets, args=(gas_url, payload), daemon=True).start()

def get_user_history(user_id):
    """Retrieve the last 5 searches for this specific user safely."""
    with history_lock:
        if not os.path.exists(HISTORY_FILE):
            return []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
            return [entry for entry in history if entry.get("user_id") == user_id][:5]
        except Exception:
            return []

# ==========================================
# LOCAL PDF CACHING & PRUNING (LRU)
# ==========================================
def prune_pdf_cache(cache_dir, max_files=500, max_size_mb=300):
    """Removes the oldest cached PDF files if limits are exceeded (LRU)."""
    try:
        if not os.path.exists(cache_dir):
            return
        files = []
        total_size = 0
        for entry in os.scandir(cache_dir):
            if entry.is_file() and entry.name.endswith(".pdf"):
                stat = entry.stat()
                files.append((entry.path, stat.st_mtime, stat.st_size))
                total_size += stat.st_size
        
        max_size_bytes = max_size_mb * 1024 * 1024
        if len(files) > max_files or total_size > max_size_bytes:
            # Sort oldest modified first
            files.sort(key=lambda x: x[1])
            for path, _, size in files:
                try:
                    os.remove(path)
                    total_size -= size
                    if len(files) <= max_files * 0.8 and total_size <= max_size_bytes * 0.8:
                        break
                except Exception:
                    pass
    except Exception:
        pass

def get_cached_pdf(doi):
    """Retrieve cached PDF bytes if available and valid."""
    if not doi:
        return None
    cache_path = os.path.join(CACHE_DIR, f"{hashlib.md5(doi.encode()).hexdigest()}.pdf")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "rb") as f:
                content = f.read()
            # Verify it's a valid PDF (starts with %PDF)
            if content.startswith(b"%PDF") or b"%PDF" in content[:1024]:
                return content
            else:
                # Corrupt cache file, delete it so it won't block future downloads
                try:
                    os.remove(cache_path)
                except Exception:
                    pass
        except Exception:
            pass
    return None

def save_pdf_to_cache(doi, pdf_bytes):
    """Save resolved PDF bytes to local cache atomically."""
    if not doi or not pdf_bytes:
        return
    cache_path = os.path.join(CACHE_DIR, f"{hashlib.md5(doi.encode()).hexdigest()}.pdf")
    temp_path = cache_path + ".tmp"
    try:
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes)
        os.replace(temp_path, cache_path)
        # Run LRU pruning
        prune_pdf_cache(CACHE_DIR)
    except Exception:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

# ==========================================
# UTILITY & HELPER FUNCTIONS
# ==========================================
def extract_doi_from_text(text):
    match = re.search(DOI_REGEX, text.strip())
    if match:
        return match.group(1)
    return None

def normalize_url(url, base_url):
    if not url:
        return None
    if url.startswith("//"):
        return "https:" + url
    return urljoin(base_url, url)

def check_link_is_pdf(url):
    """Verify if URL points to a PDF without connection leaks."""
    try:
        # Use HEAD request for efficiency first
        response_head = requests.head(url, headers=HEADERS, timeout=5, allow_redirects=True)
        content_type = response_head.headers.get("Content-Type", "").lower()
        if "pdf" in content_type:
            return True
        if "html" in content_type:
            return False
    except Exception:
        pass

    # Fallback to streaming GET wrapped in a 'with' block
    try:
        with requests.get(url, headers=HEADERS, timeout=8, stream=True) as response:
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" in content_type:
                    return False
                if "pdf" in content_type:
                    return True
                chunk = next(response.iter_content(1024), b"")
                if b"%PDF" in chunk:
                    return True
        return False
    except Exception:
        pass
    return False

def is_academic_url(url):
    """Filter out obviously non-academic or general domains from fallback results."""
    if not url:
        return False
        
    blocked_domains = [
        "youtube.com", "youtu.be", "wikipedia.org", "facebook.com", "twitter.com", "x.com", 
        "instagram.com", "reddit.com", "pinterest.com", "amazon.com", "ebay.com", "netflix.com", 
        "vimeo.com", "tiktok.com", "github.com", "gitlab.com", "bitbucket.org", "stackoverflow.com", 
        "quora.com", "medium.com", "linkedin.com", "tumblr.com", "flickr.com", "imgur.com", 
        "imdb.com", "spotify.com", "apple.com", "microsoft.com", "google.com", "yahoo.com", "bing.com"
    ]
    
    url_lower = url.lower()
    for domain in blocked_domains:
        if domain in url_lower:
            return False
    return True

def sanitize_search_query(title):
    """Sanitize and shorten long titles so search engines don't get confused and return generic results."""
    if not title:
        return ""
    if re.search(DOI_REGEX, title):
        return title
        
    # Remove quotes, colons, brackets, and punctuation
    clean_title = re.sub(r'["\':;,.\-\(\)\[\]\{\}]', ' ', title)
    words = clean_title.split()
    
    # Take at most 7 words. If it starts with common stopwords, take a bit more
    limit = 7
    if words and words[0].lower() in ["a", "an", "the", "on", "in", "of", "to"]:
        limit = 9
        
    short_query = " ".join(words[:limit])
    return short_query

def fetch_paper_title(doi):
    """Fetch official paper title from Crossref or Semantic Scholar given a DOI."""
    # 1. Try Crossref directly
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, headers=HEADERS, timeout=7)
        if response.status_code == 200:
            data = response.json()
            title_list = data.get("message", {}).get("title") or []
            if title_list:
                return title_list[0]
    except Exception:
        pass
        
    # 2. Try Semantic Scholar
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
        params = {"fields": "title"}
        response = requests.get(url, params=params, timeout=7)
        if response.status_code == 200:
            data = response.json()
            return data.get("title")
    except Exception:
        pass
        
    return None

# ==========================================
# AGENT PIPELINE STEPS
# ==========================================

# Step 1: DOI Resolution (Crossref & Semantic Scholar)
def resolve_title_to_doi(title):
    url = "https://api.crossref.org/works"
    params = {"query": title, "rows": 1, "mailto": CROSSREF_MAILTO}
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("message", {}).get("items", [])
            if items:
                item = items[0]
                doi = item.get("DOI")
                title_list = item.get("title") or [""]
                title_resolved = title_list[0] if isinstance(title_list, list) and title_list else ""
                return doi, title_resolved
    except Exception as e:
        st.warning(f"שגיאה בהתחברות ל-Crossref: {e}")
    return None, None

def resolve_title_to_doi_semantic_scholar(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title, "limit": 1, "fields": "title,DOI"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            papers = data.get("data", [])
            if papers:
                paper = papers[0]
                doi = paper.get("DOI")
                title_resolved = paper.get("title")
                return doi, title_resolved
    except Exception:
        pass
    return None, None

# Step 2: Unpaywall (Open Access)
def get_unpaywall_data(doi):
    url = f"https://api.unpaywall.org/v2/{doi}"
    params = {"email": CROSSREF_MAILTO}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("is_oa"):
                best_loc = data.get("best_oa_location") or {}
                pdf_url = best_loc.get("url_for_pdf")
                landing_url = best_loc.get("url")
                
                if not pdf_url:
                    for loc in (data.get("oa_locations") or []):
                        if loc:
                            pdf_url = loc.get("url_for_pdf")
                            if pdf_url:
                                break
                return pdf_url, landing_url
    except Exception:
        pass
    return None, None

# Step 2b: Semantic Scholar (Open Access)
def get_semantic_scholar_data(doi):
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    params = {"fields": "title,openAccessPdf,url"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            oa_info = data.get("openAccessPdf")
            pdf_url = oa_info.get("url") if oa_info else None
            landing_url = data.get("url")
            return pdf_url, landing_url
    except Exception:
        pass
    return None, None

# Step 3: Sci-Hub Scraper
def get_scihub_pdf(doi):
    for mirror in SCIHUB_MIRRORS:
        url = f"{mirror}/{doi}"
        try:
            time.sleep(1)
            response = requests.get(url, headers=HEADERS, timeout=12)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                iframe = soup.find("iframe", id="pdf")
                if iframe and iframe.get("src"):
                    resolved = normalize_url(iframe.get("src"), url)
                    if resolved: return resolved
                
                embed = soup.find("embed", id="pdf")
                if embed and embed.get("src"):
                    resolved = normalize_url(embed.get("src"), url)
                    if resolved: return resolved
                
                button = soup.find("button", onclick=True)
                if button:
                    onclick_text = button["onclick"]
                    match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", onclick_text)
                    if match:
                        resolved = normalize_url(match.group(1), url)
                        if resolved: return resolved
                            
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "download=true" in href or href.endswith(".pdf") or "pdf" in href.lower():
                        resolved = normalize_url(href, url)
                        if resolved: return resolved
        except Exception:
            continue
    return None

# Step 4b: Fallback DuckDuckGo Search
def search_fallback_links(title, doi=None, green_url=None, sem_scholar_url=None):
    links = []
    
    if green_url:
        links.append({
            "title": "🟢 קישור ירוק - עמוד מאמר בגישה חופשית (Unpaywall)",
            "url": green_url
        })
    if sem_scholar_url:
        links.append({
            "title": "🎓 עמוד מאמר ב-Semantic Scholar (גישה חופשית)",
            "url": sem_scholar_url
        })
        
    # Clean and optimize search query to prevent generic letters matching
    search_query = sanitize_search_query(title) if title else ""
    
    if search_query:
        # Execute fallback searches reusing a single DDGS session to avoid rate limits
        try:
            with DDGS() as ddgs:
                # 1. ResearchGate Search
                try:
                    rg_results = ddgs.text(f'site:researchgate.net "{search_query}"', max_results=3)
                    for r in rg_results:
                        url = r.get("href")
                        if is_academic_url(url):
                            links.append({
                                "title": f"👥 ResearchGate: {r.get('title', 'עמוד מאמר')}",
                                "url": url
                            })
                except Exception:
                    pass
                
                # 2. General web PDF Search
                try:
                    pdf_results = ddgs.text(f'"{search_query}" filetype:pdf', max_results=4)
                    for r in pdf_results:
                        url = r.get("href")
                        if is_academic_url(url):
                            links.append({
                                "title": f"📄 PDF מהרשת: {r.get('title', 'קישור למאמר')}",
                                "url": url
                            })
                except Exception:
                    pass
        except Exception:
            pass
        
    if doi:
        links.append({
            "title": "🔗 קישור למזהה DOI רשמי של המוציא לאור (dx.doi.org)",
            "url": f"https://dx.doi.org/{doi}"
        })
        for mirror in SCIHUB_MIRRORS:
            links.append({
                "title": f"דף המאמר ב-Sci-Hub ({mirror.split('//')[-1]})",
                "url": f"{mirror}/{doi}"
            })
            
    return links

# PDF Preview Embedder
def display_pdf_preview(pdf_bytes):
    """Embeds a scrollable PDF viewer safely with premium styling."""
    try:
        # Cap display preview to protect client browser from crashing
        if len(pdf_bytes) > 5 * 1024 * 1024:
            st.info("💡 קובץ ה-PDF גדול מ-5MB. תצוגה מקדימה הושבתה כדי לשמור על יציבות הדפדפן. ניתן להוריד את הקובץ ישירות.")
            return
            
        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'''
        <div class="pdf-preview-wrapper">
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="750px" style="border: none;"></iframe>
        </div>
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"שגיאה בהצגת תצוגה מקדימה של ה-PDF: {e}")

# ==========================================
# STREAMLIT STATE & SESSION MANAGEMENT
# ==========================================
# First enforce authentication
if not check_password():
    st.stop()

user_id = get_user_id()

if "search_results" not in st.session_state:
    st.session_state["search_results"] = None
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""
if "show_history" not in st.session_state:
    st.session_state["show_history"] = False

# ==========================================
# MAIN INTERFACE BRANDING HEADER
# ==========================================
st.write("")
col_logo_r, col_title, col_logo_l = st.columns([1, 3, 1])

with col_logo_r:
    if os.path.exists("לוגו מדור מופ.png"):
        st.image("לוגו מדור מופ.png", width=95)
    else:
        st.image("https://via.placeholder.com/150?text=MOP+Logo", width=95)

with col_title:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px;">
            <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 5px; background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 50%, #2dd4bf 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">סוכן הורדת מאמרים אקדמאיים 📑</h1>
            <p style="color: #9ca3af; font-size: 1.05rem;">מערכת חכמה לאיתור, משיכה ותצוגה מקדימה של מאמרי מחקר</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col_logo_l:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=95)
    else:
        st.image("https://via.placeholder.com/150?text=Division+Logo", width=95)

st.write("---")

# Handle text input bound to st.session_state["search_input"]
user_input = st.text_input(
    label="שם המאמר (למשל: Attention Is All You Need) או קוד DOI (למשל: 10.1145/3065386):",
    placeholder="הקלד כאן...",
    key="search_input"
)

# Column layout for search controls (extremely responsive)
col_search, col_new, col_hist = st.columns([2, 1, 1])
with col_search:
    search_button = st.button("🔎 התחל באיתור והורדה", use_container_width=True, type="primary")
with col_new:
    new_search_button = st.button("➕ חיפוש חדש", use_container_width=True, type="secondary")
with col_hist:
    history_button = st.button("🕒 היסטוריה", use_container_width=True, type="secondary")

# Handle search control triggers
if new_search_button:
    st.session_state["search_results"] = None
    st.session_state["search_input"] = ""
    st.session_state["last_query"] = ""
    st.session_state["show_history"] = False
    st.rerun()

if history_button:
    st.session_state["show_history"] = not st.session_state["show_history"]
    st.rerun()

# Render inline History Panel if toggled
if st.session_state["show_history"]:
    st.write("")
    st.markdown("### 🕒 חיפושים אחרונים")
    user_history = get_user_history(user_id)
    if user_history:
        for idx, entry in enumerate(user_history):
            status_icon = "🟢" if entry['status'] == "הצלחה" else "🟡"
            title_truncated = entry['resolved_title']
            
            st.markdown(
                f"""
                <div class="history-item">
                    <div style="font-size: 14px; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">{title_truncated}</div>
                    <div style="font-size: 12px; color: #9ca3af; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span>סטטוס: {status_icon} {entry['status']}</span>
                        <span>זמן: {entry['timestamp']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔎 טען מאמר זה מחדש", key=f"hist_btn_{entry['timestamp']}_{idx}", use_container_width=True, type="secondary"):
                st.session_state["search_input"] = entry["query"]
                st.session_state["search_results"] = None  # Reset results
                st.session_state["show_history"] = False   # Close history panel
                st.rerun()
    else:
        st.caption("אין חיפושים קודמים במכשיר זה.")
    st.write("---")

# Reset search results if the user types a new query
if user_input.strip() != st.session_state["last_query"]:
    st.session_state["search_results"] = None

# Trigger search execution
should_search = False
if search_button and user_input.strip():
    should_search = True
elif st.session_state["search_input"] and st.session_state["search_results"] is None and st.session_state["last_query"] != st.session_state["search_input"].strip():
    should_search = True

# ==========================================
# MAIN EXECUTION FLOW
# ==========================================
if should_search:
    # Clear state is handled by last_query synchronization
    
    query = user_input.strip()
    pdf_bytes = None
    pdf_link = None
    resolved_title = query
    doi = extract_doi_from_text(query)
    
    # 0. Check local server cache first!
    if doi:
        cached_pdf_content = get_cached_pdf(doi)
        if cached_pdf_content:
            pdf_bytes = cached_pdf_content
            pdf_link = "LOCAL_CACHE"
            resolved_title = f"קובץ שמור מהשרת (DOI: {doi})"
            
    # If not found in cache, run full pipeline
    if pdf_bytes is None:
        with st.status("🤖 מתחיל בתהליך האיתור...", expanded=True) as status:
            
            # --- Step 1: Input Analysis & DOI Resolution ---
            status.write("🔍 מנתח את קלט המשתמש...")
            
            if doi:
                status.write(f"✅ זוהה קוד DOI ישיר: `{doi}`")
                status.write("🔍 מאתר את כותרת המאמר לטובת חיפושי גיבוי...")
                title_fetched = fetch_paper_title(doi)
                if title_fetched:
                    resolved_title = title_fetched
                    status.write(f"📚 שם המאמר הרשמי: *{resolved_title}*")
                else:
                    status.write("⚠️ לא הצלחנו לאחזר את כותרת המאמר מרשתות המידע. נשתמש ב-DOI כזיהוי.")
            else:
                status.write("🌐 הקלט זוהה כשם מאמר. מבצע חיפוש ב-Crossref לקבלת DOI...")
                doi, resolved_title = resolve_title_to_doi(query)
                if doi:
                    status.write(f"✅ נמצא מזהה DOI תואם ב-Crossref: `{doi}`")
                    status.write(f"📚 שם המאמר הרשמי: *{resolved_title}*")
                else:
                    status.write("⚠️ לא נמצא DOI ב-Crossref. מנסה לאתר ב-Semantic Scholar...")
                    doi, resolved_title = resolve_title_to_doi_semantic_scholar(query)
                    if doi:
                        status.write(f"✅ נמצא מזהה DOI תואם ב-Semantic Scholar: `{doi}`")
                        status.write(f"📚 שם המאמר הרשמי: *{resolved_title}*")
                    else:
                        status.write("⚠️ לא נמצא DOI גם ב-Semantic Scholar. נמשיך לחיפוש חופשי בלבד.")
            
            # Check cache again if DOI resolved just now
            if doi and not pdf_bytes:
                cached_pdf_content = get_cached_pdf(doi)
                if cached_pdf_content:
                    pdf_bytes = cached_pdf_content
                    pdf_link = "LOCAL_CACHE"
                    status.write("📦 המאמר נמצא בזיכרון המטמון המקומי של השרת!")
            
            # --- Step 2: The "Green" Route (Unpaywall & Semantic Scholar) ---
            green_landing_url = None
            sem_scholar_url = None
            
            if doi and not pdf_bytes:
                status.write("🟢 בודק זמינות בגישה חופשית ב-Unpaywall...")
                pdf_link, green_landing_url = get_unpaywall_data(doi)
                
                if pdf_link:
                    status.write("🔗 נמצא קישור פתוח ב-Unpaywall. מאמת את הקישור...")
                    if check_link_is_pdf(pdf_link):
                        status.write("🎯 הקישור מ-Unpaywall אומת בהצלחה!")
                    else:
                        status.write("⚠️ הקישור מ-Unpaywall נכשל באימות. נמשיך לבדיקת Semantic Scholar.")
                        pdf_link = None
                
                # If Unpaywall didn't yield a direct PDF, check Semantic Scholar
                status.write("🟢 בודק זמינות בגישה חופשית ב-Semantic Scholar...")
                sem_pdf, sem_scholar_url = get_semantic_scholar_data(doi)
                if not pdf_link and sem_pdf:
                    status.write("🔗 נמצא קישור פתוח ב-Semantic Scholar. מאמת את הקישור...")
                    if check_link_is_pdf(sem_pdf):
                        pdf_link = sem_pdf
                        status.write("🎯 הקישור מ-Semantic Scholar אומת בהצלחה!")
                    else:
                        status.write("⚠️ הקישור מ-Semantic Scholar נכשל באימות.")
            
            # --- Step 3: The "Grey" Route (Sci-Hub) ---
            if doi and not pdf_link and not pdf_bytes:
                status.write("🔘 מחפש בשרתי Sci-Hub (רוטציית שרתים)...")
                pdf_link = get_scihub_pdf(doi)
                
                if pdf_link:
                    status.write("🔗 נמצא קישור פוטנציאלי ב-Sci-Hub. מאמת את הקישור...")
                    if check_link_is_pdf(pdf_link):
                        status.write("🎯 הקישור מ-Sci-Hub אומת בהצלחה!")
                    else:
                        status.write("⚠️ הקישור מ-Sci-Hub נכשל באימות. נמשיך לחיפוש כללי.")
                        pdf_link = None
            
            # Download bytes if we found a URL (with size checking to prevent OOM)
            if pdf_link and pdf_link != "LOCAL_CACHE" and not pdf_bytes:
                status.write("⬇️ מוריד קובץ PDF לזיכרון השרת...")
                try:
                    with requests.get(pdf_link, headers=HEADERS, timeout=15, stream=True) as pdf_res:
                        if pdf_res.status_code == 200:
                            content_length = pdf_res.headers.get("Content-Length")
                            if content_length and int(content_length) > 25 * 1024 * 1024:
                                status.write("⚠️ קובץ ה-PDF גדול מ-25MB. הורדה ישירה הושבתה.")
                            else:
                                temp_bytes_list = []
                                downloaded = 0
                                for chunk in pdf_res.iter_content(chunk_size=8192):
                                    downloaded += len(chunk)
                                    if downloaded > 25 * 1024 * 1024:
                                        raise ValueError("הקובץ חורג ממגבלת הנפח המותרת של 25MB.")
                                    temp_bytes_list.append(chunk)
                                
                                temp_bytes = b"".join(temp_bytes_list)
                                # Verify the download is actually a PDF
                                if temp_bytes.startswith(b"%PDF") or b"%PDF" in temp_bytes[:1024]:
                                    pdf_bytes = temp_bytes
                                    save_pdf_to_cache(doi, pdf_bytes) # Cache it for next searches
                                    status.write("💾 הקובץ נשמר בזיכרון המטמון של השרת לנוחות עתידית.")
                                else:
                                    status.write("⚠️ הקובץ שהורד מהקישור המאומת אינו קובץ PDF תקין (ייתכן דף שגיאה או חומת תשלום).")
                except Exception as e:
                    status.write(f"⚠️ הורדת קובץ ה-PDF נכשלה: {e}")
            
            # --- Step 4: Fallback Search (DuckDuckGo & ResearchGate) ---
            fallback_results = []
            if not pdf_bytes:
                status.write("🌐 הורדה ישירה נכשלה. מבצע חיפוש חלופי ברשת...")
                fallback_results = search_fallback_links(resolved_title, doi, green_landing_url, sem_scholar_url)
                
            # Complete the status spinner
            if pdf_bytes:
                status.update(label="🚀 המאמר נמצא והורד בהצלחה!", state="complete")
            else:
                status.update(label="⚠️ לא נמצא קובץ PDF ישיר להורדה.", state="error")

    # Store search results in Session State for persistence across reruns
    st.session_state["search_results"] = {
        "pdf_bytes": pdf_bytes,
        "pdf_link": pdf_link,
        "resolved_title": resolved_title,
        "doi": doi,
        "fallback_results": fallback_results
    }
    st.session_state["last_query"] = query

    # ==========================================
    # LOGGING RESULT
    # ==========================================
    log_status = "הצלחה" if pdf_bytes else "חיפוש חלופי"
    log_link = pdf_link if pdf_bytes else (fallback_results[0]["url"] if fallback_results else "לא נמצא")
    log_search(
        user_id=user_id,
        query=query,
        resolved_title=resolved_title,
        doi=doi,
        status=log_status,
        link_found=log_link,
        gas_url=DEFAULT_GAS_URL
    )

# ==========================================
# DISPLAY FINAL RESULTS & PDF PREVIEW (FROM SESSION STATE)
# ==========================================
if st.session_state["search_results"] is not None:
    res = st.session_state["search_results"]
    pdf_bytes = res["pdf_bytes"]
    pdf_link = res["pdf_link"]
    resolved_title = res["resolved_title"]
    doi = res["doi"]
    fallback_results = res["fallback_results"]
    
    st.write("") 
    
    if pdf_bytes:
        # Elegant Success Alert Card
        st.markdown(
            f"""
            <div class="success-alert">
                <span style="font-size: 16px; font-weight: 600; color: #34d399;">🎉 המאמר נמצא והורד בהצלחה!</span><br/>
                <span style="font-size: 14px; color: #e5e7eb;"><b>כותרת:</b> {resolved_title}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col_actions, col_info = st.columns([1, 1])
        with col_actions:
            filename = f"{doi.replace('/', '_') if doi else 'paper'}.pdf"
            st.download_button(
                label="⬇️ שמירת קובץ PDF במחשב",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        with col_info:
            if pdf_link != "LOCAL_CACHE":
                st.link_button("🔗 פתיחת מקור ישיר בדפדפן", pdf_link, use_container_width=True, type="secondary")
            else:
                st.info("💡 נטען ישירות משרת המטמון המקומי.")
                
        # Premium: Inline PDF Preview
        st.write("---")
        st.markdown("### 📖 תצוגה מקדימה של המאמר:")
        display_pdf_preview(pdf_bytes)
            
    elif fallback_results:
        # Elegant Warning Alert Card
        st.markdown(
            f"""
            <div class="warning-alert">
                <span style="font-size: 16px; font-weight: 600; color: #f59e0b;">⚠️ לא הצלחנו להוריד את המאמר ישירות</span><br/>
                <span style="font-size: 14px; color: #e5e7eb;">אך מצאנו מספר קישורים בעלי סבירות גבוהה לאיתור הקובץ:</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        for idx, item in enumerate(fallback_results, 1):
            st.markdown(f"**{idx}. [{item['title']}]({item['url']})**")
            st.caption(f"קישור: {item['url']}")
            
    else:
        st.error("❌ מצטערים, לא הצלחנו למצוא קישורים זמינים למאמר זה במערכת.")
        st.markdown(
            """
            <div style="direction: rtl; text-align: right; background-color: rgba(255, 75, 75, 0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(255, 75, 75, 0.2);">
                <p style="font-weight: bold; margin-bottom: 8px;">💡 טיפים לשיפור החיפוש:</p>
                <ul style="margin-right: 20px;">
                    <li><b>חיפוש לפי מזהה DOI</b>: אם קיים מזהה ייחודי למאמר (מתחיל ב-10.), עדיף להזין אותו. זה יבטיח 100% דיוק במציאת המאמר.</li>
                    <li><b>הזן את כותרת המאמר בלבד</b>: אם העתקת ציטוט שלם הכולל מחברים, שנה ושם כתב-עת, מחק אותם והשאר רק את כותרת המאמר (למשל: <i>Attention Is All You Need</i>).</li>
                    <li><b>בדוק שגיאות הקלדה</b>: ודא שאין שגיאות כתיב בשם המאמר, ושהשם מוזן באנגלית.</li>
                    <li><b>נסה להשמיט מילים פחות קריטיות</b>: אם שם המאמר ארוך מאוד, נסה להזין רק את החלק העיקרי של הכותרת.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
