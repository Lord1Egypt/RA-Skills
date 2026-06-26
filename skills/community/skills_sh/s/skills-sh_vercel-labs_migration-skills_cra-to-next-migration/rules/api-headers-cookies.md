---
title: Access Headers and Cookies
impact: MEDIUM
impactDescription: Read request headers and cookies
tags: api, headers, cookies
---

## Access Headers and Cookies

Access request headers and cookies in Next.js Route Handlers.

**Express/CRA Backend (before):**

```js
router.get('/profile', async (req, res) => {
  const authHeader = req.headers.authorization
  const sessionId = req.cookies.session
  // ...
})
```

**Next.js Route Handler (after):**

```tsx
// app/api/profile/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { cookies, headers } from 'next/headers'

// Method 1: From request object
export async function GET(request: NextRequest) {
  // Headers
  const authHeader = request.headers.get('authorization')
  const contentType = request.headers.get('content-type')

  // Cookies from request
  const sessionId = request.cookies.get('session')?.value

  return NextResponse.json({ /* ... */ })
}

// Method 2: Using next/headers helpers
export async function GET() {
  const headersList = headers()
  const cookieStore = cookies()

  const authHeader = headersList.get('authorization')
  const sessionId = cookieStore.get('session')?.value

  return NextResponse.json({ /* ... */ })
}
```

**Setting cookies in response:**

```tsx
export async function POST(request: NextRequest) {
  const response = NextResponse.json({ success: true })

  // Set cookie
  response.cookies.set('session', 'abc123', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 1 week
  })

  // Delete cookie
  response.cookies.delete('oldCookie')

  return response
}
```

**Setting headers in response:**

```tsx
export async function GET() {
  return new NextResponse(JSON.stringify({ data: 'value' }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
      'X-Custom-Header': 'value',
    },
  })
}
```

See also: `gotchas-cookies.md` for cookies in Server Components, `gotchas-headers.md` for setting response headers.
