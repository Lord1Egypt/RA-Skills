"""Config management: API key loading and persistence."""

import json
import os
from pathlib import Path

API_BASE = os.environ.get("REDDITRANK_API_BASE", "https://clawagents.dev/reddit-rank/v1")

CONFIG_DIR = Path.home() / ".redditrank"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_api_key() -> str | None:
    """Load API key from env var, then config file."""
    key = os.environ.get("REDDITRANK_API_KEY")
    if key:
        return key

    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
            return data.get("api_key")
        except Exception:
            pass

    return None


def save_api_key(key: str):
    """Save API key to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text())
        except Exception:
            pass
    data["api_key"] = key
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def mask_key(key: str) -> str:
    """Show first 10 chars + masked remainder."""
    if len(key) <= 14:
        return key[:6] + "****"
    return key[:10] + "****" + key[-4:]
