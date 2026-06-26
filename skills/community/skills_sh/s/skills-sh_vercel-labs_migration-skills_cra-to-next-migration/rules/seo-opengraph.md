---
title: Configure Open Graph Metadata
impact: MEDIUM
impactDescription: Social media previews
tags: seo, opengraph, social
---

## Configure Open Graph Metadata

Configure Open Graph metadata for rich social media previews.

**CRA with react-helmet (before):**

```tsx
<Helmet>
  <meta property="og:title" content="Page Title" />
  <meta property="og:description" content="Page description" />
  <meta property="og:image" content="https://example.com/image.jpg" />
  <meta property="og:url" content="https://example.com/page" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="My Site" />
</Helmet>
```

**Next.js Metadata API (after):**

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  openGraph: {
    title: 'Page Title',
    description: 'Page description',
    url: 'https://example.com/page',
    siteName: 'My Site',
    images: [
      {
        url: 'https://example.com/image.jpg',
        width: 1200,
        height: 630,
        alt: 'Preview image',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
}
```

**Article type (for blog posts):**

```tsx
export const metadata: Metadata = {
  openGraph: {
    title: 'Blog Post Title',
    description: 'Post excerpt',
    type: 'article',
    publishedTime: '2024-01-01T00:00:00Z',
    modifiedTime: '2024-01-02T00:00:00Z',
    authors: ['Author Name'],
    tags: ['tech', 'react'],
  },
}
```

**Default OG image in layout:**

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  openGraph: {
    images: [
      {
        url: '/default-og.jpg',
        width: 1200,
        height: 630,
      },
    ],
  },
}
```

**Dynamic OG image:**

```tsx
// app/blog/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'

export default async function Image({ params }) {
  const post = await fetchPost(params.slug)

  return new ImageResponse(
    <div style={{ /* ... */ }}>{post.title}</div>,
    { width: 1200, height: 630 }
  )
}
```
