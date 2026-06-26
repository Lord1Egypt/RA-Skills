---
title: Create Route Handlers in app/api
impact: HIGH
impactDescription: Backend API endpoints
tags: api, route-handlers, backend
---

## Create Route Handlers in app/api

CRA typically uses a separate backend or proxied API. Next.js provides built-in API routes.

**CRA Pattern (before):**

```tsx
// Separate Express server or proxy setup
// setupProxy.js
const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function(app) {
  app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5000',
  }))
}
```

**Next.js Route Handler (after):**

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await db.users.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await db.users.create({ data: body })
  return NextResponse.json(user, { status: 201 })
}
```

**Route structure:**

```
app/
├── api/
│   ├── users/
│   │   ├── route.ts          # /api/users
│   │   └── [id]/
│   │       └── route.ts      # /api/users/[id]
│   ├── posts/
│   │   └── route.ts          # /api/posts
│   └── health/
│       └── route.ts          # /api/health
```

**Calling from components:**

```tsx
// Client component
'use client'

async function createUser(data) {
  const res = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return res.json()
}
```

Note: For simple data mutations, consider Server Actions instead of API routes.
