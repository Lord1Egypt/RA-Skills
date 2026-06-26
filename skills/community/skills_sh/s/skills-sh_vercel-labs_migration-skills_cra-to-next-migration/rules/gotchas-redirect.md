---
title: Handle Redirects Properly
impact: MEDIUM
impactDescription: Multiple redirect methods
tags: gotchas, redirect, navigation
---

## Handle Redirects Properly

Next.js has multiple ways to redirect. Choose the right one for your use case.

**1. redirect() function (Server Components):**

```tsx
// app/old-page/page.tsx
import { redirect } from 'next/navigation'

export default function OldPage() {
  redirect('/new-page') // Server-side redirect
  // Code after redirect won't run
}

// With condition
export default async function ProtectedPage() {
  const session = await getSession()
  if (!session) {
    redirect('/login')
  }
  return <Dashboard />
}
```

**2. permanentRedirect() (301 redirect):**

```tsx
import { permanentRedirect } from 'next/navigation'

export default function OldPage() {
  permanentRedirect('/new-page') // SEO-friendly permanent redirect
}
```

**3. next.config.js redirects:**

```js
// next.config.js
module.exports = {
  async redirects() {
    return [
      {
        source: '/old-blog/:slug',
        destination: '/blog/:slug',
        permanent: true,
      },
      {
        source: '/about-us',
        destination: '/about',
        permanent: false,
      },
    ]
  },
}
```

**4. Middleware redirects:**

```tsx
// middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request) {
  if (request.nextUrl.pathname === '/old') {
    return NextResponse.redirect(new URL('/new', request.url))
  }
}
```

**5. Client-side redirect (useRouter):**

```tsx
'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function LoginSuccess() {
  const router = useRouter()

  useEffect(() => {
    router.push('/dashboard')
    // or router.replace('/dashboard') to not add to history
  }, [])

  return <p>Redirecting...</p>
}
```

**Which to use:**
| Scenario | Method |
|----------|--------|
| Always redirect (SEO) | `next.config.js` |
| Auth check | `redirect()` in Server Component |
| After form submit | `redirect()` or `router.push()` |
| Conditional in middleware | `NextResponse.redirect()` |
| After client action | `router.push()` |
