---
title: Fetch Data in Parallel on Server
impact: HIGH
impactDescription: Avoid server-side waterfalls
tags: data-fetching, parallel, performance
---

## Fetch Data in Parallel on Server

When fetching multiple independent pieces of data, fetch them in parallel to avoid waterfalls.

**CRA Pattern - Sequential (before):**

```tsx
useEffect(() => {
  async function fetchData() {
    const user = await fetch('/api/user').then(r => r.json())
    const posts = await fetch('/api/posts').then(r => r.json())
    const comments = await fetch('/api/comments').then(r => r.json())
    // Total time: user + posts + comments
  }
  fetchData()
}, [])
```

**Next.js - Parallel Fetching (after):**

```tsx
// app/dashboard/page.tsx
export default async function Dashboard() {
  // Start all fetches simultaneously
  const [user, posts, comments] = await Promise.all([
    fetch('https://api.example.com/user').then(r => r.json()),
    fetch('https://api.example.com/posts').then(r => r.json()),
    fetch('https://api.example.com/comments').then(r => r.json()),
  ])
  // Total time: max(user, posts, comments)

  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
      <Comments comments={comments} />
    </div>
  )
}
```

**With separate async components (parallel by default):**

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function Dashboard() {
  // These components fetch in parallel automatically
  return (
    <div>
      <Suspense fallback={<Skeleton />}>
        <UserProfile /> {/* Fetches user */}
      </Suspense>
      <Suspense fallback={<Skeleton />}>
        <PostList />   {/* Fetches posts */}
      </Suspense>
      <Suspense fallback={<Skeleton />}>
        <Comments />   {/* Fetches comments */}
      </Suspense>
    </div>
  )
}

async function UserProfile() {
  const user = await fetchUser()
  return <Profile user={user} />
}
```

**Key insight:** Sibling async Server Components automatically fetch in parallel when wrapped in separate Suspense boundaries.
