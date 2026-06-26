# super_memori — Implementation Order for Weak Models

## Goal
Provide a deterministic sequence that a weaker model can follow later to finish the remaining hybrid-memory implementation safely.

## Order

### Step 1 — Check baseline
Run:
```bash
health-check.sh --json
index-memory.sh --stats --json
query-memory.sh --json "test"
```
Do not start semantic work until lexical baseline is healthy.

### Step 2 — Verify semantic prerequisites
Confirm:
- Qdrant reachable
- embedding dependencies installed
- vector collection configured
- host has enough disk/RAM for local embeddings

### Step 3 — Implement semantic indexing path
Add a deterministic path from canonical files → embeddings → Qdrant upsert.
Do not change canonical storage.

### Step 4 — Add semantic freshness state
Track:
- last semantic index build
- semantic queue backlog
- semantic stale age

### Step 5 — Implement hybrid retrieval
Inside `query-memory.sh`:
- lexical retrieve
- semantic retrieve
- fuse
- return one result bundle

### Step 6 — Verify degraded behavior
Simulate or observe:
- semantic unavailable
- lexical still healthy
- warnings surfaced correctly

### Step 7 — Add reranker last
Only after hybrid retrieval is stable.
Reranker is a quality layer, not a prerequisite.

### Step 8 — Update docs last
Only after runtime behavior is verified.
Never lead with docs when the mechanism is not ready.

## Exit rule
If any step fails, stop and fix that layer before moving forward.
Weak models must not skip forward into a more complex stage.
