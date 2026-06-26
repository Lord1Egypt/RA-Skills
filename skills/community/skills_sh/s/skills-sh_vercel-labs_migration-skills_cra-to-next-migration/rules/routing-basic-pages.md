---
title: Convert Components to File-Based Routes
impact: CRITICAL
impactDescription: Core routing paradigm change
tags: routing, pages, app-router, file-based
---

## Convert Components to File-Based Routes

CRA uses React Router for routing. Next.js uses file-based routing where the file path determines the URL.

**CRA with React Router (before):**

```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import About from './pages/About'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

// src/pages/Home.tsx
export default function Home() {
  return <h1>Home Page</h1>
}
```

**Next.js App Router (after):**

```tsx
// app/page.tsx - maps to /
export default function Home() {
  return <h1>Home Page</h1>
}

// app/about/page.tsx - maps to /about
export default function About() {
  return <h1>About Page</h1>
}

// app/dashboard/page.tsx - maps to /dashboard
export default function Dashboard() {
  return <h1>Dashboard Page</h1>
}
```

**Route mapping:**
| React Router | Next.js App Router |
|--------------|-------------------|
| `path="/"` | `app/page.tsx` |
| `path="/about"` | `app/about/page.tsx` |
| `path="/blog"` | `app/blog/page.tsx` |

No router configuration needed - the folder structure IS the routing configuration.
