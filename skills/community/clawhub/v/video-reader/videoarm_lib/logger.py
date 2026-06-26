"""VideoARM logging — structured, file-backed analysis tracing.

Every tool call gets logged to:
  ~/.videoarm/logs/YYYY-MM-DD.jsonl   (structured, machine-readable)
  ~/.videoarm/logs/YYYY-MM-DD.log     (human-readable)

Each analysis session gets a unique session_id for end-to-end tracing.
"""

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from videoarm_lib.config import PROJECT_ROOT

LOG_DIR = PROJECT_ROOT / "logs"


def _ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _get_session_id() -> str:
    """Get or create a session ID from environment."""
    sid = os.environ.get("VIDEOARM_SESSION_ID")
    if not sid:
        sid = uuid.uuid4().hex[:12]
        os.environ["VIDEOARM_SESSION_ID"] = sid
    return sid


def get_logger(name: str) -> logging.Logger:
    """Get a logger with file + stderr handlers.
    
    Human-readable logs go to ~/.videoarm/logs/YYYY-MM-DD.log
    Stderr gets minimal output (warnings+).
    """
    _ensure_log_dir()
    logger = logging.getLogger(f"videoarm.{name}")

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # File handler — human-readable, all levels
    today = datetime.now().strftime("%Y-%m-%d")
    fh = logging.FileHandler(LOG_DIR / f"{today}.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    ))
    logger.addHandler(fh)

    # Stderr handler — warnings only (don't pollute CLI JSON output)
    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(logging.WARNING)
    sh.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(sh)

    return logger


def log_event(
    tool: str,
    event: str,
    data: Optional[Dict[str, Any]] = None,
    level: str = "info",
    session_id: Optional[str] = None,
):
    """Append a structured JSONL event to the daily log.

    Args:
        tool: Tool name (e.g. "scene", "analyze-clip", "audio")
        event: Event type (e.g. "start", "api_call", "result", "error")
        data: Arbitrary payload
        level: Log level string
        session_id: Override session id (auto-generated if not set)
    """
    _ensure_log_dir()
    sid = session_id or _get_session_id()
    today = datetime.now().strftime("%Y-%m-%d")

    record = {
        "ts": datetime.now().isoformat(),
        "session_id": sid,
        "tool": tool,
        "event": event,
        "level": level,
        "data": data or {},
    }

    log_path = LOG_DIR / f"{today}.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Also write to the text logger
    logger = get_logger(tool)
    msg = f"[{sid}] {event}"
    if data:
        # Truncate large values for readability
        summary = {k: (str(v)[:200] + "..." if len(str(v)) > 200 else v)
                   for k, v in data.items()}
        msg += f" | {json.dumps(summary, ensure_ascii=False)}"

    log_fn = getattr(logger, level, logger.info)
    log_fn(msg)


class ToolTracer:
    """Context manager for tracing a single tool invocation.
    
    Usage:
        with ToolTracer("scene", video="test.mp4", ranges=[...]) as t:
            # do work
            t.log("api_call", model="gpt-4o", frames=30)
            result = ...
            t.set_result(result)
    """

    def __init__(self, tool: str, **params):
        self.tool = tool
        self.session_id = _get_session_id()
        self.trace_id = uuid.uuid4().hex[:8]
        self.params = params
        self.start_time = None
        self.result = None
        self.error = None

    def __enter__(self):
        self.start_time = time.time()
        log_event(
            self.tool, "start",
            data={"trace_id": self.trace_id, **self.params},
            session_id=self.session_id,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = round(time.time() - self.start_time, 2)
        if exc_val:
            self.error = str(exc_val)
            log_event(
                self.tool, "error",
                data={
                    "trace_id": self.trace_id,
                    "error": self.error,
                    "elapsed_sec": elapsed,
                },
                level="error",
                session_id=self.session_id,
            )
        else:
            result_summary = self.result
            if isinstance(result_summary, dict):
                # Don't log huge blobs
                result_summary = {
                    k: (f"<{len(str(v))} chars>" if len(str(v)) > 500 else v)
                    for k, v in result_summary.items()
                }
            log_event(
                self.tool, "done",
                data={
                    "trace_id": self.trace_id,
                    "elapsed_sec": elapsed,
                    "result": result_summary,
                },
                session_id=self.session_id,
            )
        return False  # don't suppress exceptions

    def log(self, event: str, **data):
        """Log an intermediate event."""
        log_event(
            self.tool, event,
            data={"trace_id": self.trace_id, **data},
            session_id=self.session_id,
        )

    def set_result(self, result):
        """Store result for the exit log."""
        self.result = result
