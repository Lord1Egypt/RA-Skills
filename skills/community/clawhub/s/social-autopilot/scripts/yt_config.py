import random
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secrets.json"
TOKEN_FILE = BASE_DIR / "youtube_token.json"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"
CSV_PATH = BASE_DIR / "data" / "questions.csv"

OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ── YouTube API ───────────────────────────────────────────────────────────────
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

# Privacy: "private", "public", or "unlisted"
VIDEO_PRIVACY = "public"

# Category ID for Education
YOUTUBE_CATEGORY_EDUCATION = "27"


def build_title(question_data: dict) -> str:
    """Build YouTube video title — format-aware, lowercase, engaging, under 100 chars + #Shorts."""
    from bot.html_video_generator import get_video_format_for_day
    from bot.formatter import format_yt_title

    fmt = get_video_format_for_day()

    FORMAT_TITLES = {
        "timer_challenge": "90% fail this UPSC question. can you get it right? #Shorts",
        "shocking_stat": "went through 3274 UPSC questions. this pattern blew my mind #Shorts",
        "comparison": "₹0 vs ₹2 lakh UPSC prep — which one actually works? #Shorts",
        "loop_format": "answer in 3 seconds. bet you can't #Shorts",
    }

    if fmt in FORMAT_TITLES:
        return FORMAT_TITLES[fmt][:100]

    # Fallback: existing title logic
    title = format_yt_title(question_data)
    return title[:100]


def build_description(question_data: dict) -> str:
    """Build YouTube video description — format-aware, casual 2-3 lines + site link."""
    from bot.html_video_generator import get_video_format_for_day
    from bot.formatter import format_yt_description

    fmt = get_video_format_for_day()

    FORMAT_DESCRIPTIONS = {
        "timer_challenge": (
            "90% of UPSC aspirants get this question wrong on their first try.\n\n"
            "watch to the end to see the answer + explanation.\n\n"
            "free pyq practice: {BRAND_URL}"
        ),
        "shocking_stat": (
            "analyzed 3274 UPSC questions from 1995–2025. the patterns are wild.\n\n"
            "sharing so you don't have to figure it out the hard way.\n\n"
            "free pyq practice: {BRAND_URL}"
        ),
        "comparison": (
            "₹2 lakh coaching vs ₹0 self-study — the data on what actually works.\n\n"
            "bookmark this and share with every UPSC aspirant you know.\n\n"
            "free pyq practice: {BRAND_URL}"
        ),
        "loop_format": (
            "can you answer this UPSC question in 3 seconds?\n\n"
            "follow for a new question every day — your daily exam-mode practice.\n\n"
            "free pyq practice: {BRAND_URL}"
        ),
    }

    if fmt in FORMAT_DESCRIPTIONS:
        return FORMAT_DESCRIPTIONS[fmt]

    # Fallback: existing description logic
    return format_yt_description(question_data)
