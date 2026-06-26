# Site Config Reference

> Source: https://vitepress.dev/reference/site-config

## Config Resolution

Config file: `<root>/.vitepress/config.[ext]` (.js, .ts, .mjs, .mts)

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'en-US',
  title: 'VitePress',
  description: 'Vite & Vue powered static site generator.',
})
```

### Dynamic Config

```typescript
export default async () => {
  const posts = await fetch('https://my-cms.com/blog-posts').then(r => r.json())
  return defineConfig({
    themeConfig: { sidebar: posts.map(p => ({ text: p.name, link: `/posts/${p.name}` })) }
  })
}
```

### Typed Theme Config

```typescript
import { defineConfigWithTheme } from 'vitepress'
import type { ThemeConfig } from 'your-theme'

export default defineConfigWithTheme<ThemeConfig>({ themeConfig: {} })
```

## Config Options

### Basic

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | `string` | `VitePress` | Site title |
| `titleTemplate` | `string \| boolean` | - | Title suffix. Use `:title` to inject page's `<h1>` |
| `description` | `string` | `A VitePress site` | Meta description |
| `head` | `HeadConfig[]` | `[]` | Extra head tags |
| `lang` | `string` | `en-US` | HTML lang attribute |
| `base` | `string` | `/` | Base URL for deployment |

### Routing

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cleanUrls` | `boolean` | `false` | Remove `.html` from URLs |
| `rewrites` | `Record<string, string>` | - | Custom directory <-> URL mappings |

### Build

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `srcDir` | `string` | `.` | Markdown source directory |
| `srcExclude` | `string[]` | - | Glob patterns to exclude |
| `outDir` | `string` | `./.vitepress/dist` | Build output |
| `assetsDir` | `string` | `assets` | Asset subdirectory |
| `cacheDir` | `string` | `./.vitepress/cache` | Cache directory |
| `ignoreDeadLinks` | `boolean \| 'localhostLinks' \| (string \| RegExp \| fn)[]` | `false` | Dead link handling |
| `metaChunk` | `boolean` | `false` | (experimental) Extract metadata to separate chunk |
| `mpa` | `boolean` | `false` | (experimental) MPA mode |

### Theming

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `appearance` | `boolean \| 'dark' \| 'force-dark' \| 'force-auto'` | `true` | Dark mode behavior |
| `lastUpdated` | `boolean` | `false` | Show Git-based last updated |

### Customization

| Option | Type | Description |
|--------|------|-------------|
| `markdown` | `MarkdownOption` | Markdown-it and Shiki config |
| `vite` | `UserConfig` | Raw Vite config |
| `vue` | `@vitejs/plugin-vue` options | Vue plugin options |

## head Config Type

```typescript
type HeadConfig =
  | [string, Record<string, string>]
  | [string, Record<string, string>, string]

// Examples:
head: [['link', { rel: 'icon', href: '/favicon.ico' }]]
head: [
  ['script', { async: '', src: 'https://ga.com/gtag.js' }],
  ['script', {}, `window.dataLayer = ...`]
]
```

## Build Hooks

### buildEnd

```typescript
async buildEnd(siteConfig: SiteConfig)
```
Runs after SSG build finishes, before CLI exits.

### postRender

```typescript
async postRender(context: SSGContext)
interface SSGContext {
  content: string
  teleports?: Record<string, string>
}
```

### transformHead

```typescript
async transformHead(context: TransformContext): HeadConfig[]
interface TransformContext {
  page: string
  assets: string[]
  siteConfig: SiteConfig
  siteData: SiteData
  pageData: PageData
  title: string
  description: string
  head: HeadConfig[]
  content: string
}
```

### transformHtml

```typescript
async transformHtml(code: string, id: string, context: TransformContext): string | void
```

### transformPageData

```typescript
async transformPageData(
  pageData: PageData,
  context: TransformPageContext
): Partial<PageData> | void
interface TransformPageContext {
  siteConfig: SiteConfig
}
```

## Markdown Config

```typescript
markdown: {
  // markdown-it-anchor options
  anchor: { permalink: markdownItAnchor.permalink.headerLink() },
  // @mdit-vue/plugin-toc options
  toc: { level: [1, 2] },
  // Custom markdown-it plugins
  config: (md) => { md.use(plugin) }
}
```

## Full Example

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'My Site',
  description: 'A VitePress site',
  base: '/docs/',
  srcDir: './src',
  cleanUrls: true,
  appearance: 'dark',
  lastUpdated: true,

  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Guide', link: '/guide/' },
      { text: 'Config', link: '/reference/site-config' }
    ],
    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Getting Started', link: '/guide/getting-started' },
          { text: 'Routing', link: '/guide/routing' }
        ]
      }
    ]
  },

  markdown: {
    lineNumbers: true
  },

  async buildEnd(siteConfig) {
    // Generate sitemap, etc.
  }
})
```
