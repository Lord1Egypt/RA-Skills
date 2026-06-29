# Changelog

All notable changes to this project will be documented in this file.

## [2.0.16-beta] - 2026-06-28

### Fixed

- **P0 - 硬编码路径问题**：`save_content_hints_to_outline` 硬编码 `~/.openclaw/workspace` 路径，导致 THESIS_WORKSPACE 环境变量不生效。改用 `_get_state_path()` 统一路径计算。
- **P1 - 嵌套结构兼容层**：新增 `_get_outline_nodes()` / `_set_outline_nodes()` 两个 helper 函数，统一处理 3 种历史嵌套结构：
  - 结构 A: `state["outline"]["outline_tree"]["nodes"]` （期望结构）
  - 结构 B: `state["outline"]["nodes"]` （简化结构）
  - 结构 C: `state["outline"]["outline"]["outline_tree"]["nodes"]` （旧版嵌套）
- **P1 - 19 处硬编码替换**：state_manager_v2 (7处) + orchestrator_v2 (10处) + outline_parser (2处) 的 `state["outline"]["outline_tree"]["nodes"]` 全部替换为 `_get_outline_nodes(state)`
- **P1 - 隐藏 bug 修复**：`_set_outline_nodes` 中 `if not state` 改为 `if state is None`，修复空 dict `{}` 作为 falsy 值导致函数直接 return 的问题
- **P1 - 防御性压平逻辑**：`outline_save` 写盘前自动将 C 结构压平为 A 结构，保证磁盘持久化为标准结构

### Technical

- 新增 helper：`state_manager_v2._get_outline_nodes()` / `_set_outline_nodes()`
- orchestrator_v2.py 新增导入：`_get_outline_nodes`
- outline_parser.py 新增导入：`_get_state_path`, `_get_outline_nodes`, `_set_outline_nodes`
- `save_content_hints_to_outline` 重写：约 20 行（读+写统一走 helper）
