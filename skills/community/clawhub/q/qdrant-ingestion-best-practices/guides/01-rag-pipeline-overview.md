# Guide 01 — RAG Pipeline Overview

## Purpose

This guide describes the end-to-end architecture of a production RAG pipeline using Qdrant. It defines the two halves of the system — **ingestion** and **retrieval** — and establishes the architectural principles that all other guides build on.

---

## The Two Halves of a RAG Pipeline

```
INGESTION SIDE                          RETRIEVAL SIDE
─────────────────────────────────       ──────────────────────────────────
Source System                           User / Agent Query
    │                                       │
    ▼                                       ▼
Source Capture (API / connector)        Query Embedding (same model as ingest)
    │                                       │
    ▼                                       ▼
Normalization                           Access Control Filter Resolution
    │                                       │
    ▼                                       ▼
Change Detection (hash compare)         Qdrant Query (filters embedded)
    │                                       │
    ▼                                   Dense Search ──┐
Chunking                                Sparse Search ──┤ RRF Fusion
    │                                       │           │
    ▼                                       ▼           │
Chunk Hashing                          Top-N Candidates◄┘
    │                                       │
    ▼                                       ▼
Embedding (dense + sparse or dense)    Optional Re-ranking (cross-encoder)
    │                                       │
    ▼                                       ▼
Metadata Assembly                      Result Assembly + Attribution
    │                                       │
    ▼                                       ▼
Qdrant Upsert                          Return to LLM / Agent
```

---

## Mandatory Processing Order (Ingestion)

Every ingestion pipeline MUST execute these stages in this exact order. Do not skip or reorder.

1. **Source capture** — Fetch raw content and metadata from the source system API.
2. **Normalization** — Apply universal + source-specific normalization rules. See `04-source-normalization.md`.
3. **Document hashing** — Compute `document_content_hash` (SHA-256) from the full normalized document text.
4. **Change detection** — Compare hash to the previously stored hash. If unchanged, refresh metadata only and skip steps 5–8.
5. **Chunking** — Apply the chunking strategy for the content type. See `05-chunking-standards.md`.
6. **Chunk hashing** — Compute `content_hash` (SHA-256) for each chunk from normalized chunk text.
7. **Embedding** — Generate dense and/or sparse vectors. See `06-embedding-models.md`.
8. **Storage** — Upsert chunks with full metadata payload to Qdrant. See `07-ingestion-pipeline.md`.

---

## Core Architectural Principles

### 1. Separation of Concerns: Data vs. Access Policy

The vector store holds **data characteristics** (what the content is, who authored it, what domain it belongs to). It does NOT hold **access policy** (which agents or users may access it). Access mappings belong exclusively in your orchestration layer (e.g., n8n, LangGraph, custom middleware).

**Prohibited in chunk metadata:**
- `allowed_agents`, `permitted_agents`, or any agent identity list
- Agent-level permission scopes embedded as payload fields
- Any field that dynamically changes based on who is querying

**Why:** If you embed agent permissions in chunks, every access change requires re-ingesting thousands of chunks. The orchestration layer can be updated instantly without touching the vector store.

### 2. Filters Must Be Applied Inside Qdrant Queries

Access control filters (sensitivity, group membership, scope tags) must be passed as Qdrant payload filter conditions within the query itself — never applied post-retrieval to a raw result set.

**Why post-filtering is dangerous:**
- Qdrant returns top-K candidates from the full vector space. If you filter afterwards, you may discard half the results, leaving fewer than expected — or returning none at all for highly restricted content.
- Post-filtering creates a window where restricted content is briefly retrieved before being discarded. This is a compliance risk.

### 3. Classify at Ingest Time, Never at Retrieval Time

Every chunk must have its sensitivity tier and scope tags assigned during ingestion. Retrieval pipelines must never attempt to classify content on the fly.

**Why:** Classification at retrieval time is too slow, inconsistent, and untestable. Ingest-time classification is auditable and deterministic.

### 4. Deterministic Ingestion

The same normalized source content must always produce the same chunks, the same hashes, and the same `doc_id`s. This is what makes the pipeline safe to re-run (idempotent) and what enables reliable change detection.

### 5. Upsert, Not Insert

All writes to Qdrant use upsert semantics. If a point with the same ID already exists, it is overwritten. This is the foundation of idempotent ingestion.

---

## Collection Architecture Principles

Do NOT create a collection per data source. Collections should be justified by one or more of:

| Criterion | Example |
|---|---|
| Security boundary | Confidential/PII data must not coexist with public data |
| Query pattern | Different collections may require different HNSW tuning |
| Scale / index tuning | Very large datasets benefit from isolated indexing |
| Lifecycle / retention | Data with different retention policies |

A typical production setup uses 3 collections:

| Collection | Contents | Access |
|---|---|---|
| `company_memory` | Public + internal tier (messages, transcripts, docs, tasks) | All staff |
| `restricted_memory` | Restricted tier (email, finance, legal, HR non-PII) | Authorized roles only |
| `pii_memory` | Confidential tier (PII: salary, health, tax IDs) | HR leadership, compliance |

See `03-data-classification.md` for the full sensitivity tier model.

---

## Choosing Retrieval Mode

| Scenario | Recommended Mode |
|---|---|
| Content contains proper nouns, IDs, codes, product names, exact phrases | **Hybrid** (dense + sparse) |
| Users search with natural language, vague intent | **Dense-only** acceptable, hybrid preferred |
| Need to balance semantic understanding with exact keyword matching | **Hybrid** with RRF |
| Latency-critical, simple domain | **Dense-only** with `text-embedding-3-small` |
| Complex enterprise knowledge base | **Hybrid** with BGE-M3 |

See `06-embedding-models.md` and `08-retrieval-architecture.md` for implementation.

---

## Evaluation Is Not Optional

Every retrieval architecture and chunking configuration must be validated before going to production. Minimum requirements:

- Minimum 50 representative queries with known expected results
- Precision and recall benchmarks at top-5 and top-10
- Latency benchmarks (mean, p95, p99)
- Citation accuracy: do returned chunks contain the claimed answer?
- Source coverage: does the system find content from all active source types?
- Regression tests: do changes to chunking or embedding degrade existing queries?

Document your evaluation results and link them to your pipeline version.
