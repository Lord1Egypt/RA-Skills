---
title: Configure CORS Properly
impact: MEDIUM
impactDescription: Cross-origin requests
tags: api, cors, security
---

## Configure CORS Properly

Configure CORS (Cross-Origin Resource Sharing) for API routes that need to be accessed from different domains.

**Express/CRA Backend (before):**

```js
const cors = require('cors')

app.use(cors({
  origin: 'https://example.com',
  methods: ['GET', 'POST'],
  credentials: true,
}))
```

**Next.js Route Handler (after):**

```tsx
// app/api/data/route.ts
import { NextResponse } from 'next/server'

const corsHeaders = {
  'Access-Control-Allow-Origin': 'https://example.com',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Credentials': 'true',
}

// Handle preflight requests
export async function OPTIONS() {
  return new NextResponse(null, { headers: corsHeaders })
}

export async function GET() {
  const data = await fetchData()
  return NextResponse.json(data, { headers: corsHeaders })
}

export async function POST(request: Request) {
  const body = await request.json()
  const result = await createData(body)
  return NextResponse.json(result, { headers: corsHeaders })
}
```

**Reusable CORS helper:**

```tsx
// lib/cors.ts
export function corsResponse(data: any, status = 200) {
  return NextResponse.json(data, {
    status,
    headers: {
      'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGIN || '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  })
}

// Usage in route
import { corsResponse } from '@/lib/cors'

export async function GET() {
  const data = await fetchData()
  return corsResponse(data)
}
```

**Using next.config.js headers:**

```js
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE' },
        ],
      },
    ]
  },
}
```
