---
name: copywriter
description: 短文案写作：标题、广告语、CTA、着陆页、邮件文案，基于 PAS/AIDA/BAB 框架
source:
  type: derived
  url: https://skills.sh/kostja94/marketing-skills/copywriting
  repo: skills-repo/writer-studio
  path: skills/copywriter/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 文案
  platform: 通用
  difficulty: 入门
---

# 短文案写作

> 面向独立开发者的短文案写作工具：用 PAS/AIDA/BAB 框架写标题、广告语、CTA、着陆页和邮件文案。

## 能力

- 5 种文案框架（PAS、AIDA、BAB、FAB、4U）辅助创作
- 6 种标题公式：How to、数字列表、谁+收益、问题→方案、Before→After
- 广告语与着陆页对齐检查（避免 promise-mismatch 导致跳出）
- CTA 优化：动词引导、价值驱动、A/B 测试建议
- 项目上下文感知：自动读取 `.claude/project-context.md` 的品牌定位

## 使用方式

在 Claude Code 中使用 `/copywriter` 调用。

```
/copywriter 为我的 SaaS 着陆页写 3 个标题方案
/copywriter 优化这个 CTA 按钮文案
/copywriter 用 PAS 框架写一段广告语
```

## 工作流

1. 识别场景（广告/着陆页/邮件/CTA）和目标阶段（意识/考虑/转化/留存）
2. 读取项目上下文（如存在 `.claude/project-context.md`）
3. 推荐合适的文案框架
4. 输出标题方案（2-3 个）、正文结构、CTA 选项
5. 提供 A/B 测试建议

## 适用场景

- 独立开发者的产品着陆页文案
- SaaS 订阅广告语和 CTA 优化
- 邮件营销主题行和正文
- 社交媒体推广短文案

## 限制

- 不适合长篇博客/文章正文（使用 `content-writer`）
- 不处理 SEO 关键词策略（使用 `seo-checker`）
- 框架建议需要人类判断确认

## 相关参考（Playbook）

- 通用写作流程与 6 种标题公式（How to / 数字列表 / 谁+收益 / 问题→方案 / Before→After）、编辑清单：[writing-process 流程篇](../../references/writing-process.md)
