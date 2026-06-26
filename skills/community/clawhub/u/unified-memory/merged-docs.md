# Quick Start

> Get up and running with Unified Memory in 5 minutes

## Installation

```bash
npm install unified-memory
```

## Basic Usage

```javascript
import { getEnhancedMemorySystem } from 'unified-memory';

const memory = await getEnhancedMemorySystem();

// Add a memory
const memory = await memory.addMemory({
  text: 'Remember that meeting with the design team',
  category: 'work',
  importance: 0.8,
  tags: ['meeting', 'design']
});

// Search memories
const results = await memory.search('design team meeting');

// Get all memories
const allMemories = await memory.getAllMemories();
```

## Configuration

Create a `.env` file:

```bash
OLLAMA_URL=http://localhost:11434
MEMORY_FILE=./memory/memories.json
VECTOR_DB=lancedb
```

## Next Steps

- [API Reference](../api/README.md) - Full API documentation
- [Architecture](../architecture/README.md) - System design
# Configuration Guide

> Customize Unified Memory to fit your needs.

## 📁 Configuration File

The main configuration file is located at:
```
~/.unified-memory/config.json
```

## 🔧 Configuration Sections

### Storage Configuration

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    },
    "backup": {
      "enable": true,
      "interval": 86400,
      "maxBackups": 5
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"json"` | Storage mode: `"json"` or `"sqlite"` |
| `memoryFile` | `string` | `"~/.unified-memory/memories.json"` | Path to memory file |
| `vectorStore.backend` | `string` | `"lancedb"` | Vector backend: `"lancedb"` or `"chromadb"` |
| `vectorStore.path` | `string` | `"~/.unified-memory/vector.lance"` | Vector store path |
| `vectorStore.dimension` | `number` | `768` | Embedding vector dimension |

### Transaction Configuration

```json
{
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true,
    "timeout": 30000
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable` | `boolean` | `true` | Enable atomic transactions |
| `recoveryLog` | `string` | `"~/.unified-memory/transactions.log"` | WAL log path |
| `fsync` | `boolean` | `true` | fsync to disk on write |
| `timeout` | `number` | `30000` | Transaction timeout (ms) |

### Search Configuration

```json
{
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10,
    "minScore": 0.1
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `defaultMode` | `string` | `"hybrid"` | Default search mode |
| `bm25Weight` | `number` | `0.3` | BM25 weight in hybrid search (0-1) |
| `vectorWeight` | `number` | `0.7` | Vector weight in hybrid search (0-1) |
| `rrfK` | `number` | `60` | RRF constant for rank fusion |
| `topK` | `number` | `10` | Default number of results |
| `minScore` | `number` | `0.1` | Minimum relevance score |

### Cache Configuration

```json
{
  "cache": {
    "enable": true,
    "type": "semantic",
    "maxSize": 1000,
    "ttl": 3600,
    "evictionPolicy": "lru"
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable` | `boolean` | `true` | Enable caching |
| `type` | `string` | `"semantic"` | Cache type: `"semantic"` or `"exact"` |
| `maxSize` | `number` | `1000` | Maximum cache entries |
| `ttl` | `number` | `3600` | Cache TTL in seconds |
| `evictionPolicy` | `string` | `"lru"` | Eviction policy |

### Embedding Configuration

```json
{
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "url": "http://localhost:11434",
    "batchSize": 100,
    "dimension": 768
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `provider` | `string` | `"ollama"` | Embedding provider |
| `model` | `string` | `"nomic-embed-text"` | Embedding model |
| `url` | `string` | `"http://localhost:11434"` | Provider URL |
| `batchSize` | `number` | `100` | Batch size for embedding |
| `dimension` | `number` | `768` | Embedding dimension |

### Tier Configuration

```json
{
  "tier": {
    "hot": {
      "maxAge": 7,
      "compression": false
    },
    "warm": {
      "minAge": 7,
      "maxAge": 30,
      "compression": "light"
    },
    "cold": {
      "minAge": 30,
      "compression": "heavy"
    }
  }
}
```

| Tier | Age | Compression | Description |
|------|-----|-------------|-------------|
| HOT | ≤ 7 days | None | Active memories |
| WARM | 7-30 days | Light | Less active |
| COLD | > 30 days | Heavy | Archived |

### Plugin Configuration

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["sync-workspace"]
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dir` | `string` | `"~/.unified-memory/plugins"` | Plugin directory |
| `autoReload` | `boolean` | `true` | Hot reload plugins |
| `enabled` | `array` | `[]` | List of enabled plugins |

### Observability Configuration

```json
{
  "observability": {
    "metrics": {
      "enable": true,
      "port": 3852
    },
    "logging": {
      "level": "info",
      "file": "~/.unified-memory/logs/app.log"
    }
  }
}
```

## 🌐 Environment Variables

Override config values with environment variables:

```bash
# Storage
export UNIFIED_MEMORY_STORAGE_MODE=json
export UNIFIED_MEMORY_MEMORY_FILE=~/.unified-memory/memories.json

# Vector Store
export UNIFIED_MEMORY_VECTOR_BACKEND=lancedb
export UNIFIED_MEMORY_VECTOR_PATH=~/.unified-memory/vector.lance

# Ollama
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=nomic-embed-text

# Server
export UNIFIED_MEMORY_PORT=3851
export UNIFIED_MEMORY_HOST=0.0.0.0
```

## 📋 Complete Example

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true
  },
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10
  },
  "cache": {
    "enable": true,
    "maxSize": 1000,
    "ttl": 3600
  },
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "url": "http://localhost:11434"
  },
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true
  }
}
```

## 🔍 Validate Configuration

```bash
# Validate your config file
unified-memory config:validate

# Show current configuration
unified-memory config:show

# Generate default config
unified-memory config:init
```

## 🚨 Configuration Errors

| Error | Solution |
|-------|----------|
| Invalid JSON | Check syntax with `json_validate` |
| Unknown key | Remove or correct the key |
| Invalid value type | Ensure type matches expected type |
| Missing required | Add the required configuration |

## 📚 Next Steps

- [Quick Start Tutorial](./quickstart.md) - Try the configured system
- [Basic Usage Guide](../guides/basic-usage.md) - Learn core operations
- [Advanced Usage](../guides/advanced-usage.md) - Advanced features
# Atomic Transactions Architecture

[English](./atomic-transactions.md) · [中文](../../zh/architecture/atomic-transactions.md)

## 🎯 Overview

Unified Memory v5.2.0 introduces a robust atomic transaction system that guarantees data consistency between JSON storage and vector storage. This solves the critical problem of data inconsistency when writing to both storage backends.

## 🔄 The Problem: Dual-Write Inconsistency

Before v5.2.0, when adding a memory:

```javascript
// Problem: No atomicity guarantee
await jsonStorage.add(memory);      // Step 1: Write to JSON
await vectorStorage.add(memory);    // Step 2: Write to vector store

// If Step 2 fails, data is inconsistent!
// JSON has the memory, but vector store doesn't
```

This could lead to:
- **Search failures**: Memory exists but can't be found via vector search
- **Data corruption**: Partial writes create orphaned records
- **Recovery complexity**: Manual cleanup required after failures

## 🏗️ Solution: Two-Phase Commit Protocol

### Phase 1: Prepare
```javascript
// 1. Prepare JSON write (creates temporary file)
const jsonTempFile = await transactionManager.prepareJsonWrite(memory);

// 2. Prepare vector write (creates temporary record)
const vectorTempId = await transactionManager.prepareVectorWrite(memory);

// 3. Mark transaction as prepared
transactionManager.markPrepared(transactionId);
```

### Phase 2: Commit
```javascript
// 1. Atomically rename JSON temp file to final location
await transactionManager.commitJsonWrite(jsonTempFile);

// 2. Atomically move vector temp record to main index
await transactionManager.commitVectorWrite(vectorTempId);

// 3. Mark transaction as committed
transactionManager.markCommitted(transactionId);
```

### Rollback on Failure
```javascript
// If any step fails, rollback everything
await transactionManager.rollbackJsonWrite(jsonTempFile);
await transactionManager.rollbackVectorWrite(vectorTempId);
await transactionManager.markRolledBack(transactionId);
```

## 📁 File System Implementation

### Transaction Directory Structure
```
~/.unified-memory/
├── memories.json              # Main JSON storage
├── vector.lance              # Main vector storage
├── temp/                     # Temporary transaction files
│   ├── tx_1234567890_json.tmp
│   ├── tx_1234567890_vector.tmp
│   └── ...
├── logs/                     # Transaction logs
│   ├── transaction-2026-04-15.log
│   └── recovery.log
└── config.json               # Configuration
```

### Atomic File Operations
```javascript
// Atomic rename (fsync guaranteed)
const atomicRename = async (tempPath, finalPath) => {
  // 1. Write to temp file
  await fs.writeFile(tempPath, data);
  
  // 2. fsync to ensure data is on disk
  await fs.fsync(fs.openSync(tempPath, 'r+'));
  
  // 3. Atomic rename (POSIX guarantees atomicity)
  await fs.rename(tempPath, finalPath);
  
  // 4. fsync directory to ensure rename is persisted
  const dir = path.dirname(finalPath);
  await fs.fsync(fs.openSync(dir, 'r+'));
};
```

## 🔒 Data Persistence Guarantee

### fsync Strategy
```javascript
class PersistentStorage {
  async writeWithFsync(filePath, data) {
    const tempPath = `${filePath}.tmp${Date.now()}`;
    
    // Write to temp file
    await fs.writeFile(tempPath, data);
    
    // Force data to disk
    const fd = fs.openSync(tempPath, 'r+');
    await fs.fsync(fd);
    fs.closeSync(fd);
    
    // Atomic rename
    await fs.rename(tempPath, filePath);
    
    // Force directory metadata to disk
    const dirFd = fs.openSync(path.dirname(filePath), 'r');
    await fs.fsync(dirFd);
    fs.closeSync(dirFd);
  }
}
```

### Recovery Mechanism
```javascript
class TransactionRecovery {
  async recoverIncompleteTransactions() {
    // 1. Scan temp directory for unfinished transactions
    const tempFiles = await fs.readdir(tempDir);
    
    // 2. Check transaction log for status
    const transactions = await this.loadTransactionLog();
    
    // 3. Recover prepared but not committed transactions
    for (const tx of transactions) {
      if (tx.status === 'prepared') {
        // Transaction was prepared but not committed
        // Need to decide: commit or rollback
        
        if (this.shouldCommit(tx)) {
          await this.commitTransaction(tx);
        } else {
          await this.rollbackTransaction(tx);
        }
      }
    }
  }
}
```

## ⚡ Performance Optimizations

### Batch Transactions
```javascript
// Group multiple writes into a single transaction
const batchTransaction = async (memories) => {
  const tx = await beginTransaction();
  
  try {
    for (const memory of memories) {
      await addMemory(memory, { transaction: tx });
    }
    
    await commitTransaction(tx);
    return { success: true, count: memories.length };
    
  } catch (error) {
    await rollbackTransaction(tx);
    throw error;
  }
};
```

### Write-Behind Caching
```javascript
class WriteBehindCache {
  constructor() {
    this.cache = new Map();
    this.writeQueue = [];
    this.writeInterval = 500; // ms
  }
  
  async queueWrite(memory) {
    // Add to cache immediately
    this.cache.set(memory.id, memory);
    
    // Queue for background write
    this.writeQueue.push(memory);
    
    // Start write timer if not already running
    if (!this.writeTimer) {
      this.writeTimer = setTimeout(() => this.flush(), this.writeInterval);
    }
  }
  
  async flush() {
    const batch = this.writeQueue.splice(0, 100);
    if (batch.length > 0) {
      await batchTransaction(batch);
    }
    this.writeTimer = null;
  }
}
```

## 🧪 Testing Atomicity

### Test Suite
```javascript
describe('Atomic Transactions', () => {
  it('should maintain consistency on successful write', async () => {
    const memory = createTestMemory();
    const tx = await beginTransaction();
    
    await addMemory(memory, { transaction: tx });
    await commitTransaction(tx);
    
    // Verify both storages have the memory
    const jsonHas = await jsonStorage.has(memory.id);
    const vectorHas = await vectorStorage.has(memory.id);
    
    expect(jsonHas).toBe(true);
    expect(vectorHas).toBe(true);
  });
  
  it('should rollback on vector store failure', async () => {
    const memory = createTestMemory();
    const tx = await beginTransaction();
    
    // Simulate vector store failure
    jest.spyOn(vectorStorage, 'add').mockRejectedValue(new Error('Vector store down'));
    
    await expect(addMemory(memory, { transaction: tx })).rejects.toThrow();
    
    // Verify neither storage has the memory
    const jsonHas = await jsonStorage.has(memory.id);
    const vectorHas = await vectorStorage.has(memory.id);
    
    expect(jsonHas).toBe(false);
    expect(vectorHas).toBe(false);
  });
});
```

## 📊 Performance Metrics

### Before v5.2.0
| Metric | Value |
|--------|-------|
| Write throughput | 100 ops/sec |
| Data consistency | 95% |
| Crash recovery | Manual required |
| Transaction support | None |

### After v5.2.0
| Metric | Value |
|--------|-------|
| Write throughput | 90 ops/sec (10% overhead) |
| Data consistency | 100% |
| Crash recovery | Automatic |
| Transaction support | Full |

## 🔧 Configuration Options

```json
{
  "transaction": {
    "enable": true,
    "mode": "two-phase",  // "two-phase" or "optimistic"
    "timeout": 30000,     // Transaction timeout in ms
    "recovery": {
      "enable": true,
      "scanInterval": 60000  // Scan for incomplete transactions every minute
    },
    "fsync": {
      "enable": true,
      "strategy": "always"  // "always", "periodic", "critical-only"
    }
  }
}
```

## 🚀 Best Practices

### 1. Use Appropriate Transaction Size
```javascript
// Good: Batch related writes
await batchTransaction(relatedMemories);

// Bad: Too many small transactions
for (const memory of memories) {
  await addMemory(memory); // Creates separate transaction each time
}
```

### 2. Handle Timeouts Gracefully
```javascript
try {
  const tx = await beginTransaction({ timeout: 10000 });
  // ... transaction operations
} catch (error) {
  if (error.name === 'TransactionTimeoutError') {
    // Implement retry logic or notify user
    await retryWithBackoff();
  }
}
```

### 3. Monitor Transaction Health
```javascript
// Regular health checks
const health = await transactionManager.getHealth();
if (health.pendingTransactions > 100) {
  // Alert: Too many pending transactions
  sendAlert('Transaction queue is growing');
}
```

## 🔍 Debugging Transactions

### Transaction Log Format
```json
{
  "transactionId": "tx_1776232481727_0i12vd",
  "status": "committed",
  "startTime": "2026-04-15T19:34:41.727Z",
  "endTime": "2026-04-15T19:34:41.732Z",
  "durationMs": 5,
  "operations": [
    {
      "type": "json_write",
      "memoryId": "mem_1776232481727_0i12vd",
      "status": "success"
    },
    {
      "type": "vector_write",
      "memoryId": "mem_1776232481727_0i12vd",
      "status": "success"
    }
  ],
  "error": null
}
```

### Recovery Log
```json
{
  "recoveryId": "rec_1776232500000_abc123",
  "timestamp": "2026-04-15T19:35:00.000Z",
  "scannedTransactions": 15,
  "recoveredTransactions": 2,
  "rolledBackTransactions": 1,
  "errors": []
}
```

## 📈 Future Improvements

### Planned Enhancements
1. **Distributed Transactions**: Support for multi-node deployments
2. **Optimistic Concurrency Control**: Reduce locking overhead
3. **Compensation Transactions**: For complex multi-step operations
4. **Transaction Chaining**: Dependent transaction sequences

### Research Areas
- **Zero-copy transactions**: Reduce memory overhead
- **Hardware acceleration**: Use CPU/GPU for transaction processing
- **Blockchain integration**: Immutable transaction ledger

---

**Related Documents:**
- [Architecture Overview](./overview.md)
- [Vector Search Architecture](./vector-search.md)
- [Performance Tuning Guide](../reference/configuration.md)

[← Back to Architecture Overview](./overview.md) · [Next: Vector Search Architecture →](./vector-search.md)# Architecture Overview

> Understand how Unified Memory is designed and how its components work together.

## 📚 Table of Contents

1. [System Overview](#-system-overview)
2. [Architecture Layers](#-architecture-layers)
3. [Core Components](#-core-components)
4. [Data Flow](#-data-flow)
5. [Storage Architecture](#-storage-architecture)
6. [Search Architecture](#-search-architecture)

## 🏗️ System Overview

Unified Memory is a layered system designed for:
- **Reliability**: Atomic transactions and WAL ensure data safety
- **Performance**: Hybrid search and caching optimize query speed
- **Extensibility**: Plugin system allows custom functionality
- **Scalability**: Modular architecture supports growth

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│        (OpenClaw, Web UI, CLI, REST API, MCP Clients)      │
└───────────────────────────┬─────────────────────────────────┘
                            │ MCP Tools / REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │ MCP Server │  │ REST API   │  │ WebSocket  │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Service Layer                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Memory    │  │   Search   │  │   Cache    │           │
│  │  Service   │  │  Service   │  │  Service   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Plugin   │  │   Profile  │  │   Tier     │           │
│  │  Service   │  │  Service   │  │  Service   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Storage Layer                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   JSON     │  │   Vector   │  │    WAL     │           │
│  │   Store    │  │   Store    │  │   Logger   │           │
│  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## �.layered Architecture

### Layer 1: API Gateway

Handles external communication:

| Component | Protocol | Purpose |
|-----------|----------|---------|
| MCP Server | MCP | AI assistant integration |
| REST API | HTTP | Web and mobile clients |
| WebSocket | WS | Real-time updates |

### Layer 2: Service Layer

Business logic and orchestration:

| Service | Responsibility |
|---------|---------------|
| Memory Service | CRUD operations for memories |
| Search Service | Hybrid search orchestration |
| Cache Service | Query result caching |
| Plugin Service | Plugin lifecycle management |
| Profile Service | User profile aggregation |
| Tier Service | Memory tier management |

### Layer 3: Storage Layer

Data persistence:

| Store | Technology | Purpose |
|-------|------------|---------|
| JSON Store | SQLite + JSON files | Primary memory storage |
| Vector Store | LanceDB/ChromaDB | Embeddings and similarity search |
| WAL Logger | Append-only log | Transaction safety |

## 🔧 Core Components

### 1. Memory Manager (`src/manager.js`)

Central coordinator for memory operations:

```javascript
// Responsibilities
- Initialize system components
- Coordinate memory lifecycle
- Handle tick/background operations
- Manage shutdown sequence
```

### 2. Storage (`src/storage.js`)

JSON file storage with SQLite:

```javascript
// Responsibilities
- Read/write memory JSON files
- Manage memory metadata
- Handle file I/O with fsync
- Ensure atomic writes
```

### 3. Vector Store (`src/vector.js` / `src/vector_lancedb.js`)

Embedding storage and search:

```javascript
// Responsibilities
- Generate embeddings via Ollama
- Store vectors in LanceDB
- Execute similarity searches
- Manage vector cache
```

### 4. BM25 Index (`src/bm25.js`)

Keyword search index:

```javascript
// Responsibilities
- Build inverted index
- Calculate BM25 scores
- Execute keyword queries
- Support incremental updates
```

### 5. Search Fusion (`src/fusion.js`)

Hybrid search orchestration:

```javascript
// Responsibilities
- Execute parallel BM25 and vector searches
- Combine results using RRF
- Apply filters and thresholds
- Format responses
```

### 6. MCP Server (`src/index.js`)

MCP protocol implementation:

```javascript
// Responsibilities
- Register MCP tools
- Handle tool requests
- Route to appropriate services
- Format responses
```

## 🔄 Data Flow

### Store Memory Flow

```
Client
  │
  ▼
MCP Server (memory_store tool)
  │
  ▼
Plugin Service (beforeStore hooks)
  │
  ▼
Memory Service
  │
  ├─────────────────────┬─────────────────────┐
  ▼                     ▼                     ▼
Storage (JSON)    Vector Store     WAL Logger
  │                     │                     │
  └─────────────────────┴─────────────────────┘
                        │
                        ▼
              Plugin Service (afterStore hooks)
                        │
                        ▼
                    Client Response
```

### Search Flow

```
Client
  │
  ▼
MCP Server (memory_search tool)
  │
  ▼
Plugin Service (beforeSearch hooks)
  │
  ▼
Cache Service (check cache)
  │
  ├─ Cache Hit ──► Return cached results
  │
  └─ Cache Miss ──►
                    │
                    ▼
            Search Fusion
              │       │
              ▼       ▼
         BM25     Vector
              │       │
              └───────┘
                    │
                    ▼
             RRF Fusion
                    │
                    ▼
            Plugin Service (afterSearch hooks)
                    │
                    ▼
              Cache Service (store results)
                    │
                    ▼
                Client Response
```

## 💾 Storage Architecture

### JSON Storage

```
~/.unified-memory/
└── memories.json
```

Structure:
```json
{
  "version": "5.2.0",
  "memories": [
    {
      "id": "mem_xxx",
      "text": "Memory content",
      "category": "fact",
      "importance": 0.8,
      "tags": ["tag1", "tag2"],
      "scope": "USER",
      "source": "manual",
      "metadata": {},
      "created_at": "2026-04-15T10:00:00Z",
      "updated_at": "2026-04-15T10:00:00Z",
      "tier": "HOT",
      "pinned": false,
      "access_count": 5,
      "last_accessed": "2026-04-20T08:00:00Z"
    }
  ],
  "indexes": {
    "byCategory": {},
    "byTag": {},
    "byScope": {}
  }
}
```

### Vector Storage (LanceDB)

```
~/.unified-memory/
└── vector.lance/
```

Schema:
```
Table: memories
├── id: string (primary key)
├── embedding: vector<float>(768)
├── text: string
├── created_at: timestamp
└── metadata: json
```

### WAL (Write-Ahead Log)

```
~/.unified-memory/
└── wal/
    ├── 000001.log
    ├── 000002.log
    └── ...
```

Entry format:
```json
{
  "txId": 123,
  "operation": "STORE",
  "timestamp": "2026-04-15T10:00:00Z",
  "data": { /* memory object */ },
  "status": "COMMITTED"
}
```

## 🔍 Search Architecture

### Hybrid Search Pipeline

```
Query: "quarterly reports meeting"
         │
         ├──────────────────────────────┐
         ▼                              ▼
    BM25 Search                   Vector Search
    "quarterly reports"           embedding(query)
         │                              │
         ▼                              ▼
    [doc1, doc3, doc5]           [doc2, doc3, doc1]
         │                              │
         └──────────────┬───────────────┘
                        ▼
                  RRF Fusion
                  k = 60
                        │
                        ▼
              Final Ranking
              [doc3, doc1, doc5, doc2]
```

### RRF Formula

Reciprocal Rank Fusion combines multiple rankings:

```
RRF_score(doc) = Σ(1 / (k + rank_i(doc)))
```

Where:
- `k` = 60 (constant)
- `rank_i` = rank from algorithm `i`

Example:
```
doc3: BM25 rank=2, Vector rank=2
RRF = 1/(60+2) + 1/(60+2) = 0.01613 + 0.01613 = 0.03226

doc1: BM25 rank=1, Vector rank=3
RRF = 1/(60+1) + 1/(60+3) = 0.01639 + 0.01587 = 0.03226
```

## 🔌 Plugin Architecture

```
┌─────────────────────────────────────────┐
│           Plugin Manager                │
│  - Load/unload plugins                 │
│  - Manage lifecycle                    │
│  - Route hooks                         │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Plugin1 │ │ Plugin2 │ │ Plugin3 │
   └─────────┘ └─────────┘ └─────────┘
```

### Hook Execution Order

1. `beforeStore` - All plugins, in order
2. Core storage operation
3. `afterStore` - All plugins, in reverse order

## 📊 Performance Optimizations

| Optimization | Description | Impact |
|--------------|-------------|--------|
| Semantic Cache | Cache similar queries | 78% hit rate |
| Vector Cache | Cache embeddings | Faster searches |
| Tier-based compression | Compress old memories | 60% storage reduction |
| Incremental BM25 | Update index incrementally | Faster indexing |
| Connection pooling | Reuse database connections | Lower latency |

## 🔒 Reliability Features

| Feature | Mechanism | Guarantee |
|---------|-----------|-----------|
| Atomic Writes | Two-phase commit | JSON + Vector consistency |
| Crash Recovery | WAL + fsync | Zero data loss |
| Transaction Rollback | Undo log | Failed tx reverted |
| Health Monitoring | Periodic checks | Early failure detection |

## 📚 Next Steps

- [Design Principles](./design-principles.md) - Key architectural decisions
- [Modules](./modules.md) - Detailed module reference
- [Data Flow](./data-flow.md) - Detailed data flow diagrams
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
# Modules Reference

> Detailed documentation for each module in Unified Memory.

## 📁 Module Directory

```
src/
├── agents/           Agent orchestration
├── api/              HTTP/MCP server interfaces
├── backup/           Backup & restore
├── benchmark/        Performance benchmarking
├── cache/            Query result caching
├── chunking/         Text chunking
├── cli/              Command-line tools
├── compress/         Memory compression
├── config/           Configuration
├── connectors/       External connectors
├── consolidate/      Memory consolidation
├── conversation/     Conversation processing
├── core/             Core memory operations
├── decay/            Time-based decay
├── deduplication/    Dedup logic
├── episode/          Episode capture
├── extraction/       Memory extraction
├── extractors/       Content extractors
├── forgetting/       TTL management
├── graph/            Knowledge graph
├── hooks/            Lifecycle hooks
├── integrations/     Third-party integrations
├── lifecycle/        Lifecycle management
├── memory_types/     Type definitions
├── multimodal/       Multimodal support
├── observability/    Metrics & monitoring
├── parsing/          Input parsing
├── persona/          Persona management
├── plugin/           Plugin system
├── profile/          User profile
├── prompts/          Prompt templates
├── quality/          Quality scoring
├── queue/            Async queue
├── recall/           Recall strategies
├── record/           L1 record processing
├── relations/        Memory relations
├── rerank/           Result reranking
├── retrieval/        Retrieval strategies
├── rule/             Rule processing
├── scene/            Scene understanding
├── search/           Search engine
├── session/          Session management
├── setup/            Initialization
├── storage/          Storage backends
├── store/            Store operations
├── system/           System operations
├── tools/            MCP tools
├── utils/            Utilities
├── v4/               v4.0 storage gateway
└── visualize/        Visualization
```

## 🔧 Core Modules

### Storage (`src/storage.js`)

Primary JSON file storage.

**Public API:**
```javascript
addMemory(memory)           // Add new memory
getMemory(id)               // Get by ID
getAllMemories(options)     // List with filters
updateMemory(id, updates)  // Update fields
deleteMemory(id)            // Delete memory
saveMemories(memories)      // Bulk save
```

**Internal Functions:**
```javascript
_readFile()                 // Read from disk
_writeFile(data)            // Write to disk with fsync
_validateMemory(memory)     // Validate structure
_indexMemory(memory)        // Update indexes
```

### Vector Store (`src/vector.js`, `src/vector_lancedb.js`)

Embedding and similarity search.

**Public API:**
```javascript
getEmbedding(text)          // Generate embedding
searchVectors(query, options) // ANN search
addVector(id, text, metadata) // Add embedding
deleteVector(id)            // Remove embedding
```

**LanceDB Backend:**
```javascript
// Uses LanceDB for vector storage
const table = await lancedb.open("~/memory.lance");
await table.add([{ id, vector, text }]);
await table.search(queryVector).limit(k);
```

**ChromaDB Backend (Alternative):**
```javascript
// ChromaDB for vector storage
const client = new ChromaClient();
const collection = client.getCollection("memories");
await collection.add({ ids, embeddings, documents });
```

### BM25 (`src/bm25.js`)

Keyword search index.

**Public API:**
```javascript
buildBM25Index(memories)    // Build from memories
bm25Search(query, options)  // Search index
updateBM25Index(memory)     // Incremental update
removeFromIndex(id)         // Remove from index
```

**Internal:**
```javascript
_tokenize(text)             // Tokenize text
_calculate IDF(documents)   // Compute IDF scores
_scoreDocument(query, doc)  // BM25 scoring
```

### Search Fusion (`src/fusion.js`)

Hybrid search orchestration.

**Public API:**
```javascript
hybridSearch(query, options) // BM25 + Vector + RRF
```

**Internal:**
```javascript
_executeBM25(query)         // Run BM25
_executeVector(query)       // Run vector search
_applyRRF(bm25Results, vectorResults, k) // RRF fusion
_applyFilters(results, filters) // Apply metadata filters
_formatResponse(results)     // Format output
```

## 🛠️ Tool Modules

### Search Tool (`src/tools/memory_search.js`)

MCP adapter for search.

```javascript
executeMemorySearch(params) // Tool executor
cmdMemorySearch(params)     // CLI command
```

### Store Tool (`src/tools/memory_store.js`)

MCP adapter for storing.

```javascript
executeMemoryStore(params)   // Tool executor
cmdMemoryStore(params)       // CLI command
```

### List Tool (`src/tools/memory_list.js`)

MCP adapter for listing.

```javascript
executeMemoryList(params)   // Tool executor
cmdMemoryList(params)       // CLI command
```

### Delete Tool (`src/tools/memory_delete.js`)

MCP adapter for deletion.

```javascript
executeMemoryDelete(params) // Tool executor
cmdMemoryDelete(params)     // CLI command
```

## 🔌 Service Modules

### Memory Service (`src/service/memory.js`)

Business logic for memory operations.

```javascript
class MemoryService {
  async store(memory)       // Store with hooks
  async search(query, opts) // Search with filters
  async get(id)             // Get single memory
  async list(options)       // List with pagination
  async delete(id)          // Delete with cleanup
}
```

### Cache Service (`src/cache/`)

Query result caching.

```javascript
class SemanticCache {
  async get(key)            // Get cached result
  async set(key, value)     // Store in cache
  async invalidate(pattern) // Clear matching
  _computeSimilarity(a, b)  // Semantic similarity
}
```

### Plugin Service (`src/plugin/`)

Plugin lifecycle management.

```javascript
class PluginManager {
  async loadPlugin(path)    // Load plugin
  async unloadPlugin(name)  // Unload plugin
  async executeHook(name, ...args) // Run hooks
}
```

## 📊 Supporting Modules

### Configuration (`src/config/`)

```javascript
loadConfig()                // Load config file
getConfig(key)              // Get config value
mergeConfig(overrides)      // Merge overrides
validateConfig(config)     // Validate structure
```

### Observability (`src/observability/`)

```javascript
emitMetric(name, value)     // Record metric
emitEvent(name, data)       // Emit event
getMetrics()                // Get all metrics
getHealth()                 // Health check
```

### WAL (`src/wal/`)

```javascript
class WAL {
  async init()              // Initialize
  async log(operation)      // Write log entry
  async commit(txId)         // Mark committed
  async recover()           // Recover from crash
}
```

## 🔀 Module Dependencies

```
                    ┌─────────────┐
                    │  index.js   │
                    │ (MCP Entry) │
                    └──────┬──────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  tools/*.js │ │  tools/*.js│ │  tools/*.js │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │  fusion.js  │
                   │  (search)   │
                   └──────┬──────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  bm25.js │   │ vector.js│   │  cache/  │
    └──────────┘   └──────────┘   └──────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  storage.js│
                   │ (JSON file)│
                   └─────────────┘
```

## 📝 Module Writing Guidelines

### Creating a New Tool

```javascript
// src/tools/my_tool.js

export const myTool = {
  name: 'memory_my_tool',
  description: 'Description of what it does',
  
  parameters: {
    // JSON Schema for parameters
  },
  
  async execute(params, context) {
    // 1. Validate parameters
    // 2. Call service layer
    // 3. Format response
    // 4. Return { content: [...] }
  }
};
```

### Adding a New Hook

```javascript
// In plugin system

const HOOKS = {
  beforeStore: [],
  afterStore: [],
  // Add new hook
  beforeExport: [],
  afterExport: []
};

async function executeHooks(hookName, ...args) {
  for (const plugin of plugins) {
    if (plugin.hooks[hookName]) {
      await plugin.hooks[hookName](...args);
    }
  }
}
```

## 📚 Next Steps

- [Data Flow](./data-flow.md) - How data moves through modules
- [Design Principles](./design-principles.md) - Architectural decisions
- [Overview](./overview.md) - System architecture
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
# Unified Memory Documentation

**English** · [中文](../zh/index.md)

Welcome to the Unified Memory v5.2.0 documentation. This documentation provides comprehensive guides, API references, and architecture details for the Unified Memory system.

## 📚 Documentation Structure

### Getting Started
- **[Quick Start Guide](./getting-started/quickstart.md)** - Get up and running in 5 minutes
- **[Installation Guide](./getting-started/installation.md)** - Detailed installation instructions
- **[Configuration Guide](./getting-started/configuration.md)** - System configuration options

### User Guides
- **[Basic Usage](./guides/basic-usage.md)** - Everyday operations and common tasks
- **[Advanced Features](./guides/advanced-features.md)** - Power features and optimizations
- **[Plugin System](./guides/plugins.md)** - Extending functionality with plugins
- **[Troubleshooting](./guides/troubleshooting.md)** - Solving common problems

### API Documentation
- **[API Overview](./api/overview.md)** - Introduction to the Unified Memory API
- **[Storage API](./api/storage-api.md)** - Memory storage and retrieval operations
- **[Vector API](./api/vector-api.md)** - Vector search and similarity operations
- **[Plugin API](./api/plugin-api.md)** - Plugin development and integration

### Architecture
- **[Architecture Overview](./architecture/overview.md)** - System design and components
- **[Atomic Transactions](./architecture/atomic-transactions.md)** - Data consistency guarantees
- **[Vector Search](./architecture/vector-search.md)** - Search algorithms and optimizations
- **[Plugin System](./architecture/plugin-system.md)** - Plugin architecture and design

### Reference
- **[CLI Reference](./reference/cli-reference.md)** - Command-line interface documentation
- **[Configuration Reference](./reference/configuration.md)** - Complete configuration options
- **[Changelog](./reference/changelog.md)** - Version history and changes
- **[FAQ](./reference/faq.md)** - Frequently asked questions
- **[Contributing Guide](./reference/contributing.md)** - How to contribute to the project

## 🎯 Key Features Documentation

### Atomic Data Consistency
- **Two-Phase Commit Protocol**: Guarantees atomic writes for JSON and vector storage
- **Transaction Recovery**: Automatic recovery of incomplete transactions
- **fsync Guarantee**: Ensures data is written to disk

### High-Performance Search
- **Hybrid Search**: BM25 + Vector + RRF fusion for best results
- **Optimized Algorithms**: 5-10x faster query performance
- **Intelligent Caching**: Memory caching for frequent queries

### Plugin System
- **Sync Bridge**: Synchronize with Workspace Memory
- **Unified Query**: Cross-system search interface
- **Health Monitoring**: Real-time system monitoring

## 🔧 Development Resources

### Code Examples


### Testing


### Building


## 📖 Reading Order

### For New Users
1. Start with the **[Quick Start Guide](./getting-started/quickstart.md)**
2. Read **[Basic Usage](./guides/basic-usage.md)** for everyday tasks
3. Explore **[Advanced Features](./guides/advanced-features.md)** as needed

### For Developers
1. Review the **[Architecture Overview](./architecture/overview.md)**
2. Study **[Atomic Transactions](./architecture/atomic-transactions.md)** for data consistency
3. Check the **[API Documentation](./api/overview.md)** for integration

### For Contributors
1. Read the **[Contributing Guide](./reference/contributing.md)**
2. Understand the **[Architecture](./architecture/overview.md)**
3. Review existing **[Code Examples](../shared/examples/)**

## 🔗 Related Resources

### External Links
- **[GitHub Repository](https://github.com/mouxangithub/unified-memory)** - Source code and issues
- **[npm Package](https://www.npmjs.com/package/unified-memory)** - Package distribution
- **[ClawHub Skill](https://clawhub.ai/)** - Skill marketplace

### Community
- **[GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)** - Community discussions
- **[Issue Tracker](https://github.com/mouxangithub/unified-memory/issues)** - Bug reports and feature requests
- **[Contributing Guide](./reference/contributing.md)** - How to contribute

## 📄 License

This documentation is part of the Unified Memory project and is licensed under the MIT License. See the [LICENSE](https://github.com/mouxangithub/unified-memory/blob/main/LICENSE) file for details.

## 🤝 Contributing to Documentation

We welcome contributions to improve this documentation! Please see our [Contributing Guide](./reference/contributing.md) for details on how to:

1. Report documentation issues
2. Suggest improvements
3. Submit documentation updates
4. Translate documentation

## 📞 Support

- **Documentation Issues**: Open an issue on [GitHub](https://github.com/mouxangithub/unified-memory/issues)
- **Questions**: Use [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)
- **Bugs**: Report via the [Issue Tracker](https://github.com/mouxangithub/unified-memory/issues)

---

**Last Updated**: 2026-04-15  
**Version**: v5.2.0  
**Documentation Version**: 1.0.0  

[← Back to Main Documentation](../README.md)
# Unified Memory Documentation

> 🧠 Enterprise-grade memory management system with hybrid search, atomic transactions, and plugin architecture

[![Version](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Links

| I want to... | Go to |
|-------------|-------|
| Get started quickly | [Quick Start](./getting-started/quickstart.md) |
| Install the system | [Installation Guide](./getting-started/installation.md) |
| Configure settings | [Configuration Guide](./getting-started/configuration.md) |
| Learn basic usage | [Basic Usage Guide](./guides/basic-usage.md) |
| Explore advanced features | [Advanced Usage](./guides/advanced-usage.md) |
| Build a plugin | [Plugin Development](./guides/plugins.md) |
| Integrate with my app | [Integration Guide](./guides/integration.md) |
| Understand the architecture | [Architecture Overview](./architecture/overview.md) |
| Find API reference | [API Reference](./api/overview.md) |
| Troubleshoot issues | [Troubleshooting](./reference/troubleshooting.md) |

## ✨ Key Features

### 🔍 Hybrid Search
Unified Memory combines multiple search algorithms for optimal relevance:
- **BM25**: Traditional keyword-based search
- **Vector Search**: Semantic similarity using embeddings
- **RRF (Reciprocal Rank Fusion)**: Combines results from multiple rankers

### ⚡ Atomic Transactions
Enterprise-grade data consistency:
- **WAL (Write-Ahead Logging)**: Crash recovery guarantee
- **Two-Phase Commit**: Atomic writes across JSON and vector storage
- **fsync Guarantee**: Data is written to disk, preventing loss

### 🔌 Plugin System
Extensible architecture with hot-reload support:
- **Lifecycle Hooks**: Before/after operation hooks
- **Sync Bridges**: Connect to external memory systems
- **Custom Processors**: Add custom memory processing

### 📊 Performance
Optimized for production workloads:
- **5-10x faster** search with optimized vector engine
- **60% storage reduction** through intelligent compression
- **78% cache hit rate** with semantic caching
- **45ms average query time**

## 📦 Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# Store a memory
unified-memory add "Remember to review quarterly reports" --tags work,reminder

# Search memories
unified-memory search "quarterly reports"

# Use via JavaScript API
node -e "
const { addMemory, searchMemories } = require('unified-memory');
(async () => {
  await addMemory({ text: 'My preference for morning meetings', tags: ['preference'] });
  const results = await searchMemories('meeting schedule');
  console.log(results);
})();
"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                       │
│        (OpenClaw, Web UI, CLI, API, MCP Clients)            │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    API Gateway Layer                        │
│           (REST API, MCP Server, WebSocket)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Service Layer                            │
│     (Memory Service, Search Service, Cache Service)           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Storage Layer                            │
│        (SQLite, Vector Database, File System)                │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Documentation Sections

### Getting Started
- [Quick Start](./getting-started/quickstart.md) - 5-minute introduction
- [Installation](./getting-started/installation.md) - Full installation guide
- [Configuration](./getting-started/configuration.md) - Configuration options

### User Guides
- [Basic Usage](./guides/basic-usage.md) - Core operations
- [Advanced Usage](./guides/advanced-usage.md) - Advanced features
- [Plugin Development](./guides/plugins.md) - Build plugins
- [Integration](./guides/integration.md) - Connect to other systems

### Architecture
- [Overview](./architecture/overview.md) - System design
- [Design Principles](./architecture/design-principles.md) - Key principles
- [Modules](./architecture/modules.md) - Module reference
- [Data Flow](./architecture/data-flow.md) - How data moves through the system

### API Reference
- [Overview](./api/overview.md) - API introduction
- [Core API](./api/core-api.md) - Core functions
- [MCP Tools](./api/mcp-tools.md) - MCP tool reference
- [Plugin API](./api/plugin-api.md) - Plugin development

### Reference
- [Configuration Reference](./reference/configuration.md) - All config options
- [Troubleshooting](./reference/troubleshooting.md) - Common issues
- [FAQ](./reference/faq.md) - Frequently asked questions

## 🔧 Development

```bash
# Clone and setup
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory
npm install

# Run tests
npm test

# Build for production
npm run build
```

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](./contributing/guidelines.md) before submitting PRs.

## 📄 License

MIT License - see [LICENSE](../../LICENSE) file for details.

## 📞 Support

- [GitHub Issues](https://github.com/mouxangithub/unified-memory/issues)
- [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)

---

**Version**: 5.2.0 | **Last Updated**: 2026-04-20
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
# Plugin API Reference

> API for building Unified Memory plugins.

## Plugin Structure

```javascript
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  // Lifecycle hooks
  hooks: {
    beforeStore: async (memory) => memory,
    afterStore: async (memory, result) => {},
    beforeSearch: async (query, options) => ({ query, options }),
    afterSearch: async (results, query) => results,
    beforeDelete: async (id) => id,
    afterDelete: async (id) => {},
    onInit: async (context) => {},
    onShutdown: async () => {}
  },

  // Custom tools exposed by this plugin
  tools: []
};
```

## Hooks API

### beforeStore(memory)

Called before a memory is stored. Use to transform or validate.

```javascript
beforeStore: async (memory) => {
  // Transform memory
  memory.text = memory.text.trim();
  
  // Add metadata
  memory.metadata = memory.metadata || {};
  memory.metadata.processedBy = 'my-plugin';
  
  // Validate (throw to reject)
  if (!memory.text) {
    throw new Error('Memory text cannot be empty');
  }
  
  return memory;
}
```

**Parameters:** `memory: Memory`  
**Returns:** `Memory` (modified)

---

### afterStore(memory, result)

Called after a memory is stored. Use for side effects.

```javascript
afterStore: async (memory, result) => {
  // Sync to external system
  await externalApi.syncMemory(memory);
  
  // Emit event
  emit('memory:stored', memory);
  
  // Update derived data
  await updateStats();
}
```

**Parameters:**
- `memory: Memory` - The stored memory
- `result: { success: boolean, id: string }`

**Returns:** `void`

---

### beforeSearch(query, options)

Called before search is executed. Use to modify query.

```javascript
beforeSearch: async (query, options) => {
  // Expand query
  const expanded = await expandQuery(query);
  
  // Add default filters
  options.scope = options.scope || 'USER';
  
  return { query: expanded, options };
}
```

**Parameters:**
- `query: string`
- `options: SearchOptions`

**Returns:** `{ query: string, options: SearchOptions }`

---

### afterSearch(results, query)

Called after search results are ready. Use to filter/rerank.

```javascript
afterSearch: async (results, query) => {
  // Filter by date
  const cutoff = Date.now() - (30 * 24 * 60 * 60 * 1000);
  return results.filter(r => 
    new Date(r.created_at).getTime() > cutoff
  );
  
  // Or rerank with custom logic
  return rerankResults(results, query);
}
```

**Parameters:**
- `results: SearchResult[]`
- `query: string`

**Returns:** `SearchResult[]`

---

### beforeDelete(id)

Called before a memory is deleted.

```javascript
beforeDelete: async (id) => {
  // Log deletion
  console.log('Memory deleted:', id);
  
  return id; // Must return the ID
}
```

**Parameters:** `id: string`  
**Returns:** `string` (ID)

---

### afterDelete(id)

Called after a memory is deleted.

```javascript
afterDelete: async (id) => {
  // Cleanup external references
  await externalApi.deleteMemory(id);
  
  // Emit event
  emit('memory:deleted', { id });
}
```

**Parameters:** `id: string`  
**Returns:** `void`

---

### onInit(context)

Called when plugin is loaded. Use for initialization.

```javascript
onInit: async (context) => {
  // Load configuration
  this.config = context.config;
  
  // Initialize resources
  this.client = new ExternalClient(this.config);
  
  // Connect
  await this.client.connect();
  
  // Register event handlers
  context.on('event', this.handleEvent);
}
```

**Parameters:** `context: PluginContext`  
**Returns:** `void`

---

### onShutdown()

Called when plugin is unloaded. Use for cleanup.

```javascript
onShutdown: async () => {
  // Close connections
  await this.client.disconnect();
  
  // Save state
  await this.saveState();
  
  // Clear timers
  this.timer && clearInterval(this.timer);
}
```

**Returns:** `void`

---

## Plugin Context API

The context object passed to `onInit`:

```javascript
interface PluginContext {
  config: PluginConfig;      // Plugin-specific config
  storage: StorageInterface; // Storage access
  search: SearchInterface;   // Search access
  emit: (event: string, data: any) => void;  // Event emitter
  on: (event: string, handler: Function) => void;  // Event subscription
  getConfig: (key: string) => any;  // Get config value
}
```

### Storage Interface

```javascript
// Get a memory
const memory = await context.storage.getMemory(id);

// Get all memories
const memories = await context.storage.getAllMemories(options);

// Add memory
await context.storage.addMemory(memory);

// Update memory
await context.storage.updateMemory(id, updates);

// Delete memory
await context.storage.deleteMemory(id);
```

### Search Interface

```javascript
// Hybrid search
const results = await context.search.hybridSearch(query, options);

// BM25 only
const results = await context.search.bm25Search(query);

// Vector only
const results = await context.search.vectorSearch(query);

// Custom search
const results = await context.search.search({
  query,
  mode: 'hybrid',
  topK: 10
});
```

### Event Emitter

```javascript
// Emit events
context.emit('memory:stored', memory);
context.emit('memory:deleted', { id });
context.emit('search:executed', { query, count });
context.emit('error', { hook: 'beforeStore', error });

// Subscribe to events
context.on('memory:stored', (memory) => {
  console.log('Memory stored:', memory.id);
});
```

## Tool Interface

Define custom MCP tools in your plugin:

```javascript
export const plugin = {
  name: 'my-plugin',
  
  tools: [
    {
      name: 'my_plugin_tool',
      description: 'Custom tool for my plugin',
      inputSchema: {
        type: 'object',
        properties: {
          param1: { type: 'string', description: 'Parameter 1' }
        },
        required: ['param1']
      },
      execute: async (params) => {
        // Tool logic
        const result = await doSomething(params.param1);
        
        return {
          content: [{ type: 'text', text: JSON.stringify(result) }]
        };
      }
    }
  ]
};
```

## Plugin Configuration

### package.json

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "main": "index.js",
  "type": "module",
  "unifiedMemory": {
    "plugin": true,
    "hooks": ["beforeStore", "afterStore"],
    "configSchema": {
      "apiUrl": { "type": "string" },
      "apiKey": { "type": "string" }
    }
  }
}
```

### config.json integration

```json
{
  "plugins": {
    "my-plugin": {
      "enabled": true,
      "apiUrl": "https://api.example.com",
      "apiKey": "secret-key"
    }
  }
}
```

## Best Practices

### Always return from hooks

```javascript
// Good
beforeStore: async (memory) => {
  return transformMemory(memory);
}

// Bad - returns undefined
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
}
```

### Handle errors gracefully

```javascript
beforeStore: async (memory) => {
  try {
    return await validateAndTransform(memory);
  } catch (error) {
    console.error('Plugin error:', error);
    return memory; // Return original on error
  }
}
```

### Clean up resources

```javascript
onShutdown: async () => {
  // Clear all timers
  this.timers.forEach(clearTimeout);
  
  // Close connections
  await this.db.close();
  
  // Remove event listeners
  this.handler && this.removeListener('event', this.handler);
}
```

## Testing Plugins

```javascript
import { describe, it, expect } from 'jest';

describe('my-plugin', () => {
  const { plugin } = require('./index.js');

  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
    expect(plugin.hooks).toBeDefined();
  });

  it('should transform memory in beforeStore', async () => {
    const memory = { text: '  Test  ', tags: ['TEST'] };
    const result = await plugin.hooks.beforeStore(memory);
    expect(result.text).toBe('Test');
    expect(result.tags).toContain('test');
  });

  it('should filter results in afterSearch', async () => {
    const results = [
      { id: '1', score: 0.9 },
      { id: '2', score: 0.5 }
    ];
    const filtered = await plugin.hooks.afterSearch(results, 'query');
    expect(filtered.length).toBe(1);
    expect(filtered[0].id).toBe('1');
  });
});
```
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
# Advanced Usage Guide

> Advanced features for power users: version control, deduplication, export, profiles, and more.

## 📚 Table of Contents

1. [Version Control](#-version-control)
2. [Deduplication](#-deduplication)
3. [Export & Import](#-export--import)
4. [Memory Profiles](#-memory-profiles)
5. [Preference Management](#-preference-management)
6. [Tier Management](#-tier-management)
7. [Quality & Decay](#-quality--decay)
8. [Prompt Composition](#-prompt-composition)

## 🔄 Version Control

Track changes and restore previous versions of memories.

### List Versions
```javascript
const { memoryVersion } = require('unified-memory');

const versions = await memoryVersion({
  action: "list",
  memoryId: "mem_xxx",
  limit: 10
});
```

### Compare Versions (Diff)
```javascript
const diff = await memoryVersion({
  action: "diff",
  memoryId: "mem_xxx",
  versionId1: "v1",
  versionId2: "v2"
});
```

### Restore Version
```javascript
await memoryVersion({
  action: "restore",
  memoryId: "mem_xxx",
  versionId: "v1",
  preview: false  // Set true to preview without restoring
});
```

## 🔀 Deduplication

Find and merge duplicate memories.

### Find Duplicates (Dry Run)
```javascript
const { memoryDedup } = require('unified-memory');

const duplicates = await memoryDedup({
  threshold: 0.85,  // Similarity threshold (0-1)
  dryRun: true      // Preview only
});
```

### Merge Duplicates
```javascript
// Actually merge duplicates
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: false
});
```

### Dedup Response
```javascript
{
  found: 5,
  merged: 3,
  candidates: [
    {
      original: "mem_xxx",
      duplicate: "mem_yyy",
      similarity: 0.92,
      merged: true
    }
  ]
}
```

## 📤 Export & Import

### Export Formats

```javascript
const { memoryExport } = require('unified-memory');

// Export as JSON
await memoryExport({
  format: "json",
  output: "~/exports/memories.json"
});

// Export as Markdown
await memoryExport({
  format: "markdown",
  output: "~/exports/memories.md"
});

// Export as CSV
await memoryExport({
  format: "csv",
  output: "~/exports/memories.csv"
});
```

### Export with Filters
```javascript
await memoryExport({
  format: "json",
  output: "~/exports/work-memories.json",
  category: "preference",
  minImportance: 0.7,
  tags: ["work"]
});
```

## 👤 Memory Profiles

Get aggregated user profiles with static/dynamic separation.

```javascript
const { memoryProfile } = require('unified-memory');

const profile = await memoryProfile({
  scope: "user",        // "agent", "user", "team", "global"
  container_tag: "project-x",
  entity_filter: "preferences",
  static_days: 30,      // Days without access to mark as static
  limit: 100
});
```

### Profile Response
```javascript
{
  scope: "user",
  static: {
    preferences: [
      { key: "language", value: "Python", confidence: 0.95 },
      { key: "meeting_time", value: "morning", confidence: 0.85 }
    ],
    lastUpdated: "2026-03-15"
  },
  dynamic: {
    recent_topics: ["project-x", "deadlines", "meetings"],
    interaction_count: 42
  }
}
```

## ❤️ Preference Management

Unified preference slots with confidence scores.

### Get Preference
```javascript
const { memoryPreference } = require('unified-memory');

const pref = await memoryPreference({
  action: "get",
  key: "meeting_preference"
});
```

### Set Preference
```javascript
await memoryPreference({
  action: "set",
  key: "preferred_language",
  value: "Python",
  confidence: 0.9,
  source: "explicit"
});
```

### Update Preference
```javascript
await memoryPreference({
  action: "update",
  key: "preferred_language",
  value: "JavaScript",
  confidence: 0.85
});
```

### Merge Preferences
```javascript
await memoryPreference({
  action: "merge",
  slots: {
    language: { value: "TypeScript", confidence: 0.9 },
    editor: { value: "VS Code", confidence: 0.95 }
  }
});
```

### Delete Preference
```javascript
await memoryPreference({
  action: "delete",
  key: "old_preference"
});
```

### Infer Preferences
```javascript
const inferred = await memoryPreference({
  action: "infer",
  messageCount: 20
});
```

### Preference Actions

| Action | Description |
|--------|-------------|
| `get` | Get single preference |
| `set` | Create new preference |
| `update` | Update existing preference |
| `merge` | Merge multiple preferences |
| `delete` | Delete preference |
| `reset` | Reset all preferences |
| `stats` | Get preference statistics |
| `explain` | Explain preference confidence |
| `infer` | Infer from conversation |

## 📊 Tier Management

HOT/WARM/COLD tier operations.

### Check Tier Status
```javascript
const { memoryTier } = require('unified-memory');

const status = await memoryTier({
  action: "status"
});
```

### Migrate Memory to Tier
```javascript
await memoryTier({
  action: "migrate",
  memories: [{ id: "mem_xxx", targetTier: "COLD" }],
  apply: true
});
```

### Compress Memories
```javascript
await memoryTier({
  action: "compress",
  memories: [{ id: "mem_xxx" }],
  apply: true
});
```

### Redistribute Tiers
```javascript
await memoryTier({
  action: "redistribute",
  apply: true
});
```

### Tier Thresholds

| Tier | Age | Compression | Eligible for Dedup |
|------|-----|------------|-------------------|
| HOT | ≤ 7 days | None | Yes |
| WARM | 7-30 days | Light | Yes |
| COLD | > 30 days | Heavy | Yes |

Pinned memories are **never** compressed or deduplicated.

## ⭐ Quality & Decay

### Quality Scoring
```javascript
const { getMemoryQuality } = require('unified-memory');

const quality = await getMemoryQuality("mem_xxx");
```

### Time-Based Decay
Memories automatically decay in importance over time unless accessed.

## 📝 Prompt Composition

Compose memory context blocks for prompt injection.

```javascript
const { memoryCompose } = require('unified-memory');

const context = await memoryCompose({
  messages: [
    { role: "user", content: "What about the project deadline?" },
    { role: "assistant", content: "The project deadline is next Friday." }
  ],
  targetTokens: 2000,
  categories: ["fact", "preference"],
  query: "project deadline",
  messageWindow: 10
});
```

### Composition Priority
Memories are included in this order:
1. **PINNED** - Always included
2. **HOT** - Recently accessed (≤ 7 days)
3. **WARM** - Medium-term (7-30 days)
4. **COLD** - Older memories (> 30 days)

## 🔍 Advanced Search

### Maximum Marginal Relevance (MMR)
```javascript
const { memoryEngine } = require('unified-memory');

const results = await memoryEngine({
  action: "mmr",
  query: "project updates",
  documents: [{ id: "1", text: "..." }],
  topK: 5,
  lambda: 0.5  // Balance relevance vs diversity
});
```

### Reranking
```javascript
const ranked = await memoryEngine({
  action: "rerank",
  query: "meeting notes",
  documents: [{ id: "1", text: "..." }],
  method: "keyword"  // or "llm", "cross"
});
```

## 🧪 Testing & Verification

### Run Health Check
```javascript
const { memoryHealth } = require('unified-memory');

const health = await memoryHealth();
```

### Get Metrics
```javascript
const { memoryMetrics } = require('unified-memory');

const metrics = await memoryMetrics();
```

### WAL Operations
```javascript
const { memoryWal } = require('unified-memory');

// Initialize WAL
await memoryWal({
  action: "init",
  runId: "run-001"
});

// Flush WAL
await memoryWal({
  action: "flush"
});

// List WAL entries
const entries = await memoryWal({
  action: "list"
});
```

## 📚 Next Steps

- [Plugin Development](./plugins.md) - Build custom plugins
- [Integration Guide](./integration.md) - Connect to other systems
- [API Reference](../api/overview.md) - Complete API docs
- [Architecture Overview](../architecture/overview.md) - System design
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
# User Guides

> In-depth guides for using Unified Memory effectively.

## 📋 Guides in This Section

| Guide | Description | Level |
|-------|-------------|-------|
| [Basic Usage](./basic-usage.md) | Core operations: store, search, list, delete | Beginner |
| [Advanced Usage](./advanced-usage.md) | Version control, dedup, export, profiles | Intermediate |
| [Plugin Development](./plugins.md) | Build custom plugins | Advanced |
| [Integration](./integration.md) | Connect to other systems | Intermediate |

## 🎯 Choose Your Path

**New to Unified Memory?**
Start with [Basic Usage](./basic-usage.md) to learn core operations.

**Want to extend functionality?**
Learn about [Plugin Development](./plugins.md) to build custom plugins.

**Need to integrate with existing systems?**
Check the [Integration Guide](./integration.md) for connectors and APIs.

## 📚 Prerequisites

Before reading these guides, you should:
- Complete the [Quick Start Tutorial](../getting-started/quickstart.md)
- Have Unified Memory installed and running
- Understand basic JavaScript/TypeScript (for API guides)

## 🔧 Common Operations

### Store Memories
```javascript
// Basic storage
await addMemory({ text: "Important note", tags: ["work"] });

// With metadata
await addMemory({
  text: "Meeting at 3 PM",
  category: "fact",
  importance: 0.9,
  tags: ["meeting"],
  metadata: { participants: ["Alice", "Bob"] }
});
```

### Search Memories
```javascript
// Simple search
const results = await searchMemories("meeting notes");

// Hybrid search
const results = await searchMemories("project update", {
  mode: "hybrid",
  vectorWeight: 0.7,
  bm25Weight: 0.3
});
```

### Manage Memories
```javascript
// List all
const all = await getAllMemories();

// Get by ID
const memory = await getMemory(memoryId);

// Delete
await deleteMemory(memoryId);
```

## 🚀 Quick Links

- [API Reference](../api/overview.md) - Complete API documentation
- [Architecture](../architecture/overview.md) - System design
- [Configuration](../getting-started/configuration.md) - Configuration options
- [Troubleshooting](../reference/troubleshooting.md) - Common issues
# Plugin Development Guide

> Build custom plugins to extend Unified Memory functionality.

## 📚 Table of Contents

1. [Plugin Overview](#-plugin-overview)
2. [Creating a Plugin](#-creating-a-plugin)
3. [Lifecycle Hooks](#-lifecycle-hooks)
4. [Plugin Examples](#-plugin-examples)
5. [Plugin API](#-plugin-api)
6. [Plugin Configuration](#-plugin-configuration)
7. [Publishing Plugins](#-publishing-plugins)

## 🔌 Plugin Overview

Plugins extend Unified Memory with custom functionality:

| Plugin Type | Description |
|-------------|-------------|
| **Sync Bridge** | Connect to external memory systems |
| **Processor** | Transform memories before storage |
| **Search Engine** | Add custom search algorithms |
| **Exporter** | Export to external formats |
| **Observer** | Monitor and report system metrics |

## 📁 Plugin Structure

```
~/.unified-memory/plugins/
└── my-plugin/
    ├── index.js          # Main entry point
    ├── package.json      # Package configuration
    └── README.md         # Documentation
```

## ✏️ Creating a Plugin

### Basic Plugin Template

```javascript
// index.js
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  // Lifecycle hooks
  hooks: {
    beforeStore: async (memory) => {
      // Transform memory before storage
      memory.metadata = memory.metadata || {};
      memory.metadata.processedBy = 'my-plugin';
      return memory;
    },
    afterSearch: async (results) => {
      // Post-process search results
      return results.filter(r => r.score > 0.5);
    }
  },

  // Plugin tools (MCP tools exposed by this plugin)
  tools: [
    {
      name: 'my_plugin_tool',
      description: 'Custom tool exposed by my plugin',
      execute: async (params) => {
        return { success: true, data: params };
      }
    }
  ]
};
```

### package.json

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin for Unified Memory",
  "main": "index.js",
  "type": "module",
  "keywords": ["unified-memory", "plugin"],
  "engines": {
    "unified-memory": ">=5.0.0"
  }
}
```

## 🪝 Lifecycle Hooks

### Available Hooks

| Hook | Timing | Purpose |
|------|--------|---------|
| `beforeStore` | Before memory stored | Transform or validate |
| `afterStore` | After memory stored | Trigger side effects |
| `beforeSearch` | Before search executed | Modify query |
| `afterSearch` | After search results | Filter or rerank |
| `beforeDelete` | Before memory deleted | Cleanup related data |
| `afterDelete` | After memory deleted | Notify external systems |
| `onInit` | On plugin load | Initialize resources |
| `onShutdown` | On plugin unload | Cleanup resources |

### Hook Signatures

```javascript
// Before Store Hook
async beforeStore(memory) {
  // memory: the memory object to be stored
  // Return modified memory or throw to reject
  return memory;
}

// After Store Hook
async afterStore(memory, result) {
  // memory: the stored memory
  // result: storage result
}

// Before Search Hook
async beforeSearch(query, options) {
  // query: search query string
  // options: search options
  // Return modified query/options
  return { query, options };
}

// After Search Hook
async afterSearch(results, query) {
  // results: search results array
  // query: original query
  // Return modified results
  return results;
}

// On Init Hook
async onInit(context) {
  // context: plugin context with config, storage, etc.
  // Initialize resources here
}

// On Shutdown Hook
async onShutdown() {
  // Cleanup resources here
}
```

## 💡 Plugin Examples

### Example 1: Tag Normalizer

Automatically normalize and add tags to memories:

```javascript
// tag-normalizer/index.js
export const plugin = {
  name: 'tag-normalizer',
  version: '1.0.0',

  hooks: {
    beforeStore: async (memory) => {
      if (memory.tags) {
        // Normalize tags: lowercase, trim, dedupe
        memory.tags = [...new Set(
          memory.tags.map(t => t.toLowerCase().trim())
        )];
      }
      return memory;
    }
  }
};
```

### Example 2: External Sync Bridge

Sync memories with an external system:

```javascript
// external-sync/index.js
export const plugin = {
  name: 'external-sync',
  version: '1.0.0',

  async onInit(context) {
    this.externalApi = context.config.apiUrl;
    this.apiKey = context.config.apiKey;
  },

  hooks: {
    afterStore: async (memory) => {
      // Sync to external system
      await fetch(`${this.externalApi}/memories`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(memory)
      });
    },

    afterDelete: async (memoryId) => {
      // Remove from external system
      await fetch(`${this.externalApi}/memories/${memoryId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        }
      });
    }
  }
};
```

### Example 3: Search Result Filter

Filter search results based on custom rules:

```javascript
// age-filter/index.js
export const plugin = {
  name: 'age-filter',
  version: '1.0.0',

  hooks: {
    afterSearch: async (results, query) => {
      // Filter out memories older than 90 days
      const cutoff = Date.now() - (90 * 24 * 60 * 60 * 1000);
      return results.filter(result => {
        return new Date(result.created_at).getTime() > cutoff;
      });
    }
  }
};
```

### Example 4: Custom Search Engine

Add a new search algorithm:

```javascript
// fuzzy-search/index.js
export const plugin = {
  name: 'fuzzy-search',
  version: '1.0.0',

  tools: [
    {
      name: 'fuzzy_search',
      description: 'Fuzzy text search with typo tolerance',
      execute: async (params) => {
        const { query, threshold = 0.8 } = params;
        const allMemories = await getAllMemories();
        
        return allMemories.filter(memory => {
          const similarity = calculateFuzzyScore(query, memory.text);
          return similarity >= threshold;
        });
      }
    }
  ]
};
```

## 🔧 Plugin API

### Context Object

The context object passed to `onInit`:

```javascript
{
  config: { /* plugin configuration */ },
  storage: { /* storage interface */ },
  search: { /* search interface */ },
  emit: (event, data) => {}  // Event emitter
}
```

### Storage Interface

```javascript
// Inside a hook
const memory = await context.storage.getMemory(id);
const allMemories = await context.storage.getAllMemories();
await context.storage.addMemory(memory);
await context.storage.updateMemory(id, updates);
await context.storage.deleteMemory(id);
```

### Search Interface

```javascript
// Inside a hook
const results = await context.search.hybridSearch(query, options);
const bm25Results = await context.search.bm25Search(query);
const vectorResults = await context.search.vectorSearch(query);
```

### Event Emitter

```javascript
// Emit events
context.emit('memory:stored', memory);
context.emit('search:executed', { query, results });
context.emit('error', { hook: 'beforeStore', error });
```

## ⚙️ Plugin Configuration

### config.json

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["tag-normalizer", "external-sync"]
  }
}
```

### Plugin-specific Config

```json
{
  "plugins": {
    "external-sync": {
      "apiUrl": "https://api.example.com",
      "apiKey": "your-api-key",
      "syncInterval": 300000
    }
  }
}
```

## 📦 Publishing Plugins

### Directory Structure
```
my-plugin/
├── index.js
├── package.json
├── README.md
└── tests/
    └── index.test.js
```

### package.json Requirements

```json
{
  "name": "unified-memory-my-plugin",
  "version": "1.0.0",
  "description": "Description of my plugin",
  "main": "index.js",
  "type": "module",
  "keywords": ["unified-memory", "plugin"],
  "engines": {
    "unified-memory": ">=5.0.0"
  },
  "license": "MIT"
}
```

### README Template

```markdown
# Unified Memory - My Plugin

Description of what this plugin does.

## Installation

```bash
npm install unified-memory-my-plugin
```

## Configuration

```json
{
  "plugins": {
    "enabled": ["my-plugin"]
  }
}
```

## Usage

Explain how to use the plugin.

## License

MIT
```

## 🧪 Testing Plugins

```javascript
// tests/index.test.js
import { describe, it, expect } from 'jest';
import { plugin } from '../index.js';

describe('my-plugin', () => {
  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
  });

  it('should transform memory in beforeStore', async () => {
    const memory = { text: 'Test', tags: ['TEST'] };
    const result = await plugin.hooks.beforeStore(memory);
    expect(result.tags).toContain('test');
  });
});
```

## 📚 Next Steps

- [Integration Guide](./integration.md) - Connect to other systems
- [API Reference](../api/overview.md) - Complete API docs
- [Architecture Overview](../architecture/overview.md) - System design
# Integration Guide

> Connect Unified Memory to other systems and applications.

## 📚 Table of Contents

1. [MCP Integration](#-mcp-integration)
2. [REST API](#-rest-api)
3. [JavaScript SDK](#-javascript-sdk)
4. [CLI Integration](#-cli-integration)
5. [WebSocket](#-websocket)
6. [External Connectors](#-external-connectors)

## 🔌 MCP Integration

Model Context Protocol (MCP) integration for AI assistants.

### Configure MCP Server

```json
{
  "mcpServers": {
    "unified-memory": {
      "command": "npx",
      "args": ["-y", "unified-memory", "serve"],
      "env": {
        "UNIFIED_MEMORY_PORT": "3851"
      }
    }
  }
}
```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `memory_search` | Hybrid search memories |
| `memory_store` | Store new memory |
| `memory_list` | List all memories |
| `memory_delete` | Delete memory by ID |
| `memory_stats` | Get memory statistics |
| `memory_health` | Health check |
| `memory_compose` | Compose prompt context |
| `memory_profile` | Get user profile |
| `memory_preference` | Manage preferences |
| `memory_version` | Version control |
| `memory_tier` | Tier management |
| `memory_dedup` | Deduplication |
| `memory_export` | Export memories |
| `memory_pin` | Pin/unpin memories |

### Example: Using with OpenClaw

```javascript
// In your OpenClaw skill or agent
const result = await mcp.call('unified-memory', 'memory_search', {
  query: 'user preferences',
  topK: 5,
  mode: 'hybrid'
});

console.log(result.results);
```

## 🌐 REST API

Start the REST API server:

```bash
unified-memory serve --port 3851
```

### Endpoints

#### Search Memories
```
GET /api/memories/search?q=<query>&mode=<mode>&topK=<n>
```

```bash
curl "http://localhost:3851/api/memories/search?q=quarterly%20reports&mode=hybrid&topK=5"
```

#### List Memories
```
GET /api/memories?limit=<n>&offset=<n>
```

```bash
curl "http://localhost:3851/api/memories?limit=10&offset=0"
```

#### Get Memory
```
GET /api/memories/:id
```

```bash
curl "http://localhost:3851/api/memories/mem_xxx"
```

#### Store Memory
```
POST /api/memories
Content-Type: application/json

{
  "text": "Memory content",
  "category": "fact",
  "importance": 0.8,
  "tags": ["work"]
}
```

```bash
curl -X POST "http://localhost:3851/api/memories" \
  -H "Content-Type: application/json" \
  -d '{"text":"New memory","tags":["test"]}'
```

#### Delete Memory
```
DELETE /api/memories/:id
```

```bash
curl -X DELETE "http://localhost:3851/api/memories/mem_xxx"
```

#### Statistics
```
GET /api/stats
```

```bash
curl "http://localhost:3851/api/stats"
```

#### Health Check
```
GET /api/health
```

```bash
curl "http://localhost:3851/api/health"
```

## 📦 JavaScript SDK

### Installation

```bash
npm install unified-memory
```

### Basic Usage

```javascript
import { 
  addMemory, 
  searchMemories, 
  getAllMemories,
  getMemory,
  deleteMemory 
} from 'unified-memory';

// Store
const id = await addMemory({
  text: "User preference for Python",
  category: "preference",
  importance: 0.9
});

// Search
const results = await searchMemories("Python preference");

// List
const all = await getAllMemories();

// Get
const memory = await getMemory(id);

// Delete
await deleteMemory(id);
```

### Advanced Usage

```javascript
import {
  beginTransaction,
  commitTransaction,
  rollbackTransaction,
  memoryProfile,
  memoryPreference,
  memoryExport
} from 'unified-memory';

// Atomic transaction
const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (e) {
  await rollbackTransaction(tx);
}

// Profile
const profile = await memoryProfile({ scope: "user" });

// Preferences
await memoryPreference({
  action: "set",
  key: "language",
  value: "Python",
  confidence: 0.95
});

// Export
await memoryExport({
  format: "json",
  output: "~/memories.json"
});
```

## 💻 CLI Integration

### Basic Commands

```bash
# Add memory
unified-memory add "Remember to check reports" --tags work,reminder

# Search
unified-memory search "reports"

# List
unified-memory list

# Get specific
unified-memory get <id>

# Delete
unified-memory delete <id>

# Stats
unified-memory stats
```

### Script Integration

```bash
#!/bin/bash
# daily-sync.sh

# Export memories
unified-memory export --format json --output /tmp/memories.json

# Process with external tool
process_memories.py /tmp/memories.json

# Import updated memories
unified-memory import /tmp/processed_memories.json
```

## 🔌 WebSocket

Real-time updates via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:3851/ws');

ws.on('open', () => {
  // Subscribe to events
  ws.send(JSON.stringify({
    action: 'subscribe',
    events: ['memory:stored', 'memory:deleted', 'search:executed']
  }));
});

ws.on('message', (event) => {
  const data = JSON.parse(event);
  console.log('Event:', data.type, data.payload);
});
```

### WebSocket Events

| Event | Payload |
|-------|---------|
| `memory:stored` | New memory object |
| `memory:updated` | Updated memory |
| `memory:deleted` | Memory ID |
| `search:executed` | Query and result count |
| `health:changed` | Health status change |

## 🔗 External Connectors

### Workspace Memory Sync

Sync with OpenClaw Workspace Memory:

```bash
# Manual sync
npm run sync:manual

# Scheduled sync (daily at 2 AM)
npm run sync

# Generate crontab
npm run crontab
```

### Custom Connector

```javascript
// connectors/my-system.js
export const connector = {
  name: 'my-system',
  
  async pull() {
    // Fetch from external system
    const data = await fetch('https://api.example.com/memories');
    return data.map(item => ({
      text: item.content,
      tags: item.labels,
      metadata: { source: 'my-system', externalId: item.id }
    }));
  },
  
  async push(memories) {
    // Push to external system
    for (const memory of memories) {
      await fetch('https://api.example.com/memories', {
        method: 'POST',
        body: JSON.stringify({
          content: memory.text,
          labels: memory.tags
        })
      });
    }
  }
};
```

## 📊 Integration Examples

### Node.js with Express

```javascript
import express from 'express';
import { addMemory, searchMemories } from 'unified-memory';

const app = express();
app.use(express.json());

app.post('/memories', async (req, res) => {
  try {
    const id = await addMemory(req.body);
    res.json({ id, success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/memories/search', async (req, res) => {
  try {
    const results = await searchMemories(req.query.q);
    res.json(results);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000);
```

### Python Integration

```python
import requests

BASE_URL = "http://localhost:3851/api"

# Search
response = requests.get(f"{BASE_URL}/memories/search", params={
    "q": "quarterly reports",
    "mode": "hybrid",
    "topK": 5
})
print(response.json())

# Store
response = requests.post(f"{BASE_URL}/memories", json={
    "text": "Python preference for data work",
    "category": "preference",
    "tags": ["python", "data"]
})
print(response.json())
```

## 📚 Next Steps

- [API Reference](../api/overview.md) - Complete API documentation
- [Plugin Development](./plugins.md) - Build custom plugins
- [Architecture Overview](../architecture/overview.md) - System design
- [Troubleshooting](../reference/troubleshooting.md) - Common issues
# Reference Documentation

> Technical reference for configuration, troubleshooting, and FAQ.

## 📚 Contents

| Document | Description |
|----------|-------------|
| [Configuration Reference](./configuration.md) | All configuration options |
| [Troubleshooting](./troubleshooting.md) | Common issues and solutions |
| [FAQ](./faq.md) | Frequently asked questions |

## Quick Links

- [Configuration](./configuration.md) - Complete config reference
- [Troubleshooting](./troubleshooting.md) - Fix common problems
- [FAQ](./faq.md) - Common questions
# Frequently Asked Questions

> Common questions about Unified Memory.

## General

### What is Unified Memory?

Unified Memory is an enterprise-grade memory management system for AI agents that provides:
- Persistent storage for memories across sessions
- Hybrid search (BM25 + Vector + RRF) for accurate retrieval
- Atomic transactions with WAL for data safety
- Plugin system for extensibility

### What version is current?

The current version is **v5.2.0**. Check with:
```bash
unified-memory --version
```

### What license does it use?

MIT License. See [LICENSE](../../LICENSE) file for details.

---

## Installation

### What are the requirements?

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0 (or yarn)
- **Git** (for manual installation)
- **Ollama** (optional, for vector search)

### How do I install?

**Quick install:**
```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**Or via npm:**
```bash
npm install -g unified-memory
```

### Can I use it without Ollama?

Yes, but you'll only have BM25 search. Vector search requires Ollama:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull embedding model
ollama pull nomic-embed-text

# Start Ollama
ollama serve
```

---

## Usage

### How do I store a memory?

**CLI:**
```bash
unified-memory add "Remember to check reports" --tags work,reminder
```

**JavaScript:**
```javascript
const { addMemory } = require('unified-memory');
await addMemory({
  text: "Remember to check reports",
  tags: ["work", "reminder"]
});
```

### How do I search?

**CLI:**
```bash
unified-memory search "quarterly reports"
```

**JavaScript:**
```javascript
const { searchMemories } = require('unified-memory');
const results = await searchMemories("quarterly reports");
```

### What's the difference between search modes?

| Mode | Description | Best For |
|------|-------------|----------|
| `hybrid` | BM25 + Vector + RRF | General use |
| `bm25` | Keyword only | Exact matches |
| `vector` | Semantic only | Conceptual matches |

### How do transactions work?

```javascript
const { beginTransaction, commitTransaction, rollbackTransaction, addMemory } = require('unified-memory');

const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (e) {
  await rollbackTransaction(tx);
}
```

---

## Data

### Where is data stored?

| Data | Location |
|------|----------|
| Memories | `~/.unified-memory/memories.json` |
| Vectors | `~/.unified-memory/vector.lance` |
| Config | `~/.unified-memory/config.json` |
| WAL | `~/.unified-memory/transactions.log` |
| Logs | `~/.unified-memory/logs/` |

### How do I backup data?

```bash
# Export to file
unified-memory export --format json --output ~/backup.json

# Or use the backup directory
ls ~/.unified-memory/backups/
```

### Can I use a different storage location?

Yes, configure in `config.json`:
```json
{
  "storage": {
    "memoryFile": "/custom/path/memories.json"
  }
}
```

---

## Search

### Why doesn't search find my memory?

1. Check if memory exists: `unified-memory list`
2. Rebuild index: `unified-memory rebuild-index`
3. Try simpler terms
4. Check importance score (lower = less likely to appear)

### What is RRF?

Reciprocal Rank Fusion combines results from multiple search algorithms:
- Takes rankings from BM25 and vector search
- Combines them using formula: `RRF = 1/(k + rank)`
- Produces better results than either alone

### How do I improve search accuracy?

1. Use more specific tags
2. Set higher importance scores
3. Add metadata for filtering
4. Use hybrid mode (default)

---

## Performance

### Why is search slow?

Possible causes:
- Large dataset (> 10,000 memories)
- Ollama not running
- Cache disabled
- No vector index

Solutions:
```bash
# Enable caching (default is on)
# Check config: "cache": { "enable": true }

# Restart Ollama
ollama serve

# Rebuild index
unified-memory rebuild-index
```

### How much memory does it use?

With ~1,760 memories:
- ~245 MB RAM
- ~50 MB storage

Scales linearly with memory count.

---

## Plugins

### How do I install a plugin?

```bash
# Copy plugin to plugins directory
cp my-plugin ~/.unified-memory/plugins/

# Enable in config
# "plugins": { "enabled": ["my-plugin"] }

# Restart server
```

### Can I create custom plugins?

Yes! See [Plugin Development Guide](../guides/plugins.md).

### How do plugins work?

Plugins hook into lifecycle events:
- `beforeStore` - Transform before saving
- `afterStore` - React after saving
- `beforeSearch` - Modify search query
- `afterSearch` - Filter results

---

## Troubleshooting

### "Module not found" error

```bash
npm install
```

### Vector store initialization failed

```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### Ollama connection failed

```bash
# Check Ollama is running
ollama serve

# Pull model
ollama pull nomic-embed-text

# Test
curl http://localhost:11434/api/generate -d '{"model":"nomic-embed-text","prompt":"Hi"}'
```

---

## Development

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests: `npm test`
5. Submit PR

See [Contributing Guidelines](../../CONTRIBUTING.md) for details.

### How do I run tests?

```bash
# All tests
npm test

# Unit tests only
npm run test:unit

# Integration tests
npm run test:integration

# Watch mode
npm run test:watch
```

### How do I build for production?

```bash
npm run build
npm run deploy
```

---

## Migration

### How do I migrate from v4 to v5?

v5 is backwards compatible with v4 storage. Simply:
1. Install v5.2.0
2. Existing data is automatically upgraded
3. New features (atomic transactions) are enabled by default

### How do I export/import between systems?

```bash
# Export on old system
unified-memory export --format json --output memories.json

# Transfer file to new system

# Import on new system
unified-memory import --input memories.json
```
# Configuration Reference

> Complete reference for all configuration options.

## Configuration File Location

```
~/.unified-memory/config.json
```

## Full Configuration Schema

```json
{
  "storage": { ... },
  "transaction": { ... },
  "search": { ... },
  "cache": { ... },
  "embedding": { ... },
  "tier": { ... },
  "plugins": { ... },
  "observability": { ... },
  "server": { ... }
}
```

## Storage Configuration

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    },
    "backup": {
      "enable": true,
      "interval": 86400,
      "maxBackups": 5,
      "path": "~/.unified-memory/backups"
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `string` | `"json"` | Storage mode: `"json"` or `"sqlite"` |
| `memoryFile` | `string` | `"~/.unified-memory/memories.json"` | Memory file path |
| `vectorStore.backend` | `string` | `"lancedb"` | Vector backend: `"lancedb"` or `"chromadb"` |
| `vectorStore.path` | `string` | `"~/.unified-memory/vector.lance"` | Vector store path |
| `vectorStore.dimension` | `number` | `768` | Embedding dimension |
| `backup.enable` | `boolean` | `true` | Enable backups |
| `backup.interval` | `number` | `86400` | Backup interval in seconds |
| `backup.maxBackups` | `number` | `5` | Maximum backups to keep |

## Transaction Configuration

```json
{
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true,
    "timeout": 30000
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable` | `boolean` | `true` | Enable atomic transactions |
| `recoveryLog` | `string` | `"~/.unified-memory/transactions.log"` | WAL log path |
| `fsync` | `boolean` | `true` | fsync on write |
| `timeout` | `number` | `30000` | Transaction timeout (ms) |

## Search Configuration

```json
{
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10,
    "minScore": 0.1,
    "enableCache": true
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `defaultMode` | `string` | `"hybrid"` | Default search mode |
| `bm25Weight` | `number` | `0.3` | BM25 weight in hybrid (0-1) |
| `vectorWeight` | `number` | `0.7` | Vector weight in hybrid (0-1) |
| `rrfK` | `number` | `60` | RRF constant |
| `topK` | `number` | `10` | Default result count |
| `minScore` | `number` | `0.1` | Minimum relevance score |
| `enableCache` | `boolean` | `true` | Enable search caching |

## Cache Configuration

```json
{
  "cache": {
    "enable": true,
    "type": "semantic",
    "maxSize": 1000,
    "ttl": 3600,
    "evictionPolicy": "lru"
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable` | `boolean` | `true` | Enable caching |
| `type` | `string` | `"semantic"` | Cache type: `"semantic"` or `"exact"` |
| `maxSize` | `number` | `1000` | Maximum entries |
| `ttl` | `number` | `3600` | TTL in seconds |
| `evictionPolicy` | `string` | `"lru"` | Eviction policy |

## Embedding Configuration

```json
{
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "url": "http://localhost:11434",
    "batchSize": 100,
    "dimension": 768,
    "timeout": 30000
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `provider` | `string` | `"ollama"` | Embedding provider |
| `model` | `string` | `"nomic-embed-text"` | Model name |
| `url` | `string` | `"http://localhost:11434"` | Provider URL |
| `batchSize` | `number` | `100` | Batch size |
| `dimension` | `number` | `768` | Embedding dimension |
| `timeout` | `number` | `30000` | Request timeout (ms) |

## Tier Configuration

```json
{
  "tier": {
    "hot": {
      "maxAge": 7,
      "compression": false
    },
    "warm": {
      "minAge": 7,
      "maxAge": 30,
      "compression": "light"
    },
    "cold": {
      "minAge": 30,
      "compression": "heavy"
    }
  }
}
```

| Tier | Option | Type | Default | Description |
|------|--------|------|---------|-------------|
| HOT | `maxAge` | `number` | `7` | Max age in days |
| HOT | `compression` | `boolean` | `false` | Enable compression |
| WARM | `minAge` | `number` | `7` | Min age in days |
| WARM | `maxAge` | `number` | `30` | Max age in days |
| WARM | `compression` | `string` | `"light"` | Compression level |
| COLD | `minAge` | `number` | `30` | Min age in days |
| COLD | `compression` | `string` | `"heavy"` | Compression level |

## Plugin Configuration

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["sync-workspace"],
    "sync-workspace": {
      "apiUrl": "https://api.example.com",
      "syncInterval": 300000
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dir` | `string` | `"~/.unified-memory/plugins"` | Plugin directory |
| `autoReload` | `boolean` | `true` | Hot reload plugins |
| `enabled` | `array` | `[]` | Enabled plugins list |

## Observability Configuration

```json
{
  "observability": {
    "metrics": {
      "enable": true,
      "port": 3852
    },
    "logging": {
      "level": "info",
      "file": "~/.unified-memory/logs/app.log",
      "maxSize": "10m",
      "maxFiles": 5
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `metrics.enable` | `boolean` | `true` | Enable metrics |
| `metrics.port` | `number` | `3852` | Metrics port |
| `logging.level` | `string` | `"info"` | Log level |
| `logging.file` | `string` | `"~/.unified-memory/logs/app.log"` | Log file path |
| `logging.maxSize` | `string` | `"10m"` | Max log file size |
| `logging.maxFiles` | `number` | `5` | Max log files |

## Server Configuration

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 3851,
    "cors": {
      "enable": true,
      "origins": ["*"]
    },
    "rateLimit": {
      "enable": true,
      "windowMs": 60000,
      "maxRequests": 100
    }
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `host` | `string` | `"0.0.0.0"` | Server host |
| `port` | `number` | `3851` | Server port |
| `cors.enable` | `boolean` | `true` | Enable CORS |
| `cors.origins` | `array` | `["*"]` | Allowed origins |
| `rateLimit.enable` | `boolean` | `true` | Enable rate limiting |
| `rateLimit.windowMs` | `number` | `60000` | Rate limit window |
| `rateLimit.maxRequests` | `number` | `100` | Max requests per window |

## Environment Variables

Override config with environment variables:

```bash
# Storage
UNIFIED_MEMORY_STORAGE_MODE=json
UNIFIED_MEMORY_MEMORY_FILE=~/.unified-memory/memories.json

# Vector Store
UNIFIED_MEMORY_VECTOR_BACKEND=lancedb
UNIFIED_MEMORY_VECTOR_PATH=~/.unified-memory/vector.lance

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=nomic-embed-text

# Server
UNIFIED_MEMORY_PORT=3851
UNIFIED_MEMORY_HOST=0.0.0.0

# Debug
UNIFIED_MEMORY_DEBUG=1
UNIFIED_MEMORY_LOG_LEVEL=debug
```

## Config Validation

```bash
# Validate config
unified-memory config:validate

# Show current config
unified-memory config:show

# Generate default config
unified-memory config:init
```
# Troubleshooting Guide

> Solutions for common issues with Unified Memory.

## 📚 Contents

1. [Installation Issues](#installation-issues)
2. [Startup Issues](#startup-issues)
3. [Storage Issues](#storage-issues)
4. [Search Issues](#search-issues)
5. [Vector Store Issues](#vector-store-issues)
6. [Plugin Issues](#plugin-issues)
7. [Performance Issues](#performance-issues)
8. [Data Recovery](#data-recovery)

## Installation Issues

### "command not found: unified-memory"

**Cause:** Installation not in PATH

**Solution:**
```bash
# Check installation
npm list -g unified-memory

# Reinstall
npm install -g unified-memory

# Or add to PATH
export PATH="$(npm root -g)/bin:$PATH"
```

### "Node.js version too old"

**Cause:** Node.js version < 18.0.0

**Solution:**
```bash
# Check version
node --version

# Update Node.js
# macOS/Linux
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo apt install -y nodejs

# Or use nvm
nvm install 18
nvm use 18
```

### "EACCES: permission denied"

**Cause:** npm global directory not writable

**Solution:**
```bash
# Create npm global directory
mkdir ~/.npm-global

# Configure npm
npm config set prefix '~/.npm-global'

# Add to PATH
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install again
npm install -g unified-memory
```

## Startup Issues

### "Failed to initialize storage"

**Cause:** Cannot create/read storage directory

**Solution:**
```bash
# Create directory manually
mkdir -p ~/.unified-memory

# Fix permissions
chmod 755 ~/.unified-memory

# Reinitialize
unified-memory init
```

### "Port already in use"

**Cause:** Another process using port 3851

**Solution:**
```bash
# Find process
lsof -i :3851

# Kill process or use different port
unified-memory serve --port 3852
```

### "Configuration file invalid"

**Cause:** Invalid JSON in config

**Solution:**
```bash
# Validate JSON
cat ~/.unified-memory/config.json | python3 -m json.tool

# Reset to default
rm ~/.unified-memory/config.json
unified-memory init
```

## Storage Issues

### "Memory file corrupted"

**Cause:** JSON file is malformed

**Solution:**
```bash
# Check for backup
ls -la ~/.unified-memory/backups/

# Restore from backup
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json

# Or rebuild from WAL
unified-memory recover
```

### "Disk full"

**Cause:** Not enough disk space

**Solution:**
```bash
# Check disk space
df -h ~/.unified-memory

# Clean old backups
rm -rf ~/.unified-memory/backups/*

# Clean vector store (will rebuild)
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "Permission denied on memory file"

**Cause:** File permissions issue

**Solution:**
```bash
# Fix permissions
chmod 644 ~/.unified-memory/memories.json
chmod 755 ~/.unified-memory
```

## Search Issues

### "Search returns no results"

**Cause:** Empty index or wrong query

**Solution:**
```bash
# Check memories exist
unified-memory list

# Rebuild search index
unified-memory rebuild-index

# Try simpler query
unified-memory search "test"
```

### "Search very slow"

**Cause:** Large dataset, no caching

**Solution:**
```bash
# Enable caching (already default)
# Check config has cache.enable = true

# Rebuild BM25 index
unified-memory rebuild-bm25

# Check Ollama is running
ollama list
```

### "Vector search fails"

**Cause:** Ollama not running or no model

**Solution:**
```bash
# Start Ollama
ollama serve

# Pull embedding model
ollama pull nomic-embed-text

# Test Ollama
curl http://localhost:11434/api/generate -d '{"model":"nomic-embed-text","prompt":"test"}'
```

## Vector Store Issues

### "LanceDB initialization failed"

**Cause:** Corrupted vector store

**Solution:**
```bash
# Remove and rebuild
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "ChromaDB connection failed"

**Cause:** ChromaDB server not running

**Solution:**
```bash
# Start ChromaDB
docker run -d -p 8000:8000 chromadb/chroma

# Or switch to LanceDB
# Edit config.json:
# "vectorStore": { "backend": "lancedb", ... }
```

### "Embedding dimension mismatch"

**Cause:** Config dimension != model dimension

**Solution:**
```bash
# Check model dimension
ollama show nomic-embed-text

# Update config (e.g., for nomic-embed-text: 768)
# ~/.unified-memory/config.json
# "embedding": { "dimension": 768 }
```

## Plugin Issues

### "Plugin not loading"

**Cause:** Plugin has errors or missing dependencies

**Solution:**
```bash
# Check plugin directory
ls -la ~/.unified-memory/plugins/

# Enable debug logging
UNIFIED_MEMORY_DEBUG=1 unified-memory serve

# Check plugin syntax
node --check ~/.unified-memory/plugins/my-plugin/index.js
```

### "Plugin hot reload not working"

**Cause:** autoReload disabled

**Solution:**
```json
{
  "plugins": {
    "autoReload": true
  }
}
```

## Performance Issues

### "High memory usage"

**Cause:** Large dataset, no tier management

**Solution:**
```bash
# Run compression
unified-memory compress

# Migrate old memories to cold tier
unified-memory tier --action redistribute

# Reduce cache size
# Edit config:
# "cache": { "maxSize": 500 }
```

### "Slow startup"

**Cause:** Large memory file, rebuilding index

**Solution:**
```bash
# Compact memory file
unified-memory compact

# Use WAL recovery instead of full rebuild
# Config should have:
# "transaction": { "enable": true }
```

### "CPU usage high"

**Cause:** Too many background operations

**Solution:**
```bash
# Reduce BM25 rebuild frequency
# "search": { "bm25RebuildInterval": 86400 }

# Disable auto-compression
# "tier": { "autoCompress": false }
```

## Data Recovery

### "Recover from crash"

```bash
# Check WAL for uncommitted transactions
unified-memory wal --action list

# Recover data
unified-memory recover

# Verify
unified-memory stats
```

### "Restore from backup"

```bash
# List backups
ls -la ~/.unified-memory/backups/

# Restore specific backup
cp ~/.unified-memory/backups/memories-2026-04-15.json ~/.unified-memory/memories.json

# Restart server
unified-memory serve
```

### "Export/Import for migration"

```bash
# Export current data
unified-memory export --format json --output /tmp/memories.json

# Install on new system
npm install -g unified-memory

# Import data
unified-memory import --input /tmp/memories.json
```

## Getting Help

### Debug Mode

```bash
# Enable debug logging
UNIFIED_MEMORY_DEBUG=1 unified-memory serve

# Check logs
tail -f ~/.unified-memory/logs/app.log
```

### Health Check

```bash
# Run health check
unified-memory health

# Check specific components
unified-memory health --component storage
unified-memory health --component vector
unified-memory health --component wal
```

### Report Issues

When reporting issues, include:
- Unified Memory version: `unified-memory --version`
- Node.js version: `node --version`
- Operating system: `uname -a`
- Configuration: `cat ~/.unified-memory/config.json`
- Relevant logs: `~/.unified-memory/logs/`
# Unified Memory 文档

> 🧠 企业级记忆管理系统，支持混合搜索、原子事务和插件架构

[![版本](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](https://nodejs.org/)
[![许可证: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 快速链接

| 我想... | 查看 |
|---------|------|
| 快速开始 | [快速入门](./getting-started/quickstart.md) |
| 安装系统 | [安装指南](./getting-started/installation.md) |
| 配置设置 | [配置指南](./getting-started/configuration.md) |
| 学习基础使用 | [基础使用](./guides/basic-usage.md) |
| 探索高级功能 | [高级使用](./guides/advanced-usage.md) |
| 开发插件 | [插件开发](./guides/plugins.md) |
| 集成到我的应用 | [集成指南](./guides/integration.md) |
| 理解架构 | [架构概述](./architecture/overview.md) |
| 查找API参考 | [API参考](./api/overview.md) |
| 排查问题 | [故障排除](./reference/troubleshooting.md) |

## ✨ 核心特性

### 🔍 混合搜索
Unified Memory 结合多种搜索算法以获得最佳相关性：
- **BM25**：传统关键词搜索
- **向量搜索**：使用嵌入的语义相似度
- **RRF（倒数排名融合）**：组合多个排名器的结果

### ⚡ 原子事务
企业级数据一致性：
- **WAL（预写日志）**：崩溃恢复保证
- **两阶段提交**：JSON 和向量存储的原子写入
- **fsync 保证**：数据写入磁盘，防止丢失

### 🔌 插件系统
支持热重载的可扩展架构：
- **生命周期钩子**：操作前后的钩子
- **同步桥接**：连接外部记忆系统
- **自定义处理器**：添加自定义记忆处理

### 📊 性能
针对生产工作负载优化：
- **搜索速度提升 5-10 倍**（优化的向量引擎）
- **存储减少 60%**（智能压缩）
- **缓存命中率 78%**（语义缓存）
- **平均查询时间 45ms**

## 📦 快速开始

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# 存储记忆
unified-memory add "Remember to review quarterly reports" --tags work,reminder

# 搜索记忆
unified-memory search "quarterly reports"

# 使用 JavaScript API
node -e "
const { addMemory, searchMemories } = require('unified-memory');
(async () => {
  await addMemory({ text: 'My preference for morning meetings', tags: ['preference'] });
  const results = await searchMemories('meeting schedule');
  console.log(results);
})();
"
```

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端应用程序                           │
│          (OpenClaw, Web UI, CLI, API, MCP 客户端)          │
└───────────────────────────┬─────────────────────────────────┘
                            │ 调用 MCP 工具
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API 网关层                                │
│           (REST API, MCP 服务器, WebSocket)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    服务层                                    │
│     (记忆服务, 搜索服务, 缓存服务)                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    存储层                                    │
│        (SQLite, 向量数据库, 文件系统)                        │
└─────────────────────────────────────────────────────────────┘
```

## 📚 文档章节

### 入门指南
- [快速入门](./getting-started/quickstart.md) - 5分钟介绍
- [安装](./getting-started/installation.md) - 完整安装指南
- [配置](./getting-started/configuration.md) - 配置选项

### 用户指南
- [基础使用](./guides/basic-usage.md) - 核心操作
- [高级使用](./guides/advanced-usage.md) - 高级功能
- [插件开发](./guides/plugins.md) - 构建插件
- [集成](./guides/integration.md) - 连接到其他系统

### 架构
- [概述](./architecture/overview.md) - 系统设计
- [设计原则](./architecture/design-principles.md) - 关键原则
- [模块](./architecture/modules.md) - 模块参考
- [数据流](./architecture/data-flow.md) - 数据如何流经系统

### API 参考
- [概述](./api/overview.md) - API 介绍
- [核心 API](./api/core-api.md) - 核心函数
- [MCP 工具](./api/mcp-tools.md) - MCP 工具参考
- [插件 API](./api/plugin-api.md) - 插件开发

### 参考
- [配置参考](./reference/configuration.md) - 所有配置选项
- [故障排除](./reference/troubleshooting.md) - 常见问题
- [FAQ](./reference/faq.md) - 常见问题

## 🔧 开发

```bash
# 克隆并设置
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory
npm install

# 运行测试
npm test

# 构建生产版本
npm run build
```

## 🤝 贡献

欢迎贡献！请在提交 PR 之前阅读我们的[贡献指南](./contributing/guidelines.md)。

## 📄 许可证

MIT 许可证 - 请参阅 [LICENSE](../../LICENSE) 文件了解详情。

## 📞 支持

- [GitHub Issues](https://github.com/mouxangithub/unified-memory/issues)
- [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)

---

**版本**: 5.2.0 | **最后更新**: 2026-04-20
# 快速开始

> 5 分钟内启动并运行 Unified Memory

## 安装

```bash
npm install unified-memory
```

## 基本用法

```javascript
import { getEnhancedMemorySystem } from 'unified-memory';

const memory = await getEnhancedMemorySystem();

// 添加记忆
const memory = await memory.addMemory({
  text: '记得和设计团队的会议',
  category: '工作',
  importance: 0.8,
  tags: ['会议', '设计']
});

// 搜索记忆
const results = await memory.search('设计团队 会议');

// 获取所有记忆
const allMemories = await memory.getAllMemories();
```

## 配置

创建 `.env` 文件：

```bash
OLLAMA_URL=http://localhost:11434
MEMORY_FILE=./memory/memories.json
VECTOR_DB=lancedb
```

## 下一步

- [API 参考](../api/README.md) - 完整的 API 文档
- [架构设计](../architecture/README.md) - 系统设计
# 入门指南

> 从这里开始！本节帮助您在10分钟内安装和运行 Unified Memory。

## 📋 本节指南

| 指南 | 描述 | 时间 |
|------|------|------|
| [概述](./overview.md) | 什么是 Unified Memory？ | 2 分钟 |
| [安装](./installation.md) | 在您的系统上安装 | 3 分钟 |
| [快速入门](./quickstart.md) | 您的第一个记忆 | 5 分钟 |
| [配置](./configuration.md) | 自定义设置 | 3 分钟 |

## 🚀 快速导航

**初次接触 Unified Memory？** 从[概述](./overview.md)开始，了解它是什么以及为什么需要它。

**准备安装了？** 按照[安装指南](./installation.md)进行安装。

**想要快速演示？** 直接跳转到[快速入门](./quickstart.md)，在5分钟内存储和搜索您的第一个记忆。

## 🔑 前置条件

安装 Unified Memory 之前，请确保您拥有：

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0 或 **yarn** >= 1.22.0
- **Git**（用于手动安装）

完整功能所需的依赖：

| 功能 | 要求 |
|------|------|
| 向量搜索 | 本地运行 Ollama（或云嵌入 API） |
| Web UI | 现代浏览器（Chrome、Firefox、Safari、Edge） |
| MCP 服务器 | OpenClaw 或任何 MCP 兼容客户端 |

## 📥 安装选项

| 方法 | 适用于 | 命令 |
|------|--------|------|
| 安装脚本 | 大多数用户 | `curl -fsSL ... \| bash` |
| npm 全局安装 | Node.js 开发者 | `npm install -g unified-memory` |
| npm 本地安装 | 项目依赖 | `npm install unified-memory` |
| 手动克隆 | 贡献者 | `git clone ... && npm install` |

请参阅[安装指南](./installation.md)获取每种方法的详细说明。

## 🎯 下一步

安装后：

1. [配置 Unified Memory](./configuration.md) 以满足您的需求
2. 尝试[快速入门](./quickstart.md)教程
3. 了解[基础使用](../guides/basic-usage.md)

## 💡 需要帮助？

- 查看[故障排除](../reference/troubleshooting.md)了解常见问题
- 搜索 [GitHub Issues](https://github.com/mouxangithub/unified-memory/issues)
- 阅读 [FAQ](../reference/faq.md)
# 概述

> 了解 Unified Memory 是什么，它如何工作，以及它与其他记忆系统有何不同。

## 🤔 什么是 Unified Memory？

**Unified Memory** 是一个为企业级 AI 代理和应用设计的记忆管理系统。它提供：

1. **持久存储** - 跨会话存储记忆
2. **智能搜索** - 使用混合搜索（BM25 + 向量 + RRF）查找相关记忆
3. **原子操作** - 通过事务保证数据一致性
4. **插件架构** - 使用自定义插件扩展功能

## 🎯 它解决的核心问题

| 问题 | 解决方案 |
|------|----------|
| 记忆不会跨会话持久化 | 持久化 JSON + SQLite 存储 |
| 简单关键词搜索不够准确 | 混合搜索结合 BM25、向量和 RRF 融合 |
| 崩溃时数据丢失 | WAL（预写日志）+ fsync |
| 无法与其他记忆系统集成 | 插件系统与同步桥接 |

## 🏗️ 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│                    您的应用程序                             │
│            (OpenClaw, CLI, API, Web UI 等)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │ 调用 MCP 工具
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Unified Memory                           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   记忆      │  │   搜索      │  │   插件      │         │
│  │   存储      │  │   引擎      │  │   系统      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    WAL     │  │   向量      │  │   缓存      │         │
│  │   记录器   │  │   存储      │  │   层        │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 搜索如何工作

Unified Memory 使用**混合搜索**方法，结合多种排名算法：

### 1. BM25（关键词搜索）
基于词频和逆文档频率的传统相关性排名。适用于精确匹配。

### 2. 向量搜索（语义搜索）
将文本转换为嵌入向量并找到语义相似的记忆。适用于概念匹配。

### 3. RRF（倒数排名融合）
使用公式组合多个算法的排名：

```
RRF_score = Σ(1 / (k + rank_i))
```

其中 `k` 是常数（默认：60），`rank_i` 是算法 `i` 的排名。

## 💾 数据存储

### 记忆 JSON 文件
记忆内容的主要存储：
```
~/.unified-memory/memories.json
```

### 向量数据库
存储用于语义搜索的嵌入：
```
~/.unified-memory/vector.lance  (LanceDB)
~/.unified-memory/vector/        (ChromaDB 备选)
```

### WAL 日志
确保原子性和崩溃恢复：
```
~/.unified-memory/wal/
~/.unified-memory/transactions.log
```

## 🔐 数据安全特性

### 原子事务
两阶段提交确保：
- 记忆内容和向量一起写入
- 失败时回滚部分写入
- 系统崩溃时无数据丢失

### WAL 协议
预写日志保证：
- 在应用之前记录所有更改
- 系统可以从崩溃中恢复
- 启用 fsync 时零数据丢失

## 🔌 插件系统

插件使用自定义功能扩展 Unified Memory：

| 插件类型 | 描述 |
|---------|------|
| **同步桥接** | 连接到外部记忆系统（Workspace Memory 等） |
| **处理器** | 存储前转换记忆 |
| **搜索引擎** | 添加自定义搜索算法 |
| **导出器** | 导出到外部格式 |

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 搜索速度 | 平均 45ms | 向量优化后快 5-10 倍 |
| 存储 | 减少 60% | 与未压缩存储相比 |
| 缓存命中率 | 78% | 智能语义缓存 |
| 内存使用 | 约 245 MB | 1,760 条记忆时 |

## 🎓 记忆生命周期

记忆自动转换层级：

| 层级 | 年龄 | 描述 |
|------|------|------|
| **HOT** | ≤ 7 天 | 活跃，经常访问 |
| **WARM** | 7-30 天 | 不太活跃，轻压缩 |
| **COLD** | > 30 天 | 很少访问，重压缩 |

**固定的记忆**被排除在层级转换和压缩之外。

## 🔄 版本历史

Unified Memory 为所有记忆维护版本历史：
- 跟踪随时间的变化
- 比较版本（差异）
- 恢复以前的版本

## 🚀 下一步是什么？

- [安装 Unified Memory](./installation.md)
- [快速入门教程](./quickstart.md)
- [配置指南](./configuration.md)
- [基础使用指南](../guides/basic-usage.md)
# 安装指南

> 所有平台和方法的完整安装说明。

## 📋 前置条件

安装前，请验证您拥有：

```bash
# 检查 Node.js 版本（必须 >= 18.0.0）
node --version

# 检查 npm 版本（必须 >= 9.0.0）
npm --version

# 检查 Git
git --version
```

**向量搜索的可选依赖：**
```bash
# 安装 Ollama (macOS/Linux)
curl -fsSL https://ollama.com/install.sh | sh

# 启动 Ollama 并加载嵌入模型
ollama pull nomic-embed-text
ollama serve
```

## 📥 安装方法

### 方法 1：安装脚本（推荐）

安装脚本自动处理所有依赖和配置。

```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**脚本执行的操作：**
1. 检测您的操作系统和架构
2. 创建 `~/.unified-memory/` 目录
3. 全局安装 npm 包或克隆仓库
4. 设置配置文件
5. 初始化存储目录
6. 验证安装

### 方法 2：npm 全局安装

```bash
npm install -g unified-memory
```

**验证安装：**
```bash
unified-memory --version
# 应该输出：v5.2.0
```

### 方法 3：npm 本地安装（项目依赖）

```bash
# 创建新项目
mkdir my-project && cd my-project
npm init -y

# 作为依赖安装
npm install unified-memory
```

### 方法 4：手动克隆

```bash
# 克隆仓库
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory

# 安装依赖
npm install

# 构建生产版本
npm run deploy

# 全局链接（可选）
npm link
```

## 🐧 Linux 安装

### Ubuntu/Debian

```bash
# 安装依赖
sudo apt update
sudo apt install -y nodejs npm git

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

### Fedora/RHEL/CentOS

```bash
# 从 NodeSource 安装 Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs npm git

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

## 🍎 macOS 安装

### 使用 Homebrew

```bash
# 安装 Homebrew（如果还没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node

# 安装 Unified Memory
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

### 使用 nvm

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# 安装并使用 Node.js 18
nvm install 18
nvm use 18

# 安装 Unified Memory
npm install -g unified-memory
```

## 🪟 Windows 安装

### 使用 Node.js 安装程序

1. 从 [nodejs.org](https://nodejs.org/) 下载 Node.js 18+
2. 运行安装程序
3. 打开 PowerShell 并安装：

```powershell
npm install -g unified-memory
```

### 使用 Windows 子系统 Linux (WSL)

```bash
# 打开 WSL 终端
wsl

# 按照 Linux 安装说明进行
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

## 🐳 Docker 安装

### 使用预构建镜像

```bash
# 拉取镜像
docker pull mouxangithub/unified-memory:latest

# 运行容器
docker run -d \
  --name unified-memory \
  -v ~/.unified-memory:/data \
  -p 3851:3851 \
  mouxangithub/unified-memory:latest
```

### 构建自己的镜像

```dockerfile
FROM node:18-alpine

WORKDIR /app
RUN npm install -g unified-memory

VOLUME ["/data"]
EXPOSE 3851

CMD ["unified-memory", "serve"]
```

构建并运行：
```bash
docker build -t my-unified-memory .
docker run -d -v ~/.unified-memory:/data -p 3851:3851 my-unified-memory
```

## ⚙️ 安装后设置

### 1. 验证安装

```bash
unified-memory --version
# 输出：v5.2.0

unified-memory --help
```

### 2. 初始化存储

```bash
unified-memory init
```

这会创建：
- `~/.unified-memory/memories.json` - 主记忆存储
- `~/.unified-memory/vector.lance` - 向量数据库
- `~/.unified-memory/config.json` - 配置文件

### 3. 配置（可选）

编辑 `~/.unified-memory/config.json`：

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance"
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log"
  },
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7
  }
}
```

### 4. 启动 MCP 服务器

```bash
# 后台启动
unified-memory serve &

# 或使用 Node.js API
node -e "require('unified-memory').serve()"
```

## 🔧 安装故障排除

### "权限被拒绝" 错误

```bash
# 修复 npm 权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 或使用 sudo（不推荐）
sudo npm install -g unified-memory
```

### "Node.js 版本太旧" 错误

```bash
# 使用 nvm 更新 Node.js
nvm install 18
nvm use 18
nvm alias default 18
```

### "找不到模块" 安装后

```bash
# 重新安装依赖
npm cache clean --force
npm install
```

### Ollama 连接错误（向量搜索）

```bash
# 确保 Ollama 正在运行
ollama serve

# 测试 Ollama
curl http://localhost:11434/api/generate -d '{"model":"llama2","prompt":"Hi"}'

# 拉取嵌入模型
ollama pull nomic-embed-text
```

## 📦 卸载

```bash
# 删除 npm 包
npm uninstall -g unified-memory

# 删除数据目录（可选）
rm -rf ~/.unified-memory

# 删除 CLI 工具
rm -f /usr/local/bin/unified-memory
```

## 🚀 下一步

- [快速入门教程](./quickstart.md) - 存储您的第一个记忆
- [配置指南](./configuration.md) - 自定义设置
- [基础使用指南](../guides/basic-usage.md) - 学习核心操作
# 配置指南

> 自定义 Unified Memory 以满足您的需求。

## 📁 配置文件

主配置文件位于：
```
~/.unified-memory/config.json
```

## 🔧 配置部分

### 存储配置

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    },
    "backup": {
      "enable": true,
      "interval": 86400,
      "maxBackups": 5
    }
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `mode` | `string` | `"json"` | 存储模式：`"json"` 或 `"sqlite"` |
| `memoryFile` | `string` | `"~/.unified-memory/memories.json"` | 记忆文件路径 |
| `vectorStore.backend` | `string` | `"lancedb"` | 向量后端：`"lancedb"` 或 `"chromadb"` |
| `vectorStore.path` | `string` | `"~/.unified-memory/vector.lance"` | 向量存储路径 |
| `vectorStore.dimension` | `number` | `768` | 嵌入向量维度 |

### 事务配置

```json
{
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true,
    "timeout": 30000
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `enable` | `boolean` | `true` | 启用原子事务 |
| `recoveryLog` | `string` | `"~/.unified-memory/transactions.log"` | WAL 日志路径 |
| `fsync` | `boolean` | `true` | 写入时 fsync |
| `timeout` | `number` | `30000` | 事务超时（毫秒） |

### 搜索配置

```json
{
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10,
    "minScore": 0.1
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `defaultMode` | `string` | `"hybrid"` | 默认搜索模式 |
| `bm25Weight` | `number` | `0.3` | 混合搜索中 BM25 权重 (0-1) |
| `vectorWeight` | `number` | `0.7` | 混合搜索中向量权重 (0-1) |
| `rrfK` | `number` | `60` | 排名融合的 RRF 常数 |
| `topK` | `number` | `10` | 默认结果数量 |
| `minScore` | `number` | `0.1` | 最小相关性分数 |

### 缓存配置

```json
{
  "cache": {
    "enable": true,
    "type": "semantic",
    "maxSize": 1000,
    "ttl": 3600,
    "evictionPolicy": "lru"
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `enable` | `boolean` | `true` | 启用缓存 |
| `type` | `string` | `"semantic"` | 缓存类型：`"semantic"` 或 `"exact"` |
| `maxSize` | `number` | `1000` | 最大缓存条目 |
| `ttl` | `number` | `3600` | 缓存 TTL（秒） |
| `evictionPolicy` | `string` | `"lru"` | 淘汰策略 |

### 嵌入配置

```json
{
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "url": "http://localhost:11434",
    "batchSize": 100,
    "dimension": 768
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `provider` | `string` | `"ollama"` | 嵌入提供商 |
| `model` | `string` | `"nomic-embed-text"` | 嵌入模型 |
| `url` | `string` | `"http://localhost:11434"` | 提供商 URL |
| `batchSize` | `number` | `100` | 嵌入批量大小 |
| `dimension` | `number` | `768` | 嵌入维度 |

### 层级配置

```json
{
  "tier": {
    "hot": {
      "maxAge": 7,
      "compression": false
    },
    "warm": {
      "minAge": 7,
      "maxAge": 30,
      "compression": "light"
    },
    "cold": {
      "minAge": 30,
      "compression": "heavy"
    }
  }
}
```

| 层级 | 年龄 | 压缩 | 描述 |
|------|------|------|------|
| HOT | ≤ 7 天 | 无 | 活跃记忆 |
| WARM | 7-30 天 | 轻度 | 不太活跃 |
| COLD | > 30 天 | 重度 | 归档 |

### 插件配置

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["sync-workspace"]
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `dir` | `string` | `"~/.unified-memory/plugins"` | 插件目录 |
| `autoReload` | `boolean` | `true` | 热重载插件 |
| `enabled` | `array` | `[]` | 启用的插件列表 |

## 🌐 环境变量

使用环境变量覆盖配置值：

```bash
# 存储
export UNIFIED_MEMORY_STORAGE_MODE=json
export UNIFIED_MEMORY_MEMORY_FILE=~/.unified-memory/memories.json

# 向量存储
export UNIFIED_MEMORY_VECTOR_BACKEND=lancedb
export UNIFIED_MEMORY_VECTOR_PATH=~/.unified-memory/vector.lance

# Ollama
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=nomic-embed-text

# 服务器
export UNIFIED_MEMORY_PORT=3851
export UNIFIED_MEMORY_HOST=0.0.0.0
```

## 📋 完整示例

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true
  },
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10
  },
  "cache": {
    "enable": true,
    "maxSize": 1000,
    "ttl": 3600
  },
  "embedding": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "url": "http://localhost:11434"
  },
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true
  }
}
```

## 🔍 验证配置

```bash
# 验证配置文件
unified-memory config:validate

# 显示当前配置
unified-memory config:show

# 生成默认配置
unified-memory config:init
```

## 🚨 配置错误

| 错误 | 解决方案 |
|------|----------|
| 无效的 JSON | 使用 `json_validate` 检查语法 |
| 未知键 | 删除或更正键 |
| 无效的值类型 | 确保类型与预期类型匹配 |
| 缺少必需项 | 添加必需的 配置 |

## 📚 下一步

- [快速入门教程](./quickstart.md) - 试用配置的 系统
- [基础使用指南](../guides/basic-usage.md) - 学习核心操作
- [高级使用](../guides/advanced-usage.md) - 高级功能
# 基础使用指南

> 学习核心操作：存储、搜索、列出和删除记忆。

## 📚 目录

1. [添加记忆](#-添加记忆)
2. [搜索记忆](#-搜索记忆)
3. [列出记忆](#-列出记忆)
4. [获取单个记忆](#-获取单个记忆)
5. [更新记忆](#-更新记忆)
6. [删除记忆](#-删除记忆)
7. [记忆元数据](#-记忆元数据)

## ➕ 添加记忆

### 基本添加
```javascript
const { addMemory } = require('unified-memory');

const memoryId = await addMemory({
  text: "Remember to call the client tomorrow"
});
```

### 完整选项
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

### 添加参数

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `text` | `string` | **必填** | 记忆内容 |
| `category` | `string` | `"general"` | 类别类型 |
| `importance` | `number` | `0.5` | 重要性 0-1 |
| `tags` | `array` | `[]` | 标签字符串数组 |
| `scope` | `string` | `null` | 范围：USER, AGENT, TEAM, GLOBAL |
| `source` | `string` | `"manual"` | 来源：manual, auto, extraction |
| `metadata` | `object` | `{}` | 自定义键值数据 |

### 记忆类别

| 类别 | 何时使用 |
|------|----------|
| `preference` | 用户偏好、喜好、厌恶 |
| `fact` | 关于世界的事实信息 |
| `decision` | 做出的决定，得到的结论 |
| `entity` | 人、组织、地点 |
| `reflection` | 想法、意见、洞察 |
| `general` | 其他记忆的默认类别 |

## 🔍 搜索记忆

### 简单搜索
```javascript
const { searchMemories } = require('unified-memory');

const results = await searchMemories("quarterly reports");
```

### 搜索选项
```javascript
const results = await searchMemories("project update", {
  mode: "hybrid",      // "hybrid", "bm25", 或 "vector"
  topK: 10,            // 结果数量
  vectorWeight: 0.7,    // 向量搜索权重 (0-1)
  bm25Weight: 0.3,     // BM25 搜索权重 (0-1)
  scope: "USER",       // 按范围过滤
  filters: {
    category: "fact",
    tags: ["work"],
    minImportance: 0.5
  }
});
```

### 搜索响应
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
    }
  ]
}
```

### 搜索模式

| 模式 | 描述 | 适用于 |
|------|------|--------|
| `hybrid` | BM25 + 向量 + RRF | 一般使用 |
| `bm25` | 仅关键词 | 精确匹配 |
| `vector` | 仅语义 | 概念匹配 |

## 📋 列出记忆

### 列出所有
```javascript
const { getAllMemories } = require('unified-memory');

const allMemories = await getAllMemories();
```

### 带过滤器的列表
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

## 🔎 获取单个记忆

```javascript
const { getMemory } = require('unified-memory');

const memory = await getMemory("mem_xxx");
```

## ✏️ 更新记忆

```javascript
const { updateMemory } = require('unified-memory');

await updateMemory("mem_xxx", {
  text: "Updated memory content"
});
```

## 🗑️ 删除记忆

```javascript
const { deleteMemory } = require('unified-memory');

await deleteMemory("mem_xxx");
```

## 🏷️ 记忆元数据

```javascript
await addMemory({
  text: "Meeting with John",
  metadata: {
    date: "2026-04-20",
    location: "Conference Room A",
    participants: ["John", "Alice"]
  }
});
```

## 📚 下一步

- [高级使用](./advanced-usage.md) - 版本控制、去重、导出
- [插件开发](./plugins.md) - 用插件扩展
- [API 参考](../api/overview.md) - 完整的 API 文档
# 用户指南

> 深入指南，有效使用 Unified Memory。

## 📋 本节指南

| 指南 | 描述 | 级别 |
|------|------|------|
| [基础使用](./basic-usage.md) | 核心操作：存储、搜索、列出、删除 | 初级 |
| [高级使用](./advanced-usage.md) | 版本控制、去重、导出、画像 | 中级 |
| [插件开发](./plugins.md) | 构建自定义插件 | 高级 |
| [集成](./integration.md) | 连接到其他系统 | 中级 |

## 🎯 选择您的路径

**初次接触 Unified Memory？**
从[基础使用](./basic-usage.md)开始，学习核心操作。

**想要扩展功能？**
了解[插件开发](./plugins.md)来构建自定义插件。

**需要与现有系统集成？**
查看[集成指南](./integration.md)获取连接器和 API。

## 📚 前置条件

阅读这些指南之前，您应该：
- 完成[快速入门教程](../getting-started/quickstart.md)
- 安装并运行 Unified Memory
- 了解基本的 JavaScript/TypeScript（用于 API 指南）

## 🔧 常见操作

### 存储记忆
```javascript
// 基本存储
await addMemory({ text: "重要笔记", tags: ["work"] });

// 带元数据
await addMemory({
  text: "下午3点开会",
  category: "fact",
  importance: 0.9,
  tags: ["meeting"],
  metadata: { participants: ["Alice", "Bob"] }
});
```

### 搜索记忆
```javascript
// 简单搜索
const results = await searchMemories("会议笔记");

// 混合搜索
const results = await searchMemories("项目更新", {
  mode: "hybrid",
  vectorWeight: 0.7,
  bm25Weight: 0.3
});
```

### 管理记忆
```javascript
// 列出所有
const all = await getAllMemories();

// 按 ID 获取
const memory = await getMemory(memoryId);

// 删除
await deleteMemory(memoryId);
```

## 🚀 快速链接

- [API 参考](../api/overview.md) - 完整的 API 文档
- [架构](../architecture/overview.md) - 系统设计
- [配置](../getting-started/configuration.md) - 配置选项
- [故障排除](../reference/troubleshooting.md) - 常见问题
# 插件开发指南

> 构建自定义插件以扩展 Unified Memory 功能。

## 🔌 插件概述

插件使用自定义功能扩展 Unified Memory：

| 插件类型 | 描述 |
|---------|------|
| **同步桥接** | 连接到外部记忆系统 |
| **处理器** | 存储前转换记忆 |
| **搜索引擎** | 添加自定义搜索算法 |
| **导出器** | 导出到外部格式 |

## 📁 插件结构

```
~/.unified-memory/plugins/
└── my-plugin/
    ├── index.js          # 主入口点
    ├── package.json      # 包配置
    └── README.md         # 文档
```

## ✏️ 创建插件

### 基本模板

```javascript
// index.js
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  hooks: {
    beforeStore: async (memory) => {
      memory.metadata = memory.metadata || {};
      memory.metadata.processedBy = 'my-plugin';
      return memory;
    },
    afterSearch: async (results) => {
      return results.filter(r => r.score > 0.5);
    }
  },

  tools: []
};
```

## 🪝 生命周期钩子

| 钩子 | 时机 | 目的 |
|------|------|------|
| `beforeStore` | 存储前 | 转换或验证 |
| `afterStore` | 存储后 | 触发副作用 |
| `beforeSearch` | 搜索前 | 修改查询 |
| `afterSearch` | 搜索后 | 过滤或重新排名 |
| `onInit` | 插件加载时 | 初始化资源 |
| `onShutdown` | 插件卸载时 | 清理资源 |

## 💡 插件示例

### 标签规范化器

```javascript
export const plugin = {
  name: 'tag-normalizer',
  version: '1.0.0',

  hooks: {
    beforeStore: async (memory) => {
      if (memory.tags) {
        memory.tags = [...new Set(
          memory.tags.map(t => t.toLowerCase().trim())
        )];
      }
      return memory;
    }
  }
};
```

### 外部同步桥接

```javascript
export const plugin = {
  name: 'external-sync',
  version: '1.0.0',

  async onInit(context) {
    this.externalApi = context.config.apiUrl;
  },

  hooks: {
    afterStore: async (memory) => {
      await fetch(`${this.externalApi}/memories`, {
        method: 'POST',
        body: JSON.stringify(memory)
      });
    }
  }
};
```

## ⚙️ 插件配置

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["tag-normalizer", "external-sync"],
    "external-sync": {
      "apiUrl": "https://api.example.com"
    }
  }
}
```

## 📚 下一步

- [集成指南](./integration.md) - 连接到其他系统
- [API 参考](../api/overview.md) - 完整的 API 文档
# 高级使用指南

> 高级功能：版本控制、去重、导出、画像等。

## 📚 目录

1. [版本控制](#-版本控制)
2. [去重](#-去重)
3. [导出与导入](#-导出与导入)
4. [记忆画像](#-记忆画像)
5. [偏好管理](#-偏好管理)
6. [层级管理](#-层级管理)

## 🔄 版本控制

### 列出版本
```javascript
const { memoryVersion } = require('unified-memory');

const versions = await memoryVersion({
  action: "list",
  memoryId: "mem_xxx",
  limit: 10
});
```

### 比较版本
```javascript
const diff = await memoryVersion({
  action: "diff",
  memoryId: "mem_xxx",
  versionId1: "v1",
  versionId2: "v2"
});
```

### 恢复版本
```javascript
await memoryVersion({
  action: "restore",
  memoryId: "mem_xxx",
  versionId: "v1"
});
```

## 🔀 去重

### 查找重复（试运行）
```javascript
const { memoryDedup } = require('unified-memory');

const duplicates = await memoryDedup({
  threshold: 0.85,
  dryRun: true
});
```

### 合并重复
```javascript
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: false
});
```

## 📤 导出

```javascript
const { memoryExport } = require('unified-memory');

// 导出为 JSON
await memoryExport({
  format: "json",
  output: "~/exports/memories.json"
});

// 导出为 Markdown
await memoryExport({
  format: "markdown",
  output: "~/exports/memories.md"
});

// 导出为 CSV
await memoryExport({
  format: "csv",
  output: "~/exports/memories.csv"
});
```

## 👤 记忆画像

```javascript
const { memoryProfile } = require('unified-memory');

const profile = await memoryProfile({
  scope: "user",
  container_tag: "project-x",
  static_days: 30,
  limit: 100
});
```

## ❤️ 偏好管理

### 获取偏好
```javascript
const pref = await memoryPreference({
  action: "get",
  key: "meeting_preference"
});
```

### 设置偏好
```javascript
await memoryPreference({
  action: "set",
  key: "preferred_language",
  value: "Python",
  confidence: 0.9
});
```

### 合并偏好
```javascript
await memoryPreference({
  action: "merge",
  slots: {
    language: { value: "TypeScript", confidence: 0.9 },
    editor: { value: "VS Code", confidence: 0.95 }
  }
});
```

## 📊 层级管理

### 检查层级状态
```javascript
const status = await memoryTier({ action: "status" });
```

### 迁移到层级
```javascript
await memoryTier({
  action: "migrate",
  memories: [{ id: "mem_xxx", targetTier: "COLD" }],
  apply: true
});
```

### 层级阈值

| 层级 | 年龄 | 压缩 | 可去重 |
|------|------|------|--------|
| HOT | ≤ 7 天 | 无 | 是 |
| WARM | 7-30 天 | 轻度 | 是 |
| COLD | > 30 天 | 重度 | 是 |

## 📚 下一步

- [插件开发](./plugins.md) - 构建自定义插件
- [集成指南](./integration.md) - 连接到其他系统
- [API 参考](../api/overview.md) - 完整的 API 文档
# 集成指南

> 将 Unified Memory 连接到其他系统和应用程序。

## 🔌 MCP 集成

MCP（模型上下文协议）集成用于 AI 助手。

### MCP 工具

| 工具 | 描述 |
|------|------|
| `memory_search` | 混合搜索记忆 |
| `memory_store` | 存储新记忆 |
| `memory_list` | 列出所有记忆 |
| `memory_delete` | 按 ID 删除记忆 |
| `memory_stats` | 获取记忆统计 |
| `memory_health` | 健康检查 |

### MCP 配置

```json
{
  "mcpServers": {
    "unified-memory": {
      "command": "npx",
      "args": ["-y", "unified-memory", "serve"]
    }
  }
}
```

## 🌐 REST API

启动 REST API 服务器：

```bash
unified-memory serve --port 3851
```

### 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/memories/search` | 搜索记忆 |
| GET | `/api/memories` | 列出记忆 |
| GET | `/api/memories/:id` | 获取单个记忆 |
| POST | `/api/memories` | 存储记忆 |
| DELETE | `/api/memories/:id` | 删除记忆 |

## 📦 JavaScript SDK

```javascript
import { 
  addMemory, 
  searchMemories, 
  getAllMemories 
} from 'unified-memory';

// 存储
const id = await addMemory({
  text: "User preference for Python",
  category: "preference"
});

// 搜索
const results = await searchMemories("Python preference");

// 列出
const all = await getAllMemories();
```

## 💻 CLI 集成

```bash
# 添加记忆
unified-memory add "Remember to check reports" --tags work

# 搜索
unified-memory search "reports"

# 列出
unified-memory list
```

## 📚 下一步

- [API 参考](../api/overview.md) - 完整的 API 文档
- [插件开发](./plugins.md) - 构建自定义插件
# 贡献指南

> 欢迎为 Unified Memory 项目做出贡献！

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境](#开发环境)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试规范](#测试规范)
- [文档规范](#文档规范)
- [发布流程](#发布流程)
- [社区角色](#社区角色)
- [获取帮助](#获取帮助)

## 行为准则

### 我们的承诺

为了营造开放、友好的环境，我们作为贡献者和维护者承诺：无论年龄、体型、身体健全与否、民族、性征、性别认同与表达、经验水平、教育程度、社会地位、国籍、相貌、种族、信仰、性取向，我们项目和社区的参与者都免于骚扰。

### 我们的准则

有助于创造积极环境的行为包括但不限于：

- 使用友好和包容性语言
- 尊重不同的观点和经历
- 耐心接受有益批评
- 关注对社区最有利的事情
- 友善对待其他社区成员

不可接受的行为包括但不限于：

- 使用与性有关的言语或图像，以及不受欢迎的性关注
- 捣乱、侮辱或贬损的评论，以及人身或政治攻击
- 公开或私下的骚扰
- 未经明确许可，发布他人的私人信息
- 其他有理由认定为违反职业操守的不当行为

### 我们的责任

项目维护者有责任诠释何谓“不可接受的行为”，并妥善、公平地纠正一切不可接受的行为。

项目维护者有权利和责任去删除、编辑、拒绝违背本行为准则的评论、提交、代码、wiki编辑、问题等，以及暂时或永久地封禁任何他们认为行为不当、威胁、冒犯、有害的贡献者。

### 适用范围

本行为准则适用于本项目所有平台，以及当个人代表本项目或本社区出席的公共场合。代表本项目或本社区的场合包括但不限于：使用官方电子邮件地址、通过官方社交媒体账号发布消息、作为指定代表参与在线或线下活动。

### 执行

如遇滥用、骚扰或其他不可接受的行为，请通过 [team@openclaw.ai](mailto:team@openclaw.ai) 联系项目团队。所有投诉都将得到及时、公正的处理。

项目团队有义务保密举报者信息。

## 如何贡献

### 贡献类型

#### 1. 报告错误
- 使用 GitHub Issues 报告错误
- 提供详细的重现步骤
- 包括环境信息
- 如果可能，提供修复建议

#### 2. 功能建议
- 使用 GitHub Issues 提出功能建议
- 描述功能的使用场景
- 如果可能，提供实现思路
- 讨论功能优先级

#### 3. 代码贡献
- Fork 仓库
- 创建功能分支
- 编写代码和测试
- 提交 Pull Request
- 参与代码审查

#### 4. 文档改进
- 修复拼写错误
- 改进文档结构
- 添加使用示例
- 翻译文档

#### 5. 社区帮助
- 回答 Issues 中的问题
- 帮助审查 Pull Requests
- 参与社区讨论
- 分享使用经验

### 贡献流程

1. **寻找任务**
   - 查看 [Good First Issues](https://github.com/mouxangithub/unified-memory/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
   - 查看 [Help Wanted](https://github.com/mouxangithub/unified-memory/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
   - 查看项目路线图

2. **讨论方案**
   - 在 Issue 中讨论实现方案
   - 确认技术细节
   - 获取维护者反馈

3. **开始开发**
   - Fork 仓库
   - 创建功能分支
   - 设置开发环境

4. **编写代码**
   - 遵循代码规范
   - 编写测试用例
   - 更新文档

5. **提交更改**
   - 遵循提交规范
   - 确保测试通过
   - 更新相关文档

6. **创建 Pull Request**
   - 描述更改内容
   - 链接相关 Issue
   - 等待代码审查

7. **代码审查**
   - 根据反馈修改
   - 保持积极沟通
   - 感谢审查者

8. **合并发布**
   - 维护者合并代码
   - 更新版本号
   - 发布新版本

## 开发环境

### 环境要求

- Node.js >= 18.0.0
- npm >= 8.0.0
- Git
- 文本编辑器（推荐 VS Code）

### 设置步骤

1. **Fork 仓库**
   ```bash
   # 访问 https://github.com/mouxangithub/unified-memory
   # 点击 "Fork" 按钮
   ```

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/unified-memory.git
   cd unified-memory
   ```

3. **添加上游仓库**
   ```bash
   git remote add upstream https://github.com/mouxangithub/unified-memory.git
   ```

4. **安装依赖**
   ```bash
   npm install
   ```

5. **设置开发环境**
   ```bash
   npm run setup:dev
   ```

6. **启动开发服务器**
   ```bash
   npm run dev
   ```

### 开发脚本

```bash
# 开发
npm run dev          # 启动开发服务器
npm run watch        # 监视模式

# 测试
npm test             # 运行所有测试
npm run test:unit    # 运行单元测试
npm run test:integration # 运行集成测试
npm run test:watch   # 监视测试模式

# 代码质量
npm run lint         # 代码检查
npm run format       # 代码格式化
npm run type-check   # 类型检查

# 构建
npm run build        # 生产构建
npm run clean        # 清理构建产物

# 文档
npm run docs:build   # 构建文档
npm run docs:serve   # 本地文档服务器
```

## 代码规范

### 语言规范

- **JavaScript**: 使用 ES6+ 语法
- **TypeScript**: 推荐使用 TypeScript
- **JSON**: 使用 2 空格缩进
- **Markdown**: 遵循 CommonMark 规范

### 命名规范

#### 变量和函数
```javascript
// 正确
const userName = '张三';
function calculateTotalPrice() { }

// 错误
const UserName = '张三';
function CalculateTotalPrice() { }
```

#### 类和构造函数
```javascript
// 正确
class UserService { }
function DatabaseConnection() { }

// 错误
class userService { }
function databaseConnection() { }
```

#### 常量和枚举
```javascript
// 正确
const MAX_RETRY_COUNT = 3;
const API_ENDPOINTS = {
  USERS: '/api/users',
  POSTS: '/api/posts'
};

// 错误
const maxRetryCount = 3;
const apiEndpoints = { ... };
```

### 代码风格

#### 缩进和空格
```javascript
// 正确：2 空格缩进
function example() {
  if (condition) {
    doSomething();
  }
}

// 错误：4 空格或制表符
function example() {
    if (condition) {
        doSomething();
    }
}
```

#### 分号
```javascript
// 正确：使用分号
const name = '张三';
function sayHello() {
  console.log('你好');
}

// 错误：省略分号
const name = '张三'
function sayHello() {
  console.log('你好')
}
```

#### 引号
```javascript
// 正确：使用单引号
const message = 'Hello World';
const template = `Hello ${name}`;

// 错误：使用双引号
const message = "Hello World";
```

### 注释规范

#### 文件头注释
```javascript
/**
 * @fileoverview 用户服务模块
 * @module services/user
 * @author 张三 <zhangsan@example.com>
 * @version 1.0.0
 * @license MIT
 */
```

#### 函数注释
```javascript
/**
 * 计算用户年龄
 * @param {Date} birthDate - 出生日期
 * @param {Date} [referenceDate=new Date()] - 参考日期，默认为当前日期
 * @returns {number} 年龄（整数）
 * @throws {Error} 如果出生日期无效
 * @example
 * const age = calculateAge(new Date('1990-01-01'));
 * console.log(age); // 34
 */
function calculateAge(birthDate, referenceDate = new Date()) {
  // 实现代码
}
```

#### 行内注释
```javascript
// 正确：解释复杂逻辑
const result = data.filter(item => {
  // 过滤掉已删除的项目
  return !item.deleted;
});

// 错误：重复明显信息
const name = '张三'; // 设置姓名为张三
```

## 提交规范

### 提交消息格式

```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

#### 类型
- `feat`: 新功能
- `fix`: 修复错误
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变更

#### 范围
- `api`: API 相关
- `ui`: 用户界面
- `db`: 数据库
- `auth`: 认证授权
- `search`: 搜索功能
- `cache`: 缓存系统
- `docs`: 文档

#### 示例
```
feat(search): 添加混合搜索功能

- 实现 BM25 搜索算法
- 集成向量搜索
- 添加 RRF 结果融合
- 更新搜索 API 文档

Closes #123
```

### 提交频率

- 每个提交应该是一个完整的功能单元
- 避免提交未完成的代码
- 及时提交，避免大量更改一次性提交
- 使用 `git rebase` 整理提交历史

### 分支管理

#### 分支命名
```
# 功能分支
feat/user-authentication
feat/search-optimization

# 修复分支
fix/login-bug
fix/memory-leak

# 发布分支
release/v1.2.0
hotfix/v1.2.1
```

#### 分支策略
```bash
# 从主分支创建功能分支
git checkout main
git pull upstream main
git checkout -b feat/your-feature

# 开发完成后
git add .
git commit -m "feat(your-feature): 描述功能"
git push origin feat/your-feature

# 创建 Pull Request
```

## 测试规范

### 测试类型

#### 单元测试
```javascript
// 测试单个函数或模块
describe('calculateAge', () => {
  it('应该正确计算年龄', () => {
    const birthDate = new Date('1990-01-01');
    const referenceDate = new Date('2024-01-01');
    const age = calculateAge(birthDate, referenceDate);
    expect(age).toBe(34);
  });
});
```

#### 集成测试
```javascript
// 测试模块间集成
describe('UserService', () => {
  it('应该创建用户并保存到数据库', async () => {
    const user = await userService.createUser({ name: '张三' });
    const savedUser = await database.findUser(user.id);
    expect(savedUser.name).toBe('张三');
  });
});
```

#### 端到端测试
```javascript
// 测试完整流程
describe('用户注册流程', () => {
  it('应该完成用户注册', async () => {
    await page.goto('/register');
    await page.fill('#name', '张三');
    await page.fill('#email', 'zhangsan@example.com');
    await page.click('#submit');
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### 测试覆盖率

- 目标覆盖率：80% 以上
- 关键功能：100% 覆盖率
- 使用 `npm run test:coverage` 生成报告

### 测试最佳实践

1. **测试独立性**: 每个测试应该独立运行
2. **确定性测试**: 测试结果应该可预测
3. **快速反馈**: 测试应该快速运行
4. **清晰断言**: 断言应该清晰表达预期
5. **模拟外部依赖**: 使用模拟对象测试外部依赖

## 文档规范

### 文档结构

```
docs/
├── en/                    # 英文文档
│   ├── getting-started/  # 入门指南
│   ├── guides/           # 使用指南
│   ├── api/              # API 参考
│   ├── architecture/     # 架构文档
│   └── contributing/     # 贡献指南
├── zh/                    # 中文文档
│   └── ...               # 相同结构
└── shared/               # 共享资源
```

### 文档格式

#### Markdown 规范
```markdown
# 一级标题

## 二级标题

### 三级标题

正文内容...

- 列表项1
- 列表项2

1. 有序列表1
2. 有序列表2

**粗体文本**
*斜体文本*

`代码片段`

```javascript
// 代码块
const example = '代码示例';
```

[链接文本](https://example.com)

![图片描述](image.png)
```

#### 中文文档规范
- 使用简体中文
- 专业术语保持英文
- 代码示例使用英文注释
- 保持中英文文档同步更新

### 文档更新

1. **代码变更时更新文档**
2. **API 变更时更新 API 文档**
3. **新功能时添加使用指南**
4. **定期检查文档准确性**

## 发布流程

### 版本规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 发布步骤

1. **准备发布**
   ```bash
   # 更新版本号
   npm version patch  # 或 minor, major
   
   # 更新 CHANGELOG.md
   # 更新文档
   ```

2. **创建发布分支**
   ```bash
   git checkout -b release/v1.2.0
   git push origin release/v1.2.0
   ```

3. **测试发布版本**
   ```bash
   npm run build
   npm test
   npm run integration-test
   ```

4. **创建 Pull Request**
   - 描述发布内容
   - 链接相关 Issues
   - 等待代码审查

5. **合并发布**
   ```bash
   git checkout main
   git merge release/v1.2.0
   git tag v1.2.0
   git push origin main --tags
   ```

6. **发布到 npm**
   ```bash
   npm publish
   ```

7. **更新文档网站**
   ```bash
   npm run docs:deploy
   ```

### 发布检查清单

- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档更新完成
- [ ] CHANGELOG 更新
- [ ] 版本号更新
- [ ] 构建产物检查
- [ ] 发布公告准备

## 社区角色

### 贡献者级别

#### 1. 首次贡献者
- 修复拼写错误
- 添加测试用例
- 报告错误
- 参与讨论

#### 2. 常规贡献者
- 实现小型功能
- 修复中等复杂度错误
- 改进文档
- 帮助审查代码

#### 3. 核心贡献者
- 实现主要功能
- 架构改进
- 指导新贡献者
- 参与路线图规划

#### 4. 维护者
- 代码审查
- 版本发布
- 社区管理
- 项目决策

### 权限和责任

| 角色 | 权限 | 责任 |
|------|------|------|
| 首次贡献者 | 提交 Issues, 参与讨论 | 遵守行为准则 |
| 常规贡献者 | 提交 Pull Requests | 代码质量, 测试覆盖 |
| 核心贡献者 | 合并 Pull Requests | 架构设计, 代码审查 |
| 维护者 | 发布版本, 管理仓库 | 项目方向, 社区管理 |

## 获取帮助

### 沟通渠道

#### GitHub Issues
- **功能建议**: 使用 `enhancement` 标签
- **错误报告**: 使用 `bug` 标签
- **问题咨询**: 使用 `question` 标签

#### GitHub Discussions
- **使用问题**: 在 Q&A 板块提问
- **功能讨论**: 在 Ideas 板块讨论
- **社区交流**: 在 General 板块交流

#### 电子邮件
- **安全问题**: security@openclaw.ai
- **合作咨询**: partnership@openclaw.ai
- **一般问题**: team@openclaw.ai

### 学习资源

#### 官方文档
- [入门指南](../getting-started/quickstart.md)
- [API 参考](../api/overview.md)
- [架构文档](../architecture/overview.md)

#### 外部资源
- [OpenClaw 文档](https://docs.openclaw.ai)
- [Node.js 文档](https://nodejs.org/docs)
- [GitHub 指南](https://docs.github.com)

### 社区活动

#### 定期会议
- **社区会议**: 每月第一个周二
- **技术分享**: 每月第三个周四
- **代码审查**: 每周三下午

#### 线上交流
- **Discord**: [OpenClaw Community](https://discord.gg/openclaw)
- **Twitter**: [@OpenClawAI](https://twitter.com/OpenClawAI)
- **博客**: [OpenClaw Blog](https://blog.openclaw.ai)

## 致谢

感谢所有为 Unified Memory 项目做出贡献的开发者！您的贡献让这个项目变得更好。

特别感谢：

- **OpenClaw 团队**: 提供平台和支持
- **核心贡献者**: 持续的代码贡献
- **文档贡献者**: 完善的中英文文档
- **测试贡献者**: 确保代码质量
- **社区成员**: 反馈和建议

让我们共同努力，打造更好的记忆管理系统！# Unified Memory 中文文档

[English](../en/index.md) · **中文**

欢迎来到 Unified Memory v5.2.0 中文文档。本文档提供 Unified Memory 系统的全面指南、API 参考和架构详情。

## 📚 文档结构

### 快速开始
- **[快速开始指南](./getting-started/quickstart.md)** - 5分钟上手
- **[安装指南](./getting-started/installation.md)** - 详细安装说明
- **[配置指南](./getting-started/configuration.md)** - 系统配置选项

### 使用指南
- **[基础使用](./guides/basic-usage.md)** - 日常操作和常见任务
- **[高级功能](./guides/advanced-features.md)** - 高级功能和优化
- **[插件系统](./guides/plugins.md)** - 使用插件扩展功能
- **[故障排除](./guides/troubleshooting.md)** - 解决常见问题

### API 文档
- **[API 概览](./api/overview.md)** - Unified Memory API 介绍
- **[存储 API](./api/storage-api.md)** - 记忆存储和检索操作
- **[向量 API](./api/vector-api.md)** - 向量搜索和相似度操作
- **[插件 API](./api/plugin-api.md)** - 插件开发和集成

### 架构设计
- **[架构概览](./architecture/overview.md)** - 系统设计和组件
- **[原子事务](./architecture/atomic-transactions.md)** - 数据一致性保证
- **[向量搜索](./architecture/vector-search.md)** - 搜索算法和优化
- **[插件系统](./architecture/plugin-system.md)** - 插件架构和设计

### 参考手册
- **[CLI 参考](./reference/cli-reference.md)** - 命令行接口文档
- **[配置参考](./reference/configuration.md)** - 完整配置选项
- **[更新日志](./reference/changelog.md)** - 版本历史和变更
- **[常见问题](./reference/faq.md)** - 常见问题解答
- **[贡献指南](./reference/contributing.md)** - 如何贡献项目

## 🎯 核心特性文档

### 原子数据一致性
- **两阶段提交协议**: 保证 JSON 和向量存储的原子性写入
- **事务恢复**: 自动恢复未完成的事务
- **fsync 保证**: 确保数据写入磁盘

### 高性能搜索
- **混合搜索**: BM25 + 向量 + RRF 融合获得最佳结果
- **优化算法**: 5-10倍查询性能提升
- **智能缓存**: 频繁查询的结果缓存

### 插件系统
- **同步桥梁**: 与 Workspace Memory 同步
- **统一查询**: 跨系统搜索接口
- **健康监控**: 实时系统监控

## 🔧 开发资源

### 代码示例


### 测试


### 构建


## 📖 阅读顺序

### 新用户
1. 从 **[快速开始指南](./getting-started/quickstart.md)** 开始
2. 阅读 **[基础使用](./guides/basic-usage.md)** 了解日常任务
3. 根据需要探索 **[高级功能](./guides/advanced-features.md)**

### 开发者
1. 查看 **[架构概览](./architecture/overview.md)**
2. 学习 **[原子事务](./architecture/atomic-transactions.md)** 了解数据一致性
3. 查阅 **[API 文档](./api/overview.md)** 进行集成

### 贡献者
1. 阅读 **[贡献指南](./reference/contributing.md)**
2. 理解 **[架构](./architecture/overview.md)**
3. 查看现有 **[代码示例](../shared/examples/)**

## 🔗 相关资源

### 外部链接
- **[GitHub 仓库](https://github.com/mouxangithub/unified-memory)** - 源代码和问题
- **[npm 包](https://www.npmjs.com/package/unified-memory)** - 包分发
- **[ClawHub 技能](https://clawhub.ai/)** - 技能市场

### 社区
- **[GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)** - 社区讨论
- **[问题跟踪器](https://github.com/mouxangithub/unified-memory/issues)** - bug 报告和功能请求
- **[贡献指南](./reference/contributing.md)** - 如何贡献

## 📄 许可证

本文档是 Unified Memory 项目的一部分，采用 MIT 许可证。详见 [LICENSE](https://github.com/mouxangithub/unified-memory/blob/main/LICENSE) 文件。

## 🤝 贡献文档

我们欢迎贡献来改进本文档！请查看我们的 [贡献指南](./reference/contributing.md) 了解如何：

1. 报告文档问题
2. 提出改进建议
3. 提交文档更新
4. 翻译文档

## 📞 支持

- **文档问题**: 在 [GitHub](https://github.com/mouxangithub/unified-memory/issues) 上提出问题
- **问题**: 使用 [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)
- **Bug**: 通过 [问题跟踪器](https://github.com/mouxangithub/unified-memory/issues) 报告

---

**最后更新**: 2026-04-15  
**版本**: v5.2.0  
**文档版本**: 1.0.0  

[← 返回主文档](../README_CN.md)
# MCP 工具 API 参考

> Unified Memory 所有 MCP 工具的完整参考。基于 `src/index.js` v1.1.0。

## 目录

- [核心工具](#核心工具) — Search、Store、List、Delete
- [Prompt 组合](#prompt-组合) — memory_compose
- [v4.0 存储网关](#v40-存储网关) — memory_v4_*
- [高级工具](#高级工具) — Export、Dedup、Decay、QA
- [偏好与画像](#偏好与画像) — memory_preference、memory_profile
- [版本控制](#版本控制) — memory_version
- [搜索引擎](#搜索引擎) — memory_engine、memory_qmd
- [分层管理](#分层管理) — memory_tier
- [系统工具](#系统工具) — Stats、Health、Metrics、WAL

---

## 核心工具

### memory_search

使用 BM25 + 向量 + RRF 融合的混合搜索。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `query` | `string` | *必填* | 搜索查询文本 |
| `topK` | `number` | `5` | 返回结果数量 |
| `mode` | `"hybrid" \| "bm25" \| "vector"` | `"hybrid"` | 搜索模式 |
| `scope` | `string` | `null` | 范围过滤：`AGENT`、`USER`、`TEAM`、`GLOBAL` |

**示例：**
```json
{
  "query": "用户偏好的编程语言",
  "topK": 5,
  "mode": "hybrid",
  "scope": "USER"
}
```

**返回：**
```json
{
  "count": 3,
  "query": "用户偏好的编程语言",
  "mode": "hybrid",
  "results": [
    {
      "id": "mem_xxx",
      "text": "用户偏好用 Python 做数据工作",
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

存储新记忆。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `text` | `string` | *必填* | 记忆内容 |
| `category` | `string` | `"general"` | 类别：`preference`、`fact`、`decision`、`entity`、`reflection` |
| `importance` | `number` | `0.5` | 重要性评分 0–1 |
| `tags` | `string[]` | `[]` | 标签 |
| `scope` | `string` | `null` | 范围：`AGENT`、`USER`、`TEAM`、`GLOBAL` |
| `source` | `string` | `"manual"` | 来源：`manual`、`auto`、`extraction` |

**自动抽取：** 当 `category="general"` 且 `importance > 0.7` 时，自动抽取结构化事实。

---

### memory_list

列出所有已存储的记忆及其元数据。

**参数：** 无

---

### memory_delete

根据 ID 删除记忆。已写入 WAL 和 transcript 日志。

**参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| `id` | `string` | 要删除的记忆 ID |

---

## Prompt 组合

### memory_compose

为 prompt 注入组合记忆上下文块。

**参数：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `messages` | `object[]` | `[]` | 对话消息 `{role, content}` |
| `targetTokens` | `number` | `2000` | 目标 token 预算 |
| `categories` | `string[]` | `[]` | 按类别过滤 |
| `query` | `string` | `null` | 偏置记忆选择的搜索查询 |
| `messageWindow` | `number` | `10` | 包含的最近消息数 |

**优先级顺序：** PIN → HOT → WARM → COLD

---

## 高级工具

### memory_export

导出记忆为 JSON、Markdown 或 CSV 格式。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `format` | `"json" \| "markdown" \| "csv"` | `"json"` | 导出格式 |
| `output` | `string` | `null` | 输出文件路径 |
| `category` | `string` | `null` | 按类别过滤 |
| `minImportance` | `number` | `null` | 最低重要性阈值 |

---

### memory_dedup

检测并合并重复记忆。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `threshold` | `number` | `0.85` | 相似度阈值 0–1 |
| `dryRun` | `boolean` | `true` | 为 true 时仅预览 |

---

### memory_qa

基于相关记忆回答问题（RAG）。

| 参数 | 类型 | 描述 |
|------|------|------|
| `question` | `string` | 要回答的问题 |

---

### memory_profile

获取具有静态/动态分离的用户画像。

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `scope` | `string` | `"user"` | 范围：`agent`、`user`、`team`、`global` |
| `container_tag` | `string` | `null` | 项目/泳道标签 |
| `entity_filter` | `string` | `null` | 聚焦特定实体 |
| `static_days` | `number` | `30` | 天数无访问则标记为静态 |
| `limit` | `number` | `100` | 最大分析记忆数 |

---

## 偏好与画像

### memory_preference

统一偏好管理。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `get`、`set`、`update`、`merge`、`delete`、`reset`、`stats`、`explain`、`infer` |
| `key` | `string` | 槽位键（用于 get/set/update/delete/explain） |
| `value` | `any` | 槽位值（用于 set/update） |
| `confidence` | `number` | 置信度 0–1 |
| `source` | `string` | `explicit`、`inferred`、`historical` |
| `slots` | `object` | 键值映射（用于 merge） |
| `messageCount` | `number` | `20` — infer 用消息数 |

---

## 版本控制

### memory_version

记忆版本控制。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `list`、`diff`、`restore` |
| `memoryId` | `string` | 记忆 ID（用于 diff/restore） |
| `versionId` | `string` | 版本 ID（用于 diff/restore） |
| `versionId1` | `string` | 第一个版本（用于 diff） |
| `versionId2` | `string` | 第二个版本（用于 diff） |
| `limit` | `number` | `10` — 最大版本数（用于 list） |
| `preview` | `boolean` | `false` — 不还原仅预览 |

---

## 搜索引擎

### memory_engine

统一搜索引擎。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `bm25`、`embed`、`search`、`mmr`、`rerank`、`qmd` |
| `query` | `string` | 查询字符串 |
| `text` | `string` | 要嵌入的文本 |
| `documents` | `object[]` | 用于 mmr/rerank 的文档 |
| `topK` | `number` | `10` — 结果数量 |
| `build` | `boolean` | `false` — 重建 BM25 索引 |
| `lambda` | `number` | `0.5` — MMR 平衡参数 |
| `method` | `enum` | `keyword`、`llm`、`cross`（用于 rerank） |

### memory_qmd

QMD 本地文件搜索。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `search`、`get`、`vsearch`、`list`、`status` |
| `query` | `string` | 搜索查询 |
| `path` | `string` | 文件路径（用于 get） |
| `mode` | `enum` | `bm25`、`vector`、`hybrid`、`auto` |

---

## 分层管理

### memory_tier

HOT/WARM/COLD 分层管理。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `status`、`migrate`、`compress`、`assign`、`partition`、`redistribute` |
| `apply` | `boolean` | `false` — 应用更改 |
| `memories` | `object[]` | 记忆（用于 assign/partition/compress） |

**分层阈值：**
- HOT：≤ 7 天
- WARM：7–30 天
- COLD：> 30 天

---

## 系统工具

### memory_stats

记忆系统统计。

**参数：** 无

返回：总数、分类、标签、分层分布、范围分布、质量分布。

---

### memory_health

MCP 服务器和依赖的健康检查。

**参数：** 无

返回：Ollama 状态、WAL 完整性、向量缓存完整率、分层分布、陈旧记忆。

---

### memory_metrics

操作指标：搜索延迟、存储计数、错误率。

**参数：** 无

---

### memory_wal

预写日志操作。

| 参数 | 类型 | 描述 |
|------|------|------|
| `action` | `enum` | `init`、`flush`、`list` |
| `runId` | `string` | 运行 ID（用于 init） |

---

### memory_pin / memory_unpin / memory_pins

固定（锁定）记忆，使其永不压缩或去重。

---

## v4.0 存储网关

完整 `memory_v4_*` 工具文档请参见 [v4 API 参考](./v4.md)。

---

## 错误响应

所有工具在出错时返回带 `isError: true` 的错误响应：

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```
# API 参考概述

> Unified Memory API 和 MCP 工具的完整参考。

## 🚀 快速参考

### 核心函数

```javascript
// 记忆操作
addMemory(memory)         // 存储新记忆
getMemory(id)            // 按 ID 获取
getAllMemories(options)  // 带过滤器的列表
updateMemory(id, updates) // 更新字段
deleteMemory(id)          // 删除记忆

// 搜索
searchMemories(query, options)  // 混合搜索
getMemoryStats()                // 统计

// 事务
beginTransaction()      // 开始事务
commitTransaction(tx)   // 提交更改
rollbackTransaction(tx) // 回滚更改
```

## 🔧 MCP 工具快速索引

| 工具 | 描述 |
|------|------|
| `memory_search` | 混合搜索 |
| `memory_store` | 存储记忆 |
| `memory_list` | 列出记忆 |
| `memory_delete` | 删除记忆 |
| `memory_compose` | 组合提示上下文 |
| `memory_profile` | 用户画像 |
| `memory_preference` | 偏好 |
| `memory_version` | 版本控制 |
| `memory_export` | 导出记忆 |
| `memory_dedup` | 去重 |
| `memory_tier` | 层级管理 |
| `memory_pin` | 固定/取消固定 |
| `memory_stats` | 统计 |
| `memory_health` | 健康检查 |
| `memory_metrics` | 指标 |

## 📚 下一步

- [MCP 工具参考](./mcp-tools.md) - 所有工具参数
- [核心 API 参考](./core-api.md) - SDK 函数
- [插件 API 参考](./plugin-api.md) - 插件钩子
# MCP 工具参考

> 所有 Unified Memory MCP 工具的完整参考。

## 核心工具

### memory_search

使用 BM25 + 向量 + RRF 融合的混合搜索。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `query` | `string` | *必填* | 搜索查询文本 |
| `topK` | `number` | `5` | 返回结果数量 |
| `mode` | `string` | `"hybrid"` | 搜索模式：`"hybrid"`, `"bm25"`, `"vector"` |
| `scope` | `string` | `null` | 范围过滤：`"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `vectorWeight` | `number` | `0.7` | 混合中向量权重 (0-1) |
| `bm25Weight` | `number` | `0.3` | 混合中 BM25 权重 (0-1) |
| `filters` | `object` | `null` | 元数据过滤器 |

**示例：**
```json
{
  "query": "用户偏好的编程语言",
  "topK": 5,
  "mode": "hybrid",
  "scope": "USER"
}
```

---

### memory_store

存储新记忆。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `text` | `string` | *必填* | 记忆内容 |
| `category` | `string` | `"general"` | 类别：`"preference"`, `"fact"`, `"decision"`, `"entity"`, `"reflection"` |
| `importance` | `number` | `0.5` | 重要性评分 0-1 |
| `tags` | `string[]` | `[]` | 记忆的标签 |
| `scope` | `string` | `null` | 范围：`"AGENT"`, `"USER"`, `"TEAM"`, `"GLOBAL"` |
| `source` | `string` | `"manual"` | 来源：`"manual"`, `"auto"`, `"extraction"` |
| `metadata` | `object` | `{}` | 自定义元数据 |

---

### memory_list

列出所有已存储的记忆及其元数据。

**参数：** 无

---

### memory_delete

根据 ID 删除记忆。已写入 WAL 和 transcript 日志。

**参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| `id` | `string` | 要删除的记忆 ID |

---

## 提示组合

### memory_compose

为提示注入组合记忆上下文块。

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `messages` | `object[]` | `[]` | 对话消息 `{role, content}` |
| `targetTokens` | `number` | `2000` | 目标 token 预算 |
| `categories` | `string[]` | `[]` | 按类别过滤 |
| `query` | `string` | `null` | 搜索查询以偏置选择 |
| `messageWindow` | `number` | `10` | 包含的最近消息数 |

**优先级顺序：** PIN → HOT → WARM → COLD

---

## 高级工具

### memory_export

导出记忆为 JSON、Markdown 或 CSV 格式。

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `format` | `string` | `"json"` | 导出格式：`"json"`, `"markdown"`, `"csv"` |
| `output` | `string` | `null` | 输出文件路径 |
| `category` | `string` | `null` | 按类别过滤 |
| `minImportance` | `number` | `null` | 最低重要性阈值 |

---

### memory_dedup

检测并合并重复记忆。

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `threshold` | `number` | `0.85` | 相似度阈值 0-1 |
| `dryRun` | `boolean` | `true` | 为 true 时仅预览 |

---

### memory_profile

获取具有静态/动态分离的用户画像。

| 参数 | 类型 | 默认 | 描述 |
|------|------|---------|-------------|
| `scope` | `string` | `"user"` | 范围：`"agent"`, `"user"`, `"team"`, `"global"` |
| `container_tag` | `string` | `null` | 项目/泳道标签 |
| `static_days` | `number` | `30` | 天数无访问则标记为静态 |
| `limit` | `number` | `100` | 最大分析记忆数 |

---

### memory_preference

统一偏好管理。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"get"`, `"set"`, `"update"`, `"merge"`, `"delete"`, `"reset"`, `"stats"`, `"explain"`, `"infer"` |
| `key` | `string` | 槽位键 |
| `value` | `any` | 槽位值 |
| `confidence` | `number` | 置信度 0-1 |
| `source` | `string` | `"explicit"`, `"inferred"`, `"historical"` |
| `slots` | `object` | 键值映射（用于 merge） |

---

## 版本控制

### memory_version

记忆版本控制。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"list"`, `"diff"`, `"restore"` |
| `memoryId` | `string` | 记忆 ID |
| `versionId` | `string` | 版本 ID |
| `limit` | `number` | `10` | 最大版本数 |

---

## 层级管理

### memory_tier

HOT/WARM/COLD 层级管理。

| 参数 | 类型 | 描述 |
|------|------|-------------|
| `action` | `string` | 操作：`"status"`, `"migrate"`, `"compress"`, `"redistribute"` |
| `apply` | `boolean` | `false` | 应用更改 |

**层级阈值：**
- HOT：≤ 7 天
- WARM：7–30 天
- COLD：> 30 天

---

## 系统工具

### memory_stats

记忆系统统计。

**参数：** 无

返回：总数、分类、标签、层级分布。

---

### memory_health

MCP 服务器和依赖的健康检查。

**参数：** 无

---

### memory_pin / memory_unpin / memory_pins

固定（锁定）记忆，使其永不压缩或去重。

---

## 错误响应

所有工具在出错时返回带 `isError: true` 的错误响应：

```json
{
  "content": [{ "type": "text", "text": "Search error: connection timeout" }],
  "isError": true
}
```
# 核心 API 参考

> Unified Memory 的 JavaScript SDK 函数。

## 安装

```bash
npm install unified-memory
```

## 导入

```javascript
// ES Modules
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// CommonJS
const { addMemory, searchMemories, getAllMemories } = require('unified-memory');
```

## 记忆函数

### addMemory(memory, options?)

存储新记忆。

```javascript
const id = await addMemory({
  text: "User preference for Python",
  category: "preference",
  importance: 0.9,
  tags: ["python", "preference"],
  scope: "USER",
  metadata: { project: "data" }
}, { transaction: tx });
```

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|------|------|
| `memory.text` | `string` | 是 | 记忆内容 |
| `memory.category` | `string` | 否 | 类别类型 |
| `memory.importance` | `number` | 否 | 0-1 评分 |
| `memory.tags` | `array` | 否 | 标签字符串 |
| `memory.scope` | `string` | 否 | USER/AGENT/TEAM/GLOBAL |
| `memory.metadata` | `object` | 否 | 自定义数据 |
| `options.transaction` | `Transaction` | 否 | 事务上下文 |

**返回：** `string` - 记忆 ID

---

### searchMemories(query, options?)

混合搜索记忆。

```javascript
const results = await searchMemories("quarterly reports", {
  mode: "hybrid",
  topK: 10,
  vectorWeight: 0.7,
  bm25Weight: 0.3,
  scope: "USER",
  filters: {
    category: "fact",
    tags: ["work"]
  }
});
```

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|-----------|------|------|------|
| `query` | `string` | 必需 | 搜索查询 |
| `options.mode` | `string` | `"hybrid"` | `"hybrid"`, `"bm25"`, `"vector"` |
| `options.topK` | `number` | `5` | 结果数量 |
| `options.vectorWeight` | `number` | `0.7` | 向量权重 |
| `options.bm25Weight` | `number` | `0.3` | BM25 权重 |
| `options.scope` | `string` | `null` | 范围过滤 |
| `options.filters` | `object` | `null` | 元数据过滤器 |

**返回：**
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
      created_at: "2026-04-15T10:00:00Z"
    }
  ]
}
```

---

### getAllMemories(options?)

带过滤器的列出所有记忆。

```javascript
const all = await getAllMemories({
  limit: 50,
  offset: 0,
  sortBy: "createdAt",
  sortOrder: "desc"
});
```

---

### getMemory(id)

按 ID 获取单个记忆。

```javascript
const memory = await getMemory("mem_xxx");
```

---

### updateMemory(id, updates, options?)

更新记忆的字段。

```javascript
await updateMemory("mem_xxx", {
  text: "Updated content",
  importance: 0.9
});
```

---

### deleteMemory(id, options?)

删除记忆。

```javascript
await deleteMemory("mem_xxx");
```

---

## 事务函数

### beginTransaction()

开始新事务。

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

### commitTransaction(tx)

提交事务。

---

### rollbackTransaction(tx)

回滚事务。

---

## 实用函数

### getMemoryStats()

获取记忆统计。

```javascript
const stats = await getMemoryStats();
```

---

### memoryExport(params)

导出记忆到文件。

```javascript
await memoryExport({
  format: "json",
  output: "~/memories.json"
});
```

---

### memoryDedup(params)

查找并合并重复。

```javascript
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: true
});
```

---

## 固定函数

### pinMemory(id)

固定记忆（防止压缩/去重）。

```javascript
await pinMemory("mem_xxx");
```

---

### unpinMemory(id)

取消固定记忆。

```javascript
await unpinMemory("mem_xxx");
```

---

### getPinnedMemories()

列出所有固定的记忆。

```javascript
const pinned = await getPinnedMemories();
```

---

## 错误处理

```javascript
import { 
  addMemory, 
  MemoryValidationError, 
  StorageError 
} from 'unified-memory';

try {
  await addMemory({ text: "Test" });
} catch (error) {
  if (error instanceof MemoryValidationError) {
    console.error("Invalid memory:", error.field);
  } else if (error instanceof StorageError) {
    console.error("Storage failed:", error.message);
  }
}
```
# 插件 API 参考

> 用于构建 Unified Memory 插件的 API。

## 插件结构

```javascript
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  description: 'My custom plugin',

  hooks: {
    beforeStore: async (memory) => memory,
    afterStore: async (memory, result) => {},
    beforeSearch: async (query, options) => ({ query, options }),
    afterSearch: async (results, query) => results,
    onInit: async (context) => {},
    onShutdown: async () => {}
  },

  tools: []
};
```

## 钩子 API

### beforeStore(memory)

在记忆存储之前调用。用于转换或验证。

```javascript
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
  memory.metadata = memory.metadata || {};
  memory.metadata.processedBy = 'my-plugin';
  return memory;
}
```

---

### afterStore(memory, result)

在记忆存储之后调用。用于副作用。

```javascript
afterStore: async (memory, result) => {
  await externalApi.syncMemory(memory);
  emit('memory:stored', memory);
}
```

---

### beforeSearch(query, options)

在搜索执行之前调用。用于修改查询。

```javascript
beforeSearch: async (query, options) => {
  const expanded = await expandQuery(query);
  options.scope = options.scope || 'USER';
  return { query: expanded, options };
}
```

---

### afterSearch(results, query)

在搜索结果准备好之后调用。用于过滤/重新排名。

```javascript
afterSearch: async (results, query) => {
  return results.filter(r => r.score > 0.5);
}
```

---

### onInit(context)

在插件加载时调用。用于初始化。

```javascript
onInit: async (context) => {
  this.config = context.config;
  this.client = new ExternalClient(this.config);
  await this.client.connect();
}
```

---

### onShutdown()

在插件卸载时调用。用于清理。

```javascript
onShutdown: async () => {
  await this.client.disconnect();
}
```

## 插件上下文 API

```javascript
interface PluginContext {
  config: PluginConfig;      // 插件特定配置
  storage: StorageInterface; // 存储访问
  search: SearchInterface;   // 搜索访问
  emit: (event: string, data: any) => void;  // 事件发射器
}
```

### 存储接口

```javascript
const memory = await context.storage.getMemory(id);
const memories = await context.storage.getAllMemories(options);
await context.storage.addMemory(memory);
await context.storage.updateMemory(id, updates);
await context.storage.deleteMemory(id);
```

### 搜索接口

```javascript
const results = await context.search.hybridSearch(query, options);
const results = await context.search.bm25Search(query);
const results = await context.search.vectorSearch(query);
```

## 最佳实践

### 总是从钩子返回

```javascript
// 好
beforeStore: async (memory) => {
  return transformMemory(memory);
}

// 坏 - 返回 undefined
beforeStore: async (memory) => {
  memory.text = memory.text.trim();
}
```

### 优雅处理错误

```javascript
beforeStore: async (memory) => {
  try {
    return await validateAndTransform(memory);
  } catch (error) {
    console.error('Plugin error:', error);
    return memory;
  }
}
```

## 测试插件

```javascript
describe('my-plugin', () => {
  it('should have required properties', () => {
    expect(plugin.name).toBe('my-plugin');
    expect(plugin.version).toBe('1.0.0');
  });
});
```
# 数据流

> 数据如何从输入流经 Unified Memory 到存储再返回。

## 存储记忆流程

```
客户端请求: memory_store({ text, category, tags, metadata })
    │
    ▼
工具适配器 (src/tools/memory_store.js)
    │ - 验证参数
    │ - 生成 ID
    │ - 设置时间戳
    └─┬
      │
      ▼
插件钩子 (beforeStore)
    │ - 转换记忆
    │ - 验证
    └─┬
      │
      ▼
记忆服务
    │ - 协调存储
    │ - 处理事务
    └─┬
      │
      ├────────────┬────────────┐
      ▼            ▼            ▼
JSON 存储    向量存储    WAL 记录器
      │            │            │
      └────────────┴────────────┘
                    │
                    ▼
插件钩子 (afterStore)
    │ - 同步外部
    │ - 发出事件
    └─┬
      │
      ▼
响应: { success: true, id: 'mem_xxx' }
```

## 搜索记忆流程

```
客户端: memory_search({ query, mode, topK, filters })
    │
    ▼
工具适配器 (验证 + 解析)
    │
    ▼
插件钩子 (beforeSearch)
    │
    ▼
缓存检查
    │
    ├─ 缓存命中 → 返回缓存的结果
    │
    └─ 缓存未命中 → 混合搜索
                        │
                        ├─────────────────┐
                        ▼                 ▼
                   BM25 搜索        向量搜索
                        │                 │
                        └────────┬────────┘
                                 ▼
                          RRF 融合
                                 │
                                 ▼
                          应用过滤器
                                 │
                                 ▼
                          缓存结果
                                 │
                                 ▼
插件钩子 (afterSearch)
    │
    ▼
响应: { count, results, query, mode }
```

## 数据一致性保证

| 操作 | JSON 存储 | 向量存储 | WAL | 一致性 |
|------|-----------|----------|-----|--------|
| 存储 | 同步写入 | 异步写入 | 同步 | 最终一致 |
| 删除 | 同步删除 | 同步删除 | 同步 | 立即 |
| 更新 | 同步更新 | 异步更新 | 同步 | 最终一致 |
| 恢复 | 重放 WAL | 重放 WAL | - | 已恢复 |

## 下一步

- [概述](./overview.md) - 系统架构
- [设计原则](./design-principles.md) - 关键决策
- [模块](./modules.md) - 模块参考
# 架构概述

> 了解 Unified Memory 的设计及其组件如何协同工作。

## 🏗️ 系统概述

Unified Memory 是一个分层系统，设计用于：
- **可靠性**：原子事务和 WAL 确保数据安全
- **性能**：混合搜索和缓存优化查询速度
- **可扩展性**：插件系统允许自定义功能
- **可扩展性**：模块化架构支持增长

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端应用程序                             │
│        (OpenClaw, Web UI, CLI, REST API, MCP 客户端)       │
└───────────────────────────┬─────────────────────────────────┘
                            │ MCP 工具 / REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API 网关层                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │ MCP 服务器 │  │ REST API   │  │ WebSocket  │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    服务层                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │   记忆     │  │   搜索     │  │   缓存     │             │
│  │   服务     │  │   服务     │  │   服务     │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    存储层                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐             │
│  │   JSON     │  │   向量     │  │    WAL     │             │
│  │   存储     │  │   存储     │  │   记录器   │             │
│  └────────────┘  └────────────┘  └────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 核心组件

| 组件 | 职责 |
|------|------|
| Memory Manager (`src/manager.js`) | 内存操作协调 |
| Storage (`src/storage.js`) | JSON 文件存储 |
| Vector Store (`src/vector.js`) | 嵌入存储和搜索 |
| BM25 Index (`src/bm25.js`) | 关键词搜索索引 |
| Search Fusion (`src/fusion.js`) | 混合搜索编排 |
| MCP Server (`src/index.js`) | MCP 协议实现 |

## 🔄 数据流

### 存储流程

```
Client → MCP Server → Plugins (beforeStore) → Memory Service
                                                      │
                              ┌───────────────────────┼───────────────────────┐
                              ▼                       ▼                       ▼
                        JSON Store            Vector Store              WAL Logger
                              │                       │                       │
                              └───────────────────────┴───────────────────────┘
                                                      │
                                              Plugins (afterStore)
                                                      │
                                                      ▼
                                                  Client Response
```

### 搜索流程

```
Client → MCP Server → Plugins (beforeSearch) → Cache Check
                                                      │
                              ┌───────────────────────┴───────────────────────┐
                              ▼                                               ▼
                      Cache Hit                                        Cache Miss
                              │                                               │
                              ▼                                               ▼
                    Return Cached                              Hybrid Search
                              │                                    │
                              │                         ┌─────────┴─────────┐
                              │                         ▼                   ▼
                              │                    BM25              Vector
                              │                         │                   │
                              │                         └─────────┬─────────┘
                              │                                   ▼
                              │                            RRF 融合
                              │                                   │
                              │                                   ▼
                              │                            应用过滤器
                              │                                   │
                              │                                   ▼
                              │                            Cache Results
                              │                                   │
                              └───────────────────────────────────┘
                                                      │
                                              Plugins (afterSearch)
                                                      │
                                                      ▼
                                                  Client Response
```

## 💾 存储架构

### JSON 存储

```
~/.unified-memory/
└── memories.json
```

### 向量存储 (LanceDB)

```
~/.unified-memory/
└── vector.lance/
```

### WAL (预写日志)

```
~/.unified-memory/
└── wal/
    ├── 000001.log
    └── ...
```

## 📊 性能优化

| 优化 | 描述 | 影响 |
|------|------|------|
| 语义缓存 | 缓存相似查询 | 78% 命中率 |
| 向量缓存 | 缓存嵌入 | 更快搜索 |
| 基于层级的压缩 | 压缩旧记忆 | 减少 60% 存储 |
| 增量 BM25 | 增量更新索引 | 更快的索引 |

## 📚 下一步

- [设计原则](./design-principles.md) - 关键架构决策
- [模块](./modules.md) - 详细的模块参考
- [数据流](./data-flow.md) - 详细的数据流图
# 设计原则

> 指导 Unified Memory 开发的核心理架构原则。

## 🎯 设计理念

Unified Memory 建立在五个基本原则之上：

1. **可靠性第一** - 数据绝不能丢失
2. **默认性能** - 开箱即用的快速
3. **设计可扩展性** - 易于定制
4. **API 简洁性** - 易于学习和使用
5. **透明度** - 清楚数据如何流动

## 📜 原则 1: 可靠性第一

### 数据安全

每个写操作都受到保护：

```javascript
// 原子写入模式
async function atomicStore(memory) {
  const tx = await beginTransaction();
  try {
    await writeJson(memory);
    await writeVector(memory);
    await logToWAL(tx, memory);
    await commitTransaction(tx);
  } catch (error) {
    await rollbackTransaction(tx);
    throw error;
  }
}
```

### WAL 在数据库之前

WAL（预写日志）在任何数据更改之前写入：

1. 记录预期操作
2. 应用操作
3. 将日志条目标记为已提交
4. （可选）fsync 到磁盘

## ⚡ 原则 2: 默认性能

### 智能默认值

系统开箱即用：

| 设置 | 默认 | 原因 |
|------|------|------|
| 搜索模式 | 混合 | 最佳准确性 |
| 缓存 | 启用 | 快速重复查询 |
| 压缩 | 基于层级 | 平衡速度/存储 |
| 向量批处理 | 100 | 最佳吞吐量 |

## 🔌 原则 3: 设计可扩展性

### 插件钩子

每个操作都可以被拦截：

```javascript
const hooks = {
  beforeStore: [],
  afterStore: [],
  beforeSearch: [],
  afterSearch: []
};
```

### 关注点分离

```
工具层 → 服务层 → 存储层 → 基础设施
```

## 📐 模块设计规则

### 单一职责

每个模块有一项工作：

| 模块 | 职责 |
|------|------|
| `storage.js` | JSON 文件 CRUD |
| `vector.js` | 向量操作 |
| `bm25.js` | BM25 索引 |
| `fusion.js` | 结果融合 |
| `tools/*.js` | MCP 工具适配器 |

## 📚 下一步

- [模块](./modules.md) - 详细的模块参考
- [数据流](./data-flow.md) - 详细的数据流图
- [概述](./overview.md) - 系统架构
# 模块参考

> Unified Memory 每个模块的详细文档。

## 📁 模块目录

```
src/
├── storage/           存储后端
├── vector/            向量存储
├── search/            搜索引擎
├── cache/             查询缓存
├── plugin/            插件系统
├── tools/             MCP 工具
├── observability/     指标和监控
└── wal/               预写日志
```

## 🔧 核心模块

### 存储 (`src/storage.js`)

主要 JSON 文件存储。

**公共 API：**
```javascript
addMemory(memory)           // 添加新记忆
getMemory(id)               // 按 ID 获取
getAllMemories(options)     // 带过滤器的列表
updateMemory(id, updates)   // 更新字段
deleteMemory(id)            // 删除记忆
```

### 向量存储 (`src/vector.js`, `src/vector_lancedb.js`)

嵌入和相似度搜索。

**公共 API：**
```javascript
getEmbedding(text)          // 生成嵌入
searchVectors(query, options) // ANN 搜索
addVector(id, text, metadata) // 添加嵌入
deleteVector(id)            // 移除嵌入
```

### BM25 (`src/bm25.js`)

关键词搜索索引。

**公共 API：**
```javascript
buildBM25Index(memories)    // 从记忆构建
bm25Search(query, options)  // 搜索索引
updateBM25Index(memory)    // 增量更新
```

### 搜索融合 (`src/fusion.js`)

混合搜索编排。

**公共 API：**
```javascript
hybridSearch(query, options) // BM25 + 向量 + RRF
```

## 📚 下一步

- [数据流](./data-flow.md) - 数据如何流经模块
- [设计原则](./design-principles.md) - 架构决策
- [概述](./overview.md) - 系统架构
# 参考文档

> 配置、故障排除和 FAQ 的技术参考。

## 📚 内容

| 文档 | 描述 |
|------|------|
| [配置参考](./configuration.md) | 所有配置选项 |
| [故障排除](./troubleshooting.md) | 常见问题和解决方案 |
| [FAQ](./faq.md) | 常见问题 |

## 快速链接

- [配置](./configuration.md) - 完整配置参考
- [故障排除](./troubleshooting.md) - 修复常见问题
- [FAQ](./faq.md) - 常见问题
# 配置参考

> 所有配置选项的完整参考。

## 配置文件位置

```
~/.unified-memory/config.json
```

## 完整配置架构

```json
{
  "storage": { ... },
  "transaction": { ... },
  "search": { ... },
  "cache": { ... },
  "embedding": { ... },
  "tier": { ... },
  "plugins": { ... },
  "observability": { ... },
  "server": { ... }
}
```

## 存储配置

```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance",
      "dimension": 768
    }
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `mode` | `string` | `"json"` | 存储模式：`"json"` 或 `"sqlite"` |
| `memoryFile` | `string` | `"~/.unified-memory/memories.json"` | 记忆文件路径 |
| `vectorStore.backend` | `string` | `"lancedb"` | 向量后端：`"lancedb"` 或 `"chromadb"` |
| `vectorStore.path` | `string` | `"~/.unified-memory/vector.lance"` | 向量存储路径 |
| `vectorStore.dimension` | `number` | `768` | 嵌入维度 |

## 事务配置

```json
{
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transactions.log",
    "fsync": true,
    "timeout": 30000
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `enable` | `boolean` | `true` | 启用原子事务 |
| `recoveryLog` | `string` | `"~/.unified-memory/transactions.log"` | WAL 日志路径 |
| `fsync` | `boolean` | `true` | 写入时 fsync |
| `timeout` | `number` | `30000` | 事务超时（毫秒） |

## 搜索配置

```json
{
  "search": {
    "defaultMode": "hybrid",
    "bm25Weight": 0.3,
    "vectorWeight": 0.7,
    "rrfK": 60,
    "topK": 10,
    "minScore": 0.1
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `defaultMode` | `string` | `"hybrid"` | 默认搜索模式 |
| `bm25Weight` | `number` | `0.3` | 混合搜索中 BM25 权重 (0-1) |
| `vectorWeight` | `number` | `0.7` | 混合搜索中向量权重 (0-1) |
| `rrfK` | `number` | `60` | RRF 常数 |
| `topK` | `number` | `10` | 默认结果数量 |
| `minScore` | `number` | `0.1` | 最小相关性分数 |

## 缓存配置

```json
{
  "cache": {
    "enable": true,
    "type": "semantic",
    "maxSize": 1000,
    "ttl": 3600
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `enable` | `boolean` | `true` | 启用缓存 |
| `type` | `string` | `"semantic"` | 缓存类型 |
| `maxSize` | `number` | `1000` | 最大条目数 |
| `ttl` | `number` | `3600` | TTL（秒） |

## 层级配置

```json
{
  "tier": {
    "hot": { "maxAge": 7, "compression": false },
    "warm": { "minAge": 7, "maxAge": 30, "compression": "light" },
    "cold": { "minAge": 30, "compression": "heavy" }
  }
}
```

| 层级 | 年龄 | 压缩 | 描述 |
|------|------|------|------|
| HOT | ≤ 7 天 | 无 | 活跃记忆 |
| WARM | 7-30 天 | 轻度 | 不太活跃 |
| COLD | > 30 天 | 重度 | 归档 |

## 插件配置

```json
{
  "plugins": {
    "dir": "~/.unified-memory/plugins",
    "autoReload": true,
    "enabled": ["sync-workspace"]
  }
}
```

| 选项 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `dir` | `string` | `"~/.unified-memory/plugins"` | 插件目录 |
| `autoReload` | `boolean` | `true` | 热重载插件 |
| `enabled` | `array` | `[]` | 启用的插件列表 |

## 环境变量

```bash
UNIFIED_MEMORY_STORAGE_MODE=json
UNIFIED_MEMORY_MEMORY_FILE=~/.unified-memory/memories.json
UNIFIED_MEMORY_VECTOR_BACKEND=lancedb
UNIFIED_MEMORY_PORT=3851
OLLAMA_HOST=http://localhost:11434
```

## 配置验证

```bash
unified-memory config:validate
unified-memory config:show
unified-memory config:init
```
# 故障排除指南

> Unified Memory 常见问题的解决方案。

## 📚 内容

1. [安装问题](#安装问题)
2. [启动问题](#启动问题)
3. [存储问题](#存储问题)
4. [搜索问题](#搜索问题)
5. [向量存储问题](#向量存储问题)
6. [插件问题](#插件问题)
7. [数据恢复](#数据恢复)

## 安装问题

### "command not found: unified-memory"

**原因：** 安装不在 PATH 中

**解决方案：**
```bash
npm install -g unified-memory
export PATH="$(npm root -g)/bin:$PATH"
```

### "Node.js version too old"

**原因：** Node.js 版本 < 18.0.0

**解决方案：**
```bash
nvm install 18
nvm use 18
```

## 启动问题

### "Failed to initialize storage"

**原因：** 无法创建/读取存储目录

**解决方案：**
```bash
mkdir -p ~/.unified-memory
chmod 755 ~/.unified-memory
unified-memory init
```

### "Port already in use"

**原因：** 其他进程使用端口 3851

**解决方案：**
```bash
lsof -i :3851
unified-memory serve --port 3852
```

## 存储问题

### "Memory file corrupted"

**原因：** JSON 文件格式错误

**解决方案：**
```bash
# 从备份恢复
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json
```

### "Disk full"

**原因：** 磁盘空间不足

**解决方案：**
```bash
rm -rf ~/.unified-memory/backups/*
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

## 搜索问题

### "Search returns no results"

**原因：** 空索引或查询错误

**解决方案：**
```bash
unified-memory list
unified-memory rebuild-index
```

### "Search very slow"

**原因：** 大数据集，无缓存

**解决方案：**
```bash
# 检查 Ollama 是否运行
ollama serve
ollama list
```

## 向量存储问题

### "LanceDB initialization failed"

**原因：** 向量存储损坏

**解决方案：**
```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### "Ollama connection failed"

**原因：** Ollama 未运行或无模型

**解决方案：**
```bash
ollama serve
ollama pull nomic-embed-text
```

## 数据恢复

### "Recover from crash"

```bash
unified-memory wal --action list
unified-memory recover
```

### "Restore from backup"

```bash
ls ~/.unified-memory/backups/
cp ~/.unified-memory/backups/memories-YYYY-MM-DD.json ~/.unified-memory/memories.json
```

## 获取帮助

### 调试模式

```bash
UNIFIED_MEMORY_DEBUG=1 unified-memory serve
tail -f ~/.unified-memory/logs/app.log
```

### 健康检查

```bash
unified-memory health
```
# 常见问题

> 关于 Unified Memory 的常见问题。

## 基础

### 什么是 Unified Memory？

Unified Memory 是一个企业级 AI 代理记忆管理系统，提供：
- 跨会话持久化存储
- 混合搜索（BM25 + 向量 + RRF）以获得准确检索
- 带 WAL 的原子事务以确保数据安全
- 用于扩展性的插件系统

### 当前版本是什么？

当前版本是 **v5.2.0**。

```bash
unified-memory --version
```

---

## 安装

### 要求是什么？

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0
- **Git**（用于手动安装）
- **Ollama**（可选，用于向量搜索）

### 如何安装？

**快速安装：**
```bash
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash
```

**或通过 npm：**
```bash
npm install -g unified-memory
```

---

## 使用

### 如何存储记忆？

**CLI：**
```bash
unified-memory add "Remember to check reports" --tags work,reminder
```

**JavaScript：**
```javascript
await addMemory({
  text: "Remember to check reports",
  tags: ["work", "reminder"]
});
```

### 如何搜索？

**CLI：**
```bash
unified-memory search "quarterly reports"
```

**JavaScript：**
```javascript
const results = await searchMemories("quarterly reports");
```

### 搜索模式有什么区别？

| 模式 | 描述 | 适用于 |
|------|------|--------|
| `hybrid` | BM25 + 向量 + RRF | 一般使用 |
| `bm25` | 仅关键词 | 精确匹配 |
| `vector` | 仅语义 | 概念匹配 |

---

## 数据

### 数据存储在哪里？

| 数据 | 位置 |
|------|------|
| 记忆 | `~/.unified-memory/memories.json` |
| 向量 | `~/.unified-memory/vector.lance` |
| 配置 | `~/.unified-memory/config.json` |
| WAL | `~/.unified-memory/transactions.log` |

### 如何备份数据？

```bash
unified-memory export --format json --output ~/backup.json
```

---

## 搜索

### 为什么搜索找不到我的记忆？

1. 检查记忆是否存在：`unified-memory list`
2. 重建索引：`unified-memory rebuild-index`
3. 尝试更简单的术语
4. 检查重要性分数（越低越不可能出现）

### 什么是 RRF？

倒数排名融合（Reciprocal Rank Fusion）组合多个搜索算法的结果：
- 获取 BM25 和向量搜索的排名
- 使用公式组合：`RRF = 1/(k + rank)`
- 产生比单独使用任一方法更好的结果

---

## 性能

### 为什么搜索很慢？

可能原因：
- 大数据集（> 10,000 条记忆）
- Ollama 未运行
- 缓存禁用
- 无向量索引

解决方案：
```bash
# 启用缓存（默认开启）
# 检查配置："cache": { "enable": true }

# 重启 Ollama
ollama serve

# 重建索引
unified-memory rebuild-index
```

### 它使用多少内存？

约 1,760 条记忆时：
- 约 245 MB RAM
- 约 50 MB 存储

随记忆数量线性增长。

---

## 插件

### 如何安装插件？

```bash
# 将插件复制到插件目录
cp my-plugin ~/.unified-memory/plugins/

# 在配置中启用
# "plugins": { "enabled": ["my-plugin"] }

# 重启服务器
```

### 我可以创建自定义插件吗？

可以！请参阅[插件开发指南](../guides/plugins.md)。

---

## 故障排除

### "Module not found" 错误

```bash
npm install
```

### 向量存储初始化失败

```bash
rm -rf ~/.unified-memory/vector.lance
unified-memory init
```

### Ollama 连接失败

```bash
ollama serve
ollama pull nomic-embed-text
```

---

## 开发

### 我如何贡献？

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 运行测试：`npm test`
5. 提交 PR

### 如何运行测试？

```bash
npm test
npm run test:unit
npm run test:integration
```

### 如何构建生产版本？

```bash
npm run build
npm run deploy
```

---

## 迁移

### 如何从 v4 迁移到 v5？

v5 与 v4 存储向后兼容。简单地：
1. 安装 v5.2.0
2. 现有数据自动升级
3. 新功能（原子事务）默认启用
# 文档目录结构

    docs
    docs en
    docs en {getting-started,guides,api,architecture,reference}
    docs zh
    docs zh {getting-started,guides,api,architecture,reference}
    docs {en,zh,shared
    docs {en,zh,shared {images,examples,diagrams}}
# Architecture Decision Records (ADR)

> This document records the architectural decisions made for the Unified Memory project.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

## ADR Template

Each ADR follows this template:

```
# [short title of solved problem and solution]

## Status
[proposed | accepted | deprecated | superseded]

## Context
[What is the issue that we're seeing that is motivating this decision or change?]

## Decision
[What is the change that we're proposing and/or doing?]

## Consequences
[What becomes easier or more difficult to do because of this change?]
```

## Table of Contents

- [ADR-001: Hybrid Search Architecture](#adr-001-hybrid-search-architecture)
- [ADR-002: Atomic Transaction System](#adr-002-atomic-transaction-system)
- [ADR-003: Plugin System Design](#adr-003-plugin-system-design)
- [ADR-004: Storage Layer Abstraction](#adr-004-storage-layer-abstraction)
- [ADR-005: Caching Strategy](#adr-005-caching-strategy)
- [ADR-006: API Gateway Design](#adr-006-api-gateway-design)
- [ADR-007: Performance Monitoring](#adr-007-performance-monitoring)
- [ADR-008: Multi-language Support](#adr-008-multi-language-support)
- [ADR-009: Security Architecture](#adr-009-security-architecture)
- [ADR-010: Deployment Architecture](#adr-010-deployment-architecture)

---

## ADR-001: Hybrid Search Architecture

### Status
Accepted (2026-03-15)

### Context
We need a search system that combines the strengths of different search techniques:
1. Keyword search (BM25) for exact matches
2. Semantic search (vector) for similarity matching
3. Result fusion for combining multiple search methods

### Decision
Implement a hybrid search system that combines:
- **BM25**: Traditional keyword-based search
- **Vector Search**: Semantic similarity using embeddings
- **RRF (Reciprocal Rank Fusion)**: Combines results from multiple search methods

Weight distribution:
- BM25: 40%
- Vector Search: 40%
- RRF: 20%

### Consequences
**Positive:**
- 5-10x faster search performance
- Better relevance for both keyword and semantic queries
- Flexible weighting based on use case

**Negative:**
- Increased complexity in search implementation
- Higher memory usage for vector indexes
- Requires tuning of weight parameters

---

## ADR-002: Atomic Transaction System

### Status
Accepted (2026-03-20)

### Context
Memory operations need to be atomic to prevent data corruption and ensure consistency. We need:
1. All-or-nothing operations
2. Rollback capability
3. Data consistency guarantees

### Decision
Implement an atomic transaction system using:
1. **WAL (Write-Ahead Logging)**: All changes logged before commit
2. **SQLite Transactions**: Leverage SQLite's ACID compliance
3. **Two-Phase Commit**: For distributed operations

Transaction flow:
```
Begin Transaction → Write to WAL → Validate → Commit → Cleanup
```

### Consequences
**Positive:**
- Data integrity guaranteed
- Recovery from crashes
- Consistent state across operations

**Negative:**
- Slightly slower write performance
- Additional storage for WAL
- Complexity in transaction management

---

## ADR-003: Plugin System Design

### Status
Accepted (2026-03-25)

### Context
We need an extensible architecture that allows:
1. Adding new features without modifying core
2. Third-party extensions
3. Hot reloading of components

### Decision
Implement a plugin system with:
1. **Plugin Registry**: Central registry for all plugins
2. **Lifecycle Hooks**: Before/after hooks for operations
3. **Dependency Injection**: Plugin dependencies managed
4. **Hot Reload**: Plugins can be reloaded without restart

Plugin types:
- Storage plugins
- Search plugins
- Analytics plugins
- Integration plugins

### Consequences
**Positive:**
- Highly extensible architecture
- Community contributions easier
- Modular design

**Negative:**
- Plugin compatibility issues
- Security concerns with third-party plugins
- Increased complexity

---

## ADR-004: Storage Layer Abstraction

### Status
Accepted (2026-04-01)

### Context
We need to support multiple storage backends:
1. SQLite for local development
2. PostgreSQL for production
3. Vector databases for embeddings

### Decision
Implement a storage abstraction layer:
1. **Storage Interface**: Common interface for all storage backends
2. **Adapter Pattern**: Adapters for different storage systems
3. **Migration Support**: Easy migration between backends

Storage hierarchy:
```
Application → Storage Interface → Adapter → Storage Backend
```

### Consequences
**Positive:**
- Database agnostic
- Easy to switch storage backends
- Better testability

**Negative:**
- Additional abstraction layer
- Performance overhead
- Complexity in adapter implementation

---

## ADR-005: Caching Strategy

### Status
Accepted (2026-04-05)

### Context
Search performance needs optimization:
1. Frequent queries should be cached
2. Cache invalidation on data changes
3. Multi-level caching for different data types

### Decision
Implement multi-level caching:
1. **Level 1**: In-memory cache (LRU)
2. **Level 2**: Redis cache (distributed)
3. **Level 3**: Database cache (query results)

Cache strategies:
- **TTL**: Time-based expiration
- **LRU**: Least Recently Used eviction
- **Write-through**: Cache updated on write
- **Predictive**: Pre-fetch based on patterns

### Consequences
**Positive:**
- 60% reduction in search latency
- Better scalability
- Reduced database load

**Negative:**
- Cache consistency issues
- Memory usage increase
- Complexity in cache management

---

## ADR-006: API Gateway Design

### Status
Accepted (2026-04-08)

### Context
Multiple API protocols needed:
1. REST for web/mobile clients
2. MCP for AI agents
3. WebSocket for real-time updates

### Decision
Implement API gateway pattern:
1. **Protocol Adapters**: Separate adapters for each protocol
2. **Common Service Layer**: Shared business logic
3. **Rate Limiting**: Per-protocol rate limits
4. **Authentication**: Unified auth across protocols

Gateway architecture:
```
Client → Protocol Adapter → Service Layer → Storage
```

### Consequences
**Positive:**
- Multiple protocol support
- Centralized authentication
- Better monitoring

**Negative:**
- Gateway becomes single point of failure
- Increased latency
- Complexity in protocol translation

---

## ADR-007: Performance Monitoring

### Status
Accepted (2026-04-10)

### Context
We need to monitor system performance:
1. Real-time metrics
2. Alerting on issues
3. Historical analysis

### Decision
Implement comprehensive monitoring:
1. **Metrics Collection**: System and application metrics
2. **Alerting System**: Threshold-based alerts
3. **Dashboard**: Real-time visualization
4. **Log Aggregation**: Centralized logging

Monitoring stack:
- **Metrics**: Prometheus
- **Visualization**: Grafana
- **Logging**: ELK Stack
- **Alerting**: Alertmanager

### Consequences
**Positive:**
- Proactive issue detection
- Performance optimization
- Better user experience

**Negative:**
- Additional infrastructure
- Performance overhead
- Maintenance complexity

---

## ADR-008: Multi-language Support

### Status
Accepted (2026-04-12)

### Context
Global user base requires:
1. Chinese language support
2. English as primary language
3. Easy addition of new languages

### Decision
Implement i18n system:
1. **Translation Files**: JSON-based translation files
2. **Language Detection**: Automatic based on user preferences
3. **Fallback Chains**: English as fallback language
4. **RTL Support**: Right-to-left language support

Implementation:
- **Frontend**: React i18next
- **Backend**: i18n-express
- **Documentation**: Separate language directories

### Consequences
**Positive:**
- Global accessibility
- Better user experience
- Community contributions easier

**Negative:**
- Translation maintenance
- Increased bundle size
- UI layout challenges

---

## ADR-009: Security Architecture

### Status
Accepted (2026-04-13)

### Context
Security requirements:
1. Data encryption
2. Access control
3. Audit logging
4. Vulnerability protection

### Decision
Implement defense-in-depth security:
1. **Encryption**: AES-256 for data at rest, TLS 1.3 for transit
2. **Authentication**: JWT with refresh tokens
3. **Authorization**: RBAC with fine-grained permissions
4. **Audit**: Comprehensive audit logging
5. **Input Validation**: Strict input validation

Security layers:
- Network security
- Application security
- Data security
- Access security

### Consequences
**Positive:**
- Comprehensive security coverage
- Regulatory compliance
- User trust

**Negative:**
- Performance impact
- Complexity in implementation
- Maintenance overhead

---

## ADR-010: Deployment Architecture

### Status
Accepted (2026-04-14)

### Context
Deployment requirements:
1. Scalability
2. High availability
3. Easy updates
4. Disaster recovery

### Decision
Implement cloud-native deployment:
1. **Containerization**: Docker containers
2. **Orchestration**: Kubernetes
3. **CI/CD**: GitHub Actions
4. **Monitoring**: Prometheus + Grafana

Deployment strategy:
- **Blue-Green**: Zero-downtime deployments
- **Canary**: Gradual rollout
- **Rollback**: Automatic rollback on failure

### Consequences
**Positive:**
- High availability
- Easy scaling
- Automated deployments

**Negative:**
- Infrastructure complexity
- Learning curve
- Cost considerations

---

## How to Propose a New ADR

1. Create a new ADR file in `docs/architecture/decisions/`
2. Use the ADR template
3. Submit for review
4. Update status based on decision

## ADR Lifecycle

1. **Proposed**: New ADR submitted
2. **Under Review**: Being reviewed by architecture team
3. **Accepted**: Approved for implementation
4. **Implemented**: Code changes made
5. **Deprecated**: Replaced by newer ADR
6. **Superseded**: New ADR replaces this one

## References

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Repository](https://github.com/joelparkerhenderson/architecture-decision-record)
- [Nygard's ADR Article](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions)# Unified Memory v5.2.0

> 🧠 **Unified Memory v5.2.0** — Atomic Write Fixes & Performance Optimization · Enterprise Memory Management Platform · Pure Node.js ESM

[![Version](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-green.svg)](https://github.com/mouxangithub/unified-memory)
[![Data Safety](https://img.shields.io/badge/data%20safety-atomic%20writes-brightgreen.svg)](https://github.com/mouxangithub/unified-memory)
[![Performance](https://img.shields.io/badge/performance-optimized-orange.svg)](https://github.com/mouxangithub/unified-memory)

**English** · [中文](./README_CN.md) · [Changelog](./en/reference/changelog.md) · [Documentation](./en/)

---

## 🚀 Latest Updates (v5.2.0)

### 🔥 Atomic Write Fixes (2026-04-15)
**Solved the most critical data consistency issues in production environments**:

| Fix | Problem | Solution | Effect |
|-----|---------|----------|--------|
| **Atomic Transaction Manager** | No atomicity in JSON and vector storage dual-writes | Two-phase commit protocol | 100% data consistency |
| **Data Persistence Guarantee** | Data loss on system crash | fsync + atomic rename | Zero data loss |
| **Vector Search Optimization** | LanceDB WHERE clause bug | Optimized memory filtering algorithm | 5-10x query performance improvement |
| **ChromaDB Backend** | LanceDB performance issues | Complete ChromaDB backend | Ready to switch anytime |

### 📊 Performance Improvements
- **Retrieval Speed**: 5-10x faster (optimized vector search)
- **Storage Space**: 60% savings (intelligent compression)
- **Data Safety**: fsync guaranteed write to disk
- **Query Performance**: Optimized memory filtering algorithm

---

## 🎯 Core Features

### 🔄 **Atomic Data Consistency**
- **Two-Phase Commit Protocol**: Guarantees atomic writes for JSON and vector storage
- **Transaction Recovery Mechanism**: Automatically recovers unfinished transactions on system crash
- **fsync Guarantee**: Ensures data is written to disk, preventing loss

### 🔍 **High-Performance Hybrid Search**
- **BM25 + Vector + RRF Fusion**: Best relevance ranking
- **Optimized Vector Engine**: Supports LanceDB and ChromaDB
- **Memory Caching**: Fast ANN similarity calculation
- **Intelligent Filtering**: Optimized memory filtering algorithm

### 💾 **Enterprise-Grade Data Security**
- **WAL Protocol**: Crash recovery guarantee
- **Atomic Transactions**: Two-phase commit ensures data consistency
- **fsync Guarantee**: Zero data loss

### 🔌 **Plugin System (New)**
- **Sync Bridge**: Intelligent synchronization between Workspace Memory ↔ Unified Memory
- **Unified Query**: Cross-system retrieval interface
- **Deduplication Check**: Prevents duplicate storage
- **Health Monitoring**: Real-time system status monitoring

---

## 🚀 Quick Start

### Installation
```bash
# Using install script (recommended)
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# Or using npm
npm install unified-memory
```

### Basic Usage
```javascript
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// Add a memory
const memoryId = await addMemory({
  text: "Meeting notes from product review",
  tags: ["meeting", "product", "review"],
  metadata: { priority: "high", project: "alpha" }
});

// Search memories
const results = await searchMemories("product review meeting");
console.log(results);

// Get all memories
const allMemories = await getAllMemories();
```

### Plugin System Usage
```bash
# Sync Workspace Memory
npm run sync:manual

# Unified query
npm run query:unified -- "search keywords"

# Deduplication check
npm run dedup

# Health monitoring
npm run monitor
```

---

## 📁 Project Structure

```
unified-memory/
├── src/                    # Core system
├── plugins/               # Plugin system
├── scripts/               # Scripts directory
├── test/                  # Tests directory
├── docs/                  # Documentation (this directory)
├── config/                # Configuration files
├── bin/                   # CLI tools
├── examples/              # Example code
├── .clawhub/              # ClawHub configuration
├── install.sh            # Installation script
├── README.md             # Main documentation (this file)
└── package.json          # Project configuration
```

---

## 🔧 Configuration

### Basic Configuration
```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance"
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transaction-recovery.log"
  }
}
```

### Performance Tuning
```json
{
  "performance": {
    "cacheSize": 1000,
    "writeBehindDelay": 500,
    "vectorCache": true,
    "batchSize": 100
  }
}
```

---

## 📚 Documentation

### Getting Started
- [Installation Guide](./en/getting-started/installation.md)
- [Quick Start Guide](./en/getting-started/quickstart.md)
- [Configuration Guide](./en/getting-started/configuration.md)

### User Guides
- [Basic Usage](./en/guides/basic-usage.md)
- [Advanced Features](./en/guides/advanced-features.md)
- [Plugin System](./en/guides/plugins.md)
- [Troubleshooting](./en/guides/troubleshooting.md)

### API Documentation
- [API Reference (English)](./en/api/README.md)
- [API 参考 (中文)](./zh/api/README.md)
- [Architecture Guide](./ARCHITECTURE.md)
- [MCP Configuration](./MCP-CONFIG-GUIDE.md)

### Architecture
- [Module Architecture](./ARCHITECTURE.md)
- [Architecture Decisions](./ARCHITECTURE_DECISIONS.md)
- [Project Structure](./STRUCTURE.md)

### Reference
- [CLI Reference](./en/reference/cli-reference.md)
- [Configuration Reference](./en/reference/configuration.md)
- [Changelog](./en/reference/changelog.md)
- [FAQ](./en/reference/faq.md)

---

## 🔌 Plugin System Usage

### Sync Workspace Memory
```bash
# Manual sync
npm run sync:manual

# Scheduled sync (daily at 2 AM)
npm run sync

# Generate crontab configuration
npm run crontab
```

### Unified Query
```bash
# Basic query
npm run query:unified -- "search keywords"

# Start query server
npm run query:unified -- --server 3851
```

### Deduplication Check
```bash
# Check for duplicate memories
npm run dedup
```

### Health Monitoring
```bash
# Single check
npm run monitor

# Dashboard view
npm run monitor:dashboard
```

### Deployment & Verification
```bash
# Deploy atomic fixes
npm run deploy

# Verify fixes
npm run verify

# Update documentation
npm run docs
```

---

## 🛠️ Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory

# Install dependencies
npm install

# Start development server
npm run dev
```

### Running Tests
```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# Performance tests
npm run bench
```

### Building for Production
```bash
# Build project
npm run deploy

# Verify build
npm run verify
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](./en/reference/contributing.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/mouxangithub/unified-memory/issues)
- **Documentation**: [Full documentation](./en/)
- **中文文档**: [Chinese documentation](./zh/)

---

## 🏆 Acknowledgments

- **OpenClaw Community** for inspiration and feedback
- **All Contributors** who helped improve Unified Memory
- **The Node.js ecosystem** for amazing tools and libraries

---

**Last Updated**: 2026-04-15  
**Version**: v5.2.0  
**Status**: 🟢 Production Ready  
**GitHub**: https://github.com/mouxangithub/unified-memory  
**Documentation**: https://github.com/mouxangithub/unified-memory/tree/main/docs# Unified Memory v5.2.0

> 🧠 **Unified Memory v5.2.0** — 原子写入修复与性能优化系统 · 企业级记忆管理平台 · Pure Node.js ESM

[![版本](https://img.shields.io/badge/版本-5.2.0-蓝色.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-绿色.svg)](https://nodejs.org/)
[![许可证: MIT](https://img.shields.io/badge/许可证-MIT-黄色.svg)](https://opensource.org/licenses/MIT)
[![构建状态](https://img.shields.io/badge/构建-通过-绿色.svg)](https://github.com/mouxangithub/unified-memory)
[![数据安全](https://img.shields.io/badge/数据安全-原子写入-亮绿色.svg)](https://github.com/mouxangithub/unified-memory)
[![性能](https://img.shields.io/badge/性能-已优化-橙色.svg)](https://github.com/mouxangithub/unified-memory)

[English](./README.md) · **中文** · [更新日志](./zh/reference/changelog.md) · [文档](./zh/)

---

## 🚀 最新更新 (v5.2.0)

### 🔥 原子写入修复 (2026-04-15)
**解决了生产环境中最严重的数据一致性问题**：

| 修复 | 问题 | 解决方案 | 效果 |
|------|------|----------|------|
| **原子事务管理器** | JSON 和向量存储双写无原子性 | 两阶段提交协议 | 100% 数据一致性 |
| **数据持久化保证** | 系统崩溃时数据丢失 | fsync + 原子重命名 | 零数据丢失 |
| **向量搜索优化** | LanceDB WHERE 子句 bug | 优化的内存过滤算法 | 5-10倍查询性能提升 |
| **ChromaDB 后端** | LanceDB 性能问题 | 完整的 ChromaDB 后端 | 随时可切换 |

### 📊 性能改进
- **检索速度**: 5-10倍提升（优化的向量搜索）
- **存储空间**: 60% 节省（智能压缩）
- **数据安全**: fsync 保证写入磁盘
- **查询性能**: 优化的内存过滤算法

---

## 🎯 核心特性

### 🔄 **原子数据一致性**
- **两阶段提交协议**: 保证 JSON 和向量存储的原子性写入
- **事务恢复机制**: 系统崩溃时自动恢复未完成的事务
- **fsync 保证**: 确保数据写入磁盘，防止丢失

### 🔍 **高性能混合搜索**
- **BM25 + 向量 + RRF 融合**: 最佳相关性排序
- **优化的向量引擎**: 支持 LanceDB 和 ChromaDB
- **内存缓存**: 快速 ANN 相似度计算
- **智能过滤**: 优化的内存过滤算法

### 💾 **企业级数据安全**
- **WAL 协议**: 崩溃恢复保障
- **原子事务**: 两阶段提交保证数据一致性
- **fsync 保证**: 零数据丢失

### 🔌 **插件系统 (新增)**
- **同步桥梁**: Workspace Memory ↔ Unified Memory 智能同步
- **统一查询**: 跨系统检索接口
- **去重检查**: 防止重复存储
- **健康监控**: 实时系统状态监控

---

## 🚀 快速开始

### 安装
```bash
# 使用安装脚本 (推荐)
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# 或使用 npm
npm install unified-memory
```

### 基本使用
```javascript
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// 添加记忆
const memoryId = await addMemory({
  text: "产品评审会议记录",
  tags: ["会议", "产品", "评审"],
  metadata: { priority: "高", project: "alpha" }
});

// 搜索记忆
const results = await searchMemories("产品评审会议");
console.log(results);

// 获取所有记忆
const allMemories = await getAllMemories();
```

### 插件系统使用
```bash
# 同步 Workspace Memory
npm run sync:manual

# 统一查询
npm run query:unified -- "搜索关键词"

# 去重检查
npm run dedup

# 健康监控
npm run monitor
```

---

## 📁 项目结构

```
unified-memory/
├── src/                    # 核心系统
├── plugins/               # 插件系统
├── scripts/               # 脚本目录
├── test/                  # 测试目录
├── docs/                  # 文档目录 (本目录)
├── config/                # 配置文件
├── bin/                   # CLI工具
├── examples/              # 示例代码
├── .clawhub/              # ClawHub 配置
├── install.sh            # 安装脚本
├── README.md             # 主文档 (本文件)
└── package.json          # 项目配置
```

---

## 🔧 配置

### 基础配置
```json
{
  "storage": {
    "mode": "json",
    "memoryFile": "~/.unified-memory/memories.json",
    "vectorStore": {
      "backend": "lancedb",
      "path": "~/.unified-memory/vector.lance"
    }
  },
  "transaction": {
    "enable": true,
    "recoveryLog": "~/.unified-memory/transaction-recovery.log"
  }
}
```

### 性能调优
```json
{
  "performance": {
    "cacheSize": 1000,
    "writeBehindDelay": 500,
    "vectorCache": true,
    "batchSize": 100
  }
}
```

---

## 📚 文档

### 快速开始
- [安装指南](./zh/getting-started/installation.md)
- [快速开始指南](./zh/getting-started/quickstart.md)
- [配置指南](./zh/getting-started/configuration.md)

### 使用指南
- [基础使用](./zh/guides/basic-usage.md)
- [高级功能](./zh/guides/advanced-features.md)
- [插件系统](./zh/guides/plugins.md)
- [故障排除](./zh/guides/troubleshooting.md)

### API 文档
- [API 概览](./zh/api/overview.md)
- [存储 API](./zh/api/storage-api.md)
- [向量 API](./zh/api/vector-api.md)
- [插件 API](./zh/api/plugin-api.md)

### 架构设计
- [架构概览](./zh/architecture/overview.md)
- [原子事务](./zh/architecture/atomic-transactions.md)
- [向量搜索](./zh/architecture/vector-search.md)
- [插件系统](./zh/architecture/plugin-system.md)

### 参考手册
- [CLI 参考](./zh/reference/cli-reference.md)
- [配置参考](./zh/reference/configuration.md)
- [更新日志](./zh/reference/changelog.md)
- [常见问题](./zh/reference/faq.md)

---

## 🔌 插件系统使用

### 同步 Workspace Memory
```bash
# 手动同步
npm run sync:manual

# 定时同步 (每日凌晨2点)
npm run sync

# 生成 crontab 配置
npm run crontab
```

### 统一查询
```bash
# 基本查询
npm run query:unified -- "搜索关键词"

# 启动查询服务器
npm run query:unified -- --server 3851
```

### 去重检查
```bash
# 检查重复记忆
npm run dedup
```

### 健康监控
```bash
# 单次检查
npm run monitor

# 仪表板视图
npm run monitor:dashboard
```

### 部署与验证
```bash
# 部署原子修复
npm run deploy

# 验证修复
npm run verify

# 更新文档
npm run docs
```

---

## 🛠️ 开发

### 设置开发环境
```bash
# 克隆仓库
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 运行测试
```bash
# 单元测试
npm run test:unit

# 集成测试
npm run test:integration

# 性能测试
npm run bench
```

### 生产环境构建
```bash
# 构建项目
npm run deploy

# 验证构建
npm run verify
```

---

## 🤝 贡献

我们欢迎贡献！请查看我们的[贡献指南](./zh/reference/contributing.md)了解详情。

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 运行测试
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。

---

## 📞 支持

- **GitHub Issues**: [报告 bug 或请求功能](https://github.com/mouxangithub/unified-memory/issues)
- **文档**: [完整文档](./zh/)
- **English Documentation**: [英文文档](./README.md)

---

## 🏆 致谢

- **OpenClaw 社区** 的灵感和反馈
- **所有贡献者** 帮助改进 Unified Memory
- **Node.js 生态系统** 提供了优秀的工具和库

---

**最后更新**: 2026-04-15  
**版本**: v5.2.0  
**状态**: 🟢 生产就绪  
**GitHub**: https://github.com/mouxangithub/unified-memory  
**文档**: https://github.com/mouxangithub/unified-memory/tree/main/docs# Unified Memory — Module Architecture

> Clear separation of responsibilities across all modules. Last updated: 2026-04-20.

---

## 📁 Directory Map

```
src/
├── agents/          Agent orchestration & collaboration
├── api/             HTTP/MCP server interfaces
├── backup/          Backup & restore
├── benchmark/       Performance benchmarking
├── chunking/        Text chunking strategies
├── claudemem_features/  Claude memory compatibility
├── cli/             Command-line tools
├── collab/          Collaboration features
├── compression/     Memory compression
├── config/          Configuration management
├── connectors/      External system connectors
├── consolidate/     Memory consolidation
├── conversation/     Conversation processing
├── core/            Core memory operations
├── decay/           Time-based importance decay
├── deduplication/   Deduplication logic
├── episode/         Episode capture & management
├── extraction/      Memory extraction from text
├── extractors/      Pluggable content extractors
├── forgetting/      Forgetting & TTL management
├── graph/           Knowledge graph
├── hooks/           Lifecycle hooks
├── integrations/     Third-party integrations
├── lifecycle/       Lifecycle management
├── memory_types/    Memory type definitions
├── multimodal/      Multimodal content support
├── observability/   Metrics & monitoring
├── parsing/         Input parsing
├── persona/         Persona management
├── plugin/          Plugin system
├── procedural/      Procedural memory
├── profile/         User profile aggregation
├── prompts/        Prompt templates
├── quality/         Memory quality scoring
├── queue/           Async operation queue
├── recall/          Memory recall strategies
├── record/          L1 record processing
├── relations/       Memory relations
├── rerank/          Result reranking
├── retrieval/       Retrieval strategies
├── rule/            Rule-based processing
├── scene/           Scene understanding
├── search/          Search engine
├── session/         Session management
├── setup/           System initialization
├── storage/         Storage backends
├── store/           Store operations
├── system/          System-level operations
├── tools/           MCP tool implementations
├── utils/           Shared utilities
├── v4/              v4.0 storage gateway
└── visualize/       Visualization

top-level (flat .js files):  Large cross-cutting modules (memory.js, index.js, etc.)
```

---

## 🎯 Core Principle: One Module = One Responsibility

| Module | Responsibility | Public API |
|--------|---------------|------------|
| `src/storage.js` | SQLite JSON file CRUD | `addMemory`, `getMemory`, `getAllMemories`, `deleteMemory`, `saveMemories` |
| `src/vector.js` / `vector_lancedb.js` | Vector embeddings & search | `getEmbedding`, `searchVectors` |
| `src/bm25.js` | BM25 keyword index | `buildBM25Index`, `bm25Search` |
| `src/fusion.js` | Hybrid search (BM25 + Vector + RRF) | `hybridSearch` |
| `src/index.js` | MCP server entry point, all tool registrations | All `server.registerTool()` calls |
| `src/manager.js` | Memory lifecycle manager | `init`, `shutdown`, `tick` |
| `src/memory.js` | Unified memory facade | `store`, `search`, `get`, `delete` |
| `src/tools/*.js` | Individual MCP tool implementations | `executeXxx`, `cmdXxx`, `XxxTool` |

---

## 🔄 Tool Flow (MCP Request → Response)

```
MCP Client
    │
    ▼
src/index.js  (McpServer)
    │  server.registerTool('memory_search', ...)
    ▼
src/tools/memory_search.js  (executeMemorySearch)
    │
    ▼
src/fusion.js  (hybridSearch)
    │
    ├──► src/bm25.js  (bm25Search)
    ├──► src/vector.js  (getEmbedding + searchVectors)
    └──► src/recall/  (recall strategies)
    │
    ▼
src/tools/memory_search.js  (formatSearchResponse)
    │
    ▼
MCP Response
```

---

## ⚠️ Responsibility Overlaps to Avoid

### 1. Storage vs. Cache
- **Storage** (`src/storage.js`): Source of truth, persists memories to disk
- **Cache** (`src/cache_semantic.js`): Ephemeral query result cache
- **Rule**: Never write to storage from cache. Never use cache as source of truth.

### 2. Search vs. Retrieval
- **Search** (`src/search/`, `src/fusion.js`): Query-time rankers
- **Retrieval** (`src/retrieval/`): What memories to fetch before ranking
- **Rule**: `fusion.js` orchestrates. Individual search engines (BM25, vector) only rank.

### 3. Tools vs. Core Logic
- **Tools** (`src/tools/*.js`): MCP adapter layer, input validation, output formatting
- **Core logic** (`src/core/`, `src/storage.js`): Business logic, no MCP dependencies
- **Rule**: Tools import from core. Core never imports from tools.

### 4. Episode vs. Conversation vs. Transcript
| Module | Scope |
|--------|-------|
| `conversation/` | L0 capture from raw messages |
| `episode/` | Grouped conversation episodes |
| `transcript_manager.js` | Persistent transcript storage |

### 5. dedup.js (top-level) vs. deduplication/ (module)
| File | Responsibility |
|------|---------------|
| `src/dedup.js` | Top-level dedup CLI/interface |
| `src/deduplication/` | Core dedup algorithm & merging |
| `src/record/l1_dedup.js` | L1 extraction dedup |

---

## 📊 Tier System

Memories are automatically classified by age:

| Tier | Age | Compression | Eligible for Dedup |
|------|-----|------------|-------------------|
| HOT | ≤ 7 days | None | Yes |
| WARM | 7–30 days | Light | Yes |
| COLD | > 30 days | Heavy | Yes |

Pinned memories are **never** compressed or deduplicated.

---

## 🔌 Plugin System

Plugins live in `plugins/` and must export:
```javascript
export const plugin = {
  name: 'my-plugin',
  version: '1.0.0',
  hooks: {
    beforeStore: async (mem) => mem,
    afterSearch: async (results) => results,
  }
};
```

---

## 🧠 v4.0 Storage Gateway

`src/v4/storage-gateway.js` is a ground-up rewrite of storage with:
- SQLite with proper schema (memories, evidence, versions, wal tables)
- Incremental BM25 (no full rebuild)
- Multi-tenant team spaces
- Evidence TTL chains
- Distributed rate limiting

**v4 is additive** — it coexists with v3 storage. Use `memory_v4_*` tools for new features.

---

## 📝 Documentation Structure

```
docs/
├── README.md              Landing page (EN)
├── README_CN.md           Landing page (ZH)
├── ARCHITECTURE.md       This file
├── STRUCTURE.md          Directory structure overview
├── MCP-CONFIG-GUIDE.md   MCP server configuration
├── en/
│   ├── README.md          EN section index
│   ├── index.md           EN landing
│   ├── getting-started/
│   │   └── quickstart.md  5-minute quick start
│   ├── guides/
│   ├── api/               API reference (MCP tools)
│   ├── architecture/
│   └── reference/
└── zh/
    ├── README.md          ZH section index
    ├── index.md           ZH landing
    ├── getting-started/
    ├── guides/
    ├── api/
    ├── architecture/
    ├── contributing/
    └── reference/
```
