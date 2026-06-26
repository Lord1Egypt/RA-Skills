---
title: Keep Client Fetches with Proper Patterns
impact: MEDIUM
impactDescription: Some fetches must stay client-side
tags: data-fetching, client-side, swr, react-query
---

## Keep Client Fetches with Proper Patterns

Some data fetching must remain client-side (user interactions, real-time updates). Use proper patterns like SWR or React Query.

**CRA Pattern (before):**

```tsx
// src/components/SearchResults.tsx
import { useState, useEffect } from 'react'

export default function SearchResults({ query }) {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!query) return
    setLoading(true)
    fetch(`/api/search?q=${query}`)
      .then(res => res.json())
      .then(setResults)
      .finally(() => setLoading(false))
  }, [query])

  return loading ? <Spinner /> : <Results data={results} />
}
```

**Next.js with SWR (after):**

```tsx
// components/SearchResults.tsx
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function SearchResults({ query }) {
  const { data, error, isLoading } = useSWR(
    query ? `/api/search?q=${query}` : null,
    fetcher
  )

  if (isLoading) return <Spinner />
  if (error) return <Error />
  return <Results data={data} />
}
```

**Next.js with React Query (after):**

```tsx
'use client'

import { useQuery } from '@tanstack/react-query'

export default function SearchResults({ query }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetch(`/api/search?q=${query}`).then(res => res.json()),
    enabled: !!query,
  })

  if (isLoading) return <Spinner />
  if (error) return <Error />
  return <Results data={data} />
}
```

**When to use client-side fetching:**
- User-triggered searches/filters
- Real-time data (polling, WebSockets)
- Infinite scroll/pagination
- Data that changes based on client state
- After user interactions

Remember to add `'use client'` directive for components using these hooks.
