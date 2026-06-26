---
title: Use (group) Folders for Organization
impact: MEDIUM
impactDescription: Organize routes without affecting URLs
tags: routing, route-groups, organization
---

## Use (group) Folders for Organization

CRA organizes routes in code. Next.js uses `(group)` folders to organize routes without affecting the URL structure.

**CRA with React Router (before):**

```tsx
// src/App.tsx - organized with nested routes
<Routes>
  {/* Marketing pages */}
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="/pricing" element={<Pricing />} />

  {/* App pages (with different layout) */}
  <Route element={<AppLayout />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/settings" element={<Settings />} />
  </Route>
</Routes>
```

**Next.js App Router (after):**

```
app/
├── (marketing)/          # Group - doesn't affect URL
│   ├── layout.tsx        # Marketing layout
│   ├── page.tsx          # /
│   ├── about/
│   │   └── page.tsx      # /about
│   └── pricing/
│       └── page.tsx      # /pricing
├── (app)/                # Group - doesn't affect URL
│   ├── layout.tsx        # App layout
│   ├── dashboard/
│   │   └── page.tsx      # /dashboard
│   └── settings/
│       └── page.tsx      # /settings
└── layout.tsx            # Root layout
```

```tsx
// app/(marketing)/layout.tsx
export default function MarketingLayout({ children }) {
  return (
    <div className="marketing">
      <MarketingHeader />
      {children}
      <MarketingFooter />
    </div>
  )
}

// app/(app)/layout.tsx
export default function AppLayout({ children }) {
  return (
    <div className="app">
      <Sidebar />
      {children}
    </div>
  )
}
```

Parentheses `()` in folder names are ignored in the URL path but allow separate layouts.

## Route Groups vs Route Segments

**Critical distinction:** Folders with parentheses create **route groups** (don't affect URL), while regular folders create **route segments** (add to URL):

```
app/(app)/dashboard/page.tsx  →  /dashboard      (route group - parentheses ignored)
app/app/dashboard/page.tsx    →  /app/dashboard  (route segment - adds to URL)
```

Use route groups `(folder)` when you want to:
- Share layouts between routes without affecting URLs
- Organize code logically (e.g., `(marketing)`, `(auth)`, `(dashboard)`)
- Create multiple root layouts for different sections

## Update All Hardcoded Paths When Using Route Groups

**When migrating CRA routes like `/app/dashboard` to a route group structure like `(app)/dashboard/`, you must update ALL hardcoded path references.** The old paths will return 404 errors because route group folder names are not part of the URL.

**Common symptom:** After login, the app redirects to `/app/welcome` which returns 404.

**Before (broken - path doesn't exist):**

```tsx
// src/app/page.tsx
useEffect(() => {
  if (isAuthenticated) {
    router.replace('/app/welcome')  // 404 - (app) is a route group, not a URL segment
  }
}, [])
```

**After (fixed - correct path):**

```tsx
// src/app/page.tsx
useEffect(() => {
  if (isAuthenticated) {
    router.replace('/welcome')  // Correct - matches (app)/welcome/page.tsx
  }
}, [])
```

**Files to check when using route groups:**

Update ALL of the following to remove the old path prefix:
- Root page redirects (`app/page.tsx`)
- Login/logout redirect handlers
- Sidebar and header navigation links
- Any `Link` component `href` props
- Any `router.push()` or `router.replace()` calls
- Protected route redirect logic

**Detection script:**

```bash
# Find hardcoded /app/ paths that need updating when using (app) route group
grep -rE "(href|to|push|replace|redirect|location\.href).*['\"]\/app\/" \
  --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" src/
```
