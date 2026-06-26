---
title: Implement Rate Limiting
impact: LOW
impactDescription: Protect against abuse
tags: api, rate-limiting, security
---

## Implement Rate Limiting

Implement rate limiting to protect your API from abuse and ensure fair usage.

**Express/CRA Backend (before):**

```js
const rateLimit = require('express-rate-limit')

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per window
})

app.use('/api/', limiter)
```

**Next.js - Simple in-memory rate limiter:**

```tsx
// lib/rateLimit.ts
const rateLimitMap = new Map<string, { count: number; lastReset: number }>()

export function rateLimit(
  ip: string,
  limit: number = 10,
  windowMs: number = 60000
): { success: boolean; remaining: number } {
  const now = Date.now()
  const record = rateLimitMap.get(ip)

  if (!record || now - record.lastReset > windowMs) {
    rateLimitMap.set(ip, { count: 1, lastReset: now })
    return { success: true, remaining: limit - 1 }
  }

  if (record.count >= limit) {
    return { success: false, remaining: 0 }
  }

  record.count++
  return { success: true, remaining: limit - record.count }
}

// app/api/data/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { rateLimit } from '@/lib/rateLimit'

export async function GET(request: NextRequest) {
  const ip = request.ip || request.headers.get('x-forwarded-for') || 'unknown'
  const { success, remaining } = rateLimit(ip, 100, 60000)

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      {
        status: 429,
        headers: { 'X-RateLimit-Remaining': '0' },
      }
    )
  }

  const data = await fetchData()
  return NextResponse.json(data, {
    headers: { 'X-RateLimit-Remaining': String(remaining) },
  })
}
```

**Using Upstash for distributed rate limiting:**

```tsx
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
})

export async function GET(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1'
  const { success } = await ratelimit.limit(ip)

  if (!success) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 })
  }

  return NextResponse.json({ data: 'success' })
}
```
