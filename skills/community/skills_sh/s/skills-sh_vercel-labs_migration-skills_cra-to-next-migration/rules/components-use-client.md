---
title: Add 'use client' Directive for Client Components
impact: CRITICAL
impactDescription: Required for interactive components
tags: components, use-client, client-components
---

## Add 'use client' Directive for Client Components

In Next.js App Router, components are Server Components by default. Add `'use client'` for components that need browser APIs or React hooks.

**CRA Pattern (before):**

```tsx
// All components are client components by default
// src/components/Counter.tsx
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

**Next.js App Router (after):**

```tsx
// components/Counter.tsx
'use client' // Required! Must be at the top of the file

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  )
}
```

**When you need 'use client':**

| Feature | Needs 'use client' |
|---------|-------------------|
| `useState`, `useReducer` | Yes |
| `useEffect`, `useLayoutEffect` | Yes |
| `onClick`, `onChange`, etc. | Yes |
| `useContext` | Yes |
| Browser APIs (window, document) | Yes |
| Third-party hooks | Usually yes |
| Just rendering props | No |
| Async data fetching | No (prefer Server) |

**Common mistake - unnecessary 'use client':**

```tsx
// DON'T add 'use client' just for props
// This can be a Server Component
export default function UserCard({ user }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  )
}
```

See also: `gotchas-window-undefined.md` for handling browser APIs in SSR.
