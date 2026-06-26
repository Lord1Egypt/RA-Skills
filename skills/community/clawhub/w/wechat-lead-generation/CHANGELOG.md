# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-26

### Added
- 初始版本发布
- 微信多渠道数据抓取（好友/群聊/朋友圈/公众号）
- 客户意向分析（关键词 + 意图识别）
- 线索评分系统（0-100 分）
- 自动回复生成（可选，支持自定义模板）
- Markdown 报告输出（微信友好格式）
- agentmemory 历史存储
- 完整文档（SKILL.md, README.md, Requirements.md）
- MIT 许可证

### Fixed
- N/A (initial release)

### Known Issues
- 模拟数据层（真实微信抓取待集成）
- 未集成真实 LLM 深度分析
- 缺乏 CI/CD 自动化测试
- 未上架 ClawHub（等待 PR 审核）

## [Planned] - Upcoming

### v0.2.0
- [ ] 真实微信抓取（wechat-md-publish 集成）
- [ ] LLM 深度分析（生成客户画像）
- [ ] 多账号轮询支持

### v0.3.0
- [ ] 可视化 HTML 报告
- [ ] CRM 导出（CSV / API）
- [ ] 定时任务向导

### v1.0.0
- [ ] 完整测试覆盖
- [ ] CI/CD 流水线
- [ ] ClawHub 上架
