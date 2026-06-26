---
title: Provide Width and Height
impact: HIGH
impactDescription: Prevents layout shift
tags: images, dimensions, cls
---

## Provide Width and Height

Next.js Image requires width and height to prevent Cumulative Layout Shift (CLS).

**CRA Pattern (before):**

```tsx
// No dimensions required (but causes layout shift)
<img src="/photo.jpg" alt="Photo" />
```

**Next.js Pattern (after):**

```tsx
import Image from 'next/image'

// Option 1: Explicit dimensions
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>

// Option 2: Static import (dimensions inferred)
import photo from './photo.jpg'
<Image src={photo} alt="Photo" />

// Option 3: Fill prop (requires positioned parent)
<div style={{ position: 'relative', width: '100%', height: '400px' }}>
  <Image
    src="/photo.jpg"
    alt="Photo"
    fill
    style={{ objectFit: 'cover' }}
  />
</div>
```

**Determining dimensions:**

1. **Known dimensions:** Use actual width/height
2. **Static import:** Dimensions auto-detected
3. **Responsive:** Use `fill` with sized parent
4. **Aspect ratio:** Use `fill` with aspect-ratio CSS

**Common pattern for responsive images:**

```tsx
// Fixed aspect ratio container
<div className="relative aspect-video">
  <Image
    src={imageUrl}
    alt="Video thumbnail"
    fill
    className="object-cover"
  />
</div>
```

```css
/* If not using Tailwind */
.relative { position: relative; }
.aspect-video { aspect-ratio: 16 / 9; }
.object-cover { object-fit: cover; }
```

**Warning: width/height props override CSS sizing**

The `width` and `height` props on next/image create a fixed container that can override CSS sizing rules. This is a common issue when migrating CRA apps that use viewport-relative CSS units.

```tsx
// PROBLEM: CSS height: 40vmin is overridden by width={300} height={300}
<Image src="/logo.svg" width={300} height={300} className="logo" />

// SOLUTION: For SVGs or images needing CSS-based sizing, use regular <img>
<img src="/logo.svg" className="logo" alt="Logo" />
```

If you need CSS to control the image size (especially with `vmin`, `vmax`, `vh`, `vw` units), use a regular `<img>` tag instead of next/image. See `images-next-image.md` for details.
