# Unified Memory 中文文档

[English](../en/index.md) · **中文**

欢迎来到 Unified Memory v5.2.0 中文文档。本文档提供 Unified Memory 系统的全面指南、API 参考和架构详情。

## 📚 文档结构

### 快速开始
- **[快速开始指南](./getting-started/quickstart.md)** - 5分钟上手
- **[安装指南](./getting-started/installation.md)** - 详细安装说明
- **[配置指南](./getting-started/configuration.md)** - 系统配置选项

### 使用指南
- **[基础使用](./guides/basic-usage.md)** - 日常操作和常见任务
- **[高级功能](./guides/advanced-features.md)** - 高级功能和优化
- **[插件系统](./guides/plugins.md)** - 使用插件扩展功能
- **[故障排除](./guides/troubleshooting.md)** - 解决常见问题

### API 文档
- **[API 概览](./api/overview.md)** - Unified Memory API 介绍
- **[存储 API](./api/storage-api.md)** - 记忆存储和检索操作
- **[向量 API](./api/vector-api.md)** - 向量搜索和相似度操作
- **[插件 API](./api/plugin-api.md)** - 插件开发和集成

### 架构设计
- **[架构概览](./architecture/overview.md)** - 系统设计和组件
- **[原子事务](./architecture/atomic-transactions.md)** - 数据一致性保证
- **[向量搜索](./architecture/vector-search.md)** - 搜索算法和优化
- **[插件系统](./architecture/plugin-system.md)** - 插件架构和设计

### 参考手册
- **[CLI 参考](./reference/cli-reference.md)** - 命令行接口文档
- **[配置参考](./reference/configuration.md)** - 完整配置选项
- **[更新日志](./reference/changelog.md)** - 版本历史和变更
- **[常见问题](./reference/faq.md)** - 常见问题解答
- **[贡献指南](./reference/contributing.md)** - 如何贡献项目

## 🎯 核心特性文档

### 原子数据一致性
- **两阶段提交协议**: 保证 JSON 和向量存储的原子性写入
- **事务恢复**: 自动恢复未完成的事务
- **fsync 保证**: 确保数据写入磁盘

### 高性能搜索
- **混合搜索**: BM25 + 向量 + RRF 融合获得最佳结果
- **优化算法**: 5-10倍查询性能提升
- **智能缓存**: 频繁查询的结果缓存

### 插件系统
- **同步桥梁**: 与 Workspace Memory 同步
- **统一查询**: 跨系统搜索接口
- **健康监控**: 实时系统监控

## 🔧 开发资源

### 代码示例


### 测试


### 构建


## 📖 阅读顺序

### 新用户
1. 从 **[快速开始指南](./getting-started/quickstart.md)** 开始
2. 阅读 **[基础使用](./guides/basic-usage.md)** 了解日常任务
3. 根据需要探索 **[高级功能](./guides/advanced-features.md)**

### 开发者
1. 查看 **[架构概览](./architecture/overview.md)**
2. 学习 **[原子事务](./architecture/atomic-transactions.md)** 了解数据一致性
3. 查阅 **[API 文档](./api/overview.md)** 进行集成

### 贡献者
1. 阅读 **[贡献指南](./reference/contributing.md)**
2. 理解 **[架构](./architecture/overview.md)**
3. 查看现有 **[代码示例](../shared/examples/)**

## 🔗 相关资源

### 外部链接
- **[GitHub 仓库](https://github.com/mouxangithub/unified-memory)** - 源代码和问题
- **[npm 包](https://www.npmjs.com/package/unified-memory)** - 包分发
- **[ClawHub 技能](https://clawhub.ai/)** - 技能市场

### 社区
- **[GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)** - 社区讨论
- **[问题跟踪器](https://github.com/mouxangithub/unified-memory/issues)** - bug 报告和功能请求
- **[贡献指南](./reference/contributing.md)** - 如何贡献

## 📄 许可证

本文档是 Unified Memory 项目的一部分，采用 MIT 许可证。详见 [LICENSE](https://github.com/mouxangithub/unified-memory/blob/main/LICENSE) 文件。

## 🤝 贡献文档

我们欢迎贡献来改进本文档！请查看我们的 [贡献指南](./reference/contributing.md) 了解如何：

1. 报告文档问题
2. 提出改进建议
3. 提交文档更新
4. 翻译文档

## 📞 支持

- **文档问题**: 在 [GitHub](https://github.com/mouxangithub/unified-memory/issues) 上提出问题
- **问题**: 使用 [GitHub Discussions](https://github.com/mouxangithub/unified-memory/discussions)
- **Bug**: 通过 [问题跟踪器](https://github.com/mouxangithub/unified-memory/issues) 报告

---

**最后更新**: 2026-04-15  
**版本**: v5.2.0  
**文档版本**: 1.0.0  

[← 返回主文档](../README_CN.md)
