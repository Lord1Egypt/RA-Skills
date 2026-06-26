---
name: vercel-config-analyzer
description: Analyze Vercel project configurations — audit vercel.json, framework detection, build settings, edge functions, headers, redirects, rewrites, environment variables, and deployment performance. Use when asked to review, debug, or optimize a Vercel deployment.
metadata:
  tags: ["vercel", "deployment", "serverless", "edge", "next.js", "frontend"]
---

# Vercel Config Analyzer

Analyze Vercel project configurations for correctness, performance, and security. Examines `vercel.json`, framework settings, build configuration, edge functions, middleware, headers, redirects, environment variables, and deployment patterns. Finds misconfigurations before they cause production incidents.

Use when: "review our Vercel config", "why is our Vercel deployment slow", "check vercel.json", "optimize our edge functions", "fix Vercel build errors", "audit our headers and redirects", or when deploying a new project to Vercel.

## Analysis Steps

### 1. Inventory Project Configuration

Locate and read all Vercel-relevant files:
- `vercel.json` — primary configuration
- Framework config: `next.config.js`, `nuxt.config.ts`, `svelte.config.js`, `astro.config.mjs`, etc.
- `package.json` — build commands and framework detection
- `.env*` files — check existence, not content
- `middleware.ts` / `middleware.js` — edge middleware
- `api/` / `pages/api/` / `app/api/` — serverless and edge functions (search for `export const runtime`)

### 2. Analyze vercel.json

Check each section of `vercel.json` for correctness:

**Build Configuration:**
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm ci",
  "framework": "nextjs"
}
```

**Common issues:**
- `buildCommand` not matching `package.json` scripts
- `outputDirectory` wrong for the framework (Next.js: `.next`, Vite: `dist`, CRA: `build`)
- Missing `framework` field causing incorrect auto-detection
- Using `npm install` instead of `npm ci` (non-deterministic builds)

**Framework detection matrix:**

| Framework | Expected Output Dir | Auto-Detected | Build Command |
|-----------|-------------------|---------------|---------------|
| Next.js | `.next` | Yes | `next build` |
| Vite | `dist` | Yes | `vite build` |
| Create React App | `build` | Yes | `react-scripts build` |
| Nuxt | `.output` | Yes | `nuxt build` |
| SvelteKit | `.svelte-kit` | Yes | `vite build` |
| Astro | `dist` | Yes | `astro build` |
| Remix | `build` | Yes | `remix build` |
| Plain HTML | `public` or `.` | No | None |

### 3. Audit Headers Configuration

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    }
  ]
}
```

**Security headers checklist:**

| Header | Required | Purpose | Recommended Value |
|--------|----------|---------|-------------------|
| `Strict-Transport-Security` | Critical | Force HTTPS | `max-age=63072000; includeSubDomains; preload` |
| `X-Content-Type-Options` | Critical | Prevent MIME sniffing | `nosniff` |
| `X-Frame-Options` | High | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| `Content-Security-Policy` | High | Prevent XSS/injection | Application-specific |
| `Referrer-Policy` | Medium | Control referrer info | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Medium | Restrict browser features | Deny unused features |
| `X-XSS-Protection` | Low | Legacy XSS filter | `0` (or omit; CSP replaces this) |

**Cache strategy recommendations:**

| Resource Type | Cache-Control | Why |
|--------------|---------------|-----|
| Hashed assets (JS/CSS) | `public, max-age=31536000, immutable` | Content-addressed, never changes |
| Images/fonts | `public, max-age=86400, stale-while-revalidate=604800` | Changes rarely |
| HTML pages | `public, max-age=0, must-revalidate` | Should always check for updates |
| API responses | `no-store` or `private, max-age=60` | Depends on data freshness needs |
| User-specific data | `private, no-store` | Must never be cached in shared caches |

### 4. Analyze Redirects and Rewrites

**Redirect issues to check:**
- Using `permanent: true` (301) for temporary moves — browsers cache 301s aggressively, very hard to undo
- Redirect chains (A->B->C) — merge into A->C
- Missing trailing slash consistency (`/about` vs `/about/`)
- Manual HTTP->HTTPS redirect — Vercel handles this automatically

**Rewrite issues to check:**
- External API rewrites without `has` conditions — creates an open proxy
- SPA catch-all (`/:path* -> /index.html`) not placed LAST — overrides API routes
- External rewrite targets not using HTTPS
- Conflicting rewrites — first match wins, order matters

### 5. Evaluate Serverless and Edge Functions

Functions can be configured in `vercel.json` (per-file `memory`, `maxDuration`, `runtime`) or inline with `export const runtime = 'edge'` and `export const maxDuration = 30`.

**Function optimization checklist:**
- **Cold starts:** Lazy-load heavy dependencies, reduce bundle size (1-5s savings)
- **Memory:** Default 1024MB is overkill for simple handlers — set 128-256MB
- **Duration:** Set explicit `maxDuration` for long operations (default: 10s Hobby / 60s Pro)
- **Runtime choice:** Use edge for auth/geo/A/B tests, serverless for DB queries and file processing
- **Static generation:** If an API route returns the same data for all users, use ISR instead

**Edge vs Serverless decision matrix:**

| Use Case | Recommended Runtime | Why |
|----------|-------------------|-----|
| Authentication/authorization | Edge | Low latency, runs before page loads |
| Geolocation-based routing | Edge | Access to `request.geo` |
| A/B testing | Edge | Modify response before it reaches client |
| Feature flags | Edge | Fast, runs at the edge |
| Database queries | Serverless (Node.js) | Most DB drivers need Node.js APIs |
| File processing | Serverless (Node.js) | Needs Node.js fs/stream APIs |
| Heavy computation | Serverless (Node.js) | Edge has CPU time limits |
| External API proxy | Either | Edge if latency-sensitive |

### 6. Check Environment Variables

Search code for `process.env.*` and client-exposed prefixes. Key audit checks:

- **API keys/DB URLs in client-exposed vars** (Critical) — move to server-side, proxy through API route
- **Missing variables in production** — verify all required vars in Vercel dashboard
- **Different values across environments** — audit Preview vs Production values
- **Hardcoded secrets in code** — move to environment variables immediately
- **Missing `VERCEL_URL` usage** — use for dynamic base URL on preview deployments

**Framework-specific variable exposure:**

| Framework | Client-Exposed Prefix | Server-Only |
|-----------|----------------------|-------------|
| Next.js | `NEXT_PUBLIC_*` | Everything else |
| Vite | `VITE_*` | Everything else |
| Create React App | `REACT_APP_*` | Everything else |
| Nuxt | `NUXT_PUBLIC_*` | `NUXT_*` (server) |
| SvelteKit | `PUBLIC_*` | Everything else |
| Astro | `PUBLIC_*` | Everything else |

### 7. Analyze Build Performance

**Common build time culprits and fixes:**

| Culprit | Time Cost | Fix |
|---------|----------|-----|
| `npm install` | 30-120s | Use `npm ci`, enable Vercel dependency cache |
| TypeScript compilation | 15-60s | Use SWC (Next.js default), check tsconfig strictness |
| Static page generation | Varies | Reduce build-time pages, use ISR for long-tail |
| Image optimization | 10-60s | Use external image CDN |
| Linting/testing in build | 30-120s | Move to CI (GitHub Actions), don't block deploy |

Check build output size with `du -sh .next/ dist/ build/` and analyze `build-manifest.json` for oversized pages.

### 8. Review Middleware

**Middleware audit checklist:**
- [ ] Matcher excludes `_next/static`, `_next/image`, and `favicon.ico`
- [ ] No database or heavy API calls (runs on EVERY request)
- [ ] Error handling prevents middleware crash from taking down the site
- [ ] Body under 1MB (edge runtime limit)
- [ ] No Node.js-specific APIs (middleware runs on edge by default)
- [ ] Cookies set with proper `SameSite`, `Secure`, and `HttpOnly` flags

### 9. Deployment Checklist

- [ ] Production domain has correct DNS (CNAME to `cname.vercel-dns.com`)
- [ ] Preview deployments are protected (password or Vercel Authentication)
- [ ] Build caching enabled (40-60% faster repeated deploys)
- [ ] Skew protection enabled for Next.js (prevents version mismatch during deploy)
- [ ] Speed Insights or Web Analytics enabled for production

## Output Format

```markdown
# Vercel Configuration Analysis

## Project Overview
- **Framework:** {detected framework}
- **Runtime:** {Edge / Serverless / Static}
- **Build Command:** {command}
- **Output Directory:** {path}

## Findings

### Critical
- {Security or correctness issue that will cause production problems}

### Warnings
- {Performance or best-practice issue}

### Recommendations
- {Optimization opportunities}

## Security Headers
- {Present: list}
- {Missing: list with recommended values}

## Environment Variables
- {Count of server-only vars}
- {Count of client-exposed vars}
- {Any sensitive vars exposed to client}

## Performance
- {Build time analysis}
- {Bundle size concerns}
- {Caching recommendations}

## Suggested vercel.json
{Optimized configuration}
```

## Tips

- Always check if `vercel.json` settings conflict with framework config (e.g., `next.config.js` headers override `vercel.json` headers in Next.js)
- Preview deployments use the `preview` environment — verify env vars are set for preview, not just production
- Vercel's edge network caches static assets automatically — don't add redundant CDN layers
- Use `vercel env pull` locally to sync environment variables for local development
- For monorepos, set `Root Directory` in project settings and use `ignoreCommand` to skip unchanged projects
- ISR pages re-generate on the first request after `revalidate` — the stale page is served while regenerating (stale-while-revalidate pattern)
- Edge middleware adds ~1-5ms to every matched request — keep it lean
- Use `vercel build` locally to test the exact build process Vercel will run
- Check Vercel's function logs (`vercel logs`) for runtime errors that don't appear in build output
- Protect preview URLs from search engine indexing with `X-Robots-Tag: noindex` header on non-production deployments
