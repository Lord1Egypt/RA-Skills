# Example Opening Turn - v1.0.1

This is the canonical first response when `start_confirmed: false`. It is `STARTUP_PLAN_ONLY (TEXT_ONLY)`. It must list S0, B1-B9, and P1-P9 individually and must not generate images.

## 当前执行计划

当前处于 S0：启动确认。此轮只展示流程，不做论文分析、不生成候选方案、不调用 Create image、`$imagegen` 或图像 API。

| 编号 | 层级 | 回复类型 | 做什么 | 本步产物 |
|---|---|---|---|---|
| S0 | Startup | STARTUP_PLAN_ONLY (TEXT_ONLY) | 展示完整流程 | 启动计划 |
| B1 | Skill Builder | TEXT_ONLY | 定义目标图类和 skill 目标 | figure-class brief |
| B2 | Skill Builder | TEXT_ONLY | 制定语料和合法获取计划 | corpus plan |
| B3 | Skill Builder | TEXT_ONLY | 获取/整理 PDF 和 manifest | local corpus |
| B4 | Skill Builder | TEXT_ONLY | 提取 figure/caption/panel 证据 | evidence map |
| B5 | Skill Builder | TEXT_ONLY | 构建图类 taxonomy | taxonomy |
| B6 | Skill Builder | TEXT_ONLY | 生成专项 skill blueprint | blueprint |
| B7 | Skill Builder | TEXT_ONLY | 生成 skill 包 | skill package |
| B8 | Skill Builder | TEXT_ONLY | 测试和修补 skill | test report |
| B9 | Skill Builder | TEXT_ONLY | 锁定专项 skill | locked skill |
| P1 | Figure Production | TEXT_ONLY | 收集目标论文材料 | material status |
| P2 | Figure Production | TEXT_ONLY | 诊断图需求和子类型 | subtype routing |
| P3 | Figure Production | TEXT_ONLY | 给出 4-6 个文字候选方案 | text candidates |
| P4 | Figure Production | TEXT_ONLY | 设置视觉候选图板 | candidate-board brief |
| P5 | Figure Production | IMAGE_ONLY | 生成/展示多张候选图 | image candidates only |
| P6 | Figure Production | TEXT_ONLY | 回看候选图并锁定/修正方向 | selected direction |
| P7 | Figure Production | TEXT_ONLY | 构建正式 image brief | final image brief |
| P8 | Figure Production | IMAGE_ONLY | 生成正式候选图/修订图 | formal images only |
| P9 | Figure Production | TEXT_ONLY | 诊断、caption、legend、正文衔接 | final text package |

## 默认推荐

先确认目标图类，进入 B1。生成专项 skill 后，后续具体制图会强制经过 P3 文本候选、P4 候选图设置、P5 多张候选图、P6 候选图选择，而不是只从文字方案里定稿。

## 当前状态与产物

- **阶段：**Startup
- **当前步骤：**S0
- **当前回复模式：**STARTUP_PLAN_ONLY (TEXT_ONLY)
- **全部步骤与当前位置：**S0 [当前位置] -> B1 -> B2 -> B3 -> B4 -> B5 -> B6 -> B7 -> B8 -> B9 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9
- **本轮新增产物：**启动计划
- **待产物：**目标图类定义、corpus/evidence、专项 skill、候选图桥接测试
- **session 状态延续提醒：**默认根据当前 session/history 自动延续状态。

## 下一步你可以这样问

1. `请使用**research-paper-figure-skill-factory**，执行，根据当前状态，下一步执行：确认开始，我想生成一个论文 diagram 制图 skill。`
2. `请使用**research-paper-figure-skill-factory**，根据当前状态，提供下一步提问建议。`
