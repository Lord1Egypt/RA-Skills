## 推荐 Prompt 结构 / Recommended Prompt Structure

默认推荐 / Default recommendation:

```md
# Skill: xxx

## Goal
...

## Core Principles
...

## Responsibilities
...

## Workflow
...

## Output Strategy
...

## Constraints
...

## Multi-turn Conversation
...

## Ideal Outcome
...
```

---

## 各平台文件格式参考 / Platform File Format Reference

**OpenClaw:**
```yaml
---
name: <skill-name>
homepage: https://github.com/user/repo
description: >
  <中文 description>
  <English description>
  触发词：...
---
```

**Claude Code:**
```markdown
# <Skill Name>

<直接放 prompt 正文>
```

**Cursor:**
```markdown
---
description: <英文 description>
globs: **/*.{ts,tsx,js,jsx}
alwaysApply: false
---
<prompt 正文>
```

**Cline:**
```
<prompt 正文，无额外包装>
```

**通用 System Prompt:**
```markdown
<prompt 正文>
```
