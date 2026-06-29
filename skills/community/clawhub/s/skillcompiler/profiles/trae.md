# TRAE Platform Profile

> Target: TRAE IDE Skill Runtime
> Profile Version: 1.0.0

---

## Frontmatter 规范

```yaml
---
name: {kebab-case-name}
description: "{单行描述，不超过 500 字符}"
---
```

### 约束

| 字段 | 约束 | 说明 |
|------|------|------|
| `name` | kebab-case，仅小写字母、数字、连字符 | 对应 SKILL.md 文件名 |
| `description` | **单行字符串**，不支持多行 YAML / `>-` / `|-` | **关键约束：** TRAE 的 frontmatter parser 不解析多行描述。所有内容必须在一行内完成。 |
| `description 长度` | ≤ 500 字符 | 超长会被截断 |
| `description 格式` | 以 `Use when` 或 `Use for` 开头 | TRAE 触发匹配依赖 description 开头的场景引导词 |
| 额外字段 | `version` 可选 | TRAE 不强制但推荐标注 |

### 触发词规则

- TRAE 使用 **关键词匹配**（非语义匹配）
- 描述中必须包含 3-5 个**用户可能直接输入的动词/名词**
- 不支持正则、不支持通配符
- 触发词用「逗号 + 空格」分隔列举
- 示例：`Triggers on: code review, PR review, 代码审查`

### 描述模板（单行版）

```
Use when {触发场景一览}. Triggers on: {触发词1}, {触发词2}, {触发词3}. {核心功能一句话}.
```

### 示例

```
Use when you need to review Python code for bugs, style, and security issues. Triggers on: code review, PR review, 代码审查, 审查代码. Produces severity-graded reports.
```

---

## 加载机制

- TRAE 支持 SKILL.md + references/ 懒加载
- **不支持** agents/ 目录分离（multi-agent 需用 references/ 子目录模拟）
- 📍 标记用于 `references/*.md`，TRAE 识别此标记

## 文件结构约束

| 目录 | 支持 | 说明 |
|------|------|------|
| `references/` | ✅ | 按需懒加载 |
| `templates/` | ✅ | 输出模板 |
| `workflows/` | ❌ | 不识别 workflow 目录 |
| `agents/` | ❌ | 不识别独立 agent 目录 |
| `rubrics/` | ✅ | 但放在 references/ 内更安全 |
| `checklists/` | ⚠️ | 建议合并到 references/ |

## 已知限制

1. description 不支持分段、多行、block scalar（`>-` / `|`）
2. frontmatter 不支持嵌套字段
3. 触发匹配基于关键词，不基于语义
4. `references/` 中文件过多（> 15 个）可能影响加载性能
