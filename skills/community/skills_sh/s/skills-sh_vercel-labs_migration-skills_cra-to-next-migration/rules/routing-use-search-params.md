---
title: Replace useSearchParams Properly
impact: HIGH
impactDescription: Query string handling differs
tags: routing, search-params, query-string
---

## Replace useSearchParams Properly

React Router's `useSearchParams` differs from Next.js's implementation.

**CRA with React Router (before):**

```tsx
import { useSearchParams } from 'react-router-dom'

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q')
  const page = searchParams.get('page') || '1'

  const updateQuery = (newQuery: string) => {
    setSearchParams({ q: newQuery, page: '1' })
  }

  return (
    <div>
      <input
        value={query || ''}
        onChange={(e) => updateQuery(e.target.value)}
      />
      <p>Searching for: {query}</p>
    </div>
  )
}
```

**Next.js App Router - Server Component (after):**

```tsx
// app/search/page.tsx
export default function SearchPage({
  searchParams,
}: {
  searchParams: { q?: string; page?: string }
}) {
  const query = searchParams.q
  const page = searchParams.page || '1'

  return (
    <div>
      <SearchInput defaultValue={query} />
      <p>Searching for: {query}</p>
    </div>
  )
}
```

**Next.js App Router - Client Component (after):**

```tsx
'use client'

import { useSearchParams, useRouter, usePathname } from 'next/navigation'

export default function SearchInput() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  const query = searchParams.get('q')

  const updateQuery = (newQuery: string) => {
    const params = new URLSearchParams(searchParams)
    params.set('q', newQuery)
    params.set('page', '1')
    router.push(`${pathname}?${params.toString()}`)
  }

  return (
    <input
      defaultValue={query || ''}
      onChange={(e) => updateQuery(e.target.value)}
    />
  )
}
```

**Key differences:**
- Server Components receive `searchParams` as a prop (read-only)
- Client Components use `useSearchParams()` from `next/navigation`
- No `setSearchParams` - use `router.push()` to update URL
