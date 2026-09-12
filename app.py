import os
import streamlit as st
from groq import Groq

# Page layout setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# Retrieve API key from environment variable or user input
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
    st.sidebar.markdown("[Get a free Groq API key](https://console.groq.com/keys)")

if not groq_api_key:
    st.info("Please provide a Groq API Key to continue.", icon="🔑")
    st.stop()

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Input controls
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox("Content Type", ["Social Media Post", "Article / Blog Summary", "Announcement", "Product Pitch"])
    platform = st.selectbox("Target Platform", ["LinkedIn", "Twitter / X", "Instagram", "Facebook"])
    tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Persuasive", "Informative", "Humorous"])

with col2:
    topic = st.text_input("Topic / Main Idea", placeholder="e.g., Remote work best practices")
    target_audience = st.text_input("Target Audience", placeholder="e.g., Software engineers, Small business owners")

# Generation logic
if st.button("Generate Content", type="primary", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic before generating content.")
    else:
        prompt = f""" You are an expert content manager and copywriter.
Create a complete post based on these requirements:
- Content Type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target Audience: {target_audience if target_audience else 'General Audience'}
- Tone: {tone}

Output structure required:
1. **Post Hook & Main Body**: Tailored specifically for {platform}.
2. **Caption**: A short, engaging 1-2 sentence caption.
3. **Hashtags**: 5-8 relevant, highly-searched hashtags.
"""

        with st.spinner("Generating post..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                output = response.choices[0].message.content
                st.success("Generated successfully!")
                st.markdown("---")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error generating content: {e}")