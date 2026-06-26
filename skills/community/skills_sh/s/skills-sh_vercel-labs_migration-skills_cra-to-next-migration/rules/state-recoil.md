---
title: Configure Recoil Properly
impact: MEDIUM
impactDescription: Recoil requires RecoilRoot
tags: state, recoil, atoms
---

## Configure Recoil Properly

Recoil requires wrapping your app in `RecoilRoot` with a Client Component.

**CRA Pattern (before):**

```tsx
// src/atoms.ts
import { atom } from 'recoil'

export const countState = atom({
  key: 'countState',
  default: 0,
})

// src/App.tsx
import { RecoilRoot } from 'recoil'

function App() {
  return (
    <RecoilRoot>
      <Main />
    </RecoilRoot>
  )
}

// src/components/Counter.tsx
import { useRecoilState } from 'recoil'
import { countState } from '../atoms'

export function Counter() {
  const [count, setCount] = useRecoilState(countState)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**Next.js Pattern (after):**

```tsx
// atoms/index.ts
import { atom } from 'recoil'

export const countState = atom({
  key: 'countState',
  default: 0,
})

// providers/RecoilProvider.tsx
'use client'

import { RecoilRoot } from 'recoil'

export function RecoilProvider({ children }: { children: React.ReactNode }) {
  return <RecoilRoot>{children}</RecoilRoot>
}

// app/layout.tsx
import { RecoilProvider } from '@/providers/RecoilProvider'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <RecoilProvider>{children}</RecoilProvider>
      </body>
    </html>
  )
}

// components/Counter.tsx
'use client'

import { useRecoilState } from 'recoil'
import { countState } from '@/atoms'

export function Counter() {
  const [count, setCount] = useRecoilState(countState)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**Note:** Recoil has limited maintenance. Consider Jotai as a more actively maintained alternative with similar API.
