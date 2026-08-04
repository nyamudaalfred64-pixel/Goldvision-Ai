
import os
import base64
import streamlit as st
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
# Safely fetch API Key from Streamlit Secrets
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ API Key missing! Please add `OPENAI_API_KEY` in Streamlit Manage App > Settings > Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------------------------------------------------
# 3. APP HEADER & LOGO (SAFE DISPLAY)
# ---------------------------------------------------------
# Displays logo if uploaded to GitHub root; skips safely if missing
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)

st.title("Goldvision AI")
st.markdown("##### Upload a chart screenshot for clear technical analysis & risk management.")

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
        with st.spinner("Analyzing market structure, risk parameters, and setups..."):
            try:
                # Convert uploaded image to base64 for OpenAI Vision
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode("utf-8")
                
                # Structured prompt enforcing simple language & proper risk management
                prompt_text = (
                    "You are Goldvision AI, an expert trading assistant specializing in clear technical analysis and proper risk management.\n\n"
                    "Analyze the provided chart and return the breakdown using simple, easy-to-understand explanations in the following structure:\n\n"
                    "### 📈 1. Market Overview\n"
                    "- Explain current market direction (Upward/Downward/Ranging) in simple language.\n"
                    "- Identify key support and resistance zones clearly.\n\n"
                    "### 🎯 2. Trade Setups (Maximum 3 Setups)\n"
                    "- Recommend up to a MAXIMUM of 3 high-probability open trade setups.\n"
                    "- For each setup, specify:\n"
                    "  * **Direction:** BUY or SELL\n"
                    "  * **Entry Level:** Precise price or zone\n"
                    "  * **Stop-Loss (SL):** Specific price level (Crucial for protection)\n"
                    "  * **Take-Profit (TP):** Specific price level\n"
                    "  * **Risk-to-Reward Ratio (RRR):** Aim for at least 1:2 or higher.\n\n"
                    "### 🛡️ 3. Proper Risk Management Rules\n"
                    "- Give simple, clear advice on account capital protection:\n"
                    "  * **Account Risk:** Advise risking no more than 1% to 2% of total capital per trade.\n"
                    "  * **Lot Sizing Tip:** Simple reminder on keeping lot sizes controlled relative to the Stop-Loss.\n"
                    "  * **Trade Execution Note:** Explain simply why they should wait for confirmation before entering."
                )

                # Send request to OpenAI Vision model
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": prompt_text
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ]
                        }
                    ],
                    max_tokens=850
                )
                
                # Display output
                st.success("Analysis Complete!")
                st.markdown("### 📊 Market Breakdown & Risk Guidelines")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Error analyzing chart: {e}")
