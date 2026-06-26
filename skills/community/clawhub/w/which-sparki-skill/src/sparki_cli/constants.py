"""Edit modes, style catalog, error codes, and limit constants."""

from enum import StrEnum


class EditMode(StrEnum):
    STYLE_GUIDED = "style-guided"
    PROMPT_DRIVEN = "prompt-driven"


STYLE_CATALOG: dict[str, dict[str | None, dict]] = {
    "vlog": {
        "energetic-sports":   {"tags": ["19"], "agent_type": None},
        "funny-commentary":   {"tags": ["20"], "agent_type": None},
        "daily":              {"tags": ["21"], "agent_type": "vlog"},
        "upbeat-energy":      {"tags": ["22"], "agent_type": None},
        "chill-vibe":         {"tags": ["23"], "agent_type": "vlog"},
    },
    "montage": {
        "highlight-reel":         {"tags": ["28"], "agent_type": None},
        "hype-beatsync":          {"tags": ["29"], "agent_type": None},
        "creative-splitscreen":   {"tags": ["30"], "agent_type": None},
        "meme-moments":           {"tags": ["31"], "agent_type": None},
    },
    "commentary": {
        "tiktok-trending-recap":  {"tags": ["24"], "agent_type": None},
        "funny-commentary":       {"tags": ["25"], "agent_type": None},
        "master-storyteller":     {"tags": ["26"], "agent_type": None},
        "first-person-narration": {"tags": ["27"], "agent_type": None},
    },
    "talking-head": {
        "tutorial":               {"tags": ["32"], "agent_type": None},
        "podcast-interview":      {"tags": ["33"], "agent_type": None},
        "product-review":         {"tags": ["34"], "agent_type": None},
        "reaction-commentary":    {"tags": ["35"], "agent_type": None},
    },
    "long-to-short": {
        None: {"tags": [], "agent_type": None,
               "default_prompt": "Find hooks, highlights, and turn the video into viral shorts"},
    },
    "ai-caption": {
        None: {"tags": [], "agent_type": None,
               "default_prompt": "Add captions to the video"},
    },
    "video-resizer": {
        None: {"tags": [], "agent_type": None,
               "default_prompt": "Reframe the video for the target aspect ratio"},
    },
}

VALID_DURATION_RANGES = {"<30s", "30s~60s", "60s~90s", ">90s", "custom"}

TELEGRAM_FILE_SIZE_LIMIT = 100 * 1024 * 1024
MAX_UPLOAD_SIZE = 3 * 1024 * 1024 * 1024
ALLOWED_EXTENSIONS = {"mp4", "mov"}
MAX_FILES_PER_UPLOAD = 10
DEFAULT_ASSET_POLL_INTERVAL = 10
DEFAULT_ASSET_POLL_TIMEOUT = 1200
DEFAULT_PROJECT_POLL_INTERVAL = 30
DEFAULT_PROJECT_POLL_TIMEOUT = 3600
DEFAULT_BASE_URL = "https://agent-api.sparki.io"
DEFAULT_UPLOAD_TG_LINK = "https://t.me/Sparki_AI_bot/upload"


def validate_style(style: str) -> bool:
    if not style:
        return False
    if "/" in style:
        category, sub = style.split("/", 1)
        return category in STYLE_CATALOG and sub in STYLE_CATALOG[category]
    else:
        return style in STYLE_CATALOG and None in STYLE_CATALOG[style]


def style_to_payload(style: str) -> dict:
    if "/" in style:
        category, sub = style.split("/", 1)
        return STYLE_CATALOG[category][sub]
    else:
        return STYLE_CATALOG[style][None]


def all_styles_list() -> list[str]:
    styles = []
    for category, subs in STYLE_CATALOG.items():
        for sub in subs:
            if sub is None:
                styles.append(category)
            else:
                styles.append(f"{category}/{sub}")
    return styles


ERROR_CODES: dict[str, dict[str, str]] = {
    "AUTH_FAILED": {
        "message": "Invalid or missing API key",
        "action": "Run `sparki setup --api-key <key>` or get a key from @sparki_bot on Telegram",
    },
    "QUOTA_EXCEEDED": {
        "message": "API quota exhausted",
        "action": "Visit https://sparki.io/pricing to upgrade",
    },
    "FILE_TOO_LARGE": {
        "message": "File exceeds 3GB limit",
        "action": "Compress or trim the video before uploading",
    },
    "CONCURRENT_LIMIT": {
        "message": "Too many projects running",
        "action": "Wait for a running project to complete",
    },
    "INVALID_FILE_FORMAT": {
        "message": "Unsupported file format",
        "action": "Only mp4 and mov files are supported",
    },
    "INVALID_STYLE": {
        "message": "Unknown style",
        "action": "See available styles with `sparki edit --help`",
    },
    "INVALID_MODE": {
        "message": "Unknown edit mode",
        "action": "Choose from: style-guided, prompt-driven",
    },
    "UPLOAD_FAILED": {
        "message": "Upload failed",
        "action": "Check your network connection and try again",
    },
    "RENDER_TIMEOUT": {
        "message": "Video processing timed out",
        "action": "Try a shorter clip or increase --timeout",
    },
    "TASK_NOT_FOUND": {
        "message": "Task not found",
        "action": "Run `sparki history` to see your recent tasks",
    },
    "NETWORK_ERROR": {
        "message": "Cannot reach Sparki servers",
        "action": "Check your internet connection and try again",
    },
}
