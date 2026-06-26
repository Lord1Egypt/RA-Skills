---
title: Migrate Sentry Error Monitoring
impact: MEDIUM
impactDescription: Error tracking integration
tags: integrations, sentry, error-monitoring
---

## Migrate Sentry Error Monitoring

Replace `@sentry/browser` or `@sentry/react` with `@sentry/nextjs` for proper Next.js integration.

**CRA Pattern (before):**

```tsx
// src/index.tsx
import * as Sentry from '@sentry/react'

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
})
```

```tsx
// src/App.tsx
import * as Sentry from '@sentry/react'

function App() {
  return (
    <Sentry.ErrorBoundary fallback={<ErrorPage />}>
      <Router>...</Router>
    </Sentry.ErrorBoundary>
  )
}
```

**Next.js Pattern (after):**

**1. Install the Next.js SDK:**

```bash
npm remove @sentry/browser @sentry/react
npm install @sentry/nextjs
```

**2. Run the setup wizard (recommended):**

```bash
npx @sentry/wizard@latest -i nextjs
```

This creates the required configuration files automatically.

**3. Or configure manually:**

```ts
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,

  // Capture replay for errors
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})
```

```ts
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
})
```

```ts
// sentry.edge.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
})
```

**4. Update next.config.js:**

```js
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your existing config
}

module.exports = withSentryConfig(nextConfig, {
  // Sentry options
  silent: true,
  org: 'your-org',
  project: 'your-project',
})
```

**5. Add global error handler:**

```tsx
// app/global-error.tsx
'use client'

import * as Sentry from '@sentry/nextjs'
import { useEffect } from 'react'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    Sentry.captureException(error)
  }, [error])

  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

**Environment variables:**

```bash
# .env
NEXT_PUBLIC_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_AUTH_TOKEN=your-auth-token  # For source maps upload
```

**Key differences from CRA:**

| CRA (@sentry/react) | Next.js (@sentry/nextjs) |
|---------------------|--------------------------|
| Single client config | Separate client/server/edge configs |
| `REACT_APP_SENTRY_DSN` | `NEXT_PUBLIC_SENTRY_DSN` |
| ErrorBoundary wrapper | `global-error.tsx` + `error.tsx` |
| Client-only errors | Server + client errors captured |

**Disable Sentry in development/Docker:**

```bash
# Disable Sentry for local/Docker builds
NEXT_PUBLIC_SENTRY_DSN=
# or
NEXT_PUBLIC_DISABLE_SENTRY=true
```

```ts
// sentry.client.config.ts
if (process.env.NEXT_PUBLIC_DISABLE_SENTRY !== 'true') {
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    // ...
  })
}
```
