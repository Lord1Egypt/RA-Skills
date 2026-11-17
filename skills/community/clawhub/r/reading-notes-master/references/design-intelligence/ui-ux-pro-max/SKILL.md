---
name: ui-ux-pro-max
description: UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks for UI design, UX flows, information architecture, visual style direction, design systems/tokens, component specs, copy/microcopy, accessibility, or to generate/critique/refine frontend UI (HTML/CSS/JS, React, Next.js, Vue, Svelte, Tailwind). Includes workflows for (1) generating new UI layouts and styling, (2) improving existing UI/UX, (3) producing design-system tokens and component guidelines, and (4) turning UX recommendations into concrete code changes.
x-bundled-from: clawhub.ai/xobi667/skills/ui-ux-pro-max @ 0.1.0（上游 github.com/nextlevelbuilder/ui-ux-pro-max-skill，MIT-0）
x-bundled-in: reading-notes-master/references/design-intelligence/（2026-10-21 收录，路径已改为 bundle 内相对路径）
---

> **bundle 内路径说明**：本文件被 reading-notes-master 全量收录，下文所有
> `skills/ui-ux-pro-max/...` 路径均相对于本文件所在目录（即 `./`）。

Follow these steps to deliver high-quality UI/UX output with minimal back-and-forth.

## 1) Triage
Ask only what you must to avoid wrong work:
- Target platform: web / iOS / Android / desktop
- Stack (if code changes): React/Next/Vue/Svelte, CSS/Tailwind, component library
- Goal and constraints: conversion, speed, brand vibe, accessibility level (WCAG AA?)
- What you have: screenshot, Figma, repo, URL, user journey

If the user says "全部都要" (design + UX + code + design system), treat it as four deliverables and ship in that order.

## 2) Produce Deliverables (pick what fits)
Always be concrete: name components, states, spacing, typography, and interactions.

- **UI concept + layout**: Provide a clear visual direction, grid, typography, color system, key screens/sections.
- **UX flow**: Map the user journey, critical paths, error/empty/loading states, edge cases.
- **Design system**: Tokens (color/typography/spacing/radius/shadow), component rules, accessibility notes.
- **Implementation plan**: Exact file-level edits, component breakdown, and acceptance criteria.

## 3) Use Bundled Assets
This skill bundles data you can cite for inspiration/standards.

- **Design intelligence data**: Read from `./data/` when you need palettes, patterns, or UI/UX heuristics
  （styles / colors / typography / ux-guidelines / products / landing / charts / icons / web-interface /
  react-performance / ui-reasoning + stacks/ 下 13 个技术栈规范；原 assets/data/ 为字节级重复副本，收录时已剔除）。
- **Upstream reference**: If you need more phrasing/examples, consult `./references/upstream-skill-content.md`。

## 4) Optional Script (Design System Generator)
If you need to quickly generate tokens and page-specific overrides, use the bundled script:

```bash
python3 ./scripts/design_system.py --help
# 检索入口（BM25，推荐）：
python3 ./scripts/search.py "<query>" [--domain style|color|chart|landing|product|ux|typography|icons|react|web] [--stack nextjs|react|vue|svelte|astro|flutter|swiftui|react-native|shadcn|jetpack-compose|nuxtjs|nuxt-ui|html-tailwind] [--design-system [--persist]]
```

Prefer running it when the user wants a structured token output (ASCII-friendly).
**持久化注意**：`--persist` 会向当前工作目录写 `design-system/` 目录，使用前确认工作区范围。

## Output Standards
- Default to ASCII-only tokens/variables unless the project already uses Unicode.
- Include: spacing scale, type scale, 2-3 font pair options, color tokens, component states.
- Always cover: empty/loading/error, keyboard navigation, focus states, contrast.
