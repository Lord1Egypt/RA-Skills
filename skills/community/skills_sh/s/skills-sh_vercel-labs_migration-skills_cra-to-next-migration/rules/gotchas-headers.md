---
title: Set Response Headers
impact: LOW
impactDescription: Headers in different contexts
tags: gotchas, headers, response
---

## Set Response Headers

Setting response headers works differently in various Next.js contexts.

**1. In Route Handlers:**

```tsx
// app/api/data/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json(
    { data: 'value' },
    {
      headers: {
        'Cache-Control': 'public, max-age=3600',
        'X-Custom-Header': 'value',
      },
    }
  )
}
```

**2. In next.config.js (global):**

```js
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'X-API-Version', value: '1.0' },
        ],
      },
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
        ],
      },
    ]
  },
}
```

**3. In Middleware:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request) {
  const response = NextResponse.next()

  // Add headers to response
  response.headers.set('X-Custom-Header', 'value')

  return response
}
```

**4. Security headers example:**

```js
// next.config.js
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
]

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}
```

**Note:** You cannot set headers from Server Components directly. Use Route Handlers or Middleware for dynamic headers.

**5. COOP/COEP headers for SharedArrayBuffer:**

Apps using SharedArrayBuffer, certain WebAssembly features, or high-resolution timers need Cross-Origin isolation headers:

```js
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin',
          },
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'require-corp',
          },
        ],
      },
    ]
  },
}
```

**When you need COOP/COEP:**

- Using `SharedArrayBuffer` for multi-threaded operations
- Using high-resolution `performance.now()` timers
- Certain WebAssembly applications
- Web Workers sharing memory with main thread

**Warning:** These headers restrict loading cross-origin resources. Resources must either:
- Be same-origin
- Include `Cross-Origin-Resource-Policy: cross-origin` header
- Be loaded with `crossorigin` attribute

**Conditional headers for specific routes:**

```js
// Only apply to routes that need SharedArrayBuffer
{
  source: '/editor/:path*',
  headers: [
    { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
    { key: 'Cross-Origin-Embedder-Policy', value: 'require-corp' },
  ],
}
```
