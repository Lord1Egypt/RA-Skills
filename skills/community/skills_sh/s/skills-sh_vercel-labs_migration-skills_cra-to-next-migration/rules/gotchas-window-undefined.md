---
title: Handle window/document in SSR
impact: CRITICAL
impactDescription: Most common migration error
tags: gotchas, ssr, browser-apis
---

## Handle window/document in SSR

The most common migration issue: `window` and `document` don't exist during server-side rendering.

**CRA (works fine):**

```tsx
// Everything runs in browser
function Component() {
  const width = window.innerWidth
  const theme = localStorage.getItem('theme')
  return <div style={{ width }}>Theme: {theme}</div>
}
```

**Next.js (errors on server):**

```tsx
// ERROR: window is not defined
function Component() {
  const width = window.innerWidth // Crashes during SSR!
  return <div style={{ width }}>...</div>
}
```

**Solution 1: useEffect (runs only on client)**

```tsx
'use client'

import { useState, useEffect } from 'react'

function Component() {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // Only runs in browser
    setWidth(window.innerWidth)

    const handleResize = () => setWidth(window.innerWidth)
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return <div style={{ width: width || '100%' }}>...</div>
}
```

**Solution 2: Check for window**

```tsx
'use client'

function Component() {
  const isClient = typeof window !== 'undefined'
  const width = isClient ? window.innerWidth : 0

  return <div style={{ width: width || '100%' }}>...</div>
}
```

**Solution 3: Dynamic import with ssr: false**

```tsx
import dynamic from 'next/dynamic'

const ClientOnlyComponent = dynamic(
  () => import('./ClientOnlyComponent'),
  { ssr: false }
)

// ClientOnlyComponent will only render on client
```

**Common browser APIs that need handling:**
- `window`, `document`
- `localStorage`, `sessionStorage`
- `navigator`
- `location`
- `history`
- `matchMedia`

See also: `components-use-client.md`, `gotchas-dynamic-imports.md`
