---
title: Configure Jotai Properly
impact: MEDIUM
impactDescription: Atomic state management
tags: state, jotai, atoms
---

## Configure Jotai Properly

Jotai has excellent Next.js support with minimal configuration needed.

**CRA Pattern (before):**

```tsx
// src/atoms.ts
import { atom } from 'jotai'

export const countAtom = atom(0)

// src/components/Counter.tsx
import { useAtom } from 'jotai'
import { countAtom } from '../atoms'

export function Counter() {
  const [count, setCount] = useAtom(countAtom)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**Next.js Pattern (after):**

```tsx
// atoms/index.ts
import { atom } from 'jotai'

export const countAtom = atom(0)

// components/Counter.tsx
'use client'

import { useAtom } from 'jotai'
import { countAtom } from '@/atoms'

export function Counter() {
  const [count, setCount] = useAtom(countAtom)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**With Provider (for SSR hydration):**

```tsx
// providers/JotaiProvider.tsx
'use client'

import { Provider } from 'jotai'

export function JotaiProvider({ children }: { children: React.ReactNode }) {
  return <Provider>{children}</Provider>
}

// app/layout.tsx
import { JotaiProvider } from '@/providers/JotaiProvider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <JotaiProvider>{children}</JotaiProvider>
      </body>
    </html>
  )
}
```

**Hydration with persisted atoms:**

```tsx
// atoms/index.ts
import { atomWithStorage } from 'jotai/utils'

// Automatically synced with localStorage
export const themeAtom = atomWithStorage('theme', 'light')

// components/ThemeToggle.tsx
'use client'

import { useAtom } from 'jotai'
import { themeAtom } from '@/atoms'
import { useHydrateAtoms } from 'jotai/utils'

export function ThemeToggle() {
  const [theme, setTheme] = useAtom(themeAtom)

  return (
    <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
      {theme}
    </button>
  )
}
```
