#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _router_command(skill_root: Path) -> str:
    router = (skill_root / "scripts" / "host_executor_router.py").resolve()
    return f"python3 {router} --input {{input}} --output {{output}}"


def build_router_executor_defaults(skill_root: str | Path) -> dict[str, str]:
    root = Path(skill_root).resolve()
    command = _router_command(root)
    return {
        "WOTOHUB_HOST_ANALYSIS_EXECUTOR": command,
        "WOTOHUB_HOST_REPLY_ANALYSIS_EXECUTOR": command,
        "WOTOHUB_HOST_DRAFT_EXECUTOR": command,
    }


def ensure_router_executor_env(*, skill_root: str | Path, env: Optional[dict[str, str]] = None) -> dict[str, str]:
    base = dict(env or os.environ)
    defaults = build_router_executor_defaults(skill_root)
    for key, value in defaults.items():
        base.setdefault(key, value)
    return base
