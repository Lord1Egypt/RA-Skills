# 性能优化文档

## 性能指标

### 检索性能

| 查询类型 | 性能提升 | 响应时间 |
|----------|----------|----------|
| 标签查询 | 5-10x | < 50ms |
| 日期查询 | 3-5x | < 30ms |
| 全文搜索 | 2-3x | < 100ms |
| 情感查询 | 3-5x | < 30ms |

### 存储性能

| 指标 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 原始数据 | 4.2MB | 1.7MB | 60% |
| 索引数据 | 无 | 352KB | - |
| 归档数据 | 未归档 | 3.7MB | 清理主目录 |

### 内存优化

| 操作 | 内存占用 | 优化效果 |
|------|----------|----------|
| 索引加载 | 352KB | - |
| 查询处理 | 按需加载 | 30-50% 降低 |
| 缓存效率 | 多级缓存 | 2-3x 提升 |

## 优化策略

### 1. 索引优化

多层索引设计：
```javascript
const index = {
  byType: {},      // O(1) 类型查找
  byDate: {},      // O(1) 日期查找
  byTag: {},       // O(1) 标签查找
  bySentiment: {}, // O(1) 情感查找
  byLanguage: {},  // O(1) 语言查找
  byEntity: {}     // O(1) 实体查找
};
```

### 2. 搜索优化

混合搜索策略：
```javascript
async function hybridSearch(query, options) {
  // 1. BM25 关键词搜索
  const bm25Results = await bm25Search(query);
  
  // 2. 向量语义搜索
  const vectorResults = await vectorSearch(query);
  
  // 3. RRF 融合排名
  const fusedResults = rrfFusion(bm25Results, vectorResults);
  
  return fusedResults;
}
```

### 3. 存储优化

数据压缩策略：
- JSON → JSONL 格式压缩
- 短期数据自动归档
- 冷热数据分离存储

## 性能调优

### 调整缓存大小

```javascript
// 在 query.cjs 中
const CACHE_SIZE = 1000; // 默认1000条
```

### 调整批量大小

```javascript
// 在 import-memories.cjs 中
const BATCH_SIZE = 100; // 默认100条一批
```

### 启用压缩

```javascript
// 在 enhance-tags.cjs 中
const USE_COMPRESSION = true;
```
