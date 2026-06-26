---
title: Configure font-display Strategy
impact: MEDIUM
impactDescription: Control font loading behavior
tags: fonts, font-display, loading
---

## Configure font-display Strategy

Configure how fonts are displayed while loading with the `display` option.

**CRA Pattern (before):**

```css
@font-face {
  font-family: 'CustomFont';
  src: url('./font.woff2');
  font-display: swap;  /* Show fallback, swap when loaded */
}
```

```html
<!-- Or in Google Fonts URL -->
<link href="https://fonts.googleapis.com/css2?family=Inter&display=swap">
```

**Next.js Pattern (after):**

```tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Same behavior
})
```

**Display options:**

| Value | Behavior |
|-------|----------|
| `auto` | Browser default |
| `block` | Hide text until font loads (up to 3s) |
| `swap` | Show fallback immediately, swap when ready |
| `fallback` | Short block period, then fallback |
| `optional` | Font may not be used if slow connection |

**Recommendations:**

```tsx
// For body text - use swap
const bodyFont = Inter({
  subsets: ['latin'],
  display: 'swap',
})

// For icons/symbols - use block
const iconFont = localFont({
  src: '../fonts/icons.woff2',
  display: 'block',  // Prevent icon flash
})

// For non-critical decorative fonts
const decorativeFont = Pacifico({
  subsets: ['latin'],
  display: 'optional',  // Skip if slow connection
})
```

**Default behavior:**

```tsx
// next/font defaults to 'swap' which is recommended
const font = Inter({ subsets: ['latin'] })
// display: 'swap' is applied automatically
```
