"""Shared query extraction utilities for SCRY skill.

This replaces the duplicated _extract_core_subject() that last30days
has copied across 7 modules.
"""

import re
from typing import List

NOISE_PREFIXES = [
    "what are the best", "what is the best", "what are people saying about",
    "what's happening with", "tell me about", "how to use", "how do i",
    "tips for using", "guide to", "last 7 days", "last 30 days",
    "last 90 days", "latest on", "best practices for", "how is",
    "what do people think about", "why is", "who is", "where to find",
    "recommendations for", "top rated",
]

NOISE_SUFFIXES = [
    "best practices", "use cases", "tips and tricks", "prompt techniques",
    "in 2026", "in 2025", "reddit", "review", "alternatives",
]

NOISE_WORDS = frozenset({
    "best", "top", "trending", "popular", "latest", "new", "good",
    "great", "awesome", "amazing", "recommended", "favorite",
    "prompts", "techniques", "strategies", "methods", "practices",
})


def extract_core_subject(topic: str, max_words: int = 3) -> str:
    """Extract the core subject from a research query.

    Strips noise prefixes, suffixes, and filler words to get
    the 2-3 word core subject for API queries.
    """
    text = topic.strip().lower()

    for prefix in sorted(NOISE_PREFIXES, key=len, reverse=True):
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break

    for suffix in sorted(NOISE_SUFFIXES, key=len, reverse=True):
        if text.endswith(suffix):
            text = text[:-len(suffix)].strip()
            break

    words = text.split()
    words = [w for w in words if w not in NOISE_WORDS and len(w) > 1]

    if not words:
        return topic.strip()[:50]

    return " ".join(words[:max_words])


def build_search_variants(topic: str, max_variants: int = 3) -> List[str]:
    """Build search query variants from a topic.

    Returns the original topic plus simplified variants for retry.
    """
    core = extract_core_subject(topic)
    words = core.split()
    variants = [core]

    if len(words) > 2:
        variants.append(" ".join(words[:2]))
    if len(words) > 1:
        strongest = max(words, key=len)
        if strongest != core:
            variants.append(strongest)

    return variants[:max_variants]


def extract_keywords(topic: str) -> List[str]:
    """Extract individual keywords from topic for relevance matching."""
    text = topic.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    words = text.split()
    stopwords = frozenset({
        "the", "a", "an", "to", "for", "how", "is", "in", "of", "on",
        "and", "with", "from", "by", "at", "this", "that", "it", "my",
        "your", "i", "me", "we", "you", "what", "are", "do", "can",
        "its", "be", "or", "not", "no", "so", "if", "but", "about",
    })
    return [w for w in words if w not in stopwords and len(w) > 1]


SYNONYMS = {
    "js": "javascript", "ts": "typescript", "py": "python",
    "react": "reactjs", "reactjs": "react",
    "vue": "vuejs", "vuejs": "vue",
    "ml": "machine learning", "ai": "artificial intelligence",
    "llm": "large language model", "dl": "deep learning",
    "k8s": "kubernetes", "tf": "tensorflow",
    "gpt": "chatgpt", "claude": "anthropic",
}


def compute_relevance(topic: str, text: str) -> float:
    """Compute relevance score (0.0-1.0) via token overlap with synonym expansion."""
    topic_kw = set(extract_keywords(topic))
    expanded = set()
    for kw in topic_kw:
        expanded.add(kw)
        if kw in SYNONYMS:
            expanded.add(SYNONYMS[kw])

    text_kw = set(extract_keywords(text))
    if not expanded or not text_kw:
        return 0.0

    matches = len(expanded & text_kw)
    return min(1.0, matches / max(len(expanded), 1))
