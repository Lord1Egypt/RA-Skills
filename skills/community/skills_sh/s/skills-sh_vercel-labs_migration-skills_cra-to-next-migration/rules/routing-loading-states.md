---
title: Add loading.tsx for Suspense
impact: HIGH
impactDescription: Built-in loading UI support
tags: routing, loading, suspense
---

## Add loading.tsx for Suspense

CRA requires manual loading states. Next.js provides automatic loading UI via `loading.tsx` files.

**CRA Manual Loading (before):**

```tsx
// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return <DashboardContent data={data} />
}
```

**Next.js App Router (after):**

```
app/dashboard/
├── layout.tsx
├── loading.tsx    # Automatic loading UI
└── page.tsx
```

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <LoadingSpinner />
}

// app/dashboard/page.tsx
// Server Component - can be async!
export default async function Dashboard() {
  const data = await fetchDashboardData() // No loading state needed
  return <DashboardContent data={data} />
}
```

**How it works:**
- `loading.tsx` creates a Suspense boundary
- Shown automatically while `page.tsx` loads
- Can be placed at any level for different loading UIs

**With Suspense for partial loading:**

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<ChartSkeleton />}>
        <Charts />
      </Suspense>
      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>
    </div>
  )
}
```

**Nested loading states:**

```
app/
├── loading.tsx           # Global loading
├── products/
│   ├── loading.tsx       # Products section loading
│   └── page.tsx
└── orders/
    ├── loading.tsx       # Orders section loading
    └── page.tsx
```

**Shared skeleton component:**

```tsx
// components/skeletons.tsx
export function ProductSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="bg-gray-200 h-48 rounded" />
      <div className="bg-gray-200 h-4 mt-2 rounded w-3/4" />
      <div className="bg-gray-200 h-4 mt-1 rounded w-1/2" />
    </div>
  )
}

// app/products/loading.tsx
import { ProductSkeleton } from '@/components/skeletons'

export default function Loading() {
  return (
    <div className="grid grid-cols-4 gap-4">
      {Array.from({ length: 8 }).map((_, i) => (
        <ProductSkeleton key={i} />
      ))}
    </div>
  )
}
```
