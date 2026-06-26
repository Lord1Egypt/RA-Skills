"""
env_loader.py - Shared configuration helper for weatherpanel-note-aipc.

This helper intentionally does NOT parse generic user shell files such as env.bat.
It only exposes a stable state directory and optionally loads a dedicated JSON
config file with a small allowlist of non-secret keys.

Supported optional config file locations:
- ~/.openclaw/state/weatherpanel_note_aipc/config.json
- ~/.openclaw/state/weather_monitor/config.json  (legacy fallback)

Environment variables always take precedence over config.json.
"""

import json
import os

STATE_SLUG = "weatherpanel_note_aipc"
LEGACY_STATE_SLUG = "weather_monitor"

_HOME = os.environ.get("USERPROFILE") or os.environ.get("HOME") or os.path.expanduser("~")
if not _HOME or _HOME in {"~", "/root"}:
    _HOME = os.path.expanduser("~")

LEGACY_STATE_DIR = os.path.join(_HOME, ".openclaw", "state", LEGACY_STATE_SLUG)
STATE_DIR = os.path.join(_HOME, ".openclaw", "state", STATE_SLUG)
if not os.path.exists(STATE_DIR) and os.path.exists(LEGACY_STATE_DIR):
    STATE_DIR = LEGACY_STATE_DIR

CANVAS_ROOT_DEFAULT = os.path.join(_HOME, "clawd", "canvas")

_ALLOWED_CONFIG_KEYS = {
    "CANVAS_ROOT",
    "WEATHER_LAT",
    "WEATHER_LON",
    "WEATHER_TZ",
    "WEATHER_UNITS",
    "SUMMARIZE_BIN",
    "OBSIDIAN_BIN",
    "OBSIDIAN_VAULT",
    "OBSIDIAN_NOTE_PATH",
    "OPENCLAW_BASE_URL",
}


def _load_config_json():
    candidates = [
        os.path.join(os.path.join(_HOME, ".openclaw", "state", STATE_SLUG), "config.json"),
        os.path.join(os.path.join(_HOME, ".openclaw", "state", LEGACY_STATE_SLUG), "config.json"),
    ]
    config_path = next((p for p in candidates if os.path.exists(p)), None)
    if not config_path:
        return
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return

    if not isinstance(data, dict):
        return

    for key, value in data.items():
        if key not in _ALLOWED_CONFIG_KEYS:
            continue
        if key in os.environ:
            continue
        if value is None:
            continue
        os.environ[key] = str(value)


_load_config_json()
