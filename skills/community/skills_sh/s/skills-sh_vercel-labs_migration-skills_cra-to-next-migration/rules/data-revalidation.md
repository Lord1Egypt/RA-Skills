---
title: Configure Data Revalidation Strategies
impact: HIGH
impactDescription: Control cache freshness
tags: data-fetching, caching, revalidation, isr
---

## Configure Data Revalidation Strategies

Next.js provides multiple revalidation strategies to control when cached data is refreshed.

**CRA Pattern (before):**

```tsx
// No built-in caching - every fetch is fresh
useEffect(() => {
  fetch('/api/posts').then(res => res.json()).then(setPosts)
}, [])
```

**Next.js App Router - Time-based Revalidation:**

```tsx
// app/posts/page.tsx
export default async function Posts() {
  // Revalidate every 60 seconds
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }
  })
  const posts = await res.json()
  return <PostList posts={posts} />
}
```

**Next.js App Router - On-demand Revalidation:**

```tsx
// app/posts/page.tsx
export default async function Posts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })
  const posts = await res.json()
  return <PostList posts={posts} />
}

// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache'

export async function POST() {
  revalidateTag('posts')
  return Response.json({ revalidated: true })
}
```

**Revalidation options:**

```tsx
// No caching - always fresh
fetch(url, { cache: 'no-store' })

// Cache forever (default for static)
fetch(url, { cache: 'force-cache' })

// Time-based revalidation
fetch(url, { next: { revalidate: 3600 } })

// Tag-based for on-demand revalidation
fetch(url, { next: { tags: ['collection'] } })
```

**Page-level configuration:**

```tsx
// app/posts/page.tsx
export const revalidate = 60 // Revalidate every 60 seconds
export const dynamic = 'force-dynamic' // Always SSR

export default async function Posts() {
  // ...
}
```

**Revalidation timeline (stale-while-revalidate):**

1. Build: Page rendered, cached
2. Request at 0s: Serve cached page
3. Request at 30s: Serve cached page (< 60s)
4. Request at 61s: Serve cached page, trigger background revalidation
5. Request at 62s: Serve NEW cached page (if revalidation succeeded)

**Key insight:** Revalidation is "stale-while-revalidate" - the NEXT request gets fresh data, not the current one.

**Testing revalidation:**

```bash
# Build and start production server
npm run build && npm start

# Revalidation doesn't work in development!
# Always test with production build
```
