"""Naive-Bayes phishing scorer with Graham's combination formula.

The model (JSON) carries per-token `p_phish = P(phish|token)` learned from
a labeled corpus. Inference: pick the top-N tokens in the email whose
p_phish is furthest from 0.5, then combine:

    phish_prob = Π p_i / (Π p_i + Π (1 - p_i))

Returns a score in [0.0, 1.0] plus the tokens that contributed, so the
agent can cite them in user-facing alerts.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

from bs4 import BeautifulSoup

# Tokenizer — shared between this module and the trainer
_WORD_RE = re.compile(r"[a-z]+")

STOPWORDS = frozenset({
    "the", "and", "or", "to", "of", "a", "an", "in", "for", "is", "it",
    "on", "at", "by", "be", "as", "this", "that", "with", "you", "your",
    "are", "was", "were", "i", "we", "he", "she", "they", "them", "my",
    "me", "if", "so", "do", "does", "did", "not", "no", "yes", "but",
    "have", "has", "had", "from", "our", "us", "will", "would", "can",
    "could", "should", "been", "being", "there", "their",
})


def tokenize(text: str) -> list[str]:
    """Normalize + tokenize email text. Must match trainer tokenization."""
    if not text:
        return []
    # strip HTML if present
    if "<" in text and ">" in text:
        try:
            text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
        except Exception:
            pass
    text = text.lower()
    tokens = _WORD_RE.findall(text)
    return [t for t in tokens if len(t) > 2 and t not in STOPWORDS]


def load_model(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open() as fh:
        return json.load(fh)


def classify(
    text: str,
    model: dict,
    top_n: int = 15,
) -> tuple[float, list[tuple[str, float]]]:
    """Return (phish_probability, [(token, p_phish), ...]).

    Unknown tokens are ignored (no OOV smoothing at inference — the trainer
    applies Laplace smoothing so every known token already has defined p).
    If no known tokens are present, returns 0.5 (neutral).
    """
    tokens = tokenize(text)
    vocab = model.get("tokens", {})

    known: list[tuple[str, float]] = []
    seen: set[str] = set()
    for t in tokens:
        if t in seen:
            continue
        entry = vocab.get(t)
        if entry is None:
            continue
        seen.add(t)
        known.append((t, float(entry["p_phish"])))

    if not known:
        return 0.5, []

    # Pick the top-N most discriminating
    known.sort(key=lambda tp: abs(tp[1] - 0.5), reverse=True)
    top = known[:top_n]

    # Graham's combined probability
    prod_p = math.prod(p for _, p in top)
    prod_not_p = math.prod(1.0 - p for _, p in top)
    denom = prod_p + prod_not_p
    if denom == 0.0:
        return 0.5, top

    return prod_p / denom, top
