---
title: Replace useParams with Next.js params
impact: HIGH
impactDescription: Different param access pattern
tags: routing, params, useParams
---

## Replace useParams with Next.js params

React Router's `useParams` hook is replaced by the `params` prop passed to page components in Next.js.

**CRA with React Router (before):**

```tsx
import { useParams } from 'react-router-dom'

export default function UserProfile() {
  const { userId } = useParams()
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])

  return <div>User: {user?.name}</div>
}
```

**Next.js App Router - Server Component (after):**

```tsx
// app/users/[userId]/page.tsx
// Server Component - no hooks needed!
export default async function UserProfile({
  params,
}: {
  params: { userId: string }
}) {
  const user = await fetchUser(params.userId)
  return <div>User: {user.name}</div>
}
```

**Next.js App Router - Client Component (after):**

```tsx
// If you need client-side param access
'use client'

import { useParams } from 'next/navigation'

export default function UserProfile() {
  const params = useParams()
  const userId = params.userId as string
  // ... use in client component
}
```

**Key differences:**
- Server Components receive `params` as a prop (preferred)
- Client Components can use `useParams()` from `next/navigation`
- Params are always strings (or string arrays for catch-all)
- No need for `useEffect` to fetch data - use Server Components instead
