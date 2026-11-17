---
name: content-writer
description: 长文内容创作：博客正文、操作指南、列表文章，基于 QAE 模式和 Information Gain 策略
source:
  type: derived
  url: https://skills.sh/kostja94/marketing-skills/article-content
  repo: skills-repo/writer-studio
  path: skills/content-writer/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 内容
  platform: Web
  difficulty: 入门
---

# 长文内容创作

> 结构化创作博客正文、操作指南和长文内容。聚焦"写什么"——文章主体（引言、正文、结论）和信息增益策略。

## 能力

- 文章类型与字数指南（新闻 300-600、标准 1000-1500、支柱 2000-3500+）
- QAE 写作模式（Question → Answer → Evidence）
- Information Gain 策略：反共识、时效性、专家视角、独家数据
- TL;DR / Key Takeaways 摘要生成（GEO 友好）
- 可读性控制（段落 40-80 词、F 型扫描、粗体关键短语）
- 写作框架文章适配（AIDA 引言、PAS 操作指南、BAB 案例）
- 内容审计清单（钩子、段落、关键词、信息增益、CTA）

## 使用方式

在 Claude Code 中使用 `/content-writer` 调用。

```
/content-writer 写一篇 Go 并发模式的入门指南
/content-writer 为我的产品发布写一篇公告
/content-writer 把这篇文章的密度提升，减少水分
```

## 工作流

1. 确定文章类型和搜索意图（信息型/商业型/交易型）
2. SERP 审计：列出共识层，识别信息缺口
3. 输出提纲（H2 结构 + 关键词布局）
4. 起草引言（钩子 + 关键词 + 预期设置）
5. QAE 模式正文：每段 Question → Answer(40-60 词) → Evidence
6. 结论 + CTA + 产品关联

## 适用场景

- 独立开发者博客内容创作
- 产品博客和更新公告
- 技术教程和操作指南
- 需要信息增益（非 AI 共识内容）的竞争性文章

## 限制

- 不处理页面结构、Schema 标记和元数据（使用 `seo-checker`）
- 数据引用需人工核实
- 不自动发布或格式化 CMS
- 短文案场景使用 `copywriter`

## 相关参考（Playbook）

- 通用写作流程、标题打磨、编辑清单与文体要点（决定"什么时候用哪一个框架"）：[writing-process 流程篇](../../references/writing-process.md)
- SEO 信息增益策略与发布前策略层自查（字数分档、内链集群）：[seo-content-strategy 策略层](../../references/seo-content-strategy.md)
