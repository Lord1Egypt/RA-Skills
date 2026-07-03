from pathlib import Path
# Standalone application (no OpenClaw dependency)

__version__ = "0.1.0"
__author__ = "Amre"

# Configuration
APP_NAME = "Signet Mind"
DATA_DIR = Path.home() / "SignetMind" / "data"
CONFIG_FILE = Path.home() / "SignetMind" / "config.json"

# Database
DB_PATH = DATA_DIR / "conversations.db"
MOOD_DB_PATH = DATA_DIR / "mood.db"

# Security
ENCRYPTION_KEY_FILE = DATA_DIR / ".key"

# Default settings
DEFAULT_CHECKIN_HOUR = 20  # 8 PM
DEFAULT_CHECKIN_ENABLED = True

# Crisis resources (local, always available)
CRISIS_RESOURCES = {
    "ireland": {
        "samaritans": "116 123",
        "pieta": "1800 247 247",
        "emergency": "112"
    },
    "uk": {
        "samaritans": "116 123",
        "mind": "0300 123 3393",
        "emergency": "999"
    },
    "general": {
        "crisis_text": "Text SHANE to 51444",
        "international": "https://findahelpline.com"
    }
}
