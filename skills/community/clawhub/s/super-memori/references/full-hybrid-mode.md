# super_memori — Full Hybrid Mode

## Purpose
Define the **stable full-hybrid target state** of `super_memori` where lexical, semantic, fusion, rerank, freshness, relation-aware scoring, repair semantics, and health all operate as one coherent local-memory subsystem.

This file is intentionally a **stable-release target contract**, not a claim that the current host already runs all layers. The current line may implement these features in code while still running in degraded host state.

## Full Hybrid Definition
A stable full-hybrid `super_memori` run means:
1. canonical files are readable
2. lexical registry/index is healthy
3. semantic backend is healthy
4. embeddings can be generated locally
5. lexical + semantic candidates are fused
6. temporal / relation-aware rerank operates correctly
7. degraded states are surfaced explicitly
8. repair/audit semantics distinguish semantic-unbuilt from true drift

## Target runtime flow
```text
query-memory.sh --mode auto "query"
  → normalize query
  → apply hard filters
  → lexical retrieval (SQLite FTS5)
  → semantic retrieval (Qdrant)
  → fuse candidate sets
  → optional rerank (top-N only)
  → dedupe/diversify
  → return results + warnings + freshness
```

## Full-Hybrid Readiness Checklist
A host is only in full-hybrid mode if **all** are true:
- `health-check.sh` reports lexical DB healthy
- `health-check.sh` reports Qdrant reachable
- embedding dependencies are installed
- vector collection exists and is populated
- lexical freshness is current
- semantic freshness is current
- backlog queue is within threshold
- `query-memory.sh --mode hybrid --json` returns `mode_used=hybrid` without semantic degradation warnings

## Semantic Layer Requirements
The semantic layer in the v4 candidate line supports:
- local embeddings on CPU
- vector upsert/update
- vector search with payload filters
- freshness visibility
- explicit degraded mode when unavailable
- a fixed embedding contract (dimension + normalization + rebuild rules)

## Fusion Contract
The skill should eventually implement one deterministic fusion method:
- reciprocal rank fusion, or
- weighted lexical + semantic merge

Default recommendation:
- lexical candidates: top 20
- semantic candidates: top 20
- rerank candidates: top 10 after fusion
- if semantic returns no usable candidates, continue lexical-only and warn

This must happen inside `query-memory.sh`, not inside model reasoning.

## Rerank Requirements
Reranking is optional for baseline operation but required for full-hybrid quality mode.

Rules:
- rerank only small candidate sets
- skip rerank for exact/path-heavy queries
- do not block the whole query if reranker is unavailable
- surface reranker degradation as a warning, not a silent failure

## Stable-release validation order
Before promoting the current candidate line to a stable full-hybrid release:
1. run `validate-release.sh`
2. verify lexical baseline still passes
3. verify semantic dependencies/model are installed on at least one target host
4. verify vector collection exists and is populated on that host
5. verify semantic freshness reporting
6. verify hybrid query output on the semantic-ready host
7. verify temporal / relation-aware rerank on the semantic-ready host
8. only then consider stable promotion

## Acceptance Criteria for Full Hybrid Mode
A stable release can claim full hybrid mode only if all are true:
- lexical search works
- semantic search works
- hybrid search works
- health check distinguishes lexical-only, semantic-unbuilt, and hybrid-ready states
- queue/backlog is monitored
- stale semantic state is surfaced
- repair/audit semantics are validated
- at least one live semantic-ready host proves hybrid mode selected automatically
- documentation matches the actual runtime behavior

## Anti-Patterns
Do not call the skill full-hybrid if any of these are true:
- semantic dependencies are missing
- vector collection exists but is stale and unreported
- reranker is required for all queries
- the model must manually choose lexical vs semantic backend
- degraded states are only visible in logs, not in command output
