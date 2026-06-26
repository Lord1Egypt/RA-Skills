---
title: Update Build Scripts
impact: MEDIUM
impactDescription: Different build commands
tags: build, scripts, npm
---

## Update Build Scripts

Replace CRA's react-scripts with Next.js build commands.

**CRA package.json (before):**

```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

**Next.js package.json (after):**

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch"
  }
}
```

**Script mapping:**

| CRA | Next.js | Purpose |
|-----|---------|---------|
| `npm start` | `npm run dev` | Development server |
| `npm run build` | `npm run build` | Production build |
| (N/A) | `npm start` | Production server |
| `npm test` | `npm test` | Run tests |
| `npm run eject` | (N/A) | Not needed |

**Additional useful scripts:**

```json
{
  "scripts": {
    "dev": "next dev",
    "dev:turbo": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:ci": "jest --ci",
    "e2e": "playwright test",
    "analyze": "ANALYZE=true next build"
  }
}
```

**Environment-specific builds:**

```json
{
  "scripts": {
    "build:staging": "NEXT_PUBLIC_ENV=staging next build",
    "build:prod": "NEXT_PUBLIC_ENV=production next build"
  }
}
```

## Next.js 16+ Turbopack Default

Next.js 16 and later use Turbopack as the default bundler for development. This improves dev server startup and refresh times but may cause issues with some webpack-specific features.

**If you encounter Turbopack compatibility issues:**

```json
{
  "scripts": {
    "dev": "next dev --webpack",
    "dev:turbo": "next dev",
    "build": "next build"
  }
}
```

Common features that require `--webpack` flag:
- SCSS `:export` syntax for sharing variables with JavaScript
- Custom webpack loaders
- Some webpack plugins

Note: The build command always uses webpack, so `--webpack` only affects development.

## Build Output Directory Mapping

CRA and Next.js use different output directory structures. Update any custom scripts that reference build paths.

**Directory mapping:**

| Purpose | CRA Path | Next.js Path |
|---------|----------|--------------|
| Production build | `build/` | `.next/` |
| Static assets | `build/static/` | `.next/static/` |
| Public files | `public/` (copied to `build/`) | `public/` (served directly) |
| Generated HTML | `build/index.html` | `.next/server/app/` |
| Static export | N/A | `out/` |

**Update custom build scripts:**

```bash
# CRA (before)
cp -r build/static/* /deploy/assets/
aws s3 sync build/ s3://bucket/

# Next.js (after)
cp -r .next/static/* /deploy/assets/
aws s3 sync out/ s3://bucket/  # For static export
```

**If you have post-build scripts that reference `build/`:**

```json
{
  "scripts": {
    "build": "next build",
    "postbuild": "node scripts/post-build.js"
  }
}
```

Update the script to use `.next/` or `out/` (for static export) instead of `build/`.
