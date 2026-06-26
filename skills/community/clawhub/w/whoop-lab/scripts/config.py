"""
Shared configuration loader for the WHOOP skill.

Reads config.json from ~/.config/whoop-skill/config.json.
All path values support ~ expansion. Users can override any value in config.json.

Config keys:
  creds_path       - Path to credentials.json (OAuth tokens)
  vault_path       - Root of your Obsidian vault
  daily_notes_subdir - Subfolder inside vault for daily notes (default: "Daily Notes")
  timezone         - Your local timezone (default: "America/New_York")
  logged_by        - Name shown in the "Logged by X" footer (default: "Assistant")
"""

import json
import sys
from pathlib import Path

# Always resolve to absolute path so scripts work from any cwd
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path("~/.config/whoop-skill/config.json").expanduser()

_DEFAULTS = {
    "creds_path": "~/.config/whoop-skill/credentials.json",
    "vault_path": "~/obsidian-vault",
    "daily_notes_subdir": "Daily Notes",
    "timezone": "America/New_York",
    "logged_by": "Assistant",
}


def load() -> dict:
    cfg = dict(_DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                overrides = json.load(f)
            cfg.update(overrides)
        except Exception as e:
            print(f"WARNING: Could not read {CONFIG_PATH}: {e}", file=sys.stderr)

    # Expand ~ in path values
    for key in ("creds_path", "vault_path"):
        cfg[key] = str(Path(cfg[key]).expanduser().resolve())

    return cfg


def creds_path() -> Path:
    return Path(load()["creds_path"])


def vault_path() -> Path:
    return Path(load()["vault_path"])


def daily_notes_dir() -> Path:
    cfg = load()
    return Path(cfg["vault_path"]) / cfg["daily_notes_subdir"]


def timezone() -> str:
    return load()["timezone"]


def logged_by() -> str:
    return load()["logged_by"]
