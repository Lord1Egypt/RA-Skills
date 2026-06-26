---
title: Update .gitignore for Next.js
impact: LOW
impactDescription: Prevents committing build artifacts
tags: setup, gitignore, git
---

## Update .gitignore for Next.js

CRA and Next.js have different build output directories that should be ignored.

**CRA .gitignore (before):**

```gitignore
# dependencies
/node_modules

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
```

**Next.js .gitignore (after):**

```gitignore
# dependencies
/node_modules

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
```

**Key additions:**
- `/.next/` - Next.js build output and cache
- `/out/` - Static export output
- `.vercel` - Vercel deployment cache
- `next-env.d.ts` - Auto-generated (optional to ignore)
