# Extending Default Theme

> Source: https://vitepress.dev/guide/extending-default-theme

## Customizing CSS

```javascript
// theme/index.js
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default DefaultTheme
```

```css
/* custom.css */
:root {
  --vp-c-brand-1: #646cff;
  --vp-c-brand-2: #747bff;
}
```

## Using Different Fonts

```javascript
import DefaultTheme from 'vitepress/theme-without-fonts'
import './my-fonts.css'
```

```css
:root {
  --vp-font-family-base: /* main font */
  --vp-font-family-mono: /* code font */
}
```

## Registering Global Components

```javascript
// theme/index.js
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('MyGlobalComponent', MyGlobalComponent)
  }
}
```

## Layout Slots

```vue
<!-- MyLayout.vue -->
<template>
  <Layout>
    <template #aside-outline-before>
      My custom sidebar top content
    </template>
  </Layout>
</template>
```

Or with render functions:

```javascript
import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'

export default {
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'aside-outline-before': () => h(MyComponent)
    })
  }
}
```

### Slot Locations

**doc layout:**
- `doc-top`, `doc-bottom`
- `doc-footer-before`, `doc-before`, `doc-after`
- `sidebar-nav-before`, `sidebar-nav-after`
- `aside-top`, `aside-bottom`
- `aside-outline-before`, `aside-outline-after`
- `aside-ads-before`, `aside-ads-after`

**home layout:**
- `home-hero-before`, `home-hero-info`, `home-hero-info-after`
- `home-hero-actions-before`, `home-hero-actions-after`
- `home-hero-image`, `home-hero-after`
- `home-features-before`, `home-features-after`

**page layout:**
- `page-top`, `page-bottom`

**Always:**
- `layout-top`, `layout-bottom`
- `nav-bar-title-before`, `nav-bar-title-after`
- `nav-bar-content-before`, `nav-bar-content-after`
- `not-found`

## View Transitions

```vue
<script setup>
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { nextTick, provide } from 'vue'

const { isDark } = useData()

provide('toggle-appearance', async ({ clientX: x, clientY: y }) => {
  if (!('startViewTransition' in document)) {
    isDark.value = !isDark.value
    return
  }
  // ... view transition implementation
})
</script>

<template>
  <DefaultTheme.Layout />
</template>
```

## Overriding Internal Components

```typescript
import { fileURLToPath, URL } from 'node:url'

export default {
  vite: {
    resolve: {
      alias: [{ find: /^.*\/VPNavBar\.vue$/, replacement: './theme/components/CustomNavBar.vue' }]
    }
  }
}
```
