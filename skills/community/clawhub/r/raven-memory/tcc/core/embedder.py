from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=1)
def get_embedder():
    """
    Load the embedding model once and cache it.
    Uses all-MiniLM-L6-v2: 90MB, 384 dims, fast on CPU.
    """
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


def embed(text: str) -> list[float]:
    """
    Embed a string and return a flat list of floats.
    Input is the node's event + plan text combined.
    """
    model = get_embedder()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def embed_node(node) -> list[float]:
    """
    Embed a TCCNode. Combines event and plan for richer representation.
    """
    text = f"{node.event}. {node.plan}".strip(". ")
    return embed(text)
