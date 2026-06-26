# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-03-20

### Added
- LibSQL 存储层（替代 sql.js）
- 语义搜索（向量相似度搜索）
- AI 增强（自动摘要、标签生成）
- 本地嵌入支持（@huggingface/transformers）
- 混合搜索（语义 70% + 关键词 30%）
- 统计命令 `/统计`
- 支持 OpenAI 和本地嵌入模型切换

### Changed
- 全面异步化改造
- 统一使用异步 API
- 优化搜索回退逻辑

### Fixed
- 搜索输入截断 bug
- 关键字"搜"的解析问题

## [1.0.0] - 2026-03-19

### Added
- 初始版本
- 基础笔记记录功能
- 关键词搜索
- 版本管理（自动保存 + 手动标记）
- Markdown 导出
- OpenClaw Skill 集成

---

## 版本规划

### [1.3.0] - 计划中

- embedjs 完整集成
- 数据迁移脚本
- 单元测试

### [2.0.0] - 未来

- WebDAV 同步
- 网页抓取（readability）
- PDF 处理
- Yjs 实时同步
- Web 画布界面
