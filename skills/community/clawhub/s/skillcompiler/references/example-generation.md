# Conditional Pass: Example Generation

**加载时机：** 📍 仅当 Skill 涉及复杂流程/规则/评分体系时加载。

---

## 触发条件

满足任一：
- architecture_type = workflow 或 multi-agent
- 有 rubrics（评分体系）
- 有 5+ 条 rules
- 用户显式要求

---

## 生成规则

### 示例类型

| 类型 | 用途 | 何时生成 |
|------|------|---------|
| Minimal | 最简输入输出，验证基本流程 | 总是 |
| Normal | 典型使用场景 | 总是 |
| Complex | 边界条件或复杂输入 | 当有复杂规则时 |
| Edge Case | 极端输入 | 当有数值阈值时 |
| Failure Case | 应该失败的输入 | 当有输入验证时 |
| Anti-pattern | 不应该这样用 | 当有常见误用时 |

### 示例格式

```markdown
# Example: {Title}

**Type:** minimal | normal | complex | edge-case | failure | anti-pattern

## Input
{输入内容}

## Expected Output
{期望输出}

## Notes
{为什么是这个输出，关键决策点}
```

### 生成原则

1. **从 Prompt 中提取** — 如果 Prompt 自带示例，优先用
2. **覆盖关键路径** — 每个主要 workflow 步骤至少有一个示例
3. **不过度生成** — 3-5 个高质量示例 > 10 个低质量示例
4. **可扩展** — examples/ 目录设计为可追加
