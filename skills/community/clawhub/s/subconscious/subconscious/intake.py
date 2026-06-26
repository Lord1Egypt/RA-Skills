"""Conservative candidate extraction from turns and tool results.

Very lightweight — does not do heavy NLP or embedding-based extraction.
Focuses on explicit signals and simple patterns.
"""

import re
from datetime import datetime, timezone
from typing import Optional

from .schema import Item, ItemKind, ItemLayer, ItemSource, ItemLinks, ItemReinforcement


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def extract_candidates(turn_context: dict) -> list[Item]:
    """Extract candidate items from a turn context.

    Args:
        turn_context: Dict with keys like:
            - user_message: str
            - assistant_reply: str
            - tool_results: list of compacted results
            - session_id: str
            - project: str (optional)

    Returns:
        List of candidate items (not yet validated)
    """
    candidates = []
    session_id = turn_context.get("session_id", "unknown")
    project = turn_context.get("project")

    # Extract from user message
    user_msg = turn_context.get("user_message", "")
    candidates.extend(_extract_from_text(user_msg, "conversation", session_id, project))

    # Extract from tool results if present
    for result in turn_context.get("tool_results", []):
        if isinstance(result, str):
            candidates.extend(_extract_from_text(result, "observation", session_id, project))

    # Simple explicit signals
    candidates.extend(_extract_explicit_signals(user_msg, session_id, project))

    return candidates


def _extract_from_text(text: str, source_type: str, session_id: str, project: Optional[str]) -> list[Item]:
    """Extract candidates from free text using simple heuristics."""
    candidates = []

    # Pattern: "Edward prefers X" -> preference
    pref_matches = re.findall(r'(?:Edward|user) (?:prefers?|likes?|wants?) ([^.]+)', text, re.IGNORECASE)
    for match in pref_matches:
        candidates.append(_create_item(
            ItemKind.PREFERENCE,
            f"User prefers: {match.strip()}",
            source_type,
            session_id,
            confidence=0.75,
            project=project,
        ))

    # Pattern: "I should remember X" or "remember that X"
    remember_matches = re.findall(r'(?:remember|note) (?:that )?([^.]+)', text, re.IGNORECASE)
    for match in remember_matches:
        candidates.append(_create_item(
            ItemKind.CONTEXT,
            f"Note: {match.strip()}",
            source_type,
            session_id,
            confidence=0.7,
            project=project,
        ))

    # Pattern: "This might be X" -> hypothesis
    hypo_matches = re.findall(r'(?:this|that|it) might be ([^.]+)', text, re.IGNORECASE)
    for match in hypo_matches:
        candidates.append(_create_item(
            ItemKind.HYPOTHESIS,
            f"Hypothesis: {match.strip()}",
            source_type,
            session_id,
            confidence=0.6,
            project=project,
        ))

    return candidates


def _extract_explicit_signals(text: str, session_id: str, project: Optional[str]) -> list[Item]:
    """Extract from explicit signals like #project, @person, etc."""
    candidates = []

    # Extract projects from #tags
    project_tags = re.findall(r'#(\w+)', text)
    for tag in project_tags:
        candidates.append(_create_item(
            ItemKind.PROJECT,
            f"Active project: {tag}",
            "observation",
            session_id,
            confidence=0.8,
            project=tag,
        ))

    return candidates


def _create_item(
    kind: ItemKind,
    text: str,
    source_type: str,
    session_id: str,
    confidence: float,
    project: Optional[str] = None,
) -> Item:
    """Create a pending item."""
    timestamp = _utc_now()
    item_id = f"subc_pending_{_hash_id(text)}"

    links = ItemLinks()
    if project:
        links.projects.append(project)

    return Item(
        id=item_id,
        layer=ItemLayer.PENDING,
        kind=kind,
        text=text[:500],  # truncate
        weight=0.5,
        confidence=confidence,
        freshness=1.0,
        source=ItemSource(type=source_type, session=session_id, timestamp=timestamp),
        links=links,
        reinforcement=ItemReinforcement(count=1, first_at=timestamp, last_at=timestamp),
    )


def _hash_id(text: str) -> str:
    """Simple hash for ID generation."""
    import hashlib
    return hashlib.md5(text.encode()).hexdigest()[:12]


def queue_pending(candidate: Item, base_path=None) -> bool:
    """Queue a candidate to pending store.

    Args:
        candidate: Item to queue
        base_path: Optional override for storage path

    Returns:
        True if queued, False if already exists/similar
    """
    from .store import append_event, DEFAULT_BASE_PATH
    from .retrieve import is_duplicate

    base = base_path or DEFAULT_BASE_PATH

    # Check for duplicates/similar items
    if is_duplicate(candidate, base):
        return False

    # Append to pending queue
    append_event("candidate_queued", candidate.to_dict(), base_path=base)
    return True
