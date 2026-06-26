---
title: Server Components are Default
impact: HIGH
impactDescription: Fundamental paradigm shift
tags: components, server-components, rsc
---

## Server Components are Default

In Next.js App Router, all components are Server Components by default. This is a key paradigm shift from CRA.

**CRA Mental Model (before):**

```tsx
// Everything runs in the browser
// All components are "client components"

export default function ProductList() {
  // This code runs in the browser
  const products = useProducts() // Client-side fetch
  return <Grid items={products} />
}
```

**Next.js Mental Model (after):**

```tsx
// app/products/page.tsx
// This is a SERVER Component by default

export default async function ProductList() {
  // This code runs on the SERVER
  const products = await db.products.findMany() // Direct DB access!

  return <Grid items={products} />
}
```

**Server Component benefits:**
- Direct database/filesystem access
- Keep sensitive data on server (API keys, tokens)
- Zero client-side JavaScript for static content
- Better performance (no hydration needed)
- Automatic code splitting

**Server Component limitations:**
- No `useState`, `useEffect`, `useReducer`
- No event handlers (`onClick`, `onChange`)
- No browser APIs
- No `useContext`
- No custom hooks that use the above

**Practical implication:**

```tsx
// app/page.tsx - Server Component
import ClientButton from './ClientButton'

export default async function Page() {
  const data = await fetchData() // Runs on server

  return (
    <div>
      <h1>{data.title}</h1>
      {/* Interactive parts use Client Components */}
      <ClientButton />
    </div>
  )
}
```

Think: "What needs interactivity?" Only those parts need `'use client'`.
