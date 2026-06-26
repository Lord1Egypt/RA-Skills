---
title: Configure Blur Placeholders
impact: MEDIUM
impactDescription: Better loading experience
tags: images, placeholder, blur, ux
---

## Configure Blur Placeholders

Use blur placeholders to improve perceived performance while images load.

**CRA Pattern (before):**

```tsx
// Manual placeholder implementation
const [loaded, setLoaded] = useState(false)

<div className="image-wrapper">
  {!loaded && <div className="placeholder" />}
  <img
    src="/photo.jpg"
    alt="Photo"
    onLoad={() => setLoaded(true)}
    className={loaded ? 'visible' : 'hidden'}
  />
</div>
```

**Next.js - Static import (automatic blur):**

```tsx
import Image from 'next/image'
import photo from './photo.jpg'

// Blur placeholder generated automatically from static import
<Image
  src={photo}
  alt="Photo"
  placeholder="blur"
/>
```

**Next.js - Remote images (manual blurDataURL):**

```tsx
import Image from 'next/image'

// Generate blurDataURL at build time or use a service
<Image
  src="https://example.com/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
/>
```

**Generating blurDataURL:**

```tsx
// Using plaiceholder library
import { getPlaiceholder } from 'plaiceholder'

export async function getStaticProps() {
  const { base64 } = await getPlaiceholder('/path/to/image.jpg')

  return {
    props: {
      blurDataURL: base64,
    },
  }
}
```

**Simple placeholder options:**

```tsx
// Color placeholder (no blur)
<Image
  src={url}
  alt="Photo"
  placeholder="empty"  // Default - no placeholder
/>

// Blur with static import
<Image
  src={staticImage}
  placeholder="blur"  // Auto-generated from import
/>
```
