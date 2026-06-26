# Core API Reference

> JavaScript SDK — complete reference for all Unified Memory core modules.

## Installation

```bash
npm install unified-memory
```

```javascript
// ES Modules
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// CommonJS
const { addMemory, searchMemories, getAllMemories } = require('unified-memory');
```

---

## Memory Functions

### addMemory(memory, options?)

Stores a new memory. Automatically WAL-logged.

```javascript
const id = await addMemory({
  text: "User preference for Python",
  category: "preference",
  importance: 0.9,
  tags: ["python", "preference"],
  scope: "USER",
  source: "extraction",
  metadata: { project: "data" }
}, { transaction: tx });
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `memory.text` | `string` | Yes | Memory content |
| `memory.category` | `string` | No | `preference`, `fact`, `decision`, `entity`, `reflection`, `general` (default) |
| `memory.importance` | `number` | No | 0.0–1.0 (default: 0.5) |
| `memory.tags` | `string[]` | No | Tag strings for filtering |
| `memory.scope` | `string` | No | `USER`, `AGENT`, `TEAM`, `GLOBAL` |
| `memory.source` | `string` | No | `manual`, `auto`, `extraction` (default: `manual`) |
| `memory.metadata` | `object` | No | Custom key-value data |
| `memory.pinned` | `boolean` | No | If true, never compressed/deduped |
| `options.transaction` | `Transaction` | No | Transaction context |

**Returns:** `string` — Memory ID (format: `mem_xxx`)

**Errors:** `MemoryValidationError` if text is empty; `StorageError` on write failure.

---

### searchMemories(query, options?)

Hybrid search combining BM25 + vector + RRF fusion.

```javascript
const results = await searchMemories("quarterly reports", {
  mode: "hybrid",
  topK: 10,
  vectorWeight: 0.7,
  bm25Weight: 0.3,
  scope: "USER",
  filters: {
    category: "fact",
    tags: ["work"],
    importance: { min: 0.5 }
  }
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | Required | Search query text |
| `options.mode` | `string` | `"hybrid"` | `hybrid`, `bm25`, `vector` |
| `options.topK` | `number` | `5` | Number of results to return |
| `options.vectorWeight` | `number` | `0.7` | Vector weight in hybrid mode |
| `options.bm25Weight` | `number` | `0.3` | BM25 weight in hybrid mode |
| `options.scope` | `string` | `null` | Scope filter |
| `options.filters` | `object` | `null` | Metadata filters |
| `options.filters.category` | `string` | — | Filter by category |
| `options.filters.tags` | `string[]` | — | Filter by tags (AND logic) |
| `options.filters.importance.min` | `number` | — | Minimum importance |
| `options.filters.importance.max` | `number` | — | Maximum importance |
| `options.type` | `string` | `null` | Memory type filter |
| `options.scene` | `string` | `null` | Scene name filter |

**Returns:**
```javascript
{
  count: 3,
  query: "quarterly reports",
  mode: "hybrid",
  results: [
    {
      id: "mem_xxx",
      text: "Memory text",
      category: "fact",
      importance: 0.8,
      score: 0.923,
      tags: ["work"],
      tier: "HOT",
      created_at: "2026-04-15T10:00:00Z"
    }
  ]
}
```

---

### getAllMemories(options?)

List all memories with optional filters and pagination.

```javascript
const all = await getAllMemories({
  limit: 50,
  offset: 0,
  sortBy: "created_at",
  sortOrder: "desc",
  filters: {
    category: "preference",
    scope: "USER"
  }
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `options.limit` | `number` | `100` | Maximum results |
| `options.offset` | `number` | `0` | Pagination offset |
| `options.sortBy` | `string` | `"created_at"` | Sort field: `created_at`, `importance`, `updated_at` |
| `options.sortOrder` | `string` | `"desc"` | `asc` or `desc` |
| `options.filters` | `object` | `null` | Same structure as searchMemories |
| `options.transaction` | `Transaction` | No | Transaction context |

**Returns:**
```javascript
{
  count: 42,
  memories: [/* Memory objects */]
}
```

---

### getMemory(id)

Retrieve a single memory by ID.

```javascript
const memory = await getMemory("mem_xxx");
```

**Parameters:** `id: string` — Memory ID

**Returns:** `Memory` object or `null` if not found.

---

### updateMemory(id, updates, options?)

Update specific fields of a memory.

```javascript
await updateMemory("mem_xxx", {
  text: "Updated content",
  importance: 0.9,
  tags: ["updated"],
  pinned: true
});
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | Memory ID |
| `updates` | `object` | Fields to update (partial update) |
| `options.transaction` | `Transaction` | Transaction context |

**Returns:** `void`

**Updatable fields:** `text`, `category`, `importance`, `tags`, `scope`, `metadata`, `pinned`

---

### deleteMemory(id, options?)

Delete a memory. WAL-logged and transcript-logged.

```javascript
await deleteMemory("mem_xxx");
await deleteMemory("mem_xxx", { transaction: tx });
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | `string` | Memory ID |
| `options.transaction` | `Transaction` | Transaction context |

**Returns:** `void`

---

### touchMemory(id)

Update `last_accessed` timestamp without returning data. Used to promote tier.

```javascript
await touchMemory("mem_xxx");
```

---

### saveMemories(memories)

Bulk save (replace) the entire memory store. Used internally and for migrations.

```javascript
await saveMemories(memoryArray);
```

---

## Transaction Functions

### beginTransaction()

Start a new ACID transaction.

```javascript
const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (error) {
  await rollbackTransaction(tx);
}
```

**Returns:** `Transaction` object

---

### commitTransaction(tx)

Commit a transaction atomically.

```javascript
await commitTransaction(tx);
```

---

### rollbackTransaction(tx)

Roll back all changes in the transaction.

```javascript
await rollbackTransaction(tx);
```

---

## Profile & Preference Functions

### memoryProfile(options)

Get aggregated user profile with static/dynamic separation.

```javascript
const profile = await memoryProfile({
  scope: "user",
  container_tag: "project-x",
  entity_filter: "preferences",
  static_days: 30,
  limit: 100
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `options.scope` | `string` | `"user"` | `agent`, `user`, `team`, `global` |
| `options.container_tag` | `string` | `null` | Project/lane tag filter |
| `options.entity_filter` | `string` | `null` | Focus on specific entity |
| `options.static_days` | `number` | `30` | Days without access to mark as static |
| `options.limit` | `number` | `100` | Max memories to analyze |

**Returns:**
```javascript
{
  static: { /* long-lived facts */ },
  dynamic: { /* frequently updated */ },
  entities: { /* known entities */ },
  count: 42
}
```

---

### memoryPreference(params)

Unified preference management with get/set/update/merge/infer actions.

```javascript
// Get a preference
const pref = await memoryPreference({ action: "get", key: "language" });

// Set a preference
await memoryPreference({
  action: "set",
  key: "language",
  value: "Python",
  confidence: 0.95,
  source: "explicit"
});

// Update
await memoryPreference({
  action: "update",
  key: "language",
  value: "JavaScript",
  confidence: 0.85
});

// Merge multiple
await memoryPreference({
  action: "merge",
  slots: {
    language: { value: "TypeScript", confidence: 0.9 },
    editor: { value: "VS Code", confidence: 0.95 }
  }
});

// Delete
await memoryPreference({ action: "delete", key: "old_key" });

// Infer from recent messages
const inferred = await memoryPreference({ action: "infer", messageCount: 20 });

// Get stats
const stats = await memoryPreference({ action: "stats" });

// Explain a slot
const explanation = await memoryPreference({ action: "explain", key: "language" });
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | `get`, `set`, `update`, `merge`, `delete`, `reset`, `stats`, `explain`, `infer` |
| `key` | `string` | Slot key (for get/set/update/delete/explain) |
| `value` | `any` | Slot value (for set/update) |
| `confidence` | `number` | Confidence 0–1 |
| `source` | `string` | `explicit`, `inferred`, `historical` |
| `slots` | `object` | Key-value map (for merge) |
| `messageCount` | `number` | `20` — messages for infer action |

---

## Search Functions

### hybridSearch(query, topK, mode)

Hybrid search using BM25 + vector + RRF.

```javascript
const results = await hybridSearch("quarterly reports", 10, "hybrid");
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | Required | Search query |
| `topK` | `number` | `5` | Number of results |
| `mode` | `string` | `"hybrid"` | `hybrid`, `bm25`, `vector` |

---

### bm25Search(query, topK)

Pure BM25/FTS5 keyword search.

```javascript
const results = await bm25Search("quarterly reports", 10);
```

---

### vectorSearch(queryEmbedding, topK)

Pure vector similarity search.

```javascript
const results = await vectorSearch(queryEmbedding, 10);
```

---

### mmrSelect(documents, queryEmbedding, lambda, topK)

Maximal Marginal Relevance selection for diverse results.

```javascript
const selected = await mmrSelect(documents, queryEmbedding, 0.5, 5);
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `documents` | `object[]` | Required | Documents with embedding field |
| `queryEmbedding` | `number[]` | Required | Query embedding vector |
| `lambda` | `number` | `0.5` | Balance factor (0=relevance, 1=diversity) |
| `topK` | `number` | Required | Number to select |

---

### rerankResults(query, documents, method)

Rerank search results using cross-encoder or keyword methods.

```javascript
const reranked = await rerankResults("query", documents, "keyword");
const reranked = await rerankResults("query", documents, "llm");
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `string` | Required | Search query |
| `documents` | `object[]` | Required | Documents to rerank |
| `method` | `string` | `"keyword"` | `keyword`, `llm`, `cross` |

---

## Prompt Composition

### memoryCompose(params)

Compose a memory context block for prompt injection.

```javascript
const result = await memoryCompose({
  messages: [
    { role: "user", content: "What are my project priorities?" }
  ],
  targetTokens: 2000,
  categories: ["preference", "decision"],
  query: null,
  messageWindow: 10
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `messages` | `object[]` | `[]` | Conversation messages `{role, content}` |
| `targetTokens` | `number` | `2000` | Max tokens for memory context |
| `categories` | `string[]` | `[]` | Category filter |
| `query` | `string` | `null` | Search query to bias selection |
| `messageWindow` | `number` | `10` | Recent messages to include |

**Priority order:** PIN → HOT → WARM → COLD

**Returns:**
```javascript
{
  composed: "== Memory Context ... ==",
  total_tokens: 1850,
  memory_tokens: 1600,
  context_tokens: 250,
  remaining: 150,
  fill_rate: 92.5,
  count: 12,
  memories: [/* Memory objects with tier info */],
  tier_breakdown: { PIN: 2, HOT: 5, WARM: 3, COLD: 2 }
}
```

---

## Utility Functions

### getMemoryStats()

Get comprehensive memory system statistics.

```javascript
const stats = await getMemoryStats();
```

**Returns:**
```javascript
{
  total: 150,
  categories: { preference: 45, fact: 60, decision: 20, entity: 15, reflection: 10 },
  tags: { work: 42, personal: 38, python: 15 },
  tiers: { hot: 45, warm: 60, cold: 45 },
  scopes: { USER: 120, AGENT: 20, TEAM: 10 },
  pinned: 5,
  avg_importance: 0.62,
  search_stats: { total_searches: 1234, avg_latency_ms: 45 }
}
```

---

### memoryExport(params)

Export memories to file in various formats.

```javascript
const result = await memoryExport({
  format: "json",          // json | markdown | csv
  output: "~/memories.json",
  category: null,
  minImportance: 0.5
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | `string` | `"json"` | Export format |
| `output` | `string` | `null` | Output file path |
| `category` | `string` | `null` | Filter by category |
| `minImportance` | `number` | `null` | Minimum importance threshold |

---

### memoryDedup(params)

Detect and merge duplicate memories using similarity detection.

```javascript
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: true
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `threshold` | `number` | `0.85` | Similarity threshold 0–1 |
| `dryRun` | `boolean` | `true` | Preview only if true |

**Returns:**
```javascript
{
  duplicate_groups: 3,
  duplicates_found: 7,
  estimated_merge_tokens_saved: 350,
  dry_run: true,
  groups: [
    { id: "mem_xxx", duplicates: ["mem_yyy", "mem_zzz"], similarity: 0.92 }
  ]
}
```

---

### askQuestion(question)

Answer a question using relevant memories as context (RAG).

```javascript
const answer = await askQuestion("What is the user's preferred language?");
```

---

## Tier Functions

### partitionByTier(memories)

Partition an array of memories into HOT/WARM/COLD tiers.

```javascript
const tiers = partitionByTier(memories);
// { HOT: [...], WARM: [...], COLD: [...] }
```

**Tier thresholds (default):**

| Tier | Criteria |
|------|----------|
| HOT | Last accessed ≤ 7 days |
| WARM | Last accessed 7–30 days |
| COLD | Last accessed > 30 days |

---

### assignTiers(apply?)

Recalculate and reassign tiers for all memories.

```javascript
await assignTiers(false); // Preview
await assignTiers(true);  // Apply changes
```

---

### redistributeTiers(options)

Redistribute memories across tiers to optimize storage.

```javascript
await redistributeTiers({ targetHot: 50, targetWarm: 100, apply: false });
```

---

### compressColdTier(options)

Compress cold tier memories to reduce storage.

```javascript
await compressColdTier({ batchSize: 50, apply: false });
```

---

## Version Functions

### memoryVersion(params)

Version control operations for memory history.

```javascript
// List versions
const versions = await memoryVersion({
  action: "list",
  memoryId: "mem_xxx",
  limit: 10
});

// Compare two versions
const diff = await memoryVersion({
  action: "diff",
  memoryId: "mem_xxx",
  versionId1: "v1",
  versionId2: "v2"
});

// Restore a version
await memoryVersion({
  action: "restore",
  memoryId: "mem_xxx",
  versionId: "v1"
});
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `string` | `list`, `diff`, `restore` |
| `memoryId` | `string` | Memory ID |
| `versionId` | `string` | Version ID (for diff/restore) |
| `versionId1` | `string` | First version (for diff) |
| `versionId2` | `string` | Second version (for diff) |
| `limit` | `number` | `10` — max versions to return |
| `preview` | `boolean` | `false` — preview without restore |

---

## Pin Functions

### pinMemory(id)

Pin a memory to prevent compression or deduplication.

```javascript
await pinMemory("mem_xxx");
```

---

### unpinMemory(id)

Remove pin from a memory.

```javascript
await unpinMemory("mem_xxx");
```

---

### getPinnedMemories()

List all pinned memories.

```javascript
const pinned = await getPinnedMemories();
```

---

## Extraction & Learning

### extractMemories(text, options?)

Extract structured memories from raw text using LLM.

```javascript
const extracted = await extractMemories(
  "User prefers Python for data science work. They work at Acme Corp.",
  { scope: "USER" }
);
```

---

### batchExtract(texts, options?)

Batch extract memories from multiple text entries.

```javascript
const results = await batchExtract(textArray, { scope: "USER" });
```

---

### analyzeInsights(query)

Analyze memories to generate insights and patterns.

```javascript
const insights = await analyzeInsights("user work patterns");
```

---

## WAL (Write-Ahead Log)

### walWrite(operation, data)

Write an operation to the WAL.

```javascript
await walWrite("addMemory", { id: "mem_xxx", text: "..." });
```

---

### walReplay(runId?)

Replay WAL operations to recover state.

```javascript
await walReplay("run-123");
```

---

### walStatus()

Get WAL status and integrity information.

```javascript
const status = await walStatus();
// { pending_ops: 5, last_flush: "...", corrupted: false }
```

---

### walExport(path), walImport(path)

Export/import WAL for backup and migration.

```javascript
await walExport("/tmp/wal-backup.jsonl");
await walImport("/tmp/wal-backup.jsonl");
```

---

## Error Handling

```javascript
import {
  addMemory,
  MemoryValidationError,
  StorageError,
  TransactionError,
  SearchError,
} from 'unified-memory';

try {
  await addMemory({ text: "Test" });
} catch (error) {
  switch (error.constructor) {
    case MemoryValidationError:
      console.error("Invalid memory:", error.field, error.value);
      break;
    case StorageError:
      console.error("Storage failed:", error.message);
      break;
    case TransactionError:
      console.error("Transaction failed:", error.message);
      break;
    case SearchError:
      console.error("Search failed:", error.message);
      break;
  }
}
```

---

## TypeScript Types

```typescript
interface Memory {
  id: string;
  text: string;
  category: 'preference' | 'fact' | 'decision' | 'entity' | 'reflection' | 'general';
  importance: number;
  tags: string[];
  scope: 'USER' | 'AGENT' | 'TEAM' | 'GLOBAL' | null;
  source: 'manual' | 'auto' | 'extraction';
  metadata: Record<string, any>;
  tier: 'HOT' | 'WARM' | 'COLD';
  pinned: boolean;
  access_count: number;
  last_accessed: string;
  created_at: string;
  updated_at: string;
}

interface SearchResult {
  id: string;
  text: string;
  category: string;
  importance: number;
  score: number;
  tags: string[];
  tier: string;
  created_at: string;
}

interface SearchResponse {
  count: number;
  query: string;
  mode: string;
  results: SearchResult[];
  token_budget?: {
    used_tokens: number;
    max_tokens: number;
    remaining_tokens: number;
    percent_used: number;
  };
}

interface Transaction {
  id: string;
  operations: Operation[];
  started_at: string;
}
```
