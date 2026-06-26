import os

# ==========================================
# Google Gemini API Settings
# ==========================================
# Your Gemini API Key from Google AI Studio
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# ==========================================
# Telegram Bot Settings
# ==========================================
# Your Bot Token from @BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "YOUR_TG_BOT_TOKEN")

# The Chat ID where the bot will send the summary
# (Can be your user ID or a Group Chat ID)
TG_CHAT_ID = os.environ.get("TG_CHAT_ID", "YOUR_TG_CHAT_ID")

# ==========================================
# YouTube Settings
# ==========================================
# YouTube channels to monitor (Dictionary: Channel ID -> Channel Name)
# Example Channel ID (UC_x5XG1OV2P6uZZ5FSM9Ttw is Google Developers)
YOUTUBE_CHANNELS = {
    "UC_x5XG1OV2P6uZZ5FSM9Ttw": "Google Developers (Example)"
}

# ==========================================
# General Application Settings
# ==========================================
# Polling interval in minutes (how often to check for new videos)
POLL_INTERVAL_MINUTES = 60

# Data persistence file (records which videos have been summarized)
DB_FILE = "db.json"
