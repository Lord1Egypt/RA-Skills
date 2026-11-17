"""Configuration, secret resolution, migration, and atomic persistence."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .errors import SkillError
from .paths import config_file, credentials_file


DEFAULT_BASE_URL = "https://api.showmeai.art/v1"
ONBOARDING_CATEGORIES = ("image", "video", "3d", "tts", "music")

DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": 3,
    "api": {"base_url": DEFAULT_BASE_URL},
    "catalog": {"refresh_ttl_hours": 24, "available_models_hash": ""},
    "onboarding": {
        "version": 1,
        "completed_categories": [],
        "catalog_hash": "",
        "completed_at": None,
    },
    "defaults": {
        "image": {
            "model": "gemini-3.1-flash-image",
            "fallback_candidates": ["gpt-image-2", "gemini-3-pro-image", "nano-banana-pro"],
            "fallback_on": ["model_unavailable", "capacity_unavailable"],
            "params": {"image_size": "1K", "aspect_ratio": "1:1"},
        },
        "video": {"model": "doubao-seedance-1-5-pro-251215", "params": {}},
        "3d": {"model": "Hunyuan3D-2", "params": {"format": "glb", "texture": True}},
        "tts": {"model": "tts-1", "params": {"voice": "alloy", "response_format": "mp3"}},
        "music": {"model": "chirp-crow", "params": {}},
    },
    "polling": {
        "wait_until_terminal": True,
        "max_wait_seconds": None,
        "heartbeat_seconds": 30,
        "max_transient_errors": 8,
    },
    "output": {
        "directory": "./showmeai-output",
        "download_remote_results": True,
        "collision": "suffix",
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config() -> dict[str, Any]:
    path = config_file()
    if not path.exists():
        return deepcopy(DEFAULT_CONFIG)
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SkillError("CONFIG_INVALID", f"Cannot read configuration: {error}") from error
    if not isinstance(loaded, dict):
        raise SkillError("CONFIG_INVALID", "Configuration root must be an object.")
    return _deep_merge(DEFAULT_CONFIG, loaded)


def _atomic_write(path: Path, text: str, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp_name, mode)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def save_config(config: dict[str, Any]) -> Path:
    path = config_file()
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup)
    config = deepcopy(config)
    config["schema_version"] = 3
    config["updated_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_write(path, json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    return path


def resolve_api_key(required: bool = True) -> tuple[str, str]:
    canonical = os.environ.get("SHOWMEAI_API_KEY", "").strip()
    if canonical:
        return canonical, "environment"
    legacy = os.environ.get("Showmeai_API_KEY", "").strip()
    if legacy:
        return legacy, "legacy_environment"
    path = credentials_file()
    if path.exists():
        value = path.read_text(encoding="utf-8").strip()
        if value:
            return value, "credentials_file"
    if required:
        raise SkillError(
            "SETUP_REQUIRED",
            "ShowMeAI API key is not configured.",
            details={
                "action": "run_setup",
                "command": "python3 scripts/showmeai.py setup",
                "agent_command": "python3 scripts/showmeai.py setup --key-stdin --json",
            },
        )
    return "", "missing"


def save_api_key(api_key: str) -> Path:
    value = api_key.strip()
    if len(value) < 8:
        raise SkillError("KEY_INVALID", "API key is too short.")
    path = credentials_file()
    _atomic_write(path, value + "\n", 0o600)
    return path


def set_path(config: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = [part for part in dotted_path.split(".") if part]
    if not parts:
        raise SkillError("CONFIG_PATH_INVALID", "Configuration path is empty.")
    cursor: dict[str, Any] = config
    for part in parts[:-1]:
        child = cursor.get(part)
        if child is None:
            child = {}
            cursor[part] = child
        if not isinstance(child, dict):
            raise SkillError("CONFIG_PATH_INVALID", f"{part} is not an object.")
        cursor = child
    cursor[parts[-1]] = value


def onboarding_status(config: dict[str, Any], category: str = "") -> str:
    """Return whether saved defaults have been explicitly confirmed."""
    completed = set(config.get("onboarding", {}).get("completed_categories", []))
    if category:
        return "complete" if category in completed else "needs_defaults"
    return "complete" if set(ONBOARDING_CATEGORIES).issubset(completed) else "needs_defaults"


def complete_onboarding_category(config: dict[str, Any], category: str, catalog_hash: str) -> None:
    """Persist an explicit default-model decision for one media category."""
    if category not in ONBOARDING_CATEGORIES:
        raise SkillError("ONBOARDING_CATEGORY_INVALID", f"Unsupported onboarding category: {category}")
    onboarding = config.setdefault("onboarding", {})
    completed = list(dict.fromkeys(onboarding.get("completed_categories", [])))
    if category not in completed:
        completed.append(category)
    onboarding.update(
        {
            "version": 1,
            "completed_categories": completed,
            "catalog_hash": catalog_hash,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
    )


def reset_onboarding_category(config: dict[str, Any], category: str) -> None:
    """Require confirmation again after a default is edited or becomes unavailable."""
    onboarding = config.setdefault("onboarding", {})
    onboarding["completed_categories"] = [
        item for item in onboarding.get("completed_categories", []) if item != category
    ]


def public_config(config: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(config)
    key, source = resolve_api_key(required=False)
    result["credential"] = {
        "configured": bool(key),
        "source": source,
        "fingerprint": f"***{key[-4:]}" if key else "",
    }
    return result
