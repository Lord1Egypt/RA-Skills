---
title: Convert useEffect to getServerSideProps (Pages Router)
impact: HIGH
impactDescription: Server-side rendering for Pages Router
tags: data-fetching, ssr, getServerSideProps, pages-router
---

## Convert useEffect to getServerSideProps (Pages Router)

For Pages Router migrations, use `getServerSideProps` for server-side data fetching on every request.

**CRA Pattern (before):**

```tsx
// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/stats')
      .then(res => res.json())
      .then(setStats)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Loading />
  return <StatsDisplay stats={stats} />
}
```

**Next.js Pages Router (after):**

```tsx
// pages/dashboard.tsx
import { GetServerSideProps } from 'next'

interface Props {
  stats: Stats
}

export default function Dashboard({ stats }: Props) {
  // No loading state - data is already available
  return <StatsDisplay stats={stats} />
}

export const getServerSideProps: GetServerSideProps<Props> = async (context) => {
  const res = await fetch('https://api.example.com/stats')
  const stats = await res.json()

  return {
    props: {
      stats,
    },
  }
}
```

**When to use:**
- Data must be fresh on every request
- Data depends on request (cookies, headers, query params)
- Page requires authentication check

**With request context:**

```tsx
export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const token = req.cookies.token
  const page = query.page || '1'

  const res = await fetch(`https://api.example.com/data?page=${page}`, {
    headers: { Authorization: `Bearer ${token}` }
  })

  return { props: { data: await res.json() } }
}
```

Note: For App Router, prefer Server Components over `getServerSideProps`.
