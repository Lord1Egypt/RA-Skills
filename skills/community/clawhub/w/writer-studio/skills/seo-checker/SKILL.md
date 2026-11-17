---
name: seo-checker
description: 博客 SEO 发布前检查：标题/描述/结构化数据/OG 标签/链接审计，产出 Pass/Fail 报告和修复清单
source:
  type: derived
  url: https://skills.sh/agricidaniel/claude-blog/blog-seo-check
  repo: skills-repo/writer-studio
  path: skills/seo-checker/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: SEO
  platform: Web
  difficulty: 入门
---

# 博客 SEO 检查

> 发布前的全面页面 SEO 验证：跑完 11 项检查，产出通过/失败报告和优先级修复清单。在点击发布之前发现问题。

## 能力

- 标题标签验证（准确性、独特性、截断韧性）
- Meta Description 审查（长度、读者价值、主题一致性）
- 标题层级检查（单 H1、无跳级、作为问题或陈述）
- 内部链接审计（3-10 条、描述性锚文本、双向检查、无孤岛）
- 外部链接验证（权威源、broken link 检测、rel 属性）
- Canonical URL 和 OG/Twitter Card 元标签验证
- 结构化数据存在性和有效性（Article + BreadcrumbList + Person/Organization）
- URL 结构优化（可读性、无文件扩展名、大小写一致）

## 使用方式

在 Claude Code 中使用 `/seo-checker` 调用。

```
/seo-checker path/to/blog-post.md
/seo-checker https://myblog.com/posts/my-article
```

## 工作流

1. 读取目标文件（frontmatter、标题结构、链接、元标签、结构化数据）
2. 逐项检查 11 个维度，产出 PASS/FAIL/WARN/NA
3. 生成结构化报告：Overall 评分 + 结果表 + 优先修复清单
4. 可选：PageSpeed 性能检查（需 Google 凭据）

## 适用场景

- 博客文章发布前的 SEO 验收
- 批量检查已有内容的 SEO 健康度
- 网站迁移后的页面质量保障
- 新写手的 SEO 规范培训参考

## 限制

- 仅检查页面级 SEO，不涉及整站 SEO 策略
- 不生成新内容，仅验证和报告
- PageSpeed 检查需要额外配置 Google API 凭据
- 不替代 Google Search Console 的索引状态检查

## 相关参考（Playbook）

- SEO 策略层 playbook（意图对齐、信息增益、内链集群、发布前策略层自查 → 本技能技术层验收）：[seo-content-strategy 策略层](../../references/seo-content-strategy.md)
- 通用写作流程与发布前验收映射：[writing-process 流程篇](../../references/writing-process.md)
