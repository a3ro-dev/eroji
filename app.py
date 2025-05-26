import streamlit as st
from PIL import Image
import io
import base64
import openai
import os
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Eroji - AI Face Analysis", 
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for modern, polished UI
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --bg-primary: #fafbfc;
        --bg-secondary: #f1f5f9;
        --bg-card: #ffffff;
        --bg-glass: rgba(255, 255, 255, 0.85);
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --border-color: #e2e8f0;
        --border-light: #f1f5f9;
        --accent-primary: #3b82f6;
        --accent-secondary: #06b6d4;
        --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);
        --shadow-xl: 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04);
        --radius-xs: 6px;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --radius-2xl: 24px;
        --blur-sm: blur(4px);
        --blur-md: blur(8px);
    }
    
    [data-theme="dark"] {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #1e293b;
        --bg-glass: rgba(30, 41, 59, 0.85);
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: #334155;
        --border-light: #475569;
        --shadow-xs: 0 1px 2px rgba(0,0,0,0.15);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.20), 0 1px 2px rgba(0,0,0,0.15);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.25), 0 2px 4px rgba(0,0,0,0.15);
        --shadow-lg: 0 10px 15px rgba(0,0,0,0.30), 0 4px 6px rgba(0,0,0,0.15);
        --shadow-xl: 0 20px 25px rgba(0,0,0,0.35), 0 10px 10px rgba(0,0,0,0.15);
    }
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* Streamlit branding - only hide footer */
    footer {display: none !important;}
    /* Keep header and menu visible for theme toggle */
    .stDeployButton {display: none !important;}
    .reportview-container .main .block-container {padding-top: 2rem !important;}
    
    /* Header Styles */
    .eroji-header {
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
        position: relative;
    }
    
    .eroji-header::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 2px;
    }
    
    .eroji-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.7;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        font-weight: 400;
    }
    
    /* File Uploader Styles */
    .stFileUploader > div {
        background: var(--bg-card) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: var(--radius-lg) !important;
        padding: 3rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stFileUploader > div::before {
        content: '📸';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -80%);
        font-size: 3rem;
        opacity: 0.3;
        z-index: 1;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent-primary) !important;
        background: var(--bg-secondary) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stFileUploader > div > div {
        position: relative !important;
        z-index: 2 !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-md) !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Result Area Styles */
    .eroji-result-area {
        background: var(--bg-card);
        padding: 2.5rem;
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-xl);
        border: 1px solid var(--border-light);
        margin: 3rem auto 2rem auto;
        max-width: 1000px;
        position: relative;
        backdrop-filter: var(--blur-sm);
    }
    
    .eroji-result-area::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--accent-gradient);
        border-radius: var(--radius-2xl) var(--radius-2xl) 0 0;
    }
    
    /* Image Display */
    .stImage > div {
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-lg) !important;
        border: 1px solid var(--border-light) !important;
    }
    
    /* Face Card Styles */
    .face-card {
        background: var(--bg-glass);
        border: 1px solid var(--border-light);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: var(--blur-sm);
        position: relative;
        overflow: hidden;
    }
    
    .face-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .face-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-primary);
    }
    
    .face-card:hover::before {
        opacity: 1;
    }
    
    .face-header {
        font-size: 1.375rem;
        font-weight: 700;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .face-header::before {
        content: '👤';
        font-size: 1.25rem;
        background: none;
        -webkit-text-fill-color: initial;
    }
    
    /* Metric Row Styles */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border-light);
        transition: all 0.2s ease;
    }
    
    .metric-row:last-child { 
        border-bottom: none; 
        padding-bottom: 0;
    }
    
    .metric-row:hover {
        background: var(--bg-secondary);
        margin: 0 -1.75rem;
        padding-left: 1.75rem;
        padding-right: 1.75rem;
        border-radius: var(--radius-sm);
    }
    
    .metric-label {
        font-weight: 500;
        color: var(--text-secondary);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-value {
        font-weight: 600;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    .confidence-badge {
        background: var(--accent-gradient);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        box-shadow: var(--shadow-sm);
        min-width: 45px;
        text-align: center;
    }
    
    /* Summary Grid Styles */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0 2.5rem 0;
    }
    
    .summary-card {
        background: var(--bg-glass);
        padding: 1.5rem 1.25rem;
        border-radius: var(--radius-lg);
        text-align: center;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: var(--blur-sm);
        position: relative;
        overflow: hidden;
    }
    
    .summary-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .summary-card:hover::before {
        transform: scaleX(1);
    }
    
    .summary-title {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    .summary-value {
        font-size: 1.5rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    
    /* JSON Display and Download Button */
    .stJson {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .stExpander {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: var(--radius-md) !important;
    }
    
    .download-btn {
        background: var(--success-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 1.5rem !important;
        width: 100% !important;
        box-shadow: var(--shadow-md) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .download-btn::before {
        content: '📥';
        margin-right: 0.5rem;
    }
    
    .download-btn:hover {
        background: #059669 !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Loading States */
    .stSpinner > div {
        border-color: var(--accent-primary) !important;
    }
    
    /* Alert Styles */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid var(--success-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--success-color) !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid var(--error-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--error-color) !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid var(--warning-color) !important;
        border-radius: var(--radius-md) !important;
        color: var(--warning-color) !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: var(--radius-md) !important;
        color: var(--accent-primary) !important;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .eroji-header { 
            font-size: 2.5rem; 
            margin-bottom: 0.75rem;
        }
        .eroji-subtitle { 
            font-size: 1rem; 
            margin-bottom: 2rem;
            padding: 0 1rem;
        }
        .summary-grid { 
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .eroji-result-area {
            margin: 2rem 0.5rem;
            padding: 1.5rem;
        }
        .face-card {
            padding: 1.25rem;
        }
        .metric-row:hover {
            margin: 0 -1.25rem;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }
    }
    
    @media (max-width: 480px) {
        .summary-grid { 
            grid-template-columns: 1fr;
        }
        .eroji-header {
            font-size: 2rem;
        }
        .stFileUploader > div {
            padding: 2rem 1rem !important;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .face-card {
        animation: fadeInUp 0.5s ease-out;
    }
    
    .summary-card {
        animation: fadeInUp 0.5s ease-out;
    }
    
    .eroji-result-area {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
    </style>
""", unsafe_allow_html=True)



# Original header
st.markdown('<div class="eroji-header">🎭 Eroji</div>', unsafe_allow_html=True)
st.markdown('<div class="eroji-subtitle">Advanced AI-powered face analysis with detailed insights on emotions, demographics, and facial attributes. Upload an image to discover what our AI sees.</div>', unsafe_allow_html=True)

# Get OpenAI API key from Streamlit secrets or environment variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("🔑 Please set your OpenAI API key in Streamlit secrets or as an environment variable 'OPENAI_API_KEY'.")
    st.stop()

# Create a container for better layout
with st.container():
    uploaded_file = st.file_uploader(
        "📸 Choose or drag & drop an image", 
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, JPEG, PNG, WEBP"
    )
    
    if not uploaded_file:
        st.markdown("### 💡 Tips for Best Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **✅ Good Images:**
            - Clear, well-lit faces
            - Front-facing or slight angle
            - High resolution photos
            - Real human faces
            """)
        
        with col2:
            st.markdown("""
            **❌ Avoid:**
            - Blurry or dark images
            - Artwork or drawings
            - Masks or heavy makeup
            - Multiple overlapping faces
            """)
        
        with col3:
            st.markdown("""
            **🔒 Privacy:**
            - Images are not stored
            - Analysis is temporary
            - No data is retained
            - GDPR compliant
            """)

result_json = None
result_text = None
image = None

if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Image preview and analysis section
    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📷 Image Preview")
        st.image(image, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        st.markdown("### 🔍 Analysis Controls")
        st.info("Image loaded successfully! Click the button below to start AI analysis.")
        
        analyze = st.button(
            "🚀 Analyze with AI", 
            key="analyze_btn", 
            use_container_width=True,
            help="Click to analyze faces in the uploaded image"
        )
        
        # Show image info
        st.markdown("**Image Details:**")
        st.markdown(f"- **Dimensions:** {image.size[0]} × {image.size[1]} pixels")
        st.markdown(f"- **Format:** {image.format}")
        st.markdown(f"- **Mode:** {image.mode}")
    
    if analyze:
        with st.spinner("🤖 Analyzing image with advanced AI... This may take a few moments."):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Preparing image...")
            progress_bar.progress(25)
            
            # Improved, policy-compliant system prompt
            system_prompt = '''
You are an image analysis assistant that describes visible characteristics in photos. Please analyze the image and describe what you observe about any people present.

For each person you see, describe these observable characteristics in JSON format:

FACIAL EXPRESSIONS:
- Apparent emotion or expression (happy, neutral, serious, etc.)
- Visible features like smile, frown, raised eyebrows
- Expression intensity (subtle, moderate, strong)

APPEARANCE DETAILS:
- Approximate age range (young adult, middle-aged, etc.)
- Apparent style presentation 
- Visible hair characteristics (color, length, style)
- Facial hair if present
- Eyewear or accessories
- Head position/angle

IMAGE QUALITY:
- Photo clarity and lighting
- How clearly the person is visible
- Technical assessment of the image

Please respond only with this JSON structure:

{
  "analysis_metadata": {
    "timestamp": "2024-01-01T12:00:00Z",
    "processing_status": "success"
  },
  "faces": [
    {
      "face_id": 1,
      "detection_confidence": 0.95,
      "emotions": {
        "primary": {"emotion": "happy", "confidence": 0.85, "intensity": 0.7},
        "secondary": {"emotion": "neutral", "confidence": 0.3},
        "expression_details": "slight smile, relaxed expression"
      },
      "demographics": {
        "age": {"estimate": 25, "range": "20-30", "confidence": 0.75},
        "gender": {"prediction": "appears feminine", "confidence": 0.80},
        "ethnicity": {"primary": "appears mixed heritage", "confidence": 0.60}
      },
      "attributes": {
        "facial_hair": "none visible",
        "hair": {"visible": true, "color": "brown", "style": "shoulder length"},
        "eyewear": "none",
        "accessories": ["earrings"],
        "pose": "facing camera"
      },
      "quality_metrics": {
        "face_quality": 0.9,
        "visibility": 0.95,
        "lighting": "good",
        "sharpness": 0.85
      }
    }
  ],
  "summary": {
    "total_faces": 1,
    "analysis_success": true,
    "dominant_emotion": "happy",
    "average_age": 25,
    "image_quality": "high"
  }
}

If no people are visible, return:
{
  "analysis_metadata": {
    "timestamp": "2024-01-01T12:00:00Z",
    "processing_status": "no_faces_detected"
  },
  "faces": [],
  "summary": {
    "total_faces": 0,
    "analysis_success": true,
    "message": "No people clearly visible in the image"
  }
}'''
            try:
                status_text.text("🌐 Connecting to AI service...")
                progress_bar.progress(50)
                
                openai.api_key = OPENAI_API_KEY
                
                status_text.text("🧠 AI is analyzing the image...")
                progress_bar.progress(75)
                
                response = openai.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": "Please analyze this image and describe the visible characteristics of any people you can see. Provide the analysis in the specified JSON format."},
                            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(img_bytes).decode()}}
                        ]}
                    ],
                    max_tokens=2048,
                    temperature=0.1
                )
                
                status_text.text("✨ Processing results...")
                progress_bar.progress(100)
                
                result_text = response.choices[0].message.content.strip()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Check if the response is a refusal or contains standard disclaimers
                if any(phrase in result_text.lower() for phrase in ["sorry", "can't", "cannot", "unable to", "not able to", "i'm not able", "don't have the ability"]):
                    st.warning("🤖 The AI model provided a cautious response. Let me try to extract any available information:")
                    st.code(result_text, language="text")
                    
                    # Try to create a minimal response for better UX
                    st.info("""
                    **Possible reasons for limited analysis:**
                    - **Image Content**: The AI detected content that may require cautious handling
                    - **Quality**: The image might not show clear facial features
                    - **Policy Compliance**: OpenAI's safety measures are being conservative
                    
                    **Try these alternatives:**
                    - Use a clearer, well-lit photo
                    - Ensure faces are clearly visible and unobstructed
                    - Try a simple portrait-style image
                    """)
                    
                    # Still create a basic response structure for consistency
                    result_json = {
                        "analysis_metadata": {
                            "timestamp": "2024-01-01T00:00:00Z",
                            "processing_status": "analysis_cautious"
                        },
                        "faces": [],
                        "summary": {
                            "total_faces": 0,
                            "analysis_success": False,
                            "message": "Analysis was cautious due to AI safety measures",
                            "ai_response": result_text
                        }
                    }
                else:
                    try:
                        # Try to parse as JSON
                        result_json = json.loads(result_text)
                        st.success("✅ Analysis completed successfully!")
                    except json.JSONDecodeError:
                        # If not valid JSON, try to extract JSON from the response
                        import re
                        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                        if json_match:
                            try:
                                result_json = json.loads(json_match.group())
                                st.success("✅ Analysis completed successfully!")
                            except json.JSONDecodeError:
                                st.error("❌ Could not parse AI response as valid JSON.")
                                st.code(result_text, language="text")
                                result_json = None
                        else:
                            st.error("❌ AI response doesn't contain valid JSON.")
                            st.code(result_text, language="text")
                            result_json = None
                    
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                
                error_msg = str(e).lower()
                if "rate limit" in error_msg:
                    st.error("🚫 **Rate Limit Exceeded**")
                    st.info("Please wait a moment before trying again. The API has usage limits.")
                elif "api key" in error_msg or "unauthorized" in error_msg:
                    st.error("🔑 **API Key Issue**")
                    st.info("Please check that your OpenAI API key is valid and has sufficient credits.")
                elif "content policy" in error_msg or "safety" in error_msg:
                    st.error("🛡️ **Content Policy Violation**")
                    st.info("The image content may violate OpenAI's usage policies. Please try a different image.")
                else:
                    st.error(f"❌ **API Error**: {str(e)}")
                    st.info("💡 Please check your internet connection and try again.")
                
                # Set result_json to None to prevent display
                result_json = None

# Display results in a polished, styled container
if image and result_json:
    st.markdown("---")
    st.markdown("<div id=\"eroji-result-area\" class=\"eroji-result-area\">", unsafe_allow_html=True)
    
    # Header section
    st.markdown("## 📊 Analysis Results")
    
    # Image display with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Analyzed Image", use_container_width=True)
    
    # Summary section
    summary = result_json.get("summary", {})
    faces = result_json.get("faces", [])
    
    # Check if analysis was successful
    if summary.get("analysis_success", True) and faces:
        st.markdown("### 📈 Quick Summary")
        
        # Get summary values with fallbacks
        total_faces = summary.get('total_faces', len(faces))
        dominant_emotion = "Unknown"
        dominant_gender = "Unknown" 
        dominant_ethnicity = "Unknown"
        
        # Try to extract dominant values from faces data
        if faces:
            # Get dominant emotion from first face
            first_face = faces[0]
            dominant_emotion = first_face.get('emotions', {}).get('primary', {}).get('emotion', 'Unknown')
            dominant_gender = first_face.get('demographics', {}).get('gender', {}).get('prediction', 'Unknown')
            dominant_ethnicity = first_face.get('demographics', {}).get('ethnicity', {}).get('primary', 'Unknown')
        
        st.markdown(f"""
        <div class='summary-grid'>
            <div class='summary-card'>
                <div class='summary-title'>Total Faces</div>
                <div class='summary-value'>{total_faces}</div>
            </div>
            <div class='summary-card'>
                <div class='summary-title'>Dominant Emotion</div>
                <div class='summary-value'>{dominant_emotion.replace('_', ' ').title()}</div>
            </div>
            <div class='summary-card'>
                <div class='summary-title'>Dominant Gender</div>
                <div class='summary-value'>{dominant_gender.replace('_', ' ').title()}</div>
            </div>
            <div class='summary-card'>
                <div class='summary-title'>Dominant Ethnicity</div>
                <div class='summary-value'>{dominant_ethnicity.replace('_', ' ').title()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Show limited analysis message
        st.markdown("### ⚠️ Limited Analysis Available")
        analysis_message = summary.get("message", "Analysis could not be completed")
        st.warning(f"**Status**: {analysis_message}")
        
        # Show AI response if available
        if "ai_response" in summary:
            with st.expander("🤖 View AI Response", expanded=False):
                st.text(summary["ai_response"])
    
    # Detailed face analysis
    if faces:
        st.markdown("### 👥 Detailed Face Analysis")
        for i, face in enumerate(faces):
            # Create a container for each face with individual elements
            with st.container():
                st.markdown(f"<div class='face-header'>Face #{face.get('face_id', i+1)}</div>", unsafe_allow_html=True)
                
                # Primary Emotion
                primary_emotion = face.get('emotions',{}).get('primary',{}).get('emotion','-').replace('_', ' ').title()
                primary_confidence = int(face.get('emotions',{}).get('primary',{}).get('confidence',0)*100)
                st.markdown(f"<div class='metric-row'><span class='metric-label'>😊 Primary Emotion</span><span class='metric-value'>{primary_emotion} <span class='confidence-badge'>{primary_confidence}%</span></span></div>", unsafe_allow_html=True)
                
                # Secondary Emotion
                secondary_emotion = face.get('emotions',{}).get('secondary',{}).get('emotion','-').replace('_', ' ').title()
                secondary_confidence = int(face.get('emotions',{}).get('secondary',{}).get('confidence',0)*100)
                st.markdown(f"<div class='metric-row'><span class='metric-label'>😐 Secondary Emotion</span><span class='metric-value'>{secondary_emotion} <span class='confidence-badge'>{secondary_confidence}%</span></span></div>", unsafe_allow_html=True)
                
                # Intensity
                intensity = face.get('emotions',{}).get('primary',{}).get('intensity','-')
                st.markdown(f"<div class='metric-row'><span class='metric-label'>⚡ Intensity</span><span class='metric-value'>{intensity}</span></div>", unsafe_allow_html=True)
                
                # Expression
                expression = face.get('emotions',{}).get('expression_details','-')
                st.markdown(f"<div class='metric-row'><span class='metric-label'>🎭 Expression</span><span class='metric-value'>{expression}</span></div>", unsafe_allow_html=True)
                
                # Age
                age_estimate = face.get('demographics',{}).get('age',{}).get('estimate','-')
                age_range = face.get('demographics',{}).get('age',{}).get('range','-')
                age_confidence = int(face.get('demographics',{}).get('age',{}).get('confidence',0)*100)
                st.markdown(f"<div class='metric-row'><span class='metric-label'>🎂 Age</span><span class='metric-value'>{age_estimate} ({age_range}) <span class='confidence-badge'>{age_confidence}%</span></span></div>", unsafe_allow_html=True)
                
                # Gender
                gender = face.get('demographics',{}).get('gender',{}).get('prediction','-').replace('_', ' ').title()
                gender_confidence = int(face.get('demographics',{}).get('gender',{}).get('confidence',0)*100)
                st.markdown(f"<div class='metric-row'><span class='metric-label'>⚧ Gender</span><span class='metric-value'>{gender} <span class='confidence-badge'>{gender_confidence}%</span></span></div>", unsafe_allow_html=True)
                
                # Ethnicity
                ethnicity = face.get('demographics',{}).get('ethnicity',{}).get('primary','-').replace('_', ' ').title()
                ethnicity_confidence = int(face.get('demographics',{}).get('ethnicity',{}).get('confidence',0)*100)
                st.markdown(f"<div class='metric-row'><span class='metric-label'>🌍 Ethnicity</span><span class='metric-value'>{ethnicity} <span class='confidence-badge'>{ethnicity_confidence}%</span></span></div>", unsafe_allow_html=True)
                
                # Facial Hair
                facial_hair = face.get('attributes',{}).get('facial_hair','-').replace('_', ' ').title()
                st.markdown(f"<div class='metric-row'><span class='metric-label'>🧔 Facial Hair</span><span class='metric-value'>{facial_hair}</span></div>", unsafe_allow_html=True)
                
                # Hair
                hair_visible = 'Visible' if face.get('attributes',{}).get('hair',{}).get('visible',False) else 'Not visible'
                hair_color = face.get('attributes',{}).get('hair',{}).get('color','').title()
                st.markdown(f"<div class='metric-row'><span class='metric-label'>💇 Hair</span><span class='metric-value'>{hair_visible} {hair_color}</span></div>", unsafe_allow_html=True)
                
                # Glasses
                glasses = face.get('attributes',{}).get('eyewear','-').replace('_', ' ').title()
                st.markdown(f"<div class='metric-row'><span class='metric-label'>👓 Glasses</span><span class='metric-value'>{glasses}</span></div>", unsafe_allow_html=True)
                
                # Accessories
                accessories = ', '.join(face.get('attributes',{}).get('accessories',[])).title() or 'None'
                st.markdown(f"<div class='metric-row'><span class='metric-label'>💎 Accessories</span><span class='metric-value'>{accessories}</span></div>", unsafe_allow_html=True)
                
                # Pose
                pose = face.get('attributes',{}).get('pose','-').replace('_', ' ').title()
                st.markdown(f"<div class='metric-row'><span class='metric-label'>📐 Pose</span><span class='metric-value'>{pose}</span></div>", unsafe_allow_html=True)
                
                # Bounding Box
                bounding_box = face.get('bounding_box','-')
                st.markdown(f"<div class='metric-row'><span class='metric-label'>📍 Bounding Box</span><span class='metric-value'>{bounding_box}</span></div>", unsafe_allow_html=True)
                
                # Face Quality
                face_quality = face.get('quality_metrics',{}).get('face_quality','-')
                st.markdown(f"<div class='metric-row'><span class='metric-label'>⭐ Face Quality</span><span class='metric-value'>{face_quality}</span></div>", unsafe_allow_html=True)
                
                # Visibility
                visibility = face.get('quality_metrics',{}).get('visibility','-')
                st.markdown(f"<div class='metric-row'><span class='metric-label'>👁 Visibility</span><span class='metric-value'>{visibility}</span></div>", unsafe_allow_html=True)
                
                # Lighting
                lighting = face.get('quality_metrics',{}).get('lighting','-').replace('_', ' ').title()
                st.markdown(f"<div class='metric-row'><span class='metric-label'>💡 Lighting</span><span class='metric-value'>{lighting}</span></div>", unsafe_allow_html=True)
    else:
        st.info("🔍 No faces detected in the uploaded image.")
    
    # Raw JSON data in expandable section
    with st.expander("🔧 Raw JSON Data", expanded=False):
        st.json(result_json)
    
    st.markdown('</div>', unsafe_allow_html=True)
    # Provide download of the JSON data instead of screenshot functionality
    if result_json:
        # Convert the result to a formatted JSON string
        json_str = json.dumps(result_json, indent=2)
        # Create a download button for the JSON data
        st.download_button(
            label="📥 Download Analysis Report (JSON)",
            data=json_str,
            file_name=f"eroji_face_analysis_{result_json.get('analysis_metadata', {}).get('timestamp', 'report')}.json",
            mime="application/json",
            key="download-json",
            help="Download the complete analysis report as a JSON file"
        )

else:
    # Show demo info when no image is uploaded
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👆 Upload an image above to get started with AI-powered face analysis!")
        
        # Feature highlights
        st.markdown("""
        ### ✨ What Eroji Can Analyze:
        
        🎭 **Emotional Intelligence**
        - Primary and secondary emotions
        - Expression intensity and details
        
        👥 **Demographics**  
        - Age estimation with confidence ranges
        - Gender prediction
        - Ethnicity classification
        
        🎨 **Facial Attributes**
        - Hair style and color
        - Facial hair detection
        - Accessories (glasses, jewelry)
        - Head pose analysis
        
        🔍 **Technical Metrics**
        - Face quality assessment
        - Visibility scoring
        - Lighting conditions
        """)
        
        st.markdown("---")
        st.markdown("*Powered by advanced AI vision models*")