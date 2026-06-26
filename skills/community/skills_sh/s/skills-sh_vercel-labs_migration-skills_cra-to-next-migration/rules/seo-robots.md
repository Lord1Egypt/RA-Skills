---
title: Configure Robots Meta Tags
impact: MEDIUM
impactDescription: Control search indexing
tags: seo, robots, indexing
---

## Configure Robots Meta Tags

Control how search engines index your pages with robots meta tags.

**CRA with react-helmet (before):**

```tsx
<Helmet>
  <meta name="robots" content="index, follow" />
  <meta name="googlebot" content="index, follow, max-snippet:-1" />
</Helmet>
```

**Next.js Metadata API (after):**

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}
```

**Blocking indexing:**

```tsx
// app/admin/page.tsx
export const metadata: Metadata = {
  robots: {
    index: false,
    follow: false,
  },
}
```

**Common patterns:**

```tsx
// Public page - full indexing
robots: {
  index: true,
  follow: true,
}

// Private/admin pages - no indexing
robots: {
  index: false,
  follow: false,
}

// Archive pages - index but don't follow links
robots: {
  index: true,
  follow: false,
}

// Utility pages (search results) - don't index
robots: {
  index: false,
  follow: true,
}
```

**Site-wide robots.txt:**

```tsx
// app/robots.ts
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/api/', '/private/'],
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```
