---
title: Convert useEffect Fetches to Server Components
impact: CRITICAL
impactDescription: Core data fetching paradigm shift
tags: data-fetching, server-components, useEffect, rsc
---

## Convert useEffect Fetches to Server Components

CRA fetches data in useEffect on the client. Next.js Server Components can fetch data directly during render on the server.

**CRA Pattern (before):**

```tsx
// src/pages/Users.tsx
import { useState, useEffect } from 'react'

export default function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => setError(err))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  if (error) return <Error message={error.message} />

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**Next.js Server Component (after):**

```tsx
// app/users/page.tsx
// No 'use client' - this is a Server Component by default

export default async function Users() {
  const res = await fetch('https://api.example.com/users')
  const users = await res.json()

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

**Benefits:**
- No loading/error state management (use `loading.tsx` and `error.tsx`)
- No client-side JavaScript for data fetching
- Data fetched at request time on server
- Better SEO - content in initial HTML
- No useEffect waterfall - data fetched before render

**With error handling:**

```tsx
// app/users/page.tsx
export default async function Users() {
  const res = await fetch('https://api.example.com/users')

  if (!res.ok) {
    throw new Error('Failed to fetch users')
  }

  const users = await res.json()
  return <UserList users={users} />
}
```
