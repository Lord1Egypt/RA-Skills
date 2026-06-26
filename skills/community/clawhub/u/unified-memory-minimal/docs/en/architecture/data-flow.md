# Data Flow

> How data moves through Unified Memory from input to storage and back.

## 📚 Table of Contents

1. [Store Flow](#store-memory-flow)
2. [Search Flow](#search-memory-flow)
3. [Delete Flow](#delete-memory-flow)
4. [Update Flow](#update-memory-flow)
5. [Recovery Flow](#crash-recovery-flow)

## Store Memory Flow

### High-Level Flow

```
Client Request: memory_store({ text, category, tags, metadata })
    │
    ▼
Tool Adapter (src/tools/memory_store.js)
    │ - Validate parameters
    │ - Generate ID
    │ - Set timestamps
    └─┬
      │
      ▼
Plugin Hooks (beforeStore)
    │ - Transform memory
    │ - Validate
    └─┬
      │
      ▼
Memory Service
    │ - Coordinate storage
    │ - Handle transactions
    └─┬
      │
      ├────────────┬────────────┐
      ▼            ▼            ▼
JSON Store    Vector Store   WAL Logger
(sync)        (async)        (sync)
      │            │            │
      └────────────┴────────────┘
                    │
                    ▼
Plugin Hooks (afterStore)
    │ - Sync external
    │ - Emit events
    └─┬
      │
      ▼
Response: { success: true, id: 'mem_xxx' }
```

### Transaction Flow

```
┌─────────────────────────────────────────┐
│           Begin Transaction            │
│           txId = WAL.nextId()          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           Phase 1: Prepare              │
│  WAL.log({ txId, PENDING, operation })  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           Phase 2: Execute              │
│  storage.addMemory(memory)              │
│  vectorStore.addVector(id, text)        │
└─────────────────┬───────────────────────┘
                  │
          ┌───────┴───────┐
          │ Success       │ Failure
          ▼               ▼
┌──────────────┐  ┌──────────────────────┐
│ WAL.commit() │  │ WAL.rollback()       │
│ fsync()      │  │ storage.revert()    │
└──────────────┘  │ vectorStore.revert() │
                  └──────────────────────┘
```

## Search Memory Flow

```
Client: memory_search({ query, mode, topK, filters })
    │
    ▼
Tool Adapter (validate + parse)
    │
    ▼
Plugin Hooks (beforeSearch)
    │
    ▼
Cache Check
    │
    ├─ Cache Hit → Return cached results
    │
    └─ Cache Miss → Hybrid Search
                        │
                        ├─────────────────┐
                        ▼                 ▼
                   BM25 Search      Vector Search
                        │                 │
                        └────────┬────────┘
                                 ▼
                          RRF Fusion
                                 │
                                 ▼
                          Apply Filters
                                 │
                                 ▼
                          Cache Results
                                 │
                                 ▼
Plugin Hooks (afterSearch)
    │
    ▼
Response: { count, results, query, mode }
```

### RRF Formula

Reciprocal Rank Fusion combines rankings:

```
RRF_score(doc) = Σ(weight_i / (k + rank_i(doc)))

Where k = 60 (constant)
      weight_i = weight for algorithm i
      rank_i = rank from algorithm i
```

## Delete Memory Flow

```
Client: memory_delete({ id })
    │
    ▼
Plugin Hooks (beforeDelete)
    │
    ▼
WAL.log({ txId, DELETE, id })
    │
    ▼
storage.delete(id)        // Mark as deleted
vectorStore.delete(id)    // Remove vector
    │
    ▼
WAL.commit(txId)
    │
    ▼
Plugin Hooks (afterDelete)
    │
    ▼
Response: { success: true }
```

## Update Memory Flow

```
Client: memory_update({ id, ...updates })
    │
    ▼
Plugin Hooks (beforeUpdate)
    │
    ▼
WAL.log({ txId, UPDATE, id, updates })
    │
    ▼
storage.update(id, updates)
vectorStore.update(id, newText)  // If text changed
    │
    ▼
WAL.commit(txId)
    │
    ▼
Plugin Hooks (afterUpdate)
    │
    ▼
Response: { success: true, memory }
```

## Crash Recovery Flow

```
System Startup
    │
    ▼
Read WAL entries
    │
    ▼
Find uncommitted transactions
    │
    ▼
For each uncommitted tx:
    │
    ├─ STORE operation → Apply (complete the write)
    │
    └─ DELETE operation → Revert (undo the delete)
    │
    ▼
Mark all as RECOVERED
    │
    ▼
Continue normal operation
```

## Data Consistency Guarantees

| Operation | JSON Store | Vector Store | WAL | Consistency |
|-----------|------------|--------------|-----|-------------|
| Store | Sync write | Async write | Sync | Eventual |
| Delete | Sync delete | Sync delete | Sync | Immediate |
| Update | Sync update | Async update | Sync | Eventual |
| Recovery | Replay WAL | Replay WAL | - | Restored |

## Next Steps

- [Overview](./overview.md) - System architecture
- [Design Principles](./design-principles.md) - Key decisions
- [Modules](./modules.md) - Module reference
