---
name: startup-founder
description: >-
  独立开发者创业技能库：覆盖点子验证、MVP 构建、创始人销售与融资准备。
  提供点子验证方法论与融资准备清单的方法论，并用子技能承载验证、构建、销售与融资的落地写法。
  触发词："创业"、"点子验证"、"MVP"、"融资"、"Pitch"、"创始人销售"、"traction"、
  "商业模式"、"冷启动"、"路演"、"投资人"。
agent_created: true
metadata:
  version: 1.0.0
  category: 创业
  difficulty: 进阶
  architecture: superpower
---

# 独立开发者创业 (Startup Founder)

> 把 AI 编程助手变成一名能陪你走完 0→1 的创业搭档：从验证点子、构建 MVP，到创始人销售与融资准备，并用子技能守住"做没人要的产品"这条失败主因。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦**创业全流程**（产品定义见 `product-manager`，日常销售执行见 `sales-professional`）。

## 何时使用

- 需要**验证点子**：判断问题是否真实紧迫、市场时机对不对
- 做 **MVP**：用最小成本交付可验证价值
- 做**创始人销售**：早期靠创始人卖愿景与专业性
- 做**融资准备**：Pitch Deck、投资人关系、交割

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体环节 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 点子验证方法论 | [references/validation-methodology.md](references/validation-methodology.md) | 验证, 问题, 时机, 商业数学, 访谈 |
| 验证量化门槛 / 证据分级 / 止损判据 | [references/validation-methodology.md](references/validation-methodology.md) §1.1、§2.1、§3.1 | 商业数学速算, 证据强度, 通过线, 时间盒, 转向, 止损 |
| 融资准备清单 | [references/fundraising-readiness.md](references/fundraising-readiness.md) | 融资, Pitch, Deck, 投资人, traction |
| 单位经济与 Runway 判档 | [references/fundraising-readiness.md](references/fundraising-readiness.md) §1.1、§1.2、§5.1 | LTV, CAC, 回收期, NDR, 毛留存, Burn Multiple, Runway, 轮次门槛 |
| 点子验证（细粒度调用） | [skills/idea-validator/SKILL.md](skills/idea-validator/SKILL.md) | 验证, 痛点, 市场, 假设 |
| MVP 构建（细粒度调用） | [skills/mvp-builder/SKILL.md](skills/mvp-builder/SKILL.md) | MVP, 手动, 流程化, 产品化 |
| 创始人销售（细粒度调用） | [skills/founder-sales/SKILL.md](skills/founder-sales/SKILL.md) | 销售, 信任, Pitch, 心理 |
| 融资指南（细粒度调用） | [skills/fundraising-guide/SKILL.md](skills/fundraising-guide/SKILL.md) | 融资, Deck, 投资人, 交割 |

> 路由规则：先判断任务属于「验证 / 融资」哪类方法论 → 读 `references/`；要落地某个环节产出 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **先验证再构建**：创业失败头号原因是做没人要的产品，先有人付钱再写代码。
2. **MVP 不是半成品**：是能交付价值的最小单位，不是砍功能的残次品。
3. **创始人是最好的销售**：早期卖的是愿景与专业性，不是功能清单。
4. **融资是放大器**：先有 traction 再谈估值，别把融资当救命稻草。判档用
   [references/fundraising-readiness.md](references/fundraising-readiness.md) §1.1 的量化门槛，别凭感觉说"有 traction"。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭热情跳步骤。
6. **明确边界**：押注方向与资源投入由创始人拍板，本技能出方法与清单。

## 与其他技能协作

- 需要**产品定义与文档** → 调用 `product-manager`
- 需要**日常销售执行** → 调用 `sales-professional`
- 需要**落地研发** → 调用 `ai-fullstack-engineer`
- 需要**增长与营销** → 调用 `marketing-master`
