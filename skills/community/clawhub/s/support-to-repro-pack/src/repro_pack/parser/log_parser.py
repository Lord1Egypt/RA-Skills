"""Multi-format log parser."""

from __future__ import annotations

import json
import re

from ..models import LogEntry, LogFormat
from .formats import detect_file_format

# Common timestamp patterns
_TS_PATTERNS = [
    # ISO 8601: 2024-03-25T14:02:11.123Z
    re.compile(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)"),
    # Syslog: Mar 25 14:02:11
    re.compile(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d{2}:\d{2}:\d{2})"),
    # Simple: 14:02:11 or 2024/03/25 14:02:11
    re.compile(r"(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})"),
    re.compile(r"(\d{2}:\d{2}:\d{2}(?:\.\d+)?)"),
]

# Log level pattern
_LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL|TRACE)\b",
    re.IGNORECASE,
)


def _extract_timestamp(text: str) -> str | None:
    for pat in _TS_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def _extract_level(text: str) -> str | None:
    m = _LEVEL_PATTERN.search(text)
    return m.group(1).upper() if m else None


def parse_json_line(line: str, line_number: int) -> LogEntry:
    """Parse a JSON log line."""
    try:
        data = json.loads(line)
    except (json.JSONDecodeError, ValueError):
        return LogEntry(message=line.strip(), raw=line, line_number=line_number)

    ts = data.get("timestamp") or data.get("time") or data.get("ts") or data.get("@timestamp")
    level = data.get("level") or data.get("severity") or data.get("log.level")
    msg = data.get("message") or data.get("msg") or data.get("log") or str(data)
    source = data.get("source") or data.get("logger") or data.get("name")

    return LogEntry(
        timestamp=str(ts) if ts else None,
        level=str(level).upper() if level else None,
        message=str(msg),
        source=str(source) if source else None,
        raw=line,
        line_number=line_number,
    )


def parse_plain_line(line: str, line_number: int) -> LogEntry:
    """Parse a plaintext log line."""
    return LogEntry(
        timestamp=_extract_timestamp(line),
        level=_extract_level(line),
        message=line.strip(),
        raw=line,
        line_number=line_number,
    )


def parse_syslog_line(line: str, line_number: int) -> LogEntry:
    """Parse a syslog-format line."""
    # <priority>Month Day HH:MM:SS hostname process[pid]: message
    m = re.match(
        r"(?:<\d+>)?"
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d{2}:\d{2}:\d{2})\s+"
        r"(\S+)\s+"  # hostname
        r"(\S+?)(?:\[\d+\])?:\s+"  # process
        r"(.*)",
        line,
    )
    if m:
        return LogEntry(
            timestamp=m.group(1),
            level=_extract_level(m.group(4)),
            message=m.group(4),
            source=f"{m.group(2)}/{m.group(3)}",
            raw=line,
            line_number=line_number,
        )
    return parse_plain_line(line, line_number)


def parse_log(text: str) -> list[LogEntry]:
    """Parse a multi-line log file into structured entries."""
    fmt = detect_file_format(text)

    parser_fn = {
        LogFormat.JSON: parse_json_line,
        LogFormat.SYSLOG: parse_syslog_line,
        LogFormat.PLAIN: parse_plain_line,
        LogFormat.UNKNOWN: parse_plain_line,
    }[fmt]

    entries = []
    for i, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        entries.append(parser_fn(line, i))
    return entries
