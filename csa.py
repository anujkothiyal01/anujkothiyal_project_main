import streamlit as st
import requests
import base64
from PIL import Image
import io

# Set page config
st.set_page_config(page_title="REAL-TIME CUSTOMER SEGMENTATION IN RETAIL MARKET", page_icon="🛒")

st.title("🛒 REAL-TIME CUSTOMER SEGMENTATION IN RETAIL MARKET")
st.markdown("Upload a customer image from a retail environment to analyze and segment the customer based on detected emotion. This demo uses OpenRouter's free multimodal AI to classify customer mood, which can be used for real-time segmentation and personalized marketing in retail analytics.")

# Input your OpenRouter API key (user input for flexibility)
api_key = st.text_input("🔑 Enter your OpenRouter API key", type="password", value="", help="Get a free key from https://openrouter.ai/ if you don't have one.")

# File uploader
uploaded_file = st.file_uploader("📷 Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    img_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(img_bytes).decode('utf-8')
    image_data_url = f"data:image/jpeg;base64,{image_base64}"

    if st.button("🧠 Segment Customer"):
        if not api_key:
            st.error("❌ Please enter your OpenRouter API key above.")
        else:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            with st.spinner("Segmenting customer..."):
                # API setup
                url = "https://openrouter.ai/api/v1/chat/completions"

                payload = {
                    "model": "meta-llama/llama-4-maverick:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are an AI assistant for real-time customer segmentation in retail. "
                                "Given a customer's image, classify them as one of: Deal Seeker, Product Researcher, Decisive Buyer, Social Shopper, Lost/Confused, Assistance Needed, Browsing Casually, Comparing Products, On a Mission, Waiting/Idle, Checking Out. "
                                "Return only the segment label. Do not explain your reasoning. Do not output anything except the label."
                            )
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_data_url
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": "Segment this retail customer by analyzing their appearance, posture, and context."
                                }
                            ]
                        }
                    ]
                }

                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=30)
                    if response.status_code == 200:
                        result = response.json()
                        emotion = result['choices'][0]['message']['content']
                        st.success("Customer Segmented ✅")
                        st.markdown(f"### 🧾 **Segment:** {emotion}")
                    else:
                        st.error(f"❌ Failed to get response: {response.status_code}")
                        st.code(response.text)
                except requests.exceptions.Timeout:
                    st.error("❌ The request timed out. Please try again.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
else:
    st.info("Please upload an image to begin.")

