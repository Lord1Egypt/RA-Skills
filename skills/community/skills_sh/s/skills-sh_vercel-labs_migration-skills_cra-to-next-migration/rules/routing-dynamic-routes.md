---
title: Use [param] Syntax for Dynamic Segments
impact: CRITICAL
impactDescription: Required for dynamic URLs
tags: routing, dynamic-routes, params
---

## Use [param] Syntax for Dynamic Segments

React Router uses `:param` syntax. Next.js uses `[param]` folder names for dynamic route segments.

**CRA with React Router (before):**

```tsx
// src/App.tsx
<Routes>
  <Route path="/users/:userId" element={<UserProfile />} />
  <Route path="/posts/:postId" element={<Post />} />
</Routes>

// src/pages/UserProfile.tsx
import { useParams } from 'react-router-dom'

export default function UserProfile() {
  const { userId } = useParams()
  return <h1>User: {userId}</h1>
}
```

**Next.js App Router (after):**

Current versions of Next.js use async params by default. The params prop is a Promise that must be awaited.

```tsx
// app/users/[userId]/page.tsx
export default async function UserProfile({
  params,
}: {
  params: Promise<{ userId: string }>
}) {
  const { userId } = await params
  return <h1>User: {userId}</h1>
}

// app/posts/[postId]/page.tsx
export default async function Post({
  params,
}: {
  params: Promise<{ postId: string }>
}) {
  const { postId } = await params
  return <h1>Post: {postId}</h1>
}
```

**Multiple dynamic segments:**

```tsx
// app/blog/[category]/[slug]/page.tsx
export default async function BlogPost({
  params,
}: {
  params: Promise<{ category: string; slug: string }>
}) {
  const { category, slug } = await params
  return <h1>{category}: {slug}</h1>
}
```

**Legacy pattern (Next.js 14 and earlier) - Do NOT use:**

In older versions of Next.js, params were synchronous. This pattern is outdated and should not be used in new migrations:

```tsx
// app/users/[userId]/page.tsx
export default function UserProfile({
  params,
}: {
  params: { userId: string }
}) {
  return <h1>User: {params.userId}</h1>
}
```
