# super_memori — Historical Roadmap to 4.0.1 (Archive Only)

> ⚠️ ARCHIVED: This promotion path has already been completed for the current stable `4.0.1` line. Keep this file only as historical evidence of the pre-stable promotion sequence; do not treat it as pending work.

## Purpose
This is the archived short instruction that was used to turn the earlier `super_memori` `4.0.0 candidate` line into the first equipped-host-verified stable full-hybrid runtime release later published as `4.0.1`.

Use this roadmap only when reviewing historical promotion logic, not when inferring the current release state.

## 7-step roadmap

### 1. Freeze and verify the baseline
Run:
```bash
health-check.sh --json
index-memory.sh --stats --json
query-memory.sh --json "deepseek"
```
Do not start hybrid work until lexical baseline is healthy.

### 2. Install and verify semantic prerequisites
Confirm all of these:
- Qdrant reachable
- embedding dependencies installed
- vector collection exists
- local CPU embedding path works

If any prerequisite fails, stop and fix it before moving on.

### 3. Verify semantic indexing for canonical files
The deterministic path from canonical memory files to vector upserts now exists in code.
Do not move canonical truth out of markdown/files.
Verify it on the target host by building vectors successfully.

### 4. Add semantic freshness + backlog visibility
Track and surface:
- last semantic index build
- semantic stale age
- semantic queue backlog
- semantic degraded state

### 5. Verify hybrid retrieval inside `query-memory.sh`
The runtime already does this internally:
- lexical retrieve
- semantic retrieve
- candidate fusion
- temporal / relation-aware rerank
- unified result bundle

Do not make weaker models choose the backend.

### 6. Add reranker last
Only after hybrid retrieval works.
Reranker is a quality layer, not the foundation.
It must degrade safely if unavailable.

### 7. Re-test and only then release the first stable line
That promotion path could be called complete only if all were true:
- lexical search verified
- semantic search verified
- hybrid search verified
- health-check distinguishes healthy hybrid vs degraded mode
- documentation matches runtime reality

## Hard rule
Do not call the skill stable full hybrid just because the code path exists or Qdrant is running.
It is stable full hybrid only when host validation, retrieval, freshness, audit semantics, and docs all agree.
That gate was later satisfied for the stable `4.0.1` line; current host truth must still be taken from live command outputs.
