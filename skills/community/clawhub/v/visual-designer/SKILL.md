---
name: visual-designer
description: >-
  视觉设计师技能库：覆盖品牌设计、插画、海报生成与网页排版。
  提供设计原则与层级、品牌与字体系统的方法论，并用子技能承载品牌、插画、海报与排版的落地写法。
  触发词："视觉设计"、"品牌"、"Logo"、"插画"、"海报"、"排版"、"字体"、"色彩"、
  "网格"、"层级"、"视觉规范"、"Web 排版"。
agent_created: true
metadata:
  version: 1.0.0
  category: 设计
  difficulty: 进阶
  architecture: superpower
---

# 视觉设计师 (Visual Designer)

> 把 AI 编程助手变成一名能扛下视觉交付链路（原则→系统→产出）的搭档：从设计原则到品牌与字体系统，并用子技能守住每个环节的视觉底线。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦**静态视觉与排版**（动效见 `animation-engineer`，UI 组件见 `design-studio`）。

## 何时使用

- 需要**设计原则**：层级、对比、对齐、留白的方法论
- 做**品牌设计**：Logo、色彩、视觉语言一致性
- 做**插画 / 海报**：风格定义与生成指引
- 做**网页排版**：字体层级、可读性、栅格

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体产出 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 设计原则与视觉层级 | [references/design-principles.md](references/design-principles.md) | 原则, 层级, 对比, 对齐, 留白, 网格 |
| 层级与间距的量化判据（字号比 / 行长 / 组间距） | [references/design-principles.md](references/design-principles.md) | 判据, 行长, measure, 间距阶梯, 分组, 8px |
| 品牌与字体系统 | [references/brand-typography-system.md](references/brand-typography-system.md) | 品牌, 字体, 色彩, 规范, 一致性 |
| 字号阶梯与字体选型（模数比 / 字重 / woff2） | [references/brand-typography-system.md](references/brand-typography-system.md) | 模数, type scale, 字号阶梯, 字重, 选型, 回退 |
| 对比度速算与 AA/AAA 判据 | [references/brand-typography-system.md](references/brand-typography-system.md) | 对比度, contrast, WCAG, AA, 可读性 |
| 品牌设计（细粒度调用） | [skills/brand-designer/SKILL.md](skills/brand-designer/SKILL.md) | 品牌, Logo, 视觉语言, 色彩 |
| 插画（细粒度调用） | [skills/illustrator/SKILL.md](skills/illustrator/SKILL.md) | 插画, 风格, 角色, 配色 |
| 海报生成（细粒度调用） | [skills/poster-design-generation/SKILL.md](skills/poster-design-generation/SKILL.md) | 海报, 构图, 文案, 生成 |
| 网页排版（细粒度调用） | [skills/web-typography/SKILL.md](skills/web-typography/SKILL.md) | 排版, 字体, 可读性, 栅格 |

> 路由规则：先判断任务属于「原则 / 品牌系统」哪类方法论 → 读 `references/`；要产出具体设计 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **层级先于装饰**：先看信息主次，再谈美化；没有层级的"好看"是噪音。
2. **对比创造价值**：字号、色块、留白制造焦点，避免平均用力。
3. **系统保证一致**：品牌与字体走规范，多物料不跑偏。
4. **可读性底线**：正文排版永远优先可读性，不为炫技牺牲清晰。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆定规范。
6. **明确边界**：最终审美拍板由设计师/客户做，本技能出方法与系统，不替代创意。

## 与其他技能协作

- 需要**动效** → 调用 `animation-engineer`
- 需要**UI 组件** → 调用 `design-studio`
- 需要**内容/文案** → 调用 `writer-studio` / `content-creator`
- 需要**落地前端** → 调用 `ai-fullstack-engineer` / `frontend-engineer`
