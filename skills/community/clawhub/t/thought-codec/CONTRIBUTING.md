# Contributing / 贡献指南

Thank you for helping improve ThoughtCodec.

感谢你帮助改进 ThoughtCodec。

## Contribution Types / 贡献类型

- Add or improve a skill.
- Improve bilingual documentation.
- Improve examples, diagrams, or release checklists.
- Improve validation scripts.
- Report unclear instructions, broken links, or missing safety boundaries.

你可以贡献：

- 新增或改进 Skill。
- 改进中英双语文档。
- 改进示例、图表或发布清单。
- 改进校验脚本。
- 反馈不清晰的说明、失效链接或缺失的安全边界。

## Add A Skill / 新增 Skill

Use this structure:

```text
skills/<skill-id>/
|-- SKILL.md
|-- SKILL.zh-CN.md
|-- assets/
|-- examples/
`-- references/
```

Rules:

- Use lowercase kebab-case for `skill-id`.
- Add English and Simplified Chinese versions.
- Add the skill to `catalog/skills.json`.
- Keep examples fictional or generic.
- Run `bash scripts/validate_structure.sh`.

规则：

- `skill-id` 使用小写 kebab-case。
- 同时提供英文和简体中文版本。
- 将 Skill 写入 `catalog/skills.json`。
- 示例使用虚构或通用数据。
- 运行 `bash scripts/validate_structure.sh`。

## Quality Bar / 质量标准

A good skill should be specific, executable, and reviewable. It should include when to use it, required inputs, workflow, output format, boundaries, and examples.

一个好的 Skill 应该具体、可执行、可审核。它应包含使用场景、输入要求、工作流程、输出格式、边界和示例。

## Privacy / 隐私

Do not include private emails, tokens, API keys, client data, private transcripts, or proprietary content.

不要提交私人邮箱、token、API key、客户数据、私人对话原文或专有内容。
