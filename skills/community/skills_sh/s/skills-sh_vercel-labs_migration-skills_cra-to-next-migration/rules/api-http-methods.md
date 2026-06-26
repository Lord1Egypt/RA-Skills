---
title: Export Named Functions for HTTP Methods
impact: HIGH
impactDescription: HTTP method handling pattern
tags: api, http-methods, route-handlers
---

## Export Named Functions for HTTP Methods

Export functions named after HTTP methods to handle different request types.

**Express/CRA Backend (before):**

```js
// server/routes/users.js
const router = express.Router()

router.get('/', async (req, res) => {
  const users = await getUsers()
  res.json(users)
})

router.post('/', async (req, res) => {
  const user = await createUser(req.body)
  res.status(201).json(user)
})

router.put('/:id', async (req, res) => {
  const user = await updateUser(req.params.id, req.body)
  res.json(user)
})

router.delete('/:id', async (req, res) => {
  await deleteUser(req.params.id)
  res.status(204).end()
})
```

**Next.js Route Handler (after):**

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await getUsers()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await createUser(body)
  return NextResponse.json(user, { status: 201 })
}

// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await getUser(params.id)
  return NextResponse.json(user)
}

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  const body = await request.json()
  const user = await updateUser(params.id, body)
  return NextResponse.json(user)
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  await deleteUser(params.id)
  return new NextResponse(null, { status: 204 })
}
```

**Supported methods:**
`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`
