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
