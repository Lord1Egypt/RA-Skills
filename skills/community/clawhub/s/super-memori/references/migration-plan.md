# super_memori v4 — Migration / Release-Line Plan

## Current state
The root scripts in this skill folder now implement the v4 candidate runtime line: lexical search, semantic indexing/search, hybrid fusion, temporal-relational rerank, integrity audit, and relation-aware learning writes all exist in code. Older v2/v3 interpretations remain only as historical reference surfaces.

## Migration goal
Finish the shift from the frozen lexical-first historical line to a fully synced current-generation local-memory subsystem with explicit implemented-vs-host-state truth, canonical relation targeting, stronger eval coverage, and publish-honest release evidence.

## Recommended phases

### Phase 1 — Stabilize public interface
- Keep the root public surface at four commands
- Keep lexical retrieval, health, queue, and freshness working
- Stop making stronger semantic claims than implementation supports

### Phase 2 — Introduce lexical registry
- Add SQLite metadata + FTS5
- Keep files canonical
- Route exact/path/tag retrieval through lexical index

### Phase 3 — Finish semantic host-state discipline
- Keep Qdrant as derived semantic backend
- Preserve freshness reporting and degraded-mode warnings
- Distinguish semantic-unbuilt host state from true integrity drift
- Keep user-facing text honest about implemented runtime vs current host state

### Phase 4 — Add quality/ops layer
- Optional CPU reranker
- queue/backlog handling
- stronger health checks
- duplicate/orphan detection
- Follow `implementation-order.md` exactly when weaker models finish the remaining work

## Rule during migration
Never claim a stable `v4.0.0 release` until scripts, contracts, health/audit semantics, and release evidence all match the current runtime truth.
