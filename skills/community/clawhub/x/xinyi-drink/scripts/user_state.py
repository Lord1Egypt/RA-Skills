#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
import os
from pathlib import Path


STATE_FILE_MODE = 0o600


def resolve_state_file() -> Path:
    configured = os.getenv("XINYI_DRINK_STATE_FILE")
    if configured:
        return Path(configured).expanduser()

    return Path.home() / ".xinyi-drink" / "state.json"


def load_state() -> dict:
    state_file = resolve_state_file()
    if not state_file.exists():
        return {}

    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def write_state(payload: dict) -> None:
    state_file = resolve_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(state_file, STATE_FILE_MODE)
    except OSError:
        pass


def save_activity_state(mobile: str, activity_joined: bool) -> None:
    payload = {
        "mobile": mobile,
        "activityJoined": activity_joined,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    write_state(payload)


def mark_activity_joined(mobile: str) -> None:
    save_activity_state(mobile, True)


def mark_activity_not_joined(mobile: str) -> None:
    save_activity_state(mobile, False)


def load_activity_joined(mobile: str | None) -> bool | None:
    if not mobile:
        return None

    payload = load_state()
    if payload.get("mobile") != mobile:
        return None

    value = payload.get("activityJoined")
    return value if isinstance(value, bool) else None


def clear_mobile() -> None:
    payload = {
        "mobile": None,
        "activityJoined": None,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }
    write_state(payload)


def load_mobile() -> str | None:
    value = load_state().get("mobile")
    return value if isinstance(value, str) and value.strip() else None
