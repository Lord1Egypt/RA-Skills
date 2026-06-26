# Memory Enhancement Engine — API Specification

## `MemorySystem`

Core class with persistent storage to local JSON file.

### Constructor

```javascript
new MemorySystem(config)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `decayHalfLifeHours` | number | 2 | Exponential decay half-life |
| `simWeight` | number | 0.6 | Semantic similarity weight |
| `recencyWeight` | number | 0.4 | Recency weight |
| `storePath` | string | auto | Path to MEMORY_STORE.json |

---

### Methods

#### `add(entry) -> string`
Write a new memory.

- **Input:** `{ content: string, importance?: number (0-2.0), metadata?: object }`
- **Output:** `memory_id` — unique 12-char hex hash
- **Errors:** Empty content → `Error`

#### `query(text, k=5) -> Array`
Semantic search.

- **Input:** `text` — search query string; `k` — max results (1-50)
- **Output:** `[{id, content, importance, score, metadata, created_at, accessed_at, hit_count}, ...]`
- **Scoring:** similarity × simWeight + recency × recencyWeight + hotness × 0.2

#### `recent(n=10) -> Array`
Get N most recently created memories.

#### `get(id) -> object|null`
Get a single memory by ID. Increments hit_count.

#### `delete(id) -> boolean`
Delete memory by ID. Returns true if existed.

#### `compact(groupSize=5, minImportance=0.5) -> Array`
Compact low-importance memories into summaries.

- Groups oldest unaccessed memories, merges their content
- Returns compaction report: `[{group, summary, importance, original_ids}]`

#### `status() -> object`
Engine stats:
```json
{
  "count": 78,
  "storeSize": 30536,
  "decayHalfLifeHours": 2,
  "totalCompactions": 3
}
```
