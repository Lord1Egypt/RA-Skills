# Design Principles

> Core architectural principles that guide Unified Memory development.

## 🎯 Design Philosophy

Unified Memory is built on five foundational principles:

1. **Reliability First** - Data must never be lost
2. **Performance by Default** - Fast without configuration
3. **Extensibility by Design** - Easy to customize
4. **Simplicity in API** - Easy to learn and use
5. **Transparency** - Clear how data flows

## 📜 Principle 1: Reliability First

### Data Safety

Every write operation is protected:

```javascript
// Atomic write pattern
async function atomicStore(memory) {
  const tx = await beginTransaction();
  try {
    // Write to JSON store
    await writeJson(memory);
    
    // Write to vector store
    await writeVector(memory);
    
    // Write to WAL
    await logToWAL(tx, memory);
    
    // Commit
    await commitTransaction(tx);
  } catch (error) {
    // Rollback on any failure
    await rollbackTransaction(tx);
    throw error;
  }
}
```

### WAL Before Database

The WAL (Write-Ahead Log) is written before any data change:

1. Log the intended operation
2. Apply the operation
3. Mark log entry as committed
4. (Optional) fsync to disk

### Crash Recovery

On startup after crash:

```javascript
async function recover() {
  // Read WAL entries
  const entries = await readWAL();
  
  // Find uncommitted entries
  const uncommitted = entries.filter(e => e.status !== 'COMMITTED');
  
  // Replay or rollback
  for (const entry of uncommitted) {
    if (entry.operation === 'STORE') {
      await applyOperation(entry);
    } else if (entry.operation === 'DELETE') {
      await revertOperation(entry);
    }
  }
}
```

## ⚡ Principle 2: Performance by Default

### Smart Defaults

Systems work well out of the box:

| Setting | Default | Reason |
|---------|--------|--------|
| Search Mode | Hybrid | Best accuracy |
| Cache | Enabled | Fast repeated queries |
| Compression | Tier-based | Balance speed/storage |
| Vector Batch | 100 | Optimal throughput |

### Lazy Operations

Don't do work until needed:

```javascript
// Don't build index until first search
let bm25Index = null;

async function search(query) {
  if (!bm25Index) {
    bm25Index = await buildBM25Index();
  }
  return bm25Index.search(query);
}
```

### Caching Strategy

```
Query → Cache Check → Cache Hit?
                          │
              ┌───────────┴───────────┐
              │ No                    │ Yes
              ▼                       ▼
         Execute Search           Return Cached
              │                       ▲
              ▼                       │
         Store in Cache              │
              │                       │
              └───────────────────────┘
```

## 🔌 Principle 3: Extensibility by Design

### Plugin Hooks

Every operation can be intercepted:

```javascript
// Hook points in memory store
const hooks = {
  beforeStore: [],
  afterStore: [],
  beforeSearch: [],
  afterSearch: []
};

// Execute hooks
async function executeHooks(hookName, ...args) {
  for (const plugin of loadedPlugins) {
    if (plugin.hooks[hookName]) {
      await plugin.hooks[hookName](...args);
    }
  }
}
```

### Separation of Concerns

```
┌─────────────────────────────────────┐
│           Tool Layer                │  ← MCP adapter
├─────────────────────────────────────┤
│          Service Layer              │  ← Business logic
├─────────────────────────────────────┤
│         Storage Layer               │  ← Data persistence
├─────────────────────────────────────┤
│        Infrastructure               │  ← I/O, logging
└─────────────────────────────────────┘
```

### Dependency Rule

- Tools → Services → Storage
- Storage never imports Services
- Services never import Tools

## 🎓 Principle 4: Simplicity in API

### One Function, One Job

```javascript
// Good: Focused functions
await addMemory({ text: "..." });
await searchMemories("query");
await getMemory(id);

// Bad: God functions
await memory({ action: "store", data: {...} });
```

### Consistent Patterns

```javascript
// All mutation operations return the affected entity
const memory = await addMemory({...});
const result = await deleteMemory(id);

// All queries return structured responses
const results = await searchMemories(query);
// { count, results, query, mode }

const stats = await getMemoryStats();
// { total, categories, tags, tiers }
```

### Fail Fast with Clear Errors

```javascript
// Bad: Generic error
throw new Error("Error");

// Good: Specific error with context
throw new MemoryValidationError({
  field: 'text',
  value: '',
  message: 'Memory text cannot be empty'
});
```

## 👁️ Principle 5: Transparency

### Observable Operations

Every operation can be monitored:

```javascript
// Emit events for monitoring
emit('memory:store:start', { id, text });
emit('memory:store:complete', { id, duration });
emit('memory:store:error', { id, error });
```

### Explicit Data Flow

Data movement is traceable:

```
Input → Validation → Processing → Storage → Response
   │         │            │           │
   └─────────┴────────────┴───────────┘
              All steps observable
```

### Configuration Over Magic

```javascript
// Bad: Hidden behavior
await addMemory({ text: "..." }); // What happens to importance?

// Good: Explicit options
await addMemory({ 
  text: "...", 
  importance: 0.5,  // Explicit
  autoExtract: false  // Opt-in behavior
});
```

## 📐 Module Design Rules

### Single Responsibility

Each module has one job:

| Module | Responsibility |
|--------|---------------|
| `storage.js` | JSON file CRUD |
| `vector.js` | Vector operations |
| `bm25.js` | BM25 index |
| `fusion.js` | Result fusion |
| `tools/*.js` | MCP tool adapters |

### Clear Boundaries

```
tools/*.js          → MCP adapter (input/output)
    ↓ imports
service/*.js        → Business logic (no MCP)
    ↓ imports
core/*.js           → Pure logic (no external deps)
    ↓ imports
storage/*.js        → Data access (no business logic)
```

## 🔄 Consistency Guarantees

### ACID for Memory Operations

| Property | Implementation |
|----------|---------------|
| Atomicity | Two-phase commit |
| Consistency | WAL + validation |
| Isolation | Transaction log |
| Durability | fsync on commit |

### Eventual Consistency for Search

- Storage writes are synchronous
- Vector index updates are asynchronous
- Search results may be slightly stale (ms delay)

## 📊 Performance Budgets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Simple search | 45ms | 100ms |
| Hybrid search | 80ms | 200ms |
| Store memory | 50ms | 150ms |
| List memories | 30ms | 100ms |

## 🛡️ Error Handling Philosophy

1. **Fail fast** - Validate early
2. **Recover gracefully** - Rollback transactions
3. **Log thoroughly** - All errors logged
4. **Inform clearly** - User-friendly error messages

## 📚 Next Steps

- [Modules](./modules.md) - Detailed module reference
- [Data Flow](./data-flow.md) - Detailed data flow diagrams
- [Overview](./overview.md) - System architecture
