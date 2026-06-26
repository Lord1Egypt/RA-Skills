# 变更日志

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-17

### Added
- ✨ 添加 token 估算功能（准确计算压缩率）
- ✨ 添加 `--dry-run` 预览模式（压缩前预览效果）
- ✨ 添加自动备份清理（保留最近7天）
- ✨ 添加配置文件权限检查（安全性提升）
- ✨ 优化压缩提示词（添加few-shot示例）

### Fixed
- 🐛 修复测试用例导入错误（`load_config` → `load_openclaw_config`）
- 🐛 修复压缩率计算不准确（现在基于token而非字节）

### Improved
- 📈 压缩效果显示更详细（同时显示字符和token压缩率）
- 📝 文档更新（添加预览模式使用说明）
- 🔒 安全性提升（检查配置文件权限）

## [1.0.0] - 2026-03-17

### Added
- 初始版本发布
- 三层索引体系（任务层/记忆层/内容层）
- 会话摘要压缩功能（92% token 节省）
- 自动判断机制（continue/compress/new_session）
- 任务隔离机制
- 支持多种 AI 提供商（OpenAI, Anthropic, Volcengine, DeepSeek）
- 配置文件支持（~/.openclaw/token-optimizer.json）
- 环境变量配置支持
- 单元测试覆盖

### Features
- `session_guard.py` - 会话健康度自动判断
- `compress_session.py` - 会话摘要压缩
- `new_session.py` - 初始化新会话
- `status.py` - 显示当前状态

### Documentation
- 完整的 README.md
- 详细的使用说明
- 故障排查指南

---

## [计划中]

### v1.2.0
- [ ] 压缩质量验证（检查关键信息是否丢失）
- [ ] 进度提示（压缩时显示进度条）
- [ ] 缓存机制（避免重复压缩相同内容）

### v2.0.0
- [ ] 可视化仪表板
- [ ] 多种压缩策略（激进/保守/平衡）
- [ ] Web 界面
- [ ] API 服务