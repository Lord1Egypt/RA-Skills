"""Voice-match scoring — how closely a draft resembles the user's *actual* reply.

The existing rule-based scores (keyword hit-rate, brevity, mode) measure whether
a draft is structurally acceptable. They do *not* measure the thing YouOS exists
to do: sound like **you**. Voice-match compares a candidate draft against the real
reply the user sent to the same inbound message (the "reference"), so we can tell
whether a model — a Qwen fine-tuned on your mail vs. a generic cloud model — is
actually reproducing your voice rather than just writing a plausible email.

This is the metric that makes a cross-model comparison meaningful: a frontier
cloud model will usually win the structural scores, but the question that decides
whether the privacy/cost trade is worth it is "does it sound more like me than my
own fine-tuned local model?" — and only voice-match answers that.

Design:
  * The core is **deterministic and dependency-free** (lexical overlap, length fit,
    greeting/closing match, stylometry) so it runs anywhere and in CI without a
    model download.
  * An optional **semantic** component uses an injected embedding function (e.g.
    ``app.core.embeddings.get_embedding``) when one is available, so the metric
    degrades gracefully on machines without the model loaded.

All sub-scores are in ``[0, 1]`` (higher = closer to the reference). The combined
``voice_match`` is a weighted blend of whichever components are available.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from difflib import SequenceMatcher
from typing import Any

# Reuse the generation layer's greeting/closing vocabulary so "has a greeting"
# means the same thing here as it does when drafting/repairing.
from app.generation.service import _CLOSING_TOKENS, _GREETING_TOKENS

_WORD_RE = re.compile(r"[A-Za-z0-9']+")
_SENT_RE = re.compile(r"[.!?]+")
_CONTRACTION_RE = re.compile(r"\b\w+'(t|re|ll|ve|m|s|d)\b", re.IGNORECASE)


def _tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def _sentences(text: str) -> list[str]:
    return [s for s in (p.strip() for p in _SENT_RE.split(text)) if s]


def _lexical_overlap(draft: str, reference: str) -> float:
    """Surface word-sequence overlap (0–1) via difflib's ratio.

    Catches reused phrasing — the user's stock openers, sign-offs and turns of
    phrase that a model trained on their mail reproduces but a generic model
    paraphrases away.
    """
    a, b = _tokens(draft), _tokens(reference)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _length_ratio(draft: str, reference: str) -> float:
    """How close the draft's length is to the reference's (1.0 = identical)."""
    a, b = len(_tokens(draft)), len(_tokens(reference))
    if a == 0 and b == 0:
        return 1.0
    if a == 0 or b == 0:
        return 0.0
    return min(a, b) / max(a, b)


def _first_line(text: str) -> str:
    return text.lstrip().split("\n", 1)[0].strip().lower()


def _tail(text: str) -> str:
    return "\n".join(text.rstrip().splitlines()[-3:]).lower()


def _has_greeting(text: str) -> bool:
    first = _first_line(text)
    return bool(first) and any(first.startswith(tok) for tok in _GREETING_TOKENS)


def _has_closing(text: str) -> bool:
    tail = _tail(text)
    return bool(tail) and any(tok in tail for tok in _CLOSING_TOKENS)


def _bool_match(a: bool, b: bool) -> float:
    """1.0 when both texts agree on a structural habit, else 0.0."""
    return 1.0 if a == b else 0.0


def _style_features(text: str) -> dict[str, float]:
    """A small, robust stylometric fingerprint of a reply.

    These are surface habits that survive paraphrase and identify a writer:
    sentence length, word length, how often they contract, how often they ask or
    exclaim. Each is later compared between draft and reference.
    """
    toks = _tokens(text)
    sents = _sentences(text)
    n_tokens = len(toks) or 1
    n_sents = len(sents) or 1
    return {
        "avg_sentence_len": len(toks) / n_sents,
        "avg_word_len": sum(len(t) for t in toks) / n_tokens,
        "contraction_rate": len(_CONTRACTION_RE.findall(text)) / n_tokens,
        "question_rate": text.count("?") / n_sents,
        "exclaim_rate": text.count("!") / n_sents,
    }


# Per-feature scale used to normalise an absolute difference into a 0–1 penalty.
# Roughly "a difference this large means the styles are unrelated on this axis".
_STYLE_SCALE = {
    "avg_sentence_len": 12.0,
    "avg_word_len": 2.5,
    "contraction_rate": 0.15,
    "question_rate": 1.0,
    "exclaim_rate": 1.0,
}


def _style_similarity(draft: str, reference: str) -> float:
    """Stylometric closeness (0–1), blending fingerprint features with the
    greeting/closing habit match."""
    if not draft.strip() or not reference.strip():
        return 0.0
    fa, fb = _style_features(draft), _style_features(reference)
    sims: list[float] = []
    for key, scale in _STYLE_SCALE.items():
        diff = abs(fa[key] - fb[key])
        sims.append(max(0.0, 1.0 - diff / scale))
    # Fold in whether the two share the greeting / sign-off habit.
    sims.append(_bool_match(_has_greeting(draft), _has_greeting(reference)))
    sims.append(_bool_match(_has_closing(draft), _has_closing(reference)))
    return sum(sims) / len(sims)


def _semantic_similarity(
    draft: str,
    reference: str,
    embed_fn: Callable[[str], Sequence[float]],
    cosine_fn: Callable[[Sequence[float], Sequence[float]], float] | None,
) -> float | None:
    """Cosine similarity of embeddings — "did it say the same thing".

    Returns ``None`` (rather than raising) if embedding fails, so a missing model
    downgrades the metric to its deterministic components instead of breaking the
    whole comparison run.
    """
    if not draft.strip() or not reference.strip():
        return 0.0
    try:
        if cosine_fn is None:
            from app.core.embeddings import cosine_similarity as cosine_fn  # noqa: PLC0415
        va, vb = embed_fn(draft), embed_fn(reference)
        return max(0.0, min(1.0, float(cosine_fn(va, vb))))
    except Exception:
        return None


# Weights when the semantic component is available vs. deterministic-only. They
# sum to 1.0 within each branch so the combined score stays in [0, 1].
_WEIGHTS_WITH_SEMANTIC = {"semantic": 0.45, "style": 0.25, "lexical": 0.20, "length": 0.10}
_WEIGHTS_NO_SEMANTIC = {"style": 0.45, "lexical": 0.35, "length": 0.20}


def voice_match_score(
    draft: str,
    reference: str,
    *,
    embed_fn: Callable[[str], Sequence[float]] | None = None,
    cosine_fn: Callable[[Sequence[float], Sequence[float]], float] | None = None,
) -> dict[str, Any]:
    """Score how closely ``draft`` matches the user's real ``reference`` reply.

    Returns a dict of sub-scores plus a combined ``voice_match`` (all 0–1, higher
    is closer). Pass ``embed_fn`` (e.g. ``app.core.embeddings.get_embedding``) to
    include the semantic component; without it the score uses the deterministic
    components only and ``semantic_similarity`` is ``None``.
    """
    lexical = _lexical_overlap(draft, reference)
    length = _length_ratio(draft, reference)
    style = _style_similarity(draft, reference)

    semantic: float | None = None
    if embed_fn is not None:
        semantic = _semantic_similarity(draft, reference, embed_fn, cosine_fn)

    if semantic is not None:
        w = _WEIGHTS_WITH_SEMANTIC
        combined = w["semantic"] * semantic + w["style"] * style + w["lexical"] * lexical + w["length"] * length
    else:
        w = _WEIGHTS_NO_SEMANTIC
        combined = w["style"] * style + w["lexical"] * lexical + w["length"] * length

    return {
        "voice_match": round(combined, 3),
        "semantic_similarity": round(semantic, 3) if semantic is not None else None,
        "lexical_overlap": round(lexical, 3),
        "style_similarity": round(style, 3),
        "length_ratio": round(length, 3),
        "greeting_match": _bool_match(_has_greeting(draft), _has_greeting(reference)) == 1.0,
        "closing_match": _bool_match(_has_closing(draft), _has_closing(reference)) == 1.0,
    }
