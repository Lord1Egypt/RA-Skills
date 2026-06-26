import os
import random
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Instagram API ────────────────────────────────────────────────────────────
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID", "")
INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET", "")
INSTAGRAM_API_BASE = "https://graph.instagram.com"
INSTAGRAM_API_VERSION = "v21.0"

# ── Cloudflare R2 ────────────────────────────────────────────────────────────
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY", "")
R2_BUCKET = os.getenv("R2_BUCKET", "quiz-reels")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL", "")

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
CSV_PATH = BASE_DIR / "data" / "questions.csv"

OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


def build_caption(question_data: dict) -> str:
    """Build Instagram caption — format-aware, personal tone, hashtags at end only."""
    from bot.html_video_generator import get_video_format_for_day
    from bot.formatter import format_ig_caption

    fmt = get_video_format_for_day()
    category = question_data.get("category", "General Studies")
    category_tag = category.replace(" ", "").replace("&", "And")

    # Viral-optimised captions per video format
    FORMAT_CAPTIONS = {
        "timer_challenge": (
            "90% fail this UPSC question. can you get it right?\n\n"
            "drop your answer in the comments 👇\n\n"
            "#UPSC #IAS #UPSCPrelims #UPSCQuiz #PreviousYearQuestions "
            f"#{category_tag} #UPSC2026 #UPSCAspirants"
        ),
        "shocking_stat": (
            "went through 3274 UPSC questions. this pattern blew my mind 🤯\n\n"
            "save this before your exam — you'll thank me later\n\n"
            "#UPSC #IAS #UPSCPreparation #UPSCStrategy #PYQ "
            f"#{category_tag} #UPSC2026 #CivilServices"
        ),
        "comparison": (
            "₹0 vs ₹2 lakh UPSC prep — which one actually works? 🧵\n\n"
            "bookmark this. share with every aspirant you know.\n\n"
            "#UPSC #IAS #UPSCPreparation #UPSCTips #SmartPrep "
            f"#{category_tag} #UPSC2026 #IASPreparation"
        ),
        "loop_format": (
            "answer in 3 seconds. bet you can't 😅\n\n"
            "follow for a new question every day 👉\n\n"
            "#UPSC #IAS #UPSCQuiz #UPSCPrelims #DailyQuiz "
            f"#{category_tag} #UPSC2026 #UPSCAspirants"
        ),
    }

    if fmt in FORMAT_CAPTIONS:
        return FORMAT_CAPTIONS[fmt]

    # Fallback: existing quiz caption logic
    return format_ig_caption(question_data)
