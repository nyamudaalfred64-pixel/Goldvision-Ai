import streamlit as st
from PIL import Image
import base64
from openai import OpenAI
import requests
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="st.set_page_config(
    page_title="Goldvision AI",
    page_icon="https://example.com/your-icon.png",
    layout="centered"
)
 "
)

# App Title & Branding
st.title("👑 KingAlfred: GoldVision AI")
st.write("Upload chart screenshots, use your phone camera, or paste image links for visual technical analysis.")

# Sidebar Configuration
st.sidebar.header("🔑 Setup & Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.caption("Powered by GoldVision AI | KingAlfred Edition")

# Input Selection
input_type = st.radio("Choose Input Method:", ["File Upload", "Camera Capture", "Image URL"])

image = None

if input_type == "File Upload":
    uploaded_file = st.file_uploader("Upload XAUUSD / Trading Chart Screenshot", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)

elif input_type == "Camera Capture":
    camera_file = st.camera_input("Take a photo of your MT5 / Trading Screen")
    if camera_file:
        image = Image.open(camera_file)

elif input_type == "Image URL":
    url = st.text_input("Paste Chart Image Link:")
    if url:
        try:
            res = requests.get(url)
            image = Image.open(BytesIO(res.content))
        except Exception:
            st.error("Unable to load image from the provided link.")

def convert_image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Process & Display Analysis
if image is not None:
    st.image(image, caption="Uploaded Market View", use_container_width=True)
    
    if st.button("🚀 Run GoldVision Analysis", type="primary"):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar menu.")
        else:
            with st.spinner("GoldVision AI is scanning trend lines, support/demand zones, and indicators..."):
                try:
                    client = OpenAI(api_key=api_key)
                    base64_image = convert_image_to_base64(image)
                    
                    prompt_instructions = """
                    You are a quantitative market analyst for KingAlfred's GoldVision AI. Analyze this trading chart in detail:
                    1. Trend & Structure: State the overall direction (Uptrend, Downtrend, Range) and market structure levels.
                    2. Support & Resistance: Identify key supply/demand zones and reaction areas.
                    3. Indicators & Price Action: Evaluate visible indicators (EMA, RSI, MACD) and candlestick patterns.
                    4. Market Bias: Output a clear verdict: Bullish, Bearish, or Neutral.
                    5. Trade Setup: If a high-probability trade exists, provide:
                       - Entry Range
                       - Stop Loss (SL)
                       - Take Profit (TP) ensuring a minimum 1:3 Risk-to-Reward ratio.
                    """
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_instructions},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ],
                        max_tokens=900
                    )
                    
                    st.success("GoldVision Analysis Complete!")
                    st.markdown("### 📊 Market Breakdown")
                    st.write(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Error executing AI analysis: {e}")
