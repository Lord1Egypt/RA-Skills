# Getting Started with Slidev

Installation, CLI commands, project structure, and common workflows.

## What is Slidev

Slidev is a presentation framework for developers. You write slides in Markdown and Slidev renders them with Vue 3 and web technologies, giving you interactive, pixel-perfect, themeable decks. It is built on Vite, Vue 3, UnoCSS, Shiki, Monaco, Mermaid, KaTeX, VueUse, and Iconify.

## Installation

Scaffold a new presentation:
```bash
# pnpm (recommended)
pnpm create slidev

# npm
npm init slidev

# yarn
yarn create slidev

# bun
bun create slidev
```

Or try online at https://sli.dev/new (StackBlitz). Slidev requires Node.js >= 18.

## Essential CLI Commands

Start the dev server (hot-reloads `slides.md`):
```bash
slidev
# or specify an entry file
slidev slides.md
```

The dev server runs at `http://localhost:3030` by default.

Build a static SPA:
```bash
slidev build
```

Export to PDF (or other formats):
```bash
slidev export
slidev export --format pptx
slidev export --format png
slidev export --format md
```

Format / normalize slide files:
```bash
slidev format
```

See `export.md` for full export and deployment options.

## Project Directory Structure

```
./
├─ components/       # Custom Vue components (auto-imported)
├─ layouts/          # Custom layouts
├─ public/           # Static assets (images, video) — served at /
├─ setup/            # Custom setup hooks (e.g. mermaid.ts)
├─ snippets/         # Reusable code snippets
├─ styles/           # Custom global styles (index.css / index.ts)
├─ slides.md         # Main presentation file
├─ vite.config.ts    # Vite configuration
└─ uno.config.ts     # UnoCSS configuration
```

Assets MUST live in `public/` and be referenced with absolute paths (`/image.png`). See `assets.md` and `anti-patterns.md`.

## Common Workflows

### Create a basic presentation
```bash
pnpm create slidev      # scaffold
# edit slides.md
slidev                  # preview with hot reload
slidev export           # export to PDF when done
```

### Add a custom component
Create a `.vue` file in `components/` — it is auto-imported, no registration needed:
```
./components/
  Counter.vue
slides.md
```
```vue
<!-- components/Counter.vue -->
<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">Count: {{ count }}</button>
</template>
```
Use it directly in a slide: `<Counter />`

### Split slides across files
Keep large decks manageable by importing slide files with `src:` (see `features.md`):
```md
---
src: ./slides/intro.md
---

---
src: ./slides/content.md
---
```

### Apply a theme
```bash
pnpm add slidev-theme-seriph   # optional; installed on first run too
```
```md
---
theme: seriph
---
```
See `themes.md` for theme configuration, local themes, and ejecting.

## Technology Stack

| Tool | Role |
|------|------|
| Vite | Build tool / dev server |
| Vue 3 | Component framework |
| UnoCSS | Atomic CSS engine (Tailwind-compatible) |
| Shiki | Syntax highlighter (the only highlighter) |
| Monaco Editor | In-slide editable code |
| Mermaid / PlantUML | Diagrams |
| KaTeX | LaTeX math rendering |
| VueUse / @vueuse/motion | Composition utilities & motion |
| Iconify | Icons (`<collection-name />`) |

## Official Links

- Website: https://sli.dev
- Guide: https://sli.dev/guide
- GitHub: https://github.com/slidevjs/slidev
- Themes gallery: https://sli.dev/resources/theme-gallery
- Discord: https://chat.sli.dev
