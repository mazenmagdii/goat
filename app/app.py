# ============================================================================
# STREAMLIT FRONTEND - AI ASSISTANT (PREMIUM PROFESSIONAL DESIGN)
# ============================================================================

import streamlit as st
import requests
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ['youtu.be']:
        return parsed.path[1:]
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
        if parsed.path.startswith(('/embed/', '/v/')):
            return parsed.path.split('/')[2]
    raise ValueError(f"Could not extract video ID from URL: {url}")

def get_transcript(video_id: str) -> str:
    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id)
        text = "\n".join(snippet.text for snippet in fetched)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# CONFIGURATION
# ============================================================================
API_URL = "your_ngrok_url_here"  # IMPORTANT: Update this with your ngrok URL
API_KEY = "secret1234"

TIMEOUT_SHORT = 60
TIMEOUT_MEDIUM = 300
TIMEOUT_LONG = 900

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="GOAT AI Assistant",
    page_icon="🐐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM PROFESSIONAL CSS - INSPIRED BY CLAUDE/CHATGPT
# ============================================================================
st.markdown("""
<style>
/* ===============================
   GLOBAL STYLES
================================ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.main {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: #e8e8e8;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* ===============================
   HEADERS - CLEAN & PROFESSIONAL
================================ */
h1, h2, h3, h4, h5, h6 {
    color: #f0f0f0 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.75rem !important;
    margin-top: 2rem !important;
}

h3 {
    font-size: 1.25rem !important;
    font-weight: 500 !important;
    color: #d0d0d0 !important;
}

/* ===============================
   PROFESSIONAL BUTTONS
================================ */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    cursor: pointer !important;
    text-transform: none !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
}

/* Secondary Button Style */
.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* ===============================
   FORM SUBMIT BUTTON (SEND ARROW)
================================ */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.25rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    min-width: 80px !important;
}

.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    transform: translateY(-1px) !important;
}

.stFormSubmitButton > button::after {
    content: '→' !important;
    margin-left: 0.5rem !important;
    font-size: 1.1rem !important;
}

/* ===============================
   INPUT FIELDS - MODERN & CLEAN
================================ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background-color: rgba(255, 255, 255, 0.03) !important;
    color: #e8e8e8 !important;
    border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(255, 255, 255, 0.4) !important;
}

/* ===============================
   FILE UPLOADER - PROFESSIONAL
================================ */
.stFileUploader {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 2px dashed rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    transition: all 0.3s ease !important;
}

.stFileUploader:hover {
    border-color: rgba(37, 99, 235, 0.5) !important;
    background-color: rgba(37, 99, 235, 0.02) !important;
}

/* ===============================
   RESPONSE BOXES - CLAUDE-STYLE
================================ */
.response-box {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 1.75rem;
    margin: 1.5rem 0;
    white-space: pre-wrap;
    line-height: 1.7;
    color: #e8e8e8;
    font-size: 0.95rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

/* ===============================
   SUMMARY BOX - PREMIUM STYLE
================================ */
.summary-box {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(29, 78, 216, 0.05) 100%);
    border: 2px solid rgba(37, 99, 235, 0.3);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    white-space: pre-wrap;
    line-height: 1.8;
    color: #f0f0f0;
    font-size: 1rem;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
    position: relative;
    overflow: hidden;
}

.summary-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
}

/* ===============================
   CHAT INTERFACE - CHATGPT-STYLE
================================ */
.chat-container {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    max-height: 550px;
    overflow-y: auto;
    backdrop-filter: blur(10px);
}

/* Custom Scrollbar */
.chat-container::-webkit-scrollbar {
    width: 8px;
}

.chat-container::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.15);
}

/* ===============================
   CHAT MESSAGES - POLISHED
================================ */
.user-message {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: #ffffff;
    padding: 1rem 1.25rem;
    border-radius: 18px 18px 4px 18px;
    margin: 1rem 0;
    max-width: 75%;
    margin-left: auto;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    font-size: 0.95rem;
    line-height: 1.6;
}

.assistant-message {
    background: rgba(255, 255, 255, 0.04);
    color: #e8e8e8;
    padding: 1rem 1.25rem;
    border-radius: 18px 18px 18px 4px;
    margin: 1rem 0;
    max-width: 75%;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    font-size: 0.95rem;
    line-height: 1.6;
}

.message-label {
    font-weight: 600;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.message-content {
    margin: 0.5rem 0;
}

.message-timestamp {
    font-size: 0.75rem;
    opacity: 0.6;
    margin-top: 0.75rem;
    font-weight: 400;
}

/* ===============================
   METADATA - SUBTLE & ELEGANT
================================ */
.timestamp {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.85rem;
    text-align: right;
    font-weight: 400;
}

.generation-time {
    color: #2563eb;
    font-weight: 600;
}

/* ===============================
   TABS - MODERN DESIGN
================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background-color: rgba(255, 255, 255, 0.02);
    border-radius: 12px;
    padding: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: rgba(255, 255, 255, 0.6);
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    border: none;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.8);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(29, 78, 216, 0.1) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(37, 99, 235, 0.3) !important;
}

/* ===============================
   SIDEBAR - SLEEK & MINIMAL
================================ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* ===============================
   SLIDER - MODERN STYLE
================================ */
.stSlider > div > div > div {
    background-color: rgba(37, 99, 235, 0.3) !important;
}

.stSlider > div > div > div > div {
    background-color: #2563eb !important;
}

/* ===============================
   SELECTBOX - CLEAN
================================ */
.stSelectbox > div > div {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 10px !important;
}

/* ===============================
   DOWNLOAD BUTTON
================================ */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
    transform: translateY(-1px) !important;
}

/* ===============================
   SUCCESS/ERROR MESSAGES
================================ */
.stSuccess {
    background-color: rgba(5, 150, 105, 0.1) !important;
    border: 1px solid rgba(5, 150, 105, 0.3) !important;
    border-radius: 10px !important;
    color: #10b981 !important;
}

.stError {
    background-color: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 10px !important;
    color: #ef4444 !important;
}

.stWarning {
    background-color: rgba(245, 158, 11, 0.1) !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 10px !important;
    color: #f59e0b !important;
}

/* ===============================
   DIVIDER
================================ */
hr {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin: 2rem 0;
}

/* ===============================
   STEP INDICATORS
================================ */
.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding: 1rem;
    background: rgba(37, 99, 235, 0.05);
    border-left: 4px solid #2563eb;
    border-radius: 8px;
}

.step-number {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.9rem;
}

.step-title {
    font-weight: 600;
    font-size: 1rem;
    color: #e8e8e8;
}

/* ===============================
   UTILITY CLASSES
================================ */
.text-muted {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.9rem;
}

.card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

/* ===============================
   ANIMATIONS
================================ */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animated-enter {
    animation: fadeIn 0.3s ease-out;
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def make_api_request(endpoint, data=None, files=None, method="POST", timeout=TIMEOUT_MEDIUM):
    """Make authenticated API request"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        url = f"{API_URL}{endpoint}"
        
        if method == "POST":
            if files:
                response = requests.post(url, data=data, files=files, headers=headers, timeout=timeout)
            else:
                response = requests.post(url, data=data, headers=headers, timeout=timeout)
        else:
            response = requests.get(url, headers=headers, timeout=timeout)
        
        return response.json()
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": f"Request timed out after {timeout} seconds."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Check if Kaggle notebook is running."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_api_status():
    """Check if backend is online"""
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        return response.status_code == 200, response.json()
    except:
        return False, {"error": "Backend offline"}

def format_timestamp(iso_timestamp):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime("%I:%M:%S %p")
    except:
        return "N/A"

def display_response_with_metadata(content, result):
    """Display response with timestamp and generation time"""
    st.markdown(f'<div class="response-box animated-enter">{content}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if result.get("timestamp"):
            timestamp_str = format_timestamp(result["timestamp"])
            st.markdown(f'<div class="timestamp">⏰ {timestamp_str}</div>', unsafe_allow_html=True)
    with col2:
        if result.get("generation_time"):
            st.markdown(f'<div class="timestamp generation-time">⚡ {result["generation_time"]}</div>', unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Initialize session states
    if "youtube_processed" not in st.session_state:
        st.session_state.youtube_processed = False
    if "youtube_messages" not in st.session_state:
        st.session_state.youtube_messages = []
    if "youtube_transcript" not in st.session_state:
        st.session_state.youtube_transcript = None
    if "youtube_summary" not in st.session_state:
        st.session_state.youtube_summary = None
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []
    if "general_messages" not in st.session_state:
        st.session_state.general_messages = []
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0 2rem 0;'>
            <div style='font-size: 4rem; margin-bottom: 0.5rem;'>🐐</div>
            <div style='font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em;'>GOAT</div>
            <div style='font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-top: 0.25rem;'>Greatest Of All Time</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 🔌 Connection Status")
        if API_URL != "YOUR_NGROK_URL_HERE":
            if st.button("🔍 Check Connection", use_container_width=True):
                with st.spinner("Checking..."):
                    is_online, response = check_api_status()
                    if is_online:
                        st.success("✅ Backend Online")
                        with st.expander("View Details"):
                            st.json(response)
                    else:
                        st.error("❌ Backend Offline")
        else:
            st.error("⚠️ Configure API_URL")
        
        st.markdown("---")
        
        st.markdown("""
        <div class='card'>
            <h4 style='margin-top: 0; font-size: 1rem;'>✨ Features</h4>
            <ul style='font-size: 0.9rem; line-height: 2; padding-left: 1.25rem;'>
                <li>📚 Study Plans</li>
                <li>🎥 YouTube Analysis</li>
                <li>📄 PDF Q&A</li>
                <li>💬 General Chat</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='card'>
            <h4 style='margin-top: 0; font-size: 1rem;'>🔧 Model Info</h4>
            <div style='font-size: 0.9rem; line-height: 1.8;'>
                <strong>Llama 3.1 8B Instruct</strong><br>
                <span class='text-muted'>• 4-bit Quantization<br>
                • Conversation Memory<br>
                • LangChain Powered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; margin-bottom: 2rem;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            GOAT AI Assistant
        </h1>
        <p style='font-size: 1.15rem; color: rgba(255,255,255,0.6); font-weight: 400;'>
            Powered by Llama 3.1 • Your Intelligent Companion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Selection Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Study Planner", "🎥 YouTube Assistant", "📄 PDF Q&A", "💬 General Chat"])
    
    # ========================================================================
    # FEATURE 1: Study Planner
    # ========================================================================
    with tab1:
        st.markdown("## 📚 Study Plan Generator")
        st.markdown('<p class="text-muted">Create personalized learning plans powered by AI</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            subject = st.text_input(
                "📖 Subject or Topic",
                placeholder="e.g., Python Programming, Machine Learning, Data Science",
                key="study_subject",
                help="What do you want to learn?"
            )
            
            goal = st.text_area(
                "🎯 Learning Goal",
                placeholder="e.g., Build production-ready web applications, Pass AWS certification, Master deep learning",
                height=120,
                key="study_goal",
                help="What do you want to achieve?"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                level = st.selectbox(
                    "📊 Current Level",
                    ["Beginner", "Intermediate", "Advanced"],
                    key="study_level"
                )
                time_available = st.slider(
                    "⏰ Hours per Week",
                    min_value=1,
                    max_value=40,
                    value=10,
                    key="study_time"
                )
            
            with col_b:
                timeline = st.selectbox(
                    "📅 Timeline",
                    ["1 month", "3 months", "6 months", "1 year"],
                    index=1,
                    key="study_timeline"
                )
                generation_type = st.radio(
                    "📋 What to Generate",
                    ["Study Plan", "Roadmap", "Resources", "All Three"],
                    key="study_type"
                )
        
        with col2:
            st.markdown("""
            <div class='card'>
                <h4 style='margin-top: 0; font-size: 1rem; color: #2563eb;'>⚡ Summary</h4>
            """, unsafe_allow_html=True)
            
            if subject:
                st.markdown(f"**📖 Subject**  \n{subject}")
            if goal:
                goal_preview = goal[:80] + "..." if len(goal) > 80 else goal
                st.markdown(f"**🎯 Goal**  \n{goal_preview}")
            st.markdown(f"**📊 Level**  \n{level}")
            st.markdown(f"**⏰ Time**  \n{time_available} hours/week")
            st.markdown(f"**📅 Timeline**  \n{timeline}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
        with col_btn1:
            generate_clicked = st.button("🚀 Generate Plan", key="generate_study", use_container_width=True)
        
        if generate_clicked:
            if not subject or not goal:
                st.error("⚠️ Please fill in both Subject and Goal fields")
            elif API_URL == "YOUR_NGROK_URL_HERE":
                st.error("⚠️ Please configure API_URL in the code")
            else:
                with st.spinner("🐐 GOAT is generating your personalized plan..."):
                    data = {
                        "subject": subject,
                        "level": level,
                        "time_available": str(time_available),
                        "goal": goal,
                        "timeline": timeline
                    }
                    
                    results = {}
                    
                    if generation_type in ["Study Plan", "All Three"]:
                        result = make_api_request("/study-plan/generate", data, timeout=TIMEOUT_LONG)
                        if result.get("success"):
                            results["study_plan"] = result
                    
                    if generation_type in ["Roadmap", "All Three"]:
                        result = make_api_request("/study-plan/roadmap", data, timeout=TIMEOUT_MEDIUM)
                        if result.get("success"):
                            results["roadmap"] = result
                    
                    if generation_type in ["Resources", "All Three"]:
                        result = make_api_request("/study-plan/resources", data, timeout=TIMEOUT_MEDIUM)
                        if result.get("success"):
                            results["resources"] = result
                    
                    if results:
                        st.success("✅ Plan generated successfully!")
                        
                        if "study_plan" in results:
                            st.markdown("### 📋 Your Personalized Study Plan")
                            display_response_with_metadata(results["study_plan"]["study_plan"], results["study_plan"])
                            st.download_button(
                                "📥 Download Study Plan",
                                results["study_plan"]["study_plan"],
                                f"study_plan_{subject.replace(' ', '_')}.txt",
                                key="dl_plan",
                                use_container_width=True
                            )
                        
                        if "roadmap" in results:
                            st.markdown("### 🗺️ Learning Roadmap")
                            display_response_with_metadata(results["roadmap"]["roadmap"], results["roadmap"])
                            st.download_button(
                                "📥 Download Roadmap",
                                results["roadmap"]["roadmap"],
                                f"roadmap_{subject.replace(' ', '_')}.txt",
                                key="dl_roadmap",
                                use_container_width=True
                            )
                        
                        if "resources" in results:
                            st.markdown("### 📚 Recommended Resources")
                            display_response_with_metadata(results["resources"]["resources"], results["resources"])
                            st.download_button(
                                "📥 Download Resources",
                                results["resources"]["resources"],
                                f"resources_{subject.replace(' ', '_')}.txt",
                                key="dl_resources",
                                use_container_width=True
                            )
                    else:
                        st.error("❌ Generation failed. Please check your backend connection.")
    
    # ========================================================================
    # FEATURE 2: YouTube Assistant
    # ========================================================================
    with tab2:
        st.markdown("## 🎥 YouTube Video Assistant")
        st.markdown('<p class="text-muted">Analyze and chat with any YouTube video</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Step 1: Process Video
        st.markdown('<div class="step-header"><div class="step-number">1</div><div class="step-title">Process Video</div></div>', unsafe_allow_html=True)
        
        youtube_url = st.text_input(
            "🔗 YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="youtube_url",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("📝 Process Video", key="process_youtube", use_container_width=True):
                if not youtube_url:
                    st.error("⚠️ Please enter a YouTube URL")
                else:
                    with st.spinner("🎬 Processing video transcript..."):
                        try:
                            video_id = extract_video_id(youtube_url)
                            transcript = get_transcript(video_id)

                            if transcript.startswith("Error"):
                                st.error(f"❌ {transcript}")
                            else:
                                result = make_api_request(
                                    "/youtube/process", 
                                    {"url": youtube_url, "transcript": transcript},
                                    timeout=TIMEOUT_MEDIUM
                                )
                                
                                if result.get("success"):
                                    st.session_state.youtube_processed = True
                                    st.session_state.youtube_messages = []
                                    st.session_state.youtube_transcript = transcript
                                    st.session_state.youtube_summary = None

                                    word_count = len(transcript.split())
                                    st.success(f"✅ Video processed successfully ({word_count:,} words)")
                                else:
                                    st.error(f"❌ {result.get('error')}")

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with col3:
            if st.button("🗑️ Clear All", key="clear_yt", use_container_width=True):
                make_api_request("/youtube/clear-history", {}, timeout=TIMEOUT_SHORT)
                st.session_state.youtube_messages = []
                st.session_state.youtube_processed = False
                st.session_state.youtube_transcript = None
                st.session_state.youtube_summary = None
                st.success("✅ Cleared successfully")
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Step 2: Summarization
        st.markdown('<div class="step-header"><div class="step-number">2</div><div class="step-title">Generate Summary</div></div>', unsafe_allow_html=True)
        
        if st.button("📊 Summarize Video", key="summarize_youtube", use_container_width=True):
            if not st.session_state.youtube_processed:
                st.warning("⚠️ Please process a video first")
            else:
                with st.spinner("🐐 Generating comprehensive summary... This may take a few minutes"):
                    result = make_api_request("/youtube/summarize", {}, timeout=TIMEOUT_LONG)
                    if result.get("success"):
                        st.session_state.youtube_summary = result
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('error')}")
        
        if st.session_state.youtube_summary:
            st.markdown("#### 📄 Video Summary")
            st.markdown(f'<div class="summary-box animated-enter">{st.session_state.youtube_summary["summary"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.youtube_summary.get("timestamp"):
                    timestamp_str = format_timestamp(st.session_state.youtube_summary["timestamp"])
                    st.markdown(f'<div class="timestamp">⏰ Generated at {timestamp_str}</div>', unsafe_allow_html=True)
            with col2:
                if st.session_state.youtube_summary.get("generation_time"):
                    st.markdown(f'<div class="timestamp generation-time">⚡ Completed in {st.session_state.youtube_summary["generation_time"]}</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 Download Summary",
                st.session_state.youtube_summary["summary"],
                "video_summary.txt",
                key="dl_summary",
                use_container_width=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Step 3: Chat
        st.markdown('<div class="step-header"><div class="step-number">3</div><div class="step-title">Chat with Video</div></div>', unsafe_allow_html=True)
        
        if st.session_state.youtube_messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.youtube_messages:
                if msg["role"] == "user":
                    st.markdown(f'''<div class="user-message animated-enter">
                        <div class="message-label">You</div>
                        <div class="message-content">{msg["content"]}</div>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div class="assistant-message animated-enter">
                        <div class="message-label">🐐 GOAT</div>
                        <div class="message-content">{msg["content"]}</div>
                        <div class="message-timestamp">Generated at {msg.get("timestamp", "N/A")} • {msg.get("time", "N/A")}</div>
                    </div>''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.form(key="youtube_chat_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                question = st.text_input(
                    "Message",
                    key="yt_input",
                    label_visibility="collapsed",
                    placeholder="Ask anything about this video..."
                )
            with cols[1]:
                submit = st.form_submit_button("Send", use_container_width=True)
            
            if submit and question:
                if not st.session_state.youtube_processed:
                    st.warning("⚠️ Please process a video first")
                else:
                    st.session_state.youtube_messages.append({"role": "user", "content": question})
                    
                    with st.spinner("Thinking..."):
                        result = make_api_request("/youtube/chat", {"question": question}, timeout=TIMEOUT_MEDIUM)
                        if result.get("success"):
                            st.session_state.youtube_messages.append({
                                "role": "assistant",
                                "content": result["answer"],
                                "timestamp": format_timestamp(result.get("timestamp", "")),
                                "time": result.get("generation_time", "N/A")
                            })
                        else:
                            st.error(f"❌ {result.get('error')}")
                    
                    st.rerun()
    
    # ========================================================================
    # FEATURE 3: PDF Q&A
    # ========================================================================
    with tab3:
        st.markdown("## 📄 PDF Question & Answer")
        st.markdown('<p class="text-muted">Upload documents and ask intelligent questions</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "📎 Upload PDF Document",
                type=["pdf"],
                key="pdf_upload",
                help="Upload a PDF file to analyze"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear History", key="clear_pdf", use_container_width=True):
                make_api_request("/pdf/clear-history", {}, timeout=TIMEOUT_SHORT)
                st.session_state.pdf_messages = []
                st.success("✅ History cleared")
                st.rerun()
        
        if uploaded_file:
            if st.button("📤 Process PDF", key="process_pdf", use_container_width=True):
                with st.spinner("📖 Processing PDF document..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    result = make_api_request("/pdf/upload", files=files, timeout=TIMEOUT_LONG)
                    if result.get("success"):
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_messages = []
                        st.success(f"✅ PDF processed successfully ({result.get('text_length'):,} words)")
                    else:
                        st.error(f"❌ {result.get('error')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💬 Ask Questions About Your Document")
        
        if st.session_state.pdf_messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.pdf_messages:
                if msg["role"] == "user":
                    st.markdown(f'''<div class="user-message animated-enter">
                        <div class="message-label">You</div>
                        <div class="message-content">{msg["content"]}</div>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div class="assistant-message animated-enter">
                        <div class="message-label">🐐 GOAT</div>
                        <div class="message-content">{msg["content"]}</div>
                        <div class="message-timestamp">Generated at {msg.get("timestamp", "N/A")} • {msg.get("time", "N/A")}</div>
                    </div>''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.form(key="pdf_chat_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                question = st.text_input(
                    "Message",
                    key="pdf_input",
                    label_visibility="collapsed",
                    placeholder="Ask questions about your PDF..."
                )
            with cols[1]:
                submit = st.form_submit_button("Send", use_container_width=True)
            
            if submit and question:
                if not st.session_state.pdf_processed:
                    st.warning("⚠️ Please upload and process a PDF first")
                else:
                    st.session_state.pdf_messages.append({"role": "user", "content": question})
                    
                    with st.spinner("Analyzing..."):
                        result = make_api_request("/pdf/ask", {"question": question}, timeout=TIMEOUT_MEDIUM)
                        if result.get("success"):
                            st.session_state.pdf_messages.append({
                                "role": "assistant",
                                "content": result["answer"],
                                "timestamp": format_timestamp(result.get("timestamp", "")),
                                "time": result.get("generation_time", "N/A")
                            })
                        else:
                            st.error(f"❌ {result.get('error')}")
                    
                    st.rerun()
    
    # ========================================================================
    # FEATURE 4: General Chat
    # ========================================================================
    with tab4:
        st.markdown("## 💬 General AI Chat")
        st.markdown('<p class="text-muted">Have a conversation with GOAT about anything</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Conversation", key="clear_general", use_container_width=True):
            make_api_request("/chat/clear-history", {}, timeout=TIMEOUT_SHORT)
            st.session_state.general_messages = []
            st.success("✅ Conversation cleared")
            st.rerun()
        
        if st.session_state.general_messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.general_messages:
                if msg["role"] == "user":
                    st.markdown(f'''<div class="user-message animated-enter">
                        <div class="message-label">You</div>
                        <div class="message-content">{msg["content"]}</div>
                    </div>''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''<div class="assistant-message animated-enter">
                        <div class="message-label">🐐 GOAT</div>
                        <div class="message-content">{msg["content"]}</div>
                        <div class="message-timestamp">Generated at {msg.get("timestamp", "N/A")} • {msg.get("time", "N/A")}</div>
                    </div>''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.form(key="general_chat_form", clear_on_submit=True):
            cols = st.columns([5, 1])
            with cols[0]:
                message = st.text_input(
                    "Message",
                    key="general_input",
                    label_visibility="collapsed",
                    placeholder="Message GOAT..."
                )
            with cols[1]:
                submit = st.form_submit_button("Send", use_container_width=True)
            
            if submit and message:
                st.session_state.general_messages.append({"role": "user", "content": message})
                
                with st.spinner("Thinking..."):
                    result = make_api_request("/chat", {"message": message}, timeout=TIMEOUT_MEDIUM)
                    if result.get("success"):
                        st.session_state.general_messages.append({
                            "role": "assistant",
                            "content": result["response"],
                            "timestamp": format_timestamp(result.get("timestamp", "")),
                            "time": result.get("generation_time", "N/A")
                        })
                    else:
                        st.error(f"❌ {result.get('error')}")
                
                st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <div style='font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🐐 GOAT AI Assistant
        </div>
        <div style='color: rgba(255,255,255,0.5); font-size: 0.9rem;'>
            Powered by Llama 3.1 8B • LangChain Framework • Running on Kaggle GPU
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()