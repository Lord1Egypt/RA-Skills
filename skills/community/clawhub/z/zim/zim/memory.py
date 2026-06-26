"""File-based JSON storage for traveler preferences and policies.

Persists to ~/.config/zim/ with one file per traveler profile.
Thread-safe for single-process use via atomic writes.
"""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path
from typing import Any

from zim.core import Policy, TravelPreferences

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "zim"


def _ensure_dir() -> Path:
    """Create the config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    return CONFIG_DIR


def _preferences_path(traveler_id: str = "default") -> Path:
    """Return the file path for a traveler's preferences."""
    return _ensure_dir() / f"preferences_{traveler_id}.json"


def _policy_path(traveler_id: str = "default") -> Path:
    """Return the file path for a traveler's policy."""
    return _ensure_dir() / f"policy_{traveler_id}.json"


def _atomic_write(path: Path, data: dict[str, Any]) -> None:
    """Write JSON atomically via temp file + rename."""
    _ensure_dir()
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, suffix=".tmp", prefix=path.stem
    )
    try:
        with open(tmp_fd, "w") as f:
            json.dump(data, f, indent=2, default=str)
        Path(tmp_path).replace(path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------

def load_preferences(traveler_id: str = "default") -> TravelPreferences:
    """Load traveler preferences from disk.

    Returns default preferences if the file doesn't exist.
    """
    path = _preferences_path(traveler_id)
    if not path.exists():
        logger.debug("No preferences file at %s — using defaults", path)
        return TravelPreferences()

    try:
        raw = json.loads(path.read_text())
        return TravelPreferences.model_validate(raw)
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Failed to load preferences from %s: %s", path, exc)
        return TravelPreferences()


def save_preferences(
    prefs: TravelPreferences,
    traveler_id: str = "default",
) -> Path:
    """Save traveler preferences to disk. Returns the file path."""
    path = _preferences_path(traveler_id)
    _atomic_write(path, prefs.model_dump())
    logger.info("Saved preferences to %s", path)
    return path


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------

def load_policy(traveler_id: str = "default") -> Policy:
    """Load travel policy from disk.

    Returns default policy if the file doesn't exist.
    """
    path = _policy_path(traveler_id)
    if not path.exists():
        logger.debug("No policy file at %s — using defaults", path)
        return Policy()

    try:
        raw = json.loads(path.read_text())
        return Policy.model_validate(raw)
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Failed to load policy from %s: %s", path, exc)
        return Policy()


def save_policy(
    pol: Policy,
    traveler_id: str = "default",
) -> Path:
    """Save travel policy to disk. Returns the file path."""
    path = _policy_path(traveler_id)
    _atomic_write(path, pol.model_dump())
    logger.info("Saved policy to %s", path)
    return path
