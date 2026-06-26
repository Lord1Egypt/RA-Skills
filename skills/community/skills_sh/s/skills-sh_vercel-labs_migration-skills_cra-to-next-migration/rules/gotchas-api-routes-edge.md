---
title: Edge vs Node.js Runtime
impact: MEDIUM
impactDescription: Different API capabilities
tags: gotchas, edge, runtime, api
---

## Edge vs Node.js Runtime

Next.js API routes can run on Edge or Node.js runtime. Know the differences.

**Node.js Runtime (default):**
- Full Node.js APIs available
- Longer cold starts
- Can use file system, native modules
- Better for complex operations

**Edge Runtime:**
- Faster cold starts
- Limited APIs (Web APIs only)
- No file system access
- Global deployment

**Setting runtime:**

```tsx
// app/api/node-route/route.ts
// Default: Node.js runtime
export async function GET() {
  // Can use Node.js APIs
  const fs = require('fs')
  return Response.json({ data: 'from node' })
}

// app/api/edge-route/route.ts
export const runtime = 'edge' // Use Edge runtime

export async function GET() {
  // Only Web APIs available
  // No 'fs', no native modules
  return Response.json({ data: 'from edge' })
}
```

**What works on Edge:**

```tsx
export const runtime = 'edge'

export async function GET(request: Request) {
  // Web APIs work
  const url = new URL(request.url)
  const headers = new Headers()
  const response = await fetch('https://api.example.com/data')

  // Cookies work
  const cookieHeader = request.headers.get('cookie')

  return Response.json({ data: 'ok' })
}
```

**What doesn't work on Edge:**

```tsx
export const runtime = 'edge'

export async function GET() {
  // These will fail:
  const fs = require('fs')           // No file system
  const path = require('path')       // No path module
  const crypto = require('crypto')   // Use Web Crypto instead

  // Some npm packages won't work
  // Database clients may need edge-compatible versions
}
```

**Edge-compatible database clients:**
- `@vercel/postgres`
- `@planetscale/database`
- `@neondatabase/serverless`
- Prisma with edge adapter
