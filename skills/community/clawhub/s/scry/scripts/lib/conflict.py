"""Cross-source conflict detection for SCRY skill."""

import re
from typing import Any, Dict, List

from .schema import ScryItem

NEGATION_WORDS = frozenset({
    "not", "no", "never", "neither", "nobody", "nothing", "nowhere",
    "doesn't", "don't", "didn't", "won't", "can't", "shouldn't",
    "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't",
    "failed", "fails", "failing", "decline", "declined", "falling",
    "dropped", "crash", "crashed", "worst", "terrible", "horrible",
})

POSITIVE_WORDS = frozenset({
    "best", "great", "excellent", "amazing", "fantastic", "wonderful",
    "success", "successful", "growing", "rising", "surging", "booming",
    "breakthrough", "revolutionary", "impressive", "outstanding",
})


def _extract_sentiment(text: str) -> str:
    """Simple sentiment: 'positive', 'negative', or 'neutral'."""
    words = set(re.sub(r"[^\w\s]", " ", text.lower()).split())
    neg_count = len(words & NEGATION_WORDS)
    pos_count = len(words & POSITIVE_WORDS)
    if neg_count > pos_count and neg_count >= 2:
        return "negative"
    if pos_count > neg_count and pos_count >= 2:
        return "positive"
    return "neutral"


def _extract_numbers(text: str) -> List[float]:
    """Extract numeric values (prices, percentages, counts)."""
    nums = re.findall(r"\$?([\d,]+\.?\d*)\s*(%|million|billion|M|B|K)?", text)
    result = []
    for val, unit in nums:
        try:
            n = float(val.replace(",", ""))
            if unit == "%":
                n = n / 100
            elif unit in ("million", "M"):
                n *= 1_000_000
            elif unit in ("billion", "B"):
                n *= 1_000_000_000
            elif unit == "K":
                n *= 1_000
            result.append(n)
        except ValueError:
            continue
    return result


def detect_conflicts(items: List[ScryItem]) -> List[Dict[str, Any]]:
    """Detect conflicts between cross-referenced items.

    Looks for:
    1. Opposing sentiments on the same topic across sources
    2. Contradictory numbers/claims
    """
    conflicts = []

    # Only check items that have cross-references
    xref_items = [item for item in items if item.cross_refs]

    for item in xref_items:
        for ref_id in item.cross_refs:
            ref_item = next((i for i in items if i.id == ref_id), None)
            if not ref_item:
                continue

            # Already processed this pair in reverse
            if item.id > ref_id:
                continue

            text_a = f"{item.title} {item.snippet}"
            text_b = f"{ref_item.title} {ref_item.snippet}"

            sent_a = _extract_sentiment(text_a)
            sent_b = _extract_sentiment(text_b)

            if sent_a != "neutral" and sent_b != "neutral" and sent_a != sent_b:
                conflicts.append({
                    "type": "sentiment",
                    "item_a": item.id,
                    "item_b": ref_item.id,
                    "source_a": item.source_id,
                    "source_b": ref_item.source_id,
                    "detail": f"{item.source_id} is {sent_a}, {ref_item.source_id} is {sent_b}",
                    "title": item.title[:80],
                })

    return conflicts
