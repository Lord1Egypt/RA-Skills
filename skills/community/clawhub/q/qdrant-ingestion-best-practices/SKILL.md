---
name: qdrant-ingestion-best-practices
description: Use this skill whenever building, designing, or debugging a RAG pipeline using Qdrant as the vector store. Covers ingestion pipelines, chunking standards, metadata schema design, hybrid dense+sparse retrieval with RRF, access control patterns, embedding model selection (BGE-M3 for hybrid, text-embedding-3-small for dense-only), collection architecture, normalization, deduplication, idempotency, and operational standards. Triggers include: any mention of Qdrant, RAG pipeline, vector ingestion, chunking, embeddings, hybrid search, payload filters, or access-controlled retrieval.
---

# Qdrant Ingestion Best Practices

## Overview

This skill package provides comprehensive, production-grade guidance for building RAG (Retrieval-Augmented Generation) pipelines using Qdrant as the vector store. It covers everything from data ingestion and chunking to hybrid retrieval, metadata standards, and access control patterns.

All detailed guidance lives in the `guides/` subfolder. **Always read the relevant guide(s) before writing code or designing a pipeline.** Use the Quick Decision Guide below to determine which guides to load.

---

## Skill Structure

| Guide | Path | When to Read |
|---|---|---|
| **RAG Pipeline Overview** | `guides/01-rag-pipeline-overview.md` | Start here. Architecture, decisions, model selection. |
| **Metadata Schema Standards** | `guides/02-metadata-schema.md` | Designing chunk payloads and payload index strategy. |
| **Data Classification & Collections** | `guides/03-data-classification.md` | Multi-collection design, sensitivity tiers, tenancy. |
| **Source Normalization** | `guides/04-source-normalization.md` | Pre-processing rules by source type before chunking. |
| **Chunking Standards** | `guides/05-chunking-standards.md` | Chunk size, overlap, strategy by content type. |
| **Embedding Models** | `guides/06-embedding-models.md` | Dense vs hybrid model selection and configuration. |
| **Ingestion Pipeline** | `guides/07-ingestion-pipeline.md` | Full pipeline steps, idempotency, upsert patterns. |
| **Retrieval Architecture** | `guides/08-retrieval-architecture.md` | Hybrid search, RRF, reranking, filter application. |
| **Access Control Patterns** | `guides/09-access-control.md` | Payload-based filtering, separation of concerns. |
| **Operational Standards** | `guides/10-operational-standards.md` | Lifecycle, retention, observability, conformance. |
| **Quick Reference** | `QUICK_REFERENCE.md` | Cheat sheet: model dims, chunk sizes, RRF params. |

---

## Quick Decision Guide

### What embedding model should I use?
Read `guides/06-embedding-models.md` for full details. Quick answer:

```
Need hybrid (semantic + keyword)?
  → BAAI/BGE-M3  (dense 1024-dim + SPLADE sparse, single model pass)

Need dense-only (simpler pipeline)?
  → text-embedding-3-small  (OpenAI, 1536-dim, cost-efficient)
  → text-embedding-3-large  (OpenAI, 3072-dim, highest quality dense)
```

### What chunking strategy should I use?
Read `guides/05-chunking-standards.md` for full code. Quick answer:

```
Conversational (Slack, short messages) → 150–300 tokens, 30 overlap, sentence window
Email threads                          → Split at reply boundary first, then 200–400 tokens
Meeting transcripts                    → Split at speaker turns, 200 tokens, 20 overlap
Documents / PDFs                       → Hierarchical paragraph, 300–500 tokens, 50 overlap
Tasks / Tickets                        → One chunk per task, max 512 tokens
```

### How many collections do I need?
Read `guides/03-data-classification.md`. Justify collections by: security boundary, query pattern, scale/index tuning, or lifecycle difference. Do NOT create a collection per data source. Standard setup = 3 collections: `company_memory`, `restricted_memory`, `pii_memory`.

### Building from scratch?
Read guides in this order: `01 → 02 → 03 → 06 → 07 → 08`

### Improving retrieval quality?
Read: `08 → 05 → 06 → 10`

### Adding access control?
Read: `09 → 03 → 02` (focus on governance fields)

### Onboarding a new data source?
Read: `04 → 05 → 02 → 07`

### Debugging ingestion or metadata issues?
Read: `07 → 10 → 02`

---

## 10 Rules — Never Violate These

1. **Classify sensitivity at ingest time.** Never defer to retrieval time.
2. **Apply access control filters inside the Qdrant query.** Never post-filter retrieved results.
3. **Never embed agent or user permission lists in chunk payloads.** Permissions belong in your orchestration layer config only.
4. **Chunking must be deterministic.** Same normalized input → same chunks → same hashes → same doc_ids.
5. **All writes to Qdrant must use upsert semantics.** Raw inserts are prohibited in pipelines.
6. **Compute all hashes from normalized content.** Never from raw source payloads.
7. **Index every field used as a payload filter.** Unindexed filter fields cause full collection scans.
8. **Never fabricate metadata.** If a value cannot be determined, use empty array or null.
9. **`model_inferred` fields must not be sole basis for security decisions.**
10. **Use the same embedding model at query time as at ingest time.** Mixing models produces meaningless scores.

---

## Mandatory Pipeline Stage Order

Every ingestion pipeline must execute these stages in this exact order:

```
1. Source capture        — fetch raw content + metadata from source API
2. Normalization         — apply universal + source-specific rules  (→ guide 04)
3. Document hash         — SHA-256 of full normalized document text
4. Change detection      — compare hash to stored hash; skip steps 5–8 if unchanged
5. Chunking              — apply strategy for content type              (→ guide 05)
6. Chunk hashing         — SHA-256 per chunk from normalized chunk text
7. Embedding             — dense ± sparse vectors                       (→ guide 06)
8. Upsert to Qdrant      — full metadata payload                        (→ guide 07)
9. Stale chunk cleanup   — delete chunks whose chunk_index is now out of range
```

---

## Sensitivity Tiers → Collections

| Tier | Examples | Collection |
|---|---|---|
| `public` | Marketing, public docs | `company_memory` |
| `internal` | Slack, all-hands, project docs | `company_memory` |
| `restricted` | Executive email, finance, legal | `restricted_memory` |
| `confidential` | Salary, PII, health records | `pii_memory` |

Default when nothing matches: **`internal`**

---

## Retrieval Pipeline Summary

```
Query → Embed (BGE-M3: dense + sparse in one pass)
     → Dense search top-20  ─┐
     → Sparse search top-20  ─┤  (access filters applied inside each branch)
                              ▼
                         RRF fusion (k=60)
                              ▼
                         Top 10–15 results
                              ▼
                    Optional: cross-encoder rerank → top 5–8
                              ▼
                         Return with attribution
```

See `guides/08-retrieval-architecture.md` for full implementation code.
