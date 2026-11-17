---
name: web-typography
description: Web 排版设计：字体选择、层级系统、可读性优化、响应式排版
source:
  type: derived
  repo: skills-repo/visual-designer
  path: skills/web-typography/SKILL.md
  url: https://skills.sh/wondelai/skills/web-typography
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 视觉设计
  platform: Web
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - typography
  - web-design
  - font
  - readability
  - visual-design
---

# Web Typography — Web 排版设计

> 排版是 Web 设计的基石——用户 95% 的时间在阅读文字，而不是看 UI。好的排版让内容可读、有节奏、有性格。本技能覆盖 Web 排版的核心实践。

## 能力

- **字体选择**：系统字体 vs Web 字体、Google Fonts 筛选、中英文搭配、性能考量
- **层级系统**：标题层级（H1-H6）、正文、注释、标签的尺寸和权重阶梯
- **可读性优化**：行高、字间距、行长（measure）、对比度、段落间距
- **响应式排版**：clamp() 流体字号、断点调整、移动端阅读体验
- **排版细节**：连字符、悬挂标点、首字母大写、引号样式

## 使用方式

在 Claude Code 中使用 `/web-typography` 调用。

```
/web-typography 帮我设计这个博客的排版层级
/web-typography 这个页面的字体组合是否合理？帮我优化
/web-typography 设计一套响应式排版系统
```

## 排版系统模板

```
Display:  clamp(3rem, 5vw, 5rem)     — 首页大标题
H1:       clamp(2rem, 3.5vw, 3rem)   — 页面标题
H2:       1.75rem                       — 章节标题
H3:       1.375rem                      — 小节标题
Body:     1rem / 1.6 line-height       — 正文
Caption:  0.875rem                      — 辅助文字
```

## 适用场景

- 独立开发者设计落地页和博客排版
- 产品页面字体层级重构
- 中英文混排的字体搭配方案
- 品牌网站的排版系统设计

## 限制

- 聚焦 Web 排版，不涉及印刷排版
- 字体选择覆盖主流平台，不涉及自建字体服务
- 不涉及字体设计和字库开发

## 相关参考（Playbook）

- [references/brand-typography-system.md](../../references/brand-typography-system.md) — 字体系统搭建方法（标题体/正文体选型、层级映射、回退方案）
- [references/design-principles.md](../../references/design-principles.md) — 对比度与留白纪律，对应 Web 正文可读性要求