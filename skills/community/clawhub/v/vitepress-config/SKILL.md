---
name: vitepress
description: 'VitePress static site generator toolkit. Use when working with VitePress configuration, theming, routing, markdown, Vue in markdown, data loading, custom themes, SSR, i18n, or deployment. Triggers: vitepress config, site-config, theme config, .vitepress/config, frontmatter, vitepress dev/build/preview, markdown extensions, custom theme, data loader.'
---

# VitePress

Vue-powered static site generator for documentation, blogs, and marketing sites.

## Quick Start

```sh
npm add -D vitepress@next
npx vitepress init
npm run docs:dev
```

## Core Config

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'My Site',
  description: 'Site description',
  base: '/docs/',                    // for sub-path deployment
  srcDir: './src',                    // markdown source directory
  cleanUrls: true,                    // remove .html
  appearance: 'dark',                 // dark mode
  lastUpdated: true,                 // Git-based timestamps

  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Guide', link: '/guide/' },
      { text: 'Config', link: '/reference/site-config' }
    ],
    sidebar: [
      { text: 'Section', items: [{ text: 'Page', link: '/page' }] }
    ],
    search: { provider: 'local' }
  }
})
```

## Frontmatter

```yaml
---
title: Page Title
layout: doc           # doc | home | page
navbar: true
sidebar: true
outline: [2, 3]       # show h2-h3 in aside
lastUpdated: true
editLink: true
footer: true
---
```

Home page hero:

```yaml
---
layout: home
hero:
  name: VitePress
  text: Static site generator
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
features:
  - icon: 🛠️
    title: Fast
    details: Built with Vite
---
```

## Markdown Extensions

```md
## Custom anchor {#custom}

::: info
Info box
:::

```js{2}
const x = 1  // highlight line 2
:::

<<< @/snippets/file.js{1}

[[toc]]
```
```

## Routing

```
index.md         -->  /
guide/start.md   -->  /guide/start/
```

Dynamic routes: `packages/[pkg].md` + `packages/[pkg].paths.js`

## Custom Theme

```javascript
// .vitepress/theme/index.js
import Layout from './Layout.vue'

export default { Layout }
```

```vue
<!-- Layout.vue -->
<template>
  <h1>Custom Layout!</h1>
  <Content />
</template>
```

Extend default theme:

```javascript
import DefaultTheme from 'vitepress/theme'
export default { extends: DefaultTheme }
```

## Data Loading

```javascript
// .vitepress/posts.data.js
import { createContentLoader } from 'vitepress'

export default createContentLoader('posts/*.md', {
  transform: (data) => data.sort(/* ... */)
})
```

```vue
<script setup>
import { data } from './posts.data.js'
</script>
```

## SSR

```vue
<ClientOnly>
  <BrowserOnlyComponent />
</ClientOnly>
```

## CLI

```sh
vitepress dev docs        # start dev server
vitepress build docs       # build for production
vitepress preview docs     # preview production build
```

## Reference Files

Detailed docs in `references/` directory:

### Guide Pages
- `what-is-vitepress.md` - What is VitePress, use cases, performance
- `getting-started.md` - Installation and setup
- `routing.md` - File routing, clean URLs, rewrites, dynamic routes
- `markdown.md` - Markdown extensions syntax
- `asset-handling.md` - Static assets, public directory, base URL
- `using-vue.md` - Using Vue in markdown, components, directives
- `extending-default-theme.md` - CSS customization, layout slots, view transitions
- `custom-theme.md` - Building custom themes
- `data-loading-ssr-i18n.md` - Data loaders, SSR, i18n
- `mpa-mode.md` - MPA mode for zero-JS sites
- `sitemap-generation.md` - Sitemap generation
- `cms.md` - Connecting to CMS
- `deploy.md` - Deployment guides for various platforms

### Reference Pages
- `site-config.md` - All config options and build hooks
- `frontmatter.md` - Page frontmatter options
- `runtime-api.md` - useData, useRoute, useRouter, withBase
- `cli.md` - Command line options
- `default-theme-config.md` - Nav, sidebar, search, footer options
- `default-theme-components.md` - Hero, features, badge, team page

## Links

- [Official Docs](https://vitepress.dev/)
- [Guide](https://vitepress.dev/guide/)
- [Reference](https://vitepress.dev/reference/site-config)
- [GitHub](https://github.com/vuejs/vitepress)
