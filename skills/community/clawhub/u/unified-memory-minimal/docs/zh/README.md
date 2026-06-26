# Unified Memory 文档

> 🧠 企业级记忆管理系统，支持混合搜索、原子事务和插件架构

[![版本](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/mouxangithub/unified-memory)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-green.svg)](https://nodejs.org/)
[![许可证: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 快速链接

| 我想... | 查看 |
|---------|------|
| 快速开始 | [快速入门](./getting-started/quickstart.md) |
| 安装系统 | [安装指南](./getting-started/installation.md) |
| 配置设置 | [配置指南](./getting-started/configuration.md) |
| 学习基础使用 | [基础使用](./guides/basic-usage.md) |
| 探索高级功能 | [高级使用](./guides/advanced-usage.md) |
| 开发插件 | [插件开发](./guides/plugins.md) |
| 集成到我的应用 | [集成指南](./guides/integration.md) |
| 理解架构 | [架构概述](./architecture/overview.md) |
| 查找API参考 | [API参考](./api/overview.md) |
| 排查问题 | [故障排除](./reference/troubleshooting.md) |

## ✨ 核心特性

### 🔍 混合搜索
Unified Memory 结合多种搜索算法以获得最佳相关性：
- **BM25**：传统关键词搜索
- **向量搜索**：使用嵌入的语义相似度
- **RRF（倒数排名融合）**：组合多个排名器的结果

### ⚡ 原子事务
企业级数据一致性：
- **WAL（预写日志）**：崩溃恢复保证
- **两阶段提交**：JSON 和向量存储的原子写入
- **fsync 保证**：数据写入磁盘，防止丢失

### 🔌 插件系统
支持热重载的可扩展架构：
- **生命周期钩子**：操作前后的钩子
- **同步桥接**：连接外部记忆系统
- **自定义处理器**：添加自定义记忆处理

### 📊 性能
针对生产工作负载优化：
- **搜索速度提升 5-10 倍**（优化的向量引擎）
- **存储减少 60%**（智能压缩）
- **缓存命中率 78%**（语义缓存）
- **平均查询时间 45ms**

## 📦 快速开始

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/mouxangithub/unified-memory/main/install.sh | bash

# 存储记忆
unified-memory add "Remember to review quarterly reports" --tags work,reminder

# 搜索记忆
unified-memory search "quarterly reports"

# 使用 JavaScript API
node -e "
const { addMemory, searchMemories } = require('unified-memory');
(async () => {
  await addMemory({ text: 'My preference for morning meetings', tags: ['preference'] });
  const results = await searchMemories('meeting schedule');
  console.log(results);
})();
"
```

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    客户端应用程序                           │
│          (OpenClaw, Web UI, CLI, API, MCP 客户端)          │
└───────────────────────────┬─────────────────────────────────┘
                            │ 调用 MCP 工具
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API 网关层                                │
│           (REST API, MCP 服务器, WebSocket)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    服务层                                    │
│     (记忆服务, 搜索服务, 缓存服务)                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    存储层                                    │
│        (SQLite, 向量数据库, 文件系统)                        │
└─────────────────────────────────────────────────────────────┘
```

## 📚 文档章节

### 入门指南
- [快速入门](./getting-started/quickstart.md) - 5分钟介绍
- [安装](./getting-started/installation.md) - 完整安装指南
- [配置](./getting-started/configuration.md) - 配置选项

### 用户指南
- [基础使用](./guides/basic-usage.md) - 核心操作
- [高级使用](./guides/advanced-usage.md) - 高级功能
- [插件开发](./guides/plugins.md) - 构建插件
- [集成](./guides/integration.md) - 连接到其他系统

### 架构
- [概述](./architecture/overview.md) - 系统设计
- [设计原则](./architecture/design-principles.md) - 关键原则
- [模块](./architecture/modules.md) - 模块参考
- [数据流](./architecture/data-flow.md) - 数据如何流经系统

### API 参考
- [概述](./api/overview.md) - API 介绍
- [核心 API](./api/core-api.md) - 核心函数
- [MCP 工具](./api/mcp-tools.md) - MCP 工具参考
- [插件 API](./api/plugin-api.md) - 插件开发

### 参考
- [配置参考](./reference/configuration.md) - 所有配置选项
- [故障排除](./reference/troubleshooting.md) - 常见问题
- [FAQ](./reference/faq.md) - 常见问题

## 🔧 开发

```bash
# 克隆并设置
git clone https://github.com/mouxangithub/unified-memory.git
cd unified-memory
npm install

# 运行测试
npm test

# 构建生产版本
npm run build
```

## 🤝 贡献

欢迎贡献！请在提交 PR 之前阅读我们的[贡献指南](./contributing/guidelines.md)。

## 📄 许可证

MIT 许可证 - 请参阅 [LICENSE](../../LICENSE) 文件了解详情。

## 📞 支持

- [GitHub Issues](https://github.com/mouxangithub/unified-memory/issues)
- [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)

---

**版本**: 5.2.0 | **最后更新**: 2026-04-20
