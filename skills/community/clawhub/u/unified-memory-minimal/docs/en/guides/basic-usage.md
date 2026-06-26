# Basic Usage Guide

> Learn the core operations: storing, searching, listing, and deleting memories.

## 📚 Table of Contents

1. [Adding Memories](#-adding-memories)
2. [Searching Memories](#-searching-memories)
3. [Listing Memories](#-listing-memories)
4. [Getting Single Memory](#-getting-a-single-memory)
5. [Updating Memories](#-updating-memories)
6. [Deleting Memories](#-deleting-memories)
7. [Memory Metadata](#-memory-metadata)

## ➕ Adding Memories

### Basic Add
```javascript
const { addMemory } = require('unified-memory');

const memoryId = await addMemory({
  text: "Remember to call the client tomorrow"
});
```

### With Full Options
```javascript
const memoryId = await addMemory({
  text: "User prefers Python for data analysis",
  category: "preference",
  importance: 0.85,
  tags: ["python", "preference", "data"],
  scope: "USER",
  source: "extraction",
  metadata: {
    project: "analytics",
    confidence: 0.9
  }
});
```

### Adding Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `string` | **required** | Memory content |
| `category` | `string` | `"general"` | Category type |
| `importance` | `number` | `0.5` | Importance 0-1 |
| `tags` | `array` | `[]` | Array of tag strings |
| `scope` | `string` | `null` | Scope: USER, AGENT, TEAM, GLOBAL |
| `source` | `string` | `"manual"` | Source: manual, auto, extraction |
| `metadata` | `object` | `{}` | Custom key-value data |

### Memory Categories

| Category | When to Use |
|----------|-------------|
| `preference` | User preferences, likes, dislikes |
| `fact` | Factual information about the world |
| `decision` | Decisions made, conclusions reached |
| `entity` | People, organizations, places |
| `reflection` | Thoughts, opinions, insights |
| `general` | Default category for misc memories |

## 🔍 Searching Memories

### Simple Search
```javascript
const { searchMemories } = require('unified-memory');

const results = await searchMemories("quarterly reports");
```

### Search Options
```javascript
const results = await searchMemories("project update", {
  mode: "hybrid",      // "hybrid", "bm25", or "vector"
  topK: 10,            // Number of results
  vectorWeight: 0.7,    // Weight for vector search (0-1)
  bm25Weight: 0.3,     // Weight for BM25 search (0-1)
  scope: "USER",       // Filter by scope
  filters: {
    category: "fact",
    tags: ["work"],
    minImportance: 0.5
  }
});
```

### Search Response
```javascript
{
  count: 3,
  query: "quarterly reports",
  mode: "hybrid",
  results: [
    {
      id: "mem_xxx",
      text: "Quarterly reports due on Friday",
      category: "fact",
      importance: 0.9,
      score: 0.923,
      tags: ["work", "deadline"],
      created_at: "2026-04-15T10:00:00Z"
    },
    // ... more results
  ]
}
```

### Search Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `hybrid` | BM25 + Vector + RRF | General use |
| `bm25` | Keyword only | Exact matches |
| `vector` | Semantic only | Conceptual matches |

## 📋 Listing Memories

### List All
```javascript
const { getAllMemories } = require('unified-memory');

const allMemories = await getAllMemories();
```

### List with Filters
```javascript
const memories = await getAllMemories({
  limit: 50,
  offset: 0,
  sortBy: "createdAt",
  sortOrder: "desc",
  filters: {
    category: "preference",
    tags: ["work"],
    scope: "USER"
  }
});
```

### List Response
```javascript
{
  count: 42,
  memories: [
    {
      id: "mem_xxx",
      text: "User prefers...",
      category: "preference",
      importance: 0.8,
      tags: ["work"],
      created_at: "2026-04-15T10:00:00Z"
    }
  ]
}
```

## 🔎 Getting a Single Memory

```javascript
const { getMemory } = require('unified-memory');

const memory = await getMemory("mem_xxx");
```

### Response
```javascript
{
  id: "mem_xxx",
  text: "User prefers Python for data analysis",
  category: "preference",
  importance: 0.85,
  tags: ["python", "preference"],
  scope: "USER",
  source: "extraction",
  metadata: {
    project: "analytics",
    confidence: 0.9
  },
  created_at: "2026-04-15T10:00:00Z",
  updated_at: "2026-04-15T12:00:00Z"
}
```

## ✏️ Updating Memories

### Update Text
```javascript
const { updateMemory } = require('unified-memory');

await updateMemory("mem_xxx", {
  text: "Updated memory content"
});
```

### Update Multiple Fields
```javascript
await updateMemory("mem_xxx", {
  text: "New content",
  importance: 0.9,
  tags: ["updated", "important"]
});
```

## 🗑️ Deleting Memories

### Delete by ID
```javascript
const { deleteMemory } = require('unified-memory');

await deleteMemory("mem_xxx");
```

### Delete with Transaction
```javascript
const { beginTransaction, commitTransaction, deleteMemory } = require('unified-memory');

const tx = await beginTransaction();
await deleteMemory("mem_xxx", { transaction: tx });
await commitTransaction(tx);
```

## 🏷️ Memory Metadata

### What is Metadata?

Metadata is custom data attached to memories:
```javascript
await addMemory({
  text: "Meeting with John",
  metadata: {
    date: "2026-04-20",
    location: "Conference Room A",
    participants: ["John", "Alice"],
    duration: 60 // minutes
  }
});
```

### Querying by Metadata
```javascript
const results = await searchMemories("meeting", {
  filters: {
    metadata: {
      location: "Conference Room A"
    }
  }
});
```

## 📊 Memory Statistics

```javascript
const { getMemoryStats } = require('unified-memory');

const stats = await getMemoryStats();
```

### Stats Response
```javascript
{
  total: 150,
  categories: {
    preference: 45,
    fact: 60,
    decision: 20,
    entity: 15,
    reflection: 10
  },
  tags: {
    work: 42,
    personal: 38,
    project: 25
  },
  tiers: {
    hot: 45,
    warm: 60,
    cold: 45
  },
  scopes: {
    USER: 120,
    AGENT: 20,
    TEAM: 10
  }
}
```

## 🔗 Related Operations

### Pinned Memories
```javascript
const { pinMemory, unpinMemory, getPinnedMemories } = require('unified-memory');

// Pin a memory
await pinMemory("mem_xxx");

// Unpin
await unpinMemory("mem_xxx");

// List pinned
const pinned = await getPinnedMemories();
```

## 🚨 Error Handling

```javascript
const { addMemory, searchMemories } = require('unified-memory');

try {
  await addMemory({ text: "Test memory" });
} catch (error) {
  if (error.code === "STORAGE_ERROR") {
    console.error("Storage failed:", error.message);
  } else if (error.code === "VALIDATION_ERROR") {
    console.error("Invalid input:", error.message);
  }
}
```

## 📚 Next Steps

- [Advanced Usage](./advanced-usage.md) - Version control, dedup, export
- [Plugin Development](./plugins.md) - Extend with plugins
- [API Reference](../api/overview.md) - Complete API docs
