# Unified Memory Architect Skill

> 梦境记忆系统重构与发布技能 - OpenClaw Agent Platform

## 技能概述

Unified Memory Architect 是一个高效的梦境记忆管理系统，为 OpenClaw Agent 提供强大的记忆存储、检索和关联能力。

**版本**: 1.0.0  
**作者**: OpenClaw Team  
**平台**: OpenClaw Agent Platform >= 2.7.0

## 核心能力

### 1. 记忆存储
- **1760个梦境记忆** - 海量记忆存储
- **7层目录结构** - 清晰的数据组织
- **60%存储节省** - 高效的数据压缩

### 2. 智能索引
- **49个语义标签** - 自动标签提取
- **181个实体识别** - 实体自动识别
- **多层索引** - 按类型/日期/标签/情感/语言/实体

### 3. 高速检索
- **5-10倍加速** - 混合搜索技术
- **BM25 + 向量 + RRF** - 多算法融合
- **毫秒级响应** - 优化的查询性能

## 使用方式

### CLI 命令

```bash
# 查看统计
node memory/scripts/query.cjs stats

# 按标签查询
node memory/scripts/query.cjs tag reflection 5

# 按日期查询
node memory/scripts/query.cjs date 2026-04-12 3

# 全文搜索
node memory/scripts/query.cjs search "关键词" 3

# 按情感查询
node memory/scripts/query.cjs sentiment neutral 2
```

### 编程接口

```javascript
const memory = require('./memory/scripts/query.cjs');

// 获取统计
const stats = memory.getStats();

// 按标签查询
const byTag = memory.queryByTag('reflection', 10);

// 按日期查询
const byDate = memory.queryByDate('2026-04-12', 10);

// 全文搜索
const search = memory.searchMemories('关键词', 10);

// 按情感查询
const bySentiment = memory.queryBySentiment('neutral', 10);
```

## 性能指标

| 指标 | 数值 |
|------|------|
| 总记忆数 | 1760 |
| 唯一标签 | 49 |
| 唯一实体 | 181 |
| 检索加速 | 5-10x |
| 存储节省 | 60% |

## 系统要求

- Node.js >= 14.0.0
- 磁盘空间 >= 100MB
- 内存 >= 512MB

## 相关文档

- [用户指南](docs/USER_GUIDE.md)
- [API文档](docs/API.md)
- [架构设计](docs/ARCHITECTURE.md)
- [快速开始](docs/QUICKSTART.md)
- [常见问题](docs/FAQ.md)
- [故障排除](docs/TROUBLESHOOTING.md)

## 发布信息

- **GitHub**: https://github.com/openclaw/unified-memory-architect
- **License**: MIT
- **Changelog**: [CHANGELOG](github/CHANGELOG.md)
