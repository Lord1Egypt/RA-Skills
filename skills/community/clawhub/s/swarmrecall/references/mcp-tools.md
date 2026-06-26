# MCP tools — full reference

52 tools across 6 modules, plus 4 resources. Every tool mirrors a `SwarmRecallClient` SDK method; inputs are validated with Zod.

## Memory (10)

| Tool | Inputs | Description |
| --- | --- | --- |
| `memory_store` | `content`, `category`, `importance?`, `tags?`, `metadata?`, `sessionId?`, `poolId?` | Store a memory. |
| `memory_search` | `query`, `limit?`, `minScore?` | Semantic search. |
| `memory_get` | `id` | Fetch by ID. |
| `memory_list` | `category?`, `sessionId?`, `limit?`, `offset?`, `includeArchived?` | List with filtering. |
| `memory_update` | `id`, `importance?`, `tags?`, `metadata?`, `archived?` | Update metadata. |
| `memory_delete` | `id` | Permanent delete. |
| `memory_sessions_start` | `context?`, `poolId?` | Start a session. |
| `memory_sessions_current` | — | Fetch the active session. |
| `memory_sessions_update` | `id`, `currentState?`, `summary?`, `ended?` | Update session. |
| `memory_sessions_list` | `limit?`, `offset?` | List sessions. |

## Knowledge (11)

| Tool | Inputs | Description |
| --- | --- | --- |
| `knowledge_entity_create` | `type`, `name`, `properties?`, `poolId?` | Create entity. |
| `knowledge_entity_get` | `id` | Fetch with outgoing relations. |
| `knowledge_entity_list` | `type?`, `limit?`, `offset?`, `includeArchived?` | List. |
| `knowledge_entity_update` | `id`, `name?`, `properties?`, `archived?` | Update. |
| `knowledge_entity_delete` | `id` | Delete (cascades to relations). |
| `knowledge_relation_create` | `fromEntityId`, `toEntityId`, `relation`, `properties?`, `poolId?` | Create relation. |
| `knowledge_relation_list` | `entityId?`, `relation?`, `limit?`, `offset?` | List relations. |
| `knowledge_relation_delete` | `id` | Delete relation. |
| `knowledge_traverse` | `startId`, `relation?`, `depth?`, `limit?` | Graph walk. |
| `knowledge_search` | `query`, `limit?`, `minScore?` | Semantic search. |
| `knowledge_validate` | — | Check constraints. |

## Learnings (9)

| Tool | Inputs | Description |
| --- | --- | --- |
| `learning_log` | `category`, `summary`, `details?`, `priority?`, `area?`, `suggestedAction?`, `tags?`, `metadata?`, `poolId?` | Log a learning. |
| `learning_search` | `query`, `limit?`, `minScore?` | Semantic search. |
| `learning_get` | `id` | Fetch by ID. |
| `learning_list` | `category?`, `status?`, `priority?`, `area?`, `limit?`, `offset?` | List. |
| `learning_update` | `id`, `status?`, `priority?`, `resolution?`, `resolutionCommit?`, `area?`, `tags?` | Update. |
| `learning_patterns` | — | Recurring pattern clusters. |
| `learning_promotions` | — | Promotion candidates. |
| `learning_resolve` | `id`, `resolution`, `commit?` | Mark resolved. |
| `learning_link` | `id`, `targetId` | Link related learnings. |

## Skills (6)

| Tool | Inputs | Description |
| --- | --- | --- |
| `skill_register` | `name`, `version?`, `source?`, `description?`, `triggers?`, `dependencies?`, `config?`, `poolId?` | Register a skill. |
| `skill_list` | `status?`, `limit?`, `offset?` | List registered skills. |
| `skill_get` | `id` | Fetch by ID. |
| `skill_update` | `id`, `version?`, `config?`, `status?` | Update. |
| `skill_remove` | `id` | Unregister. |
| `skill_suggest` | `context`, `limit?` | Suggest skills for a task context. |

## Pools (2)

| Tool | Inputs | Description |
| --- | --- | --- |
| `pool_list` | — | Pools this agent belongs to. |
| `pool_get` | `poolId` | Pool details + members. |

## Dream (14)

| Tool | Inputs | Description |
| --- | --- | --- |
| `dream_start` | `operations?`, `thresholds?`, `dryRun?` | Start a cycle. |
| `dream_get` | `id` | Get a cycle. |
| `dream_list` | `status?`, `limit?`, `offset?` | List cycles. |
| `dream_update` | `id`, `status?`, `results?`, `error?` | Update. |
| `dream_complete` | `id`, `results` | Mark completed. |
| `dream_fail` | `id`, `error` | Mark failed. |
| `dream_get_config` | — | Get config. |
| `dream_update_config` | `enabled?`, `intervalHours?`, `operations?`, `thresholds?` | Update config. |
| `dream_get_duplicates` | `limit?` | Memory clusters over similarity threshold. |
| `dream_get_unsummarized_sessions` | `limit?` | Completed sessions without summaries. |
| `dream_get_duplicate_entities` | `limit?` | Entity pairs that may be dupes. |
| `dream_get_stale` | `limit?` | Memories past decay age. |
| `dream_get_contradictions` | `limit?` | Memory pairs with divergent content. |
| `dream_get_unprocessed` | `limit?` | Memories missing entity extraction. |
| `dream_execute` | `operations?` | Run Tier 1 ops (decay, prune, cleanup). |

## Resources (4)

| URI | Purpose |
| --- | --- |
| `swarmrecall://pools` | Pools this agent belongs to with access levels. |
| `swarmrecall://skills` | Registered skills. |
| `swarmrecall://sessions/current` | Current memory session. |
| `swarmrecall://dream/config` | Dream configuration. |

## Tool output shape

Every tool returns `{ content: [{ type: "text", text: "<stringified JSON>" }] }`. Errors return the same shape with `isError: true` and the error message in `text`.
