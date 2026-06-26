---
title: Configure Twitter Card Metadata
impact: MEDIUM
impactDescription: Twitter/X previews
tags: seo, twitter, social
---

## Configure Twitter Card Metadata

Configure Twitter Card metadata for rich previews on Twitter/X.

**CRA with react-helmet (before):**

```tsx
<Helmet>
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@myhandle" />
  <meta name="twitter:creator" content="@author" />
  <meta name="twitter:title" content="Page Title" />
  <meta name="twitter:description" content="Page description" />
  <meta name="twitter:image" content="https://example.com/image.jpg" />
</Helmet>
```

**Next.js Metadata API (after):**

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  twitter: {
    card: 'summary_large_image',
    site: '@myhandle',
    creator: '@author',
    title: 'Page Title',
    description: 'Page description',
    images: ['https://example.com/image.jpg'],
  },
}
```

**Card types:**

```tsx
// Summary card (small image)
twitter: {
  card: 'summary',
}

// Large image card
twitter: {
  card: 'summary_large_image',
}

// App card
twitter: {
  card: 'app',
  app: {
    name: 'My App',
    id: { iphone: '123', ipad: '123', googleplay: 'com.app' },
    url: { iphone: 'myapp://...', ipad: 'myapp://...' },
  },
}

// Player card (for video/audio)
twitter: {
  card: 'player',
  players: [{ playerUrl: '...', streamUrl: '...' }],
}
```

**Default Twitter config in layout:**

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  twitter: {
    card: 'summary_large_image',
    site: '@myhandle',
  },
}
```

Pages inherit and can override specific properties.
