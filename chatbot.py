from google import genai
import os
import streamlit as st
import base64
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

# Works locally with .env
# Also works on Streamlit Cloud with Secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=api_key)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Your Personal Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# RESPONSIVE CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN STREAMLIT CONTAINER
       ========================================= */

    .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }


    /* =========================================
       TITLE
       ========================================= */

    .chatbot-title {
        text-align: center;
        font-size: 44px;
        font-weight: 700;
        line-height: 1.2;
        color: #183153;

        /* Keeps heading close to robot */
        margin-top: -5px;
        margin-bottom: 10px;
    }


    /* =========================================
       SUBTITLE
       ========================================= */

    .chatbot-subtitle {
        text-align: center;
        font-size: 18px;
        color: #555555;
        margin-bottom: 25px;
    }


    /* =========================================
       ROBOT
       ========================================= */

    .animated-bot {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;

        /* Change this value to adjust distance
           between robot and heading */
        margin: 0 auto -15px auto;
    }

    .animated-bot img {
        width: 160px;
        max-width: 100%;
        height: auto;
        display: block;
    }


    /* =========================================
       CHAT MESSAGES
       ========================================= */

    [data-testid="stChatMessage"] {
        width: 100% !important;
    }

    [data-testid="stChatMessageContent"] {
        font-size: 16px;
    }


    /* =========================================
       CHAT INPUT
       ========================================= */

    [data-testid="stChatInput"] {
        width: 100% !important;
    }


    /* =========================================
       CLEAR CHAT BUTTON
       ========================================= */

    .clear-chat-container {
        display: flex;
        justify-content: center;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .clear-chat-container button {
        border-radius: 10px;
        padding: 8px 18px;
        border: 1px solid #ddd8ee;
        background-color: white;
        color: #333333;
        font-size: 13px;
    }

    .clear-chat-container button:hover {
        border-color: #7651e8;
        color: #7651e8;
    }


    /* =========================================
       MOBILE DEVICES
       ========================================= */

    @media (max-width: 768px) {

        .block-container {
            max-width: 100% !important;
            padding-top: 1rem !important;
            padding-bottom: 5rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }

        .chatbot-title {
            font-size: 29px !important;
            line-height: 1.2 !important;
            margin-top: -3px !important;
            margin-bottom: 8px !important;
        }

        .chatbot-subtitle {
            font-size: 15px !important;
            margin-bottom: 15px !important;
        }

        .animated-bot {
            margin-top: 0 !important;

            /* Robot closer to heading on mobile */
            margin-bottom: -10px !important;
        }

        .animated-bot img {
            width: 100px !important;
            max-width: 100px !important;
        }

        [data-testid="stChatMessage"] {
            padding: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 14px !important;
        }

        .clear-chat-container {
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .clear-chat-container button {
            font-size: 12px !important;
            padding: 7px 14px !important;
        }
    }


    /* =========================================
       SMALL PHONES
       ========================================= */

    @media (max-width: 480px) {

        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }

        .chatbot-title {
            font-size: 25px !important;
            margin-top: -3px !important;
        }

        .chatbot-subtitle {
            font-size: 14px !important;
        }

        .animated-bot {
            margin-bottom: -8px !important;
        }

        .animated-bot img {
            width: 85px !important;
            max-width: 85px !important;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 13px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD ANIMATED ROBOT
# =========================================================

try:

    with open("assets/animated_bot.gif", "rb") as f:
        gif = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div class="animated-bot">
            <img
                src="data:image/gif;base64,{gif}"
                alt="Animated chatbot robot"
            >
        </div>
        """,
        unsafe_allow_html=True
    )

except FileNotFoundError:

    st.warning("Animated bot image was not found.")


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="chatbot-title">Your Personal Chatbot</div>',
    unsafe_allow_html=True
)


# =========================================================
# SUBTITLE
# =========================================================

st.markdown(
    '<div class="chatbot-subtitle">Ask me anything!</div>',
    unsafe_allow_html=True
)


# =========================================================
# CREATE CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input("Type your message...")


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # -----------------------------------------------------
    # CREATE FULL CONVERSATION HISTORY
    # -----------------------------------------------------
    #
    # This is the important part.
    #
    # Previously, only "user_input" was sent to Gemini.
    # Now the complete conversation is sent.
    #
    # This allows Gemini to understand questions such as:
    #
    # User: Tell me about Python.
    # Bot: Python is a programming language...
    # User: What are its advantages?
    #
    # Gemini can now understand that "its" means Python.
    # -----------------------------------------------------

    conversation = []

    for message in st.session_state.messages:

        # Streamlit uses "assistant"
        # Gemini uses "model"
        if message["role"] == "assistant":
            role = "model"
        else:
            role = "user"

        conversation.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )


    # -----------------------------------------------------
    # GENERATE AI RESPONSE
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=conversation
        )

        ai_message = response.text

        if not ai_message:
            ai_message = "Sorry, I couldn't generate a response."

    except Exception as e:

        ai_message = f"Error: {e}"


    # -----------------------------------------------------
    # SAVE AI RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )


    # -----------------------------------------------------
    # REFRESH PAGE
    # -----------------------------------------------------

    st.rerun()


# =========================================================
# CLEAR CHAT BUTTON
# =========================================================

st.markdown(
    '<div class="clear-chat-container">',
    unsafe_allow_html=True
)

clear_chat = st.button(
    "🗑️ Clear Chat",
    key="clear_chat"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CLEAR CHAT ACTION
# =========================================================

if clear_chat:

    # Delete conversation history
    st.session_state.messages = []

    # Refresh application
    st.rerun()
