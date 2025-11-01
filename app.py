import streamlit as st
from transformers import pipeline
import torch

st.title("alai")
st.markdown("Ask what you want")

@st.cache_resource
def load_chatbot():
    return pipeline(
        "text-generation",
        model="Qwen/Qwen2-1.5B-Instruct",
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )

with st.spinner("Loading chatbot..."):
    try:
        pipe = load_chatbot()
        st.success("Ready!")
    except Exception as e:
        st.error(f"Failed to load: {e}")
        st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Your question"):
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = pipe(
                    prompt, 
                    max_new_tokens=150, 
                    temperature=0.7
                )[0]['generated_text']
                st.markdown(response)
                st.session_state.history.append({
                    "role": "assistant", 
                    "content": response
                })
            except Exception as e:
                st.error(f"Error: {e}")
