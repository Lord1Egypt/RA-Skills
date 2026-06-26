---
title: Handle Hash-Based Routing
impact: MEDIUM
impactDescription: Client-side hash routing patterns
tags: routing, hash, client-only, spa
---

## Handle Hash-Based Routing

Some CRA applications use hash-based routing (`#/path` or `#key=value`) for client-side state that shouldn't trigger server requests. This pattern requires special handling in Next.js.

**CRA Pattern (before):**

```tsx
// Hash used for client-side state (e.g., collaboration rooms, shared content)
// URL: https://app.com/#room=abc123,key=xyz
// URL: https://app.com/#json=documentId,encryptionKey

function App() {
  const [roomId, setRoomId] = useState<string | null>(null)

  useEffect(() => {
    const hash = window.location.hash
    const params = parseHash(hash) // Custom parser for #room=x,key=y
    if (params.room) {
      setRoomId(params.room)
      joinRoom(params.room, params.key)
    }
  }, [])

  // Listen for hash changes
  useEffect(() => {
    const handleHashChange = () => {
      const params = parseHash(window.location.hash)
      // Handle state change
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  return <Editor roomId={roomId} />
}
```

**Next.js Pattern (after):**

Hash-based routing requires client-side rendering since the hash is never sent to the server.

**1. Create a client-only page:**

```tsx
// app/page.tsx
import dynamic from 'next/dynamic'

// Load the entire app client-side only
const App = dynamic(() => import('@/components/App'), {
  ssr: false,
  loading: () => <LoadingSkeleton />,
})

export default function Page() {
  return <App />
}
```

**2. Handle hash in the client component:**

```tsx
// components/App.tsx
'use client'

import { useState, useEffect } from 'react'

function parseHash(hash: string): Record<string, string> {
  // Example: #room=abc,key=xyz -> { room: 'abc', key: 'xyz' }
  if (!hash || hash === '#') return {}

  const params: Record<string, string> = {}
  const parts = hash.slice(1).split(',')

  for (const part of parts) {
    const [key, value] = part.split('=')
    if (key && value) {
      params[key] = value
    }
  }

  return params
}

export default function App() {
  const [hashParams, setHashParams] = useState<Record<string, string>>({})
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    // Initial hash read
    setHashParams(parseHash(window.location.hash))
    setIsLoaded(true)

    // Listen for hash changes
    const handleHashChange = () => {
      setHashParams(parseHash(window.location.hash))
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  if (!isLoaded) {
    return <LoadingSkeleton />
  }

  if (hashParams.room) {
    return <CollaborationRoom roomId={hashParams.room} encryptionKey={hashParams.key} />
  }

  if (hashParams.json) {
    return <SharedDocument documentId={hashParams.json} encryptionKey={hashParams.key} />
  }

  return <Editor />
}
```

**3. Update hash programmatically:**

```tsx
'use client'

function setHashParams(params: Record<string, string>) {
  const hash = Object.entries(params)
    .map(([key, value]) => `${key}=${value}`)
    .join(',')

  // Update without triggering navigation
  window.history.replaceState(null, '', `#${hash}`)

  // Or trigger hashchange event
  window.location.hash = hash
}

// Usage
function shareRoom(roomId: string, key: string) {
  setHashParams({ room: roomId, key })
}
```

**Why hash routing?**

Hash-based routing is used when:
- State should not be sent to the server (security/privacy)
- Encryption keys in URLs (end-to-end encrypted apps)
- Real-time collaboration room IDs
- Sharing state that's purely client-side
- Legacy URL compatibility requirements

**Alternative: Use searchParams for server-compatible state**

If the state doesn't need to be hidden from the server, use query parameters instead:

```tsx
// app/editor/page.tsx
export default function EditorPage({
  searchParams,
}: {
  searchParams: { room?: string; key?: string }
}) {
  // Can be read on server
  const { room, key } = searchParams

  return <Editor roomId={room} encryptionKey={key} />
}
```

**Verification checklist for hash routing:**

- [ ] Hash parameters are read correctly on initial load
- [ ] Hash changes trigger state updates
- [ ] Direct URL access with hash works (e.g., `/#room=abc,key=xyz`)
- [ ] Sharing URLs with hash preserves functionality
- [ ] Browser back/forward with hash changes works
