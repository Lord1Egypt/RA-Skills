---
title: Understand .env File Loading Order
impact: MEDIUM
impactDescription: Different precedence than CRA
tags: environment, env-files, configuration
---

## Understand .env File Loading Order

Next.js loads environment files in a specific order, which differs slightly from CRA.

**CRA Loading Order:**

```
.env.local (highest priority)
.env.development / .env.production / .env.test
.env (lowest priority)
```

**Next.js Loading Order:**

```
process.env (highest - system/CLI vars)
.env.$(NODE_ENV).local (e.g., .env.development.local)
.env.local (NOT loaded in test environment)
.env.$(NODE_ENV) (e.g., .env.development)
.env (lowest priority)
```

**File purposes:**

| File | Committed | Purpose |
|------|-----------|---------|
| `.env` | Yes | Default values for all environments |
| `.env.local` | No | Local overrides (secrets) |
| `.env.development` | Yes | Development defaults |
| `.env.development.local` | No | Local dev overrides |
| `.env.production` | Yes | Production defaults |
| `.env.production.local` | No | Local prod testing |
| `.env.test` | Yes | Test environment |

**Example setup:**

```bash
# .env (committed)
NEXT_PUBLIC_APP_NAME=MyApp

# .env.local (NOT committed - add to .gitignore)
DATABASE_URL=postgres://localhost/mydb
API_SECRET=local_secret

# .env.production (committed)
NEXT_PUBLIC_API_URL=https://api.myapp.com

# .env.development (committed)
NEXT_PUBLIC_API_URL=http://localhost:3001
```

**Accessing in code:**

```tsx
// Same as CRA
const appName = process.env.NEXT_PUBLIC_APP_NAME
```
