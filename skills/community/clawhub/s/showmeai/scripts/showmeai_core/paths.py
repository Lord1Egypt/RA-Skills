"""OS-native paths that never depend on an Agent brand."""

from __future__ import annotations

import os
import sys
from pathlib import Path


APP_NAME = "ShowMeAI Skill"
SLUG = "showmeai-skill"


def _home() -> Path:
    return Path.home()


def config_dir() -> Path:
    override = os.environ.get("SHOWMEAI_CONFIG_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        return Path(os.environ.get("APPDATA", _home() / "AppData" / "Roaming")) / APP_NAME
    if sys.platform == "darwin":
        return _home() / "Library" / "Application Support" / APP_NAME
    return Path(os.environ.get("XDG_CONFIG_HOME", _home() / ".config")) / SLUG


def config_file() -> Path:
    override = os.environ.get("SHOWMEAI_CONFIG_FILE", "").strip()
    return Path(override).expanduser() if override else config_dir() / "config.json"


def credentials_file() -> Path:
    return config_dir() / "credentials"


def state_dir() -> Path:
    override = os.environ.get("SHOWMEAI_STATE_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", _home() / "AppData" / "Local")) / APP_NAME
    if sys.platform == "darwin":
        return _home() / "Library" / "Application Support" / APP_NAME / "state"
    return Path(os.environ.get("XDG_STATE_HOME", _home() / ".local" / "state")) / SLUG


def task_dir() -> Path:
    return state_dir() / "tasks"
