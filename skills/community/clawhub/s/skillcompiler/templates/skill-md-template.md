# SKILL.md Output Template

**用途：** Pass 4 生成 SKILL.md 时的参考模板。

---

```markdown
---
name: {{skill-name}}
description: "Use when {{触发场景}}. Triggers on: {{trigger1}}, {{trigger2}}, {{trigger3}}. {{核心功能一句话}}"
version: 1.0.0
---

# {{Skill Name}}

{{一句话定位——这个 Skill 做什么}}

## 核心流程

{{3-5 步流程概览，每步一句话，不展开细节}}

1. {{Step 1 概览}}
2. {{Step 2 概览}}
3. {{Step 3 概览}}

## 执行步骤

### Step 1 — {{名称}}

📍 加载文件: references/{{file}}.md

{{简要说明这一步做什么}}

**输入：** {{输入描述}}
**输出：** {{输出描述}}

### Step 2 — {{名称}}

📍 加载文件: references/{{file}}.md

{{简要说明}}

**输入：** {{输入}}
**输出：** {{输出}}

## 输出格式

📍 加载文件: templates/{{output-template}}.md

{{或直接描述输出 schema}}

## Gotchas / Footguns

> 上线后根据实际 failure case 填充。

- {{常见陷阱 1}}

---

## Provenance

- **Built with:** Skill Compiler v1.0.0
- **Source:** {{来源 Prompt 概述}}
```

---

## 模板变量

| 变量 | 说明 | 来源 |
|------|------|------|
| `{{skill-name}}` | kebab-case 名称 | Pass 3 IR |
| `{{Skill Name}}` | 显示名称 | Pass 3 IR |
| `{{触发场景}}` | 用户何时需要 | Pass 1 IR |
| `{{triggerN}}` | 触发词 | Pass 1 capability_hints |
| `{{核心功能一句话}}` | 核心功能 | Pass 1 prompt_summary |
| `{{file}}.md` | reference 文件名 | Pass 3 reference_tree |
| `{{output-template}}.md` | 输出模板 | Pass 3 module_decomposition.templates |
