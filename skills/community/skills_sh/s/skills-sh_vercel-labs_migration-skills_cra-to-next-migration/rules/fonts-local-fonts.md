---
title: Load Local Font Files
impact: MEDIUM
impactDescription: Self-hosted custom fonts
tags: fonts, local-fonts, custom
---

## Load Local Font Files

Use `next/font/local` to load custom font files with the same optimization benefits.

**CRA Pattern (before):**

```css
/* src/fonts.css */
@font-face {
  font-family: 'CustomFont';
  src: url('./fonts/CustomFont-Regular.woff2') format('woff2'),
       url('./fonts/CustomFont-Regular.woff') format('woff');
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: 'CustomFont';
  src: url('./fonts/CustomFont-Bold.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}

body {
  font-family: 'CustomFont', sans-serif;
}
```

**Next.js Pattern (after):**

```tsx
// app/layout.tsx
import localFont from 'next/font/local'

const customFont = localFont({
  src: [
    {
      path: '../fonts/CustomFont-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../fonts/CustomFont-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-custom',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={customFont.variable}>
      <body>{children}</body>
    </html>
  )
}
```

**Single font file:**

```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: '../fonts/MyFont.woff2',
})

export default function Layout({ children }) {
  return <main className={myFont.className}>{children}</main>
}
```

**Variable font file:**

```tsx
import localFont from 'next/font/local'

const myVariableFont = localFont({
  src: '../fonts/MyVariableFont.woff2',
  variable: '--font-my-variable',
})
```

Font files should be placed in your project (e.g., `fonts/` directory).
