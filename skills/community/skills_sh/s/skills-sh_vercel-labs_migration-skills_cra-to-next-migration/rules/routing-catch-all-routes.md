---
title: Use [...slug] for Catch-All Routes
impact: HIGH
impactDescription: Handles variable path segments
tags: routing, catch-all, dynamic-routes
---

## Use [...slug] for Catch-All Routes

React Router uses `*` for catch-all routes. Next.js uses `[...slug]` folder syntax.

**CRA with React Router (before):**

```tsx
// src/App.tsx
<Routes>
  <Route path="/docs/*" element={<Docs />} />
</Routes>

// src/pages/Docs.tsx
import { useParams } from 'react-router-dom'

export default function Docs() {
  const { '*': splat } = useParams()
  // /docs/getting-started/installation -> splat = "getting-started/installation"
  const segments = splat?.split('/') || []
  return <h1>Docs: {segments.join(' > ')}</h1>
}
```

**Next.js App Router (after):**

```tsx
// app/docs/[...slug]/page.tsx
export default function Docs({
  params,
}: {
  params: { slug: string[] }
}) {
  // /docs/getting-started/installation -> slug = ["getting-started", "installation"]
  return <h1>Docs: {params.slug.join(' > ')}</h1>
}
```

**URL to params mapping:**

| URL | `params.slug` |
|-----|---------------|
| `/docs/intro` | `["intro"]` |
| `/docs/api/auth` | `["api", "auth"]` |
| `/docs/a/b/c` | `["a", "b", "c"]` |

Note: `/docs` alone will 404 with `[...slug]`. Use `[[...slug]]` for optional catch-all to also match `/docs`.
