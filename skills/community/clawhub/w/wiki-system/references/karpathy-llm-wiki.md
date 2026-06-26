# Karpathy's LLM Wiki Pattern

**Source:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Core Idea

"Compilation over retrieval" — instead of RAG (fetch raw docs every query), the LLM builds and maintains a structured wiki that compounds knowledge over time.

## Three Layers

1. **Raw Sources** (immutable) — curated documents, PDFs, articles. The LLM reads but never modifies.
2. **The Wiki** (LLM-maintained) — markdown pages with summaries, entity profiles, cross-references.
3. **The Schema** (configuration) — rules for structure, naming, workflows. Co-evolves with the project.

## Three Operations

- **Ingest:** Source added -> LLM reads it, extracts insights, creates/updates wiki pages, adds cross-references. A single source may touch 10-15 existing pages.
- **Query:** Ask questions against the wiki. LLM searches pages, synthesizes answers, optionally files results back as new pages.
- **Lint:** Periodic health check for contradictions, stale claims, orphaned pages, missing cross-references.

## Philosophy

"The tedious part of maintaining a knowledge base is not the reading or thinking — it's the bookkeeping." The human curates sources and directs analysis; the LLM handles summarization, cross-referencing, and maintenance.

## Scaling Notes

- index.md overflows context windows beyond ~100 pages (use domain sub-indices)
- Semantic search needed for large wikis (QMD/vector embeddings)
- Provenance tracking important for multi-session consistency
