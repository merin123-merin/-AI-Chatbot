from google import genai
import os
import requests
from dotenv import load_dotenv
import streamlit as st
import base64
from pathlib import Path

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")




#initialize genai client
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Chatbot with Streamlit and GEMINI",page_icon="robot_face:")
st.title("Your Personal Chatbot")
st.write("Ask me anything!")


# Animated bot
with open("assets/animated_bot.gif", "rb") as f:
    gif = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
.animated-bot {{
    position: fixed;
    top: 50px;
    left: 10px;
    z-index: 999;
}}

.animated-bot img {{
    width: 250px;
}}
</style>

<div class="animated-bot">
    <img src="data:image/gif;base64,{gif}">
</div>
""", unsafe_allow_html=True)


# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate chatbot response
    response = get_response(user_input)

    # Add chatbot response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(response)

# ---------------------------------------------------------
# CLEAR CHAT BUTTON
# ---------------------------------------------------------

if st.button("🗑️ Clear Chat", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate AI response
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_input
        )

        ai_message = response.text

        # Save AI message
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_message
        })

    except Exception as e:
        ai_message = f"Error: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_message
        })

    # Refresh the page so BOTH messages are displayed
    st.rerun()

st.markdown("""
<style>

/* Only position the Clear Chat container */
.st-key-clear_chat_container {
    position: fixed;
    bottom: 80px;
    right: 30px;
    z-index: 999;
}

/* Clear Chat button */
.st-key-clear_chat_container button {
    border-radius: 10px;
    padding: 8px 18px;
    border: 1px solid #ddd8ee;
    background-color: white;
    color: #333;
    font-size: 11px;
}

.st-key-clear_chat_container button:hover {
    border-color: #7651e8;
    color: #7651e8;
}

</style>
""", unsafe_allow_html=True)


    
    
