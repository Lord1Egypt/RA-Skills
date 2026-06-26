# Data Loading, SSR & i18n Reference

> Source: https://vitepress.dev/guide/data-loading, ssr-compat, i18n

## Build-Time Data Loading

Data loaders execute only at build time, serialized as JSON in bundle.

### Basic Loader

```javascript
// example.data.js
export default {
  load() {
    return { hello: 'world' }
  }
}
```

```vue
<script setup>
import { data } from './example.data.js'
</script>
```

### Async Loader

```javascript
export default {
  async load() {
    return await fetch('https://api.example.com/data').then(r => r.json())
  }
}
```

### Watch Local Files

```javascript
export default {
  watch: ['./data/*.csv'],
  load(watchedFiles) {
    return watchedFiles.map(file => parseFile(file))
  }
}
```

## createContentLoader

```javascript
import { createContentLoader } from 'vitepress'

export default createContentLoader('posts/*.md', {
  includeSrc: true,
  render: true,
  excerpt: true,
  transform(rawData) {
    return rawData
      .sort((a, b) => +new Date(b.frontmatter.date) - +new Date(a.frontmatter.date))
      .map(page => ({
        title: page.frontmatter.title,
        url: page.url,
        date: page.frontmatter.date
      }))
  }
})
```

Returns:

```typescript
interface ContentData {
  url: string
  frontmatter: Record<string, any>
  src?: string
  html?: string
  excerpt?: string
}
```

## Typed Data Loaders

```typescript
import { defineLoader } from 'vitepress'

export interface Data { posts: Post[] }
declare const data: Data
export { data }

export default defineLoader({
  watch: ['./posts/*.md'],
  async load(): Promise<Data> {
    return { posts: [] }
  }
})
```

## SSR Compatibility

### ClientOnly

```vue
<ClientOnly>
  <NonSSRFriendlyComponent />
</ClientOnly>
```

### Browser API on Import

**In mounted hook:**

```vue
onMounted(() => {
  import('./lib-browser-only').then(module => { /* ... */ })
})
```

**Conditional import:**

```javascript
if (!import.meta.env.SSR) {
  import('./lib-browser-only')
}
```

**In enhanceApp:**

```javascript
async enhanceApp({ app }) {
  if (!import.meta.env.SSR) {
    const plugin = await import('plugin-browser-only')
    app.use(plugin.default)
  }
}
```

### defineClientComponent

```vue
<script setup>
import { defineClientComponent } from 'vitepress'

const ClientComp = defineClientComponent(() => {
  return import('component-browser-only')
})
</script>

<template>
  <ClientComp />
</template>
```

## Internationalization (i18n)

### Directory Structure

```
docs/
├─ en/
│  ├─ foo.md
├─ fr/
│  ├─ foo.md
├─ foo.md    # default/root
```

### Config

```typescript
export default {
  locales: {
    root: {
      label: 'English',
      lang: 'en'
    },
    fr: {
      label: 'French',
      lang: 'fr',
      link: '/fr/guide'
      // other locale-specific options...
    }
  }
}
```

### Locale-Specific Properties

```typescript
interface LocaleSpecificConfig<ThemeConfig> {
  lang?: string
  dir?: string
  title?: string
  titleTemplate?: string | boolean
  description?: string
  head?: HeadConfig[]
  themeConfig?: ThemeConfig
}
```

### RTL Support (Experimental)

```typescript
dir: 'rtl'  // in locale config
```

### Redirects

```
/*  /fr/:splat  302  Language=fr
/*  /en/:splat  302
```

Or with cookie persistence:

```vue
<script setup>
import { useData, inBrowser } from 'vitepress'
import { watchEffect } from 'vue'

const { lang } = useData()
watchEffect(() => {
  if (inBrowser) {
    document.cookie = `nf_lang=${lang.value}; expires=...; path=/`
  }
})
</script>
```

### Search i18n

```typescript
search: {
  provider: 'local',
  options: {
    locales: {
      zh: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: { noResultsText: '没有结果', /* ... */ }
        }
      }
    }
  }
}
```
