---
title: Understand Build-Time vs Runtime Env Vars
impact: HIGH
impactDescription: Critical deployment concept
tags: environment, build-time, runtime, deployment
---

## Understand Build-Time vs Runtime Env Vars

Environment variables in Next.js are inlined at build time, not read at runtime by default.

**CRA Behavior:**

```tsx
// Variables are inlined during `npm run build`
const url = process.env.REACT_APP_API_URL
// After build: const url = "https://api.example.com"
```

**Next.js - Same behavior by default:**

```tsx
// NEXT_PUBLIC_ vars are inlined at build time
const url = process.env.NEXT_PUBLIC_API_URL
// After build, this becomes a string literal
```

**Implication for deployments:**

```bash
# Wrong expectation
NEXT_PUBLIC_API_URL=https://staging.api.com npm run build
# Deploy to staging...

NEXT_PUBLIC_API_URL=https://prod.api.com
# Deploy same build to prod - STILL uses staging URL!
```

**Solutions:**

**1. Build per environment:**
```bash
# Staging build
NEXT_PUBLIC_API_URL=https://staging.api.com npm run build
# Deploy to staging

# Production build (separate)
NEXT_PUBLIC_API_URL=https://prod.api.com npm run build
# Deploy to production
```

**2. Use server-side env vars:**
```tsx
// app/api/config/route.ts
export async function GET() {
  return Response.json({
    apiUrl: process.env.API_URL // Read at runtime on server
  })
}
```

**3. Use runtime configuration:**
```tsx
// next.config.js
module.exports = {
  publicRuntimeConfig: {
    apiUrl: process.env.API_URL,
  },
}
```

**Best practice:** Use server-side env vars for sensitive/dynamic values, `NEXT_PUBLIC_` only for truly static public values.

**Using .env files:**

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.com

# .env.staging (custom)
NEXT_PUBLIC_API_URL=https://staging-api.com

# Build with custom env
npx dotenv -e .env.staging -- next build
```

**CI/CD configuration:**

```yaml
# GitHub Actions example
jobs:
  build:
    steps:
      - name: Build
        env:
          NEXT_PUBLIC_API_URL: ${{ vars.API_URL }}
          NEXT_PUBLIC_GA_ID: ${{ vars.GA_ID }}
        run: npm run build
```
