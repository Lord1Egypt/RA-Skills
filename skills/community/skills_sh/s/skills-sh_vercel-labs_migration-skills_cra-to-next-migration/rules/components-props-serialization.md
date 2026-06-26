---
title: Ensure Props are Serializable
impact: HIGH
impactDescription: Server-to-client data boundary
tags: components, serialization, props
---

## Ensure Props are Serializable

Props passed from Server Components to Client Components must be serializable (convertible to JSON).

**CRA Pattern (before):**

```tsx
// Can pass anything - all client-side
<UserCard
  user={user}
  onClick={() => console.log('clicked')}  // Function - fine in CRA
  renderHeader={(u) => <h1>{u.name}</h1>}  // Render prop - fine in CRA
/>
```

**Next.js - Must be serializable (after):**

```tsx
// app/page.tsx (Server Component)
import { UserCard } from './UserCard'

export default async function Page() {
  const user = await fetchUser()

  return (
    <UserCard
      user={user}                           // ✅ Object - serializable
      userId={user.id}                      // ✅ Primitive - serializable
      tags={['admin', 'active']}            // ✅ Array - serializable
      // onClick={() => {}}                 // ❌ Function - NOT serializable
      // renderHeader={(u) => <h1>{u}</h1>} // ❌ Function - NOT serializable
      // connection={dbConnection}          // ❌ Class instance - NOT serializable
    />
  )
}
```

**Serializable types:**
- Primitives: string, number, boolean, null, undefined
- Plain objects and arrays (with serializable values)
- Date (serialized as string)
- Map, Set (converted to array)
- React elements (JSX)

**Not serializable:**
- Functions, callbacks, event handlers
- Class instances
- Symbols
- Circular references

**Solution - Move logic to Client Component:**

```tsx
// page.tsx (Server Component)
export default async function Page() {
  const user = await fetchUser()
  return <UserCard user={user} /> // Just pass data
}

// UserCard.tsx (Client Component)
'use client'

export function UserCard({ user }) {
  // Define handlers in the Client Component
  const handleClick = () => {
    console.log('clicked', user.id)
  }

  return (
    <div onClick={handleClick}>
      <h1>{user.name}</h1>
    </div>
  )
}
```
