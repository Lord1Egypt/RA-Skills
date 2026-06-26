# MCP Tools API Reference

> Complete reference for all Unified Memory MCP tools. Based on `src/index.js` v1.1.0.

## Table of Contents

- [Core Tools](#core-tools) — Search, Store, List, Delete
- [Prompt Composition](#prompt-composition) — memory_compose
- [v4.0 Storage Gateway](#v40-storage-gateway) — memory_v4_*
- [Advanced Tools](#advanced-tools) — Export, Dedup, Decay, QA
- [Preference & Profile](#preference--profile) — memory_preference, memory_profile
- [Version Control](#version-control) — memory_version
- [Search Engines](#search-engines) — memory_engine, memory_qmd
- [Tier Management](#tier-management) — memory_tier
- [System Tools](#system-tools) — Stats, Health, Metrics, WAL

---

## Core Tools

### memory_search

Hybrid search using BM25 + Vector + RRF fusion.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | *required* | Search query text |
| `topK` | `number` | `5` | Number of results to return |
| `mode` | `"hybrid" \| "bm25" \| "vector"` | `"hybrid"` | Search mode |
| `scope` | `string` | `null` | Scope filter: `AGENT`, `USER`, `TEAM`, `GLOBAL` |

**Example:**
```json
{
  "query": "user's preferred programming language",
  "topK": 5,
  "mode": "hybrid",
  "scope": "USER"
}
```

**Response:**
```json
{
  "count": 3,
  "query": "user's preferred programming language",
  "mode": "hybrid",
  "results": [
    {
      "id": "mem_xxx",
      "text": "The user prefers Python for data work",
      "category": "preference",
      "importance": 0.85,
      "score": 0.923,
      "created_at": "2026-04-15T10:00:00Z"
    }
  ],
  "token_budget": {
    "used_tokens": 1200,
    "max_tokens": 2000,
    "remaining_tokens": 800,
    "percent_used": 60.0
  }
}
```

---

### memory_store

Store a new memory.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `string` | *required* | Memory content |
| `category` | `string` | `"general"` | Category: `preference`, `fact`, `decision`, `entity`, `reflection` |
| `importance` | `number` | `0.5` | Importance score 0–1 |
| `tags` | `string[]` | `[]` | Tags for the memory |
| `scope` | `string` | `null` | Scope: `AGENT`, `USER`, `TEAM`, `GLOBAL` |
| `source` | `string` | `"manual"` | Source: `manual`, `auto`, `extraction` |

**Example:**
```json
{
  "text": "User prefers morning meetings",
  "category": "preference",
  "importance": 0.8,
  "tags": ["meetings", "schedule"],
  "scope": "USER"
}
```

**Auto-extraction:** When `category="general"` and `importance > 0.7`, automatically extracts structured facts.

---

### memory_list

List all stored memories with metadata.

**Parameters:** None

**Example:** `{}`

**Response:**
```json
{
  "count": 42,
  "memories": [
    {
      "id": "mem_xxx",
      "text": "User prefers...",
      "category": "preference",
      "importance": 0.8,
      "created_at": "2026-04-15T10:00:00Z"
    }
  ]
}
```

---

### memory_delete

Delete a memory by ID. WAL-logged and transcript-logged.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | Memory ID to delete |

---

## Prompt Composition

### memory_compose

Compose a memory context block for prompt injection.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `object[]` | `[]` | Conversation messages `{role, content}` |
| `targetTokens` | `number` | `2000` | Target token budget |
| `categories` | `string[]` | `[]` | Filter by category |
| `query` | `string` | `null` | Search query to bias selection |
| `messageWindow` | `number` | `10` | Recent messages to include |

**Priority order:** PIN → HOT → WARM → COLD

---

## Advanced Tools

### memory_export

Export memories to JSON, Markdown, or CSV.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | `"json" \| "markdown" \| "csv"` | `"json"` | Export format |
| `output` | `string` | `null` | Output file path |
| `category` | `string` | `null` | Filter by category |
| `minImportance` | `number` | `null` | Minimum importance threshold |

---

### memory_dedup

Detect and merge duplicate memories.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | `number` | `0.85` | Similarity threshold 0–1 |
| `dryRun` | `boolean` | `true` | Preview only if true |

---

### memory_qa

Answer questions based on relevant memories (RAG).

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `string` | Question to answer |

---

### memory_profile

Get user profile with static/dynamic separation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scope` | `string` | `"user"` | Scope: `agent`, `user`, `team`, `global` |
| `container_tag` | `string` | `null` | Project/lane tag |
| `entity_filter` | `string` | `null` | Focus on specific entity |
| `static_days` | `number` | `30` | Days without access to mark as static |
| `limit` | `number` | `100` | Max memories to analyze |

---

## Preference & Profile

### memory_preference

Unified preference management.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `get`, `set`, `update`, `merge`, `delete`, `reset`, `stats`, `explain`, `infer` |
| `key` | `string` | Slot key (for get/set/update/delete/explain) |
| `value` | `any` | Slot value (for set/update) |
| `confidence` | `number` | Confidence 0–1 |
| `source` | `string` | `explicit`, `inferred`, `historical` |
| `slots` | `object` | Key-value map (for merge) |
| `messageCount` | `number` | `20` — messages for infer |

---

## Version Control

### memory_version

Version control for memories.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `list`, `diff`, `restore` |
| `memoryId` | `string` | Memory ID (for diff/restore) |
| `versionId` | `string` | Version ID (for diff/restore) |
| `versionId1` | `string` | First version (for diff) |
| `versionId2` | `string` | Second version (for diff) |
| `limit` | `number` | `10` — max versions (for list) |
| `preview` | `boolean` | `false` — preview without restore |

---

## Search Engines

### memory_engine

Unified search engine.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `bm25`, `embed`, `search`, `mmr`, `rerank`, `qmd` |
| `query` | `string` | Query string |
| `text` | `string` | Text to embed |
| `documents` | `object[]` | Documents for mmr/rerank |
| `topK` | `number` | `10` — number of results |
| `build` | `boolean` | `false` — rebuild BM25 index |
| `lambda` | `number` | `0.5` — MMR balance |
| `method` | `enum` | `keyword`, `llm`, `cross` (for rerank) |

### memory_qmd

QMD local file search.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `search`, `get`, `vsearch`, `list`, `status` |
| `query` | `string` | Search query |
| `path` | `string` | File path (for get) |
| `mode` | `enum` | `bm25`, `vector`, `hybrid`, `auto` |

---

## Tier Management

### memory_tier

HOT/WARM/COLD tier management.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `status`, `migrate`, `compress`, `assign`, `partition`, `redistribute` |
| `apply` | `boolean` | `false` — apply changes |
| `memories` | `object[]` | Memories (for assign/partition/compress) |

**Tier thresholds:**
- HOT: ≤ 7 days
- WARM: 7–30 days
- COLD: > 30 days

---

## System Tools

### memory_stats

Memory system statistics.

**Parameters:** None

Returns: total count, categories, tags, tier distribution, scope distribution, quality distribution.

---

### memory_health

Health check for MCP server and dependencies.

**Parameters:** None

Returns: Ollama status, WAL integrity, vector cache completeness, tier distribution, stale memories.

---

### memory_metrics

Operational metrics: search latency, store counts, error rates.

**Parameters:** None

---

### memory_wal

Write-Ahead Log operations.

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `enum` | `init`, `flush`, `list` |
| `runId` | `string` | Run ID (for init) |

---

### memory_pin / memory_unpin / memory_pins

Pin (lock) memories so they are never compressed or deduplicated.

---

## v4.0 Storage Gateway

See [v4 API Reference](./v4.md) for complete `memory_v4_*` tool documentation.

---

## Error Responses

All tools return error responses with `isError: true`:

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```
