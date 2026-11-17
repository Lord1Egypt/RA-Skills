---
name: technical-writer
description: 技术文章全流程写作：选题打磨、标题设计、结构规划、正文起草、编辑润色，面向开发者读者
source:
  type: derived
  url: https://skills.sh/samber/cc-skills/technical-article-writer
  repo: skills-repo/writer-studio
  path: skills/technical-writer/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 写作
  platform: Web
  difficulty: 进阶
---

# 技术文章写作

> 写出开发者真正想读的技术文章。从选题到发布的全流程辅助，结合技术写作的结构框架和文案钩子设计。

## 能力

- 7 阶段全流程：选题打磨 → 标题生成 → 开头钩子 → 正文结构 → 全稿起草 → CTA → 图片建议
- 8 种内容类型模板：Bug 溯源、用 X 重写 Y、构建记录、经验教训、趋势评论、基准测试、教程、解析
- 10 种标题钩子策略
- 选题质量过滤（Julia Evans 实用主义 + Julian Shapiro 新颖性检验）
- 代码示例规范（≤20 行、Before/After 对比、非显而易见行注释）
- AI 痕迹去除（去 AI 腔调，保留钩子和标题）

## 使用方式

在 Claude Code 中使用 `/technical-writer` 调用。

```
/technical-writer 我想写一篇关于 Rust 内存管理的文章
/technical-writer 帮我把这个笔记变成一篇技术博客
/technical-writer 为我的数据库优化文章设计 10 个标题
```

## 工作流

1. 选题采访：确认主题、目标、受众、内容类型、长度、核心论点
2. 标题生成：产出 10 个变体，标注优劣，用户挑选
3. 钩子设计：3-4 个开头策略，包含悬念、痛点或反直觉事实
4. 正文结构：按内容类型选择模板，逐节填充
5. 全稿起草：穿插钩子、章节、结论
6. CTA 委托：根据第一阶段目标设计行动号召
7. 标题终审：根据成稿重选最优标题

## 适用场景

- 独立开发者的技术博客写作
- 开源项目的发布公告和技术文档
- 技术品牌建设（thought leadership）
- 技术教程和深度解析文章

## 限制

- 不处理 SEO 优化（使用 `seo-checker`）
- 不处理平台分发策略和社交媒体适配
- 不自动发布到 CMS（需手动复制）
- 需要用户参与选题环节，非一次性自动生成

## 相关参考（Playbook）

- 通用写作流程与 10 种技术文章标题钩子策略、文体要点：[writing-process 流程篇](../../references/writing-process.md)
