---
title: Implement Middleware Patterns
impact: MEDIUM
impactDescription: Request processing pipeline
tags: api, middleware, authentication
---

## Implement Middleware Patterns

Implement middleware patterns for authentication, logging, and other cross-cutting concerns.

**Express/CRA Backend (before):**

```js
// Middleware function
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) return res.status(401).json({ error: 'Unauthorized' })

  try {
    req.user = verifyToken(token)
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}

router.get('/protected', authMiddleware, (req, res) => {
  res.json({ user: req.user })
})
```

**Next.js - Route Handler with auth check:**

```tsx
// lib/auth.ts
export async function verifyAuth(request: Request) {
  const token = request.headers.get('authorization')?.split(' ')[1]
  if (!token) return null

  try {
    return await verifyToken(token)
  } catch {
    return null
  }
}

// app/api/protected/route.ts
import { verifyAuth } from '@/lib/auth'

export async function GET(request: Request) {
  const user = await verifyAuth(request)

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  return NextResponse.json({ user })
}
```

**Next.js Middleware (for multiple routes):**

```tsx
// middleware.ts (at project root)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')

  // Protect /api/admin routes
  if (request.nextUrl.pathname.startsWith('/api/admin')) {
    if (!token) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/api/:path*',
}
```
