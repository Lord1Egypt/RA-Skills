# 用户指南

## 系统概述

Unified Memory 文档整理与发布系统是一个高效的梦境记忆管理系统，支持海量记忆存储、智能标签、多层索引和高速检索。

## 核心功能

### 1. 记忆查询

系统支持多种查询方式：

#### 按标签查询
```bash
node memory/scripts/query.cjs tag reflection 10
```

常用标签：
- `dream` - 梦境条目
- `reflection` - 反思内容
- `memory` - 记忆相关
- `water` - 水相关意象
- `mirror` - 镜子意象
- `technology` - 技术相关
- `sentiment:positive` - 积极情感
- `sentiment:negative` - 消极情感

#### 按日期查询
```bash
node memory/scripts/query.cjs date 2026-04-12 20
```

#### 全文搜索
```bash
node memory/scripts/query.cjs search "关键词" 10
```

#### 情感查询
```bash
node memory/scripts/query.cjs sentiment positive 5
```

### 2. 编程接口

```javascript
const query = require('./memory/scripts/query.cjs');

// 获取所有统计
const stats = query.getStats();

// 按标签查询
const byTag = query.queryByTag('reflection', 10);

// 按日期查询
const byDate = query.queryByDate('2026-04-12', 10);

// 全文搜索
const search = query.searchMemories('关键词', 10);

// 按情感查询
const bySentiment = query.queryBySentiment('neutral', 10);
```

### 3. 数据统计

```bash
# 查看完整统计
node memory/scripts/query.cjs stats
```

统计内容包括：
- 总记忆数
- 唯一标签数
- 唯一实体数
- 按类型分布
- 按日期分布
- 按标签分布
- 按情感分布
- 按语言分布

## 高级功能

### 自定义分析

编辑 `scripts/enhance-tags.cjs` 添加自定义分析逻辑：

```javascript
const customAnalyzer = {
  analyze(text) {
    return {
      tags: extractCustomTags(text),
      entities: extractCustomEntities(text),
      sentiment: analyzeSentiment(text)
    };
  }
};
```

### 批量导入

```bash
# 重新导入记忆
node memory/scripts/import-memories.cjs
```

### 系统验证

```bash
# 验证系统完整性
node memory/scripts/verify-system.cjs
```

## 最佳实践

1. **定期清理**: 每月运行 `cleanup.cjs` 归档旧数据
2. **索引更新**: 重要数据变更后运行 `enhance-tags.cjs`
3. **备份数据**: 定期备份 `processed/` 目录
4. **监控统计**: 定期检查 `stats` 接口确保数据健康

## 故障处理

详见 [故障排除指南](TROUBLESHOOTING.md)
