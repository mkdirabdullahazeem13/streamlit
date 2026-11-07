# 💌 Ask-Out App

A small, cute web page built with [Streamlit](https://streamlit.io) for asking someone out on a date.
They pick Yes or No. If they say yes, they choose a spot and a time, and a confirmation email is sent.

## How it works

1. Edit `config.properties` to set their name, your name, and the date ideas.
2. Run the app and send them the link.
3. When they lock in a date, the confirmation goes to their email (and to yours).

## Quick start

```bash
cd ask-out-app
pip install -r requirements.txt
streamlit run app.py
```

The page opens at http://localhost:8501.

## Customise it

Open `config.properties` and change the values after each `=` sign:

| Setting | What it does |
|---|---|
| `partner_name` | The name in the heading ("Hey Sam! 💌") |
| `your_name` | Signs the confirmation email |
| `your_email` | You get a copy of the confirmation. Leave empty to skip |
| `question` | The big question |
| `date_spots` | Date ideas to choose from, separated by a vertical bar character |
| `time_slots` | Times to choose from, separated by a vertical bar character |

Restart the app after editing the file.

## Turn on confirmation emails (optional)

The page works without this, but no emails will be sent.

1. Copy `secrets.example.toml` to `.streamlit/secrets.toml`.
2. Put in the sending email address and an app password. For Gmail, create one at
   https://myaccount.google.com/apppasswords. Your normal password won't work.
3. Restart the app.

⚠️ Never commit `.streamlit/secrets.toml`. It contains your password. This repo's `.gitignore`
already excludes the `.streamlit/` folder.

## Share it

You can host it for free on [Streamlit Community Cloud](https://streamlit.io/cloud). Add your email
settings under the app's **Secrets** setting instead of using a file.

## Project files

```
ask-out-app/
├── app.py                # the web page
├── config.properties     # names, questions, date ideas (edit this)
├── secrets.example.toml  # template for email login details
├── requirements.txt      # Python packages needed
└── README.md
```
