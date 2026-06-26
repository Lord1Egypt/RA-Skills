# cognition: analysis — 分析类策略 / Analysis Policy

**继承 / Inherits from**: `base/reliability.md`, `base/maintainability.md`, `base/ux.md`

分析类 Skill 的专属评审策略。在 base 基础上增加分析解读特有观察项。

## 专属观察项 / Domain-Specific Observations

- **Analytical Accuracy / 分析准确性** — 分析结论是否有据可依，是否正确
- **Data Interpretation / 数据解读** — 能否从数据/代码中提取关键信息
- **Insight Depth / 洞察深度** — 是否只停留在表面描述，还是有深层分析

## 评审侧重 / Focus

| 一级维度 | 侧重内容 |
|---|---|
| Reliability | 分析结论是否准确、是否有遗漏 |
| Engineering | 分析框架是否清晰、是否可复用 |
| UX | 分析报告是否易读、重点是否突出 |
| Maintainability | 分析维度是否便于扩展 |

## 对抗测试建议 / Adversarial Tests

- 分析一个结构混乱的项目（测试信息抽取能力）
- 分析一个包含矛盾信息的项目（测试判断能力）
- 分析一个超大型项目（测试 context 处理）

## 评分权重 / Scoring Weight

查阅 `scoring/SKILL.md` 预计算权重表中 **cognition/analysis** 行。
