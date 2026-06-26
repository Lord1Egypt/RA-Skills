"""
config.py — Centralized configuration loaded from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── OpenAI ─────────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
IMAGE_MODEL: str = os.getenv("IMAGE_MODEL", "dall-e-3")

# ── Apify ──────────────────────────────────────────────────
APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")

# ── Facebook App ───────────────────────────────────────────
FB_APP_ID: str = os.getenv("FB_APP_ID", "")
FB_APP_SECRET: str = os.getenv("FB_APP_SECRET", "")
FB_CLIENT_TOKEN: str = os.getenv("FB_CLIENT_TOKEN", "")

# ── Facebook Page ──────────────────────────────────────────
FB_PAGE_ID: str = os.getenv("FB_PAGE_ID", "")
FB_USER_ACCESS_TOKEN: str = os.getenv("FB_USER_ACCESS_TOKEN", "")
FB_PAGE_ACCESS_TOKEN: str = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
FB_API_VERSION: str = os.getenv("API_VERSION", "v21.0")
FB_BASE_URL: str = f"https://graph.facebook.com/{FB_API_VERSION}"

# ── Runtime ────────────────────────────────────────────────
MAX_POST_RETRIES: int = int(os.getenv("MAX_POST_RETRIES", "3"))
POST_DELAY_SECONDS: int = int(os.getenv("POST_DELAY_SECONDS", "2"))


def validate():
    """Kiểm tra các biến môi trường bắt buộc."""
    missing = []
    required = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "APIFY_API_TOKEN": APIFY_API_TOKEN,
        "FB_APP_ID": FB_APP_ID,
        "FB_APP_SECRET": FB_APP_SECRET,
        "FB_PAGE_ID": FB_PAGE_ID,
    }
    for name, val in required.items():
        if not val:
            missing.append(name)
    if missing:
        raise EnvironmentError(
            f"❌ Thiếu biến môi trường: {', '.join(missing)}\n"
            "→ Kiểm tra file .env"
        )
