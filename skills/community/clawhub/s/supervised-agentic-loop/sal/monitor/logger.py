"""Tool-call JSONL logger — append-only, sanitized.

Logs all agent tool calls to daily JSONL files.
Every entry passes through sanitize_args() before writing (🔴 Dr. Neuron).
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sal.monitor.sanitizer import sanitize_args


def _default_state_dir() -> str:
    return os.environ.get("MONITOR_STATE_DIR", ".state")


class ToolCallLogger:
    """Append-only JSONL logger for tool calls.

    File per day: tool-call-log-YYYY-MM-DD.jsonl
    """

    def __init__(self, state_dir: Optional[str] = None) -> None:
        self.state_dir = Path(state_dir or _default_state_dir())
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _log_path(self, date: Optional[datetime] = None) -> Path:
        """Get log file path for a given date."""
        dt = date or datetime.now(timezone.utc)
        return self.state_dir / f"tool-call-log-{dt.strftime('%Y-%m-%d')}.jsonl"

    def log(
        self,
        agent_id: str,
        session_id: str,
        tool: str,
        args: dict,
        result_code: int = 0,
        duration_ms: int = 0,
    ) -> dict:
        """Log a single tool call.

        Args:
            agent_id: Agent identifier.
            session_id: Session identifier.
            tool: Tool name (exec, write, edit, browser, read).
            args: Raw tool arguments — will be sanitized.
            result_code: Exit/status code.
            duration_ms: Execution time in ms.

        Returns:
            The sanitized log entry dict.
        """
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "session_id": session_id,
            "tool": tool,
            "args": sanitize_args(args),
            "result_code": result_code,
            "duration_ms": duration_ms,
        }

        path = self._log_path()
        with open(path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def read_session(
        self, session_id: str, date: Optional[datetime] = None
    ) -> list[dict]:
        """Read all entries for a session from today's log."""
        path = self._log_path(date)
        if not path.exists():
            return []

        entries = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("session_id") == session_id:
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
        return entries

    def read_recent(self, limit: int = 100, date: Optional[datetime] = None) -> list[dict]:
        """Read most recent N entries from today's log."""
        path = self._log_path(date)
        if not path.exists():
            return []

        entries = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return entries[-limit:]

    def count_today(self) -> int:
        """Count entries in today's log."""
        path = self._log_path()
        if not path.exists():
            return 0
        with open(path) as f:
            return sum(1 for line in f if line.strip())
