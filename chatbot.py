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
st.markdown(
    '<div class="chatbot-title">Your Personal Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chatbot-subtitle">Ask me anything!</div>',
    unsafe_allow_html=True
)



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

st.markdown("""
<style>
/* ================================
   RESPONSIVE CHATBOT DESIGN
   ================================ */

/* Main app container */
.block-container {
    max-width: 1100px !important;
    padding-top: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Desktop title */
.chatbot-title {
    font-size: 42px;
    font-weight: 700;
    color: #183153;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Subtitle */
.chatbot-subtitle {
    font-size: 18px;
    color: #555;
    margin-bottom: 25px;
}

/* Robot */
.animated-bot {
    display: flex;
    justify-content: center;
    align-items: center;
}

.animated-bot img {
    width: 180px;
    max-width: 100%;
    height: auto;
}

/* Chat messages */
.stChatMessage {
    width: 100% !important;
}

/* Chat input */
.stChatInput {
    width: 100% !important;
}


/* ================================
   MOBILE
   ================================ */

@media (max-width: 768px) {

    .block-container {
        padding: 1rem 0.8rem 5rem 0.8rem !important;
        max-width: 100% !important;
    }

    .chatbot-title {
        font-size: 28px !important;
        text-align: center !important;
        line-height: 1.2 !important;
        margin-top: 5px !important;
        margin-bottom: 8px !important;
    }

    .chatbot-subtitle {
        font-size: 15px !important;
        text-align: center !important;
        margin-bottom: 15px !important;
    }

    .animated-bot {
        margin: 5px auto 10px auto !important;
        display: flex !important;
        justify-content: center !important;
    }

    .animated-bot img {
        width: 110px !important;
        max-width: 110px !important;
        height: auto !important;
    }

    /* Chat messages fit the phone */
    .stChatMessage {
        padding: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    .stChatMessage p {
        font-size: 14px !important;
    }

    /* Input area */
    .stChatInput {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* Buttons */
    .stButton button {
        width: 100% !important;
        font-size: 14px !important;
    }
}


/* Extra-small phones */
@media (max-width: 480px) {

    .block-container {
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }

    .chatbot-title {
        font-size: 24px !important;
    }

    .chatbot-subtitle {
        font-size: 14px !important;
    }

    .animated-bot img {
        width: 90px !important;
    }
}
</style>
""", unsafe_allow_html=True)



#creating chat history
if "messages" not in st.session_state:
    st.session_state.messages=[]

    #display the previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        #accept user input
user_input = st.chat_input("Type your message...")


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


    
    
