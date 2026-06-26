#!/usr/bin/env python3
"""Persistent user taste profile for the spotify-playlist-curator skill.

Stores musical preferences (excluded artists, favorite genres, notes) in a
JSON file that agents read on every run. This lets agents remember things
like "never include Taylor Swift" or "user loves shoegaze" across sessions.

The profile file lives at:
  <skill_root>/taste_profile.json
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROFILE_PATH = Path(__file__).resolve().parent.parent / "taste_profile.json"

DEFAULT_PROFILE: dict[str, Any] = {
    "excluded_artists": [],
    "favorite_genres": [],
    "favorite_artists": [],
    "notes": [],
}


def load() -> dict[str, Any]:
    """Load the taste profile from disk, or return defaults if missing."""
    if PROFILE_PATH.exists():
        try:
            data = json.loads(PROFILE_PATH.read_text())
            # Ensure all expected keys exist
            for key, default in DEFAULT_PROFILE.items():
                if key not in data:
                    data[key] = default
            return data
        except (json.JSONDecodeError, KeyError):
            return dict(DEFAULT_PROFILE)
    return dict(DEFAULT_PROFILE)


def save(profile: dict[str, Any]) -> None:
    """Write the taste profile to disk."""
    PROFILE_PATH.write_text(json.dumps(profile, indent=2) + "\n")


def add_to_list(profile: dict[str, Any], key: str, value: str) -> bool:
    """Add a value to a list field (dedupe, case-insensitive match)."""
    existing = [v.lower() for v in profile.get(key, [])]
    if value.lower() not in existing:
        profile[key].append(value)
        return True
    return False


def remove_from_list(profile: dict[str, Any], key: str, value: str) -> bool:
    """Remove a value from a list field (case-insensitive match)."""
    original = profile.get(key, [])
    filtered = [v for v in original if v.lower() != value.lower()]
    if len(filtered) < len(original):
        profile[key] = filtered
        return True
    return False
