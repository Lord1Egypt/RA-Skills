---
title: Understand Automatic Optimization
impact: MEDIUM
impactDescription: Know what Next.js does
tags: images, optimization, webp, avif
---

## Understand Automatic Optimization

Next.js automatically optimizes images on-demand. Understand how it works.

**CRA (no automatic optimization):**

```tsx
// Image served as-is
<img src="/large-photo.jpg" /> // 2MB JPEG served directly
```

**Next.js automatic optimization:**

```tsx
import Image from 'next/image'

// Same image, automatically:
// - Converted to WebP/AVIF
// - Resized to requested size
// - Cached for subsequent requests
<Image
  src="/large-photo.jpg"
  width={800}
  height={600}
  alt="Photo"
/>
```

**What Next.js does automatically:**
1. **Format conversion**: JPEG → WebP/AVIF (based on browser support)
2. **Resizing**: Generates multiple sizes based on `sizes` prop
3. **Quality optimization**: Default 75% quality (configurable)
4. **Lazy loading**: Images load when entering viewport
5. **Caching**: Optimized images cached on server

**Configuration options:**

```js
// next.config.js
module.exports = {
  images: {
    // Supported formats
    formats: ['image/avif', 'image/webp'],

    // Device sizes for responsive images
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],

    // Image sizes for the sizes attribute
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],

    // Minimum cache TTL
    minimumCacheTTL: 60,

    // Disable optimization for specific paths
    unoptimized: false,
  },
}
```

**Disable optimization for specific images:**

```tsx
// When you don't want optimization (e.g., animated GIFs)
<Image
  src="/animation.gif"
  unoptimized
  alt="Animation"
  width={300}
  height={200}
/>
```

**Static export (no server):**

```js
// next.config.js
module.exports = {
  output: 'export',
  images: {
    unoptimized: true, // Required for static export
  },
}
```
