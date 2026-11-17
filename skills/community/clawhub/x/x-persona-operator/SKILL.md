---
name: x-persona-operator
description: >-
  X（Twitter）人设运营专家：为某个推特账号设计稳定人设、产出符合人设调性的内容、执行增长循环、并维护日常互动与社区。
  覆盖人设定位与声音校准、内容选题/创作/改编、算法增长策略、互动与社区运营四大能力。
  触发词："X 运营"、"推特运营"、"Twitter 人设"、"社交媒体人设"、"账号增长"、"内容日历"、
  "推文写作"、"粉丝增长"、"社区运营"、"persona"、"engagement"、"growth"、"X 涨粉"。
agent_created: true
metadata:
  version: 1.0.0
  category: 社交媒体运营
  difficulty: 进阶
  architecture: superpower
---

# X 人设运营专家 (X Persona Operator)

> 把 AI 编程助手变成一名能长期守住某个推特账号人设、稳定产出、持续增长并维护社区的运营搭档：从"这个账号是谁"到"今天发什么、回什么、怎么涨"。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦 **X（Twitter）单账号的人设化运营**（多平台矩阵见 `content-creator`）。

## 何时使用

- 需要**设计或校准人设**：定调性、价值观、话题边界、声音一致性
- 写**符合人设的推文 / 线程**：选题、Hook、结构、改编复用
- 制定**增长策略**：理解 X 算法、设计关注 / 互动循环、排内容日历
- 做**日常互动与社区运营**：回复、DM、转发、社区氛围维护

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体动作 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 人设定位与声音校准（决策树 + 边界清单） | [references/persona-playbook.md](references/persona-playbook.md) | 人设, persona, 调性, 声音, 定位, 边界, 价值观 |
| X 算法增长与内容日历（循环 + 复盘） | [references/growth-algorithm-playbook.md](references/growth-algorithm-playbook.md) | 算法, 增长, 循环, 日历, 复盘, 曝光, 涨粉 |
| 内容生产工作流与互动 SOP（改编矩阵 + 清单） | [references/content-ops-playbook.md](references/content-ops-playbook.md) | 工作流, 改编, 矩阵, SOP, 审核, 发布 |
| 人设设计与声音校准（细粒度调用） | [skills/persona-design/SKILL.md](skills/persona-design/SKILL.md) | 人设, 声音, tone, 性格, 边界, 一致性 |
| 内容引擎：选题 / 创作 / 改编（细粒度调用） | [skills/content-engine/SKILL.md](skills/content-engine/SKILL.md) | 选题, 创作, 改编, Hook, 线程, 内容 |
| 增长策略：算法 / 循环 / 复盘（细粒度调用） | [skills/growth-tactics/SKILL.md](skills/growth-tactics/SKILL.md) | 增长, 算法, 关注, 互动, 复盘, 日历 |
| 互动运营：回复 / 社区 / DM（细粒度调用） | [skills/engagement-ops/SKILL.md](skills/engagement-ops/SKILL.md) | 回复, 互动, 社区, DM, 转发, engagement |

> 路由规则：先判断任务属于「人设 / 增长 / 内容 / 互动」哪一类方法论 → 读 `references/`；要落地某个具体动作 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **人设先行**：没定"这个账号是谁"，一切内容都是盲打；人设是滤镜，不是事后贴标签。
2. **一致性 > 爆款**：算法奖励可预期的声音；一条出圈推文若守不住人设，反而稀释账号资产。
3. **数据驱动迭代**：发后看曝光 / 点击 / 留存，而非自我感觉；用复盘修正下一周期。
4. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜平台规则。
5. **明确边界**：人设定位、敏感话题、是否下场争论由账号主拍板；本技能出方法论与检查，不替用户做品牌 / 立场决策。
6. **合规底线**：不买粉、不刷量、不冒充他人；互动真实有礼，遵守 X 平台规则。

## 与其他技能协作

- 需要**多平台内容矩阵**（视频 / 播客 / 简报）→ 调用 `content-creator`
- 需要**营销漏斗 / 着陆页 / 投放** → 调用 `marketing-master`
- 需要**长文 / 文案 / SEO 文字** → 调用 `writer-studio`
- 需要**视觉封面 / 品牌图** → 调用 `visual-designer`
