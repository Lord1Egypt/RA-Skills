---
title: Use next/font for Optimization
impact: HIGH
impactDescription: Zero layout shift fonts
tags: fonts, optimization, next-font
---

## Use next/font for Optimization

Replace CSS font imports with `next/font` for automatic optimization and zero layout shift.

**CRA Pattern (before):**

```css
/* src/index.css */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}
```

**Next.js Pattern (after):**

```tsx
// app/layout.tsx
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={roboto.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Benefits of next/font:**
- **Self-hosted**: Fonts downloaded at build time, served from your domain
- **Zero layout shift**: CSS `size-adjust` prevents CLS
- **No external requests**: No runtime calls to Google Fonts
- **Automatic subset**: Only loads needed characters
- **Privacy**: No data sent to Google at runtime

**Using CSS variable:**

```tsx
const roboto = Roboto({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-roboto',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={roboto.variable}>
      <body>{children}</body>
    </html>
  )
}
```

```css
/* Use in CSS */
body {
  font-family: var(--font-roboto);
}
```

**Multiple fonts:**

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

**With Tailwind:**

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)'],
        mono: ['var(--font-roboto-mono)'],
      },
    },
  },
}
```
