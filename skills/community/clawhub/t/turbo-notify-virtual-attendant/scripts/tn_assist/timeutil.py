"""Time helpers. Timestamps stored by the helper are UTC with a ``Z`` suffix, seconds precision."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(text: str) -> datetime:
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
