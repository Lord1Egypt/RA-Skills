---
title: Convert Nested Routes to Layouts
impact: HIGH
impactDescription: Different nesting paradigm
tags: routing, layouts, nested-routes
---

## Convert Nested Routes to Layouts

React Router uses `<Outlet />` for nested routes. Next.js uses `layout.tsx` files that wrap child routes.

**CRA with React Router (before):**

```tsx
// src/App.tsx
<Routes>
  <Route element={<RootLayout />}>
    <Route path="/" element={<Home />} />
    <Route path="/dashboard" element={<DashboardLayout />}>
      <Route index element={<DashboardHome />} />
      <Route path="settings" element={<Settings />} />
      <Route path="profile" element={<Profile />} />
    </Route>
  </Route>
</Routes>

// src/layouts/DashboardLayout.tsx
import { Outlet } from 'react-router-dom'

export default function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>
        <Outlet />
      </main>
    </div>
  )
}
```

**Next.js App Router (after):**

```
app/
├── layout.tsx              # Root layout
├── page.tsx                # Home (/)
└── dashboard/
    ├── layout.tsx          # Dashboard layout
    ├── page.tsx            # Dashboard home (/dashboard)
    ├── settings/
    │   └── page.tsx        # /dashboard/settings
    └── profile/
        └── page.tsx        # /dashboard/profile
```

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

// app/dashboard/layout.tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>{children}</main>
    </div>
  )
}

// app/dashboard/page.tsx
export default function DashboardHome() {
  return <h1>Dashboard</h1>
}
```

**Key differences:**
- `children` prop replaces `<Outlet />`
- Layouts automatically wrap all child routes
- Layouts don't re-render on navigation between child pages
