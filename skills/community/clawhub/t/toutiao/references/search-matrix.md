# 检索词矩阵

用于系统化收集候选新闻并保证覆盖率。

## 最低执行标准

- 总检索次数：至少 8 次，建议 10-12 次。
- 维度覆盖：A/B/C/D/E/F 六个维度必须全部覆盖。
- 每个维度至少 1 次检索；若结果为空，换词重搜一次。

## 时间占位符

在检索式中替换以下占位符：

- `<month_year>` 示例：`March 2026`
- `<month>` 示例：`March`
- `<date_iso>` 示例：`2026-03-11`

## A. 周报 / Newsletter（优先）

- `"last week in AI" <month_year>`
- `"AI weekly roundup" <month_year>`
- `"the batch AI newsletter"`
- `site:substack.com "AI news" <month>`

## B. 社区热度 / 病毒传播

- `"viral AI tool" OR "viral AI agent"`
- `"AI trending" site:reddit.com OR site:news.ycombinator.com`
- `"GitHub trending AI" OR "AI open source trending"`
- `"everyone is talking about" AI`
- `"most popular AI" this week`

## C. 产品发布与模型更新

- `"AI model release" OR "LLM launch" <month>`
- `"AI product launch" <month_year>`
- `OpenAI OR Anthropic OR Google OR Meta AI announcement`
- `"大模型 发布" OR "AI 新产品"`

## D. 融资与商业

- `"AI startup funding" <month_year>`
- `"AI acquisition" OR "AI IPO"`
- `"AI 融资" OR "人工智能投资"`

## E. 研究突破

- `"AI breakthrough" OR "AI paper" <month>`
- `"state of the art" machine learning`
- `"AI 论文" OR "机器学习突破"`
- `site:arxiv.org cs.AI recent`
- `site:arxiv.org cs.LG recent`

## F. 监管与政策

- `"AI regulation" OR "AI policy" <month_year>`
- `"AI law" OR "AI governance"`
- `"AI 监管" OR "人工智能法案"`

## 反模式清单

| 不建议 | 建议 | 原因 |
|---|---|---|
| `AI news today` | 分维度检索（A-F） | 泛词噪声高，易漏社区热点 |
| `AI news today February 2026` | `AI weekly roundup February 2026` | 具体日期易命中预测/展望文 |
| 只搜 3 次就输出 | 至少 8 次并覆盖 6 维 | 覆盖不足，遗漏率高 |

## 执行记录建议

每次检索记录：

- 关键词
- 时间
- 命中链接数
- 是否进入候选池
