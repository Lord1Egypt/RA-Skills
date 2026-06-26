---
title: Understand useEffect in Next.js
impact: MEDIUM
impactDescription: useEffect timing differs
tags: gotchas, useEffect, lifecycle
---

## Understand useEffect in Next.js

useEffect behavior in Next.js differs from CRA due to Server Components and SSR.

**Key differences:**

1. **Server Components don't have useEffect**
2. **useEffect only runs on client**
3. **Initial render is server-side (no useEffect)**

**CRA (always runs):**

```tsx
function Component() {
  useEffect(() => {
    console.log('Component mounted')
    // Always runs after mount
  }, [])

  return <div>Content</div>
}
```

**Next.js Client Component:**

```tsx
'use client'

function Component() {
  useEffect(() => {
    // Runs ONLY on client after hydration
    // Does NOT run during SSR
    console.log('Component hydrated')
  }, [])

  return <div>Content</div>
}
```

**Common patterns:**

**Initialize client-only state:**
```tsx
'use client'

function Component() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  // Render differently before/after mount
  if (!mounted) {
    return <Skeleton />
  }

  return <ClientFeature />
}
```

**Fetch data (prefer Server Components instead):**
```tsx
// Instead of useEffect for data fetching...
'use client'
function OldPattern() {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch('/api/data').then(r => r.json()).then(setData)
  }, [])
}

// ...use Server Components
async function NewPattern() {
  const data = await fetch('/api/data').then(r => r.json())
  return <DataDisplay data={data} />
}
```

**Setup subscriptions/intervals:**
```tsx
'use client'

function LiveClock() {
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(interval)
  }, [])

  return <span suppressHydrationWarning>{time.toLocaleTimeString()}</span>
}
```
