---
title: Use Fill for Responsive Images
impact: MEDIUM
impactDescription: Flexible image sizing
tags: images, responsive, fill
---

## Use Fill for Responsive Images

Use the `fill` prop when you want images to fill their parent container responsively.

**CRA Pattern (before):**

```tsx
// CSS handles sizing
<div className="image-container">
  <img src="/hero.jpg" alt="Hero" />
</div>
```

```css
.image-container {
  position: relative;
  width: 100%;
  height: 400px;
}
.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Next.js Pattern (after):**

```tsx
import Image from 'next/image'

// Parent must have position: relative and defined dimensions
<div className="relative w-full h-[400px]">
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    style={{ objectFit: 'cover' }}
  />
</div>
```

**With Tailwind CSS:**

```tsx
// Aspect ratio container
<div className="relative aspect-video">
  <Image
    src="/video-thumb.jpg"
    alt="Thumbnail"
    fill
    className="object-cover"
  />
</div>

// Fixed height container
<div className="relative h-96 w-full">
  <Image
    src="/banner.jpg"
    alt="Banner"
    fill
    className="object-cover"
  />
</div>
```

**With sizes for responsive optimization:**

```tsx
<div className="relative aspect-square">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    className="object-contain"
  />
</div>
```

**Important:** Parent element MUST have:
- `position: relative` (or absolute/fixed)
- Defined dimensions (width AND height, or aspect-ratio)
