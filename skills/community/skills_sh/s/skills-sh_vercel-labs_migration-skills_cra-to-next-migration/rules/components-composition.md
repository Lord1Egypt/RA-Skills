---
title: Use Composition to Minimize Client JS
impact: HIGH
impactDescription: Keep static content as Server Components
tags: components, composition, patterns
---

## Use Composition to Minimize Client JS

Use component composition to keep Server Components for static content while Client Components handle interactivity.

**CRA Pattern (before):**

```tsx
// src/components/Sidebar.tsx
import { useState } from 'react'

export default function Sidebar({ children }) {
  const [isOpen, setIsOpen] = useState(true)

  return (
    <aside className={isOpen ? 'open' : 'closed'}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      <nav>
        <a href="/home">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
      </nav>
      {children}
    </aside>
  )
}
```

**Next.js - Composition Pattern (after):**

```tsx
// components/SidebarWrapper.tsx
'use client'

import { useState } from 'react'

export function SidebarWrapper({ children }) {
  const [isOpen, setIsOpen] = useState(true)

  return (
    <aside className={isOpen ? 'open' : 'closed'}>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {children} {/* Server Components passed as children */}
    </aside>
  )
}

// components/SidebarNav.tsx - Server Component (no 'use client')
export function SidebarNav() {
  return (
    <nav>
      <a href="/home">Home</a>
      <a href="/about">About</a>
      <a href="/contact">Contact</a>
    </nav>
  )
}

// app/layout.tsx - Server Component
import { SidebarWrapper } from '@/components/SidebarWrapper'
import { SidebarNav } from '@/components/SidebarNav'

export default function Layout({ children }) {
  return (
    <div>
      <SidebarWrapper>
        <SidebarNav /> {/* This stays a Server Component! */}
      </SidebarWrapper>
      <main>{children}</main>
    </div>
  )
}
```

**Key insight:** When you pass Server Components as `children` to a Client Component, they remain Server Components. Only the wrapper has client-side JavaScript.

This pattern is especially useful for:
- Modals with static content
- Collapsible sections
- Tab panels
- Any interactive container with static children
