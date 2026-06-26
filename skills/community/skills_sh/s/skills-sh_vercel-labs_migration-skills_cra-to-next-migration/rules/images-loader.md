---
title: Configure Custom Image Loaders
impact: LOW
impactDescription: For custom CDN integration
tags: images, loader, cdn, cloudinary
---

## Configure Custom Image Loaders

Use custom loaders when using image CDNs like Cloudinary, Imgix, or custom solutions.

**CRA Pattern (before):**

```tsx
// Manual URL construction
const cloudinaryUrl = `https://res.cloudinary.com/demo/image/upload/w_${width},h_${height}/${imageId}`

<img src={cloudinaryUrl} alt="Image" />
```

**Next.js - Custom loader (after):**

```tsx
// lib/imageLoader.ts
export default function cloudinaryLoader({
  src,
  width,
  quality,
}: {
  src: string
  width: number
  quality?: number
}) {
  const params = ['f_auto', 'c_limit', `w_${width}`, `q_${quality || 'auto'}`]
  return `https://res.cloudinary.com/demo/image/upload/${params.join(',')}${src}`
}
```

```tsx
// components/CloudinaryImage.tsx
import Image from 'next/image'
import cloudinaryLoader from '@/lib/imageLoader'

export function CloudinaryImage({ src, alt, ...props }) {
  return (
    <Image
      loader={cloudinaryLoader}
      src={src}
      alt={alt}
      {...props}
    />
  )
}
```

**Global loader configuration:**

```js
// next.config.js
module.exports = {
  images: {
    loader: 'custom',
    loaderFile: './lib/imageLoader.ts',
  },
}
```

**Built-in loaders:**

```js
// next.config.js
module.exports = {
  images: {
    loader: 'cloudinary',
    path: 'https://res.cloudinary.com/demo/image/upload/',
  },
}
```

Supported built-in loaders:
- `default` - Next.js Image Optimization
- `cloudinary`
- `imgix`
- `akamai`
- `custom` - Your own loader
