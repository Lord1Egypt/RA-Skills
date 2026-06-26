---
title: Replace React Router Link with next/link
impact: CRITICAL
impactDescription: Required for client-side navigation
tags: routing, link, navigation
---

## Replace React Router Link with next/link

React Router's `Link` must be replaced with Next.js's `Link` component from `next/link`.

**CRA with React Router (before):**

```tsx
import { Link } from 'react-router-dom'

export default function Navigation() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to={`/users/${userId}`}>Profile</Link>
      <Link to="/dashboard" replace>Dashboard</Link>
      <Link to={{ pathname: '/search', search: '?q=test' }}>
        Search
      </Link>
    </nav>
  )
}
```

**Next.js (after):**

```tsx
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href={`/users/${userId}`}>Profile</Link>
      <Link href="/dashboard" replace>Dashboard</Link>
      <Link href={{ pathname: '/search', query: { q: 'test' } }}>
        Search
      </Link>
    </nav>
  )
}
```

**Key differences:**
| React Router | Next.js |
|--------------|---------|
| `to="/path"` | `href="/path"` |
| `to={{ pathname, search }}` | `href={{ pathname, query }}` |
| `<Link><a>Text</a></Link>` | `<Link>Text</Link>` (no nested `<a>`) |

**Prefetching:**
Next.js `Link` automatically prefetches linked pages in the viewport. Control with:
```tsx
<Link href="/heavy-page" prefetch={false}>No Prefetch</Link>
```

## NavLink Replacement Pattern

React Router's `NavLink` with `isActive` callback requires manual implementation using `usePathname`:

**React Router NavLink (before):**

```tsx
import { NavLink } from 'react-router-dom'

<NavLink
  to="/dashboard"
  className={({ isActive }) => isActive ? 'nav-active' : 'nav-link'}
>
  Dashboard
</NavLink>
```

**Next.js with usePathname (after):**

```tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function NavLink({ href, children }) {
  const pathname = usePathname()
  const isActive = pathname === href

  return (
    <Link href={href} className={isActive ? 'nav-active' : 'nav-link'}>
      {children}
    </Link>
  )
}
```

For nested route matching (e.g., `/dashboard/settings` should highlight `/dashboard`):

```tsx
const isActive = pathname === href || pathname.startsWith(`${href}/`)
```
