---
title: Zustand Works with Hydration Care
impact: MEDIUM
impactDescription: Popular state library migration
tags: state, zustand, hydration
---

## Zustand Works with Hydration Care

Zustand works in Next.js but needs care to avoid hydration mismatches.

**CRA Pattern (before):**

```tsx
// src/stores/useStore.ts
import { create } from 'zustand'

interface Store {
  count: number
  increment: () => void
}

export const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// src/components/Counter.tsx
import { useStore } from '../stores/useStore'

export function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>{count}</button>
}
```

**Next.js - Basic usage (after):**

```tsx
// stores/useStore.ts
import { create } from 'zustand'

interface Store {
  count: number
  increment: () => void
}

export const useStore = create<Store>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))

// components/Counter.tsx
'use client'

import { useStore } from '@/stores/useStore'

export function Counter() {
  const { count, increment } = useStore()
  return <button onClick={increment}>{count}</button>
}
```

**With persistence (requires hydration handling):**

```tsx
// stores/useStore.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export const useStore = create(
  persist<Store>(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
    }),
    {
      name: 'app-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
)

// components/Counter.tsx
'use client'

import { useStore } from '@/stores/useStore'
import { useEffect, useState } from 'react'

export function Counter() {
  const [hydrated, setHydrated] = useState(false)
  const { count, increment } = useStore()

  useEffect(() => {
    setHydrated(true)
  }, [])

  if (!hydrated) return <button>0</button> // SSR fallback

  return <button onClick={increment}>{count}</button>
}
```
