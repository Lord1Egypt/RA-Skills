---
title: Analyze Bundle Size
impact: MEDIUM
impactDescription: Identify large dependencies
tags: build, bundle, analysis, performance
---

## Analyze Bundle Size

Analyze your bundle to identify large dependencies and optimization opportunities.

**CRA bundle analysis:**

```bash
npm run build
# Uses source-map-explorer or similar
```

**Next.js bundle analysis:**

```bash
npm install -D @next/bundle-analyzer
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // your config
}

module.exports = withBundleAnalyzer(nextConfig)
```

```json
// package.json
{
  "scripts": {
    "analyze": "ANALYZE=true next build"
  }
}
```

```bash
# Run analysis
npm run analyze
# Opens browser with bundle visualization
```

**Reading the analysis:**
- **client.html** - Code sent to browser
- **server.html** - Server-side code
- Look for large chunks and duplicate dependencies

**Common issues and fixes:**

```tsx
// BAD: Importing entire library
import _ from 'lodash'
_.debounce(...)

// GOOD: Import specific function
import debounce from 'lodash/debounce'
debounce(...)
```

```tsx
// BAD: Static import of heavy component
import HeavyChart from './HeavyChart'

// GOOD: Dynamic import
import dynamic from 'next/dynamic'
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
})
```

**Build output size check:**

```bash
npm run build
# Check the size output
# First Load JS shared by all: 84 kB
# Keep shared JS under 100kB for good performance
```
