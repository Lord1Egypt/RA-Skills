"""Simple text similarity utilities for auto-feedback capture."""

from __future__ import annotations

from difflib import SequenceMatcher


def similarity_ratio(a: str, b: str) -> float:
    """Returns 0.0 (completely different) to 1.0 (identical)."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def token_similarity(a: str, b: str) -> float:
    """Word-level Jaccard similarity (intersection / union of word sets, lowercased)."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a and not words_b:
        return 1.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 1.0


def hybrid_similarity(a: str, b: str) -> float:
    """Blend of sequence similarity and token-level Jaccard (50/50)."""
    return 0.5 * similarity_ratio(a, b) + 0.5 * token_similarity(a, b)


def is_meaningfully_different(draft: str, actual: str, threshold: float = 0.80) -> bool:
    """True if draft and actual differ enough to be a useful training pair."""
    return hybrid_similarity(draft, actual) < threshold
