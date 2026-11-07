"""
Ask-out app: a small Streamlit web page for asking someone on a date.

Settings (names, date ideas, times) live in config.properties.
Email login details live in .streamlit/secrets.toml (never commit that file).
"""

import html
import smtplib
from email.message import EmailMessage
from pathlib import Path

import streamlit as st

CONFIG_PATH = Path(__file__).with_name("config.properties")
YES = "Yes! Absolutely 💖"
NO = "No way 😢"


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------
@st.cache_data
def load_config(path: Path = CONFIG_PATH) -> dict:
    """Read simple `key = value` lines from the properties file."""
    defaults = {
        "partner_name": "there",
        "your_name": "Someone special",
        "your_email": "",
        "page_title": "A Special Question!",
        "intro_text": "I have a very important question to ask you...",
        "question": "Will you go out on a date with me?",
        "date_spots": "Dinner | Movie night",
        "time_slots": "This Saturday evening at 7:00 PM",
        "smtp_host": "smtp.gmail.com",
        "smtp_port": "465",
    }
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "!")) or "=" not in line:
                continue
            key, value = line.split("=", 1)
            defaults[key.strip()] = value.strip()
    return defaults


def as_list(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


cfg = load_config()
partner = cfg["partner_name"]

st.set_page_config(page_title=f"{cfg['page_title']} 💖", page_icon="💌", layout="centered")

if "locked_in" not in st.session_state:
    st.session_state.locked_in = False
    st.session_state.email_sent = False

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4ec 50%, #ffd6e3 100%);
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* The white card in the middle of the page */
    .block-container {
        max-width: 640px;
        margin-top: 2rem;
        padding: 2.5rem 2.5rem 3rem 2.5rem;
        background: rgba(255, 255, 255, 0.85);
        border-radius: 28px;
        box-shadow: 0 12px 40px rgba(255, 75, 110, 0.18);
    }

    .title {
        text-align: center;
        font-size: 2.6em;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.2em;
        background: linear-gradient(90deg, #ff4b6e, #ff8fa3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        color: #6b6b6b;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 1.2em;
    }
    h2, h3 { color: #ff4b6e !important; text-align: center; }

    /* Radio options as clickable cards */
    div[data-baseweb="radio"] label {
        background-color: #ffffff;
        border: 2px solid #ffb6c1;
        border-radius: 16px;
        padding: 12px 18px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    div[data-baseweb="radio"] label:hover {
        border-color: #ff4b6e;
        background-color: #ffe4e1;
        transform: translateY(-2px);
    }

    /* Main button */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 999px;
        padding: 0.7em 1em;
        font-weight: 600;
        font-size: 1.05em;
        color: white;
        background: linear-gradient(90deg, #ff4b6e, #ff7a93);
        box-shadow: 0 6px 18px rgba(255, 75, 110, 0.35);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(255, 75, 110, 0.45);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Email
# ----------------------------------------------------------------------------
def send_invitation_emails(spot: str, time_slot: str, partner_email: str) -> bool:
    """Send the confirmation. Returns True if it worked, False if anything failed."""
    recipients = [e for e in (cfg["your_email"], partner_email.strip()) if e]
    if not recipients:
        return False
    try:
        sender = st.secrets["email"]["sender"]
        password = st.secrets["email"]["password"]

        msg = EmailMessage()
        msg["Subject"] = "Date Confirmed! 🥰💖"
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg.set_content(
            f"Yay! The date is officially locked in! 🎉\n\n"
            f"📍 Spot: {spot}\n"
            f"⏰ Time: {time_slot}\n\n"
            f"Can't wait! 🥰💖\n— {cfg['your_name']}"
        )

        with smtplib.SMTP_SSL(cfg["smtp_host"], int(cfg["smtp_port"])) as server:
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception:
        return False


# ----------------------------------------------------------------------------
# Page
# ----------------------------------------------------------------------------
# html.escape stops a name like "<script>" from being treated as code.
st.markdown(f'<h1 class="title">Hey {html.escape(partner)}! 💌</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{html.escape(cfg["intro_text"])}</p>', unsafe_allow_html=True)

st.subheader(f"{cfg['question']} 🥰")

answer = st.radio("Make your choice:", [YES, NO], index=None, key="main_answer")

if answer == YES:
    st.markdown("### Yay! 🥰 Where should we go?")

    spot = st.selectbox("Choose a fun spot:", as_list(cfg["date_spots"]))
    time_slot = st.selectbox("What time works best?", as_list(cfg["time_slots"]))
    partner_email = st.text_input("Your email, so we can send you the confirmation 💌")

    if st.button("Lock it in! 💌"):
        with st.spinner("Sending confirmation..."):
            st.session_state.email_sent = send_invitation_emails(spot, time_slot, partner_email)
            st.session_state.locked_in = True

    if st.session_state.locked_in:
        st.balloons()
        st.success(f"It's a date! Can't wait for **{spot}** at **{time_slot}**! 🥰💖")
        if st.session_state.email_sent:
            st.info("📨 The details have been emailed to you!")
        else:
            st.warning(
                "The date is set, but the confirmation email couldn't be sent. "
                "Check the email address and the app's email settings."
            )

elif answer == NO:
    st.warning("Are you sure? Try clicking 'Yes!' instead! 😉 (No pressure, but you know you want to!)")
