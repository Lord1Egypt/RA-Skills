---
name: vm-memory-oracle
description: >
  Production-grade memory persistence and lifecycle management for VM-hosted
  OpenClaw agents. Implements structured 4-layer memory (knowledge graph,
  semantic index, daily summaries, canonical MEMORY.md), activation/decay
  scoring, nightly consolidation, disk-health monitoring, and self-healing
  maintenance. Fully local — zero network calls, zero cloud dependencies.
version: 2.0.0
author: ssharif
license: MIT-0
tags:
  - memory
  - persistence
  - vm
  - infrastructure
  - knowledge-graph
  - lifecycle
  - maintenance
metadata:
  openclaw:
    requires:
      bins:
        - jq
        - cron
    primaryEnv: null
  compatibility:
    openclaw: ">=1.8.0"
    platforms:
      - linux
  permissions:
    - filesystem
  category: memory-management
  quality-signals:
    no-network: true
    no-credentials: true
    no-sudo: true
    local-only: true
---

# VM Memory Oracle

Production-grade memory persistence and lifecycle management for VM-hosted OpenClaw agents.

You are a memory management specialist. Your job is to maintain a structured, persistent memory system that survives reboots, context compaction, and VM redeployment. You operate entirely on local files — you never make network requests, access credentials, or require elevated permissions.

## Memory Architecture

You manage a 4-layer memory system stored under the agent's data directory (default: `/data/memory/`). Each layer serves a distinct purpose:

```
Layer 0 — Knowledge Graph    : Durable facts, relationships, entities
Layer 1 — Semantic Index     : Embedding vectors for similarity search
Layer 2 — Daily Summaries    : Per-day session digests
Layer 3 — Canonical Memory   : MEMORY.md — the single source of truth
```

### Directory Layout

```
/data/memory/
  knowledge-graph/
    facts.jsonl              # One JSON object per line: {id, subject, predicate, object, source, created, activation}
    entities.jsonl           # Unique entities extracted from facts
    relations.jsonl          # Relationship types and counts
  embeddings/
    index.bin                # FAISS or ONNX-exported vector index
    metadata.jsonl           # Maps vector IDs to fact IDs
  daily/
    YYYY-MM-DD.md            # Daily session summary
  sessions/
    YYYY-MM-DD-HHMMSS.jsonl  # Raw session logs (pre-summarization)
  activation-metadata.json   # Activation scores and last-access timestamps
  MEMORY.md                  # Canonical long-term memory
  health.json                # Latest health check results
```

## Core Operations

### 1. Fact Ingestion

When the agent learns something new during a session, store it as a structured fact:

```json
{
  "id": "fact-<uuid>",
  "subject": "deployment project",
  "predicate": "started_on",
  "object": "2026-05-15",
  "source": "user-stated",
  "created": "2026-05-15T14:30:00Z",
  "activation": 1.0
}
```

Append to `knowledge-graph/facts.jsonl`. Update `entities.jsonl` and `relations.jsonl` if new entities or relation types appear.

Rules:
- Deduplicate before appending. If a fact with the same subject+predicate+object exists, update its activation score instead of adding a duplicate.
- Never overwrite the file. Always append or update in place.
- Validate JSON before writing. Malformed lines corrupt the graph.

### 2. Activation and Decay

Every fact has an activation score between 0.0 and 1.0. This controls recall priority.

**Decay formula** (applied nightly):
```
new_activation = current_activation * (0.5 ^ (days_since_last_access / half_life))
```

**Default parameters:**
- `half_life`: 30 days
- `recall_boost`: 0.3 (added on each recall, capped at 1.0)
- `search_threshold`: 0.15 (facts below this are excluded from search results)
- `prune_threshold`: 0.05 (facts below this are eligible for archival)
- `max_facts`: 10000 (hard cap; lowest-activation facts archived first)

**On every recall:** When a fact is used to answer a query, increase its activation:
```
activation = min(1.0, activation + recall_boost)
last_accessed = now()
```

Update `activation-metadata.json` after every recall or decay pass.

### 3. Daily Summarization

At the end of each day (or when triggered manually), produce a daily summary:

1. Read all session files from `sessions/` for the current date.
2. Extract key facts, decisions, preferences, and action items.
3. Write a structured summary to `daily/YYYY-MM-DD.md` with sections:
   - **Facts Learned** — new information stated by the user or discovered
   - **Decisions Made** — choices, approvals, rejections
   - **Preferences Noted** — how the user likes things done
   - **Action Items** — pending tasks or follow-ups
4. For each fact in the summary, ensure it exists in the knowledge graph.

### 4. Nightly Consolidation

Run the full maintenance pipeline in sequence:

**Step 1 — Summarize** (if not already done):
Generate today's daily summary from session logs.

**Step 2 — Decay**:
Apply the decay formula to all facts in `activation-metadata.json`.

**Step 3 — Index**:
Rebuild the embedding index from all facts above `search_threshold`.

**Step 4 — Prune**:
Archive facts below `prune_threshold` to `knowledge-graph/archived-facts.jsonl`.
Remove them from the active `facts.jsonl` and the embedding index.

**Step 5 — Reconcile MEMORY.md**:
Read all facts with activation > 0.5. Compare against current MEMORY.md content.
Add any missing high-activation facts. Remove any entries whose underlying facts have decayed below 0.15.
Keep MEMORY.md under 200 lines.

**Step 6 — Clean sessions**:
Delete session files older than 30 days.
Delete daily summaries older than 365 days.

**Step 7 — Health check**:
Write results to `health.json` (see Monitoring section).

### 5. Recall and Search

When the agent needs to remember something:

1. **Exact match**: Search `facts.jsonl` for matching subject/predicate/object.
2. **Semantic search**: Query the embedding index for the top-K most similar facts (K=10).
3. **Activation filter**: Exclude results below `search_threshold` (0.15).
4. **Boost accessed facts**: Update activation scores for all returned facts.
5. **Return**: Merge and deduplicate results, sorted by activation score descending.

Always prefer facts from the knowledge graph over raw daily files. MEMORY.md is a summary — the graph is the source of truth.

## Monitoring and Health

### Health Check Output

Write to `health.json` after every consolidation run:

```json
{
  "timestamp": "2026-05-15T00:45:00Z",
  "status": "healthy",
  "disk_usage_bytes": 2147483648,
  "disk_usage_percent": 3.3,
  "total_facts": 2847,
  "active_facts": 2103,
  "archived_facts": 744,
  "avg_activation": 0.42,
  "daily_files_count": 128,
  "session_files_count": 45,
  "embedding_index_size_bytes": 52428800,
  "memory_md_lines": 87,
  "last_consolidation": "2026-05-15T00:30:00Z",
  "consolidation_duration_seconds": 142,
  "warnings": []
}
```

### Warning Conditions

Flag these in `health.json` warnings array:
- `disk_usage_percent > 80` — "Disk usage high"
- `total_facts > 9000` — "Approaching fact limit"
- `avg_activation < 0.2` — "Most facts are decaying; consider lowering half_life"
- `avg_activation > 0.8` — "Facts not decaying enough; consider raising half_life"
- `memory_md_lines > 180` — "MEMORY.md approaching 200-line limit"
- `consolidation_duration_seconds > 600` — "Consolidation taking too long"

### Quality Probe

Maintain a set of canary facts in `knowledge-graph/canary-facts.json`:

```json
[
  {
    "query": "When did the fleet deployment project start?",
    "expected_contains": "May 15, 2026"
  }
]
```

Periodically (weekly), run each canary query through the recall pipeline. Log the pass/fail ratio. If accuracy drops below 70%, add a warning to `health.json`.

## Cron Schedule (for VM deployments)

Set up these cron jobs for automated lifecycle management:

```
# Daily summarization at 23:00
0 23 * * * openclaw skill run vm-memory-oracle --action summarize

# Full consolidation at 00:30
30 0 * * * openclaw skill run vm-memory-oracle --action consolidate

# Health check every 6 hours
0 */6 * * * openclaw skill run vm-memory-oracle --action health-check

# Quality probe every Sunday at 03:00
0 3 * * 0 openclaw skill run vm-memory-oracle --action quality-probe
```

## Configuration

Override defaults by setting values in the agent's configuration:

```yaml
memory_oracle:
  data_path: /data/memory
  half_life_days: 30
  recall_boost: 0.3
  search_threshold: 0.15
  prune_threshold: 0.05
  max_facts: 10000
  session_retention_days: 30
  daily_retention_days: 365
  memory_md_max_lines: 200
  canary_check_interval: weekly
  embedding_model: multilingual-e5-large
  embedding_device: cpu
```

## Safety Guarantees

- **Local-only**: This skill never makes network requests. All data stays on the local filesystem.
- **No credentials**: This skill never reads, writes, or transmits API keys, tokens, passwords, or any authentication material.
- **No elevation**: This skill never uses sudo, su, or any privilege escalation.
- **Append-only writes**: Facts are appended, never bulk-overwritten. Archival moves facts to a separate file rather than deleting them.
- **Idempotent**: Running any operation twice produces the same result. Safe to retry after failures.
- **Transparent**: All operations write human-readable files (JSONL, Markdown, JSON). No binary blobs except the embedding index, which is rebuildable from source facts.
