#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py - Cross-platform path and runtime configuration helpers.

Goals:
- No hard-coded Windows drive letters
- Safe, configurable output directories
- Browser profile persistence is opt-in, not the default
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / ".local"


def get_data_dir() -> Path:
    """Return the base data directory used by the skill."""
    raw = os.environ.get("SKILL_DATA_DIR")
    base_dir = Path(raw).expanduser() if raw else DEFAULT_DATA_DIR
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_subdir(name: str) -> Path:
    """Create and return a named subdirectory under the skill data dir."""
    path = get_data_dir() / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def resolve_profile_dir(profile_dir: Optional[str] = None) -> tuple[Path, bool]:
    """
    Return (path, persistent).

    Priority:
    1. Explicit function argument
    2. XHS_PROFILE_DIR env var
    3. Temporary directory (non-persistent, default)
    """
    raw = profile_dir or os.environ.get("XHS_PROFILE_DIR")
    if raw:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        path.mkdir(parents=True, exist_ok=True)
        return path, True

    temp_path = Path(tempfile.mkdtemp(prefix="xhs_profile_"))
    return temp_path, False
