---
name: swarmrecall-skills
description: Skill registry for tracking agent capabilities and getting contextual suggestions via the SwarmRecall API. Register, list, and query installed skills with semantic matching for task-relevant recommendations.
metadata:
  openclaw:
    emoji: "\U0001F527"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Skill registry data is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per agent and owner. The agent must have user consent before storing personal or sensitive information.
    dataHandling: All data is transmitted over HTTPS. Skills are stored in PostgreSQL with pgvector embeddings. Data is tenant-isolated by owner ID and agent ID.
version: 1.1.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [skills, ai-agents, skill-registry, persistence, suggestions]
---

# SwarmRecall Skills

Skill registry for tracking agent capabilities and getting contextual suggestions via the SwarmRecall API.

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
- Skill registry data is stored server-side with vector embeddings for semantic search
- Data is isolated per agent and owner — no cross-tenant access
- Before storing user-provided content, ensure the user has consented to external storage
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

## Endpoints

### Register a skill
```
POST /api/v1/skills
{
  "name": "code-review",
  "version": "1.0.0",
  "source": "clawhub/code-review",
  "description": "Automated code review with inline suggestions",
  "triggers": ["review", "PR"],
  "dependencies": ["git"],
  "config": {},
  "poolId": "<uuid>"           // optional — write to shared pool
}
```

### List skills
```
GET /api/v1/skills?status=active&limit=20&offset=0
```

### Get a skill
```
GET /api/v1/skills/:id
```

### Update a skill
```
PATCH /api/v1/skills/:id
{ "version": "1.1.0", "config": {}, "status": "active" }
```

### Remove a skill
```
DELETE /api/v1/skills/:id
```

### Get skill suggestions
```
GET /api/v1/skills/suggest?context=<task-description>&limit=5
```

## Behavior

- On skill install: call `POST /api/v1/skills` to register the skill with name, version, and source.
- On "what can I do?": call `GET /api/v1/skills` to list installed capabilities.
- On task context: call `GET /api/v1/skills/suggest?context=<description>` for relevant skill recommendations.

## Shared Pools

- The `POST /api/v1/skills` endpoint accepts an optional `"poolId"` field.
- When `poolId` is provided, the skill is shared with all pool members who have skills read access.
- The agent must have readwrite access to the pool's skills module to register shared skills.
- List (`GET /api/v1/skills`) and suggest (`GET /api/v1/skills/suggest`) results automatically include data from pools the agent belongs to.
- Pool data in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.
