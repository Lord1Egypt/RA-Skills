## [2.102.9] - 2026-07-09

### 修复
- **displayName 统一为 kebab-case**：ClawHub/SkillHub 发布的显示名与技能名一致（），废除驼峰格式

## [2.102.8] - 2026-07-09
## [2.102.8] - 2026-07-03

### 修复
- 修复: `structure_checker.py` C-13 索引表检查仅匹配 `references/` 前缀的表格行，漏检 `scripts/` 等非 references 条目。新增 EXTRA 检查：索引表中所有文件路径必须以 `references/` 开头，否则报 WARN

## [2.102.7] - 2026-07-03

### 修复
- 修复: `fix.py` `fix_section_trigger()` 在 auto-fix 生成的触发词前硬加"用户需要"前缀，导致 auto-fix→audit→refix 非收敛循环。改为直接使用采集到的触发词原文（来自脚本 docstring / frontmatter / description），不再前缀"用户需要"

## [2.102.6] - 2026-07-03

## [2.102.5] - 2026-07-03

### 修复
- 修复: `body.json` 在 约束 章节同义词中添加「能力边界」「能力边界与限制」「能力与边界」，使 C-11 不再误报这些常用章节名

## [2.102.4] - 2026-07-03

### 修复
- 修复: `structure_checker.py` R-23 路径解析使用源文件目录而非 skill_dir（`references/` 下的路径应相对 source file 目录解析，而不是从 skill_dir 解析）
- 修复: `fix.py` `fix_section_workflow()` 在 ## 工作流程 已有自定义内容时跳过覆盖（避免每次 refactor --continue 销毁已有的工作流表格和门禁表）

## [2.102.3] - 2026-07-01

### 修复
- 修复: `fix_progressive_index_table()` 在替换索引表时会丢失 SKILL.md 中已有的人工填写内容。新增 `existing_rows` 保留机制：先读取现有表格行内容，仅对新文件调用 STANDARDIZED 或 auto-generate，已有行保持原有 4 列内容不变。
