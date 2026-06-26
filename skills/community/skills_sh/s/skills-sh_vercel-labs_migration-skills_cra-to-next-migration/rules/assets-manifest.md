---
title: Configure Web App Manifest
impact: LOW
impactDescription: PWA configuration
tags: assets, manifest, pwa
---

## Configure Web App Manifest

Next.js App Router can generate the web app manifest dynamically or use a static file.

**CRA Pattern (before):**

```json
// public/manifest.json
{
  "short_name": "My App",
  "name": "My Application",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

```html
<!-- public/index.html -->
<link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
```

**Next.js - Static file:**

```json
// public/manifest.json (same content)
```

```tsx
// app/layout.tsx
export const metadata = {
  manifest: '/manifest.json',
}
```

**Next.js - Dynamic generation (recommended):**

```tsx
// app/manifest.ts
import { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'My Application',
    short_name: 'My App',
    description: 'My awesome application',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  }
}
```

This generates `/manifest.webmanifest` automatically with proper headers.

## Full PWA Setup with next-pwa

For complete PWA functionality including service workers, offline support, and caching, use the `next-pwa` package.

**Installation:**

```bash
npm install next-pwa
```

**Configuration:**

```js
// next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Your other config options
}

module.exports = withPWA(nextConfig)
```

**TypeScript configuration:**

```ts
// next.config.ts
import type { NextConfig } from 'next'
import withPWAInit from 'next-pwa'

const withPWA = withPWAInit({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  register: true,
  skipWaiting: true,
})

const nextConfig: NextConfig = {
  // Your other config options
}

export default withPWA(nextConfig)
```

**Required manifest and icons:**

Ensure you have the manifest (via `app/manifest.ts` or `public/manifest.json`) and PWA icons in the `public/` directory:

```
public/
├── icon-192.png
├── icon-512.png
└── manifest.json (optional if using app/manifest.ts)
```

**CRA with vite-plugin-pwa migration:**

If migrating from CRA with `vite-plugin-pwa` or `workbox`:

| vite-plugin-pwa | next-pwa |
|-----------------|----------|
| `registerType: 'autoUpdate'` | `skipWaiting: true` |
| `devOptions.enabled` | `disable: process.env.NODE_ENV === 'development'` |
| Custom service worker in `src/` | Custom service worker via `sw` option |

**Verification:**

After building for production, verify PWA installation:
- Build: `npm run build && npm start`
- Open in Chrome, check DevTools > Application > Service Workers
- Test install prompt appears in browser
