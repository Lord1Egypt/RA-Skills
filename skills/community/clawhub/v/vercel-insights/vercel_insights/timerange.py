"""Time parsing, range resolution, granularity translation and bucket rendering.

The time vocabulary here is the *meaning* vocabulary (``hour``, ``day``,
``week``, ``month``, ``year``). The two APIs spell those meanings differently,
and there is no single spelling that satisfies both, so this module owns the
translation: :func:`normalize_granularity` takes what the user typed in either
vocabulary and returns the spelling the named surface uses, or refuses when
that surface has no equivalent.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from . import ConfigError

#: Time buckets. At most one may appear in a single grouping.
TIME_GRANULARITIES: tuple[str, ...] = ("hour", "day", "week", "month", "year")

#: The three query surfaces, spelled as the user facing messages spell them.
WEB_ANALYTICS = "web-analytics"
SPEED_INSIGHTS = "speed-insights"
LOGS = "logs"
SURFACES: tuple[str, ...] = (WEB_ANALYTICS, SPEED_INSIGHTS, LOGS)

#: How a surface is named in prose.
SURFACE_LABELS: dict[str, str] = {
    WEB_ANALYTICS: "Web Analytics",
    SPEED_INSIGHTS: "Speed Insights",
    LOGS: "request logs",
}

#: Every spelling a user may type, mapped to the meaning it names. Both
#: vocabularies are accepted on input, whichever surface is active.
GRANULARITY_ALIASES: dict[str, str] = {
    "hour": "hour",
    "1h": "hour",
    "day": "day",
    "1d": "day",
    "week": "week",
    "month": "month",
    "1mo": "month",
    "year": "year",
}

#: How each meaning is spelled on each surface. ``None`` means that surface has
#: no documented equivalent, which is a configuration error rather than
#: something to translate approximately. LOGS is deliberately absent: that
#: surface has no time buckets at all, ``--granularity`` is rejected before any
#: request is built, and inventing an entry here would imply a translation that
#: does not exist.
GRANULARITY_BY_SURFACE: dict[str, dict[str, str | None]] = {
    WEB_ANALYTICS: {
        "hour": "hour",
        "day": "day",
        "week": "week",
        "month": "month",
        "year": "year",
    },
    SPEED_INSIGHTS: {
        "hour": "1h",
        "day": "1d",
        "week": None,
        "month": "1mo",
        "year": None,
    },
}

#: Accepted ``--granularity`` values, in a sensible reading order.
ACCEPTED_GRANULARITIES: tuple[str, ...] = (
    "hour",
    "1h",
    "day",
    "1d",
    "week",
    "month",
    "1mo",
    "year",
)

#: The reporting window guaranteed by the most generous plan tier.
MAX_REPORTING_WINDOW = timedelta(days=730)

#: Unix milliseconds outside this range cannot become a :class:`datetime`.
MIN_UNIX_MS = -62135596800000  # 0001-01-01T00:00:00Z
MAX_UNIX_MS = 253402300799999  # 9999-12-31T23:59:59.999Z

_RELATIVE_RE = re.compile(r"^(\d+)\s*([mhdw])$", re.IGNORECASE)
_UNIX_MS_RE = re.compile(r"^\d{11,}$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_RELATIVE_UNITS: dict[str, str] = {
    "m": "minutes",
    "h": "hours",
    "d": "days",
    "w": "weeks",
}

TIME_HELP = (
    "accepted forms: a relative offset such as 30m, 24h, 7d or 4w; "
    "now, today or yesterday; an ISO date such as 2026-08-01; an ISO datetime "
    "such as 2026-08-01T12:00:00Z; or Unix milliseconds (11 or more digits)"
)


def parse_time_value(value: str, now: datetime) -> datetime:
    """Turn one ``--since`` or ``--until`` token into an aware UTC datetime.

    Args:
        value: The raw token, for example ``7d``, ``today`` or ``2026-08-01``.
        now: The reference instant relative offsets are measured back from.

    Returns:
        The resolved instant, always timezone aware and in UTC.

    Raises:
        ConfigError: If the token matches none of the documented forms.
    """
    raw = value.strip()
    if not raw:
        raise ConfigError(f"empty time value: {TIME_HELP}")

    reference = now.astimezone(timezone.utc)
    lowered = raw.lower()

    if lowered == "now":
        return reference
    if lowered == "today":
        return reference.replace(hour=0, minute=0, second=0, microsecond=0)
    if lowered == "yesterday":
        midnight = reference.replace(hour=0, minute=0, second=0, microsecond=0)
        return midnight - timedelta(days=1)

    relative = _RELATIVE_RE.match(lowered)
    if relative:
        amount = int(relative.group(1))
        unit = _RELATIVE_UNITS[relative.group(2).lower()]
        return reference - timedelta(**{unit: amount})

    if _UNIX_MS_RE.match(raw):
        return _from_unix_ms(raw)

    if raw.isdigit():
        raise ConfigError(
            f"time value {raw!r} looks like Unix seconds; this option wants Unix "
            f"milliseconds (11 or more digits), so try {raw}000, or use an ISO "
            "date such as 2026-08-01"
        )

    if _ISO_DATE_RE.match(raw):
        try:
            return datetime.strptime(raw, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError as exc:
            raise ConfigError(f"time value {raw!r} is not a real date: {exc}") from exc

    candidate = raw[:-1] + "+00:00" if raw.endswith(("Z", "z")) else raw
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ConfigError(f"unrecognised time value {raw!r}: {TIME_HELP}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _from_unix_ms(raw: str) -> datetime:
    """Convert a Unix millisecond string to an aware UTC datetime.

    A value large enough to fall outside the year 1 to year 9999 range that
    :class:`datetime` can represent raises ``ValueError``, ``OverflowError`` or
    ``OSError`` depending on the platform. All three become a ``ConfigError``
    naming the accepted range, so no traceback ever reaches the user.

    Raises:
        ConfigError: When the value is outside the representable range.
    """
    try:
        milliseconds = int(raw)
    except ValueError as exc:  # pragma: no cover - the regex admits digits only
        raise ConfigError(f"time value {raw!r} is not an integer") from exc
    if MIN_UNIX_MS <= milliseconds <= MAX_UNIX_MS:
        try:
            return datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            pass
    raise ConfigError(
        f"time value {raw!r} is Unix milliseconds outside the representable "
        f"range of {MIN_UNIX_MS} to {MAX_UNIX_MS} (0001-01-01T00:00:00Z to "
        "9999-12-31T23:59:59Z); check the value has not been given in "
        "microseconds or nanoseconds, or use an ISO date such as 2026-08-01"
    )


def resolve_range(since: str, until: str, now: datetime) -> tuple[datetime, datetime]:
    """Resolve both time tokens and check that they describe a real window.

    Args:
        since: The ``--since`` token.
        until: The ``--until`` token.
        now: The reference instant for relative offsets.

    Returns:
        A ``(since, until)`` pair of aware UTC datetimes, strictly ordered.

    Raises:
        ConfigError: If either token is unparseable, or ``since`` is not
            strictly earlier than ``until``.
    """
    start = parse_time_value(since, now)
    end = parse_time_value(until, now)
    if start >= end:
        raise ConfigError(
            f"--since must be strictly earlier than --until, but --since {since!r} "
            f"resolves to {to_api_timestamp(start)} and --until {until!r} resolves "
            f"to {to_api_timestamp(end)}; widen the window, for example "
            "--since 7d --until now"
        )
    return start, end


def to_api_timestamp(dt: datetime) -> str:
    """Render an aware datetime as the UTC ISO-8601 string the API accepts."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def to_unix_ms(dt: datetime) -> str:
    """Render an aware datetime as the Unix millisecond string one API wants.

    The request-logs endpoint takes ``startDate`` and ``endDate`` in
    milliseconds, unlike the two ISO-8601 surfaces, and every query parameter
    this client sends is a string.

    Args:
        dt: The instant to render. A naive value is read as UTC.

    Returns:
        Whole milliseconds since the Unix epoch, as a decimal string.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return str(int(dt.astimezone(timezone.utc).timestamp() * 1000))


def reporting_window_warning(since: datetime, now: datetime) -> str | None:
    """Return a warning when ``since`` predates the longest reporting window.

    The plan tier is not discoverable from this API, so an old ``--since`` is a
    warning rather than an error: the query stays legal and may return data.
    """
    if now.astimezone(timezone.utc) - since.astimezone(timezone.utc) > (
        MAX_REPORTING_WINDOW
    ):
        return (
            f"--since resolves to {to_api_timestamp(since)}, which is more than 24 "
            "months ago; the guaranteed reporting window is 1 month on Hobby, 12 "
            "months on Pro and 24 months on Enterprise, so older buckets may come "
            "back empty"
        )
    return None


def granularity_meaning(value: str) -> str | None:
    """The meaning a granularity spelling names, in either vocabulary."""
    return GRANULARITY_ALIASES.get(value.strip().lower())


def normalize_granularity(value: str, surface: str) -> str:
    """Translate a granularity into the spelling ``surface`` uses.

    Both vocabularies are accepted on input: ``hour`` and ``1h`` mean the same
    thing, and which of the two goes on the wire depends only on the surface
    the query is destined for. A meaning the surface cannot express is refused
    here, before any request is built, rather than sent for the API to reject.

    Args:
        value: What the user typed, for example ``day`` or ``1d``.
        surface: :data:`WEB_ANALYTICS` or :data:`SPEED_INSIGHTS`.

    Returns:
        The spelling for that surface, for example ``day`` or ``1d``.

    Raises:
        ConfigError: When the spelling is not one this client accepts, or the
            surface has no equivalent for it. Both messages name the offending
            value, the surface, and what to use instead.
    """
    spellings = GRANULARITY_BY_SURFACE.get(surface)
    if spellings is None:
        raise ConfigError(
            f"unknown query surface {surface!r}; the surfaces are "
            f"{', '.join(SURFACES)}"
        )

    meaning = granularity_meaning(value)
    if meaning is None:
        raise ConfigError(
            f"unknown granularity {value!r}; this client accepts "
            f"{', '.join(ACCEPTED_GRANULARITIES)}, and translates whichever "
            "spelling you use into the one the target API wants"
        )

    spelling = spellings[meaning]
    if spelling is None:
        supported = [
            f"{name} ({spellings[name]})"
            for name in TIME_GRANULARITIES
            if spellings[name] is not None
        ]
        label = SURFACE_LABELS.get(surface, surface)
        raise ConfigError(
            f"--granularity {value!r} has no equivalent on the {label} surface, "
            f"which buckets only by {', '.join(supported)}; pick one of those, "
            f"or run a Web Analytics preset such as trend, which does support "
            f"{meaning} buckets"
        )
    return spelling


def format_timestamp(value: str, granularity: str | None) -> str:
    """Render an API row timestamp at a sensible precision for its bucket.

    The granularity may arrive in either vocabulary, since the label a result
    carries is the one its own surface uses.
    """
    candidate = value[:-1] + "+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return value
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc)
    meaning = granularity_meaning(granularity) if granularity else None
    if meaning == "hour":
        return parsed.strftime("%Y-%m-%d %H:%M")
    if meaning == "month":
        return parsed.strftime("%Y-%m")
    if meaning == "year":
        return parsed.strftime("%Y")
    if meaning in ("day", "week"):
        return parsed.strftime("%Y-%m-%d")
    return parsed.strftime("%Y-%m-%d %H:%M")
