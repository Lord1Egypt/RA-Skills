# Changelog

All notable changes to `thesis-docx-export` are documented in this file.

## [1.0.0] - 2026-07-02

### Added
- 从 `thesis-workflow-v2` Phase 5.2 段拆出独立 skill
- `scripts/md2docx_strict.py`（软链接 → 主 skill 真身）
- `scripts/loop_self_check.py`（软链接 → 主 skill 真身）
- `references/checklist.md`（18 项格式规范 + 10 项 Guardrails 校验项 + Phase 退出门禁，从主 skill 真身迁移至此）

### Notes
- 本 skill 是 `thesis-workflow-v2` 的下游模块，主 skill 通过 `references/loop-design.md` 的 Phase 5.2 段引用本 skill
- Python 脚本采用软链接方式共享主 skill 真身，避免代码 drift
- 如果发现 `loop_self_check.py` 或 `md2docx_strict.py` 的 bug，请直接修改主 skill `scripts/` 目录下的真身文件
