# Guide 08 — Retrieval Architecture

## Purpose

This guide covers the full retrieval pipeline: hybrid search with RRF, access control filter application, reranking, result assembly, and quality requirements.

---

## The Core Rule: Filters Inside the Query

Access control filters must be applied **within** the Qdrant query — not post-retrieval.

**Why filtering post-retrieval is wrong:**
- Qdrant returns top-K candidates from the full vector space before your code sees them
- If you filter afterward, you may discard most results, getting fewer than requested
- Post-filtering creates a window where restricted content is briefly retrieved, which is a compliance risk
- It wastes compute fetching content that will be discarded

**Always pass filters as Qdrant payload filter conditions, built server-side by your orchestration layer.**

---

## Hybrid Retrieval Pipeline (Recommended)

The standard pipeline for enterprise RAG using BGE-M3:

```
User/Agent Query
       │
       ▼
  Embed query with BGE-M3
  (produces dense + sparse in one pass)
       │
       ├─────────────────────────────────────────────┐
       ▼                                             ▼
  Dense Search (top-20)                    Sparse Search (top-20)
  + access control filters                 + access control filters
       │                                             │
       └──────────────────┬──────────────────────────┘
                          ▼
              RRF Fusion (k=60)
              Combined ranking
                          │
                          ▼
              Top 10–15 candidates
                          │
                          ▼
         Optional: Cross-encoder reranking
         (BGE-Reranker-v2 → top 5–8)
                          │
                          ▼
              Return results + attribution
```

---

## Implementation

### Dense-Only Query

```python
from qdrant_client import QdrantClient, models

def retrieve_dense(
    client: QdrantClient,
    collection: str,
    query_vector: list[float],
    access_filters: models.Filter,
    top_k: int = 20,
) -> list:
    """Single dense vector search with access control filters."""
    
    results = client.query_points(
        collection_name=collection,
        query=query_vector,
        using="dense",
        query_filter=access_filters,  # Filters applied INSIDE Qdrant query
        limit=top_k,
        with_payload=True,
    )
    return results.points
```

### Hybrid Query with RRF (Recommended)

```python
def retrieve_hybrid_rrf(
    client: QdrantClient,
    collection: str,
    query_dense: list[float],
    query_sparse: dict,  # {"indices": [...], "values": [...]}
    access_filters: models.Filter,
    prefetch_k: int = 20,
    final_k: int = 10,
) -> list:
    """
    Hybrid retrieval: dense + sparse with RRF fusion.
    Filters are applied inside each prefetch branch.
    """
    
    results = client.query_points(
        collection_name=collection,
        prefetch=[
            # Dense branch
            models.Prefetch(
                query=query_dense,
                using="dense",
                filter=access_filters,  # Filters inside the prefetch
                limit=prefetch_k,
            ),
            # Sparse branch
            models.Prefetch(
                query=models.SparseVector(
                    indices=query_sparse["indices"],
                    values=query_sparse["values"],
                ),
                using="sparse",
                filter=access_filters,  # Same filters applied to sparse branch
                limit=prefetch_k,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),  # RRF fusion
        limit=final_k,
        with_payload=True,
    )
    return results.points
```

### Multi-Collection Query (Searching Across Multiple Sensitivity Tiers)

```python
def retrieve_across_collections(
    client: QdrantClient,
    permitted_collections: list[str],
    query_dense: list[float],
    query_sparse: dict,
    access_filters: models.Filter,
    top_k: int = 10,
) -> list:
    """
    Query multiple collections in parallel and merge results.
    Use when a user has access to multiple sensitivity tiers.
    """
    import asyncio
    
    all_results = []
    for collection in permitted_collections:
        results = retrieve_hybrid_rrf(
            client, collection, query_dense, query_sparse,
            access_filters, prefetch_k=20, final_k=top_k
        )
        all_results.extend(results)
    
    # Apply RRF across collection results
    all_results.sort(key=lambda r: r.score, reverse=True)
    return all_results[:top_k]
```

---

## Building Access Control Filters

Access filters are constructed by your orchestration layer based on the resolved permission scope for the current user/agent pair. **The AI agent never constructs these filters.**

```python
def build_access_filter(permission_scope: dict) -> models.Filter:
    """
    Build a Qdrant filter from the resolved permission scope.
    
    permission_scope = {
        "org_id": "org-456",
        "workspace_id": "ws-123",
        "permitted_sensitivity": ["internal", "public"],
        "team_ids": ["team_sales_a"],           # None = no team restriction
        "allowed_groups": ["g_all_staff"],       # None = no group restriction
        "data_scope_tags": ["sales", "region:emea"],  # None = no scope restriction
    }
    """
    
    must_conditions = [
        # Always apply org and workspace isolation first
        models.FieldCondition(
            key="org_id",
            match=models.MatchValue(value=permission_scope["org_id"])
        ),
        models.FieldCondition(
            key="workspace_id",
            match=models.MatchValue(value=permission_scope["workspace_id"])
        ),
        # Sensitivity tier filter
        models.FieldCondition(
            key="sensitivity",
            match=models.MatchAny(any=permission_scope["permitted_sensitivity"])
        ),
    ]
    
    # Optional: team-scoped filter
    if permission_scope.get("team_ids"):
        must_conditions.append(
            models.FieldCondition(
                key="team_ids",
                match=models.MatchAny(any=permission_scope["team_ids"])
            )
        )
    
    # Optional: group-scoped filter
    if permission_scope.get("allowed_groups"):
        must_conditions.append(
            models.FieldCondition(
                key="allowed_groups",
                match=models.MatchAny(any=permission_scope["allowed_groups"])
            )
        )
    
    # Optional: data scope tag filter
    if permission_scope.get("data_scope_tags"):
        must_conditions.append(
            models.FieldCondition(
                key="data_scope_tags",
                match=models.MatchAny(any=permission_scope["data_scope_tags"])
            )
        )
    
    return models.Filter(must=must_conditions)
```

---

## RRF Parameters

Reciprocal Rank Fusion score: `score(d) = Σ 1/(k + rank_i(d))` for each ranked list i.

| Parameter | Default | Notes |
|---|---|---|
| `k` | 60 | Smoothing constant. Higher k = less differentiation at the top. 60 is the standard. |
| Dense prefetch | 20 | Retrieve top-20 from dense search before fusion |
| Sparse prefetch | 20 | Retrieve top-20 from sparse search before fusion |
| Final results | 10–15 | After RRF fusion, take top-10 to top-15 |
| After reranking | 5–8 | Final results passed to LLM after cross-encoder reranking |

**Only change k if measured retrieval quality degrades** and you have evidence that a different k improves it.

---

## Optional: Cross-Encoder Reranking

After RRF fusion, optionally apply a cross-encoder reranker to the top-N candidates. This produces higher quality final rankings but adds latency.

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")  # Recommended for multilingual

def rerank_results(query: str, candidates: list, top_k: int = 7) -> list:
    """
    Apply cross-encoder reranking to RRF candidates.
    Only use on small candidate sets (top 10–15 from RRF).
    """
    if not candidates:
        return candidates
    
    pairs = [(query, c.payload.get("text", "")) for c in candidates]
    scores = reranker.predict(pairs)
    
    ranked = sorted(
        zip(scores, candidates),
        key=lambda x: x[0],
        reverse=True,
    )
    
    return [c for _, c in ranked[:top_k]]
```

**Reranker options:**
| Model | Notes |
|---|---|
| `BAAI/bge-reranker-v2-m3` | Multilingual, recommended for enterprise |
| `BAAI/bge-reranker-large` | High quality English-focused |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | Fast, English, lower latency |

---

## Result Assembly and Attribution

Every result returned to the LLM must include human-readable attribution. Never return a chunk without its source attribution.

```python
def assemble_results(raw_points: list) -> list[dict]:
    """Format Qdrant results for LLM consumption."""
    assembled = []
    
    for point in raw_points:
        p = point.payload
        assembled.append({
            "text": p.get("text", ""),
            "context_header": p.get("context_header", ""),
            "attribution": {
                "source": p.get("source_type"),
                "title": p.get("title"),
                "author": p.get("author_name"),
                "created_at": p.get("created_at"),
                "doc_id": p.get("doc_id"),
            },
            "score": point.score,
        })
    
    return assembled
```

---

## Near-Duplicate Suppression

Near-duplicate chunks should be collapsed so the top results are not dominated by repeated content.

```python
def suppress_near_duplicates(
    results: list,
    similarity_threshold: float = 0.95,
) -> list:
    """
    Remove results that are near-duplicates of higher-ranked results.
    Uses content_hash for exact duplicates, parent_doc_id for near-duplicates.
    """
    seen_hashes = set()
    seen_parent_ids = {}  # parent_doc_id → best chunk score
    deduplicated = []
    
    for result in results:
        content_hash = result.payload.get("content_hash", "")
        parent_id = result.payload.get("parent_doc_id", "")
        
        # Exact duplicate: same content_hash
        if content_hash in seen_hashes:
            continue
        seen_hashes.add(content_hash)
        
        # Near-duplicate: same parent document, score within threshold of the best
        if parent_id in seen_parent_ids:
            best_score = seen_parent_ids[parent_id]
            if result.score >= best_score * similarity_threshold:
                continue  # Too similar, skip this one
        else:
            seen_parent_ids[parent_id] = result.score
        
        deduplicated.append(result)
    
    return deduplicated
```

---

## Retrieval Quality Requirements

| Requirement | Standard |
|---|---|
| Minimum context | Returned chunks must contain enough surrounding context to be useful without navigating to source |
| Attribution | Every result includes source system, document/conversation title, author, and timestamp |
| Near-duplicate handling | Top results must not be dominated by repeated content from the same source document |
| Version freshness | When multiple versions of the same document exist, the current version outranks superseded versions |
| Latency | p95 retrieval latency must stay within defined SLA (typically <500ms for hybrid, <200ms for dense-only) |

---

## Retrieval Path Observability

Log the following for every retrieval request:

```python
{
    "request_id": "...",          # Trace ID for the full request
    "query_text": "...",          # Query submitted
    "collection": "...",          # Collection(s) queried
    "filters_applied": {          # Filters applied (sensitivity, team_ids, scope_tags)
        "sensitivity": ["internal"],
        "team_ids": ["team_sales_a"],
        "data_scope_tags": ["sales"],
    },
    "dense_candidates": 20,       # Candidates from dense search
    "sparse_candidates": 18,      # Candidates from sparse search
    "rrf_candidates": 15,         # After RRF fusion
    "after_reranking": 7,         # After reranking
    "after_dedup": 6,             # After near-duplicate suppression
    "doc_ids_returned": ["..."],  # Final doc_ids returned to LLM
    "latency_ms": 145,            # Total retrieval latency
}
```
