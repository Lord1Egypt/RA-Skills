"""Normalization: raw API dicts → ScryItem objects."""

from typing import Any, Dict, List

from . import dates
from .schema import Engagement, ScryItem


def normalize_items(
    raw_items: List[Dict[str, Any]],
    source_id: str,
    id_prefix: str,
    from_date: str,
    to_date: str,
) -> List[ScryItem]:
    """Convert raw source dicts into ScryItem objects.

    Each raw dict should have: title, url, date (optional), relevance,
    engagement (optional dict), and any source-specific extras.
    """
    items = []
    for idx, raw in enumerate(raw_items):
        item_id = f"{id_prefix}{idx + 1}"

        # Parse date
        date_str = raw.get("date")
        if date_str and len(date_str) == 8 and date_str.isdigit():
            # YYYYMMDD format (from yt-dlp)
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

        # Date confidence
        confidence = dates.get_date_confidence(date_str, from_date, to_date)

        # Build engagement
        eng_data = raw.get("engagement") or {}
        engagement = Engagement.from_dict(eng_data) if eng_data else None

        # Extract standard fields vs extras
        standard_keys = {
            "title", "url", "date", "relevance", "why_relevant",
            "engagement", "author", "snippet", "tags",
        }
        extras = {k: v for k, v in raw.items() if k not in standard_keys and v is not None}

        item = ScryItem(
            id=item_id,
            source_id=source_id,
            title=raw.get("title") or raw.get("text", ""),
            url=raw.get("url", ""),
            author=raw.get("author", ""),
            date=date_str,
            date_confidence=confidence,
            snippet=raw.get("snippet", ""),
            relevance=float(raw.get("relevance", 0.5)),
            why_relevant=raw.get("why_relevant", ""),
            engagement=engagement,
            tags=raw.get("tags") or [],
            extras=extras,
        )
        items.append(item)

    return items


def filter_by_date(items: List[ScryItem], from_date: str, to_date: str) -> List[ScryItem]:
    """Filter items to only those within date range (keep items with unknown dates)."""
    result = []
    for item in items:
        if not item.date:
            result.append(item)
            continue
        conf = dates.get_date_confidence(item.date, from_date, to_date)
        if conf != "low":
            result.append(item)
        else:
            # Keep it but mark low confidence
            item.date_confidence = "low"
            result.append(item)
    return result
