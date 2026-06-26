# Changelog

## [0.3] - 2026-03-06 20:47 (Asia/Shanghai)

### Changed
- 目标发布名调整为英文：`Session Cleanup Pro`。
- 优化 `description` 为中英双语，信息更完整。
- `metadata.version` 升级至 `0.3`，并更新 `updatedAt`。

## [0.2] - 2026-03-06 20:34 (Asia/Shanghai)

### Added
- 新增 `scripts/scan_sessions.sh`，提供确定性扫描能力。
- 新增 `references/policy.md`，明确清理策略与确认流程。

### Changed
- 重构 SKILL 工作流为：scan → confirm → apply。
- 强化 72 小时保护规则与当前会话永不删除规则。
- `metadata` 增加 `version` 与 `updatedAt`。

## [0.1] - 2026-03-06 20:10 (Asia/Shanghai)

### Added
- 初版 `session-cleanup` 技能。
- 支持识别孤儿 `.jsonl` 与过期会话。
