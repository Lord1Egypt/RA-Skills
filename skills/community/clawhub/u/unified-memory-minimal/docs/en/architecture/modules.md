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
