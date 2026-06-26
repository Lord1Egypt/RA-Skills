# 基础使用指南

> 学习核心操作：存储、搜索、列出和删除记忆。

## 📚 目录

1. [添加记忆](#-添加记忆)
2. [搜索记忆](#-搜索记忆)
3. [列出记忆](#-列出记忆)
4. [获取单个记忆](#-获取单个记忆)
5. [更新记忆](#-更新记忆)
6. [删除记忆](#-删除记忆)
7. [记忆元数据](#-记忆元数据)

## ➕ 添加记忆

### 基本添加
```javascript
const { addMemory } = require('unified-memory');

const memoryId = await addMemory({
  text: "Remember to call the client tomorrow"
});
```

### 完整选项
```javascript
const memoryId = await addMemory({
  text: "User prefers Python for data analysis",
  category: "preference",
  importance: 0.85,
  tags: ["python", "preference", "data"],
  scope: "USER",
  source: "extraction",
  metadata: {
    project: "analytics",
    confidence: 0.9
  }
});
```

### 添加参数

| 参数 | 类型 | 默认 | 描述 |
|------|------|------|------|
| `text` | `string` | **必填** | 记忆内容 |
| `category` | `string` | `"general"` | 类别类型 |
| `importance` | `number` | `0.5` | 重要性 0-1 |
| `tags` | `array` | `[]` | 标签字符串数组 |
| `scope` | `string` | `null` | 范围：USER, AGENT, TEAM, GLOBAL |
| `source` | `string` | `"manual"` | 来源：manual, auto, extraction |
| `metadata` | `object` | `{}` | 自定义键值数据 |

### 记忆类别

| 类别 | 何时使用 |
|------|----------|
| `preference` | 用户偏好、喜好、厌恶 |
| `fact` | 关于世界的事实信息 |
| `decision` | 做出的决定，得到的结论 |
| `entity` | 人、组织、地点 |
| `reflection` | 想法、意见、洞察 |
| `general` | 其他记忆的默认类别 |

## 🔍 搜索记忆

### 简单搜索
```javascript
const { searchMemories } = require('unified-memory');

const results = await searchMemories("quarterly reports");
```

### 搜索选项
```javascript
const results = await searchMemories("project update", {
  mode: "hybrid",      // "hybrid", "bm25", 或 "vector"
  topK: 10,            // 结果数量
  vectorWeight: 0.7,    // 向量搜索权重 (0-1)
  bm25Weight: 0.3,     // BM25 搜索权重 (0-1)
  scope: "USER",       // 按范围过滤
  filters: {
    category: "fact",
    tags: ["work"],
    minImportance: 0.5
  }
});
```

### 搜索响应
```javascript
{
  count: 3,
  query: "quarterly reports",
  mode: "hybrid",
  results: [
    {
      id: "mem_xxx",
      text: "Quarterly reports due on Friday",
      category: "fact",
      importance: 0.9,
      score: 0.923,
      tags: ["work", "deadline"],
      created_at: "2026-04-15T10:00:00Z"
    }
  ]
}
```

### 搜索模式

| 模式 | 描述 | 适用于 |
|------|------|--------|
| `hybrid` | BM25 + 向量 + RRF | 一般使用 |
| `bm25` | 仅关键词 | 精确匹配 |
| `vector` | 仅语义 | 概念匹配 |

## 📋 列出记忆

### 列出所有
```javascript
const { getAllMemories } = require('unified-memory');

const allMemories = await getAllMemories();
```

### 带过滤器的列表
```javascript
const memories = await getAllMemories({
  limit: 50,
  offset: 0,
  sortBy: "createdAt",
  sortOrder: "desc",
  filters: {
    category: "preference",
    tags: ["work"],
    scope: "USER"
  }
});
```

## 🔎 获取单个记忆

```javascript
const { getMemory } = require('unified-memory');

const memory = await getMemory("mem_xxx");
```

## ✏️ 更新记忆

```javascript
const { updateMemory } = require('unified-memory');

await updateMemory("mem_xxx", {
  text: "Updated memory content"
});
```

## 🗑️ 删除记忆

```javascript
const { deleteMemory } = require('unified-memory');

await deleteMemory("mem_xxx");
```

## 🏷️ 记忆元数据

```javascript
await addMemory({
  text: "Meeting with John",
  metadata: {
    date: "2026-04-20",
    location: "Conference Room A",
    participants: ["John", "Alice"]
  }
});
```

## 📚 下一步

- [高级使用](./advanced-usage.md) - 版本控制、去重、导出
- [插件开发](./plugins.md) - 用插件扩展
- [API 参考](../api/overview.md) - 完整的 API 文档
