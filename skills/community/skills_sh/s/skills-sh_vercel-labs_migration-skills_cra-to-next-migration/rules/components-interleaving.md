---
title: Interleave Server and Client Components
impact: MEDIUM
impactDescription: Optimal component architecture
tags: components, interleaving, architecture
---

## Interleave Server and Client Components

Server and Client Components can be mixed throughout your component tree. Understand the rendering rules.

**CRA Mental Model (before):**

```tsx
// Flat - everything is client
<App>
  <Header />
  <Sidebar />
  <Content />
  <Footer />
</App>
```

**Next.js Interleaving (after):**

```tsx
// app/page.tsx (Server Component)
import { ClientCounter } from './ClientCounter'

export default async function Page() {
  const data = await fetchData() // Server

  return (
    <div>
      <ServerHeader data={data} />        {/* Server */}
      <ClientCounter />                    {/* Client */}
      <ServerContent data={data}>          {/* Server */}
        <ClientInteractive />              {/* Client */}
        <ServerNested>                     {/* Server (via children) */}
          <ClientButton />                 {/* Client */}
        </ServerNested>
      </ServerContent>
    </div>
  )
}
```

**Rules for interleaving:**

1. **Server → Client**: Server Components can import Client Components
2. **Client → Server**: Client Components can accept Server Components as `children` or props
3. **Client cannot import Server**: Can't `import ServerComponent from './Server'` in a Client Component

**Pattern: Server in Client via children:**

```tsx
// ClientModal.tsx
'use client'

export function ClientModal({ children, isOpen }) {
  if (!isOpen) return null
  return <div className="modal">{children}</div>
}

// page.tsx (Server Component)
import { ClientModal } from './ClientModal'
import { ServerContent } from './ServerContent'

export default function Page() {
  return (
    <ClientModal isOpen={true}>
      <ServerContent /> {/* Works! Passed as children */}
    </ClientModal>
  )
}
```

**This won't work:**

```tsx
// ClientComponent.tsx
'use client'
import ServerComponent from './ServerComponent' // Error!

export function ClientComponent() {
  return <ServerComponent /> // Can't import Server in Client
}
```
