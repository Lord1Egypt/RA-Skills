# 核心 API 参考

> Unified Memory 的 JavaScript SDK 函数。

## 安装

```bash
npm install unified-memory
```

## 导入

```javascript
// ES Modules
import { addMemory, searchMemories, getAllMemories } from 'unified-memory';

// CommonJS
const { addMemory, searchMemories, getAllMemories } = require('unified-memory');
```

## 记忆函数

### addMemory(memory, options?)

存储新记忆。

```javascript
const id = await addMemory({
  text: "User preference for Python",
  category: "preference",
  importance: 0.9,
  tags: ["python", "preference"],
  scope: "USER",
  metadata: { project: "data" }
}, { transaction: tx });
```

**参数：**

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|------|------|
| `memory.text` | `string` | 是 | 记忆内容 |
| `memory.category` | `string` | 否 | 类别类型 |
| `memory.importance` | `number` | 否 | 0-1 评分 |
| `memory.tags` | `array` | 否 | 标签字符串 |
| `memory.scope` | `string` | 否 | USER/AGENT/TEAM/GLOBAL |
| `memory.metadata` | `object` | 否 | 自定义数据 |
| `options.transaction` | `Transaction` | 否 | 事务上下文 |

**返回：** `string` - 记忆 ID

---

### searchMemories(query, options?)

混合搜索记忆。

```javascript
const results = await searchMemories("quarterly reports", {
  mode: "hybrid",
  topK: 10,
  vectorWeight: 0.7,
  bm25Weight: 0.3,
  scope: "USER",
  filters: {
    category: "fact",
    tags: ["work"]
  }
});
```

**参数：**

| 参数 | 类型 | 默认 | 描述 |
|-----------|------|------|------|
| `query` | `string` | 必需 | 搜索查询 |
| `options.mode` | `string` | `"hybrid"` | `"hybrid"`, `"bm25"`, `"vector"` |
| `options.topK` | `number` | `5` | 结果数量 |
| `options.vectorWeight` | `number` | `0.7` | 向量权重 |
| `options.bm25Weight` | `number` | `0.3` | BM25 权重 |
| `options.scope` | `string` | `null` | 范围过滤 |
| `options.filters` | `object` | `null` | 元数据过滤器 |

**返回：**
```javascript
{
  count: 3,
  query: "quarterly reports",
  mode: "hybrid",
  results: [
    {
      id: "mem_xxx",
      text: "Memory text",
      category: "fact",
      importance: 0.8,
      score: 0.923,
      tags: ["work"],
      created_at: "2026-04-15T10:00:00Z"
    }
  ]
}
```

---

### getAllMemories(options?)

带过滤器的列出所有记忆。

```javascript
const all = await getAllMemories({
  limit: 50,
  offset: 0,
  sortBy: "createdAt",
  sortOrder: "desc"
});
```

---

### getMemory(id)

按 ID 获取单个记忆。

```javascript
const memory = await getMemory("mem_xxx");
```

---

### updateMemory(id, updates, options?)

更新记忆的字段。

```javascript
await updateMemory("mem_xxx", {
  text: "Updated content",
  importance: 0.9
});
```

---

### deleteMemory(id, options?)

删除记忆。

```javascript
await deleteMemory("mem_xxx");
```

---

## 事务函数

### beginTransaction()

开始新事务。

```javascript
const tx = await beginTransaction();
try {
  await addMemory({ text: "Memory 1" }, { transaction: tx });
  await addMemory({ text: "Memory 2" }, { transaction: tx });
  await commitTransaction(tx);
} catch (error) {
  await rollbackTransaction(tx);
}
```

---

### commitTransaction(tx)

提交事务。

---

### rollbackTransaction(tx)

回滚事务。

---

## 实用函数

### getMemoryStats()

获取记忆统计。

```javascript
const stats = await getMemoryStats();
```

---

### memoryExport(params)

导出记忆到文件。

```javascript
await memoryExport({
  format: "json",
  output: "~/memories.json"
});
```

---

### memoryDedup(params)

查找并合并重复。

```javascript
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: true
});
```

---

## 固定函数

### pinMemory(id)

固定记忆（防止压缩/去重）。

```javascript
await pinMemory("mem_xxx");
```

---

### unpinMemory(id)

取消固定记忆。

```javascript
await unpinMemory("mem_xxx");
```

---

### getPinnedMemories()

列出所有固定的记忆。

```javascript
const pinned = await getPinnedMemories();
```

---

## 错误处理

```javascript
import { 
  addMemory, 
  MemoryValidationError, 
  StorageError 
} from 'unified-memory';

try {
  await addMemory({ text: "Test" });
} catch (error) {
  if (error instanceof MemoryValidationError) {
    console.error("Invalid memory:", error.field);
  } else if (error instanceof StorageError) {
    console.error("Storage failed:", error.message);
  }
}
```
