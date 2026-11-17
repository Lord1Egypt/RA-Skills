# Skill 质量指南

一个好的 ThoughtCodec Skill 应该具体、可执行、双语化，并且可审核。

## 必要章节

每个正式 Skill 应包含：

- Frontmatter：`name`、`description`、`version`、`status`、`language`、`type` 和 `models`。
- 一级标题。
- 什么时候使用。
- Skill 所需输入。
- 分步骤工作流程。
- 输出约定。
- Codex 使用说明。
- Claude 使用说明。
- 边界与安全说明。
- 示例提示词。

## 写作原则

- 优先使用直接指令，而不是抽象建议。
- 明确说明假设。
- 让 Skill 的范围足够窄，确保可以稳定运行。
- 在容易误解的地方加入示例。
- 示例中不包含私人信息。
- 大型支撑材料放入 `references/`。
- 同时维护英文和简体中文版本。

## 状态等级

- `draft`：尚未完成，或仅作为模板材料，不应被视为已发布 Skill。
- `preview`：已经过发布前复核，可公开使用，但仍会通过真实使用继续迭代。
- `stable`：已在真实工作流中多次验证，预期变更较少。

ThoughtCodec 首批公开 Skill 使用 `preview`。这既说明内容已经可用、可审核，也保留后续迭代空间。

## 兼容性说明

ThoughtCodec 为双语 catalog 与发布流程保留了额外 frontmatter 字段。如果将某个 Skill 复制到 Codex 原生 Skill 目录中，至少保留 `name` 与可触发的 `description`；若目标运行时要求更严格的 frontmatter，可移除项目专用元数据。

## 审核清单

- 新读者能否理解什么时候使用这个 Skill？
- 输入要求是否清楚？
- 步骤是否有序且可执行？
- 输出格式是否明确？
- 是否在必要处说明 Codex 与 Claude 的差异？
- 是否说明边界情况或安全风险？
- catalog 条目是否与文件匹配？
