# 配置说明

## 配置文件

### 1. 集成配置

文件: `memory/integration-config.json`

```json
{
  "version": "1.0.0",
  "unifiedMemory": {
    "enabled": true,
    "path": "../unified-memory"
  },
  "search": {
    "hybrid": true,
    "bm25": true,
    "vector": true,
    "rrf": true
  },
  "storage": {
    "rawPath": "memory/raw",
    "processedPath": "memory/processed",
    "archivePath": "memory/archive",
    "importPath": "memory/import"
  },
  "indexing": {
    "autoBuild": true,
    "incremental": true,
    "rebuildOnChange": false
  }
}
```

### 2. 脚本配置

在脚本中直接配置：

```javascript
// query.cjs 配置
const CONFIG = {
  DEFAULT_LIMIT: 100,      // 默认返回数量
  MAX_LIMIT: 1000,         // 最大返回数量
  CACHE_SIZE: 500,         // 缓存大小
  TIMEOUT: 5000            // 超时时间(ms)
};
```

## 环境变量

### 可选环境变量

```bash
# 数据目录
export UNIFIED_MEMORY_DATA="/path/to/data"

# 缓存大小
export UNIFIED_MEMORY_CACHE=1000

# 日志级别
export UNIFIED_MEMORY_LOG="info"

# 调试模式
export UNIFIED_MEMORY_DEBUG=false
```

## 自定义配置

### 自定义查询行为

```javascript
// 创建自定义配置
const customQuery = require('./memory/scripts/query.cjs');

// 使用自定义配置
customQuery.configure({
  defaultLimit: 50,
  enableCache: true,
  logLevel: 'debug'
});
```

### 自定义标签

编辑 `scripts/enhance-tags.cjs`：

```javascript
const CUSTOM_TAGS = {
  priority: ['high', 'medium', 'low'],
  domain: ['technical', 'creative', 'personal'],
  status: ['active', 'archived', 'deleted']
};
```

## 配置验证

验证配置：

```bash
node memory/scripts/verify-system.cjs
```

输出：
```
Configuration:
  - Search: hybrid (BM25 + Vector + RRF)
  - Storage: 7-layer structure
  - Index: auto-build enabled
  - Cache: 500 items
```
