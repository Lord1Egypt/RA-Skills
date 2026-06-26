---
name: swarmrecall-pools
description: Named shared data containers for cross-agent collaboration via the SwarmRecall API. Manage shared pools that let multiple agents contribute to and query from a common dataset across memory, knowledge, learnings, and skills modules.
metadata:
  openclaw:
    emoji: "\U0001F91D"
    requires:
      env: [SWARMRECALL_API_KEY]
    primaryEnv: SWARMRECALL_API_KEY
    privacyPolicy: Pool data is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per pool membership and access level. The agent must have user consent before storing personal or sensitive information to shared pools.
    dataHandling: All data is transmitted over HTTPS. Pools and membership are stored in PostgreSQL. Data is tenant-isolated by owner ID and pool access controls.
version: 1.1.0
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [pools, ai-agents, collaboration, shared-data, persistence]
---

# SwarmRecall Pools

Named shared data containers for cross-agent collaboration via the SwarmRecall API.

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
- Pool membership and shared data is stored server-side
- Data is isolated per pool with access controls — no unauthorized cross-pool access
- Before storing user-provided content to shared pools, ensure the user has consented to external storage
- The `SWARMRECALL_API_KEY` should be stored as an environment variable only, not written to disk

## Endpoints

### List pools
```
GET /api/v1/pools
```
Returns the pools this agent belongs to. Requires `pools.read` scope.

### Get pool details
```
GET /api/v1/pools/:id
```
Returns pool details and its members. Requires `pools.read` scope.

## Behavior

- Pools let agents share data across organizational boundaries. When an agent belongs to a pool, search and list results across all modules (memory, knowledge, learnings, skills) automatically include data from that pool.
- To write data to a shared pool, include `"poolId": "<uuid>"` in any create request for memory, knowledge entities, knowledge relations, learnings, or skills.
- The agent must have the appropriate access level for the pool and module (e.g., readwrite access to the pool's memory module to store shared memories).
- Pool data returned in responses includes `poolId` and `poolName` fields to distinguish shared data from the agent's own data.
