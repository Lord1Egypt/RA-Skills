from __future__ import annotations

import json
from typing import Any

from toupiaoya.constants import CONFIG_PATH, CONFIG_TOKEN_KEY


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.is_file():
        return {}
    try:
        raw = CONFIG_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_config(data: dict[str, Any]) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass


def token_from_config(cfg: dict[str, Any]) -> str:
    v = cfg.get(CONFIG_TOKEN_KEY) or cfg.get("x_openclaw_token")
    return (v if isinstance(v, str) else str(v or "")).strip()
