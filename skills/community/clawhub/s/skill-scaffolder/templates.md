---
when: 写骨架 SKILL.md、拆出文件 frontmatter、或 ARCHITECT_REPORT
topics: frontmatter, skill-skeleton, architect-report, taxonomy-worksheet, token-accounting
---

# SKILL.md 骨架模板

````markdown
---
name: <skill-name>
description: <primary capability>。<unique identifier 关键词>。<trigger condition>。
---

# <SkillName>

## Trigger
- `/<skill-name>`
- <典型触发场景 1>
- <典型触发场景 2>

## <流程 / 步骤标题>
1. <core_rule step 1>
2. <core_rule step 2>
...

## 约束
- <must 列表>
- <禁止项 / 数字 / 阈值>

## 不该用的情况
- <负面场景>
````

# 拆出文件 frontmatter 模板

每个 `background.md` / `examples.md` / `templates.md` 顶部必有：

```markdown
---
when: <一句话：agent 什么条件下该 read_file 这个文件>
topics: <3–5 个关键词，逗号分隔>
---
```

**`when` 写法**：
- 动词开头："想...", "不确定...", "写..."
- 描述**触发条件**而非**内容**。错："示例集合"；对："想看前后对照走查或分类拿不准"
- 让 agent 能从自己当前的状态判断是否要读

**`topics` 写法**：
- 3–5 个关键词，涵盖：核心概念 + 具体产物名 + 触发场景
- 用于 semantic match，比自然语言描述更耐模糊查询

---

# Taxonomy 预标 worksheet

写 body 前，先列一张表，把脑子里所有内容一次打标签：

| # | 规则 / 内容 | 类型 | 去向 |
|---|-----------|------|------|
| 1 | <规则 / 动作 / 阈值> | `core_rule` | `SKILL.md` |
| 2 | <动机 / 为什么> | `background` | `background.md` |
| 3 | <I/O 对 / 示范> | `example` | `examples.md` |
| 4 | <固定格式 / boilerplate> | `template` | `templates.md` 或合回 `SKILL.md` |
| 5 | <已在 refs 重复> | `redundant` | 丢弃 |

**打标签优先级规则**：
- 含数字 / 阈值 / 路径 / API 名 / env → `core_rule`（即使看起来像 background）
- 写了"为什么" / "因为" → `background`
- 给了具体 I/O 对 → `example`（即使含 rule，Faithfulness 会捞回 core_rule）
- 纯格式 / boilerplate / JSON schema → `template`
- 和 refs 已有内容重复 → `redundant`

---

# ARCHITECT_REPORT.md 模板

````markdown
# Architect Report — <skill-name>

## Gate 0: Retirement check
- 3 典型触发场景：
  1. <场景 1>
  2. <场景 2>
  3. <场景 3>
- 裸模型能替代? <yes / no>
- 现有 skill / MCP / tool 能替代? <yes / no>
- 只需放 CLAUDE.md? <yes / no>
- **结论**: <创建 / 建议退休 + 理由>

## Routing signal 三要素
- primary capability (<N> tok): <...>
- trigger condition (<N> tok): <...>
- unique identifier (<N> tok): <...>

## Description (<N> tok)
> <description 文本>

**DDMIN 自检**: 能否再删一词仍唯一触发? <yes / no + 测试查询>

## Body taxonomy 分布
| 类型 | 数量 | Token |
|------|------|------|
| core_rule | N | N |
| background | N | N |
| example | N | N |
| template | N | N |
| redundant（丢弃） | N | — |

**core_rule 占比**: N%（应 ≥ 80%）

## 文件拆分
- `SKILL.md`: N tok
- `background.md`: N tok（when: ...  /  topics: ...）
- `examples.md`: N tok（when: ...  /  topics: ...）
- `templates.md`: N tok（when: ...  /  topics: ...）

## 四反模式检查
- [ ] 无 examples-as-specification（规则未藏在示例里）
- [ ] 无 background 藏 operational 信息（数字 / 阈值 / 路径 / API / env）
- [ ] description 无触发词枚举
- [ ] 无 redundant（body 未重复 refs）

## Faithfulness（Gate 1）
- operational concept 抽取：N 条
- 全部保留：✓ / 回滚次数：k
- 标"不可在 core_rule 内保留"的段：[列表，若有]

## 输出路径
`<path>/<skill-name>/`

## 下一步建议
- [ ] 用户跑一次 3 场景触发测试，验证 router 匹中
- [ ] 运行几轮真实用例后，用 `skill-compressor` 回归测试（理论上应压不了多少）
````

---

# Token 估算（未装 tiktoken 时）

- 英文：`tokens ≈ chars / 4`
- 中文：`tokens ≈ chars / 1.5`
- 混合：`tokens ≈ chars / 2.5`

有 tiktoken：
```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
len(enc.encode(text))
```

报告中写明使用的估算方式。
