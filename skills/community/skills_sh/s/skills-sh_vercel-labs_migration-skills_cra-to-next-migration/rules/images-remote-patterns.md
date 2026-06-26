---
title: Configure Remote Image Domains
impact: CRITICAL
impactDescription: Required for external images
tags: images, configuration, remote, domains
---

## Configure Remote Image Domains

External images must be explicitly allowed in `next.config.js` for security.

**CRA Pattern (before):**

```tsx
// Any image URL works
<img src="https://any-domain.com/image.jpg" alt="Image" />
```

**Next.js - Without configuration (error):**

```tsx
import Image from 'next/image'

// Error: Invalid src prop, hostname not configured
<Image
  src="https://example.com/image.jpg"
  alt="Image"
  width={800}
  height={600}
/>
```

**Next.js - With configuration (after):**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        port: '',
        pathname: '/images/**',
      },
      {
        protocol: 'https',
        hostname: '**.amazonaws.com',  // Wildcard subdomain
      },
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/**',  // All paths
      },
    ],
  },
}

module.exports = nextConfig
```

**Common services configuration:**

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [
      // AWS S3
      { protocol: 'https', hostname: '**.s3.amazonaws.com' },
      // Cloudinary
      { protocol: 'https', hostname: 'res.cloudinary.com' },
      // Unsplash
      { protocol: 'https', hostname: 'images.unsplash.com' },
      // GitHub avatars
      { protocol: 'https', hostname: 'avatars.githubusercontent.com' },
      // Gravatar
      { protocol: 'https', hostname: '**.gravatar.com' },
    ],
  },
}
```

**Legacy domains config (deprecated):**

```js
// Old way - still works but deprecated
images: {
  domains: ['example.com', 'cdn.example.com'],
}
```

Use `remotePatterns` for more control and security.

**Fallback - Use unoptimized:**

```tsx
// Skip optimization for problematic images
<Image
  src="https://unknown-domain.com/image.jpg"
  unoptimized
  width={400}
  height={300}
  alt="Image"
/>
```

**Or use regular img tag:**

```tsx
// eslint-disable-next-line @next/next/no-img-element
<img src="https://any-domain.com/image.jpg" alt="Image" />
```
