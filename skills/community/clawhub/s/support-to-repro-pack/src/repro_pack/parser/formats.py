"""Auto-detect log format."""

from __future__ import annotations

import json

from ..models import LogFormat


def detect_format(line: str) -> LogFormat:
    """Detect the format of a single log line."""
    stripped = line.strip()
    if not stripped:
        return LogFormat.UNKNOWN

    # Try JSON
    if stripped.startswith("{"):
        try:
            json.loads(stripped)
            return LogFormat.JSON
        except (json.JSONDecodeError, ValueError):
            pass

    # Syslog: starts with month or timestamp like "Mar 25" or "<134>"
    import re
    syslog_pattern = re.compile(
        r"^(?:<\d+>)?"  # optional priority
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+"  # month day
    )
    if syslog_pattern.match(stripped):
        return LogFormat.SYSLOG

    return LogFormat.PLAIN


def detect_file_format(text: str) -> LogFormat:
    """Detect the predominant format of a log file by sampling first non-empty lines."""
    counts: dict[LogFormat, int] = {}
    for line in text.splitlines()[:20]:
        if not line.strip():
            continue
        fmt = detect_format(line)
        counts[fmt] = counts.get(fmt, 0) + 1

    if not counts:
        return LogFormat.UNKNOWN

    return max(counts, key=lambda k: counts[k])
