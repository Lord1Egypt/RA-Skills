# 高级使用指南

> 高级功能：版本控制、去重、导出、画像等。

## 📚 目录

1. [版本控制](#-版本控制)
2. [去重](#-去重)
3. [导出与导入](#-导出与导入)
4. [记忆画像](#-记忆画像)
5. [偏好管理](#-偏好管理)
6. [层级管理](#-层级管理)

## 🔄 版本控制

### 列出版本
```javascript
const { memoryVersion } = require('unified-memory');

const versions = await memoryVersion({
  action: "list",
  memoryId: "mem_xxx",
  limit: 10
});
```

### 比较版本
```javascript
const diff = await memoryVersion({
  action: "diff",
  memoryId: "mem_xxx",
  versionId1: "v1",
  versionId2: "v2"
});
```

### 恢复版本
```javascript
await memoryVersion({
  action: "restore",
  memoryId: "mem_xxx",
  versionId: "v1"
});
```

## 🔀 去重

### 查找重复（试运行）
```javascript
const { memoryDedup } = require('unified-memory');

const duplicates = await memoryDedup({
  threshold: 0.85,
  dryRun: true
});
```

### 合并重复
```javascript
const result = await memoryDedup({
  threshold: 0.85,
  dryRun: false
});
```

## 📤 导出

```javascript
const { memoryExport } = require('unified-memory');

// 导出为 JSON
await memoryExport({
  format: "json",
  output: "~/exports/memories.json"
});

// 导出为 Markdown
await memoryExport({
  format: "markdown",
  output: "~/exports/memories.md"
});

// 导出为 CSV
await memoryExport({
  format: "csv",
  output: "~/exports/memories.csv"
});
```

## 👤 记忆画像

```javascript
const { memoryProfile } = require('unified-memory');

const profile = await memoryProfile({
  scope: "user",
  container_tag: "project-x",
  static_days: 30,
  limit: 100
});
```

## ❤️ 偏好管理

### 获取偏好
```javascript
const pref = await memoryPreference({
  action: "get",
  key: "meeting_preference"
});
```

### 设置偏好
```javascript
await memoryPreference({
  action: "set",
  key: "preferred_language",
  value: "Python",
  confidence: 0.9
});
```

### 合并偏好
```javascript
await memoryPreference({
  action: "merge",
  slots: {
    language: { value: "TypeScript", confidence: 0.9 },
    editor: { value: "VS Code", confidence: 0.95 }
  }
});
```

## 📊 层级管理

### 检查层级状态
```javascript
const status = await memoryTier({ action: "status" });
```

### 迁移到层级
```javascript
await memoryTier({
  action: "migrate",
  memories: [{ id: "mem_xxx", targetTier: "COLD" }],
  apply: true
});
```

### 层级阈值

| 层级 | 年龄 | 压缩 | 可去重 |
|------|------|------|--------|
| HOT | ≤ 7 天 | 无 | 是 |
| WARM | 7-30 天 | 轻度 | 是 |
| COLD | > 30 天 | 重度 | 是 |

## 📚 下一步

- [插件开发](./plugins.md) - 构建自定义插件
- [集成指南](./integration.md) - 连接到其他系统
- [API 参考](../api/overview.md) - 完整的 API 文档
