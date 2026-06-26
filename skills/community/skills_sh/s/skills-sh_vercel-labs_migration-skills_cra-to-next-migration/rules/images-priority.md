---
title: Use Priority for LCP Images
impact: HIGH
impactDescription: Improves largest contentful paint
tags: images, performance, lcp, priority
---

## Use Priority for LCP Images

Add `priority` to images that are the Largest Contentful Paint (LCP) element for better performance.

**CRA Pattern (before):**

```tsx
// No built-in optimization for critical images
<img src="/hero.jpg" alt="Hero" />
```

**Next.js Pattern (after):**

```tsx
import Image from 'next/image'

// Hero image - likely LCP element
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  priority  // Preloads this image
/>
```

**When to use `priority`:**
- Hero images above the fold
- Product images on detail pages
- Featured content images
- Any image that's the LCP element

**When NOT to use `priority`:**
- Images below the fold
- Gallery/carousel images
- Lazy-loaded content
- Multiple images (only 1-2 should be priority)

**Checking LCP:**
1. Open Chrome DevTools
2. Go to Performance tab
3. Run Lighthouse
4. Check "Largest Contentful Paint element"

**Common patterns:**

```tsx
// Hero section
export function Hero() {
  return (
    <section>
      <Image
        src="/hero.jpg"
        alt="Welcome"
        width={1920}
        height={800}
        priority  // Always preload hero
      />
      <h1>Welcome to our site</h1>
    </section>
  )
}

// Blog post - featured image
export function BlogPost({ post }) {
  return (
    <article>
      <Image
        src={post.featuredImage}
        alt={post.title}
        width={800}
        height={450}
        priority  // First visible image
      />
      <h1>{post.title}</h1>
    </article>
  )
}
```
