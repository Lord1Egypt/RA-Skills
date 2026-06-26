# API 参考概述

> Unified Memory API 和 MCP 工具的完整参考。

## 🚀 快速参考

### 核心函数

```javascript
// 记忆操作
addMemory(memory)         // 存储新记忆
getMemory(id)            // 按 ID 获取
getAllMemories(options)  // 带过滤器的列表
updateMemory(id, updates) // 更新字段
deleteMemory(id)          // 删除记忆

// 搜索
searchMemories(query, options)  // 混合搜索
getMemoryStats()                // 统计

// 事务
beginTransaction()      // 开始事务
commitTransaction(tx)   // 提交更改
rollbackTransaction(tx) // 回滚更改
```

## 🔧 MCP 工具快速索引

| 工具 | 描述 |
|------|------|
| `memory_search` | 混合搜索 |
| `memory_store` | 存储记忆 |
| `memory_list` | 列出记忆 |
| `memory_delete` | 删除记忆 |
| `memory_compose` | 组合提示上下文 |
| `memory_profile` | 用户画像 |
| `memory_preference` | 偏好 |
| `memory_version` | 版本控制 |
| `memory_export` | 导出记忆 |
| `memory_dedup` | 去重 |
| `memory_tier` | 层级管理 |
| `memory_pin` | 固定/取消固定 |
| `memory_stats` | 统计 |
| `memory_health` | 健康检查 |
| `memory_metrics` | 指标 |

## 📚 下一步

- [MCP 工具参考](./mcp-tools.md) - 所有工具参数
- [核心 API 参考](./core-api.md) - SDK 函数
- [插件 API 参考](./plugin-api.md) - 插件钩子
