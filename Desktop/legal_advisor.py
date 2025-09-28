# legal_advisor.py - DEBUG TO FIND WORKING MODEL
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Legal Advisor AI", page_icon="⚖️")

# Load API key
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ No API key found")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# LIST ALL AVAILABLE MODELS
st.title("🔍 Finding Working Gemini Model...")

try:
    models = genai.list_models()
    st.success("✅ Connected to API! Available models:")
    
    working_models = []
    for model in models:
        st.write(f"📦 {model.name}")
        if 'generateContent' in model.supported_generation_methods:
            working_models.append(model.name)
            st.success(f"✅ CAN USE: {model.name}")
    
    st.subheader("🎯 Working Models:")
    for model_name in working_models:
        st.code(model_name)
        
    # Test the first working model
    if working_models:
        st.subheader("🚀 Testing first working model...")
        test_model = genai.GenerativeModel(working_models[0])
        response = test_model.generate_content("Hello, are you working?")
        st.success(f"✅ {working_models[0]} WORKS! Response: {response.text}")
        
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
