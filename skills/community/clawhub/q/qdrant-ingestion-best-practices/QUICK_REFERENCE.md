# Quick Reference — Qdrant Ingestion Best Practices

## Embedding Model Cheat Sheet

| Need | Model | Dim | Notes |
|---|---|---|---|
| Hybrid (default) | `BAAI/bge-m3` | 1024 dense + sparse | One pass, dense + SPLADE sparse |
| Dense-only (efficient) | `text-embedding-3-small` | 1536 | OpenAI API, cost-efficient |
| Dense-only (quality) | `text-embedding-3-large` | 3072 | OpenAI API, highest quality |
| Sparse companion | Qdrant BM25 `modifier=IDF` | sparse | Native, no extra model |
| Sparse companion (quality) | `Qdrant/bm42-all-minilm-l6-v2-attentions` | sparse | Attention-weighted, better than BM25 |

## Chunking Parameters Cheat Sheet

| Content Type | Tokens | Overlap | Strategy |
|---|---|---|---|
| Slack / short messages | 150–300 | 30 | Sentence window |
| Email threads | 200–400 | 30 | Reply-boundary split first |
| Meeting transcripts | 150–250 | 20 | Speaker-turn split first |
| Documents / PDFs | 300–500 | 50 | Hierarchical paragraph |
| Tasks / Tickets | ≤ 512 | N/A | One chunk per task |
| Code | 200–400 | 50 | Function/class boundary-aware |

**Token estimation:** 4 characters ≈ 1 token (deterministic heuristic, no tokenizer needed).

## Sensitivity Tiers

| Tier | Examples | Collection |
|---|---|---|
| `public` | Marketing, public docs | `company_memory` |
| `internal` | Slack, all-hands, project docs | `company_memory` |
| `restricted` | Executive email, finance, legal | `restricted_memory` |
| `confidential` | Salary, PII, health records | `pii_memory` |

**Default:** `internal` when nothing matches.

## RRF Parameters

```
Dense prefetch: top-20
Sparse prefetch: top-20
RRF constant k: 60
Final results: 10–15
After reranking: 5–8
```

## Required Payload Indexes

```python
# Always create these indexes on every collection
fields_to_index = [
    ("sensitivity", "keyword"),
    ("org_id", "keyword", is_tenant=True),
    ("workspace_id", "keyword"),
    ("allowed_groups", "keyword"),
    ("data_scope_tags", "keyword"),
    ("team_ids", "keyword"),
    ("source_type", "keyword"),
    ("is_pii", "bool"),
    ("created_at", "datetime"),
    ("content_type", "keyword"),
]
```

## 10 Rules to Never Break

1. Classify sensitivity at ingest time — never at retrieval time
2. Apply access control filters inside the Qdrant query — never post-retrieval
3. Never store agent IDs or agent permission lists in chunk payloads
4. Chunking must be deterministic — same input always produces same chunks
5. All Qdrant writes must use upsert semantics — never raw insert
6. Compute all hashes from normalized content — never from raw source
7. Index every field used as a payload filter
8. Never fabricate metadata — use empty array or null for unknown values
9. `model_inferred` fields must not be sole basis for security decisions
10. Same embedding model must be used at both ingest time and query time

## Pipeline Stage Order

```
1. Source capture
2. Normalization
3. Document hash (SHA-256 of full normalized text)
4. Change detection (compare to stored hash)
5. Chunking
6. Chunk hashing (SHA-256 per chunk)
7. Embedding (dense ± sparse)
8. Upsert to Qdrant
9. Delete stale chunks (if re-ingestion produced fewer chunks)
```

## Scope Tags Taxonomy

| Prefix | Example | When |
|---|---|---|
| None (domain) | `sales`, `finance`, `hr` | Content is in this business domain |
| `team:` | `team:sales_a` | Content scoped to a specific team |
| `category:` | `category:pipeline` | Specific data category |
| `region:` | `region:emea` | Regional scope |
| `project:` | `project:alpha` | Specific project |

Tags must be: lowercase_snake_case, source_asserted or system_derived, stable, from the approved list.

## Guide Index

| Guide | Topic |
|---|---|
| `guides/01-rag-pipeline-overview.md` | Architecture, principles, decision guide |
| `guides/02-metadata-schema.md` | Full payload schema, all fields, indexes |
| `guides/03-data-classification.md` | Sensitivity tiers, collection setup, HNSW tuning |
| `guides/04-source-normalization.md` | Normalization rules by source type |
| `guides/05-chunking-standards.md` | Chunk sizes, strategies, code examples |
| `guides/06-embedding-models.md` | Model selection, BGE-M3, OpenAI, sparse |
| `guides/07-ingestion-pipeline.md` | Full pipeline code, lifecycle, idempotency |
| `guides/08-retrieval-architecture.md` | Hybrid search, RRF, reranking, filters |
| `guides/09-access-control.md` | Separation of concerns, permission flow, anti-patterns |
| `guides/10-operational-standards.md` | Schema versioning, retention, monitoring, conformance |
