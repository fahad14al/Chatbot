import streamlit as st
from chatbot.chatbot import chatbot_response

# ------------------- Streamlit App Config -------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Title and Description
st.title("🤖 AI Chatbot using NLTK + TensorFlow + Free APIs")
st.markdown(
    """
    Welcome! 👋  
    Talk to your intelligent chatbot.  
    You can ask for **jokes**, **quotes**, **advice**, **cat facts**, **weather**, or **latest news**!  
    Example:  
    - "Tell me a joke"  
    - "Give me advice"  
    - "Weather in Dhaka"  
    - "Show me news"  
    """
)

# ------------------- Session State for Chat History -------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ------------------- Chat Input -------------------
if user_input := st.text_input("💬 You:", placeholder="Type your message here..."):
    # Get bot response from chatbot_core.py
    reply = chatbot_response(user_input)

    # Save to session history
    st.session_state["messages"].append(("🧍‍♂️ You", user_input))
    st.session_state["messages"].append(("🤖 Bot", reply))

# ------------------- Chat Display -------------------
st.markdown("### 💭 Chat History:")
if st.session_state["messages"]:
    for sender, msg in st.session_state["messages"]:
        with st.chat_message("user" if "You" in sender else "assistant"):
            st.markdown(f"**{sender}:** {msg}")
else:
    st.info("Start chatting above 👆")

# ------------------- Clear Chat Button -------------------
if st.button("Rerun app"):
    st.rerun()

# ------------------- Footer -------------------
st.markdown(
    """
    ---
    💡 **Built with Python, Streamlit, NLTK, and TensorFlow**  
    Free APIs used: Joke, Quote, Advice, Cat Facts, Weather, News 🌐
    """
)