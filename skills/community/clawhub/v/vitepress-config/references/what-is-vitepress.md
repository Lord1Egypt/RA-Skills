# What is VitePress

> Source: https://vitepress.dev/guide/what-is-vitepress

VitePress is a Static Site Generator (SSG) designed for building fast, content-centric websites. It takes your source content written in Markdown, applies a theme, and generates static HTML pages.

## Use Cases

- **Documentation** - Default theme designed for technical docs. Powers Vue, Vite, Rollup, Pinia, VueUse, Vitest, D3, UnoCSS docs.
- **Blogs, Portfolios, Marketing Sites** - Fully custom themes with Vite + Vue developer experience.

## Developer Experience

- **Vite-Powered** - Instant server start, edits reflected <100ms without reload
- **Built-in Markdown Extensions** - Frontmatter, tables, syntax highlighting, code blocks
- **Vue-Enhanced Markdown** - Markdown files become Vue SFCs

## Performance

- Initial visit: static HTML + Vue SPA hydration
- Post-load navigation: SPA-style, no full page reload
- Automatic prefetching for links in viewport
- Static/dynamic parts optimized by Vue compiler

## VitePress vs VuePress

VitePress is the spiritual successor of VuePress 1 (Vue 2 + webpack). With Vue 3 and Vite, VitePress provides:
- Better DX
- Better production performance
- More polished default theme
- More flexible customization API

VuePress 1 is deprecated. VuePress 2 is maintained by the community.
