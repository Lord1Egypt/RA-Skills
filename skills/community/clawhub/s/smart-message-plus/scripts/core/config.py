#!/usr/bin/env python3
"""smart-message-plus: config & paths (platform-agnostic).

Data dir resolution priority:
  1. $SMP_DATA_DIR
  2. <agent workspace>/.smart-message/  (first existing workspace dir)
  3. ~/.smart-message/
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

DEFAULT_HTTP_TIMEOUT = 15

DEFAULT_CONFIG = {
    "default_provider": "",
    "http_timeout": DEFAULT_HTTP_TIMEOUT,
    "safety_gate": {
        "enabled": True,
        "warn_threshold": 50,
        "review_threshold": 100,
        "admins": [],  # [{"provider": "dingtalk", "user_id": "..."}]
        "notify_provider": "",
        "code_ttl_minutes": 30,
    },
    "org_lookup": {
        "mode": "builtin",  # builtin | custom
        "custom_url": "",
        "custom_auth_header_env": "SMP_ORG_AUTH",
        "timeout": 10,
    },
}


def data_dir() -> Path:
    env = os.environ.get("SMP_DATA_DIR", "").strip()
    if env:
        p = Path(env).expanduser()
    else:
        p = Path.home() / ".smart-message"
        for ws in (
            Path.home() / ".openclaw" / "workspace",
            Path.home() / ".claude" / "workspace",
            Path.cwd(),
        ):
            if ws.is_dir():
                p = ws / ".smart-message"
                break
    p.mkdir(mode=0o700, parents=True, exist_ok=True)
    return p


def _path(name: str) -> Path:
    return data_dir() / name


def load_json(name: str, default):
    p = _path(name)
    if not p.exists():
        return default
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(name: str, obj, secret: bool = False) -> None:
    """Atomic write (tmp + os.replace). secret=True -> chmod 600."""
    p = _path(name)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        if secret:
            os.chmod(tmp, 0o600)
        os.replace(tmp, p)
        if secret:
            os.chmod(p, 0o600)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_config() -> dict:
    cfg = load_json("config.json", {})
    merged = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    _deep_merge(merged, cfg)
    return merged


def save_config(cfg: dict) -> None:
    save_json("config.json", cfg)


def _deep_merge(base: dict, override: dict) -> None:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def mask_secret(s: str, keep: int = 4) -> str:
    if not s:
        return ""
    if len(s) <= keep:
        return "*" * len(s)
    return s[:keep] + "*" * 8
