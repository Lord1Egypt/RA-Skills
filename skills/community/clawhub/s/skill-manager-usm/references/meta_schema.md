# meta.yaml Schema

每个技能目录下的 `meta.yaml` 定义该技能的元数据和分发维度。

## 完整字段

```yaml
# === 必填 ===
name: "skill-name"        # 与目录名一致
version: "1.0"            # 语义化版本号

# === 核心：维度定义 ===
# 控制技能对哪些 Agent 可见
#
# 方式一：通用维度 — 所有已注册 Agent 都可见
scope: "universal"
#
# 方式二：特定维度 — 仅列出的 Agent 可见
# scope:
#   - claude_code
#   - cursor
#   - gemini

# === 可选 ===
description: ""           # 简短描述（补充 SKILL.md frontmatter）
tags: []                  # 分类标签，如 ["ai", "workflow", "utility"]
author: ""                # 作者
```

## scope 取值

| 值 | 含义 | 示例 |
|---|---|---|
| `"universal"` | 所有 Agent 可见 | 通用工具类技能 |
| `["claude_code"]` | 仅 Claude Code | 依赖 Claude 特有工具的技能 |
| `["claude_code", "cursor"]` | Claude + Cursor | 跨部分 Agent 的技能 |

## Agent 标识符

与 `~/.skills/agents.yaml` 中的键名一致：

- `claude_code`
- `cursor`
- `codex`
- `gemini`

## 示例

### 通用技能
```yaml
name: "skill-creator"
version: "1.0"
scope: "universal"
description: "Create and manage skills"
tags: ["meta", "management"]
```

### 特定技能
```yaml
name: "xinyuan"
version: "1.0"
scope:
  - claude_code
description: "Claude Code 专用知识管理"
tags: ["knowledge", "memory"]
```
