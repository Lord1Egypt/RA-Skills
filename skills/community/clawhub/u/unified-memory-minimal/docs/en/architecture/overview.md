# Architecture Overview

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
