---
title: Validate Required Environment Variables
impact: MEDIUM
impactDescription: Fail fast on missing config
tags: environment, validation, typescript
---

## Validate Required Environment Variables

Validate environment variables at build/startup time to catch configuration errors early.

**CRA Pattern (before):**

```tsx
// Often no validation - runtime errors
const apiUrl = process.env.REACT_APP_API_URL
// If undefined, might cause cryptic errors later
```

**Next.js Pattern (after):**

```tsx
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  API_SECRET: z.string().min(1),
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_APP_ENV: z.enum(['development', 'staging', 'production']),
})

// Validate at module load time
const env = envSchema.parse({
  DATABASE_URL: process.env.DATABASE_URL,
  API_SECRET: process.env.API_SECRET,
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  NEXT_PUBLIC_APP_ENV: process.env.NEXT_PUBLIC_APP_ENV,
})

export default env
```

**Using validated env:**

```tsx
// app/api/users/route.ts
import env from '@/lib/env'

export async function GET() {
  const db = connect(env.DATABASE_URL) // Type-safe!
}
```

**Type-safe without Zod:**

```tsx
// env.d.ts
declare namespace NodeJS {
  interface ProcessEnv {
    DATABASE_URL: string
    API_SECRET: string
    NEXT_PUBLIC_API_URL: string
  }
}

// lib/env.ts
function getEnvVar(key: string): string {
  const value = process.env[key]
  if (!value) {
    throw new Error(`Missing environment variable: ${key}`)
  }
  return value
}

export const env = {
  databaseUrl: getEnvVar('DATABASE_URL'),
  apiSecret: getEnvVar('API_SECRET'),
}
```

**Using @t3-oss/env-nextjs:**

```tsx
// env.mjs
import { createEnv } from '@t3-oss/env-nextjs'
import { z } from 'zod'

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
})
```
