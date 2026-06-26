# engineering: coding — 开发类策略 / Coding Policy

**继承 / Inherits from**: `base/reliability.md`, `base/maintainability.md`, `base/ux.md`

开发类 Skill 的专属评审策略。在 base 基础上增加工程化特有观察项。

## 专属观察项 / Domain-Specific Observations

- **Determinism / 确定性** — 同样的输入是否产出一致结构的结果
- **Execution Stability / 执行稳定性** — 多轮调用是否稳定，是否 context 漂移
- **Tech Accuracy / 技术准确性** — 技术选型、API 用法、配置项是否正确

## 评审侧重 / Focus

| 一级维度 | 侧重内容 |
|---|---|
| Reliability | 生成结果是否正确、可运行、符合预期 |
| Engineering | 技术栈选择、项目结构、代码规范、配置合理性 |
| UX | 使用者是否能快速上手，指令是否直观 |
| Maintainability | Skill 是否便于扩展（如新增框架支持、新增模板） |

## 对抗测试建议 / Adversarial Tests

- 需求模糊（只说"搭个项目"，不指定技术栈）
- 技术冲突（要求 React + Vue 混用）
- 超出能力（要求不支持的框架或版本）
- 边界场景（空项目、超大项目、monorepo）

## 评分权重 / Scoring Weight

查阅 `scoring/SKILL.md` 预计算权重表中 **engineering/coding** 行。
