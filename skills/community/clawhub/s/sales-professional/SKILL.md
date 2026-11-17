---
name: sales-professional
description: >-
  销售专业技能库：覆盖冷邮件、线索生成、GTM 策略与 CRM 自动化。
  提供销售管道与 GTM 决策、外联与跟进的方法论，并用子技能承载冷邮件、线索挖掘、上市策略与 CRM 自动化的落地写法。
  触发词："销售"、"冷邮件"、"线索"、"GTM"、"出海"、"CRM"、"跟进"、"转化"、
  "外联"、"管道"、"成交"、"客户开发"。
agent_created: true
metadata:
  version: 1.0.0
  category: 销售
  difficulty: 进阶
  architecture: superpower
---

# 销售专业 (Sales Professional)

> 把 AI 编程助手变成一名能扛下销售交付链路（线索→外联→跟进→成交）的搭档：从管道搭建到 CRM 自动化，并用子技能守住每个环节的转化底线。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦**销售执行与管道**（产品定义见 `product-manager`，融资见 `startup-founder`）。

## 何时使用

- 需要**销售管道**：搭 GTM 路径、定阶段与转化目标
- 写**冷邮件 / 外联**：高回复率的开场与跟进
- 做**线索生成**：找对人、写对话、筛优先级
- 做**CRM 自动化**：把重复动作交给系统，不漏跟进

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体产出 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 销售管道与 GTM 决策 | [references/sales-pipeline.md](references/sales-pipeline.md) | 管道, GTM, 阶段, 转化, 出海, 定价 |
| 外联与跟进 playbook | [references/outreach-playbook.md](references/outreach-playbook.md) | 冷邮件, 外联, 跟进, 回复率, 模板 |
| 冷邮件（细粒度调用） | [skills/cold-email/SKILL.md](skills/cold-email/SKILL.md) | 冷邮件, 开场, 主题行, 跟进 |
| 线索生成（细粒度调用） | [skills/lead-generation/SKILL.md](skills/lead-generation/SKILL.md) | 线索, ICP, 挖掘, 优先级, 名单 |
| GTM 策略（细粒度调用） | [skills/gtm-strategy/SKILL.md](skills/gtm-strategy/SKILL.md) | GTM, 上市, 渠道, 定价, 定位 |
| CRM 自动化（细粒度调用） | [skills/crm-automation/SKILL.md](skills/crm-automation/SKILL.md) | CRM, 自动化, 流程, 跟进, 漏斗 |

> 路由规则：先判断任务属于「管道策略 / 外联执行」哪类方法论 → 读 `references/`；要产出具体邮件或名单 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **先 ICP 后广撒网**：清楚理想客户画像，再决定去哪找、怎么说。
2. **价值前置**：冷邮件讲"对你有什么用"，不讲"我是谁"。
3. **系统化跟进**：多数正向回复出现在第 2-4 次**触达**（基线节奏 = 首封 + 3 次跟进，见 [references/outreach-playbook.md](references/outreach-playbook.md) §3），漏跟进=漏收入。
4. **用自动化守纪律**：CRM 自动提醒与分发，避免人为遗漏。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆写销售信。
6. **明确边界**：报价与承诺由人拍板，本技能出方法与模板，不替代商务判断。

## 与其他技能协作

- 需要**产品定义** → 调用 `product-manager`
- 需要**融资/GTM 资金** → 调用 `startup-founder`
- 需要**营销内容** → 调用 `marketing-master`
- 需要**邮件自动化落地** → 调用 `office-master`
