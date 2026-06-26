---
title: Access Query Parameters
impact: MEDIUM
impactDescription: Handle URL query strings
tags: api, query-params, url
---

## Access Query Parameters

Access URL query parameters using the URL API in Next.js Route Handlers.

**Express/CRA Backend (before):**

```js
// GET /api/users?page=1&limit=10&search=john
router.get('/users', async (req, res) => {
  const { page, limit, search } = req.query
  const users = await getUsers({ page, limit, search })
  res.json(users)
})
```

**Next.js Route Handler (after):**

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const page = searchParams.get('page') || '1'
  const limit = searchParams.get('limit') || '10'
  const search = searchParams.get('search') || ''

  const users = await getUsers({
    page: parseInt(page),
    limit: parseInt(limit),
    search,
  })

  return NextResponse.json(users)
}
```

**Multiple values for same param:**

```tsx
// GET /api/users?tag=react&tag=typescript
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const tags = searchParams.getAll('tag')  // ['react', 'typescript']
  // ...
}
```

**Check if param exists:**

```tsx
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams

  if (searchParams.has('featured')) {
    // ?featured or ?featured=true
  }

  // Iterate all params
  for (const [key, value] of searchParams) {
    console.log(`${key}: ${value}`)
  }
}
```

**Type-safe parsing:**

```tsx
import { z } from 'zod'

const querySchema = z.object({
  page: z.coerce.number().default(1),
  limit: z.coerce.number().default(10),
  search: z.string().optional(),
})

export async function GET(request: NextRequest) {
  const params = Object.fromEntries(request.nextUrl.searchParams)
  const { page, limit, search } = querySchema.parse(params)
  // ...
}
```
