---
title: Middleware Runs on Edge
impact: MEDIUM
impactDescription: Middleware limitations
tags: gotchas, middleware, edge
---

## Middleware Runs on Edge

Next.js Middleware always runs on the Edge runtime, which has limitations.

**Middleware location:**

```
project/
├── middleware.ts    # Must be at project root
├── app/
├── pages/
└── ...
```

**Basic middleware:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Runs on EVERY request matching the config

  // Add headers
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')

  return response
}

export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

**What works in middleware:**

```tsx
export function middleware(request: NextRequest) {
  // URL manipulation
  const url = request.nextUrl.clone()

  // Redirects
  if (url.pathname === '/old') {
    url.pathname = '/new'
    return NextResponse.redirect(url)
  }

  // Rewrites
  if (url.pathname === '/blog') {
    url.pathname = '/news'
    return NextResponse.rewrite(url)
  }

  // Read/set cookies
  const token = request.cookies.get('token')
  const response = NextResponse.next()
  response.cookies.set('visited', 'true')

  // Read headers
  const authHeader = request.headers.get('authorization')

  return response
}
```

**What doesn't work in middleware:**

```tsx
export function middleware(request: NextRequest) {
  // NO: Node.js APIs
  const fs = require('fs')

  // NO: Database connections (usually)
  const db = new Database()

  // NO: Heavy computation
  // Middleware should be fast

  // NO: Response body modification
  // Can only redirect/rewrite/set headers
}
```

**Authentication pattern:**

```tsx
export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}
```
