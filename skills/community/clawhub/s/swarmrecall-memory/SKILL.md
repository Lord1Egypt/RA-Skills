---
name: swarmrecall-memory
description: Conversational memory persistence with semantic search and session tracking via the SwarmRecall API. Stores and retrieves agent memories with vector embeddings for contextual recall.
metadata:
  openclaw:
    emoji: "\U0001F9E0"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Memory content is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per agent and owner. The agent must have user consent before storing personal or sensitive information.
    dataHandling: All data is transmitted over HTTPS. Memories are stored in PostgreSQL with pgvector embeddings. Data is tenant-isolated by owner ID and agent ID.
version: 1.1.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [memory, ai-agents, semantic-search, persistence, recall]
---

# SwarmRecall Memory

Conversational memory persistence with semantic search and session tracking via the SwarmRecall API.

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
- Memory content is stored server-side with vector embeddings for semantic search
- Data is isolated per agent and owner — no cross-tenant access
- Before storing user-provided content, ensure the user has consented to external storage
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

## Endpoints

### Store a memory
```
POST /api/v1/memory
{
  "content": "User prefers dark mode",
  "category": "preference",   // fact | preference | decision | context | session_summary
  "importance": 0.8,           // 0.0 to 1.0
  "tags": ["ui"],
  "metadata": {},
  "poolId": "<uuid>"           // optional — write to shared pool
}
```

### Search memories
```
GET /api/v1/memory/search?q=<query>&limit=10&minScore=0.5
```

### List memories
```
GET /api/v1/memory?category=preference&limit=20&offset=0&includeArchived=false
```

### Get a memory
```
GET /api/v1/memory/:id
```

### Update a memory
```
PATCH /api/v1/memory/:id
{ "importance": 0.9, "tags": ["updated"], "archived": false }
```

### Delete a memory
```
DELETE /api/v1/memory/:id
```

### Start a session
```
POST /api/v1/memory/sessions
{
  "context": {},
  "poolId": "<uuid>"           // optional — write to shared pool
}
```

### Get current session
```
GET /api/v1/memory/sessions/current
```

### Update a session
```
PATCH /api/v1/memory/sessions/:id
{ "summary": "Discussed project setup", "ended": true }
```

### List sessions
```
GET /api/v1/memory/sessions?limit=20&offset=0
```

## Behavior

- On session start: call `GET /api/v1/memory/sessions/current` to load context from the last session. If none, call `POST /api/v1/memory/sessions` to start one.
- On fact, preference, or decision: call `POST /api/v1/memory` with appropriate category and importance.
- On recall needed: call `GET /api/v1/memory/search?q=<query>` and use returned memories to inform your response.
- On session end: call `PATCH /api/v1/memory/sessions/:id` with `ended: true` and a summary.

## Shared Pools

- The `POST /api/v1/memory` and `POST /api/v1/memory/sessions` endpoints accept an optional `"poolId"` field.
- When `poolId` is provided, the memory or session is shared with all pool members who have memory read access.
- The agent must have readwrite access to the pool's memory module to write shared memories.
- Search (`GET /api/v1/memory/search`) and list (`GET /api/v1/memory`) results automatically include data from pools the agent belongs to.
- Pool data in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.

## Dreaming Integration

Memory is the primary target of dream operations. During a dream cycle:

- **Duplicate clusters**: Groups of similar memories are identified by the dream service. The agent reads the cluster, merges content into the anchor memory, and archives the rest. Use `PATCH /api/v1/memory/:id` to update the anchor and `DELETE /api/v1/memory/:id` to archive duplicates.
- **Session summaries**: Unsummarized sessions are flagged. The agent reads session memories via `GET /api/v1/memory?sessionId=X`, then writes a summary via `POST /api/v1/memory` with `category: "session_summary"`.
- **Decay and pruning**: The server automatically reduces importance of old memories and archives those below the prune threshold. Memories with `category: "session_summary"` or tag `"pinned"` are protected.
- **Contradictions**: Memory pairs with high similarity but divergent content are flagged. The agent reviews both, archives the stale one, and optionally updates the current one.

To protect a memory from pruning, add the `"pinned"` tag:
```
PATCH /api/v1/memory/:id
{ "tags": ["pinned", ...existing_tags] }
```
