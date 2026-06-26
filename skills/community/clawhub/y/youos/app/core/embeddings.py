"""Local semantic embeddings using MLX + Qwen2.5 mean pooling.

Zero new dependencies — reuses the mlx_lm / transformers stack already present.
Embeddings are optional at runtime; the system falls back to FTS5-only retrieval.
"""

from __future__ import annotations

import functools
import math
import struct
from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from app.core.config import get_base_model

# Module-level singleton for lazy model loading
_model = None
_tokenizer = None


def get_embedding_model_id() -> str:
    """Identifier of the model used to produce embeddings.

    Today this is the LoRA base (e.g. ``Qwen/Qwen2.5-1.5B-Instruct``), but
    surfacing it as a function lets us:

    - record which model produced each stored embedding (so a future swap
      can detect and re-embed stale rows), and
    - let users override it via the ``embeddings.model_id`` config key
      without having to change the LoRA base.
    """
    from app.core.config import load_config

    cfg = load_config() or {}
    emb_cfg = cfg.get("embeddings", {}) if isinstance(cfg, dict) else {}
    override = emb_cfg.get("model_id") if isinstance(emb_cfg, dict) else None
    if isinstance(override, str) and override.strip():
        return override.strip()
    return get_base_model()


def _load_model():
    """Lazy-load the Qwen model and tokenizer for embedding generation."""
    global _model, _tokenizer
    if _model is not None:
        return _model, _tokenizer
    try:
        import mlx.core as mx  # noqa: F401
        from mlx_lm import load
    except ImportError as exc:
        raise RuntimeError("mlx_lm is required for embedding generation. Install with: pip install mlx-lm") from exc

    model_id = get_embedding_model_id()
    _model, _tokenizer = load(model_id)
    return _model, _tokenizer


@functools.lru_cache(maxsize=512)
def get_embedding(text: str) -> tuple[float, ...]:
    """Generate a normalized embedding for *text* using mean-pooled Qwen hidden states.

    Returns a tuple (hashable) for lru_cache compatibility.
    """
    import mlx.core as mx

    model, tokenizer = _load_model()
    tokens = tokenizer.encode(text, return_tensors=None)
    if not tokens:
        # Empty text — return zero vector of expected dimension
        dim = model.model.embed_tokens.weight.shape[1]
        return tuple([0.0] * dim)

    input_ids = mx.array([tokens])
    hidden = model.model(input_ids)  # (1, seq_len, hidden_dim)

    # Mean pool over sequence length
    embedding = mx.mean(hidden, axis=1).squeeze(0)  # (hidden_dim,)

    # L2-normalize
    norm = mx.sqrt(mx.sum(embedding * embedding))
    norm = mx.maximum(norm, mx.array(1e-12))
    embedding = embedding / norm

    return tuple(embedding.tolist())


def get_embedding_cache_info() -> dict[str, int]:
    """Return cache stats for get_embedding."""
    info = get_embedding.cache_info()
    return {"hits": info.hits, "misses": info.misses, "size": info.currsize}


def clear_embedding_cache() -> None:
    """Clear the embedding LRU cache."""
    get_embedding.cache_clear()


def get_embedding_batch(texts: list[str]) -> list[tuple[float, ...]]:
    """Generate embeddings for a batch of texts in a single forward pass.

    Uses MLX batched inference when possible; falls back to sequential
    per-item processing if batching fails (e.g. variable-length tokens).
    """
    if not texts:
        return []

    # Check cache first — return immediately if all cached
    results: list[tuple[float, ...] | None] = [None] * len(texts)
    uncached_indices: list[int] = []
    for i, t in enumerate(texts):
        # Attempt cache hit via the existing lru_cache function
        try:
            # lru_cache lookup: call the function, it will hit cache if available
            results[i] = get_embedding(t)
        except Exception:
            uncached_indices.append(i)

    # All cached
    if not uncached_indices:
        return [r for r in results if r is not None]

    # Batch the uncached texts through MLX in one forward pass
    try:
        import mlx.core as mx

        model, tokenizer = _load_model()
        uncached_texts = [texts[i] for i in uncached_indices]

        # Tokenize all texts
        token_lists = [tokenizer.encode(t, return_tensors=None) for t in uncached_texts]

        # Pad to max length for batched inference
        max_len = max((len(tl) for tl in token_lists), default=1)
        padded = [tl + [tokenizer.pad_token_id or 0] * (max_len - len(tl)) for tl in token_lists]
        input_ids = mx.array(padded)  # (batch, seq_len)

        hidden = model.model(input_ids)  # (batch, seq_len, hidden_dim)

        for j, orig_idx in enumerate(uncached_indices):
            tl_len = len(token_lists[j])
            if tl_len == 0:
                dim = model.model.embed_tokens.weight.shape[1]
                emb_tuple = tuple([0.0] * dim)
            else:
                # Mean pool only over non-padded tokens
                emb = mx.mean(hidden[j, :tl_len, :], axis=0)
                norm = mx.sqrt(mx.sum(emb * emb))
                norm = mx.maximum(norm, mx.array(1e-12))
                emb = emb / norm
                emb_tuple = tuple(emb.tolist())
            results[orig_idx] = emb_tuple

    except Exception:
        # Fall back to sequential processing
        for i in uncached_indices:
            results[i] = get_embedding(texts[i])

    return [r if r is not None else get_embedding(texts[i]) for i, r in enumerate(results)]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if len(a) != len(b):
        raise ValueError(f"Dimension mismatch: {len(a)} vs {len(b)}")
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a < 1e-12 or norm_b < 1e-12:
        return 0.0
    return dot / (norm_a * norm_b)


def serialize_embedding(emb: list[float]) -> bytes:
    """Serialize embedding to bytes (float32 array) for SQLite BLOB storage."""
    return struct.pack(f"<{len(emb)}f", *emb)


def deserialize_embedding(blob: bytes) -> list[float]:
    """Deserialize embedding from SQLite BLOB back to float list."""
    count = len(blob) // 4
    return list(struct.unpack(f"<{count}f", blob))
