---
title: Understand Build Output
impact: LOW
impactDescription: Different build structure
tags: build, output, deployment
---

## Understand Build Output

CRA and Next.js produce different build outputs with different deployment requirements.

**CRA build output:**

```
build/
├── static/
│   ├── css/
│   │   └── main.abc123.css
│   ├── js/
│   │   ├── main.abc123.js
│   │   └── runtime.abc123.js
│   └── media/
│       └── logo.abc123.png
├── index.html
├── asset-manifest.json
└── favicon.ico
```

- Static files only
- Deploy to any static host (S3, Netlify, Vercel)
- Single `index.html` for all routes

**Next.js build output:**

```
.next/
├── cache/           # Build cache
├── server/          # Server-side code
│   ├── app/
│   │   ├── page.js
│   │   └── api/
│   ├── chunks/
│   └── pages/
├── static/          # Static assets
│   ├── chunks/
│   └── css/
└── BUILD_ID

public/              # Copied as-is
```

- Server code + static assets
- Requires Node.js server (or serverless)
- Each route can be static or dynamic

**Checking build output:**

```bash
# Build and see output
npm run build

# Output shows:
# - Route types (Static/Dynamic)
# - Bundle sizes
# - Build time
```

**Build output information:**

```
Route (app)                    Size     First Load JS
┌ ○ /                         5.2 kB        89.1 kB
├ ○ /about                    1.3 kB        85.2 kB
├ λ /api/users                0 B                0 B
└ λ /blog/[slug]              2.1 kB        86.0 kB

○  (Static)   prerendered as static content
λ  (Dynamic)  server-rendered on demand
```
