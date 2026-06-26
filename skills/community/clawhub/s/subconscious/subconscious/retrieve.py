"""Simple relevance scoring and retrieval from core/live stores.

Uses keyword overlap + link matching + weights. No embeddings in v1.5.
"""

from typing import Optional

from .schema import Item, ItemLayer
from .store import load


def fetch_relevant(context: dict, limit: int = 5, min_confidence: float = 0.7, base_path = None) -> list[Item]:
    """Fetch relevant items from core and live stores.

    Args:
        context: Dict with keys like:
            - query: str (the text to match against)
            - project: str (current project)
            - topics: list[str]
        limit: Max items to return
        min_confidence: Minimum confidence threshold
        base_path: Optional override for storage path

    Returns:
        List of relevant items, sorted by score
    """
    from .store import DEFAULT_BASE_PATH

    query = context.get("query", "")
    project = context.get("project")
    topics = context.get("topics", [])
    base = base_path or DEFAULT_BASE_PATH

    # Load all items
    core_items = [Item.from_dict(d) for d in load("core", base)]
    live_items = [Item.from_dict(d) for d in load("live", base)]
    all_items = core_items + live_items

    # Score and filter
    scored = []
    for item in all_items:
        # Skip low confidence
        if item.confidence < min_confidence:
            continue

        # Skip archived
        if item.status.value == "archived":
            continue

        score = _score_item(item, query, project, topics)
        if score > 0:
            scored.append((score, item))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Return top N
    return [item for _, item in scored[:limit]]


def _score_item(item: Item, query: str, project: Optional[str], topics: list) -> float:
    """Score an item for relevance."""
    score = 0.0

    # Weight and confidence baseline
    score += item.weight * 0.3
    score += item.confidence * 0.2
    score += item.freshness * 0.1

    # Keyword overlap with query
    if query:
        query_words = set(query.lower().split())
        item_words = set(item.text.lower().split())
        overlap = len(query_words & item_words)
        score += (overlap / max(len(query_words), 1)) * 0.2

    # Project match
    if project and project in item.links.projects:
        score += 0.15

    # Topic match
    for topic in topics:
        if topic in item.links.topics:
            score += 0.05

    return score


def score_item(item: Item, context: dict) -> float:
    """Public scoring function for a single item."""
    query = context.get("query", "")
    project = context.get("project")
    topics = context.get("topics", [])
    return _score_item(item, query, project, topics)


def is_duplicate(candidate: Item, base_path=None) -> bool:
    """Check if a similar or identical item already exists.

    Uses two strategies:
    1. ID match — exact match means the same learning was already ingested
    2. Text similarity — catches items with substantially similar content
    """
    from difflib import SequenceMatcher
    from .store import DEFAULT_BASE_PATH

    base = base_path or DEFAULT_BASE_PATH

    # Collect all items from all layers
    all_items = load("core", base) + load("live", base)

    # Also check pending.jsonl — extract item data from event records
    pending_records = load("pending", base)
    for record in pending_records:
        item_data = record.get("data", {}) if isinstance(record, dict) else record
        all_items.append(item_data)

    # Strategy 1: exact ID match — prevents re-queuing the same learning
    candidate_id = candidate.id
    for item_data in all_items:
        if item_data.get("id") == candidate_id:
            return True

    # Strategy 2: text similarity — catches content drift
    candidate_text = candidate.text.lower()
    for item_data in all_items:
        existing_text = item_data.get("text", "").lower()
        if not existing_text:
            continue
        similarity = SequenceMatcher(None, candidate_text, existing_text).ratio()
        if similarity > 0.85:
            return True

    return False
