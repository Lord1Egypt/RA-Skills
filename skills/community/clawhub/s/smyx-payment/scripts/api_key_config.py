#!/usr/bin/env python3
"""apiKey local storage and stub notice helpers.

Rules:
- Only process apiKey returned by cloud order creation.
- Compare with workspace data/smyx-api-key.txt.
- If missing or different: write/overwrite smyx-api-key.txt and return a one-time stub notice payload.
- If the same value already exists: do not return plaintext to avoid repeated sensitive display.
- Never read or write skills/smyx_common/scripts/config.yaml.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional


def extract_api_key(value: Any) -> Optional[str]:
    """Recursively extract apiKey/api-key/api_key from an order response."""
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).replace("_", "").replace("-", "").lower()
            if normalized == "apikey" and item:
                return str(item).strip()
        for item in value.values():
            found = extract_api_key(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = extract_api_key(item)
            if found:
                return found
    return None


def workspace_root() -> Path:
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if env_workspace:
        return Path(env_workspace)
    # /root/.openclaw/workspace/skills/smyx_payment/scripts/api_key_config.py -> workspace root = parents[3]
    return Path(__file__).resolve().parents[3]


def api_key_file_path() -> Path:
    """The only local storage path for apiKey."""
    return workspace_root() / "data" / "smyx-api-key.txt"


def read_stored_api_key() -> Optional[str]:
    path = api_key_file_path()
    if not path.exists():
        return None
    try:
        value = path.read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return value or None


def persist_new_api_key_if_needed(api_key: Optional[str]) -> dict:
    """Compare and write apiKey to workspace data/smyx-api-key.txt if needed.

    Returns:
        {
          "has_api_key": bool,
          "changed": bool,
          "reason": "first"|"changed"|"same"|"missing",
          "path": str,
          "api_key": str|None,  # only returned when changed=True for one-time stub notice
        }
    """
    path = api_key_file_path()
    if not api_key:
        return {
            "has_api_key": False,
            "changed": False,
            "reason": "missing",
            "path": str(path),
            "api_key": None,
        }

    old_api_key = read_stored_api_key()
    if old_api_key == api_key:
        return {
            "has_api_key": True,
            "changed": False,
            "reason": "same",
            "path": str(path),
            "api_key": None,
        }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(api_key.strip() + "\n", encoding="utf-8")

    return {
        "has_api_key": True,
        "changed": True,
        "reason": "first" if not old_api_key else "changed",
        "path": str(path),
        "api_key": api_key,
    }


def print_api_key_stub_notice(info: dict) -> None:
    """Print prominent Markdown stub notice only when first/changed."""
    if not info.get("changed") or not info.get("api_key"):
        return

    api_key = info.get("api_key")

    print()
    print(f"# ⚠️ **重要：您的 ApiKey 为：`{api_key}`**")
    print()
    print("## **请务必复制存根，以免遗失。**")
    print()
