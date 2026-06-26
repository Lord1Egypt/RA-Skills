from __future__ import annotations

from datetime import datetime, timezone

from dateutil.parser import isoparse


def parse_sherpadesk_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = isoparse(value)
    except (ValueError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
