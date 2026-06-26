"""Date utilities for SCRY skill."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def get_date_range(days: int = 30) -> Tuple[str, str]:
    today = datetime.now(timezone.utc).date()
    from_date = today - timedelta(days=days)
    return from_date.isoformat(), today.isoformat()


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        ts = float(date_str)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (ValueError, TypeError):
        pass
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y%m%d",
        "%d %b %Y",
        "%B %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def timestamp_to_date(ts: Optional[float]) -> Optional[str]:
    if ts is None:
        return None
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.date().isoformat()
    except (ValueError, TypeError, OSError):
        return None


def get_date_confidence(date_str: Optional[str], from_date: str, to_date: str) -> str:
    if not date_str:
        return "low"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        start = datetime.strptime(from_date, "%Y-%m-%d").date()
        end = datetime.strptime(to_date, "%Y-%m-%d").date()
        if start <= dt <= end:
            return "high"
        return "low"
    except ValueError:
        return "low"


def days_ago(date_str: Optional[str]) -> Optional[int]:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now(timezone.utc).date()
        return (today - dt).days
    except ValueError:
        return None


def recency_score(date_str: Optional[str], max_days: int = 30) -> int:
    age = days_ago(date_str)
    if age is None:
        return 0
    if age < 0:
        return 100
    if age >= max_days:
        return 0
    return int(100 * (1 - age / max_days))
