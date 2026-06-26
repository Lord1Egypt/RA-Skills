---
title: Place Client Boundaries Strategically
impact: HIGH
impactDescription: Minimize client bundle size
tags: components, boundaries, optimization
---

## Place Client Boundaries Strategically

Push `'use client'` boundaries as low as possible in the component tree to minimize client JavaScript.

**CRA Pattern - Everything is client (before):**

```tsx
// src/pages/ProductPage.tsx
// Entire page is client-rendered
export default function ProductPage() {
  const [quantity, setQuantity] = useState(1)
  const product = useProduct()

  return (
    <div>
      <ProductHeader product={product} />
      <ProductDescription description={product.description} />
      <ProductSpecs specs={product.specs} />
      <QuantitySelector value={quantity} onChange={setQuantity} />
      <AddToCartButton product={product} quantity={quantity} />
    </div>
  )
}
```

**Next.js - Client boundary at leaf (after):**

```tsx
// app/products/[id]/page.tsx - Server Component
import { QuantitySelector } from './QuantitySelector'
import { AddToCartButton } from './AddToCartButton'

export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.id)

  return (
    <div>
      {/* These are Server Components - zero JS */}
      <ProductHeader product={product} />
      <ProductDescription description={product.description} />
      <ProductSpecs specs={product.specs} />

      {/* Only interactive parts are Client Components */}
      <QuantitySelector productId={product.id} />
      <AddToCartButton product={product} />
    </div>
  )
}

// components/QuantitySelector.tsx
'use client'

export function QuantitySelector({ productId }) {
  const [quantity, setQuantity] = useState(1)
  // Only this small component ships JS to client
  return (...)
}
```

**Bad - Boundary too high:**

```tsx
// DON'T: Making entire page client-side
'use client'

export default function ProductPage() {
  // Now EVERYTHING is client-rendered
}
```

**Good - Boundary at interactive leaf:**

```tsx
// DO: Only the interactive button is client
// components/LikeButton.tsx
'use client'

export function LikeButton({ postId }) {
  const [liked, setLiked] = useState(false)
  return <button onClick={() => setLiked(!liked)}>Like</button>
}
```
