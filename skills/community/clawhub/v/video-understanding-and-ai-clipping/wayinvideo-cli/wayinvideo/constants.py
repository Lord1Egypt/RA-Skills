"""Constants, enumerations and default configuration for WayinVideo CLI."""

# ── API Endpoints ────────────────────────────────────────────────────────────

SUBMIT_ENDPOINTS = {
    "clip":          "https://wayinvideo-api.wayin.ai/api/v2/clips",
    "search":        "https://wayinvideo-api.wayin.ai/api/v2/clips/find-moments",
    "summarize":     "https://wayinvideo-api.wayin.ai/api/v2/summaries",
    "transcribe":    "https://wayinvideo-api.wayin.ai/api/v2/transcripts",
    "export":        "https://wayinvideo-api.wayin.ai/api/v2/clips/export",
}

UPLOAD_ENDPOINT = "https://wayinvideo-api.wayin.ai/api/v2/upload/single-file"

# ── Task categories ──────────────────────────────────────────────────────────

TASK_TYPES = ["clip", "search", "summarize", "transcribe", "export"]

# clip / search / export: results arrive incrementally while status is ONGOING
INCREMENTAL_TASKS = {"clip", "search", "export"}

# summarize / transcribe: full result only appears on SUCCEEDED
FINAL_ONLY_TASKS = {"summarize", "transcribe"}

# ── Terminal statuses ────────────────────────────────────────────────────────

TERMINAL_STATUSES = {"SUCCEEDED", "FAILED"}

# ── Parameter value sets ─────────────────────────────────────────────────────

DURATION_CHOICES = [
    "DURATION_0_30",
    "DURATION_0_90",
    "DURATION_30_60",
    "DURATION_60_90",
    "DURATION_90_180",
    "DURATION_180_300",
]

RATIO_CHOICES = [
    "RATIO_16_9",
    "RATIO_1_1",
    "RATIO_4_5",
    "RATIO_9_16",
]

RESOLUTION_CHOICES = [
    "SD_480",
    "HD_720",
    "FHD_1080",
    "QHD_2K",
    "UHD_4K",
]

CAPTION_DISPLAY_CHOICES = [
    "none",
    "both",
    "original",
    "translation",
]

AI_HOOK_SCRIPT_STYLE_CHOICES = [
    "serious",
    "casual",
    "informative",
    "conversational",
    "humorous",
    "parody",
    "inspirational",
    "dramatic",
    "empathetic",
    "persuasive",
    "neutral",
    "excited",
    "calm",
]

AI_HOOK_POSITION_CHOICES = [
    "beginning",
    "end",
]

# Supported language codes (ISO 639-1 / BCP 47 variants)
# Source: references/supported_languages.md
SUPPORTED_LANGUAGES = [
    "af", "sq", "am", "ar", "hy", "as", "az", "ba", "eu", "be", "bn", "bs", "br",
    "bg", "my", "ca", "zh-cn", "zh-tw", "hr", "cs", "da", "nl", "en", "et", "fo",
    "fi", "fr", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "hi", "hu",
    "is", "id", "it", "ja", "jw", "kn", "kk", "km", "ko", "lo", "la", "lv", "ln",
    "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "ne", "no", "nn",
    "oc", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sa", "sr", "sn", "sd", "si",
    "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta", "tt", "te", "th",
    "bo", "tr", "tk", "uk", "ur", "uz", "vi", "cy", "yi", "yo"
]

# ── File upload ──────────────────────────────────────────────────────────────

ALLOWED_VIDEO_MIMETYPES = [
    "video/x-msvideo",
    "video/mp4",
    "video/quicktime",
    "video/webm",
]
ALLOWED_VIDEO_EXTENSIONS = ["avi", "mp4", "mov", "webm"]
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024 * 1024  # 5 GB

# ── HTTP defaults ────────────────────────────────────────────────────────────

API_VERSION = "v2"
USER_AGENT = "wayinvideo-cli"

# ── Persistent configuration defaults ────────────────────────────────────────
# Stored in  ~/.wayinvideo/config.json

DEFAULT_CONFIG = {
    "save_results":   True,
    "save_dir":       "~/.wayinvideo/cache",
    "event_enabled":  False,
    "event_interval": 60,
    "poll_timeout":   3600,
    "poll_interval":  10,
    "defaults": {
        "target":              None,
        "clip": {
            "top_k":           10,
            "duration":        None,
            "export":          True,
            "ratio":           "RATIO_9_16",
            "resolution":      "FHD_1080",
            "caption_display": None,
            "cc_style_tpl":    None,
            "ai_hook":         True,
            "ai_hook_style":   "serious",
            "ai_hook_pos":     "beginning",
        },
        "search": {
            "top_k":           10,
            "export":          True,
            "ratio":           "RATIO_9_16",
            "resolution":      "FHD_1080",
            "caption_display": None,
            "cc_style_tpl":    None,
        },
        "export": {
            "resolution":      "FHD_1080",
            "ratio":           "RATIO_9_16",
            "caption_display": None,
            "cc_style_tpl":    None,
            "ai_hook":         True,
            "ai_hook_style":   "serious",
            "ai_hook_pos":     "beginning",
        },
    },
}

# ── Config key documentation (shown by `wayinvideo config keys`) ─────────────

CONFIG_KEYS_DOC = {
    "save_results":                     "Auto-save task results to file (bool, default: true)",
    "save_dir":                         "Default directory for result files (path)",
    "event_enabled":                    "Enable system event notifications via openclaw (bool, default: false)",
    "event_interval":                   "Min seconds between event notifications (int, default: 60)",
    "poll_timeout":                     "Default max polling duration in seconds (int, default: 3600)",
    "poll_interval":                    "Seconds between poll API requests (int, default: 10)",
    "defaults.target":                  "Global default target language, e.g. en, zh (str or null)",
    "defaults.clip.top_k":              "Default clip count for AI clipping (int, default: 10)",
    "defaults.clip.duration":           "Default clip duration range, e.g. DURATION_0_30 (str or null)",
    "defaults.clip.export":             "Enable rendering by default for clipping (bool, default: true)",
    "defaults.clip.ratio":              "Default aspect ratio for clipping export (str, default: RATIO_9_16)",
    "defaults.clip.resolution":         "Default resolution for clipping export (str, default: FHD_1080)",
    "defaults.clip.caption_display":    "Default caption mode for clipping export (str, default: null)",
    "defaults.clip.cc_style_tpl":       "Default caption style template for clipping (str, default: null)",
    "defaults.clip.ai_hook":            "Add an automatically generated, attention-grabbing text hook (bool, default: true)",
    "defaults.clip.ai_hook_style":      "Style of the generated hook text (str, default: serious)",
    "defaults.clip.ai_hook_pos":        "Position of the generated hook text (str, default: beginning)",
    "defaults.search.top_k":            "Default result count for find-moments (int, default: 10)",
    "defaults.search.export":           "Enable rendering by default for moments (bool, default: true)",
    "defaults.search.ratio":            "Default aspect ratio for moments export (str, default: RATIO_9_16)",
    "defaults.search.resolution":       "Default resolution for moments export (str, default: FHD_1080)",
    "defaults.search.caption_display":  "Default caption mode for moments export (str, default: null)",
    "defaults.search.cc_style_tpl":     "Default caption style template for moments (str, default: null)",
    "defaults.export.resolution":       "Default resolution for export task (str, default: FHD_1080)",
    "defaults.export.ratio":            "Default aspect ratio for export task (str, default: null)",
    "defaults.export.caption_display":  "Default caption mode for export task (str, default: null)",
    "defaults.export.cc_style_tpl":     "Default caption style template for export task (str, default: null)",
    "defaults.export.ai_hook":          "Enable text hooks for export task (bool, default: true)",
    "defaults.export.ai_hook_style":    "Style of hook text for export task (str, default: serious)",
    "defaults.export.ai_hook_pos":      "Position of hook text for export task (str, default: beginning)",
}
