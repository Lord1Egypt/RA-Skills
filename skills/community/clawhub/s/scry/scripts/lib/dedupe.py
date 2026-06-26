"""Near-duplicate detection for SCRY skill."""

import re
from typing import List, Set, Tuple

from .schema import ScryItem

STOPWORDS = frozenset({
    "the", "a", "an", "to", "for", "how", "is", "in", "of", "on",
    "and", "with", "from", "by", "at", "this", "that", "it", "my",
    "your", "i", "me", "we", "you", "what", "are", "do", "can",
    "its", "be", "or", "not", "no", "so", "if", "but", "about",
    "all", "just", "get", "has", "have", "was", "will", "show", "hn",
})


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_ngrams(text: str, n: int = 3) -> Set[str]:
    text = normalize_text(text)
    if len(text) < n:
        return {text}
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def _get_item_text(item: ScryItem) -> str:
    """Get comparable text from an item."""
    text = item.title
    if item.source_id in ("x_twitter", "bluesky", "mastodon", "threads", "tiktok", "instagram"):
        text = text[:100]  # Truncate social posts for fair comparison
    if item.source_id in ("hackernews", "lobsters"):
        for prefix in ("Show HN:", "Ask HN:", "Tell HN:"):
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break
    if item.source_id in ("polymarket",):
        text = f"{item.title} {item.extras.get('question', '')}"
    return text


def _tokenize(text: str) -> Set[str]:
    words = re.sub(r"[^\w\s]", " ", text.lower()).split()
    return {w for w in words if w not in STOPWORDS and len(w) > 1}


def _token_jaccard(text_a: str, text_b: str) -> float:
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def _hybrid_similarity(text_a: str, text_b: str) -> float:
    trigram_sim = jaccard_similarity(get_ngrams(text_a), get_ngrams(text_b))
    token_sim = _token_jaccard(text_a, text_b)
    return max(trigram_sim, token_sim)


def dedupe_items(items: List[ScryItem], threshold: float = 0.7) -> List[ScryItem]:
    """Remove near-duplicates within same source, keeping highest-scored."""
    if len(items) <= 1:
        return items

    ngrams = [get_ngrams(_get_item_text(item)) for item in items]
    to_remove = set()

    for i in range(len(items)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(items)):
            if j in to_remove:
                continue
            if items[i].source_id != items[j].source_id:
                continue
            sim = jaccard_similarity(ngrams[i], ngrams[j])
            if sim >= threshold:
                if items[i].score >= items[j].score:
                    to_remove.add(j)
                else:
                    to_remove.add(i)

    return [item for idx, item in enumerate(items) if idx not in to_remove]


def cross_source_link(items: List[ScryItem], threshold: float = 0.40) -> None:
    """Annotate items with cross-source references. Modifies in-place."""
    if len(items) <= 1:
        return

    texts = [_get_item_text(item) for item in items]

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i].source_id == items[j].source_id:
                continue
            sim = _hybrid_similarity(texts[i], texts[j])
            if sim >= threshold:
                if items[j].id not in items[i].cross_refs:
                    items[i].cross_refs.append(items[j].id)
                if items[i].id not in items[j].cross_refs:
                    items[j].cross_refs.append(items[i].id)
