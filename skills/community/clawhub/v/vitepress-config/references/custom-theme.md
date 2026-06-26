# Custom Theme Reference

> Source: https://vitepress.dev/guide/custom-theme

## Theme Resolving

Create `.vitepress/theme/index.js`:

```
docs/
├─ .vitepress/
│  ├─ theme/
│  │  └─ index.js   # theme entry
│  └─ config.js
└─ index.md
```

VitePress uses custom theme when `theme/index.js` exists.

## Theme Interface

```typescript
interface Theme {
  Layout: Component           // required
  enhanceApp?: (ctx) => Awaitable<void>  // optional
  extends?: Theme            // optional
}

interface EnhanceAppContext {
  app: App
  router: Router
  siteData: Ref<SiteData>
}
```

## Basic Layout

```vue
<!-- .vitepress/theme/Layout.vue -->
<template>
  <h1>Custom Layout!</h1>
  <Content />
</template>
```

### Handle 404

```vue
<script setup>
import { useData } from 'vitepress'
const { page } = useData()
</script>

<template>
  <div v-if="page.isNotFound">Custom 404!</div>
  <Content v-else />
</template>
```

### Handle Layout Types

```vue
<script setup>
import { useData } from 'vitepress'
const { page, frontmatter } = useData()
</script>

<template>
  <div v-if="frontmatter.layout === 'home'">Home layout</div>
  <Content v-else />
</template>
```

## Enhancing App

```javascript
// theme/index.js
import Layout from './Layout.vue'
import MyComponent from './MyComponent.vue'

export default {
  Layout,
  enhanceApp({ app, router, siteData }) {
    app.component('MyComponent', MyComponent)
  }
}
```

## Extending Themes

```javascript
import BaseTheme from 'awesome-vitepress-theme'

export default {
  extends: BaseTheme,
  enhanceApp({ app }) {
    // extend the base theme
  }
}
```

## Distributing Themes

### As npm Package

1. Export theme as default
2. Export `ThemeConfig` type
3. Export config at `my-theme/config` for special configs
4. Document usage

```javascript
// package.json entry
export default Theme

// types
export interface ThemeConfig { ... }

// optional special config
export const config = { ... }
```

### As Template Repository

Create GitHub template repository.

## TypeScript

```typescript
// theme/index.ts
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'

export default {
  extends: DefaultTheme,
  Layout: MyLayout
} satisfies Theme
```
