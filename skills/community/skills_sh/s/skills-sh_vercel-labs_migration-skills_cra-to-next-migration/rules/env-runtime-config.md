---
title: Use Runtime Configuration When Needed
impact: MEDIUM
impactDescription: Dynamic environment values
tags: environment, runtime-config, configuration
---

## Use Runtime Configuration When Needed

For values that need to change without rebuilding, use runtime configuration instead of build-time env vars.

**CRA Pattern (before):**

```tsx
// All env vars are baked in at build time
const apiUrl = process.env.REACT_APP_API_URL
// Must rebuild to change
```

**Next.js - Build-time (default):**

```tsx
// next.config.js
module.exports = {
  env: {
    API_URL: process.env.API_URL, // Baked in at build
  },
}
```

**Next.js - Runtime configuration:**

```tsx
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Runtime env vars (server-side)
  serverRuntimeConfig: {
    apiSecret: process.env.API_SECRET,
  },
  // Runtime env vars (both server and client)
  publicRuntimeConfig: {
    apiUrl: process.env.API_URL,
  },
}

module.exports = nextConfig
```

```tsx
// Using runtime config
import getConfig from 'next/config'

const { serverRuntimeConfig, publicRuntimeConfig } = getConfig()

// Server-side only
const secret = serverRuntimeConfig.apiSecret

// Client and server
const apiUrl = publicRuntimeConfig.apiUrl
```

**Modern alternative - Edge Config (Vercel):**

```tsx
import { get } from '@vercel/edge-config'

export default async function Page() {
  const featureFlag = await get('newFeatureEnabled')
  // Can change without redeploy
}
```

**When to use runtime config:**
- Feature flags that change frequently
- Multi-tenant applications
- A/B testing configurations
- Environment-specific URLs that change between deploys
