---
title: Use Suspense for Streaming Data
impact: MEDIUM
impactDescription: Progressive page loading
tags: data-fetching, streaming, suspense
---

## Use Suspense for Streaming Data

Next.js supports streaming HTML with Suspense, allowing parts of the page to load progressively.

**CRA Pattern (before):**

```tsx
// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const [stats, setStats] = useState(null)
  const [activity, setActivity] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/api/user').then(r => r.json()),
      fetch('/api/stats').then(r => r.json()),
      fetch('/api/activity').then(r => r.json()),
    ]).then(([u, s, a]) => {
      setUser(u)
      setStats(s)
      setActivity(a)
      setLoading(false)
    })
  }, [])

  if (loading) return <FullPageLoader />
  // All data or nothing
}
```

**Next.js with Streaming (after):**

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* User info loads first */}
      <Suspense fallback={<UserSkeleton />}>
        <UserInfo />
      </Suspense>

      {/* Stats stream in independently */}
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>

      {/* Activity streams in independently */}
      <Suspense fallback={<ActivitySkeleton />}>
        <ActivityFeed />
      </Suspense>
    </div>
  )
}

// Each component fetches its own data
async function UserInfo() {
  const user = await fetchUser() // Slow? Only this section waits
  return <UserCard user={user} />
}

async function Stats() {
  const stats = await fetchStats()
  return <StatsDisplay stats={stats} />
}

async function ActivityFeed() {
  const activity = await fetchActivity()
  return <Activity items={activity} />
}
```

**Benefits:**
- Page shell appears immediately
- Each section loads independently
- No waterfall - all fetches start in parallel
- Better perceived performance
- Progressive enhancement
