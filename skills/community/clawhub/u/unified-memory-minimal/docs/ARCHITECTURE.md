# Unified Memory — Module Architecture

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
