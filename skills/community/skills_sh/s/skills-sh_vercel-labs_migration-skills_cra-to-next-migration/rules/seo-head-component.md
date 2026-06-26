---
title: Migrate from next/head to Metadata API
impact: HIGH
impactDescription: Pages Router to App Router migration
tags: seo, next-head, metadata, migration
---

## Migrate from next/head to Metadata API

When migrating from Pages Router to App Router, replace `next/head` with the Metadata API.

**Next.js Pages Router (before):**

```tsx
// pages/about.tsx
import Head from 'next/head'

export default function About() {
  return (
    <>
      <Head>
        <title>About Us | My App</title>
        <meta name="description" content="Learn about our company" />
        <meta property="og:title" content="About Us" />
        <meta property="og:description" content="Learn about our company" />
        <link rel="canonical" href="https://example.com/about" />
      </Head>
      <main>
        <h1>About Us</h1>
      </main>
    </>
  )
}
```

**Next.js App Router (after):**

```tsx
// app/about/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us | My App',
  description: 'Learn about our company',
  openGraph: {
    title: 'About Us',
    description: 'Learn about our company',
  },
  alternates: {
    canonical: 'https://example.com/about',
  },
}

export default function About() {
  return (
    <main>
      <h1>About Us</h1>
    </main>
  )
}
```

**Migration mapping:**

| next/head | Metadata API |
|-----------|--------------|
| `<title>` | `title` |
| `<meta name="description">` | `description` |
| `<meta property="og:*">` | `openGraph: { ... }` |
| `<meta name="twitter:*">` | `twitter: { ... }` |
| `<link rel="canonical">` | `alternates: { canonical }` |
| `<meta name="robots">` | `robots: { ... }` |
| `<link rel="icon">` | `icons: { ... }` |

**Benefits of Metadata API:**
- Type-safe
- Automatic deduplication
- Streaming compatible
- Better for SSR
- Easier to maintain
