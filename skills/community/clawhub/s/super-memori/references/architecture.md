# super_memori v4 — Architecture

## Objective
Operate a current-generation local-only memory system for OpenClaw agents where files are canonical truth, retrieval can be lexical/semantic/hybrid, degraded host states remain honest, and weak models still face a compact interface.

## Canonical layers
1. Markdown/files in `memory/` are the source of truth.
2. SQLite FTS5 is the lexical / metadata index.
3. Qdrant is the semantic index.
4. Optional CPU reranker improves final ranking but is not required for core operation.
5. Host-profile shaping is derived, never canonical: it adjusts chunking, candidate budgets, audit depth, and truth surfaces, but it never replaces file truth.

## Why this architecture
- Files survive index corruption and remain readable to humans.
- SQLite FTS5 handles exact/path/tag/command recall in the active runtime.
- Qdrant backs semantic recall and filtered vector retrieval when the host is equipped.
- Weak models perform best when the retrieval logic stays hidden behind a small CLI surface.

## Runtime pipeline now implemented in code
```text
query
  → hard filters
  → lexical retrieval (FTS5)
  → semantic retrieval when local semantic stack is ready
  → reciprocal-rank fusion
  → temporal / relation-aware rerank
  → dedupe/diversity pass
  → result bundle + warnings + host-state truth
```

Host-profile shaping is applied before this flow chooses budgets and audit depth:
- `standard` for smaller hosts and conservative operation
- `max` for EPYC-class local hosts with large RAM and enough CPU

The host profile changes candidate budgets and audit depth, not the public command surface.

## Storage model
- Canonical memory remains file-based.
- Chunk metadata lives in SQLite.
- Embeddings live in Qdrant.
- Queue/backlog state lives locally on disk.

## Required degraded modes
- Qdrant down or semantic host stack unavailable → lexical-only mode with warning
- semantic-unbuilt host state → lexical runtime remains valid; semantic path reported unavailable
- stale vectors → lexical or partial hybrid with warning until rebuild
- lexical DB damaged → emergency grep fallback if possible
- broken relation targets → maintenance/audit warning; new writes must reject them

## Target environment
- Ubuntu
- CPU-only host
- OpenClaw agent controlled by weaker models
- Local-first operation with no mandatory external APIs

## Non-goals for the current v4 line
- graph database first
- autonomous self-rewrite of memory policy
- cloud-backed memory services
- many public scripts for weak models
- canonical storage inside vector DB
