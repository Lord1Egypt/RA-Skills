#!/usr/bin/env python3
"""Small JSONL run logger for zhizhi-math-coach scripts."""

from __future__ import annotations

import datetime as dt
import json
import time
import uuid
from pathlib import Path
from typing import Any


def new_run_id() -> str:
    return uuid.uuid4().hex[:12]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def append_run_log(workspace: Path, event: dict[str, Any]) -> None:
    path = workspace.resolve() / ".zhizhi-math-coach" / "run-log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"time": now_iso(), **event}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


class Timer:
    def __init__(self) -> None:
        self.started = time.perf_counter()

    def elapsed_ms(self) -> int:
        return int((time.perf_counter() - self.started) * 1000)
