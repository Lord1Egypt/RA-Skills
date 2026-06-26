# 用户指南

> 深入指南，有效使用 Unified Memory。

## 📋 本节指南

| 指南 | 描述 | 级别 |
|------|------|------|
| [基础使用](./basic-usage.md) | 核心操作：存储、搜索、列出、删除 | 初级 |
| [高级使用](./advanced-usage.md) | 版本控制、去重、导出、画像 | 中级 |
| [插件开发](./plugins.md) | 构建自定义插件 | 高级 |
| [集成](./integration.md) | 连接到其他系统 | 中级 |

## 🎯 选择您的路径

**初次接触 Unified Memory？**
从[基础使用](./basic-usage.md)开始，学习核心操作。

**想要扩展功能？**
了解[插件开发](./plugins.md)来构建自定义插件。

**需要与现有系统集成？**
查看[集成指南](./integration.md)获取连接器和 API。

## 📚 前置条件

阅读这些指南之前，您应该：
- 完成[快速入门教程](../getting-started/quickstart.md)
- 安装并运行 Unified Memory
- 了解基本的 JavaScript/TypeScript（用于 API 指南）

## 🔧 常见操作

### 存储记忆
```javascript
// 基本存储
await addMemory({ text: "重要笔记", tags: ["work"] });

// 带元数据
await addMemory({
  text: "下午3点开会",
  category: "fact",
  importance: 0.9,
  tags: ["meeting"],
  metadata: { participants: ["Alice", "Bob"] }
});
```

### 搜索记忆
```javascript
// 简单搜索
const results = await searchMemories("会议笔记");

// 混合搜索
const results = await searchMemories("项目更新", {
  mode: "hybrid",
  vectorWeight: 0.7,
  bm25Weight: 0.3
});
```

### 管理记忆
```javascript
// 列出所有
const all = await getAllMemories();

// 按 ID 获取
const memory = await getMemory(memoryId);

// 删除
await deleteMemory(memoryId);
```

## 🚀 快速链接

- [API 参考](../api/overview.md) - 完整的 API 文档
- [架构](../architecture/overview.md) - 系统设计
- [配置](../getting-started/configuration.md) - 配置选项
- [故障排除](../reference/troubleshooting.md) - 常见问题
