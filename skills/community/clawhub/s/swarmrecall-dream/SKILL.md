---
name: swarmrecall-dream
description: Agent dreaming — memory consolidation, deduplication, pruning, contradiction resolution, and session summarization via the SwarmRecall API. Enables agents to optimize their memory store during idle periods.
metadata:
  openclaw:
    emoji: "\U0001F4A4"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Dream operations read and modify existing agent data on SwarmRecall servers (swarmrecall-api.onrender.com). No new external data is collected. Archived memories are soft-deleted and recoverable.
    dataHandling: All data is transmitted over HTTPS. Tier 1 operations (decay, prune, candidate detection) run server-side. Tier 2 operations (merge, summarize, resolve) are agent-driven using existing API endpoints. Data remains tenant-isolated by owner ID and agent ID.
version: 1.0.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [dreaming, memory-consolidation, pruning, deduplication, contradiction-resolution, ai-agents, persistence]
---

# SwarmRecall Dream

Agent dreaming — memory consolidation, deduplication, pruning, contradiction resolution, and session summarization. Run during idle periods to keep your memory store lean and accurate.

## Auto-Registration

Before making any API calls, check for a `SWARMRECALL_API_KEY` environment variable:

1. If `SWARMRECALL_API_KEY` is set, use it for all requests as a Bearer token.
2. If `SWARMRECALL_API_KEY` is not set, self-register by calling:
   ```
   POST https://swarmrecall-api.onrender.com/api/v1/register
   Content-Type: application/json

   { "name": "<your-agent-name>" }
   ```
3. The response returns `{ "apiKey": "...", "claimToken": "..." }`. Save the `apiKey` to the `SWARMRECALL_API_KEY` environment variable for all subsequent requests. Do NOT write the key to disk or any file without user consent.
4. Tell the user: "SwarmRecall is set up! To manage your agent's data, visit swarmrecall.ai/claim with code: `<claimToken>`"

## Authentication

All API requests require:
```
Authorization: Bearer <SWARMRECALL_API_KEY>
```

## API Base URL

`https://swarmrecall-api.onrender.com` (override with `SWARMRECALL_API_URL` if set)

All endpoints below are prefixed with `/api/v1`.

## Privacy & Data Handling

- All data is sent to `swarmrecall-api.onrender.com` over HTTPS
- Dream operations only read and modify your agent's existing data — no new external data is collected
- Archived memories are soft-deleted (recoverable) — never hard-deleted
- Data is isolated per agent and owner — no cross-tenant access
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

---

## How Dreaming Works

Dreaming uses a two-tier architecture:

**Tier 1 (server-side):** SwarmRecall runs deterministic operations that don't need intelligence — finding duplicate clusters, decaying importance, pruning low-importance memories, cleaning orphaned relations, and surfacing candidates for agent review.

**Tier 2 (agent-driven):** You (the agent) orchestrate the intelligent operations — reading candidate clusters, reasoning about what to merge/keep/archive, writing summaries, and resolving contradictions. You use the standard memory/knowledge/learnings endpoints to make changes.

---

## Endpoints

### Dream Cycle Management

#### Start a dream cycle
```
POST /api/v1/dream
{
  "operations": ["deduplicate", "decay_prune", "summarize_sessions"],  // optional, defaults to config
  "thresholds": {           // optional, override defaults for this cycle
    "similarityThreshold": 0.90,
    "decayAgeDays": 30,
    "decayFactor": 0.95,
    "pruneThreshold": 0.05,
    "batchSize": 500
  }
}
```
Returns the dream cycle with `status: "running"`. Only one cycle can run per agent at a time (409 if already running).

#### List dream cycles
```
GET /api/v1/dream?limit=20&offset=0&status=completed
```

#### Get a dream cycle
```
GET /api/v1/dream/:id
```

#### Update a dream cycle (report results, mark complete/failed)
```
PATCH /api/v1/dream/:id
{
  "status": "completed",
  "results": {
    "deduplicate": { "clustersFound": 3, "memoriesMerged": 5, "memoriesArchived": 5 },
    "decay_prune": { "memoriesDecayed": 12, "memoriesPruned": 2 },
    "summarize_sessions": { "sessionsProcessed": 4, "summariesCreated": 4, "memoriesDecayed": 0 },
    "durationMs": 4500
  }
}
```

### Dream Config

#### Get dream config
```
GET /api/v1/dream/config
```

#### Update dream config
```
PATCH /api/v1/dream/config
{
  "enabled": true,           // enable/disable auto-dreaming
  "intervalHours": 24,       // how often to auto-dream (1-168)
  "operations": ["deduplicate", "decay_prune", "summarize_sessions"],
  "thresholds": {
    "similarityThreshold": 0.90,
    "decayAgeDays": 30
  }
}
```

### Tier 1 Execute (run server-side ops)

```
POST /api/v1/dream/execute
{
  "operations": ["decay_prune"]   // optional, defaults to Tier 1 ops in config
}
```
Runs server-side operations (decay, prune, orphan cleanup) immediately. Returns results.

### Candidate Endpoints

These return pre-computed analysis for agent-driven (Tier 2) operations.

#### Duplicate memory clusters
```
GET /api/v1/dream/candidates/duplicates?limit=50
```
Response:
```json
{
  "clusters": [
    {
      "anchor": { "id": "mem_1", "content": "User prefers dark mode", "importance": 0.8 },
      "members": [
        { "id": "mem_7", "content": "The user likes dark mode themes", "importance": 0.5, "similarity": 0.94 },
        { "id": "mem_12", "content": "User said they prefer dark mode", "importance": 0.6, "similarity": 0.92 }
      ]
    }
  ],
  "totalClusters": 3,
  "thresholdUsed": 0.90
}
```

#### Unsummarized sessions
```
GET /api/v1/dream/candidates/unsummarized-sessions?limit=20
```
Response:
```json
{
  "sessions": [
    { "id": "sess_1", "memoryCount": 14, "startedAt": "2026-03-15T...", "endedAt": "2026-03-15T..." },
    { "id": "sess_2", "memoryCount": 8, "startedAt": "2026-03-18T...", "endedAt": "2026-03-18T..." }
  ],
  "totalSessions": 2
}
```

#### Duplicate entity pairs
```
GET /api/v1/dream/candidates/duplicate-entities?limit=50
```
Response:
```json
{
  "pairs": [
    {
      "entity_a": { "id": "ent_1", "type": "Person", "name": "John Smith", "properties": {} },
      "entity_b": { "id": "ent_5", "type": "Person", "name": "J. Smith", "properties": {} },
      "similarity": 0.93
    }
  ],
  "totalPairs": 1,
  "thresholdUsed": 0.92
}
```

#### Stale memories
```
GET /api/v1/dream/candidates/stale?limit=100
```
Response:
```json
{
  "memories": [
    { "id": "mem_20", "content": "...", "importance": 0.12, "createdAt": "2025-12-01T...", "ageDays": 121 }
  ],
  "totalStale": 15,
  "decayAgeDaysUsed": 30
}
```

#### Contradiction pairs
```
GET /api/v1/dream/candidates/contradictions?limit=50
```
Response:
```json
{
  "pairs": [
    {
      "memory_a": { "id": "mem_3", "content": "User's timezone is PST", "createdAt": "2026-01-15T..." },
      "memory_b": { "id": "mem_45", "content": "User's timezone is EST", "createdAt": "2026-03-20T..." },
      "similarity": 0.91,
      "contentDivergence": 0.67
    }
  ],
  "totalPairs": 1
}
```

#### Unprocessed memories (for knowledge graph enrichment)
```
GET /api/v1/dream/candidates/unprocessed?limit=100
```
Returns memories where `metadata.dreamProcessedAt` is null or before the last dream cycle.

---

## Behavior

### When to dream

- **Between sessions**: After ending a session and before starting the next one. This is the natural idle period.
- **On idle detection**: If your framework detects the agent is idle (no user interaction for a configured period), trigger a dream.
- **Periodically**: If auto-dream is enabled in your config, the server runs Tier 1 ops automatically on your interval. You can layer Tier 2 on top.
- **On explicit request**: When the user says something like "clean up your memory" or "consolidate what you know."

### Full dream flow

Follow this sequence for a complete dream cycle:

1. **Start the cycle:**
   ```
   POST /api/v1/dream
   { "operations": ["deduplicate", "summarize_sessions", "decay_prune", "resolve_contradictions"] }
   ```

2. **Run Tier 1 server-side ops (decay, prune, orphan cleanup):**
   ```
   POST /api/v1/dream/execute
   ```

3. **Fetch and process duplicate clusters:**
   ```
   GET /api/v1/dream/candidates/duplicates
   ```
   For each cluster:
   - Read all members, reason about which content to keep
   - Update the anchor memory with merged content: `PATCH /api/v1/memory/:anchorId`
   - Archive each duplicate: `PATCH /api/v1/memory/:duplicateId` with `{ "archived": true }`

4. **Fetch and process unsummarized sessions:**
   ```
   GET /api/v1/dream/candidates/unsummarized-sessions
   ```
   For each session:
   - Read its memories: `GET /api/v1/memory?sessionId=<id>&limit=100`
   - Reason about the session's key decisions, facts, and outcomes
   - Write the summary: `POST /api/v1/memory` with `{ "content": "<summary>", "category": "session_summary", "sessionId": "<id>", "importance": 0.7 }`

5. **Fetch and resolve contradictions:**
   ```
   GET /api/v1/dream/candidates/contradictions
   ```
   For each pair:
   - Read both memories and their context (timestamps, sessions)
   - Decide which is the current truth
   - Archive the stale one: `PATCH /api/v1/memory/:staleId` with `{ "archived": true }`
   - Optionally update the current one with a note about what changed

6. **Complete the cycle:**
   ```
   PATCH /api/v1/dream/:cycleId
   {
     "status": "completed",
     "results": { ... counts of what you did ... }
   }
   ```

### Tips

- **Start small**: For your first dream, just run `decay_prune` and `deduplicate`. Add more operations as you get comfortable.
- **Check before you merge**: Always read the full content of duplicate clusters before merging. High similarity doesn't always mean the memories are truly redundant — they might add different context.
- **Protect important memories**: Add the `"pinned"` tag to any memory that should never be pruned. Session summaries are automatically protected.
- **Report results**: Always update the dream cycle with results when done. This creates an audit trail and helps the dashboard show what happened.
- **Don't dream too often**: Once every 24 hours is a good default. More frequent dreaming wastes compute with diminishing returns.

## Shared Pools

- Dream operations respect pool boundaries. Candidate endpoints only return data the agent has access to.
- Pool-scoped data (memories, entities, learnings with a `poolId`) is included in candidate analysis if the agent has `readwrite` access to the pool.
- When merging pool-scoped memories, ensure the merged result retains the `poolId`.
