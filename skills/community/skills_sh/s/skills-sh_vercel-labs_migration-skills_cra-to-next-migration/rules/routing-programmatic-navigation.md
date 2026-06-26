---
title: Replace useNavigate with useRouter
impact: CRITICAL
impactDescription: Required for programmatic navigation
tags: routing, navigation, useRouter, useNavigate
---

## Replace useNavigate with useRouter

React Router's `useNavigate` hook is replaced by Next.js's `useRouter` from `next/navigation`.

**CRA with React Router (before):**

```tsx
import { useNavigate } from 'react-router-dom'

export default function LoginForm() {
  const navigate = useNavigate()

  const handleLogin = async () => {
    await login()
    navigate('/dashboard')
  }

  const handleBack = () => {
    navigate(-1) // Go back
  }

  const handleReplace = () => {
    navigate('/new-page', { replace: true })
  }

  return (
    <form onSubmit={handleLogin}>
      <button type="submit">Login</button>
      <button type="button" onClick={handleBack}>Back</button>
    </form>
  )
}
```

**Next.js App Router (after):**

```tsx
'use client'

import { useRouter } from 'next/navigation'

export default function LoginForm() {
  const router = useRouter()

  const handleLogin = async () => {
    await login()
    router.push('/dashboard')
  }

  const handleBack = () => {
    router.back() // Go back
  }

  const handleReplace = () => {
    router.replace('/new-page')
  }

  return (
    <form onSubmit={handleLogin}>
      <button type="submit">Login</button>
      <button type="button" onClick={handleBack}>Back</button>
    </form>
  )
}
```

**Method mapping:**
| React Router | Next.js |
|--------------|---------|
| `navigate('/path')` | `router.push('/path')` |
| `navigate('/path', { replace: true })` | `router.replace('/path')` |
| `navigate(-1)` | `router.back()` |
| `navigate(1)` | `router.forward()` |

**Important:** `useRouter` requires `'use client'` directive since it uses browser APIs.

## Replace useLocation with usePathname

React Router's `useLocation` is replaced by `usePathname` from `next/navigation`:

**React Router (before):**

```tsx
import { useLocation } from 'react-router-dom'

function Component() {
  const location = useLocation()
  console.log(location.pathname)  // '/dashboard'
  console.log(location.search)    // '?tab=settings'
  console.log(location.hash)      // '#section'
}
```

**Next.js (after):**

```tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'

function Component() {
  const pathname = usePathname()           // '/dashboard' (direct string)
  const searchParams = useSearchParams()   // URLSearchParams object
  const tab = searchParams.get('tab')      // 'settings'
}
```

**Key difference:** `usePathname()` returns the path string directly, not an object with a `.pathname` property.
