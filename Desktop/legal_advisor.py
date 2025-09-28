# legal_advisor.py
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Page setup
st.set_page_config(
    page_title="Legal Advisor AI - Indian Law Specialist",
    page_icon="⚖️",
    layout="wide"
)

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ No API key found. Add GEMINI_API_KEY to your .env file")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# LEGAL SPECIALIZED CONFIGURATION
legal_generation_config = {
    "temperature": 0.2,  # More factual and precise
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

legal_safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

legal_model = genai.GenerativeModel(
    legal_model = genai.GenerativeModel("gemini-1.0-pro"),
    generation_config=legal_generation_config,
    safety_settings=legal_safety_settings
)

# LEGAL SYSTEM PROMPT - This makes it a legal advisor
LEGAL_ADVISOR_PROMPT = """You are LegalBot, an AI legal advisor specializing in Indian law. You provide:

1. General information about Indian laws (IPC, CrPC, Constitution, Contract Act, etc.)
2. Basic legal guidance and explanations
3. Direction to relevant legal provisions
4. Suggestions for next steps in legal matters

IMPORTANT DISCLAIMERS:
- You are not a substitute for a qualified lawyer
- You cannot provide legally binding advice
- Always recommend consulting with a human lawyer for serious matters
- You don't have access to real-time case law updates

Focus on Indian legal system. Be precise, factual, and cautious in your responses."""

# Initialize chat history with legal context
if "legal_messages" not in st.session_state:
    st.session_state.legal_messages = [
        {"role": "system", "content": LEGAL_ADVISOR_PROMPT},
        {"role": "assistant", "content": "Hello! I'm LegalBot, your AI assistant for Indian legal matters. How can I help you today?"}
    ]

# UI Header
st.title("⚖️ Legal Advisor AI")
st.caption("Specialized in Indian Law - Providing general legal information and guidance")

# Disclaimer
with st.expander("⚠️ Important Disclaimer"):
    st.warning("""
    This AI provides general legal information only. It is NOT a substitute for:
    - Qualified legal advice from a human lawyer
    - Court proceedings or legal representation
    - Legally binding opinions
    
    Always consult with a practicing advocate for serious legal matters.
    """)

# Display chat messages (excluding system prompt)
for message in st.session_state.legal_messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input with legal placeholder
if prompt := st.chat_input("Ask about Indian law, rights, or legal procedures..."):
    # Add user message to history
    st.session_state.legal_messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response with legal context
    with st.chat_message("assistant"):
        with st.spinner("Researching legal information..."):
            try:
                # Build conversation context
                conversation_context = "\n".join(
                    [f"{m['role']}: {m['content']}" for m in st.session_state.legal_messages]
                )
                
                response = legal_model.generate_content(conversation_context)
                answer = response.text
                
                # Display response
                st.markdown(answer)
                
                # Add to history
                st.session_state.legal_messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"I apologize, I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
                st.error(error_msg)
                st.session_state.legal_messages.append({"role": "assistant", "content": error_msg})

# Sidebar with legal resources
with st.sidebar:
    st.header("📚 Legal Resources")
    st.markdown("""
    **Indian Legal Portals:**
    - [Indian Kanoon](https://indiankanoon.org) - Case law database
    - [Bare Acts](https://www.indiacode.nic.in) - Official laws
    - [NALSA](https://nalsa.gov.in) - Legal aid services
    
    **Emergency Contacts:**
    - National Legal Services Authority: 011-23382778
    - Police Emergency: 100
    - Women's Helpline: 1091
    
    **Remember:** This AI provides general information only.
    For specific legal advice, consult a qualified advocate.
    """)
    
    # Clear chat button
    if st.button("🔄 Start New Conversation"):
        st.session_state.legal_messages = [
            {"role": "system", "content": LEGAL_ADVISOR_PROMPT},
            {"role": "assistant", "content": "Hello! I'm LegalBot, your AI assistant for Indian legal matters. How can I help you today?"}
        ]
        st.rerun()

# Footer
st.divider()
st.caption("LegalBot AI - Providing accessible legal information for Indian citizens. Not a substitute for professional legal advice.")
