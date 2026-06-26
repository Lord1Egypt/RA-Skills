---
title: Parse Request Body Properly
impact: MEDIUM
impactDescription: Handle POST/PUT data
tags: api, request-body, parsing
---

## Parse Request Body Properly

Next.js Route Handlers use the Web Request API for parsing request bodies.

**Express/CRA Backend (before):**

```js
// With body-parser middleware
app.use(express.json())

router.post('/users', async (req, res) => {
  const { name, email } = req.body  // Already parsed
  // ...
})
```

**Next.js Route Handler (after):**

```tsx
// app/api/users/route.ts

// JSON body
export async function POST(request: Request) {
  const body = await request.json()
  const { name, email } = body
  // ...
  return NextResponse.json({ success: true })
}

// Form data
export async function POST(request: Request) {
  const formData = await request.formData()
  const name = formData.get('name')
  const file = formData.get('file') as File
  // ...
}

// Text body
export async function POST(request: Request) {
  const text = await request.text()
  // ...
}

// ArrayBuffer (binary)
export async function POST(request: Request) {
  const buffer = await request.arrayBuffer()
  // ...
}
```

**With validation (using Zod):**

```tsx
import { z } from 'zod'
import { NextResponse } from 'next/server'

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
})

export async function POST(request: Request) {
  const body = await request.json()

  const result = userSchema.safeParse(body)
  if (!result.success) {
    return NextResponse.json(
      { error: result.error.flatten() },
      { status: 400 }
    )
  }

  const user = await createUser(result.data)
  return NextResponse.json(user, { status: 201 })
}
```
