# workflow: planner — 规划类策略 / Planner Policy

**继承 / Inherits from**: `base/reliability.md`, `base/maintainability.md`, `base/ux.md`

规划类 Skill 的专属评审策略。在 base 基础上增加流程规划特有观察项。

## 专属观察项 / Domain-Specific Observations

- **Process Completeness / 流程完整性** — 是否覆盖正常路径和异常路径
- **State Management / 状态管理** — 流程中的状态是否清晰、可追溯
- **Error Recovery / 错误恢复** — 中断后是否能恢复或回退

## 评审侧重 / Focus

| 一级维度 | 侧重内容 |
|---|---|
| Reliability | 流程是否完整、步骤是否有遗漏、异常处理是否到位 |
| Engineering | 流程定义是否清晰、条件分支是否覆盖 |
| UX | 用户在流程中是否清楚当前状态和下一步 |
| Maintainability | 流程步骤增删是否方便、新流程模板是否易添加 |

## 对抗测试建议 / Adversarial Tests

- 流程中途失败（第 3 步出错了怎么办）
- 用户跳步（直接跳到第 5 步）
- 重复执行（连续触发两次）
- 并发冲突（两个流程同时运行）

## 评分权重 / Scoring Weight

查阅 `scoring/SKILL.md` 预计算权重表中 **workflow/planner** 行。
