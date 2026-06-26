---
title: Configure Static Export
impact: MEDIUM
impactDescription: Pure static site generation
tags: build, static-export, ssg
---

## Configure Static Export

Export your Next.js app as a static site, similar to CRA's build output.

**When to use static export:**
- No server-side features needed
- Deploying to static hosts (S3, GitHub Pages)
- Simple static websites
- CRA-like deployment model

**Configuration:**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // Optional: Add trailing slashes
  trailingSlash: true,
  // Optional: Disable image optimization (not available in static)
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
```

**Build output:**

```bash
npm run build
# Outputs to 'out/' directory

out/
├── index.html
├── about/
│   └── index.html
├── blog/
│   ├── index.html
│   └── post-1/
│       └── index.html
├── _next/
│   └── static/
└── favicon.ico
```

**Limitations (not supported in static export):**
- Server-side rendering (SSR)
- API routes
- Middleware
- Image optimization
- Internationalized routing
- Dynamic routes without `generateStaticParams`

**Dynamic routes with static export:**

```tsx
// app/blog/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await fetchAllPosts()
  return posts.map((post) => ({
    slug: post.slug,
  }))
}

export default function BlogPost({ params }) {
  // ...
}
```

**Deploying:**

```bash
# Deploy 'out/' to any static host
npx serve out
# or
aws s3 sync out/ s3://my-bucket
```
