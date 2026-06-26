---
title: Handle WebSocket Optional Dependencies
impact: HIGH
impactDescription: socket.io and ws libraries have native deps that fail bundling
tags: gotchas, websocket, webpack, native-modules
---

## Handle WebSocket Optional Dependencies

When migrating CRA apps that use `socket.io-client` or `ws` for WebSocket connections, you may encounter bundling errors due to optional native dependencies.

**Error you'll see:**

```
Module not found: Can't resolve 'bufferutil'
Module not found: Can't resolve 'utf-8-validate'
```

These are optional native modules that provide performance optimizations for WebSocket connections. They're not required for functionality but cause build failures because webpack tries to resolve them.

**Solution: Configure webpack fallbacks in next.config.js**

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Handle optional WebSocket native dependencies (client-side only)
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        bufferutil: false,
        'utf-8-validate': false,
      }
    }
    return config
  },

  // Required for Next.js 16+ when using webpack config
  turbopack: {},
}

module.exports = nextConfig
```

The `isServer` check ensures the fallback is only applied to client-side bundles where it's needed. Server-side builds can use the native modules if available.

**Why this works:**

Setting fallbacks to `false` tells webpack to provide an empty module instead of trying to resolve the native dependency. Since these are optional performance optimizations, the application works correctly without them.

**Alternative: Install the native modules**

If you want the performance benefits and have a native build environment:

```bash
npm install bufferutil utf-8-validate
```

Note: This requires node-gyp and a C++ compiler, which can complicate CI/CD and Docker builds.

**Libraries that commonly need this fix:**

- `socket.io-client`
- `ws`
- `engine.io-client`
- Any library using `ws` internally

**Check if your project needs this:**

```bash
# Check for WebSocket libraries in dependencies
grep -E "(socket\.io|\"ws\")" package.json
```

See also: `setup-next-config` for the complete CRA migration config template.
