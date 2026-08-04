import streamlit as st
import base64
from openai import OpenAI

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Goldvision AI",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. OPENAI CLIENT INITIALIZATION (SECURE)
# ---------------------------------------------------------
# Pulls the API key safely from Streamlit Secrets
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ API Key missing! Please add `OPENAI_API_KEY` to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------------------------------------------------
# 3. APP HEADER & LOGO
# ---------------------------------------------------------
# Displays your logo centered at the top
st.image("logo.png", use_container_width=True)

st.title("Goldvision AI")
st.markdown("##### Upload a chart screenshot for automated technical analysis & risk management.")

# ---------------------------------------------------------
# 4. CHART UPLOAD & ANALYSIS SECTION
# ---------------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Chart Screenshot", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Display preview of uploaded chart
    st.image(uploaded_file, caption="Uploaded Chart Preview", use_container_width=True)
    
    if st.button("Analyze Chart", type="primary"):
        with st.spinner("Analyzing market structure, levels, and trends..."):
            try:
                # Convert uploaded image to base64 for OpenAI Vision
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode("utf-8")
                
                # Send request to OpenAI GPT-4 Vision model
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "Analyze this trading chart. Provide technical structure, trend bias, key support/resistance levels, and risk management recommendations."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                    max_tokens=600
                )
                
                # Display output
                st.success("Analysis Complete!")
                st.markdown("### 📊 Market Breakdown")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error analyzing chart: {e}")


