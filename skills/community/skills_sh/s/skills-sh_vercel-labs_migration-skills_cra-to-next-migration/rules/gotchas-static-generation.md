---
title: Static vs Dynamic Rendering
impact: HIGH
impactDescription: Understanding render modes
tags: gotchas, static, dynamic, rendering
---

## Static vs Dynamic Rendering

Understanding when Next.js renders statically vs dynamically is crucial for performance.

**Static Rendering (at build time):**
- HTML generated once at build
- Cached and served from CDN
- Fastest response times
- Default for routes without dynamic data

**Dynamic Rendering (at request time):**
- HTML generated for each request
- Can access request data (cookies, headers)
- Required for personalized content

**What makes a route dynamic:**

```tsx
// STATIC by default
export default function Page() {
  return <h1>Hello</h1>
}

// DYNAMIC: Uses cookies/headers
import { cookies } from 'next/headers'
export default function Page() {
  const token = cookies().get('token')
  return <h1>Hello {token?.value}</h1>
}

// DYNAMIC: Uses searchParams
export default function Page({ searchParams }) {
  return <h1>Query: {searchParams.q}</h1>
}

// DYNAMIC: Uncached fetch
export default async function Page() {
  const data = await fetch(url, { cache: 'no-store' })
  return <h1>{data.title}</h1>
}
```

**Force static or dynamic:**

```tsx
// Force static (error if dynamic features used)
export const dynamic = 'force-static'

// Force dynamic (SSR every request)
export const dynamic = 'force-dynamic'

// Error if accidentally dynamic
export const dynamic = 'error'
```

**Check in build output:**

```
Route (app)                    Size     First Load JS
┌ ○ /                         5.2 kB        89.1 kB  (Static)
├ ○ /about                    1.3 kB        85.2 kB  (Static)
├ λ /dashboard                2.1 kB        86.0 kB  (Dynamic)
└ λ /api/users                0 B                0 B  (Dynamic)

○  (Static)   prerendered as static content
λ  (Dynamic)  server-rendered on demand
```

**Common gotcha:**
```tsx
// Accidentally dynamic due to Date
export default function Page() {
  return <p>Built at: {new Date().toISOString()}</p> // Makes route dynamic!
}

// Fix: Use build-time date
export default function Page() {
  return <p>Built at: {process.env.BUILD_TIME}</p>
}
```
