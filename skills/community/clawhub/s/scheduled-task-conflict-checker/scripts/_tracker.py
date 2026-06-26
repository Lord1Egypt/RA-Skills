#!/usr/bin/env python3
"""scheduled-task-conflict-checker 的本地打点工具。

只记录脚本级运行事件，不采集店铺、商品、订单、用户原始话术等业务敏感内容。
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict


SKILL_NAME = "scheduled-task-conflict-checker"
DEFAULT_TRACK_DIR = Path.home() / ".openclaw" / "workspace" / "skill-telemetry"


def _enabled() -> bool:
    value = os.environ.get("SCHEDULED_TASK_CONFLICT_CHECKER_TRACKING", "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def _track_path() -> Path:
    configured = os.environ.get("SCHEDULED_TASK_CONFLICT_CHECKER_TRACK_PATH")
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_TRACK_DIR / f"{SKILL_NAME}.jsonl"


def emit(event: str, payload: Dict[str, Any] | None = None) -> None:
    """Best-effort JSONL event write; telemetry failure must never affect skill output."""
    if not _enabled():
        return

    record = {
        "ts_ms": int(time.time() * 1000),
        "skill": SKILL_NAME,
        "event": event,
        "payload": payload or {},
    }
    try:
        path = _track_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception:
        return
