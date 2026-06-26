# workflow: reviewer — 评审类策略 / Reviewer Policy

**继承 / Inherits from**: `base/reliability.md`, `base/maintainability.md`, `base/ux.md`

评审类 Skill 的专属评审策略。在 base 基础上增加评审判断特有观察项。

## 专属观察项 / Domain-Specific Observations

- **Judgment Stability / 判断稳定性** — 同类问题在不同目标上评分是否一致
- **Attribution Accuracy / 归因准确性** — 能否区分目标本身问题 vs 环境问题
- **Actionability / 建议可执行性** — 改进建议是否具体到可直接操作
- **Bias Detection / 偏见检测** — 评审是否存在系统性偏好（如偏爱某种风格）

## 评审侧重 / Focus

| 一级维度 | 侧重内容 |
|---|---|
| Reliability | 评审结论是否准确、是否有遗漏 |
| Engineering | 评分体系是否严谨、规则是否可量化 |
| UX | 评审报告是否清晰易懂、建议是否可执行 |
| Maintainability | 评审标准是否便于扩展和调整 |

## 对抗测试建议 / Adversarial Tests

- 评审一个故意写得很好看但内容空洞的 Skill
- 评审一个风格与评审者截然不同的 Skill
- 评审一个功能正确但格式混乱的 Skill
- 评审一个超长 Skill（测试 context 处理）

## 评分权重 / Scoring Weight

查阅 `scoring/SKILL.md` 预计算权重表中 **workflow/reviewer** 行。
