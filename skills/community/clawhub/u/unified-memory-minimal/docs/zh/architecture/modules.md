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
