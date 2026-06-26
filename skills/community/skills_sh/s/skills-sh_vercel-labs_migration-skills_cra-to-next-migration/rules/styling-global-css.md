---
title: Move Global CSS to app/layout.tsx
impact: CRITICAL
impactDescription: CSS import location changes
tags: styling, css, global-styles
---

## Move Global CSS to app/layout.tsx

CRA imports global CSS in `index.tsx`. Next.js App Router imports global CSS in the root `layout.tsx`.

**CRA Pattern (before):**

```tsx
// src/index.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'        // Global styles
import './styles/reset.css' // Reset styles
import App from './App'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

**Next.js App Router (after):**

```tsx
// app/layout.tsx
import './globals.css'        // Global styles
import './styles/reset.css'   // Reset styles

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**File organization:**

```
app/
├── globals.css    # Global styles (imported in layout.tsx)
├── layout.tsx     # Root layout
└── page.tsx

# Or keep in styles folder
styles/
├── globals.css
└── reset.css

app/
├── layout.tsx     # import '@/styles/globals.css'
└── page.tsx
```

**Important notes:**
- Global CSS can ONLY be imported in `layout.tsx` or via CSS Modules
- Importing global CSS in `page.tsx` or components will cause an error
- This prevents style conflicts and ensures predictable loading order
