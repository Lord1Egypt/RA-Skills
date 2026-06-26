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
