"""Query expansion via synonym injection for FTS retrieval."""

from __future__ import annotations

SYNONYMS: dict[str, list[str]] = {
    "schedule": ["meeting", "call", "sync", "calendar", "appointment"],
    "postpone": ["reschedule", "delay", "move", "push back", "shift"],
    "urgent": ["asap", "immediately", "critical", "priority", "time-sensitive"],
    "proposal": ["offer", "quote", "pitch", "suggestion"],
    "confirm": ["approve", "sign off", "green light", "authorize"],
    "update": ["status", "progress", "news", "latest"],
    "issue": ["problem", "bug", "error", "concern"],
    "team": ["colleagues", "staff", "group", "members"],
}

# Build reverse lookup: word -> synonym group key
_WORD_TO_GROUP: dict[str, str] = {}
for _key, _syns in SYNONYMS.items():
    _WORD_TO_GROUP[_key] = _key
    for _syn in _syns:
        # Only map single words (skip multi-word synonyms for tokenization)
        if " " not in _syn:
            _WORD_TO_GROUP[_syn] = _key


def expand_query(text: str, max_expansions: int = 3) -> str:
    """Expand query with synonym groups.

    Finds words in text that have synonyms and appends up to max_expansions
    synonym groups as: 'text synonym1 synonym2'. The synonyms are appended bare
    (no 'also:' label) — the label tokenized into the FTS query and the word
    'also' polluted BM25 ranking.
    Caps total expansion at 50 extra chars.
    """
    if not text:
        return text

    words = text.lower().split()
    seen_groups: set[str] = set()
    expansion_parts: list[str] = []

    for word in words:
        clean = word.strip(",.!?;:")
        group_key = _WORD_TO_GROUP.get(clean)
        if group_key and group_key not in seen_groups:
            seen_groups.add(group_key)
            # Get single-word synonyms only, exclude the original word
            syns = [s for s in SYNONYMS[group_key] if " " not in s and s != clean]
            if syns:
                expansion_parts.append(" ".join(syns[:3]))
            if len(expansion_parts) >= max_expansions:
                break

    if not expansion_parts:
        return text

    expansion = " ".join(expansion_parts)
    if len(expansion) > 50:
        expansion = expansion[:50].rsplit(" ", 1)[0]

    return f"{text} {expansion}"
