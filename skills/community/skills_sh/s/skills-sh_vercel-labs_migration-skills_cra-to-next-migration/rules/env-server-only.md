---
title: Use Non-Prefixed Vars for Server-Only
impact: HIGH
impactDescription: Keep secrets secure
tags: environment, env-vars, security, server
---

## Use Non-Prefixed Vars for Server-Only

Variables without `NEXT_PUBLIC_` prefix are only available on the server, keeping secrets secure.

**CRA Pattern (before):**

```bash
# .env - All accessible (but only REACT_APP_ in browser)
REACT_APP_API_URL=https://api.example.com
DATABASE_URL=postgres://...  # Not accessible in browser
API_SECRET=secret123         # Not accessible in browser
```

```tsx
// Had to use backend/API routes for secrets
// or risk exposing them in client bundle
```

**Next.js Pattern (after):**

```bash
# .env
# Browser-accessible (client + server)
NEXT_PUBLIC_API_URL=https://api.example.com

# Server-only (NEVER sent to browser)
DATABASE_URL=postgres://user:pass@localhost/db
API_SECRET=super_secret_key
STRIPE_SECRET_KEY=sk_live_xxx
```

```tsx
// app/api/checkout/route.ts
// Server-only - safe to use secrets
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!) // Safe!

export async function POST(request: Request) {
  // Direct access to secrets in Route Handlers
}
```

```tsx
// app/users/page.tsx (Server Component)
// Also safe - Server Components run on server
export default async function Users() {
  const users = await db.query({
    connectionString: process.env.DATABASE_URL // Safe!
  })
  return <UserList users={users} />
}
```

**Security benefit:**

```tsx
// Client Component - secrets NOT accessible
'use client'

export function ClientComponent() {
  // process.env.DATABASE_URL is undefined here
  // process.env.NEXT_PUBLIC_API_URL works
}
```
