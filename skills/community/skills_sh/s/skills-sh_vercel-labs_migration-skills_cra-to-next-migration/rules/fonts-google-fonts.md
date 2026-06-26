---
title: Load Google Fonts Properly
impact: HIGH
impactDescription: Optimized Google Font loading
tags: fonts, google-fonts, next-font
---

## Load Google Fonts Properly

Use `next/font/google` to load Google Fonts with automatic optimization.

**CRA Pattern (before):**

```html
<!-- public/index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Next.js Pattern (after):**

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Variable fonts (recommended):**

```tsx
import { Inter } from 'next/font/google'

// Variable font - all weights included
const inter = Inter({
  subsets: ['latin'],
})

// Use any weight in CSS
// font-weight: 100 to 900
```

**Static fonts (specific weights):**

```tsx
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: ['400', '700'],  // Only these weights
  style: ['normal', 'italic'],
  subsets: ['latin'],
})
```

**Multiple fonts:**

```tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```
