---
name: swarmrecall-learnings
description: Error tracking, correction logging, and pattern detection via the SwarmRecall API. Tracks agent mistakes, corrections, and discoveries to surface recurring issues and promote learnings into actionable rules.
metadata:
  openclaw:
    emoji: "\U0001F4A1"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Learning data is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per agent and owner. The agent must have user consent before storing personal or sensitive information.
    dataHandling: All data is transmitted over HTTPS. Learnings are stored in PostgreSQL with pgvector embeddings. Data is tenant-isolated by owner ID and agent ID.
version: 1.1.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [learnings, ai-agents, error-tracking, pattern-detection, persistence]
---

# SwarmRecall Learnings

Error tracking, correction logging, and pattern detection via the SwarmRecall API.

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
- Learning data (errors, corrections, discoveries) is stored server-side with vector embeddings for semantic search
- Data is isolated per agent and owner — no cross-tenant access
- Before storing user-provided content, ensure the user has consented to external storage
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

## Endpoints

### Log a learning
```
POST /api/v1/learnings
{
  "category": "error",        // error | correction | discovery | optimization | preference
  "summary": "npm install fails with peer deps",
  "details": "Full error output...",
  "priority": "high",         // low | medium | high | critical
  "area": "build",
  "suggestedAction": "Use --legacy-peer-deps flag",
  "tags": ["npm", "build"],
  "metadata": {},
  "poolId": "<uuid>"          // optional — write to shared pool
}
```

### Search learnings
```
GET /api/v1/learnings/search?q=<query>&limit=10&minScore=0.5
```

### Get a learning
```
GET /api/v1/learnings/:id
```

### List learnings
```
GET /api/v1/learnings?category=error&status=open&priority=high&area=build&limit=20&offset=0
```

### Update a learning
```
PATCH /api/v1/learnings/:id
{ "status": "resolved", "resolution": "Added --legacy-peer-deps", "resolutionCommit": "abc123" }
```

### Get recurring patterns
```
GET /api/v1/learnings/patterns
```

### Get promotion candidates
```
GET /api/v1/learnings/promotions
```

### Link related learnings
```
POST /api/v1/learnings/:id/link
{ "targetId": "<other-learning-id>" }
```

## Behavior

- On error: call `POST /api/v1/learnings` with `category: "error"`, the summary, details, and the command/output that failed.
- On correction: call `POST /api/v1/learnings` with `category: "correction"` and what was wrong vs. what is correct.
- On session start: call `GET /api/v1/learnings/patterns` to preload known recurring issues. Check `GET /api/v1/learnings/promotions` for patterns ready to be promoted.
- On promotion candidates: surface candidates to the user for approval before acting on them.

## Shared Pools

- The `POST /api/v1/learnings` endpoint accepts an optional `"poolId"` field.
- When `poolId` is provided, the learning is shared with all pool members who have learnings read access.
- The agent must have readwrite access to the pool's learnings module to write shared learnings.
- Search (`GET /api/v1/learnings/search`) and list (`GET /api/v1/learnings`) results automatically include data from pools the agent belongs to.
- Pool data in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.

## Dreaming Integration

Learnings benefit from dream-time promotion:

- **Promotion candidates**: The existing `GET /api/v1/learnings/promotions` endpoint surfaces patterns meeting promotion criteria (3+ recurrences, 2+ sessions, within 30 days). During a dream cycle, the agent reads each candidate, synthesizes a best-practice learning, and creates it via `POST /api/v1/learnings` with `category: "best_practice"` and `status: "promoted"`.
- **Pattern consolidation**: Related learnings are already linked via `POST /api/v1/learnings/:id/link`. During dreaming, the agent can review patterns and archive individual learnings that are fully subsumed by the promoted best practice.
