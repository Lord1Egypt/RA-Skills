from __future__ import annotations

from datetime import date, datetime

from .text import normalize_text


DATE_FORMATS = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d.%m.%Y",
    "%m/%d/%Y",
    "%m/%d/%y",
    "%d/%m/%Y",
    "%Y.%m.%d",
)


def parse_date(value: str | date | datetime | None) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    cleaned = normalize_text(value)
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date()
        except ValueError:
            continue
    return None


def normalize_date(value: str | date | datetime | None) -> str | None:
    parsed = parse_date(value)
    return parsed.isoformat() if parsed else (normalize_text(str(value)) if value else None)
