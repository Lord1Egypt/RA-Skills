---
when: 写 REDUCTION_REPORT.md,或给拆出的附属文件加 frontmatter
topics: report-format, token-accounting, frontmatter
---

# REDUCTION_REPORT.md 模板

```markdown
# Reduction Report — <skill name>

## Token 对比

| 部分 | 原 | 压缩后 | 降幅 |
|------|----|----|------|
| description | X | X' | N% |
| body (always loaded) | Y | b* | N% |
| references | Z | Σrʲ | N% |
| 核心调用 (desc + b*) | ... | ... | ... |
| 全量 (desc + b* + all refs) | ... | ... | ... |

## 分类分布

core_rule: N 段 · background: N · example: N · template: N · redundant(丢弃): N

## 新拆出文件

- examples.md(X tok, when: ..., topics: ...)
- templates.md(X tok, when: ..., topics: ...)
- background.md(X tok, when: ..., topics: ...)

## Faithfulness(Gate 1)

- 抽取 operational concept:N 条
- 全部保留:✓ / 回滚次数:k(≤2)
- 标"不可压"的段落:[列表,若有]

## Gate 2 任务验证

- [ ] 有样例:对比 score_C vs score_A,记录 pass rate
- [x] 无样例:未验证运行时行为,建议在 <skill> 被实际调用 3–5 次后复检

## 风险 / 待人工确认

- [疑似 example-as-specification 的段落,让用户判断]
- [判为 redundant 但不确定的段落]
- [疑似已退休(obsolete)的 skill]

## 建议

- 是否候选退休:......
- 下一步:用户 diff `.reduced/SKILL.md` 与原文件,确认后替换
```

---

# 拆出文件的 frontmatter 模板

每个 `examples.md` / `templates.md` / `background.md` 顶部必须有:

```markdown
---
when: <一句话说明 agent 什么条件下应 read_file 这个文件>
topics: <3–5 个关键词,逗号分隔>
---
```

## when 写法

- 动词开头:"需要...", "想...", "不确定...", "写..."
- 描述**触发条件**而非**内容**。错:"示例集合";对:"想看前后对照走查或分类拿不准"
- 让 agent 能从自己当前的状态判断是否要读

## topics 写法

- 3–5 个关键词,涵盖:核心概念 + 具体产物名 + 触发场景
- 用于 semantic match,比自然语言描述更耐模糊查询

---

# Token 估算

没装 tiktoken 时的近似:
- 英文:`tokens ≈ chars / 4`
- 中文:`tokens ≈ chars / 1.5`(单字符占 1–2 token)
- 混合:取 `chars / 2.5`

有 tiktoken:
```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
len(enc.encode(text))
```

报告中写明使用的估算方式。
