# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-04-23

### Added
- `metadata.name` 字段（clawhub 识别必需）
- `SKILL.md` 精简重组，移除与 MATERIAL_PACKING.md 的重复内容

### Changed
- `SKILL.md`：全面精简（9768→4262字节），保留核心操作文档
- `README.md`：精简为快速入口文档
- `migrate.py`：修复选项1 bug（找workspace逻辑写错，candidates循环里写成死代码）

### Fixed
- `SKILL.md` 的 `metadata.name` 从 `team-resurrection` 修正为 `quick-resurrection`（与 clawhub slug 一致）

### Removed
- `MATERIAL_PACKING.md`：内容70%与SKILL.md重复，已废弃

---

## [1.0.0] - 2026-04-22

- 初始版本：pack.py + migrate.py
- 支持有/无团队的通用化检测
- Main Agent 三个选项（选项1/2 当时执行逻辑残缺）
