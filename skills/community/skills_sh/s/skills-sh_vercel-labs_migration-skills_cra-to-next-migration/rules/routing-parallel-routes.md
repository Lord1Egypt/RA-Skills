---
title: Use @slot for Parallel Routes
impact: LOW
impactDescription: Advanced layout pattern
tags: routing, parallel-routes, slots, layouts
---

## Use @slot for Parallel Routes

Parallel routes allow rendering multiple pages in the same layout simultaneously, useful for dashboards, modals, or split views.

**CRA with React Router (before):**

```tsx
// src/pages/Dashboard.tsx
import { Outlet } from 'react-router-dom'

export default function Dashboard() {
  return (
    <div className="dashboard">
      <div className="main-content">
        <Outlet /> {/* Main content */}
      </div>
      <div className="sidebar">
        <Analytics /> {/* Always shown */}
      </div>
    </div>
  )
}
```

**Next.js Parallel Routes (after):**

```
app/dashboard/
├── layout.tsx
├── page.tsx              # Main content
├── @analytics/           # Parallel route slot
│   └── page.tsx          # Analytics panel
└── @notifications/       # Another slot
    └── page.tsx          # Notifications panel
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  notifications,
}: {
  children: React.ReactNode
  analytics: React.ReactNode
  notifications: React.ReactNode
}) {
  return (
    <div className="dashboard">
      <div className="main">{children}</div>
      <div className="sidebar">
        {analytics}
        {notifications}
      </div>
    </div>
  )
}
```

**Use cases:**
- Dashboards with multiple independent panels
- Modal routes that don't replace the background
- Split views with independent loading states
