---
name: swarmrecall
description: "Use SwarmRecall when an AI agent needs persistent memory, a knowledge graph, learnings, a skill registry, shared pools, or background dream consolidation across sessions. Works via the SwarmRecall CLI (for stdio MCP) or directly over HTTP/SDK. Every module supports semantic search with vector embeddings and tenant-isolated storage."
version: "1.2.0"
metadata: '{"openclaw":{"requires":{"anyBins":["swarmrecall"]},"install":[{"id":"node","kind":"node","package":"@swarmrecall/cli","bins":["swarmrecall"],"label":"Install SwarmRecall CLI (npm)"}],"mcp_servers":[{"id":"swarmrecall","label":"SwarmRecall (local stdio)","command":"swarmrecall","args":["mcp"],"env":{"SWARMRECALL_API_KEY":"${env:SWARMRECALL_API_KEY}"}},{"id":"swarmrecall-remote","label":"SwarmRecall (remote HTTP)","transport":"streamable-http","url":"https://swarmrecall-api.onrender.com/mcp","headers":{"Authorization":"Bearer ${env:SWARMRECALL_API_KEY}"}}],"emoji":"🧠","homepage":"https://www.swarmrecall.ai/docs/mcp","privacyPolicy":"All data is stored on SwarmRecall servers (swarmrecall-api.onrender.com). Data is scoped per agent and owner. The agent must have user consent before storing personal or sensitive information.","dataHandling":"All data is transmitted over HTTPS. Data is stored in PostgreSQL with pgvector embeddings. Data is tenant-isolated by owner ID and agent ID across all modules.","primaryEnv":"SWARMRECALL_API_KEY"}}'
author: swarmclawai
homepage: https://www.swarmrecall.ai
tags: [memory, knowledge-graph, learnings, skills, pools, dreaming, consolidation, mcp, ai-agents, persistence]
---

# SwarmRecall

Persistent memory, a knowledge graph, learnings, a skill registry, shared collaboration pools, and background "dream" consolidation — for any AI agent — via the SwarmRecall API at <https://swarmrecall-api.onrender.com>.

For onboarding, examples, command references, or troubleshooting, read the bundled `README.md`, `examples/`, `references/`, and `TROUBLESHOOTING.md` before improvising workflow advice.

## Setup

Three ways to connect, in increasing order of flexibility:

### 1. MCP (recommended for Claude Desktop, Claude Code, Cursor)

**Local stdio (default):**

```bash
npm install -g @swarmrecall/cli
swarmrecall register --save      # mints an API key and stores it in ~/.config/swarmrecall/config.json
swarmrecall mcp                  # runs the MCP server over stdio — point your client at this command
```

**Remote HTTP (no install):**

```
URL:     https://swarmrecall-api.onrender.com/mcp
Auth:    Authorization: Bearer ${SWARMRECALL_API_KEY}
Transport: streamable-http
```

Both transports expose the same 52 tools and 4 resources. See <https://www.swarmrecall.ai/docs/mcp> for client-specific configuration snippets.

### 2. CLI

```bash
npm install -g @swarmrecall/cli
swarmrecall register --save
swarmrecall memory store "<content>" --category fact --importance 0.8
swarmrecall memory search "<query>"
swarmrecall knowledge create --type person --name "Alice" --props '{"role":"engineer"}'
swarmrecall learnings log --category error --summary "<summary>"
swarmrecall dream start
```

See `references/commands.md` for the full command surface.

### 3. Raw HTTP / SDK

If the user is wiring a custom agent, install the SDK:

```bash
npm install @swarmrecall/sdk
```

```ts
import { SwarmRecallClient } from '@swarmrecall/sdk';
const client = new SwarmRecallClient({ apiKey: process.env.SWARMRECALL_API_KEY! });
await client.memory.store({ content: 'User prefers dark mode', category: 'preference', importance: 0.8 });
```

If `SWARMRECALL_API_KEY` is not set and a hosted agent needs one, self-register with no account:

```
POST https://swarmrecall-api.onrender.com/api/v1/register
Content-Type: application/json

{ "name": "<agent-name>" }
```

Response returns `{ "apiKey": "...", "claimToken": "..." }`. Tell the user: "SwarmRecall is set up! To manage your agent's data, visit <https://swarmrecall.ai/claim> with code: `<claimToken>`."

## Authentication

All API requests require a Bearer token in the Authorization header: `Authorization: Bearer <SWARMRECALL_API_KEY>`.

## Privacy & Data Handling

- All data is sent to `swarmrecall-api.onrender.com` over HTTPS.
- Memories, entities, learnings, skills, sessions, and dream cycles are stored server-side with vector embeddings for semantic search.
- Data is isolated per agent and owner — no cross-tenant access.
- Before storing user-provided content, ensure the user has consented to external storage.
- Store `SWARMRECALL_API_KEY` as an environment variable or in `~/.config/swarmrecall/config.json` (created by `swarmrecall register --save`). Do not check it into source control.

---

## Module 1: Memory

Conversational memory with semantic search and session tracking.

### When to use

- Storing user preferences, facts, decisions, and context.
- Recalling relevant information from past interactions.
- Managing conversation sessions end-to-end.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `memory_store` | Store a memory with category, importance, and tags. |
| `memory_search` | Semantic search over memories. |
| `memory_get` / `memory_list` | Fetch a specific memory or filtered list. |
| `memory_update` / `memory_delete` | Update metadata or archive a memory. |
| `memory_sessions_start` | Start a new memory session. |
| `memory_sessions_current` | Get the active session. |
| `memory_sessions_update` | Append state, summary, or mark ended. |
| `memory_sessions_list` | List sessions. |

### Behavior

- On session start: call `memory_sessions_current` to load context. If none, call `memory_sessions_start`.
- On fact, preference, or decision: call `memory_store` with an appropriate category and importance.
- On recall needed: call `memory_search` and use returned memories to inform your response.
- On session end: call `memory_sessions_update` with `ended: true` and a summary.

---

## Module 2: Knowledge

Knowledge graph with entities, relations, traversal, and semantic search.

### When to use

- Storing structured information about people, projects, tools, and concepts.
- Linking related entities together.
- Exploring connections between concepts.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `knowledge_entity_create/get/list/update/delete` | Entity CRUD. |
| `knowledge_relation_create/list/delete` | Relation CRUD. |
| `knowledge_traverse` | Walk the graph from an entity, filtered by relation and depth. |
| `knowledge_search` | Semantic search over entities. |
| `knowledge_validate` | Check graph constraints. |

### Behavior

- When the user provides structured information: call `knowledge_entity_create`.
- When linking concepts: call `knowledge_relation_create`.
- When the user asks "what do I know about X?": `knowledge_search` then `knowledge_traverse` to explore connections.
- Periodically: `knowledge_validate` to catch orphaned entities or conflicting relations.

---

## Module 3: Learnings

Error tracking, correction logging, and pattern detection that surfaces recurring issues.

### When to use

- Logging errors, corrections, discoveries, optimizations, or preferences.
- Detecting recurring patterns across sessions.
- Promoting learnings into actionable rules the agent surfaces to the user.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `learning_log` | Log a learning with category, summary, priority, area. |
| `learning_search/get/list/update` | Retrieve and update. |
| `learning_patterns` | List recurring patterns. |
| `learning_promotions` | List promotion candidates. |
| `learning_resolve` | Mark resolved with a resolution + optional commit SHA. |
| `learning_link` | Link two learnings for pattern detection. |

### Behavior

- On error or correction: `learning_log` with the full error output / what was wrong vs. correct.
- On session start: `learning_patterns` to preload known recurring issues; `learning_promotions` for patterns ready to be promoted.
- On promotion candidates: surface to the user for approval before acting on them.

---

## Module 4: Skills

Skill registry for tracking installed agent capabilities and getting contextual suggestions.

### When to use

- Registering capabilities the agent acquires.
- Listing what the agent can do.
- Getting skill recommendations for a given task.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `skill_register` | Register a new skill. |
| `skill_list/get/update/remove` | Manage registered skills. |
| `skill_suggest` | Get skill suggestions for a task context. |

### Behavior

- On skill install: `skill_register` with name, version, and source.
- On "what can I do?": `skill_list`.
- On task context: `skill_suggest` for relevant skill recommendations.

---

## Module 5: Shared Pools

Named shared data containers for cross-agent collaboration.

### When to use

- Sharing memories, knowledge, learnings, or skills between agents.
- Building collaborative workflows where multiple agents contribute to a shared dataset.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `pool_list` | List pools this agent belongs to. |
| `pool_get` | Pool details + members. |

### Behavior

- Pool data returned in responses includes `poolId` and `poolName` to distinguish shared data from the agent's private data.
- To write to a pool, pass `poolId` to any `memory_store`, `knowledge_entity_create`, `knowledge_relation_create`, `learning_log`, or `skill_register` call.
- On session start: `pool_list` to see available pools and their access levels.

---

## Module 6: Dreaming

Background memory consolidation — deduplication, pruning, contradiction resolution, and session summarization.

### When to use

- Between sessions or during idle periods for memory maintenance.
- When the user asks to "clean up", "consolidate", or "optimize" memories.
- Periodically via auto-dream scheduling.

### MCP tools

| Tool | Purpose |
| --- | --- |
| `dream_start` | Start a dream cycle. |
| `dream_get/list/update` | Cycle management. |
| `dream_complete/fail` | Cycle completion. |
| `dream_get_config` / `dream_update_config` | Configuration. |
| `dream_get_duplicates/unsummarized_sessions/duplicate_entities/stale/contradictions/unprocessed` | Candidate primitives. |
| `dream_execute` | Run Tier 1 server-side operations (decay, prune, orphan cleanup). |

### Behavior

1. Start a cycle: `dream_start`.
2. Run Tier 1 ops: `dream_execute` (decay, prune, orphan cleanup).
3. Fetch candidates: `dream_get_duplicates`, `dream_get_unsummarized_sessions`, `dream_get_contradictions`.
4. For each candidate: reason about it, then use the memory / knowledge / learnings tools to act.
5. Complete the cycle: `dream_complete` with the results.

---

## Resources

Read-only MCP resources for clients that surface resources as inline context:

- `swarmrecall://pools` — pools this agent belongs to
- `swarmrecall://skills` — skills this agent has registered
- `swarmrecall://sessions/current` — current memory session
- `swarmrecall://dream/config` — dream configuration

## Pointers

- <https://www.swarmrecall.ai/docs/mcp> — MCP setup for Claude Desktop, Claude Code, Cursor, MCP Inspector
- <https://www.swarmrecall.ai/docs/api-reference> — raw HTTP endpoints
- <https://www.npmjs.com/package/@swarmrecall/cli> — CLI source
- <https://github.com/swarmclawai/swarmrecall> — source repository
- `examples/quickstart.md`, `examples/memory-workflow.md`, `examples/knowledge-graph.md`, `examples/learnings-workflow.md` — workflow recipes
- `references/commands.md`, `references/mcp-tools.md` — complete command and tool references
- `TROUBLESHOOTING.md` — common auth and connectivity issues
