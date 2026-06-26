---
title: Use Static Imports for Assets
impact: MEDIUM
impactDescription: Better asset handling
tags: assets, imports, static
---

## Use Static Imports for Assets

Import images and other assets directly for automatic optimization and type safety.

**CRA Pattern (before):**

```tsx
// src/components/Logo.tsx
import logo from './logo.png'

export function Logo() {
  return <img src={logo} alt="Logo" />
}
```

**Next.js Pattern (after):**

```tsx
// components/Logo.tsx
import Image from 'next/image'
import logo from './logo.png'

export function Logo() {
  return (
    <Image
      src={logo}        // StaticImageData - includes dimensions
      alt="Logo"
      // width and height inferred from import
    />
  )
}
```

**Benefits of static imports in Next.js:**
- Automatic width/height detection
- Prevents Cumulative Layout Shift
- Enables blur placeholder
- Optimized at build time

**With blur placeholder:**

```tsx
import Image from 'next/image'
import heroImage from './hero.jpg'

export function Hero() {
  return (
    <Image
      src={heroImage}
      alt="Hero"
      placeholder="blur" // Automatic blur placeholder from import
    />
  )
}
```

**Importing other assets:**

```tsx
// JSON data
import data from './data.json'

// Fonts (prefer next/font instead)
import fontFile from './font.woff2'
```

## SVG Migration from CRA

CRA supports importing SVGs as React components using a special syntax that does not work in Next.js.

**CRA SVG pattern (does NOT work in Next.js):**

```tsx
// CRA allows this - Next.js does NOT
import { ReactComponent as Logo } from './logo.svg'
import { ReactComponent as Icon } from './icon.svg'

function Header() {
  return (
    <header>
      <Logo className="logo" />
      <Icon width={24} height={24} />
    </header>
  )
}
```

**Option 1: Use next/image for SVGs (Recommended for most cases)**

```tsx
import Image from 'next/image'
import logoSvg from './logo.svg'

function Header() {
  return (
    <header>
      <Image
        src={logoSvg}
        alt="Logo"
        width={100}
        height={40}
      />
    </header>
  )
}
```

Note: With `next/image`, you must provide explicit `width` and `height` props for SVGs - they are not automatically inferred like with raster images. If the original code uses CSS for sizing (e.g., `className="logo"` with CSS rules), you'll need to extract those dimensions.

For responsive SVGs with CSS-based sizing, use the `fill` prop with a sized container:

```tsx
<div style={{ position: 'relative', width: '100px', height: '40px' }}>
  <Image src={logoSvg} alt="Logo" fill />
</div>
```

**Option 2: Configure @svgr/webpack for component imports**

If you need SVGs as React components (for styling, animations, or dynamic manipulation):

```bash
npm install --save-dev @svgr/webpack
```

```js
// next.config.js
module.exports = {
  webpack(config) {
    // Find the existing rule that handles SVG imports
    const fileLoaderRule = config.module.rules.find((rule) =>
      rule.test?.test?.('.svg'),
    )

    config.module.rules.push(
      // Reapply the existing rule, but only for svg imports ending in ?url
      {
        ...fileLoaderRule,
        test: /\.svg$/i,
        resourceQuery: /url/, // *.svg?url
      },
      // Convert all other *.svg imports to React components
      {
        test: /\.svg$/i,
        issuer: fileLoaderRule.issuer,
        resourceQuery: { not: [...fileLoaderRule.resourceQuery.not, /url/] },
        use: ['@svgr/webpack'],
      },
    )

    // Modify the file loader rule to ignore *.svg
    fileLoaderRule.exclude = /\.svg$/i

    return config
  },
}
```

Then use SVGs as components:

```tsx
import Logo from './logo.svg'
import Image from 'next/image'
import iconUrl from './icon.svg?url'

function Header() {
  return (
    <header>
      <Logo className="logo" />           {/* As component */}
      <Image src={iconUrl} alt="Icon" />  {/* As image */}
    </header>
  )
}
```

**SVG Migration checklist:**

1. Search for `{ ReactComponent as` imports in your codebase
2. Decide per-SVG: use `next/image` or convert to SVGR component
3. For `next/image`, add explicit `width` and `height` props (check CSS for dimensions if needed)
4. For SVGs needing manipulation, install and configure `@svgr/webpack`
5. Update all import statements accordingly

**Search for CRA SVG imports:**

```bash
grep -r "ReactComponent as" --include="*.tsx" --include="*.ts" --include="*.jsx" --include="*.js"
```
