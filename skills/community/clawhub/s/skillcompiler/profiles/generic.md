# Generic Platform Profile

> Target: Unknown / Custom / Future Skill Runtime
> Profile Version: 1.0.0

---

## 用途

当目标平台未显式指定时使用此 profile。它采用**最保守的规范**——假设平台对 frontmatter、description 格式、文件结构有最严格的限制。编译出的 skill 在通用性上最大，但在利用平台特性方面最小。

---

## Frontmatter 规范

```yaml
---
name: {kebab-case-name}
description: "{单行描述，不超过 300 字符}"
---
```

### 约束

| 字段 | 约束 | 说明 |
|------|------|------|
| `name` | kebab-case | 通用安全 |
| `description` | **严格单行**，不使用任何 YAML block scalar | 兼容所有解析器 |
| `description 长度` | ≤ 300 字符 | 最严格限制，保证不被截断 |
| `version` | 可选 | 部分平台不识别 |
| 额外字段 | **不允许** | 只保留 name + description 以保证最大兼容 |

### 描述模板（严格单行版）

```
Use when {触发场景}. Triggers on: {触发词1}, {触发词2}, {触发词3}. {核心功能一句话}.
```

---

## 加载机制

只使用 SKILL.md + references/ 的基础加载模式。不假设平台支持 agents/, workflows/ 等高级目录。

## 文件结构约束

| 目录 | 支持 | 说明 |
|------|------|------|
| `references/` | ✅ | 最安全的懒加载方式 |
| `templates/` | ✅ | 广泛支持 |
| 其他目录 | ❌ | 不生成，避免兼容性问题 |

## Compaction 行为

| 字段 | 值 | 说明 |
|------|---|------|
| `strategy` | `unknown` | 未知平台，假设最坏情况 |
| `body_limit_lines` | 80 | 保守估计，保证大多数平台不丢失关键信息 |
| `preserves` | frontmatter, first_50_lines | 保留的部分 |
| `loses` | 假设 body 后半部分可能丢失 | 最坏假设 |

**对编译器的启示：** 采用最保守策略——routing table 和所有关键信息必须在前 80 行内完整表达。

## 定制指南

要在特定平台使用此 profile 编译的 skill：

1. 将 description 改为目标平台支持的多行格式（如有需要）
2. 按平台能力选择性地启用 agents/, workflows/ 目录
3. 按平台触发机制调整触发词数量与格式

编写自定义 profile 时，参考 `profiles/trae.md` 和 `profiles/claude.md` 的结构：Frontmatter 规范（字段约束 + description 格式 + 长度上限）+ Compaction 行为 + 加载机制 + 文件结构约束。
