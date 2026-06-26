"""Domain-aware scoring for SCRY skill."""

import math
from typing import List

from . import dates
from .domain import get_source_weight
from .schema import Engagement, ScryItem, SubScores

WEIGHT_RELEVANCE = 0.45
WEIGHT_RECENCY = 0.25
WEIGHT_ENGAGEMENT = 0.30


def _log1p(x):
    return math.log1p(max(0, x or 0))


def compute_engagement_raw(eng: Engagement, source_id: str) -> float:
    """Compute raw engagement score based on source type."""
    if eng is None:
        return 0.0

    if source_id in ("reddit",):
        return (0.55 * _log1p(eng.score) +
                0.40 * _log1p(eng.num_comments) +
                0.05 * (eng.upvote_ratio or 0.5) * 10)

    if source_id in ("x_twitter", "bluesky", "mastodon", "threads"):
        return (0.55 * _log1p(eng.likes) +
                0.25 * _log1p(eng.reposts) +
                0.15 * _log1p(eng.replies) +
                0.05 * _log1p(eng.quotes))

    if source_id in ("youtube", "tiktok", "instagram"):
        return (0.50 * _log1p(eng.views) +
                0.35 * _log1p(eng.likes) +
                0.15 * _log1p(eng.num_comments))

    if source_id in ("hackernews", "lobsters"):
        return (0.55 * _log1p(eng.score) +
                0.45 * _log1p(eng.num_comments))

    if source_id in ("github", "gitlab"):
        return (0.50 * _log1p(eng.stars) +
                0.35 * _log1p(eng.forks) +
                0.15 * _log1p(eng.num_comments))

    if source_id in ("polymarket",):
        return (0.60 * _log1p(eng.volume) +
                0.40 * _log1p(eng.liquidity))

    if source_id in ("arxiv", "semantic_scholar", "openalex"):
        return (0.70 * _log1p(eng.citations) +
                0.30 * _log1p(eng.downloads))

    if source_id in ("devto", "stackoverflow"):
        return (0.50 * _log1p(eng.score) +
                0.30 * _log1p(eng.num_comments) +
                0.20 * _log1p(eng.likes))

    if source_id in ("huggingface",):
        return (0.50 * _log1p(eng.downloads) +
                0.30 * _log1p(eng.likes) +
                0.20 * _log1p(eng.stars))

    if source_id in ("coingecko",):
        return (0.60 * _log1p(eng.volume) +
                0.40 * _log1p(eng.score))

    if source_id in ("product_hunt",):
        return (0.60 * _log1p(eng.score) +
                0.40 * _log1p(eng.num_comments))

    # Fallback for sources with no engagement data
    return 0.0


def normalize_to_100(values: List[float]) -> List[int]:
    """Min-max normalize values to 0-100 scale."""
    if not values:
        return []
    mn, mx = min(values), max(values)
    rng = mx - mn
    if rng == 0:
        return [50] * len(values)
    return [int(100 * (v - mn) / rng) for v in values]


def score_items(items: List[ScryItem], domain: str = "general", max_days: int = 30) -> List[ScryItem]:
    """Score all items with domain-aware weights."""
    if not items:
        return items

    # Compute raw engagement scores
    raw_eng = [compute_engagement_raw(item.engagement, item.source_id) for item in items]
    norm_eng = normalize_to_100(raw_eng)

    for i, item in enumerate(items):
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date, max_days)
        eng_score = norm_eng[i]

        base = (WEIGHT_RELEVANCE * rel_score +
                WEIGHT_RECENCY * rec_score +
                WEIGHT_ENGAGEMENT * eng_score)

        # Domain source weight multiplier
        multiplier = get_source_weight(item.source_id, domain)
        adjusted = base * multiplier

        # Penalties
        if item.engagement is None:
            adjusted -= 3
        if item.date_confidence == "low":
            adjusted -= 5
        elif item.date_confidence == "med":
            adjusted -= 2

        # Extra penalty for web/substack sources without engagement
        if item.source_id in ("websearch", "substack", "google_news", "techmeme", "wikipedia"):
            if item.engagement is None:
                adjusted -= 10

        item.subs = SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=eng_score,
        )
        item.score = max(0, min(100, int(adjusted)))

    return items


def sort_items(items: List[ScryItem]) -> List[ScryItem]:
    """Sort items by score descending, then date descending."""
    source_priority = {
        "reddit": 0, "x_twitter": 1, "bluesky": 2, "hackernews": 3,
        "lobsters": 4, "youtube": 5, "github": 6, "devto": 7,
        "stackoverflow": 8, "tiktok": 9, "instagram": 10,
        "product_hunt": 11, "huggingface": 12, "threads": 13,
        "mastodon": 14, "arxiv": 15, "semantic_scholar": 16,
        "openalex": 17, "polymarket": 18, "coingecko": 19,
        "sec_edgar": 20, "gdelt": 21, "techmeme": 22,
        "wikipedia": 23, "gitlab": 24, "substack": 25,
        "google_news": 26, "websearch": 27,
    }

    def sort_key(item):
        date_val = item.date or "0000-00-00"
        return (-item.score, date_val, source_priority.get(item.source_id, 99))

    items.sort(key=sort_key)
    return items
