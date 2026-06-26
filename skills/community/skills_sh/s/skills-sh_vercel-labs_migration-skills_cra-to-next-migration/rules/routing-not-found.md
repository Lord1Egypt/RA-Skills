---
title: Add not-found.tsx for 404 Pages
impact: MEDIUM
impactDescription: Custom 404 page handling
tags: routing, not-found, 404
---

## Add not-found.tsx for 404 Pages

CRA handles 404s with a catch-all route. Next.js uses `not-found.tsx` files for custom 404 pages.

**CRA with React Router (before):**

```tsx
// src/App.tsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="*" element={<NotFound />} />
</Routes>

// src/pages/NotFound.tsx
export default function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <Link to="/">Go Home</Link>
    </div>
  )
}
```

**Next.js App Router (after):**

```tsx
// app/not-found.tsx - Global 404 page
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h1>404 - Page Not Found</h1>
      <p>Could not find the requested resource</p>
      <Link href="/">Go Home</Link>
    </div>
  )
}
```

**Triggering 404 programmatically:**

```tsx
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation'

export default async function UserPage({ params }) {
  const user = await fetchUser(params.id)

  if (!user) {
    notFound() // Renders the nearest not-found.tsx
  }

  return <UserProfile user={user} />
}
```

**Nested not-found pages:**

```
app/
├── not-found.tsx           # Global 404
├── dashboard/
│   ├── not-found.tsx       # Dashboard-specific 404
│   └── [id]/
│       └── page.tsx        # Can call notFound()
```

Each route segment can have its own `not-found.tsx` with context-appropriate messaging.

**With API response check:**

```tsx
// app/posts/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function Post({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`)

  if (res.status === 404) {
    notFound()
  }

  if (!res.ok) {
    throw new Error('Failed to fetch post') // Goes to error.tsx
  }

  const post = await res.json()
  return <Article post={post} />
}
```

**Key difference:** `notFound()` triggers the 404 UI while errors trigger `error.tsx`. Use the appropriate one for the situation.
