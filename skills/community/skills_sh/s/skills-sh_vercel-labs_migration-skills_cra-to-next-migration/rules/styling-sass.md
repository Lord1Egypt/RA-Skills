---
title: Configure Sass Support
impact: LOW
impactDescription: Requires package installation
tags: styling, sass, scss
---

## Configure Sass Support

CRA includes Sass support after installing `sass`. Next.js works the same way.

**CRA Setup (before):**

```bash
npm install sass
```

```scss
// src/styles/variables.scss
$primary-color: #0070f3;
$spacing: 8px;

// src/components/Button.module.scss
@import '../styles/variables';

.button {
  background: $primary-color;
  padding: $spacing * 2;
}
```

**Next.js Setup (after):**

```bash
npm install sass
```

```scss
// styles/variables.scss
$primary-color: #0070f3;
$spacing: 8px;

// components/Button.module.scss
@use '../styles/variables' as *;

.button {
  background: $primary-color;
  padding: $spacing * 2;
}
```

**Configure Sass options:**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  sassOptions: {
    includePaths: ['./styles'],
    prependData: `@import "variables.scss";`,
  },
}

module.exports = nextConfig
```

**Global Sass in layout:**

```tsx
// app/layout.tsx
import './globals.scss' // Works with .scss files

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**Note:** Use `@use` instead of `@import` for Sass as `@import` is deprecated.
