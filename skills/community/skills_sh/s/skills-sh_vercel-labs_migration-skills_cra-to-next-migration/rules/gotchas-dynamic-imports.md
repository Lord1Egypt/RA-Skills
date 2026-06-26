---
title: Use next/dynamic Properly
impact: MEDIUM
impactDescription: Code splitting patterns
tags: gotchas, dynamic-import, code-splitting
---

## Use next/dynamic Properly

Use `next/dynamic` for code splitting and client-only components instead of React.lazy.

**CRA with React.lazy:**

```tsx
import { lazy, Suspense } from 'react'

const HeavyComponent = lazy(() => import('./HeavyComponent'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  )
}
```

**Next.js with next/dynamic:**

```tsx
import dynamic from 'next/dynamic'

// Basic dynamic import
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />,
})

// Client-only component (no SSR)
const ClientOnlyChart = dynamic(() => import('./Chart'), {
  ssr: false,
  loading: () => <ChartSkeleton />,
})

// Named export
const Modal = dynamic(
  () => import('./components').then((mod) => mod.Modal),
  { loading: () => <ModalSkeleton /> }
)
```

**Common use cases:**

**1. Heavy libraries (charts, editors):**
```tsx
const Chart = dynamic(() => import('recharts').then(m => m.LineChart), {
  ssr: false, // Charts often need browser APIs
})
```

**2. Below-the-fold content:**
```tsx
const Comments = dynamic(() => import('./Comments'), {
  loading: () => <CommentsSkeleton />,
})
```

**3. Modals (loaded on demand):**
```tsx
const SettingsModal = dynamic(() => import('./SettingsModal'))

function App() {
  const [showSettings, setShowSettings] = useState(false)

  return (
    <>
      <button onClick={() => setShowSettings(true)}>Settings</button>
      {showSettings && <SettingsModal onClose={() => setShowSettings(false)} />}
    </>
  )
}
```

**Don't overuse:** Only use dynamic imports for large components that aren't needed immediately.

See also: `components-third-party.md` for wrapping third-party client components.
