# VitePress Theme Customization

## Custom Styles

### Method 1: Inline Styles

In `.vitepress/theme/index.ts`:

```typescript
import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    // Custom logic
  }
}
```

### Method 2: CSS Variable Overrides

Create `.vitepress/theme/custom.css`:

```css
:root {
  --vp-c-brand: #007acc;
  --vp-c-brand-light: #0094e6;
  --vp-font-family-base: 'Inter', sans-serif;
}

.dark {
  --vp-c-brand: #0094e6;
}
```

## Custom Layout

### Adding Custom Components

```vue
<!-- .vitepress/components/MyComponent.vue -->
<template>
  <div class="my-component">
    <slot />
  </div>
</template>
```

Register in `index.ts`:

```typescript
import MyComponent from '../components/MyComponent.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('MyComponent', MyComponent)
  }
}
```

## Common CSS Variables

```css
/* Colors */
--vp-c-brand          /* Primary color */
--vp-c-text-1         /* Main text color */
--vp-c-bg             /* Background color */

/* Fonts */
--vp-font-family-base /* Base font */
--vp-font-family-mono /* Code font */

/* Dimensions */
--vp-nav-height       /* Navbar height */
--vp-sidebar-width    /* Sidebar width */
```

## Dark Mode Customization

```css
.dark {
  --vp-c-brand: #your-dark-theme-color;
  --vp-c-bg: #1a1a1a;
}
```