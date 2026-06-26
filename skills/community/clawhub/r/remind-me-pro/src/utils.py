from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones


def format_timestamp_ms(ts_ms: int | None) -> str:
    """Format a millisecond epoch timestamp into a human-readable UTC string."""
    if ts_ms is None:
        return "N/A"
    try:
        return datetime.utcfromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M:%S UTC")
    except (TypeError, ValueError, OSError):
        return "N/A"


def format_schedule(schedule: dict) -> str:
    """Format a cron job schedule dict into a readable string."""
    if not schedule:
        return "N/A"

    kind = schedule.get("kind", "")

    if kind == "at":
        raw = schedule.get("at", "")
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return f"Once at {dt.strftime('%Y-%m-%d %H:%M UTC')}"
        except Exception:
            return f"Once at {raw}"

    if kind == "every":
        return f"Every {schedule.get('every', 'N/A')}"

    if kind == "cron":
        return f"Cron: {schedule.get('expr', 'N/A')}"

    return str(schedule)


def format_status_icon(status: str | None) -> str:
    """Map a last-run status string to a display icon."""
    if status == "ok":
        return "✅"
    if status == "error":
        return "❌"
    if status is None:
        return "⏳"
    return "⚠️"


def build_channel_tag(channel: str, to: str) -> str:
    """Build a scoping tag embedded in job descriptions for channel-based filtering.

    Format: [remind-me:<channel>:<chatId>]
    """
    return f"[remind-me:{channel}:{to}]"


def parse_schedule_arg(schedule: str) -> tuple[str, str]:
    """Parse a prefixed schedule string into (kind, value).

    Accepts: every:<duration> | cron:<expr> | at:<duration>
    Returns a tuple of (kind, value) or raises ValueError.
    """
    if ":" not in schedule:
        raise ValueError(
            f"Invalid schedule '{schedule}'. "
            "Expected: every:<duration>, cron:<expr>, or at:<duration>"
        )
    kind, _, value = schedule.partition(":")
    return kind.strip().lower(), value.strip()


def is_valid_iana_timezone(tz: str) -> bool:
    """Return True if the given string is a valid IANA timezone identifier.

    Uses zoneinfo.available_timezones() for a fast set lookup, with a
    fallback ZoneInfo() construction to catch edge-cases not in the set.
    """
    if not tz or not isinstance(tz, str):
        return False
    if tz in available_timezones():
        return True
    try:
        ZoneInfo(tz)
        return True
    except (ZoneInfoNotFoundError, KeyError):
        return False


def normalize_timezone(tz: str | None, fallback: str = "UTC") -> str:
    """Return a validated IANA timezone string, falling back to UTC if invalid.

    Strips whitespace and performs a case-insensitive best-effort match
    for common aliases (e.g. 'london' -> 'Europe/London').
    """
    if not tz:
        return fallback

    tz = tz.strip()

    if is_valid_iana_timezone(tz):
        return tz

    # Common short aliases that users or the AI might pass
    _ALIASES: dict[str, str] = {
        "utc": "UTC",
        "gmt": "GMT",
        "est": "America/New_York",
        "cst": "America/Chicago",
        "mst": "America/Denver",
        "pst": "America/Los_Angeles",
        "ist": "Asia/Kolkata",
        "cet": "Europe/Paris",
        "eet": "Europe/Helsinki",
        "aest": "Australia/Sydney",
        "jst": "Asia/Tokyo",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "berlin": "Europe/Berlin",
        "moscow": "Europe/Moscow",
        "dubai": "Asia/Dubai",
        "lagos": "Africa/Lagos",
        "nairobi": "Africa/Nairobi",
        "new york": "America/New_York",
        "los angeles": "America/Los_Angeles",
        "chicago": "America/Chicago",
        "toronto": "America/Toronto",
        "sydney": "Australia/Sydney",
        "tokyo": "Asia/Tokyo",
        "singapore": "Asia/Singapore",
        "shanghai": "Asia/Shanghai",
        "beijing": "Asia/Shanghai",
        "mumbai": "Asia/Kolkata",
        "karachi": "Asia/Karachi",
        "jakarta": "Asia/Jakarta",
        "cairo": "Africa/Cairo",
        "johannesburg": "Africa/Johannesburg",
        "sao paulo": "America/Sao_Paulo",
        "mexico city": "America/Mexico_City",
    }

    resolved = _ALIASES.get(tz.lower())
    if resolved:
        return resolved

    return fallback


def format_timezone_label(tz: str) -> str:
    """Return a display-friendly label for a timezone, including current UTC offset.

    Example: 'Europe/Lagos' -> 'Africa/Lagos (UTC+1)'
    """
    try:
        now = datetime.now(tz=ZoneInfo(tz))
        offset = now.utcoffset()
        if offset is None:
            return tz
        total_minutes = int(offset.total_seconds() // 60)
        sign = "+" if total_minutes >= 0 else "-"
        hours, mins = divmod(abs(total_minutes), 60)
        offset_str = (
            f"UTC{sign}{hours}" if mins == 0 else f"UTC{sign}{hours}:{mins:02d}"
        )
        return f"{tz} ({offset_str})"
    except Exception:
        return tz
