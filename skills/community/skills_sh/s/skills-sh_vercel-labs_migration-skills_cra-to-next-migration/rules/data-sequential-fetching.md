---
title: Handle Sequential Data Dependencies
impact: MEDIUM
impactDescription: When data depends on previous fetches
tags: data-fetching, sequential, dependencies
---

## Handle Sequential Data Dependencies

When one fetch depends on another's result, handle the sequence properly while still optimizing where possible.

**CRA Pattern (before):**

```tsx
useEffect(() => {
  async function fetchData() {
    const user = await fetch('/api/user').then(r => r.json())
    // Posts depend on user.id
    const posts = await fetch(`/api/posts?userId=${user.id}`).then(r => r.json())
    setData({ user, posts })
  }
  fetchData()
}, [])
```

**Next.js Server Component (after):**

```tsx
// app/profile/page.tsx
export default async function Profile() {
  // First fetch - required for subsequent fetches
  const user = await fetchUser()

  // Dependent fetch - needs user.id
  const posts = await fetchPosts(user.id)

  return (
    <div>
      <UserInfo user={user} />
      <PostList posts={posts} />
    </div>
  )
}
```

**Optimized with parallel where possible:**

```tsx
// app/profile/page.tsx
export default async function Profile() {
  const user = await fetchUser()

  // These don't depend on each other, fetch in parallel
  const [posts, followers, settings] = await Promise.all([
    fetchPosts(user.id),
    fetchFollowers(user.id),
    fetchSettings(user.id),
  ])

  return (
    <div>
      <UserInfo user={user} />
      <PostList posts={posts} />
      <Followers followers={followers} />
      <Settings settings={settings} />
    </div>
  )
}
```

**With Suspense for progressive loading:**

```tsx
// app/profile/page.tsx
import { Suspense } from 'react'

export default async function Profile() {
  const user = await fetchUser()

  return (
    <div>
      <UserInfo user={user} />
      {/* Posts can load after user is shown */}
      <Suspense fallback={<PostsSkeleton />}>
        <UserPosts userId={user.id} />
      </Suspense>
    </div>
  )
}

async function UserPosts({ userId }) {
  const posts = await fetchPosts(userId)
  return <PostList posts={posts} />
}
```
