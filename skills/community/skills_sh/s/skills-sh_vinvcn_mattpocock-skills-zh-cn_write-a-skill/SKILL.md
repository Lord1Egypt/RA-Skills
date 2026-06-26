---
name: write-a-skill
description: 创建结构正确、支持 progressive disclosure 并带 bundled resources 的新 agent skills。Use when user wants to create, write, or build a new skill.
---

# Writing Skills

## Process

1. **Gather requirements** — 询问用户：
   - skill 覆盖什么 task/domain？
   - 应处理哪些具体 use cases？
   - 需要 executable scripts，还是只需要 instructions？
   - 是否有 reference materials 要包含？

2. **Draft the skill** — 创建：
   - 带 concise instructions 的 SKILL.md
   - 如果内容超过 500 行，创建 additional reference files
   - 如果需要 deterministic operations，创建 utility scripts

3. **Review with user** — 展示 draft 并询问：
   - 是否覆盖你的 use cases？
   - 是否缺失或不清楚？
   - 是否有 section 应更详细或更简短？

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

description 是 agent 决定是否加载 skill 时**唯一看到的内容**。它会和其他 installed skills 一起出现在 system prompt 中。agent 会读取这些 descriptions，并根据用户请求选择相关 skill。

**Goal**：给 agent 足够信息，让它知道：

1. 这个 skill 提供什么 capability
2. 何时/为什么触发它（specific keywords、contexts、file types）

**Format**：

- 最多 1024 chars
- 使用 third person
- 第一句说明它做什么
- 第二句："Use when [specific triggers]"

**Good example**：

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example**：

```
Helps with documents.
```

坏例子无法让 agent 区分它和其他 document skills。

## When to Add Scripts

以下情况添加 utility scripts：

- Operation 是 deterministic（validation、formatting）
- 同一段 code 会被反复生成
- Errors 需要明确 handling

相比 generated code，scripts 节省 tokens 并提升 reliability。

## When to Split Files

以下情况拆分为独立文件：

- SKILL.md 超过 100 行
- 内容有不同 domains（finance vs sales schemas）
- Advanced features 很少需要

## Review Checklist

draft 完成后验证：

- [ ] Description 包含 triggers（"Use when..."）
- [ ] SKILL.md 低于 100 行
- [ ] 没有 time-sensitive info
- [ ] Terminology 一致
- [ ] 包含 concrete examples
- [ ] References 只深入一层
