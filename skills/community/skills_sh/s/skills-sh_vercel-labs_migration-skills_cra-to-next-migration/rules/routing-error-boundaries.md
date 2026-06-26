---
title: Add error.tsx for Error Handling
impact: HIGH
impactDescription: Built-in error boundary support
tags: routing, errors, error-boundary
---

## Add error.tsx for Error Handling

CRA requires manual Error Boundaries. Next.js provides automatic error handling via `error.tsx` files.

**CRA Manual Error Boundary (before):**

```tsx
// src/components/ErrorBoundary.tsx
import { Component } from 'react'

class ErrorBoundary extends Component {
  state = { hasError: false, error: null }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h1>Something went wrong</h1>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

// Usage in App.tsx
<ErrorBoundary>
  <Dashboard />
</ErrorBoundary>
```

**Next.js App Router (after):**

```
app/dashboard/
├── layout.tsx
├── error.tsx      # Automatic error boundary
└── page.tsx
```

```tsx
// app/dashboard/error.tsx
'use client' // Error components must be Client Components

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h1>Something went wrong</h1>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

**Key features:**
- `error.tsx` must be a Client Component (`'use client'`)
- Receives `error` object and `reset` function
- Automatically wraps the route segment in an error boundary
- `reset()` re-renders the segment without a full reload

**Global error handling:**

```tsx
// app/global-error.tsx - Catches root layout errors
'use client'

export default function GlobalError({ error, reset }) {
  return (
    <html>
      <body>
        <h1>Something went wrong!</h1>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

**Error boundaries scope:**

```
app/
├── error.tsx             # Catches errors from all routes
├── products/
│   ├── error.tsx         # Catches only products errors
│   └── page.tsx
└── orders/
    └── page.tsx          # Falls back to root error.tsx
```

**Logging errors:**

```tsx
// app/products/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({ error, reset }) {
  useEffect(() => {
    // Log to error reporting service
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```
