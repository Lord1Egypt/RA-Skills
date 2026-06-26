---
title: Fix Hydration Mismatches
impact: HIGH
impactDescription: Server/client HTML must match
tags: gotchas, hydration, ssr
---

## Fix Hydration Mismatches

Hydration errors occur when server HTML doesn't match client render. Debug and fix them.

**Error message:**
```
Warning: Text content did not match. Server: "..." Client: "..."
Warning: Hydration failed because the initial UI does not match what was rendered on the server.
```

**Common causes and fixes:**

**1. Random values:**
```tsx
// BAD: Different on each render
function Component() {
  return <p>ID: {Math.random()}</p>
}

// GOOD: Use useId or stable values
import { useId } from 'react'
function Component() {
  const id = useId()
  return <p>ID: {id}</p>
}
```

**2. Dates/times:**
```tsx
// BAD: Server time != client time
function Component() {
  return <p>{new Date().toLocaleString()}</p>
}

// GOOD: Suppress warning or use client-only
function Component() {
  return (
    <p suppressHydrationWarning>
      {new Date().toLocaleString()}
    </p>
  )
}
```

**3. Browser-only data:**
```tsx
// BAD: localStorage doesn't exist on server
function Component() {
  const theme = localStorage.getItem('theme') || 'light'
  return <div className={theme}>...</div>
}

// GOOD: Use useEffect for client-only data
'use client'
function Component() {
  const [theme, setTheme] = useState('light')
  useEffect(() => {
    setTheme(localStorage.getItem('theme') || 'light')
  }, [])
  return <div className={theme}>...</div>
}
```

**4. Extensions modifying HTML:**
```tsx
// Browser extensions (Grammarly, etc.) can modify HTML
// Use suppressHydrationWarning on body if needed
<body suppressHydrationWarning>
```

**5. Invalid HTML nesting:**
```tsx
// BAD: <p> cannot contain <div>
<p><div>Content</div></p>

// GOOD: Use valid nesting
<div><div>Content</div></div>
```

**Solution: Client-only wrapper component:**

```tsx
'use client'

import { useEffect, useState } from 'react'

function ClientOnly({ children }) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null // Or a skeleton

  return children
}

// Usage
<ClientOnly>
  <ComponentThatUsesLocalStorage />
</ClientOnly>
```

**Solution: Dynamic import with ssr: false:**

```tsx
import dynamic from 'next/dynamic'

const ClientOnlyComponent = dynamic(
  () => import('./ClientOnlyComponent'),
  { ssr: false }
)
```

See also: `gotchas-window-undefined.md` for handling browser APIs in SSR.
