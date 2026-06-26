---
title: Change REACT_APP_ to NEXT_PUBLIC_
impact: CRITICAL
impactDescription: Required for client-side env vars
tags: environment, env-vars, configuration
---

## Change REACT_APP_ to NEXT_PUBLIC_

CRA uses `REACT_APP_` prefix for browser-exposed variables. Next.js uses `NEXT_PUBLIC_`.

**CRA Pattern (before):**

```bash
# .env
REACT_APP_API_URL=https://api.example.com
REACT_APP_GOOGLE_ANALYTICS_ID=UA-123456
REACT_APP_FEATURE_FLAG=true
```

```tsx
// src/api.ts
const apiUrl = process.env.REACT_APP_API_URL
```

**Next.js Pattern (after):**

```bash
# .env
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=UA-123456
NEXT_PUBLIC_FEATURE_FLAG=true
```

```tsx
// lib/api.ts
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

**Migration script:**

```bash
# Rename all REACT_APP_ to NEXT_PUBLIC_ in .env files
sed -i '' 's/REACT_APP_/NEXT_PUBLIC_/g' .env .env.local .env.development .env.production

# Find and replace in code
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" \) \
  -exec sed -i '' 's/REACT_APP_/NEXT_PUBLIC_/g' {} +
```

**Key differences:**

| CRA | Next.js | Exposed to Browser |
|-----|---------|-------------------|
| `REACT_APP_*` | `NEXT_PUBLIC_*` | Yes |
| Other vars | Other vars | No (server only) |

**Important:** Only variables starting with `NEXT_PUBLIC_` are exposed to the browser. All other variables are server-only for security.

**Discovery Strategy:**

Before migrating, find all environment variable references to ensure none are missed:

```bash
# Find all REACT_APP_ references in source files
grep -r "REACT_APP_" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/

# Find all REACT_APP_ references in env files
grep "REACT_APP_" .env* 2>/dev/null

# List unique environment variables used
grep -roh "REACT_APP_[A-Z_]*" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/ | sort -u
```

**Verification Checklist:**

After migration, verify all references are updated:

```bash
# Should return no results if migration is complete
grep -r "REACT_APP_" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" .

# Verify new variables are set
grep "NEXT_PUBLIC_" .env* 2>/dev/null
```

**Commonly Missed Locations:**

Don't forget to update environment variables in:

- `.env.example` or `.env.template` files
- CI/CD configuration (GitHub Actions, CircleCI, etc.)
- Docker files and docker-compose.yml
- Deployment platform settings (Vercel, Netlify, AWS)
- Documentation and README files
- Shell scripts that set environment variables
- Test configuration files (jest.config.js, cypress.config.js)
