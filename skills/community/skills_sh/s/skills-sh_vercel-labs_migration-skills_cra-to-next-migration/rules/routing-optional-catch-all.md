---
title: Use [[...slug]] for Optional Catch-All
impact: MEDIUM
impactDescription: Matches routes with or without segments
tags: routing, catch-all, optional, dynamic-routes
---

## Use [[...slug]] for Optional Catch-All

When you need to match both the base route AND all sub-routes, use optional catch-all `[[...slug]]`.

**CRA with React Router (before):**

```tsx
// src/App.tsx
<Routes>
  <Route path="/shop" element={<Shop />} />
  <Route path="/shop/*" element={<Shop />} />
</Routes>

// src/pages/Shop.tsx
import { useParams } from 'react-router-dom'

export default function Shop() {
  const { '*': category } = useParams()
  // /shop -> category = undefined
  // /shop/electronics/phones -> category = "electronics/phones"
  return <div>{category ? `Category: ${category}` : 'All Products'}</div>
}
```

**Next.js App Router (after):**

```tsx
// app/shop/[[...slug]]/page.tsx
export default function Shop({
  params,
}: {
  params: { slug?: string[] }
}) {
  // /shop -> slug = undefined
  // /shop/electronics -> slug = ["electronics"]
  // /shop/electronics/phones -> slug = ["electronics", "phones"]

  if (!params.slug) {
    return <div>All Products</div>
  }

  return <div>Category: {params.slug.join(' > ')}</div>
}
```

**Comparison:**

| Folder | `/shop` | `/shop/a` | `/shop/a/b` |
|--------|---------|-----------|-------------|
| `[...slug]` | 404 | Match | Match |
| `[[...slug]]` | Match | Match | Match |
