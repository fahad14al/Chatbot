!pip install transformers accelerate bitsandbytes streamlit

import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

st.title("alai)")
st.markdown("ASk what you want")

model_name = "Qwen/Qwen2-1.5B-Instruct"

with st.spinner("Model is Loading"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Write your question"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Now I am thinking🤔..."):
            reply = pipe(prompt, max_new_tokens=200, temperature=0.7)[0]['generated_text']
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
