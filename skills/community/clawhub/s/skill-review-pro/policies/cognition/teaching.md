# cognition: teaching — 教学类策略 / Teaching Policy

**继承 / Inherits from**: `base/reliability.md`, `base/maintainability.md`, `base/ux.md`

教学类 Skill 的专属评审策略。在 base 基础上增加教学认知特有观察项。

## 专属观察项 / Domain-Specific Observations

- **Pedagogy Clarity / 教学清晰度** — 概念解释是否通俗易懂，是否有类比
- **Learning Curve / 学习曲线** — 是否从简单到复杂，节奏是否合理
- **Concept Density / 概念密度** — 单次输出是否信息过载
- **Adaptability / 适应性** — 是否能根据学习者水平调整深度

## 评审侧重 / Focus

| 一级维度 | 侧重内容 |
|---|---|
| Reliability | 知识准确性、概念讲解是否正确 |
| Engineering | 教学结构是否清晰（渐进式、有节奏） |
| UX | 学习者是否容易跟、是否有趣不枯燥 |
| Maintainability | 知识库更新、新主题扩展是否方便 |

## 对抗测试建议 / Adversarial Tests

- 学习者完全零基础（不理解任何专业术语）
- 学习者提出错误理解（需要纠正而非直接说"不对"）
- 学习者跳跃提问（跳过基础直接问高级问题）
- 学习者表达不清（不知道自己想问什么）

## 评分权重 / Scoring Weight

查阅 `scoring/SKILL.md` 预计算权重表中 **cognition/teaching** 行。
