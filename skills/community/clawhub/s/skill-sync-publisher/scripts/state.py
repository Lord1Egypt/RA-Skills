from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLATFORMS = (
    "github",
    "awesome-codex-plugins",
    "hol",
    "skills.sh",
    "skillsmp",
    "lobehub",
    "clawhub",
    "cursor-directory",
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def state_path() -> Path:
    override = os.environ.get("SKILL_SYNC_STATE")
    return Path(override).expanduser() if override else Path.home() / ".codex" / "skill-sync" / "state.json"


def load() -> dict[str, Any]:
    path = state_path()
    if not path.exists():
        return {"version": 1, "skills": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot read state file {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("skills", {}), dict):
        raise RuntimeError(f"invalid state file {path}")
    return data


def save(data: dict[str, Any]) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="state-", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def get_record(data: dict[str, Any], key: str) -> dict[str, Any]:
    return data.setdefault("skills", {}).setdefault(key, {"platforms": {}})


def update_platform(data: dict[str, Any], key: str, platform: str, **values: Any) -> None:
    record = get_record(data, key)
    record.setdefault("platforms", {}).setdefault(platform, {}).update(values)
