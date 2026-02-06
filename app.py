import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import json
from pathlib import Path

# --- CONFIGURATION ---
st.set_page_config(
    page_title="ATIK SZ - Bangladesh Voter Info",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #006a4e 0%, #f42a41 100%);
    }
    
    .main {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #006a4e 0%, #f42a41 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #006a4e;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #f42a41;
        box-shadow: 0 0 0 3px rgba(0, 106, 78, 0.1);
    }
    
    h1 {
        background: linear-gradient(135deg, #006a4e 0%, #f42a41 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #006a4e 0%, #f42a41 100%);
        color: white;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #006a4e 0%, #f42a41 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        margin: 1rem 0;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px dashed #006a4e;
    }
</style>
""", unsafe_allow_html=True)

# --- API CONFIGURATION ---
# --- API CONFIGURATION ---
# Robust API Key Loading (Works locally and on Streamlit Cloud)
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = os.getenv("GEMINI_API_KEY")
        
    if not API_KEY:
        st.error("⚠️ Gemini API Key not found! Please set 'GEMINI_API_KEY' in .streamlit/secrets.toml or Streamlit Cloud Secrets.")
        st.stop()
        
    genai.configure(api_key=API_KEY)
except FileNotFoundError:
    # Fallback if secrets file doesn't exist (e.g. initial local run without setup)
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
         st.warning("⚠️ Tips: To use the AI features, you need to configure your API key.")
         API_KEY = st.text_input("Enter your Gemini API Key manually:", type="password")
         if not API_KEY:
             st.stop()
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# --- DATA MANAGEMENT ---
KNOWLEDGE_BASE_PATH = Path("knowledge_base")
KNOWLEDGE_BASE_PATH.mkdir(exist_ok=True)

def load_knowledge_base():
    """Load all knowledge files from the knowledge base directory"""
    knowledge_content = ""
    files = list(KNOWLEDGE_BASE_PATH.glob("*.txt"))
    
    if not files:
        # Create default knowledge file if none exist
        default_file = KNOWLEDGE_BASE_PATH / "my_knowledge.txt"
        default_content = """# Sample Knowledge Base

## About This Bot
This is an AI-powered knowledge assistant that can answer questions based on your custom knowledge base.

## Features
- Custom knowledge base management
- File upload capability
- Chat history export
- Modern, beautiful UI
- Powered by Google Gemini AI

## How to Use
1. Upload your knowledge files using the sidebar
2. Ask questions in the chat
3. The AI will answer based on your uploaded knowledge
4. Export chat history when needed
"""
        default_file.write_text(default_content, encoding="utf-8")
        files = [default_file]
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
            knowledge_content += f"\n\n--- Source: {file_path.name} ---\n{content}"
        except Exception as e:
            st.sidebar.error(f"Error loading {file_path.name}: {e}")
    
    return knowledge_content, [f.name for f in files]

def save_uploaded_file(uploaded_file):
    """Save uploaded file to knowledge base"""
    try:
        file_path = KNOWLEDGE_BASE_PATH / uploaded_file.name
        file_path.write_bytes(uploaded_file.getvalue())
        return True
    except Exception as e:
        st.sidebar.error(f"Error saving file: {e}")
        return False

def delete_knowledge_file(filename):
    """Delete a file from knowledge base"""
    try:
        file_path = KNOWLEDGE_BASE_PATH / filename
        file_path.unlink()
        return True
    except Exception as e:
        st.sidebar.error(f"Error deleting file: {e}")
        return False

# --- AI AGENT SETUP ---
@st.cache_resource
def get_model(knowledge_content):
    """Initialize and cache the Gemini model"""
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 2048,
    }
    
    system_instruction = f"""You are ATIK SZ's AI assistant specialized in Bangladesh Election Commission Voter List Data.

Your role:
- Help users find information about Bangladesh Election Commission voter lists
- Answer questions ONLY based on the provided voter data knowledge base from NotebookLM
- Provide accurate voter information, polling station details, and election-related data
- If information is not in the knowledge base, clearly state that
- Be helpful, professional, and respectful when handling voter information
- Cite the source document when providing information

Knowledge Base (From NotebookLM):
{knowledge_content}
"""
    
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_instruction
    )

# --- CHAT EXPORT ---
def export_chat_history():
    """Export chat history as JSON"""
    if st.session_state.messages:
        chat_data = {
            "exported_at": datetime.now().isoformat(),
            "messages": st.session_state.messages,
            "total_messages": len(st.session_state.messages)
        }
        return json.dumps(chat_data, indent=2)
    return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🗳️ ATIK SZ - Voter Info Assistant")
    st.markdown("---")
    
    # Knowledge Base Management
    st.markdown("### 📊 Voter Data Source")
    knowledge_content, knowledge_files = load_knowledge_base()
    
    st.markdown(f"**Active Data Files:** {len(knowledge_files)}")
    
    with st.expander("📁 Manage Voter Data Files", expanded=False):
        for i, filename in enumerate(knowledge_files):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(filename)
            with col2:
                if st.button("🗑️", key=f"del_{i}"):
                    if delete_knowledge_file(filename):
                        st.success(f"Deleted {filename}")
                        st.rerun()
    
    # File Upload
    st.markdown("### 📤 Upload Voter Data")
    uploaded_file = st.file_uploader(
        "Upload .txt files",
        type=["txt"],
        help="Upload voter data files from NotebookLM (text format)"
    )
    
    if uploaded_file:
        if st.button("💾 Save to Voter Database"):
            if save_uploaded_file(uploaded_file):
                st.success(f"✅ Saved {uploaded_file.name}")
                st.rerun()
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("📥 Export Chat"):
        export_data = export_chat_history()
        if export_data:
            st.download_button(
                label="💾 Download JSON",
                data=export_data,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("No chat history to export")
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Statistics")
    st.markdown(f"""
    <div class="stats-card">
        <h4 style="margin: 0; color: white;">Chat Statistics</h4>
        <p style="font-size: 2rem; margin: 0.5rem 0; font-weight: 700;">
            {len(st.session_state.get('messages', []))}
        </p>
        <p style="margin: 0; opacity: 0.9;">Total Messages</p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN APP ---
st.title("🗳️ ATIK SZ - Bangladesh Voter Information")
st.markdown("🇧🇩 Search Bangladesh Election Commission Voter List Data | Powered by NotebookLM")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat session
if "chat_session" not in st.session_state:
    model = get_model(knowledge_content)
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("🔍 Search voter information, polling stations, or election data..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # Generate Response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Thinking..."):
            try:
                # Reload knowledge base to get latest updates
                knowledge_content, _ = load_knowledge_base()
                model = get_model(knowledge_content)
                chat_session = model.start_chat(history=[])
                
                response = chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.7; padding: 1rem;">
    🗳️ ATIK SZ • Bangladesh Election Commission Voter Data • Powered by <strong>Google Gemini AI</strong> & <strong>NotebookLM</strong>
</div>
""", unsafe_allow_html=True)
