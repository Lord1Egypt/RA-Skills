# Runtime API Reference

> Source: https://vitepress.dev/reference/runtime-api

Import from `vitepress`. Methods starting with `use*` are Vue Composition API composables.

## useData

```typescript
const {
  site,           // Ref<SiteData<T>>
  theme,          // Ref<T> (themeConfig)
  page,           // Ref<PageData>
  frontmatter,    // Ref<PageData['frontmatter']>
  params,         // Ref<PageData['params']>
  title,          // Ref<string>
  description,    // Ref<string>
  lang,           // Ref<string>
  isDark,         // Ref<boolean>
  dir,            // Ref<string>
  localeIndex,    // Ref<string>
  hash            // Ref<string>
} = useData()
```

### PageData Type

```typescript
interface PageData {
  title: string
  titleTemplate?: string | boolean
  description: string
  relativePath: string
  filePath: string
  headers: Header[]
  frontmatter: Record<string, any>
  params?: Record<string, any>
  isNotFound?: boolean
  lastUpdated?: number
}
```

## useRoute

```typescript
const { path, data, component } = useRoute()
```

## useRouter

```typescript
const router = useRouter()

router.go(to)                              // Navigate
router.onBeforeRouteChange((to) => ...)     // Before navigation
router.onBeforePageLoad((to) => ...)       // Before page loads
router.onAfterPageLoad((to) => ...)        // After page loads
router.onAfterRouteChange((to) => ...)      // After route changes
```

## withBase

```typescript
withBase(path: string): string
```

Appends configured `base` to URL path. Use for dynamic asset paths:

```vue
<img :src="withBase(theme.logoPath)" />
```

## Components

### Content

Renders markdown content:

```vue
<template>
  <h1>Custom Layout!</h1>
  <Content />
</template>
```

### ClientOnly

Renders slot only at client side (SSR safety):

```vue
<ClientOnly>
  <NonSSRFriendlyComponent />
</ClientOnly>
```

## Template Globals

### $frontmatter

Access current page's frontmatter:

```md
# {{ $frontmatter.title }}
```

### $params

Access dynamic route params:

```md
- package: {{ $params.pkg }}
- version: {{ $params.version }}
```

## Full Example

```vue
<script setup>
import { useData, useRoute, useRouter, withBase, Content, ClientOnly } from 'vitepress'

const { site, theme, page, frontmatter, params, title, isDark } = useData()
const { path } = useRoute()
const router = useRouter()

function navigate() {
  router.go('/guide/')
}
</script>

<template>
  <h1>{{ title }}</h1>
  <Content />

  <div v-if="frontmatter.showWidget">
    <ClientOnly>
      <SomeWidget />
    </ClientOnly>
  </div>

  <img :src="withBase('/logo.png')" />
</template>
```
