import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")
st.title("📝 AI Text Summarizer")

text = st.text_area("Paste your text here", height=250)
length = st.selectbox("Summary length", ["1 sentence", "Short paragraph", "5 bullet points"])
tone = st.selectbox("Style", ["Simple", "Professional", "Explain like I'm 10"])

if st.button("Summarize") and text.strip():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("Add ANTHROPIC_API_KEY to your .env file.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"Summarize the text below as: {length}. Style: {tone}.\n\nText:\n{text}"
    with st.spinner("Summarizing..."):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=700,
                messages=[{"role": "user", "content": prompt}],
            )
            st.subheader("Summary")
            st.write(resp.content[0].text)
        except anthropic.APIError as e:
            st.error(f"Error: {e}")
