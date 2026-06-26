# 设计原则

> 指导 Unified Memory 开发的核心理架构原则。

## 🎯 设计理念

Unified Memory 建立在五个基本原则之上：

1. **可靠性第一** - 数据绝不能丢失
2. **默认性能** - 开箱即用的快速
3. **设计可扩展性** - 易于定制
4. **API 简洁性** - 易于学习和使用
5. **透明度** - 清楚数据如何流动

## 📜 原则 1: 可靠性第一

### 数据安全

每个写操作都受到保护：

```javascript
// 原子写入模式
async function atomicStore(memory) {
  const tx = await beginTransaction();
  try {
    await writeJson(memory);
    await writeVector(memory);
    await logToWAL(tx, memory);
    await commitTransaction(tx);
  } catch (error) {
    await rollbackTransaction(tx);
    throw error;
  }
}
```

### WAL 在数据库之前

WAL（预写日志）在任何数据更改之前写入：

1. 记录预期操作
2. 应用操作
3. 将日志条目标记为已提交
4. （可选）fsync 到磁盘

## ⚡ 原则 2: 默认性能

### 智能默认值

系统开箱即用：

| 设置 | 默认 | 原因 |
|------|------|------|
| 搜索模式 | 混合 | 最佳准确性 |
| 缓存 | 启用 | 快速重复查询 |
| 压缩 | 基于层级 | 平衡速度/存储 |
| 向量批处理 | 100 | 最佳吞吐量 |

## 🔌 原则 3: 设计可扩展性

### 插件钩子

每个操作都可以被拦截：

```javascript
const hooks = {
  beforeStore: [],
  afterStore: [],
  beforeSearch: [],
  afterSearch: []
};
```

### 关注点分离

```
工具层 → 服务层 → 存储层 → 基础设施
```

## 📐 模块设计规则

### 单一职责

每个模块有一项工作：

| 模块 | 职责 |
|------|------|
| `storage.js` | JSON 文件 CRUD |
| `vector.js` | 向量操作 |
| `bm25.js` | BM25 索引 |
| `fusion.js` | 结果融合 |
| `tools/*.js` | MCP 工具适配器 |

## 📚 下一步

- [模块](./modules.md) - 详细的模块参考
- [数据流](./data-flow.md) - 详细的数据流图
- [概述](./overview.md) - 系统架构
