# Changelog

All notable changes to Session Guardian will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-03

### Added
- 五层防护体系：增量备份 + 快照 + 智能总结 + 健康检查 + 项目管理
- 计划文件机制：复杂任务状态管理（`scripts/plan-manager.sh`）
- Session 隔离检查：防止跨 session/跨渠道混淆（`scripts/session-isolation-check.sh`）
- GatewayRestart 强制恢复：自动恢复未完成任务
- 健康检查：自动清理过大 session 文件（>1MB）、修复配置、恢复任务
- 增量备份：每5分钟自动备份，最多丢失5分钟数据
- 快照备份：每小时完整备份，可恢复到任意时刻
- 智能总结：每日 AI 总结，提取关键对话、决策、成果
- 一键安装脚本：自动配置 crontab 和 OpenClaw cron
- 恢复脚本：支持从增量备份、快照、每日总结恢复
- 完整文档：SKILL.md、EXAMPLES.md、RELEASE-v1.0.md
- 使用示例：实战案例和常见问题解答

### Technical Details
- 基于 Lobster Studio 多智能体军团协作的实战经验
- 零 Token 成本（备份和快照不调用 LLM）
- 完全独立运行（使用系统 crontab）
- 自动清理和磁盘空间管理
- 向后兼容（未来版本升级无需修改配置）

[1.0.0]: https://github.com/cyber-axin/session-guardian/releases/tag/v1.0.0
