---
title: Convert CRA Folder Structure to Next.js App Router
impact: CRITICAL
impactDescription: Required first step
tags: setup, structure, app-router, migration
---

## Convert CRA Folder Structure to Next.js App Router

CRA uses a flat `src/` structure with manual routing. Next.js App Router uses a `app/` directory where folders define routes.

**CRA Structure (before):**

```
my-app/
├── public/
│   └── index.html
├── src/
│   ├── index.tsx
│   ├── App.tsx
│   ├── components/
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── About.tsx
│   │   └── Users.tsx
│   └── styles/
└── package.json
```

**Next.js App Router Structure (after):**

```
my-app/
├── public/
├── app/
│   ├── layout.tsx        # Root layout (replaces index.html + App.tsx)
│   ├── page.tsx          # Home page (/)
│   ├── about/
│   │   └── page.tsx      # About page (/about)
│   ├── users/
│   │   └── page.tsx      # Users page (/users)
│   └── globals.css
├── components/           # Shared components (outside app/)
└── package.json
```

**Root Layout (app/layout.tsx):**

```tsx
// Replaces public/index.html and parts of App.tsx
import './globals.css'

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

Move shared components to a top-level `components/` directory. Page-specific components can live alongside their `page.tsx` files.
