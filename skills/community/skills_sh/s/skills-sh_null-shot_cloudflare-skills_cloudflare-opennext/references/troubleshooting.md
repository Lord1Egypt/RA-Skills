# Troubleshooting Reference

Common issues, errors, and solutions when deploying Next.js to Cloudflare Workers with OpenNext.

## Worker Size Limits

### Error: "Your Worker exceeded the size limit"

**Free Plan**: 3 MiB compressed
**Paid Plan**: 10 MiB compressed

When deploying, Wrangler shows both original and compressed sizes:

```
Total Upload: 13833.20 KiB / gzip: 2295.89 KiB
```

Only the **compressed (gzip)** size matters for the limit.

### Solution 1: Analyze Bundle Size

Use the ESBuild Bundle Analyzer to identify large dependencies:

```bash
# 1. Build your app
npx @opennextjs/cloudflare build

# 2. Navigate to server function directory
cd .open-next/server-functions/default

# 3. Find the meta.json file
ls -la | grep meta.json

# 4. Visit ESBuild Bundle Analyzer
# https://esbuild.github.io/analyze/

# 5. Upload handler.mjs.meta.json
```

The analyzer shows:
- Which packages are largest
- Duplicate dependencies
- Unnecessary code in bundle

### Solution 2: Optimize Dependencies

**Remove unused dependencies**:

```json
// package.json - audit and remove unused packages
{
  "dependencies": {
    // Only include what you actually use
  }
}
```

**Use lighter alternatives**:

| Heavy Package | Lighter Alternative |
|--------------|---------------------|
| `moment` | `date-fns` or native `Intl` |
| `lodash` | `lodash-es` with tree-shaking or native methods |
| `axios` | Native `fetch` |
| Large UI libraries | Only import what you need |

**Tree-shake properly**:

```typescript
// ❌ Imports entire library
import _ from "lodash";

// ✅ Import only what you need
import debounce from "lodash/debounce";
```

### Solution 3: Code Splitting

Use Next.js dynamic imports for client components:

```typescript
// Heavy component loaded only when needed
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <p>Loading chart...</p>,
  ssr: false,  // Don't include in server bundle
});
```

### Solution 4: External Packages

Externalize large packages if they're not needed at runtime:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  serverExternalPackages: [
    "@prisma/client",
    "large-package"
  ],
};
```

## Compatibility Errors

### Error: "node:buffer is not available"

**Cause**: Missing `nodejs_compat` compatibility flag.

**Fix**: Add to wrangler.jsonc:

```jsonc
{
  "compatibility_flags": ["nodejs_compat"],
  "compatibility_date": "2024-09-23"  // Or later
}
```

**Why needed**: Enables Node.js APIs like `Buffer`, `process`, `path`, etc.

### Error: "FinalizationRegistry is not defined"

**Cause**: Old compatibility date.

**Fix**: Update compatibility date:

```jsonc
{
  "compatibility_date": "2025-05-05"  // Or later
}
```

**Why**: `FinalizationRegistry` was added in newer Workers runtime versions.

### Error: "global_fetch_strictly_public"

Not an error, but a recommended security flag:

```jsonc
{
  "compatibility_flags": [
    "nodejs_compat",
    "global_fetch_strictly_public"  // Prevents fetching local IPs
  ]
}
```

## Build Errors

### Error: "Failed to load chunk server/chunks/ssr/..."

**Cause**: Using Turbopack build which is not supported.

**Fix**: Use standard Next.js build:

```json
// package.json
{
  "scripts": {
    "build": "next build"  // NOT "next build --turbo"
  }
}
```

**Why**: OpenNext doesn't support Turbopack's output format yet.

### Error: "Could not resolve '<package>'"

**Cause**: Package has workerd-specific code or export conditions.

**Fix**: Configure Wrangler build conditions:

```bash
# .env (at project root)
WRANGLER_BUILD_CONDITIONS=""
WRANGLER_BUILD_PLATFORM="node"
```

This tells Wrangler to use `node` exports instead of `browser` or `default`.

**Common packages needing this**:
- Some database drivers
- Packages with `exports` field using specific conditions

### Error: "Service binding 'WORKER_SELF_REFERENCE' not found"

**Cause**: Service binding name doesn't match worker name.

**Fix**: Ensure they match in wrangler.jsonc:

```jsonc
{
  "name": "my-app",  // Worker name
  "services": [
    {
      "binding": "WORKER_SELF_REFERENCE",
      "service": "my-app"  // Must match "name" above
    }
  ]
}
```

## Runtime Errors

### Error: "Cannot perform I/O on behalf of a different request"

**Cause**: Global database client reusing connections across requests.

**Fix**: Create client per-request with `maxUses: 1`:

```typescript
// ❌ WRONG - Global client
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const getDb = () => {
  return drizzle({ client: pool });
};

// ✅ CORRECT - Per-request client
import { cache } from "react";
import { Pool } from "pg";

export const getDb = cache(() => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    maxUses: 1,  // CRITICAL: Don't reuse connections
  });
  return drizzle({ client: pool });
});
```

**Why**: Workers have strict request isolation. Database connections cannot be shared across requests.

**Affected packages**:
- `pg` (PostgreSQL)
- `mysql2`
- Any package using persistent connections

See [database-orm.md](database-orm.md) for complete patterns.

### Error: "Module not found: @cloudflare/next-on-pages"

**Cause**: Mixing `@cloudflare/next-on-pages` with `@opennextjs/cloudflare`.

**Fix**: Remove `@cloudflare/next-on-pages`:

```bash
npm uninstall @cloudflare/next-on-pages
npm uninstall eslint-plugin-next-on-pages
```

Update imports:

```typescript
// ❌ Old
import { getRequestContext } from "@cloudflare/next-on-pages";

// ✅ New
import { getCloudflareContext } from "@opennextjs/cloudflare";
```

Remove from next.config.ts:

```typescript
// ❌ Remove this
import { setupDevPlatform } from "@cloudflare/next-on-pages/next-dev";
setupDevPlatform();

// ✅ Use this instead
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

### Error: "getCloudflareContext is not a function"

**Cause**: Not initializing OpenNext in next.config.ts.

**Fix**: Add to next.config.ts:

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Your config
};

export default nextConfig;

// Add this
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

**Why**: Enables bindings access during `next dev`.

## Deployment Errors

### Error: "Failed to publish"

**Cause**: Various deployment issues.

**Diagnosis**:

```bash
# Check deployment logs
wrangler tail

# Try dry-run
wrangler deploy --dry-run

# Check configuration
wrangler whoami
```

**Common fixes**:
- Ensure you're logged in: `wrangler login`
- Check account ID and zone settings
- Verify bindings exist (KV, R2, D1, etc.)

### Error: "Binding '<NAME>' not found"

**Cause**: Binding configured in wrangler.jsonc but not created in Cloudflare.

**Fix**: Create the binding:

```bash
# KV
wrangler kv namespace create MY_KV

# R2
wrangler r2 bucket create my-bucket

# D1
wrangler d1 create my-database

# Durable Objects - automatically created
```

Then add binding ID to wrangler.jsonc.

### Error: "Asset not found: .open-next/assets"

**Cause**: Build output missing or corrupted.

**Fix**: Rebuild:

```bash
# Clean and rebuild
rm -rf .open-next .next
npx @opennextjs/cloudflare build
```

**Why**: The `.open-next/` directory is generated during build. Never commit it.

## Caching Issues

### Pages Not Revalidating

**Symptom**: ISR pages never update, even after revalidation time.

**Diagnosis**: Enable debug mode:

```bash
# .env
NEXT_PRIVATE_DEBUG_CACHE=1
```

Check logs for cache operations.

**Common causes**:

1. **Queue not configured**:

```typescript
// open-next.config.ts - Missing queue
export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  // queue: doQueue,  // Missing!
});
```

Fix: Add queue configuration.

2. **R2 bucket empty**:

```bash
# Check if cache was populated
wrangler r2 object list my-next-cache

# Repopulate
npx opennextjs-cloudflare populateCache remote
```

3. **DO Queue not working**:

Check Durable Objects in dashboard. Ensure migration was applied:

```jsonc
{
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["DOQueueHandler"] }
  ]
}
```

### revalidateTag/revalidatePath Not Working

**Symptom**: Calling `revalidateTag()` doesn't invalidate cache.

**Diagnosis**:

1. **Tag cache not configured**:

```typescript
// Missing tagCache
export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  queue: doQueue,
  // tagCache: d1NextTagCache,  // Missing!
});
```

2. **D1 table not created**:

```bash
wrangler d1 execute NEXT_TAG_CACHE_D1 --command "
CREATE TABLE IF NOT EXISTS revalidations (
  tag TEXT PRIMARY KEY,
  revalidated_at INTEGER NOT NULL
)
"
```

3. **Cache purge not working** (with regional cache):

Add cache purge configuration and secrets:

```bash
wrangler secret put CACHE_PURGE_API_TOKEN
wrangler secret put CACHE_PURGE_ZONE_ID
```

See [caching.md](caching.md) for complete setup.

## Environment Variable Issues

### process.env Variables Undefined

**Symptom**: `process.env.MY_VAR` is undefined in production.

**Causes and fixes**:

1. **Not set in dashboard**:

```bash
# Set via Wrangler
wrangler secret put MY_SECRET

# Or in dashboard
# Workers & Pages > your-worker > Settings > Variables
```

2. **Using wrong environment**:

```bash
# Deploy to specific environment
npx opennextjs-cloudflare deploy --env production
```

3. **NEXT_PUBLIC_ variables not inlined**:

`NEXT_PUBLIC_` variables are inlined during build. Set them:
- As "Build variables" in Workers Builds
- In `.env` files for local builds

### NEXTJS_ENV Not Working

**Symptom**: Wrong `.env` file loaded during `next dev`.

**Fix**: Set in `.dev.vars`:

```bash
# .dev.vars
NEXTJS_ENV=development
```

**Not** in `.env` files. Wrangler reads `.dev.vars`.

## Image Optimization Issues

### Images Not Optimizing

**Symptom**: Images served without optimization.

**Diagnosis**:

1. **IMAGES binding missing**:

```jsonc
// wrangler.jsonc
{
  "images": {
    "binding": "IMAGES"  // Required for optimization
  }
}
```

2. **Using unsupported format**:

Supported: PNG, JPEG, WEBP, AVIF, GIF, SVG
Unsupported: BMP, TIFF, etc.

3. **Image domain not allowed**:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "example.com",
      }
    ],
  },
};
```

### Image Optimization Costs High

Cloudflare Images has usage-based pricing:
- $5/month per 100,000 images
- $1 per 1,000 image transformations

**Alternatives**:

1. **Custom loader**: Use Cloudflare Images via custom loader (no binding)
2. **Disable optimization**: Use unoptimized images
3. **Optimize at build time**: Generate multiple sizes during build

## Known Issues

### Durable Objects Warning During Build

**Warning**:

```
[WARNING] You have defined bindings to the following internal Durable Objects:
- {"name":"NEXT_CACHE_DO_QUEUE","class_name":"DOQueueHandler"}
These will not work in local development, but they should work in production.
```

**Status**: Harmless warning. Durable Objects for caching work fine in production.

**Why**: Caching DOs are not used during the build process itself.

### Node Middleware Not Supported (Next.js 15.2+)

**Feature**: Next.js 15.2 introduced Node Middleware.

**Status**: Not yet supported by OpenNext.

**Workaround**: Use standard Next.js middleware (without Node Middleware features).

### PPR with Cache Interception

**Feature**: Partial Prerendering (PPR)

**Issue**: Cache interception doesn't work with PPR.

**Fix**: Disable cache interception if using PPR:

```typescript
export default defineCloudflareConfig({
  enableCacheInterception: false,  // Required for PPR
});
```

## Debugging Strategies

### Enable Verbose Logging

```jsonc
// wrangler.jsonc
{
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1  // 100% sampling
  }
}
```

View logs:

```bash
wrangler tail
```

### Check Bundle Contents

```bash
# After build, inspect generated worker
cat .open-next/worker.js | grep "import"

# Check asset directory
ls -lah .open-next/assets
```

### Test Locally with Preview

```bash
# Build and preview locally
npm run preview

# Access in browser
# http://localhost:8787
```

Closer to production than `next dev`.

### Use Remote Bindings for Development

```jsonc
// wrangler.jsonc
{
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-bucket",
      "remote": true  // Use remote bucket in dev
    }
  ]
}
```

For wrangler >= 4.36.0. Earlier versions need:

```typescript
// next.config.ts
initOpenNextCloudflareForDev({
  experimental: { remoteBindings: true }
});
```

### Inspect Cache State

```bash
# Check R2 cache
wrangler r2 object list NEXT_INC_CACHE_R2_BUCKET

# Check D1 tag cache
wrangler d1 execute NEXT_TAG_CACHE_D1 --command "SELECT * FROM revalidations"

# Check KV cache
wrangler kv key list --namespace-id=<your-kv-id>
```

## Performance Issues

### Slow Cold Starts

**Causes**:

1. **Large bundle size**: See "Worker Size Limits" above
2. **Heavy global initialization**:

```typescript
// ❌ Bad - runs on every cold start
const heavyObject = performExpensiveSetup();

export default {
  async fetch() { /* ... */ }
};

// ✅ Good - lazy initialization
let heavyObject: HeavyType | null = null;

export default {
  async fetch() {
    if (!heavyObject) {
      heavyObject = performExpensiveSetup();
    }
    // ...
  }
};
```

3. **Not using cache interception**:

```typescript
export default defineCloudflareConfig({
  enableCacheInterception: true,  // Skip NextServer for cached routes
});
```

### Slow Database Queries

**Causes**:

1. **Not using Hyperdrive for PostgreSQL**:

Direct connections are slow from Workers. Use Hyperdrive:

```bash
wrangler hyperdrive create my-db \
  --connection-string="postgresql://..."
```

2. **Missing indexes**:

```sql
-- Add indexes for common queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

3. **N+1 queries**:

```typescript
// ❌ Bad - N+1 query
const users = await db.select().from(usersTable);
for (const user of users) {
  const posts = await db.select().from(postsTable)
    .where(eq(postsTable.userId, user.id));
}

// ✅ Good - single join
const usersWithPosts = await db
  .select()
  .from(usersTable)
  .leftJoin(postsTable, eq(usersTable.id, postsTable.userId));
```

## Getting Help

If you can't resolve an issue:

1. **Check OpenNext documentation**: https://opennext.js.org/cloudflare
2. **Search GitHub issues**: https://github.com/opennextjs/opennextjs-cloudflare/issues
3. **Cloudflare Discord**: https://discord.gg/cloudflaredev
4. **Open an issue**: Include:
   - Next.js version
   - `@opennextjs/cloudflare` version
   - wrangler.jsonc (redacted)
   - Error messages and logs
   - Steps to reproduce

## Quick Fixes Checklist

Before asking for help, try:

- [ ] `rm -rf .next .open-next && npm run build`
- [ ] Update dependencies: `npm update`
- [ ] Check wrangler.jsonc has `nodejs_compat`
- [ ] Verify `compatibility_date` >= `2024-09-23`
- [ ] Ensure `WORKER_SELF_REFERENCE` matches `name`
- [ ] Check bindings exist in Cloudflare dashboard
- [ ] Try `npm run preview` instead of `next dev`
- [ ] Enable debug logging: `NEXT_PRIVATE_DEBUG_CACHE=1`
- [ ] Check wrangler version: `npx wrangler --version` (need >= 3.99.0)
- [ ] Verify Node.js version: `node --version` (need >= 18)

## Related Documentation

- [../SKILL.md](../SKILL.md) - Main OpenNext skill overview
- [configuration.md](configuration.md) - Complete configuration guide
- [caching.md](caching.md) - ISR, SSG, and cache setup
- [database-orm.md](database-orm.md) - Database and ORM patterns
