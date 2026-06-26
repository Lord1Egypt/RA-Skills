---
title: Use (..) for Intercepting Routes
impact: LOW
impactDescription: Advanced modal pattern
tags: routing, intercepting-routes, modals
---

## Use (..) for Intercepting Routes

Intercepting routes let you show a route in a modal while keeping the background context, with the full page accessible via direct URL.

**CRA Modal Pattern (before):**

```tsx
// src/pages/Gallery.tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Gallery() {
  const [selectedPhoto, setSelectedPhoto] = useState(null)

  return (
    <div>
      {photos.map(photo => (
        <img
          key={photo.id}
          onClick={() => setSelectedPhoto(photo)}
        />
      ))}
      {selectedPhoto && (
        <Modal onClose={() => setSelectedPhoto(null)}>
          <PhotoDetail photo={selectedPhoto} />
        </Modal>
      )}
    </div>
  )
}
```

**Next.js Intercepting Routes (after):**

```
app/
├── @modal/                    # Parallel route for modal
│   ├── (.)photos/[id]/        # Intercepts /photos/[id]
│   │   └── page.tsx           # Modal view
│   └── default.tsx            # Default (no modal)
├── photos/
│   └── [id]/
│       └── page.tsx           # Full page view
├── layout.tsx
└── page.tsx                   # Gallery
```

```tsx
// app/@modal/(.)photos/[id]/page.tsx
export default function PhotoModal({ params }: { params: { id: string } }) {
  return (
    <Modal>
      <PhotoDetail id={params.id} />
    </Modal>
  )
}

// app/photos/[id]/page.tsx - Direct URL shows full page
export default function PhotoPage({ params }: { params: { id: string } }) {
  return <PhotoDetail id={params.id} />
}

// app/layout.tsx
export default function Layout({ children, modal }) {
  return (
    <>
      {children}
      {modal}
    </>
  )
}
```

**Convention:**
- `(.)` - Same level
- `(..)` - One level up
- `(..)(..)` - Two levels up
- `(...)` - From root
