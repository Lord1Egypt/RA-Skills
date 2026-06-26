# API Overview

> Unified Memory API reference — design principles, calling conventions, and error handling.

## Architecture

Unified Memory provides three API surfaces:

| Surface | Protocol | Description |
|---------|----------|-------------|
| **MCP Tools** | JSON-RPC 2.0 / stdio | Agent-callable tools registered with the Model Context Protocol server |
| **JavaScript SDK** | ES Modules / CommonJS | Direct in-process function calls (`addMemory`, `searchMemories`, etc.) |
| **Python MCP Server** | FastMCP / stdio | Python-based MCP server for Python-first integrations |

All three surfaces share the same underlying memory engine.

---

## Design Principles

### 1. Fail-Safe by Default

Every store/delete operation is Write-Ahead Log (WAL) protected. If a write fails mid-operation, the WAL ensures the operation can be recovered or replayed.

```javascript
// Storage is transactional; failures roll back automatically
await addMemory({ text: "..." }); // WAL-logged automatically
```

### 2. Hierarchical Memory Model

Memories are automatically organized into tiers based on access recency:

| Tier | Criteria | Behavior |
|------|----------|----------|
| **PIN** | `pinned: true` | Never compressed or deduplicated |
| **HOT** | ≤ 7 days since last access | Full fidelity, fastest retrieval |
| **WARM** | 7–30 days | Kept in working set |
| **COLD** | > 30 days | Compressed, lower retrieval priority |

Priority order in retrieval: **PIN → HOT → WARM → COLD**

### 3. Scope Isolation

Four scope levels control which agent/user can access a memory:

| Scope | Access |
|-------|--------|
| `USER` | Current user's private memories |
| `AGENT` | Agent-specific memories |
| `TEAM` | Shared across a team |
| `GLOBAL` | Visible to all agents and users |

Scope hierarchy: `USER` ⊂ `TEAM` ⊂ `GLOBAL` (more specific scopes inherit from broader ones).

### 4. Hybrid Search

Default search mode combines three strategies via **Reciprocal Rank Fusion (RRF)**:

1. **BM25 / FTS5** — keyword exact match
2. **Vector embedding** — semantic similarity
3. **RRF merge** — rank fusion combining both signals

```javascript
// Search modes
hybridSearch(query, topK)   // Default: BM25 + vector + RRF
bm25Search(query, topK)      // Keywords only
vectorSearch(query, topK)   // Embedding only
```

### 5. Atomic Transactions

Multi-step operations can be wrapped in transactions:

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

---

## Calling Conventions

### MCP Tools (JSON-RPC)

All tools follow the MCP JSON-RPC 2.0 convention:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_search",
    "arguments": {
      "query": "user preferences",
      "topK": 5,
      "mode": "hybrid"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"count\": 3, \"results\": [...], \"token_budget\": {...}}"
    }]
  }
}
```

### JavaScript SDK

```javascript
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// Store
const id = await addMemory({ text: "User prefers Python", category: "preference", importance: 0.9 });

// Search
const results = await searchMemories("programming language", { mode: "hybrid", topK: 5 });

// List
const all = await getAllMemories({ filters: { category: "preference" } });
```

---

## Memory Data Model

```typescript
interface Memory {
  id: string;                    // Unique ID (format: mem_xxx)
  text: string;                  // Memory content
  category: MemoryCategory;      // preference | fact | decision | entity | reflection | general
  importance: number;             // 0.0 – 1.0
  tags: string[];                // User-defined tags
  scope: Scope | null;           // USER | AGENT | TEAM | GLOBAL
  source: Source;                 // manual | auto | extraction
  metadata: Record<string, any>;  // Custom fields
  tier: Tier;                    // HOT | WARM | COLD (auto-assigned)
  pinned: boolean;               // Locked — never compressed/deduped
  access_count: number;          // Number of times accessed
  last_accessed: string;         // ISO 8601 timestamp
  created_at: string;            // ISO 8601 timestamp
  updated_at: string;            // ISO 8601 timestamp
}

type MemoryCategory = 'preference' | 'fact' | 'decision' | 'entity' | 'reflection' | 'general';
type Scope = 'USER' | 'AGENT' | 'TEAM' | 'GLOBAL';
type Source = 'manual' | 'auto' | 'extraction';
type Tier = 'HOT' | 'WARM' | 'COLD';
```

---

## Error Handling

### Error Response Format

All MCP tools return errors with `isError: true`:

```json
{
  "content": [{ "type": "text", "text": "Error description" }],
  "isError": true
}
```

### SDK Error Types

```javascript
import {
  MemoryValidationError,  // Invalid memory fields
  StorageError,           // File/JSON/transaction failures
  TransactionError,       // Transaction commit/rollback failures
  SearchError,            // Query processing failures
} from 'unified-memory';

try {
  await addMemory({ text: "..." });
} catch (error) {
  if (error instanceof MemoryValidationError) {
    console.error("Invalid field:", error.field, error.value);
  } else if (error instanceof StorageError) {
    console.error("Storage failed:", error.message);
  } else if (error instanceof TransactionError) {
    console.error("Transaction failed:", error.message);
  } else if (error instanceof SearchError) {
    console.error("Search failed:", error.message);
  }
}
```

### Common Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| `MEMORY_NOT_FOUND` | Memory ID does not exist | Check the ID is correct |
| `VALIDATION_ERROR` | Invalid field value | Fix field per schema |
| `STORAGE_ERROR` | File system or JSON error | Check disk space / permissions |
| `TRANSACTION_CONFLICT` | Concurrent modification | Retry or use transactions |
| `EMBEDDING_UNAVAILABLE` | No embedding provider | Configure Ollama or OpenAI |
| `WAL_CORRUPT` | WAL log is corrupted | Run `memory_wal` repair |
| `TIER_THRESHOLD_INVALID` | Invalid tier parameters | Check tier config values |

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MEMORY_STORAGE_PATH` | `~/.unified-memory` | Root storage directory |
| `MEMORY_VECTOR_DB` | `lancedb` | Vector backend: `lancedb`, `chromadb` |
| `MEMORY_EMBEDDING_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `MEMORY_LLM_MODEL` | (none) | LLM for extraction/summarization |
| `MEMORY_MAX_TOKEN_BUDGET` | `2000` | Max tokens per prompt injection |
| `MEMORY_WAL_ENABLED` | `true` | Enable Write-Ahead Log |

### Feature Flags

```javascript
const config = {
  // Storage
  storagePath: '~/.unified-memory',
  maxMemorySize: 50000,

  // Search
  vectorWeight: 0.7,
  bm25Weight: 0.3,
  rrfK: 60,

  // Tier thresholds (in days)
  tierHotDays: 7,
  tierWarmDays: 30,

  // WAL
  walEnabled: true,
  walFlushInterval: 5000,
};
```

---

## Token Budget

Token budgets control how much memory context is injected into prompts:

```javascript
const result = await memoryCompose({
  messages,          // Recent conversation
  targetTokens: 2000, // Max tokens for memory context
  categories: [],    // Filter (e.g. ['preference', 'decision'])
  query: null,       // Search query to bias selection
  messageWindow: 10, // Recent messages to include
});
```

Returns:
```javascript
{
  composed: "== Memory Context ... ==",
  total_tokens: 1850,
  memory_tokens: 1600,
  context_tokens: 250,
  remaining: 150,
  fill_rate: 92.5,
  count: 12,
  memories: [...],
  tier_breakdown: { PIN: 2, HOT: 5, WARM: 3, COLD: 2 }
}
```

---

## Next Steps

- [MCP Tools Reference](./mcp-tools.md) — All callable tools
- [Core API Reference](./core-api.md) — JavaScript SDK functions
- [Plugin API Reference](./plugin-api.md) — Build plugins with hooks
