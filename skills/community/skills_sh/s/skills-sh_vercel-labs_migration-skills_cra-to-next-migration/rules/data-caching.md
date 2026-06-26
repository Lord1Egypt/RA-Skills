---
title: Configure Fetch Caching Behavior
impact: HIGH
impactDescription: Control data freshness vs performance
tags: data-fetching, caching, fetch
---

## Configure Fetch Caching Behavior

Next.js extends the native fetch API with caching options. Understand the defaults and how to override them.

**CRA Pattern (before):**

```tsx
// No automatic caching - relies on browser cache or manual implementation
fetch('/api/data')
```

**Next.js Caching Options (after):**

```tsx
// Force cache (static data) - cached until manually revalidated
const staticData = await fetch('https://api.example.com/static', {
  cache: 'force-cache' // Default in App Router
})

// No cache (dynamic data) - fresh on every request
const dynamicData = await fetch('https://api.example.com/dynamic', {
  cache: 'no-store'
})

// Time-based revalidation - cached, refreshed periodically
const timedData = await fetch('https://api.example.com/posts', {
  next: { revalidate: 3600 } // Refresh every hour
})

// Tag-based - for on-demand revalidation
const taggedData = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
})
```

**Page-level cache configuration:**

```tsx
// app/posts/page.tsx

// Make entire page dynamic
export const dynamic = 'force-dynamic'

// Or configure revalidation for all fetches in page
export const revalidate = 60

// Or make it fully static
export const dynamic = 'force-static'
```

**Opting out of caching for specific routes:**

```tsx
// app/api/realtime/route.ts
export const dynamic = 'force-dynamic'
export const revalidate = 0

export async function GET() {
  const data = await getRealTimeData()
  return Response.json(data)
}
```

**Note:** In development, caching is disabled by default for easier debugging. Test caching behavior with `next build && next start`.
