---
name: writer-studio
description: >-
  写作工作室技能库：覆盖短文案、技术文章、长文内容与 SEO 检查。
  提供写作流程与编辑、SEO 内容策略的方法论，并用子技能承载文案、技术写作、长文创作与 SEO 检查的落地写法。
  触发词："写作"、"文案"、"短文案"、"技术文章"、"博客"、"SEO"、"长文"、"编辑"、
  "标题"、"Information Gain"、"转化率"、"内容创作"。
agent_created: true
metadata:
  version: 1.0.0
  category: 写作
  difficulty: 进阶
  architecture: superpower
---

# 写作工作室 (Writer Studio)

> 把 AI 编程助手变成一名能扛下文字交付链路（选题→起草→编辑→验收）的搭档：从短文案到长文技术文章，并用子技能守住每个环节的清晰度与 SEO 底线。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能。本库聚焦**文字内容**（视频/音频见 `content-creator`）。

## 何时使用

- 写**短文案**：标题、广告语、CTA、着陆页、邮件文案
- 写**技术文章**：选题、标题、结构、起草、编辑全流程
- 写**长文内容**：博客正文、操作指南、信息增益策略
- 做**SEO 检查**：发布前 11 项 Pass/Fail 验收

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook；要落地某个具体产出 → 直接调 `skills/` 对应子技能。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 写作流程与编辑 | [references/writing-process.md](references/writing-process.md) | 流程, 起草, 编辑, 标题, 结构, 文体, 落地映射 |
| 稿件量化体检（注水词/被动句/句长/段落） | [references/writing-process.md](references/writing-process.md) §3 | 体检命令, 注水词, 被动语态, 句长, 段落, 阈值表, 盲区 |
| SEO 内容策略 | [references/seo-content-strategy.md](references/seo-content-strategy.md) | SEO, 关键词, 信息增益, 结构, 内链, 自检命令, H1, alt |
| 短文案（细粒度调用） | [skills/copywriter/SKILL.md](skills/copywriter/SKILL.md) | 文案, 标题, CTA, 着陆页, 邮件 |
| 技术文章（细粒度调用） | [skills/technical-writer/SKILL.md](skills/technical-writer/SKILL.md) | 技术文章, 选题, 结构, 编辑 |
| 长文内容（细粒度调用） | [skills/content-writer/SKILL.md](skills/content-writer/SKILL.md) | 长文, 博客, 操作指南, 信息增益 |
| SEO 检查（细粒度调用） | [skills/seo-checker/SKILL.md](skills/seo-checker/SKILL.md) | SEO, 检查, 11项, 验收, 发布前 |

> 路由规则：先判断任务属于「写作流程 / SEO 策略」哪类方法论 → 读 `references/`；要产出具体文案或文章 → 直接调 `skills/` 对应子技能。

## 核心原则（始终遵循）

1. **先受众后文风**：写给谁、解决什么，决定语气与结构。
2. **标题即门槛**：标题决定打开率，值得反复打磨。
3. **信息增益优先**：比别人多给一点真东西，不做 AI 共识搬运。
4. **编辑重于起草**：好文章是改出来的，初稿只求完整。
5. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆写。
6. **明确边界**：观点与品牌调性由人拍板，本技能出方法与检查。

## 与其他技能协作

- 需要**视频/音频内容** → 调用 `content-creator`
- 需要**视觉/封面** → 调用 `visual-designer`
- 需要**营销投放** → 调用 `marketing-master`
- 需要**产品文档** → 调用 `product-manager` / `docs-writer`
