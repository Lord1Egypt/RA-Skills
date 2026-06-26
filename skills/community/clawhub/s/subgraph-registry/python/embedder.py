"""
Subgraph Embedder

Computes one 384-dim sentence-transformers embedding per subgraph
using fastembed (pure-ONNX, no PyTorch). Runs only at crawl time.

The source string blends display_name, description, canonical entity
hints, top schema entity names, contract address keywords (chain /
protocol) into a single dense vector. Runtime consumers (Node MCP
server, Python query layer) compute cosine similarity over these
vectors — no fastembed required at runtime.

Model: sentence-transformers/all-MiniLM-L6-v2 (384 floats, 23 MB)
Wire format: little-endian float32 BLOB (384 * 4 = 1536 bytes per row)

The same exact model is shipped in JS via @xenova/transformers as
Xenova/all-MiniLM-L6-v2 — vectors are bitwise-comparable across
runtimes so the Node MCP server can embed at query time and compare
against the Python-precomputed vectors.
"""

from __future__ import annotations

import struct
from typing import Iterable, List, Optional, Sequence

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

_model = None


def _load_model():
    """Lazy-load the fastembed model. Cached for the process lifetime.

    fastembed downloads + caches to ~/.cache/fastembed on first use. In
    CI we wire actions/cache against this dir to skip the download on
    subsequent runs.
    """
    global _model
    if _model is None:
        from fastembed import TextEmbedding  # type: ignore

        _model = TextEmbedding(model_name=MODEL_NAME)
    return _model


def floats_to_blob(vec: Sequence[float]) -> bytes:
    """Pack a float vector as little-endian float32 bytes."""
    return struct.pack(f"<{len(vec)}f", *vec)


def blob_to_floats(blob: bytes) -> List[float]:
    """Unpack a little-endian float32 blob back into a Python list."""
    n = len(blob) // 4
    return list(struct.unpack(f"<{n}f", blob))


def build_source_text(
    *,
    display_name: Optional[str],
    description: Optional[str],
    auto_description: Optional[str],
    canonical_entities: Sequence[dict],
    all_entities: Sequence[dict],
    domain: Optional[str],
    protocol_type: Optional[str],
    network: Optional[str],
    contract_addresses: Optional[Sequence[dict]],
    max_chars: int = 1000,
) -> str:
    """Build the input string fed to the embedder for one subgraph.

    Order: display_name | description | entities | schema | domain |
    protocol | network | contracts. Truncated to max_chars at the end —
    MiniLM tokenizes ~4 chars/token and its cap is 256 tokens, so 1000
    chars keeps us comfortably under (~250 tokens) while preserving the
    contracts/schema tail for schema-rich subgraphs. The model auto-
    truncates internally if we overshoot.
    """
    name = (display_name or "").strip()
    desc = (description or auto_description or "").strip()

    # Top canonical-entity hints — these are the highest-signal field
    # for "what kind of subgraph is this?"
    canonical_types: List[str] = []
    for ce in (canonical_entities or [])[:8]:
        ct = ce.get("canonical_type") if isinstance(ce, dict) else None
        if ct:
            canonical_types.append(ct)

    # Raw schema entity names — picks up domain vocabulary that didn't
    # map to a canonical type (e.g. "Vault", "MarketDayData").
    schema_names: List[str] = []
    for e in (all_entities or [])[:12]:
        if isinstance(e, dict):
            n = e.get("name")
            if n and not n.startswith("_"):
                schema_names.append(n)

    contracts: List[str] = []
    for c in (contract_addresses or [])[:3]:
        if isinstance(c, dict):
            n = c.get("name") or c.get("kind")
            if n:
                contracts.append(str(n))

    parts = [
        name,
        desc,
        "entities: " + ", ".join(canonical_types) if canonical_types else "",
        "schema: " + ", ".join(schema_names) if schema_names else "",
        f"domain: {domain}" if domain else "",
        f"protocol: {protocol_type}" if protocol_type else "",
        f"network: {network}" if network else "",
        "contracts: " + ", ".join(contracts) if contracts else "",
    ]
    text = " | ".join(p for p in parts if p)
    if len(text) > max_chars:
        text = text[:max_chars]
    return text


def encode_batch(texts: Sequence[str], batch_size: int = 64) -> List[bytes]:
    """Encode a batch of strings into float32 BLOBs.

    fastembed is 5-10x faster batched at 64 than one-at-a-time. Caller
    is responsible for chunking; this iterates the model's generator
    in one pass and collects bytes for stable ordering.
    """
    if not texts:
        return []
    model = _load_model()
    blobs: List[bytes] = []
    # fastembed's .embed() returns a generator yielding numpy arrays in
    # input order. batch_size is honored internally; we just pass it.
    for vec in model.embed(list(texts), batch_size=batch_size):
        # vec is a numpy array; tolist() avoids a numpy import here.
        blobs.append(floats_to_blob(vec.tolist()))
    return blobs


def encode_query(text: str) -> List[float]:
    """Embed a single query string. Returns the raw float vector.

    Used by the Python query layer (if any). The Node MCP server has
    its own ONNX runtime path via @xenova/transformers so it doesn't
    call back into Python.
    """
    model = _load_model()
    vec = next(iter(model.embed([text])))
    return vec.tolist()


def cosine(a: Iterable[float], b: Iterable[float]) -> float:
    """Cosine similarity between two equal-length float iterables."""
    a = list(a)
    b = list(b)
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)
