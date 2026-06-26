---
title: Pass Server Components as Children
impact: MEDIUM
impactDescription: Preserve Server Component benefits
tags: components, children, patterns
---

## Pass Server Components as Children

Use the children prop to pass Server Components into Client Components, preserving their server-rendered benefits.

**CRA Pattern (before):**

```tsx
// Everything is client - no distinction needed
function Modal({ children }) {
  const [open, setOpen] = useState(false)
  return open ? <div className="modal">{children}</div> : null
}
```

**Next.js Pattern (after):**

```tsx
// components/Modal.tsx
'use client'

import { useState } from 'react'

export function Modal({ children, trigger }) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>{trigger}</button>
      {open && (
        <div className="modal">
          <button onClick={() => setOpen(false)}>Close</button>
          {children} {/* Server Components remain server-rendered */}
        </div>
      )}
    </>
  )
}

// app/page.tsx (Server Component)
import { Modal } from '@/components/Modal'

export default async function Page() {
  const data = await fetchData() // Server-side fetch

  return (
    <Modal trigger="Open Details">
      {/* This content is server-rendered, not client JS */}
      <h2>{data.title}</h2>
      <p>{data.description}</p>
      <DataTable rows={data.rows} />
    </Modal>
  )
}
```

**Why this matters:**

```tsx
// BAD: All content becomes client-side
'use client'

export function Modal() {
  const data = useData() // Client fetch, more JS
  return <div>{/* ... */}</div>
}

// GOOD: Server content passed as children
export function Modal({ children }) {
  return <div>{children}</div> // children already rendered on server
}
```

**Also works with render props pattern:**

```tsx
// page.tsx (Server Component)
const serverContent = <ServerRenderedContent data={data} />

return (
  <ClientTabs
    tabs={[
      { label: 'Tab 1', content: serverContent },
      { label: 'Tab 2', content: <OtherServerContent /> },
    ]}
  />
)
```
