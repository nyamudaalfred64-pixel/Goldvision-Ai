import streamlit as st
import openai
import base64

# Page Configuration
st.set_page_config(page_title="KingAlfred's Goldvision AI", page_icon="📈", layout="centered")

st.title("📈 KingAlfred's Goldvision AI")
st.write("Upload a chart screenshot for technical analysis and risk management.")

# API Key Handling (Reads from Streamlit Secrets or Manual Input)
api_key = st.secrets.get("OPENAI_API_KEY") if "OPENAI_API_KEY" in st.secrets else st.sidebar.text_input("OpenAI API Key", type="password")

uploaded_file = st.file_uploader("Upload Chart Screenshot", type=["png", "jpg", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

if uploaded_file and api_key:
    client = openai.OpenAI(api_key=api_key)
    base64_image = encode_image(uploaded_file)
    
    if st.button("Analyze Chart"):
        with st.spinner("Analyzing market structure & risk ratios..."):
            prompt = """
            You are KingAlfred's Goldvision AI, an expert technical chart analyst.
            Analyze the attached trading chart screenshot and provide:
            1. **Market Structure & Trend:** (Break of Structure, Change of Character, Key Support/Resistance).
            2. **Trade Setup & Entry/Exit:** Identified entry point, stop loss, and take profit targets.
            3. **Strict Risk Parameters:**
               - Verify that the Risk-to-Reward ratio is **at least 1:3**.
               - State position sizing assuming account risk capped strictly between **0.7% and 1.0%**.
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }
                    ],
                    max_tokens=800
                )
                st.markdown("### 📊 Analysis Results")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error analyzing chart: {e}")

