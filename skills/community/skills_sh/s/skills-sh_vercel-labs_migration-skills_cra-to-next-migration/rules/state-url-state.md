---
title: Use URL for Shareable State
impact: MEDIUM
impactDescription: SEO and sharing benefits
tags: state, url, search-params
---

## Use URL for Shareable State

Use URL search params for state that should be shareable, bookmarkable, or persist across refreshes.

**CRA Pattern (before):**

```tsx
// src/pages/Search.tsx
import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'

export function Search() {
  const [searchParams, setSearchParams] = useSearchParams()
  const query = searchParams.get('q') || ''
  const page = parseInt(searchParams.get('page') || '1')

  const updateQuery = (newQuery: string) => {
    setSearchParams({ q: newQuery, page: '1' })
  }

  return (
    <input
      value={query}
      onChange={(e) => updateQuery(e.target.value)}
    />
  )
}
```

**Next.js App Router (after):**

```tsx
// app/search/page.tsx (Server Component)
export default function SearchPage({
  searchParams,
}: {
  searchParams: { q?: string; page?: string }
}) {
  const query = searchParams.q || ''
  const page = parseInt(searchParams.page || '1')

  return (
    <div>
      <SearchInput defaultValue={query} />
      <Results query={query} page={page} />
    </div>
  )
}

// components/SearchInput.tsx
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'

export function SearchInput({ defaultValue }: { defaultValue: string }) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const createQueryString = useCallback(
    (name: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString())
      params.set(name, value)
      params.set('page', '1') // Reset page on new search
      return params.toString()
    },
    [searchParams]
  )

  return (
    <input
      defaultValue={defaultValue}
      onChange={(e) => {
        router.push(`${pathname}?${createQueryString('q', e.target.value)}`)
      }}
    />
  )
}
```

**Benefits of URL state:**
- Shareable links
- Works with back/forward buttons
- Survives page refresh
- Server-rendered with correct state
- Better SEO
