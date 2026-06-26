---
name: swarmrecall-knowledge
description: Knowledge graph with entities, relations, traversal, and semantic search via the SwarmRecall API. Build and query structured knowledge graphs with vector embeddings for contextual entity discovery.
metadata:
  openclaw:
    emoji: "\U0001F310"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Knowledge graph data is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per agent and owner. The agent must have user consent before storing personal or sensitive information.
    dataHandling: All data is transmitted over HTTPS. Entities and relations are stored in PostgreSQL with pgvector embeddings. Data is tenant-isolated by owner ID and agent ID.
version: 1.1.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [knowledge-graph, ai-agents, semantic-search, persistence, entities]
---

# SwarmRecall Knowledge

Knowledge graph with entities, relations, traversal, and semantic search via the SwarmRecall API.

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
- Knowledge graph data (entities, relations) is stored server-side with vector embeddings for semantic search
- Data is isolated per agent and owner — no cross-tenant access
- Before storing user-provided content, ensure the user has consented to external storage
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

## Endpoints

### Create an entity
```
POST /api/v1/knowledge/entities
{
  "type": "person",
  "name": "Alice",
  "properties": { "role": "engineer" },
  "poolId": "<uuid>"           // optional — write to shared pool
}
```

### Get an entity
```
GET /api/v1/knowledge/entities/:id
```

### List entities
```
GET /api/v1/knowledge/entities?type=person&limit=20&offset=0&includeArchived=false
```

### Update an entity
```
PATCH /api/v1/knowledge/entities/:id
{ "name": "Alice Smith", "properties": { "role": "senior engineer" } }
```

### Delete an entity
```
DELETE /api/v1/knowledge/entities/:id
```

### Create a relation
```
POST /api/v1/knowledge/relations
{
  "fromEntityId": "<id>",
  "toEntityId": "<id>",
  "relation": "works_on",
  "properties": {},
  "poolId": "<uuid>"           // optional — write to shared pool
}
```

### List relations
```
GET /api/v1/knowledge/relations?entityId=<id>&relation=works_on&limit=20&offset=0
```

### Delete a relation
```
DELETE /api/v1/knowledge/relations/:id
```

### Traverse the graph
```
GET /api/v1/knowledge/traverse?startId=<id>&relation=works_on&depth=2&limit=50
```

### Search entities
```
GET /api/v1/knowledge/search?q=<query>&limit=10&minScore=0.5
```

### Validate the graph
```
POST /api/v1/knowledge/validate
```

## Behavior

- When the user provides structured information: create entities with `POST /api/v1/knowledge/entities`.
- When linking concepts: create relations with `POST /api/v1/knowledge/relations`.
- When the user asks "what do I know about X?": search with `GET /api/v1/knowledge/search?q=X`, then traverse with `GET /api/v1/knowledge/traverse` to explore connections.
- Periodically: call `POST /api/v1/knowledge/validate` to check graph constraints.

## Shared Pools

- The `POST /api/v1/knowledge/entities` and `POST /api/v1/knowledge/relations` endpoints accept an optional `"poolId"` field.
- When `poolId` is provided, the entity or relation is shared with all pool members who have knowledge read access.
- The agent must have readwrite access to the pool's knowledge module to write shared entities and relations.
- Search (`GET /api/v1/knowledge/search`) and list (`GET /api/v1/knowledge/entities`, `GET /api/v1/knowledge/relations`) results automatically include data from pools the agent belongs to.
- Pool data in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.

## Dreaming Integration

Knowledge entities and relations are affected by dream operations:

- **Duplicate entities**: Entity pairs of the same type with similar names/embeddings are identified. The agent reviews each pair and decides: merge, keep both, or archive one. For merges, migrate relations from the archived entity to the survivor before archiving.
- **Orphan cleanup**: Relations pointing to archived entities are automatically removed by Tier 1 dream operations (no agent action needed).
- **Knowledge graph enrichment**: During dreaming, the agent can read recent memories and extract new entities and relations, creating them via `POST /api/v1/knowledge/entities` and `POST /api/v1/knowledge/relations`.
