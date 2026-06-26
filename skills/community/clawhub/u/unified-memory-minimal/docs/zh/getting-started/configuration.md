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
