# Guide 06 — Embedding Models

## Purpose

This guide covers embedding model selection, configuration, and usage for both dense-only and hybrid (dense + sparse) RAG pipelines built on Qdrant.

---

## Decision: Dense-Only vs. Hybrid

Choose **hybrid** (dense + sparse) when your content contains:
- Proper nouns, product names, model numbers, or identifiers
- Technical jargon, acronyms, or domain-specific terminology
- Code identifiers, error codes, or numeric values
- Queries where exact keyword match matters alongside semantic similarity

Choose **dense-only** when:
- Content is purely natural language with no specialized terminology
- Latency is critical and you need the simplest possible pipeline
- Your embedding budget favors one API call over two model passes
- You're prototyping and want to validate the concept first

**Recommended default:** Hybrid with BGE-M3. The single-model-pass architecture (one call produces both dense and sparse vectors) makes it operationally simple.

---

## Recommended Models

### Hybrid Pipeline: BAAI/BGE-M3

**Use when:** You need both semantic and keyword search. This is the recommended default for enterprise RAG.

- Dense dimension: **1024**
- Sparse: SPLADE-style output (produced in the same model pass)
- Distance metric: **Cosine**
- Language support: Multilingual (100+ languages)
- Context window: 8,192 tokens
- One model pass produces both vector types

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

def embed_hybrid_bgem3(texts: list[str]) -> list[dict]:
    """
    Embed a list of texts using BGE-M3.
    Returns list of dicts with 'dense' and 'sparse' vectors.
    """
    output = model.encode(
        texts,
        batch_size=12,
        max_length=512,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False,  # Set True if using late interaction reranking
    )
    
    results = []
    for i in range(len(texts)):
        dense_vector = output["dense_vecs"][i].tolist()
        sparse_weights = output["lexical_weights"][i]  # dict: {token_id: weight}
        
        # Convert sparse weights to Qdrant SparseVector format
        indices = list(sparse_weights.keys())
        values = list(sparse_weights.values())
        
        results.append({
            "dense": dense_vector,
            "sparse": {"indices": indices, "values": values},
        })
    
    return results

# Alternatively, using Qdrant's built-in BM25 with IDF for sparse
# (simpler, no external model needed for sparse):
# Configure the collection with modifier=IDF and send raw tokens for sparse
```

**Collection setup for BGE-M3:**

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="my_collection",
    vectors_config={
        "dense": models.VectorParams(
            size=1024,
            distance=models.Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "sparse": models.SparseVectorParams(
            modifier=models.Modifier.IDF  # Optional: use IDF weighting for sparse
        )
    },
)
```

---

### Dense-Only Pipeline: OpenAI text-embedding-3-small

**Use when:** You want a simple, cost-efficient dense embedding with strong performance. No local model hosting required.

- Dense dimension: **1536**
- Distance metric: **Cosine**
- Language support: Strong multilingual support
- API-based (no local GPU required)
- Supports Matryoshka truncation (can use 512-dim for faster/cheaper retrieval)

```python
from openai import OpenAI

openai_client = OpenAI()

def embed_dense_openai_small(texts: list[str], dimensions: int = 1536) -> list[list[float]]:
    """
    Embed texts using text-embedding-3-small.
    Set dimensions=512 for faster retrieval at some quality cost.
    """
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
        dimensions=dimensions,
    )
    return [item.embedding for item in response.data]
```

**Collection setup for text-embedding-3-small:**

```python
client.create_collection(
    collection_name="my_collection",
    vectors_config=models.VectorParams(
        size=1536,  # or 512 if using Matryoshka truncation
        distance=models.Distance.COSINE,
        hnsw_config=models.HnswConfigDiff(m=16, ef_construct=100),
    ),
    quantization_config=models.ScalarQuantization(
        scalar=models.ScalarQuantizationConfig(
            type=models.ScalarType.INT8,
            quantile=0.99,
            always_ram=True,
        )
    ),
)
```

---

### Dense-Only (High Quality): OpenAI text-embedding-3-large

**Use when:** Maximum embedding quality is needed and cost is not the primary constraint.

- Dense dimension: **3072**
- Distance metric: **Cosine**
- Supports Matryoshka truncation down to 256 dimensions

```python
def embed_dense_openai_large(texts: list[str], dimensions: int = 3072) -> list[list[float]]:
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=texts,
        dimensions=dimensions,
    )
    return [item.embedding for item in response.data]
```

---

### Sparse-Only Options (for Hybrid without BGE-M3)

If you're using a different dense model but still want hybrid retrieval, you can use these for the sparse side:

| Model | Notes |
|---|---|
| Qdrant BM25 with `modifier=IDF` | Native Qdrant BM25, no external model needed. Good baseline. |
| `BAAI/bge-m3` SPLADE output | Best quality sparse vectors, but requires BGE-M3. |
| `prithivida/Splade_PP_en_v1` | SPLADE model via FastEmbed. Good quality for English. |
| `Qdrant/bm42-all-minilm-l6-v2-attentions` | BM42 — attention-weighted sparse. Better than BM25 for chunked text. |

**BM42 setup (recommended sparse-only companion to any dense model):**

```python
from fastembed import SparseTextEmbedding

sparse_model = SparseTextEmbedding(model_name="Qdrant/bm42-all-minilm-l6-v2-attentions")

def embed_sparse_bm42(texts: list[str]) -> list[dict]:
    embeddings = list(sparse_model.embed(texts))
    return [
        {"indices": e.indices.tolist(), "values": e.values.tolist()}
        for e in embeddings
    ]
```

---

## Query vs. Document Embedding

For BGE-M3, use `encode_queries` for query embedding and `encode` for document embedding. This applies the E5-style instruction prefix that improves retrieval quality:

```python
# At ingestion time — embed documents
doc_embeddings = model.encode(documents, ...)

# At retrieval time — embed queries
query_embeddings = model.encode_queries(
    queries,
    return_dense=True,
    return_sparse=True,
)
```

For OpenAI models, the same model and API endpoint is used for both documents and queries.

---

## Batching and Performance

| Scenario | Recommendation |
|---|---|
| BGE-M3 local inference | Batch size 8–16 on GPU, 2–4 on CPU |
| OpenAI embeddings | Batch up to 2,048 texts per API call |
| Large ingestion runs | Process in batches; implement exponential backoff on rate limit errors |
| Real-time query embedding | Single text per call is fine; consider caching frequent queries |

```python
def embed_in_batches(texts: list[str], batch_size: int = 16, embed_fn) -> list:
    """Embed texts in batches with progress tracking."""
    all_results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        results = embed_fn(batch)
        all_results.extend(results)
    return all_results
```

---

## Model Selection Summary

| Use Case | Dense Model | Sparse Model | Collection dims |
|---|---|---|---|
| Enterprise RAG (recommended) | BGE-M3 (1024-dim) | BGE-M3 SPLADE | 1024 dense + sparse |
| Simple/budget RAG | text-embedding-3-small | Qdrant BM25 IDF | 1536 dense + sparse |
| Highest quality dense-only | text-embedding-3-large | None | 3072 dense |
| Standard dense-only | text-embedding-3-small | None | 1536 dense |
| Multilingual enterprise | BGE-M3 | BGE-M3 SPLADE | 1024 dense + sparse |

---

## Important: Use the Same Model at Query Time

The embedding model used during retrieval (query time) **must match** the model used during ingestion. Mixing models produces meaningless similarity scores.

Record the model in every chunk's payload:
```json
{
  "embedding_model": "BAAI/bge-m3",
  "sparse_model": "BAAI/bge-m3-splade"
}
```

Store the model identifier in your pipeline configuration and validate it at startup.
