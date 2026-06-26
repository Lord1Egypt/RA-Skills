"""Optional cross-encoder reranking for retrieval matches.

Off by default. To enable:

1. ``pip install youos[reranker]`` (or directly: ``pip install sentence-transformers``)
2. Set ``reranker_enabled: true`` in ``configs/retrieval/defaults.yaml``

Both gates have to be true: the flag plus the dep. If the flag is on but
the dep is missing (or the model fails to load), ``rerank()`` returns
``(matches, False)`` — original order preserved, the caller sees that
reranking did not actually fire, and the retrieval method label stays
``fts5_bm25[+semantic]`` rather than misleadingly claiming ``+reranker``.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.retrieval.service import RetrievalMatch

logger = logging.getLogger(__name__)

# Default model id — the smallest reasonable cross-encoder for MS-MARCO
# style relevance reranking. Overridable per-call via the `model_id` kwarg
# (config-driven from `retrieval/defaults.yaml`'s `reranker_model_id`).
# Note: only one model gets loaded per process — first non-None call wins
# for caching purposes. Switching models at runtime requires restart.
DEFAULT_RERANKER_MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Default blend between FTS score and cross-encoder score. 0.6 weights the
# CE score 60% / FTS 40% — picked at module-introduction time without
# measurement, so flagged as a tuning surface. Override via
# `retrieval/defaults.yaml`'s `reranker_blend_weight`.
DEFAULT_BLEND_WEIGHT = 0.6

# CE scores fall in roughly [0, 1] (sigmoid-ish output); FTS scores are
# unbounded but typically in [0, 20] after `lexical_cap`. Scale CE up
# before blending so the two halves contribute on comparable scales.
# Hardcoded historically; surfaced for tuning.
DEFAULT_CE_SCORE_SCALE = 10.0

_cross_encoder = None
_load_attempted = False
_loaded_model_id: str | None = None


def _lazy_load_cross_encoder(model_id: str | None = None):
    """Lazy-load the cross-encoder model.

    Returns the encoder, or ``None`` if ``sentence_transformers`` isn't
    installed or model loading fails. Only the first non-default ``model_id``
    is honored — subsequent calls return the already-loaded encoder
    regardless of what model_id they request. This avoids reloading on
    every retrieval call (which would dwarf the latency benefit of any
    reranker).

    A change to ``reranker_model_id`` in config takes effect on next
    process restart, not at runtime.
    """
    global _cross_encoder, _load_attempted, _loaded_model_id
    if _load_attempted:
        return _cross_encoder
    _load_attempted = True
    resolved = (model_id or "").strip() or DEFAULT_RERANKER_MODEL_ID
    try:
        from sentence_transformers import CrossEncoder

        _cross_encoder = CrossEncoder(resolved)
        _loaded_model_id = resolved
        logger.info("Cross-encoder loaded: %s", resolved)
    except ImportError:
        logger.warning(
            "sentence_transformers not installed — cross-encoder reranking "
            "disabled. Install with: pip install youos[reranker]"
        )
    except Exception as exc:
        logger.warning("Failed to load cross-encoder %r: %s", resolved, exc)
    return _cross_encoder


def loaded_model_id() -> str | None:
    """Return the model id of the loaded cross-encoder, or None if not loaded.

    Lets the stats/doctor surface report which model is actually live (vs.
    what the config claims) — important when those drift.
    """
    return _loaded_model_id


def rerank(
    query: str,
    matches: list[RetrievalMatch],
    top_n: int,
    *,
    blend_weight: float | None = None,
    ce_score_scale: float | None = None,
    model_id: str | None = None,
) -> tuple[list[RetrievalMatch], bool]:
    """Rerank matches using cross-encoder. Returns ``(matches, applied)``.

    ``applied`` is True only when the cross-encoder actually produced
    scores and the matches were re-sorted. False when the encoder isn't
    loadable (no dep, no disk space, model not found) or when
    ``encoder.predict`` raises mid-call. The caller uses this to keep
    the ``retrieval_method`` label honest — silently falling back to
    original order would otherwise mislead anyone reading the trace.

    Mutates the score attribute of the returned matches to blend FTS and
    CE scores (FTS * (1-w) + CE_scaled * w). Original input list order is
    not preserved on the returned slice — that's the point of reranking.
    """
    encoder = _lazy_load_cross_encoder(model_id=model_id)
    if encoder is None or not matches:
        return matches, False

    w = DEFAULT_BLEND_WEIGHT if blend_weight is None else float(blend_weight)
    scale = DEFAULT_CE_SCORE_SCALE if ce_score_scale is None else float(ce_score_scale)

    pairs = []
    for match in matches:
        text = match.snippet or match.content or match.inbound_text or ""
        pairs.append((query, text))

    try:
        scores = encoder.predict(pairs)
    except Exception as exc:
        logger.warning("Cross-encoder prediction failed: %s", exc)
        return matches, False

    scored = list(zip(matches, scores, strict=False))
    scored.sort(key=lambda x: -x[1])

    reranked = [m for m, _ in scored[:top_n]]
    for match, ce_score in scored[:top_n]:
        match.score = round(match.score * (1.0 - w) + float(ce_score) * scale * w, 4)

    return reranked, True


def is_reranker_available(model_id: str | None = None) -> bool:
    """True if the cross-encoder can be loaded.

    Side-effect: triggers the lazy load on first call. Used by the doctor
    check (`youos doctor`) to surface a warning when ``reranker_enabled``
    is True in config but the dep isn't installed — without this, the
    silent fallback would let the user think reranking is firing when
    nothing is being reranked.
    """
    return _lazy_load_cross_encoder(model_id=model_id) is not None
