---
title: Test API Route Handlers
impact: MEDIUM
impactDescription: Testing backend endpoints
tags: testing, api-routes, handlers
---

## Test API Route Handlers

Test Route Handlers by calling them directly or using integration tests.

**Route Handler:**

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

**Unit testing Route Handlers:**

```tsx
// app/api/users/route.test.ts
import { GET, POST } from './route'
import { NextRequest } from 'next/server'

// Mock the database
jest.mock('@/lib/db', () => ({
  users: {
    findMany: jest.fn(),
    create: jest.fn(),
  },
}))

import { db } from '@/lib/db'

describe('GET /api/users', () => {
  test('returns users', async () => {
    const mockUsers = [{ id: 1, name: 'John' }]
    ;(db.users.findMany as jest.Mock).mockResolvedValue(mockUsers)

    const response = await GET()
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data).toEqual(mockUsers)
  })
})

describe('POST /api/users', () => {
  test('creates a user', async () => {
    const newUser = { name: 'Jane', email: 'jane@example.com' }
    const createdUser = { id: 1, ...newUser }
    ;(db.users.create as jest.Mock).mockResolvedValue(createdUser)

    const request = new NextRequest('http://localhost/api/users', {
      method: 'POST',
      body: JSON.stringify(newUser),
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data).toEqual(createdUser)
  })
})
```

**Integration testing with fetch:**

```tsx
// __tests__/api/users.integration.test.ts
describe('Users API', () => {
  test('GET /api/users', async () => {
    const response = await fetch('http://localhost:3000/api/users')
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(Array.isArray(data)).toBe(true)
  })
})
```
