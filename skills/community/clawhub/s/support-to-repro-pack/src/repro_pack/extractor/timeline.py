"""Build event timeline from parsed log entries."""

from __future__ import annotations

import re

from ..models import LogEntry, TimelineEvent


# Interesting event patterns (things worth highlighting in a timeline)
_EVENT_PATTERNS = [
    (re.compile(r"(?:error|exception|fail|crash|panic|fatal)", re.IGNORECASE), "error"),
    (re.compile(r"(?:timeout|timed?\s*out|deadline)", re.IGNORECASE), "timeout"),
    (re.compile(r"(?:connect|disconnect|connection\s+(?:lost|reset|refused))", re.IGNORECASE), "connection"),
    (re.compile(r"(?:request|response|HTTP|API\s+call)", re.IGNORECASE), "request"),
    (re.compile(r"(?:login|logout|auth|token|session)", re.IGNORECASE), "auth"),
    (re.compile(r"(?:deploy|restart|shutdown|startup|boot)", re.IGNORECASE), "lifecycle"),
    (re.compile(r"(?:retry|retrying|attempt\s+\d)", re.IGNORECASE), "retry"),
    (re.compile(r"(?:OOM|out\s+of\s+memory|memory\s+limit|heap)", re.IGNORECASE), "memory"),
    (re.compile(r"(?:queue|enqueue|dequeue|backlog|backpressure)", re.IGNORECASE), "queue"),
]


def _classify_event(message: str) -> str | None:
    """Return event category if the message is 'interesting'."""
    for pattern, category in _EVENT_PATTERNS:
        if pattern.search(message):
            return category
    return None


def build_timeline(
    entries: list[LogEntry],
    include_all: bool = False,
) -> list[TimelineEvent]:
    """Build an event timeline from log entries.

    Args:
        entries: Parsed log entries.
        include_all: If True, include all entries. If False, only interesting events.

    Returns:
        Sorted list of timeline events.
    """
    events: list[TimelineEvent] = []

    for entry in entries:
        if not entry.timestamp:
            continue

        category = _classify_event(entry.message)

        if include_all or category is not None:
            # Truncate long messages
            msg = entry.message.strip()
            if len(msg) > 200:
                msg = msg[:197] + "..."

            events.append(
                TimelineEvent(
                    timestamp=entry.timestamp,
                    event=msg,
                    source=entry.source,
                    level=entry.level or category,
                )
            )

    # Sort by timestamp string (works for ISO 8601 and most formats)
    events.sort(key=lambda e: e.timestamp)
    return events


def timeline_to_markdown(events: list[TimelineEvent]) -> str:
    """Render timeline as a markdown table."""
    if not events:
        return "No timeline events found."

    lines = [
        "| Timestamp | Level | Event |",
        "|-----------|-------|-------|",
    ]
    for ev in events:
        level = ev.level or "-"
        lines.append(f"| {ev.timestamp} | {level} | {ev.event} |")
    return "\n".join(lines)
