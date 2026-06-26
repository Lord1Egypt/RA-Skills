---
title: Configure Variable Fonts
impact: MEDIUM
impactDescription: Single file, all weights
tags: fonts, variable-fonts, optimization
---

## Configure Variable Fonts

Variable fonts provide all weights in a single file, improving performance.

**CRA Pattern (before):**

```css
/* Multiple font files for different weights */
@font-face {
  font-family: 'Inter';
  src: url('./fonts/Inter-Regular.woff2');
  font-weight: 400;
}
@font-face {
  font-family: 'Inter';
  src: url('./fonts/Inter-Medium.woff2');
  font-weight: 500;
}
@font-face {
  font-family: 'Inter';
  src: url('./fonts/Inter-Bold.woff2');
  font-weight: 700;
}
```

**Next.js - Google variable font:**

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

// Inter is a variable font - one file, all weights
const inter = Inter({
  subsets: ['latin'],
  // No 'weight' prop needed - includes all weights
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Next.js - Local variable font:**

```tsx
import localFont from 'next/font/local'

const interVariable = localFont({
  src: '../fonts/Inter-VariableFont.woff2',
  variable: '--font-inter',
})
```

**Using in CSS:**

```css
/* Can use any weight from 100-900 */
.heading {
  font-weight: 700;
}

.body {
  font-weight: 400;
}

.light {
  font-weight: 300;
}
```

**Benefits:**
- Single file for all weights
- Smaller total download
- Smooth weight transitions possible
- Better caching
