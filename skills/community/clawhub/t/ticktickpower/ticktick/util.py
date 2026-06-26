import re
from datetime import datetime, timedelta


def is_task_id(s: str) -> bool:
    """Return True if s looks like a TickTick task ID (24-char hex)."""
    return bool(re.fullmatch(r"[a-f0-9]{24}", s, re.IGNORECASE))


def parse_due_date(due_str: str) -> str:
    """Parse a human-readable date string into a TickTick ISO datetime string.

    TickTick expects: "2026-01-07T23:59:59.000+0000"
    """
    lower = due_str.lower().strip()

    def end_of_day(d: datetime) -> str:
        eod = d.replace(hour=23, minute=59, second=59, microsecond=0)
        return eod.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    now = datetime.now()

    if lower == "today":
        return end_of_day(now)

    if lower == "tomorrow":
        return end_of_day(now + timedelta(days=1))

    m = re.match(r"^in (\d+) days?$", lower)
    if m:
        return end_of_day(now + timedelta(days=int(m.group(1))))

    # "next <weekday>" — JS uses Sunday=0, Python uses Monday=0
    JS_DAYS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    m = re.match(r"^next (sunday|monday|tuesday|wednesday|thursday|friday|saturday)$", lower)
    if m:
        js_index = JS_DAYS.index(m.group(1))
        # Convert JS index (sun=0) to Python weekday (mon=0): python = (js - 1) % 7
        python_target = (js_index - 1) % 7
        current = now.weekday()
        days_until = (python_target - current) % 7
        if days_until == 0:
            days_until = 7
        return end_of_day(now + timedelta(days=days_until))

    # Try ISO parse (Python 3.11+ handles full ISO 8601 with offsets)
    try:
        parsed = datetime.fromisoformat(due_str)
        # Strip tzinfo for strftime; preserve the literal offset in output
        return parsed.strftime("%Y-%m-%dT%H:%M:%S.000+0000")
    except ValueError:
        pass

    raise ValueError(
        f"Invalid date format: {due_str!r}. "
        "Try 'today', 'tomorrow', 'in 3 days', 'next monday', or ISO date."
    )
