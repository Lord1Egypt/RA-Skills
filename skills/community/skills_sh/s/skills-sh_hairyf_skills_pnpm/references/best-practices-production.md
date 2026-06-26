---
name: pnpm-production-deployment
description: Production deployment with lockfile and offline install
---

# pnpm Production Deployment

## Recommended: Lockfile + Install

1. Commit `pnpm-lock.yaml`
2. In production: `pnpm install`

Versions stay consistent with development.

## Alternative: Lockfile + Store Copy

For environments without registry access:

1. Commit lockfile
2. Copy package store to production
3. Run `pnpm install --offline`

Use only when external registry is unavailable.

## Production Dependencies Only

```bash
pnpm install --prod
pnpm install -P
```

Skips `devDependencies`. Use in Docker final stage or server deploy.

<!--
Source references:
- https://pnpm.io/production
- https://pnpm.io/git
-->
