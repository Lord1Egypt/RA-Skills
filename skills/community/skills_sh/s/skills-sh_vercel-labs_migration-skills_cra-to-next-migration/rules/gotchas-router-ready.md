---
title: Check router.isReady for Query Params
impact: MEDIUM
impactDescription: Pages Router specific gotcha
tags: gotchas, router, query-params, pages-router
---

## Check router.isReady for Query Params

In Pages Router, query params aren't available during SSR. Check `isReady` before using them.

**Problem in Pages Router:**

```tsx
// pages/search.tsx
import { useRouter } from 'next/router'

function SearchPage() {
  const router = useRouter()
  const { q } = router.query

  // BUG: q is undefined during SSR and first render
  useEffect(() => {
    if (q) {
      search(q as string) // May run with undefined!
    }
  }, [q])

  return <div>Searching for: {q}</div>
}
```

**Solution for Pages Router:**

```tsx
// pages/search.tsx
import { useRouter } from 'next/router'

function SearchPage() {
  const router = useRouter()

  useEffect(() => {
    // Wait for router to be ready
    if (!router.isReady) return

    const { q } = router.query
    if (q) {
      search(q as string)
    }
  }, [router.isReady, router.query])

  if (!router.isReady) {
    return <Loading />
  }

  return <div>Searching for: {router.query.q}</div>
}
```

**App Router (simpler):**

```tsx
// app/search/page.tsx
// searchParams are available immediately in App Router
export default function SearchPage({
  searchParams,
}: {
  searchParams: { q?: string }
}) {
  return <div>Searching for: {searchParams.q}</div>
}

// For client components, use useSearchParams
'use client'
import { useSearchParams } from 'next/navigation'

function SearchInput() {
  const searchParams = useSearchParams()
  const q = searchParams.get('q') // Available immediately
  return <input defaultValue={q || ''} />
}
```

**Key point:** This is mainly a Pages Router issue. App Router handles this better with the `searchParams` prop.
