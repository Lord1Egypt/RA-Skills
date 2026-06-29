# Claude Platform Profile (Claude.ai / Claude Code)

> Target: Claude.ai Web UI / Claude Code Skill Runtime
> Profile Version: 1.0.0

---

## Frontmatter 规范

```yaml
---
name: {kebab-case-name}
description: >
  Use when {触发场景}. Triggers on: {trigger1}, {trigger2},
  {trigger3}. {核心功能一句话}
version: 1.0.0
---
```

### 约束

| 字段 | 约束 | 说明 |
|------|------|------|
| `name` | kebab-case | 对应 SKILL.md 文件名 |
| `description` | 支持多行 block scalar（`>` / `|`） | 可分段描述 |
| `description 长度` | ≤ 500 字符 | 但推荐 ≤ 300 字符 |
| `version` | 推荐 | 用于版本管理 |
| 额外字段 | 可扩展 | Claude 对 frontmatter 额外字段容忍度较高 |

### 触发词规则

- Claude 使用 **语义匹配 + 关键词匹配** 混合
- 描述中触发词列表不需要穷举，覆盖主要变体即可
- 支持 `Triggers on:` 列表格式（可换行）
- 示例：
  ```
  Triggers on:
  - code review
  - PR review
  - 代码审查
  - security audit
  ```

### 描述模板（多行版）

```
Use when {触发场景}.

Triggers on:
- {触发词1}
- {触发词2}
- {触发词3}

{核心功能一句话描述。多行时可补充更多上下文。}
```

---

## 加载机制

- 支持 SKILL.md + 多级 reference 结构
- 📍 标记用于加载 references/, agents/, workflows/
- 支持 `agents/` 独立目录做 multi-agent 拆分
- 支持 `workflows/` 目录管理复杂工作流

## 文件结构约束

| 目录 | 支持 | 说明 |
|------|------|------|
| `references/` | ✅ | 按需懒加载 |
| `templates/` | ✅ | 输出模板 |
| `workflows/` | ✅ | workflow 定义 |
| `agents/` | ✅ | 独立 agent 文件 |
| `rubrics/` | ✅ | 评分体系 |
| `checklists/` | ✅ | 检查清单 |
| `schemas/` | ✅ | JSON Schema |
| `examples/` | ✅ | 示例 |
| `config/` | ✅ | 配置参数 |

## 已知限制与差异

1. description 支持多行但推荐不超过 500 字符
2. Semantic matching means triggering is less sensitive to exact keyword alignment than TRAE
3. 对 `references/` 目录中文件数量容忍度较高（可 > 20 个）
4. 支持 agents/ 分离，适合 multi-agent 架构
