---
name: slidev-maker
description: Use this skill when creating, editing, or exporting Slidev presentations — the Markdown + Vue web-based slide framework for developers. Covers installation and CLI commands, slide syntax and frontmatter, layouts, click animations and transitions, code highlighting (Shiki/Monaco/Magic Move), built-in components, diagrams (Mermaid/PlantUML), images/video/fonts, UnoCSS styling, LaTeX, themes, presenter mode, and exporting to PDF/PPTX/PNG. Prevents common mistakes like incorrect asset paths, deprecated features (Prism), and non-existent layouts.
---

# Slidev Maker

Domain knowledge for building [Slidev](https://sli.dev) presentations. Slidev turns Markdown into interactive, themeable slides using Vue 3, Vite, and UnoCSS.

Use this skill whenever you are scaffolding a deck, writing slide Markdown, adding interactivity, customizing themes/layouts, or exporting. Read the relevant `rules/` file below for detailed explanations and copy-pasteable examples before generating Slidev code.

## Quick Start

```bash
pnpm create slidev      # scaffold a new deck (also: npm init slidev)
slidev                  # dev server with hot reload (http://localhost:3030)
slidev build            # build a static SPA into dist/
slidev export           # export to PDF (also --format pptx|png|md)
```

Requires Node.js >= 18. Put static assets in `public/` and reference them with absolute paths (`/image.png`). Full setup, project structure, and workflows are in `rules/getting-started.md`.

## Rules

**Read `rules/anti-patterns.md` first** — it lists the critical, recurring mistakes that break decks.

Authoring:
- `rules/core-syntax.md` — slide separators, headmatter vs per-slide frontmatter, speaker notes, MDC syntax
- `rules/layouts.md` — built-in layouts, two-column slots, image/iframe layouts, custom layouts
- `rules/code-blocks.md` — Shiki highlighting, line highlighting, Monaco editor, Magic Move, TwoSlash
- `rules/animations.md` — v-click, v-after, v-clicks, v-motion, v-mark, slide transitions
- `rules/components.md` — built-in components: Arrow, Link, Toc, SlidevVideo, RenderWhen, LightOrDark, and more
- `rules/diagrams.md` — Mermaid and PlantUML integration and configuration
- `rules/assets.md` — images, video, fonts, icons — correct paths and the `public` folder
- `rules/styling.md` — UnoCSS utilities, custom & slide-scoped styles, dark mode, uno/vite config
- `rules/features.md` — LaTeX math, importing slides (`src:`), global layers, custom shortcuts

Setup & output:
- `rules/getting-started.md` — installation, CLI commands, project structure, workflows, tech stack
- `rules/themes.md` — using, configuring, overriding, and ejecting themes
- `rules/export.md` — PDF/PNG/PPTX export, SPA builds, and deployment (GitHub Pages, Netlify, Vercel)
- `rules/presenter.md` — presenter mode, speaker notes, timer, drawing, recording, remote control

Guidance:
- `rules/anti-patterns.md` — critical mistakes to avoid: deprecated features, wrong paths, non-existent layouts
- `rules/troubleshooting.md` — build/export/port/theme fixes plus authoring best practices

## Official Links

- Docs: https://sli.dev/guide · Themes: https://sli.dev/resources/theme-gallery · GitHub: https://github.com/slidevjs/slidev
