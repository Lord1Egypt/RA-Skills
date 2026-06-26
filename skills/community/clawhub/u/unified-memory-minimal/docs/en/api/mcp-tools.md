# MCP Tools Reference

> Complete reference for all Unified Memory MCP tools. Based on `src/index.js` v5.2.x.

## Tool Categories

| Category | Tools |
|----------|-------|
| [Core](#core-tools) | `memory_search`, `memory_store`, `memory_list`, `memory_delete`, `memory_get` |
| [Prompt Composition](#prompt-composition) | `memory_compose` |
| [Preference & Profile](#preference--profile) | `memory_preference`, `memory_profile` |
| [Version Control](#version-control) | `memory_version` |
| [Search Engines](#search-engines) | `memory_engine`, `memory_qmd`, `memory_conversation_search` |
| [Extraction & RAG](#extraction--rag) | `memory_extract`, `memory_qa`, `memory_inference`, `memory_summary` |
| [Deduplication & Quality](#deduplication--quality) | `memory_dedup`, `memory_decay` |
| [Tier Management](#tier-management) | `memory_tier` |
| [System Tools](#system-tools) | `memory_stats`, `memory_health`, `memory_metrics`, `memory_wal` |
| [Pins](#pin-tools) | `memory_pin`, `memory_unpin`, `memory_pins` |
| [Export](#export) | `memory_export` |
| [v4 Storage Gateway](#v4-storage-gateway) | `memory_v4_*` |

---

## Core Tools

### memory_search

Hybrid search using BM25 + Vector + RRF fusion. The default search tool.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | **required** | Search query text |
| `topK` | `number` | `5` | Number of results to return |
| `mode` | `string` | `"hybrid"` | Search mode: `"hybrid"`, `"bm25"`, `"vector"` |
| `scope` | `string` | `null` | Scope filter: `"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `vectorWeight` | `number` | `0.7` | Vector weight in hybrid mode (0–1) |
| `bm25Weight` | `number` | `0.3` | BM25 weight in hybrid mode (0–1) |
| `filters` | `object` | `null` | Metadata filters |
| `type` | `string` | `null` | Memory type filter |
| `scene` | `string` | `null` | Scene name filter |

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
      "tier": "HOT",
      "tags": ["python", "work"],
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

Store a new memory. WAL-protected and transcript-logged.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `string` | **required** | Memory content |
| `category` | `string` | `"general"` | Category: `"preference"`, `"fact"`, `"decision"`, `"entity"`, `"reflection"`, `"general"` |
| `importance` | `number` | `0.5` | Importance score 0–1 |
| `tags` | `string[]` | `[]` | Tags for the memory |
| `scope` | `string` | `null` | Scope: `"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `source` | `string` | `"manual"` | Source: `"manual"`, `"auto"`, `"extraction"` |
| `metadata` | `object` | `{}` | Custom metadata |
| `pinned` | `boolean` | `false` | Pin to prevent compression/dedup |

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

**Response:**
```json
{
  "id": "mem_xxx",
  "text": "User prefers morning meetings",
  "category": "preference",
  "importance": 0.8,
  "tags": ["meetings", "schedule"],
  "scope": "USER",
  "pinned": false,
  "tier": "HOT",
  "created_at": "2026-04-20T16:00:00Z"
}
```

**Auto-extraction:** When `category="general"` and `importance > 0.7`, the system automatically extracts structured facts.

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
      "tags": ["work"],
      "scope": "USER",
      "tier": "HOT",
      "pinned": false,
      "access_count": 5,
      "last_accessed": "2026-04-20T10:00:00Z",
      "created_at": "2026-04-15T10:00:00Z",
      "updated_at": "2026-04-18T12:00:00Z"
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
| `id` | `string` | **required** | Memory ID to delete |

**Example:** `{"id": "mem_xxx"}`

**Response:**
```json
{
  "success": true,
  "id": "mem_xxx"
}
```

---

### memory_get

Get a single memory by ID.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | **required** | Memory ID |

**Response:**
```json
{
  "id": "mem_xxx",
  "text": "Memory content",
  "category": "preference",
  "importance": 0.8,
  "tags": ["work"],
  "scope": "USER",
  "source": "manual",
  "metadata": {},
  "tier": "HOT",
  "pinned": false,
  "access_count": 5,
  "last_accessed": "2026-04-20T10:00:00Z",
  "created_at": "2026-04-15T10:00:00Z",
  "updated_at": "2026-04-18T12:00:00Z"
}
```

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

**Example:**
```json
{
  "messages": [
    { "role": "user", "content": "What are my project priorities?" }
  ],
  "targetTokens": 2000,
  "categories": ["preference", "decision"],
  "query": null,
  "messageWindow": 10
}
```

**Response:**
```json
{
  "composed": "== Memory Context (12 memories, ~1600 tokens, 92.5% fill) ==\n[preference|0.9|HOT] User prefers...",
  "total_tokens": 1850,
  "memory_tokens": 1600,
  "context_tokens": 250,
  "remaining": 150,
  "fill_rate": 92.5,
  "count": 12,
  "memories": [
    {
      "id": "mem_xxx",
      "text": "User prefers morning meetings",
      "category": "preference",
      "importance": 0.8,
      "pinned": false,
      "tier": "HOT",
      "tokens": 120
    }
  ],
  "tier_breakdown": { "PIN": 2, "HOT": 5, "WARM": 3, "COLD": 2 }
}
```

---

## Preference & Profile

### memory_preference

Unified preference management with get/set/update/merge/infer actions.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"get"`, `"set"`, `"update"`, `"merge"`, `"delete"`, `"reset"`, `"stats"`, `"explain"`, `"infer"` |
| `key` | `string` | Slot key (for get/set/update/delete/explain) |
| `value` | `any` | Slot value (for set/update) |
| `confidence` | `number` | Confidence 0–1 |
| `source` | `string` | `"explicit"`, `"inferred"`, `"historical"` |
| `slots` | `object` | Key-value map (for merge) |
| `messageCount` | `number` | `20` — messages for infer |

**Examples:**

```json
// Get
{ "action": "get", "key": "language" }

// Set
{ "action": "set", "key": "language", "value": "Python", "confidence": 0.95, "source": "explicit" }

// Update
{ "action": "update", "key": "language", "value": "JavaScript", "confidence": 0.85 }

// Merge
{ "action": "merge", "slots": { "language": { "value": "TypeScript", "confidence": 0.9 }, "editor": { "value": "VS Code", "confidence": 0.95 } } }

// Delete
{ "action": "delete", "key": "old_key" }

// Infer from recent messages
{ "action": "infer", "messageCount": 20 }

// Stats
{ "action": "stats" }

// Explain
{ "action": "explain", "key": "language" }
```

---

### memory_profile

Get user profile with static/dynamic separation.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scope` | `string` | `"user"` | Scope: `"agent"`, `"user"`, `"team"`, `"global"` |
| `container_tag` | `string` | `null` | Project/lane tag |
| `entity_filter` | `string` | `null` | Focus on specific entity |
| `static_days` | `number` | `30` | Days without access to mark as static |
| `limit` | `number` | `100` | Max memories to analyze |

**Response:**
```json
{
  "static": { "name": "User", "company": "Acme Corp" },
  "dynamic": { "current_project": "API redesign", "mood": "productive" },
  "entities": { "colleagues": ["Alice", "Bob"] },
  "count": 42
}
```

---

## Version Control

### memory_version

Version control for memories.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"list"`, `"diff"`, `"restore"` |
| `memoryId` | `string` | Memory ID (for diff/restore) |
| `versionId` | `string` | Version ID (for diff/restore) |
| `versionId1` | `string` | First version (for diff) |
| `versionId2` | `string` | Second version (for diff) |
| `limit` | `number` | `10` | Max versions (for list) |
| `preview` | `boolean` | `false` | Preview without restore |

**Examples:**

```json
// List versions
{ "action": "list", "memoryId": "mem_xxx", "limit": 10 }

// Diff two versions
{ "action": "diff", "memoryId": "mem_xxx", "versionId1": "v1", "versionId2": "v2" }

// Restore a version
{ "action": "restore", "memoryId": "mem_xxx", "versionId": "v1" }
```

---

## Search Engines

### memory_engine

Unified search engine with multiple backends.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"bm25"`, `"embed"`, `"search"`, `"mmr"`, `"rerank"`, `"qmd"` |
| `query` | `string` | Query string |
| `text` | `string` | Text to embed |
| `documents` | `object[]` | Documents for mmr/rerank |
| `topK` | `number` | `10` | Number of results |
| `build` | `boolean` | `false` | Rebuild BM25 index |
| `lambda` | `number` | `0.5` | MMR balance (0=relevance, 1=diversity) |
| `method` | `string` | `keyword`, `llm`, `cross` (for rerank) |

---

### memory_qmd

QMD (local Markdown) file search and indexing.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"search"`, `"get"`, `"vsearch"`, `"list"`, `"status"` |
| `query` | `string` | Search query |
| `path` | `string` | File path (for get) |
| `mode` | `string` | `bm25`, `vector`, `hybrid`, `auto` |

---

### memory_conversation_search

Search within conversation transcripts.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | **required** | Search query |
| `limit` | `number` | `10` | Max results |
| `sessionFilter` | `string` | `null` | Filter by session |
| `dateFilter` | `string` | `null` | Filter by date |

---

## Extraction & RAG

### memory_extract

Extract structured memories from raw text using LLM.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `string` | **required** | Text to extract from |
| `scope` | `string` | Scope filter |
| `agentId` | `string` | Agent ID |

---

### memory_qa

Answer questions based on relevant memories (RAG).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `string` | **required** | Question to answer |

**Response:**
```json
{
  "answer": "Based on your memories, you prefer Python for data science work...",
  "sources": ["mem_xxx", "mem_yyy"],
  "confidence": 0.85
}
```

---

### memory_inference

Infer preferences from recent interactions.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `messageCount` | `number` | Number of recent messages to analyze |
| `scope` | `string` | Scope filter |

---

### memory_summary

Generate a summary of recent memories.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `scope` | `string` | Scope filter |
| `days` | `number` | Days to look back |
| `format` | `string` | `"brief"` or `"detailed"` |

---

## Deduplication & Quality

### memory_dedup

Detect and merge duplicate memories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | `number` | `0.85` | Similarity threshold 0–1 |
| `dryRun` | `boolean` | `true` | Preview only if true |

**Response:**
```json
{
  "duplicate_groups": 3,
  "duplicates_found": 7,
  "dry_run": true,
  "groups": [
    {
      "id": "mem_xxx",
      "duplicates": ["mem_yyy", "mem_zzz"],
      "similarity": 0.92,
      "text": "User prefers Python"
    }
  ]
}
```

---

### memory_decay

Apply time-based importance decay to memories.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `halfLife` | `number` | `30` | Days for importance to halve |
| `apply` | `boolean` | `false` | Apply changes or preview |

---

## Tier Management

### memory_tier

HOT/WARM/COLD tier management.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"status"`, `"migrate"`, `"compress"`, `"assign"`, `"partition"`, `"redistribute"` |
| `apply` | `boolean` | `false` | Apply changes |
| `memories` | `object[]` | Memories (for assign/partition/compress) |

**Tier thresholds:**

| Tier | Criteria |
|------|----------|
| HOT | ≤ 7 days since last access |
| WARM | 7–30 days |
| COLD | > 30 days |

**Examples:**

```json
// Status
{ "action": "status" }

// Migrate
{ "action": "migrate", "apply": true }

// Compress cold tier
{ "action": "compress", "apply": false }

// Assign specific memories
{ "action": "assign", "memories": [{ "id": "mem_xxx", "tier": "HOT" }], "apply": true }

// Partition
{ "action": "partition", "apply": true }

// Redistribute
{ "action": "redistribute", "apply": true }
```

---

## System Tools

### memory_stats

Memory system statistics. **Parameters:** None

**Response:**
```json
{
  "total": 150,
  "categories": { "preference": 45, "fact": 60, "decision": 20, "entity": 15, "reflection": 10 },
  "tags": { "work": 42, "personal": 38 },
  "tiers": { "hot": 45, "warm": 60, "cold": 45 },
  "scopes": { "USER": 120, "AGENT": 20, "TEAM": 10 },
  "pinned": 5,
  "avg_importance": 0.62,
  "wal": { "pending_ops": 0, "status": "healthy" }
}
```

---

### memory_health

Health check for MCP server and all dependencies.

**Parameters:** None

**Response:**
```json
{
  "status": "healthy",
  "ollama": { "available": true, "model": "nomic-embed-text" },
  "wal": { "integrity": "ok", "pending_ops": 0 },
  "vector_cache": { "completeness": 1.0 },
  "tier_distribution": { "hot": 45, "warm": 60, "cold": 45 },
  "stale_memories": 0
}
```

---

### memory_metrics

Operational metrics: search latency, store counts, error rates.

**Parameters:** None

**Response:**
```json
{
  "search": {
    "total": 1234,
    "avg_latency_ms": 45,
    "by_mode": { "hybrid": 1000, "bm25": 200, "vector": 34 }
  },
  "store": {
    "total": 567,
    "by_source": { "manual": 400, "auto": 100, "extraction": 67 }
  },
  "errors": {
    "total": 12,
    "by_type": { "storage": 5, "embedding": 4, "search": 3 }
  }
}
```

---

### memory_wal

Write-Ahead Log operations.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | **required** | Action: `"init"`, `"flush"`, `"list"`, `"status"`, `"export"`, `"import"`, `"repair"` |
| `runId` | `string` | Run ID (for init) |
| `path` | `string` | File path (for export/import) |

---

## Pin Tools

### memory_pin

Pin a memory to prevent compression or deduplication.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | **required** | Memory ID to pin |

---

### memory_unpin

Unpin a memory.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | **required** | Memory ID to unpin |

---

### memory_pins

List all pinned memories. **Parameters:** None

**Response:**
```json
{
  "count": 5,
  "memories": [
    {
      "id": "mem_xxx",
      "text": "Critical user preference...",
      "pinned_at": "2026-04-10T10:00:00Z"
    }
  ]
}
```

---

## Export

### memory_export

Export memories to JSON, Markdown, or CSV.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | `string` | `"json"` | Format: `"json"`, `"markdown"`, `"csv"` |
| `output` | `string` | `null` | Output file path |
| `category` | `string` | `null` | Filter by category |
| `minImportance` | `number` | `null` | Minimum importance threshold |
| `scope` | `string` | `null` | Scope filter |

---

## v4 Storage Gateway

### memory_v4_read

Read from v4.0 storage format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `string` | Storage key |
| `scope` | `string` | Scope filter |

---

### memory_v4_write

Write to v4.0 storage format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `string` | Storage key |
| `value` | `any` | Value to store |
| `scope` | `string` | Scope filter |

---

### memory_v4_delete

Delete from v4.0 storage.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `string` | Storage key |
| `scope` | `string` | Scope filter |

---

### memory_v4_list

List v4.0 storage keys.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `scope` | `string` | Scope filter |
| `prefix` | `string` | Key prefix filter |

---

## Entity & Identity Tools

### memory_entity_extract

Extract named entities from memories.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `string` | Text to extract from |
| `types` | `string[]` | Entity types: `"person"`, `"org"`, `"location"`, `"concept"` |

---

### memory_entity_link

Link entities across memories.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `entity` | `string` | Entity name |
| `memoryIds` | `string[]` | Memory IDs to link |

---

### memory_identity_get

Get current user identity information.

**Parameters:** None

---

### memory_identity_update

Update user identity information.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `field` | `string` | Identity field to update |
| `value` | `any` | New value |

---

## Git Notes

### memory_gitnotes_backup

Backup memories as Git notes.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `repo` | `string` | Git repository path |
| `branch` | `string` | Branch name |

---

### memory_gitnotes_restore

Restore memories from Git notes.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `repo` | `string` | Git repository path |
| `branch` | `string` | Branch name |

---

## Error Responses

All tools return error responses with `isError: true`:

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```

**Common error messages:**

| Error | Cause |
|-------|-------|
| `Memory not found` | ID does not exist |
| `Validation error: text is required` | Required field missing |
| `Embedding service unavailable` | Ollama/OpenAI not configured |
| `WAL corruption detected` | WAL log is corrupted; run repair |
| `Transaction conflict` | Concurrent modification |
