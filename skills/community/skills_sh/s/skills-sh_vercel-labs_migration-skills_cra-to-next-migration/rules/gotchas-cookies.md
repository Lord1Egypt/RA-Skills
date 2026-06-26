---
title: Handle Cookies in RSC
impact: MEDIUM
impactDescription: Reading vs setting cookies
tags: gotchas, cookies, server-components
---

## Handle Cookies in RSC

Cookies work differently in Server Components, Route Handlers, and Client Components.

**1. Reading cookies in Server Components:**

```tsx
// app/page.tsx (Server Component)
import { cookies } from 'next/headers'

export default function Page() {
  const cookieStore = cookies()
  const theme = cookieStore.get('theme')?.value || 'light'

  return <div className={theme}>Content</div>
}
```

**2. Setting cookies in Route Handlers:**

```tsx
// app/api/theme/route.ts
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const { theme } = await request.json()

  cookies().set('theme', theme, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 365, // 1 year
  })

  return NextResponse.json({ success: true })
}
```

**3. Setting cookies in Server Actions:**

```tsx
// app/actions.ts
'use server'

import { cookies } from 'next/headers'

export async function setTheme(theme: string) {
  cookies().set('theme', theme)
}

// app/page.tsx
import { setTheme } from './actions'

export default function Page() {
  return (
    <form action={setTheme.bind(null, 'dark')}>
      <button>Set Dark Theme</button>
    </form>
  )
}
```

**4. Accessing cookies in Client Components:**

```tsx
'use client'

import { useEffect, useState } from 'react'

function ClientComponent() {
  const [theme, setTheme] = useState('light')

  useEffect(() => {
    // Read cookie on client
    const value = document.cookie
      .split('; ')
      .find(row => row.startsWith('theme='))
      ?.split('=')[1]
    if (value) setTheme(value)
  }, [])

  const updateTheme = (newTheme: string) => {
    document.cookie = `theme=${newTheme}; path=/`
    setTheme(newTheme)
  }

  return <button onClick={() => updateTheme('dark')}>Toggle</button>
}
```

**Important:** Server Components can only READ cookies. To SET cookies, use Route Handlers, Server Actions, or Middleware.

See also: `api-headers-cookies.md` for accessing cookies in Route Handlers.
