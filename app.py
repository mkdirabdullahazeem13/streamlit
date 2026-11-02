import streamlit as st
import smtplib
from email.message import EmailMessage

# Page configuration
st.set_page_config(page_title="A Special Question! 💖", page_icon="💌", layout="centered")

# Initialize session state so choices don't disappear on rerun
if "locked_in" not in st.session_state:
    st.session_state.locked_in = False

# Custom styling for a cute look & card-style radio buttons
st.markdown(
    """
    <style>
    .main {
        background-color: #fff0f5;
    }
    .title {
        color: #ff4b6e;
        text-align: center;
        font-size: 3.5em;
        font-weight: bold;
    }
    .subtitle {
        color: #555555;
        text-align: center;
        font-size: 1.2em;
    }
    /* Transform radio options into cute clickable cards */
    div[data-baseweb="radio"] label {
        background-color: #ffffff;
        border: 2px solid #ffb6c1;
        border-radius: 15px;
        padding: 12px 18px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[data-baseweb="radio"] label:hover {
        border-color: #ff4b6e;
        background-color: #ffe4e1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<h1 class="title">Hey there, Mariam! 💌</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">I have a very important question to ask you...</p>', unsafe_allow_html=True)

st.write("---")

# The Big Question
st.subheader("Will you go out on a date with me? 🥰")

# Answer selection
answer = st.radio(
    "Make your choice:",
    ["Yes! Absolutely 💖", "No way 😢"],
    index=None,
    key="main_answer"
)

# Function to send email
def send_invitation_emails(spot, time_slot, mariam_email):
    try:
        # Pulling credentials safely from Streamlit secrets
        sender_email = st.secrets["email"]["sender"]
        sender_password = st.secrets["email"]["password"]
        
        msg = EmailMessage()
        msg['Subject'] = "Date Confirmed! 🥰💖"
        msg['From'] = sender_email
        
        # Send to your email and her email
        recipients = ["abdullahazeem13@gmail.com"]
        if mariam_email:
            recipients.append(mariam_email)
        msg['To'] = ", ".join(recipients)
        
        msg.set_content(f"""
        Yay! The date is officially locked in! 🎉
        
        📍 Spot: {spot}
        ⏰ Time: {time_slot}
        
        Can't wait! 🥰💖
        """)
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

# If she selects Yes, show specific Dublin spots, time dropdown, and email inputs
if answer == "Yes! Absolutely 💖":
    st.write("---")
    st.markdown("### Yay! 🥰 Where should we go in Dublin?")
    
    dublin_spot = st.selectbox(
        "Choose a fun spot:",
        [
            "Bowling & games at Lane 7 🎳",
            "Arcade games & burgers at Token (Smithfield) 🕹️",
            "Movie night with luxury couches at Stella Cinema 🍿",
            "Cozy drinks & vibes at The Bernard Shaw 🍻",
            "Nice dinner in the city center 🍷"
        ]
    )
    
    time_slot = st.selectbox(
        "What time works best?",
        [
            "This Friday evening at 7:00 PM",
            "This Saturday afternoon at 3:00 PM",
            "This Saturday evening at 7:30 PM",
            "This Sunday afternoon at 2:00 PM",
            "This Sunday evening at 6:00 PM"
        ]
    )
    
    mariam_email = st.text_input("Enter your email address to get the confirmation invite sent to you 💌")
    
    if st.button("Lock it in! 💌"):
        with st.spinner("Sending confirmation..."):
            success = send_invitation_emails(dublin_spot, time_slot, mariam_email)
            st.session_state.locked_in = True

    if st.session_state.locked_in:
        st.balloons()
        st.success(f"It's a date! Can't wait for **{dublin_spot}** at **{time_slot}**! 🥰💖")
        st.info("📨 Details have been emailed to Abdullah and you!")

elif answer == "No way 😢":
    st.write("---")
    st.warning("Are you sure? Try clicking 'Yes!' instead! 😉 (No pressure, but you know you want to!)")