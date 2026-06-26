---
title: Create and Configure next.config.js
impact: CRITICAL
impactDescription: Configures Next.js behavior
tags: setup, config, next-config
---

## Create and Configure next.config.js

CRA uses `react-scripts` with limited configuration (via `craco` or ejecting). Next.js uses `next.config.js` for all configuration.

**CRA Configuration (before):**

```js
// craco.config.js or ejected webpack.config.js
module.exports = {
  webpack: {
    alias: {
      '@': './src'
    }
  }
}
```

**Next.js Configuration (after):**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React Strict Mode (CRA default)
  reactStrictMode: true,

  // Configure image domains for next/image
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },

  // Redirects (replaces react-router redirects)
  async redirects() {
    return [
      {
        source: '/old-path',
        destination: '/new-path',
        permanent: true,
      },
    ]
  },

  // Environment variables exposed to browser
  env: {
    CUSTOM_VAR: process.env.CUSTOM_VAR,
  },
}

module.exports = nextConfig
```

**TypeScript Configuration (next.config.ts):**

```ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
}

export default nextConfig
```

Path aliases are configured in `tsconfig.json` instead of webpack config.

**Comprehensive CRA Migration Template:**

For CRA migrations, use this complete template that handles common compatibility issues:

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React Strict Mode (CRA default behavior)
  reactStrictMode: true,

  // Webpack customizations for CRA compatibility
  webpack: (config) => {
    // Handle WebSocket optional native dependencies (socket.io, ws)
    // See: gotchas-websocket-optional-deps
    config.resolve.fallback = {
      ...config.resolve.fallback,
      bufferutil: false,
      'utf-8-validate': false,
    }

    return config
  },

  // Required placeholder when using webpack config in Next.js 16+
  // See: gotchas-turbopack
  turbopack: {},

  // Configure remote image domains (add your domains)
  // See: images-remote-patterns
  images: {
    remotePatterns: [
      // Example:
      // {
      //   protocol: 'https',
      //   hostname: 'example.com',
      // },
    ],
  },
}

module.exports = nextConfig
```

**When to extend this template:**

- **SVG imports**: Add SVGR loader if using `import { ReactComponent } from './icon.svg'` - see `assets-static-imports`
- **SCSS :export**: May need `--webpack` flag for dev - see `gotchas-turbopack`
- **Remote images**: Add domains to `images.remotePatterns` - see `images-remote-patterns`
- **Redirects**: Add `redirects()` function for route redirects - see `routing-link-component`

## Monorepo: transpilePackages

For monorepos with workspace packages that need transpilation, use `transpilePackages`:

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Transpile workspace packages
  transpilePackages: [
    '@myorg/ui-components',
    '@myorg/shared-utils',
    '@myorg/design-system',
  ],
}

module.exports = nextConfig
```

**When to use transpilePackages:**

- Local workspace packages (yarn/npm/pnpm workspaces)
- Packages that ship untranspiled TypeScript or modern JS
- Packages using syntax not supported by your target browsers

**Auto-detection (Next.js 13.1+):**

Next.js automatically transpiles packages that have `"exports"` in their `package.json`. You only need `transpilePackages` for packages without proper exports configuration.

## Node.js Polyfills and Fallbacks

Some libraries have optional Node.js dependencies that fail in the browser. Configure webpack fallbacks:

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        // Disable Node.js modules not available in browser
        fs: false,
        net: false,
        tls: false,
        crypto: false,

        // Or provide browser-compatible polyfills
        path: require.resolve('path-browserify'),
        stream: require.resolve('stream-browserify'),
        buffer: require.resolve('buffer/'),
      }
    }
    return config
  },

  turbopack: {},
}

module.exports = nextConfig
```

**Install polyfills if needed:**

```bash
npm install path-browserify stream-browserify buffer
```

**Common libraries needing fallbacks:**

| Library | Fallbacks needed |
|---------|------------------|
| `socket.io-client`, `ws` | `bufferutil: false`, `utf-8-validate: false` |
| PDF libraries | `fs: false`, `path: 'path-browserify'` |
| Crypto libraries | `crypto: false` or `crypto-browserify` |
| Font processing (woff2) | `fs: false` |

See `gotchas-websocket-optional-deps` for WebSocket-specific configuration.
