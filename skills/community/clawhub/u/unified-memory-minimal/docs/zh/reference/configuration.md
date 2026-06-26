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
