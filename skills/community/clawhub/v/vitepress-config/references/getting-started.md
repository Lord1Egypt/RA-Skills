# Getting Started Reference

> Source: https://vitepress.dev/guide/getting-started

## Installation

```sh
npm add -D vitepress@next
# or
pnpm add -D vitepress@next
# or
yarn add -D vitepress@next vue
# or
bun add -D vitepress@next
```

**Requirements:** Node.js 20+, terminal, text editor (VSCode + Vue extension recommended)

## Setup Wizard

```sh
npx vitepress init
```

Questions:
1. Config location (e.g., `./docs`)
2. Markdown files location (e.g., `./docs`)
3. Site title
4. Site description
5. Theme (Default Theme)
6. Use TypeScript? (Yes/No)
7. Add npm scripts? (Yes)
8. Prefix for scripts? (e.g., `docs`)

## File Structure

```
docs/
├─ .vitepress/
│  └─ config.js
├─ api-examples.md
├─ markdown-examples.md
└─ index.md
```

## Config File

```javascript
// .vitepress/config.js
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'VitePress',
  description: 'Just playing around.',

  themeConfig: {
    // theme-level options
  }
})
```

## NPM Scripts

```json
{
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  }
}
```

## Development

```sh
npm run docs:dev
# or
npx vitepress dev docs
```

Visit http://localhost:5173

## Build

```sh
npm run docs:build
npm run docs:preview  # preview at http://localhost:4173
```

## Next Steps

1. Read [Routing Guide](https://vitepress.dev/guide/routing) - understand file-based routing
2. Read [Markdown Extensions](https://vitepress.dev/guide/markdown) - learn markdown features
3. Read [Default Theme Config](https://vitepress.dev/reference/default-theme-config) - customize nav, sidebar, etc.
4. Read [Custom Theme](https://vitepress.dev/guide/custom-theme) - build custom themes
5. Read [Deployment Guide](https://vitepress.dev/guide/deploy) - deploy your site
