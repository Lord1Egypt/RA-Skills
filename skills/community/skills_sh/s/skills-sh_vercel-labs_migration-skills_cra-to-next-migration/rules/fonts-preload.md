---
title: Understand Automatic Font Preloading
impact: LOW
impactDescription: Fonts preloaded automatically
tags: fonts, preload, performance
---

## Understand Automatic Font Preloading

Next.js automatically preloads fonts configured with `next/font`. No manual preload links needed.

**CRA Pattern (before):**

```html
<!-- Manual preload in index.html -->
<link
  rel="preload"
  href="/fonts/inter.woff2"
  as="font"
  type="font/woff2"
  crossorigin
>
```

**Next.js Pattern (after):**

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
// Font is automatically:
// 1. Downloaded at build time
// 2. Self-hosted from your domain
// 3. Preloaded in the HTML head

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

**What Next.js does automatically:**
1. Downloads font files at build time
2. Generates optimized CSS with `size-adjust`
3. Injects preload links in HTML head
4. Serves fonts from your domain (no external requests)

**Controlling preload:**

```tsx
// Disable preload for non-critical fonts
const decorativeFont = Pacifico({
  subsets: ['latin'],
  preload: false,  // Don't preload this font
})
```

**Generated HTML:**

```html
<!-- Next.js generates this automatically -->
<link
  rel="preload"
  href="/_next/static/media/inter.woff2"
  as="font"
  type="font/woff2"
  crossorigin
>
<style>
  /* CSS with size-adjust for zero CLS */
</style>
```

**Summary:** Just use `next/font` and preloading is handled automatically. No manual `<link rel="preload">` needed.
