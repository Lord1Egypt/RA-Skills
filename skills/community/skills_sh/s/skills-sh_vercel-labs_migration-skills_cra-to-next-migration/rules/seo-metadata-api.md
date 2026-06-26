---
title: Use Metadata API Instead of react-helmet
impact: HIGH
impactDescription: Native SEO support
tags: seo, metadata, react-helmet
---

## Use Metadata API Instead of react-helmet

Replace `react-helmet` or `react-helmet-async` with Next.js's built-in Metadata API.

**CRA with react-helmet (before):**

```tsx
// src/pages/Home.tsx
import { Helmet } from 'react-helmet'

export default function Home() {
  return (
    <>
      <Helmet>
        <title>Home | My App</title>
        <meta name="description" content="Welcome to my app" />
        <meta property="og:title" content="Home | My App" />
        <meta property="og:description" content="Welcome to my app" />
        <link rel="canonical" href="https://example.com" />
      </Helmet>
      <main>
        <h1>Welcome</h1>
      </main>
    </>
  )
}
```

**Next.js Metadata API (after):**

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home | My App',
  description: 'Welcome to my app',
  openGraph: {
    title: 'Home | My App',
    description: 'Welcome to my app',
  },
  alternates: {
    canonical: 'https://example.com',
  },
}

export default function Home() {
  return (
    <main>
      <h1>Welcome</h1>
    </main>
  )
}
```

**Benefits of Metadata API:**
- Server-rendered (better SEO)
- Type-safe with TypeScript
- Automatic deduplication
- No client-side JavaScript
- Streaming compatible

**Layout-level metadata:**

```tsx
// app/layout.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'My App',
    template: '%s | My App',  // Pages can override
  },
  description: 'My awesome application',
}
```
