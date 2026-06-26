---
name: skill-registry
description: Local skill registry with trigger-word routing. Organize workspace skills and auto-match by keywords. | 本地技能注册表，基于触发词自动路由。管理 workspace 技能，按关键词匹配执行。
version: 1.0.0
triggers:
  - "what skills"
  - "list skills"
  - "有什么技能"
  - "你会什么"
  - "/skills"
  - "/技能"
metadata:
  author: Slim-Rush
  license: MIT
  openclaw:
    emoji: "📋"
    category: meta
    tags:
      - registry
      - routing
      - local
      - workspace
---

# Skill Registry | 技能注册表

Local skill registry with trigger-word based routing for OpenClaw workspaces.

本地技能注册表，基于触发词的自动路由机制。

---

## Features | 功能特性

| Feature | Description |
|---------|-------------|
| **Central Registry** | Single `REGISTRY.md` file lists all workspace skills with categories |
| **Trigger-word Routing** | Match user input keywords → auto-select skill |
| **Skill-aware Execution** | Agent scans triggers before acting |
| **Quick Query** | User asks "what skills?" → Agent lists available skills |

| 功能 | 说明 |
|------|------|
| **中央注册表** | 单一 `REGISTRY.md` 文件，分类列出所有技能 |
| **触发词路由** | 匹配用户输入关键词 → 自动选择技能 |
| **技能感知执行** | Agent 收到任务先扫描触发词 |
| **快速查询** | 用户问"有什么技能" → Agent 列出可用技能 |

---

## How It Differs | 与其他方案的区别

| Approach | This Skill | Others (LLM-based) |
|----------|------------|-------------------|
| Routing Method | Keyword rules | LLM analysis |
| Speed | Instant | Requires LLM call |
| Scope | Local workspace | ClawHub remote |
| Complexity | Simple, predictable | Complex, variable |

---

## Installation | 安装

### 1. Create Registry | 创建注册表

Copy `REGISTRY.template.md` to `skills/REGISTRY.md` and fill in your skills.

将 `REGISTRY.template.md` 复制为 `skills/REGISTRY.md`，填入你的技能列表。

### 2. Add Rules | 添加规则

Append `RULES.snippet.md` content to your `RULES.md` or `AGENTS.md`.

将 `RULES.snippet.md` 内容追加到你的 `RULES.md` 或 `AGENTS.md`。

### 3. Customize Routing Table | 自定义路由表

Edit the trigger-word table in rules to match your skills:

编辑规则中的触发词表，匹配你的技能：

```markdown
| Triggers | Skill | Description |
|----------|-------|-------------|
| video, edit | video-editor | Video editing |
| news, daily | daily-news | Daily news digest |
```

---

## Usage | 使用方法

### User Queries | 用户查询

| User Says | Agent Action |
|-----------|--------------|
| "What skills do you have?" | Read REGISTRY.md, list by category |
| "有什么技能" | 读取 REGISTRY.md，按分类列出 |
| "/skills video" | Return video-related skills only |
| "How to use XX skill?" | Read `skills/XX/SKILL.md` |

### Auto-routing Flow | 自动路由流程

```
User Request → Scan Triggers → Match Found?
                                 ↓ Yes: Read SKILL.md → Execute
                                 ↓ No:  Use general capability
```

---

## File Structure | 文件结构

```
skills/
├── REGISTRY.md              # Central registry (you maintain)
├── skill-registry/
│   ├── SKILL.md             # This file
│   ├── REGISTRY.template.md # Registry template
│   └── RULES.snippet.md     # Rules to add
├── your-skill-1/
│   └── SKILL.md
└── your-skill-2/
    └── SKILL.md
```

---

## Best Practices | 最佳实践

1. **Keep REGISTRY.md updated** — Add new skills when created
2. **Use specific triggers** — Avoid overly broad keywords
3. **Clear categories** — Group by function domain
4. **Regular cleanup** — Remove unused skills

---

## Example | 示例

**User**: Help me make a short video
**Agent thinks**: Trigger "video" → matches `video-assembler`
**Agent**: Reads `video-assembler/SKILL.md`, executes workflow...

**用户**: 帮我做个短视频
**Agent 思考**: 触发词"视频" → 匹配 `video-assembler`
**Agent**: 读取 `video-assembler/SKILL.md`，按流程执行...
