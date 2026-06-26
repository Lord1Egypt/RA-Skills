---
title: Set Canonical URLs
impact: MEDIUM
impactDescription: Prevent duplicate content
tags: seo, canonical, urls
---

## Set Canonical URLs

Set canonical URLs to prevent duplicate content issues with search engines.

**CRA with react-helmet (before):**

```tsx
<Helmet>
  <link rel="canonical" href="https://example.com/page" />
</Helmet>
```

**Next.js Metadata API (after):**

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/page',
  },
}
```

**Dynamic canonical URLs:**

```tsx
// app/blog/[slug]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({ params }): Promise<Metadata> {
  return {
    alternates: {
      canonical: `https://example.com/blog/${params.slug}`,
    },
  }
}
```

**With language alternates:**

```tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/page',
    languages: {
      'en-US': 'https://example.com/en/page',
      'de-DE': 'https://example.com/de/page',
      'es-ES': 'https://example.com/es/page',
    },
  },
}
```

**Base URL configuration:**

```tsx
// app/layout.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
}

// Now child pages can use relative URLs
// app/blog/page.tsx
export const metadata: Metadata = {
  alternates: {
    canonical: '/blog',  // Resolves to https://example.com/blog
  },
}
```
