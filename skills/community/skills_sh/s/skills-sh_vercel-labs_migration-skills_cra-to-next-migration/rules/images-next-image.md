---
title: Replace img with next/image
impact: HIGH
impactDescription: Automatic image optimization
tags: images, optimization, next-image
---

## Replace img with next/image

Replace HTML `<img>` tags with Next.js `<Image>` component for automatic optimization.

**CRA Pattern (before):**

```tsx
// src/components/Product.tsx
export function Product({ product }) {
  return (
    <div>
      <img
        src={product.imageUrl}
        alt={product.name}
        className="product-image"
      />
      <h2>{product.name}</h2>
    </div>
  )
}
```

**Next.js Pattern (after):**

```tsx
// components/Product.tsx
import Image from 'next/image'

export function Product({ product }) {
  return (
    <div>
      <Image
        src={product.imageUrl}
        alt={product.name}
        width={400}
        height={300}
        className="product-image"
      />
      <h2>{product.name}</h2>
    </div>
  )
}
```

**Benefits of next/image:**
- Automatic WebP/AVIF conversion
- Responsive image generation
- Lazy loading by default
- Prevents Cumulative Layout Shift
- On-demand optimization

**With static imports (best practice):**

```tsx
import Image from 'next/image'
import productPhoto from './product.jpg'

export function Product() {
  return (
    <Image
      src={productPhoto}
      alt="Product"
      // width/height inferred from import
      placeholder="blur"  // Automatic blur placeholder
    />
  )
}
```

**When to keep using `<img>` instead of next/image:**

1. **SVG images with CSS-based sizing** - SVGs are already optimized vector graphics and don't benefit from next/image optimization. More importantly, next/image's required width/height props create a fixed container that overrides CSS sizing rules like `height: 40vmin`.

```tsx
// CRA logo with CSS sizing - KEEP as <img>
// BAD: next/image width/height will override CSS
<Image src="/logo.svg" alt="Logo" width={300} height={300} className="App-logo" />

// GOOD: Regular <img> respects CSS sizing exactly
<img src="/logo.svg" alt="Logo" className="App-logo" />
```

```css
.App-logo {
  height: 40vmin;  /* This works with <img>, but NOT with next/image */
  pointer-events: none;
}
```

2. **SVG icons** - Use inline SVG or a regular `<img>` tag
3. **Tiny images (< 1KB)** - Optimization overhead isn't worth it
4. **Images requiring viewport-relative CSS sizing** - When you need `vmin`, `vmax`, `vh`, `vw` units to control image size
