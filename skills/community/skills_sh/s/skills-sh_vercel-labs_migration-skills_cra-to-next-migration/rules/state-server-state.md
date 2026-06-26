---
title: Minimize Client State with RSC
impact: HIGH
impactDescription: Rethink state architecture
tags: state, rsc, server-components
---

## Minimize Client State with RSC

Server Components eliminate the need for much client-side state. Rethink what truly needs to be client state.

**CRA Pattern (before):**

```tsx
// Lots of client state for data that could be server-rendered
export function ProductPage() {
  const [product, setProduct] = useState(null)
  const [reviews, setReviews] = useState([])
  const [relatedProducts, setRelatedProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchProduct(id),
      fetchReviews(id),
      fetchRelated(id),
    ]).then(([p, r, rel]) => {
      setProduct(p)
      setReviews(r)
      setRelatedProducts(rel)
      setLoading(false)
    })
  }, [id])

  if (loading) return <Loading />
  return /* ... */
}
```

**Next.js Pattern (after):**

```tsx
// app/products/[id]/page.tsx (Server Component)
// No client state needed for this data!
export default async function ProductPage({ params }) {
  // Parallel fetch on server
  const [product, reviews, relatedProducts] = await Promise.all([
    fetchProduct(params.id),
    fetchReviews(params.id),
    fetchRelated(params.id),
  ])

  return (
    <div>
      <ProductInfo product={product} />
      <Reviews reviews={reviews} />
      <RelatedProducts products={relatedProducts} />
      {/* Only interactive parts need client state */}
      <AddToCartButton productId={product.id} />
    </div>
  )
}

// Only this small component needs client state
// components/AddToCartButton.tsx
'use client'

export function AddToCartButton({ productId }) {
  const [quantity, setQuantity] = useState(1)
  const [adding, setAdding] = useState(false)

  return (
    <div>
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(Number(e.target.value))}
      />
      <button onClick={/* ... */} disabled={adding}>
        Add to Cart
      </button>
    </div>
  )
}
```

**What still needs client state:**
- Form inputs during editing
- UI state (modals, dropdowns, tabs)
- Optimistic updates
- Real-time data
- User interactions before submit
