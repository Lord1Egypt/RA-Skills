# Configuration Reference

Complete configuration guide for OpenNext on Cloudflare, including wrangler.jsonc, open-next.config.ts, environment variables, and TypeScript types.

## wrangler.jsonc Complete Template

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  
  // Worker identification
  "name": "my-nextjs-app",
  "main": ".open-next/worker.js",
  
  // Compatibility settings (REQUIRED)
  "compatibility_date": "2024-12-30",
  "compatibility_flags": [
    "nodejs_compat",                    // Required: Enable Node.js APIs
    "global_fetch_strictly_public"      // Security: Prevent fetching local IPs
  ],
  
  // Static assets (DO NOT CHANGE)
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS"
  },
  
  // Service bindings (REQUIRED)
  "services": [
    {
      "binding": "WORKER_SELF_REFERENCE",
      "service": "my-nextjs-app"        // Must match "name" above
    }
  ],
  
  // Environment variables
  "vars": {
    "ENVIRONMENT": "production",
    "CUSTOM_VAR": "value"
  },
  
  // KV Namespaces
  "kv_namespaces": [
    {
      "binding": "MY_KV",
      "id": "your-kv-namespace-id"
    }
  ],
  
  // R2 Buckets
  "r2_buckets": [
    {
      "binding": "NEXT_INC_CACHE_R2_BUCKET",
      "bucket_name": "my-next-cache"
    },
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-app-storage"
    }
  ],
  
  // D1 Databases
  "d1_databases": [
    {
      "binding": "NEXT_TAG_CACHE_D1",
      "database_name": "next-tag-cache",
      "database_id": "your-d1-database-id"
    },
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "your-db-id"
    }
  ],
  
  // Durable Objects
  "durable_objects": {
    "bindings": [
      {
        "name": "NEXT_CACHE_DO_QUEUE",
        "class_name": "DOQueueHandler"
      },
      {
        "name": "NEXT_TAG_CACHE_DO_SHARDED",
        "class_name": "DOShardedTagCache"
      },
      {
        "name": "NEXT_CACHE_DO_PURGE",
        "class_name": "BucketCachePurge"
      },
      {
        "name": "MY_DO",
        "class_name": "MyDurableObject"
      }
    ]
  },
  
  // Durable Object migrations
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": [
        "DOQueueHandler",
        "DOShardedTagCache",
        "BucketCachePurge",
        "MyDurableObject"
      ]
    }
  ],
  
  // AI Binding
  "ai": {
    "binding": "AI"
  },
  
  // Workers AI (legacy binding)
  // "workers_ai": {
  //   "binding": "AI"
  // },
  
  // Vectorize
  "vectorize": [
    {
      "binding": "VECTORIZE",
      "index_name": "my-index"
    }
  ],
  
  // Analytics Engine
  "analytics_engine_datasets": [
    {
      "binding": "ANALYTICS",
      "dataset": "my-dataset"
    }
  ],
  
  // Image optimization (Optional - incurs costs)
  "images": {
    "binding": "IMAGES"
  },
  
  // Hyperdrive
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "your-hyperdrive-id"
    }
  ],
  
  // Queues (producers)
  "queues": {
    "producers": [
      {
        "binding": "MY_QUEUE",
        "queue": "my-queue-name"
      }
    ]
  },
  
  // Browser Rendering
  "browser": {
    "binding": "BROWSER"
  },
  
  // Observability
  "observability": {
    "enabled": true,
    "head_sampling_rate": 1
  },
  
  // Cron triggers
  "triggers": {
    "crons": ["0 0 * * *"]  // Daily at midnight
  },
  
  // Routes (custom domains)
  "routes": [
    {
      "pattern": "example.com/*",
      "zone_name": "example.com"
    }
  ],
  
  // Environments
  "env": {
    "staging": {
      "name": "my-nextjs-app-staging",
      "vars": {
        "ENVIRONMENT": "staging"
      }
    },
    "production": {
      "name": "my-nextjs-app-production",
      "vars": {
        "ENVIRONMENT": "production"
      }
    }
  }
}
```

## Configuration Requirements

### Required Settings

These settings are **mandatory** for OpenNext to work:

```jsonc
{
  "compatibility_date": "2024-09-23",  // Or later
  "compatibility_flags": ["nodejs_compat"],
  "main": ".open-next/worker.js",
  "assets": {
    "directory": ".open-next/assets",
    "binding": "ASSETS"
  },
  "services": [
    {
      "binding": "WORKER_SELF_REFERENCE",
      "service": "my-nextjs-app"  // MUST match "name" field
    }
  ]
}
```

### Compatibility Flags

```jsonc
{
  "compatibility_flags": [
    // Required for Node.js APIs
    "nodejs_compat",
    
    // Security: Prevent fetching private IPs
    "global_fetch_strictly_public",
    
    // Optional: Enable FinalizationRegistry (date >= 2025-05-05)
    // (Enabled by default with recent compatibility dates)
  ]
}
```

**Critical**: `nodejs_compat` enables Node.js APIs like `Buffer`, `process`, `path`, etc. Without it, your app will fail.

### Caching Bindings

For ISR/SSG caching, add these bindings based on your cache strategy:

**R2 Incremental Cache**:

```jsonc
{
  "r2_buckets": [
    {
      "binding": "NEXT_INC_CACHE_R2_BUCKET",
      "bucket_name": "your-bucket-name"
    }
  ]
}
```

**DO Queue (for time-based revalidation)**:

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "NEXT_CACHE_DO_QUEUE",
        "class_name": "DOQueueHandler"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["DOQueueHandler"]
    }
  ]
}
```

**D1 Tag Cache (for on-demand revalidation)**:

```jsonc
{
  "d1_databases": [
    {
      "binding": "NEXT_TAG_CACHE_D1",
      "database_name": "next-tag-cache",
      "database_id": "your-database-id"
    }
  ]
}
```

**DO Sharded Tag Cache (for high-load on-demand revalidation)**:

```jsonc
{
  "durable_objects": {
    "bindings": [
      {
        "name": "NEXT_TAG_CACHE_DO_SHARDED",
        "class_name": "DOShardedTagCache"
      }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["DOShardedTagCache"]
    }
  ]
}
```

## open-next.config.ts

Configure OpenNext behavior and caching strategies:

### Basic Configuration

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";

export default defineCloudflareConfig({
  // Configuration options
});
```

### Static Site (SSG Only)

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});
```

### Small Site with ISR

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";
import d1NextTagCache from "@opennextjs/cloudflare/overrides/tag-cache/d1-next-tag-cache";

export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  queue: doQueue,
  tagCache: d1NextTagCache,
});
```

### Large Site with Regional Cache

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import { withRegionalCache } from "@opennextjs/cloudflare/overrides/incremental-cache/regional-cache";
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";
import doShardedTagCache from "@opennextjs/cloudflare/overrides/tag-cache/do-sharded-tag-cache";
import { purgeCache } from "@opennextjs/cloudflare/overrides/cache-purge/index";

export default defineCloudflareConfig({
  incrementalCache: withRegionalCache(r2IncrementalCache, {
    mode: "long-lived",
    bypassTagCacheOnCacheHit: true,
  }),
  queue: doQueue,
  tagCache: doShardedTagCache({ baseShardSize: 12 }),
  enableCacheInterception: true,
  cachePurge: purgeCache({ type: "direct" }),
});
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `incrementalCache` | Cache implementation | Storage for ISR/SSG pages |
| `queue` | Queue implementation | Time-based revalidation handler |
| `tagCache` | Tag cache implementation | On-demand revalidation storage |
| `enableCacheInterception` | boolean | Skip NextServer for cached routes (faster cold starts) |
| `cachePurge` | Cache purge implementation | Automatic cache invalidation |

## next.config.ts

### Basic Setup

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Your Next.js configuration options
  images: {
    // Image configuration
  },
  // ... other config
};

export default nextConfig;

// Initialize OpenNext for local development
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
initOpenNextCloudflareForDev();
```

### With Remote Bindings (wrangler < 4.36.0)

```typescript
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";

initOpenNextCloudflareForDev({
  experimental: {
    remoteBindings: true
  }
});
```

For wrangler >= 4.36.0, remote bindings are stable - just set `remote: true` in wrangler.jsonc.

### TypeScript Configuration

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // For Prisma with Cloudflare Workers
  serverExternalPackages: [
    "@prisma/client",
    ".prisma/client"
  ],
};

export default nextConfig;
```

## Environment Variables

### .dev.vars

Local development environment variables:

```bash
# .dev.vars
NEXTJS_ENV=development

# Database URLs
DATABASE_URL=postgresql://user:pass@localhost:5432/db
POSTGRES_URL=postgresql://user:pass@localhost:5432/db

# API Keys (for development only)
STRIPE_SECRET_KEY=sk_test_xxx
API_SECRET=dev-secret-xxx
```

**Important**: `.dev.vars` is used by `next dev` and `wrangler dev`. Add to `.gitignore`.

### NEXTJS_ENV Variable

Controls which Next.js `.env` file to load:

```bash
# .dev.vars
NEXTJS_ENV=development  # Loads .env.development
# or
NEXTJS_ENV=production   # Loads .env.production (default)
```

### Next.js .env Files

Standard Next.js environment file loading:

```bash
# .env.local (local development, not committed)
DATABASE_URL=postgresql://localhost:5432/dev

# .env.development (committed, dev defaults)
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# .env.production (committed, prod defaults)
NEXT_PUBLIC_API_URL=https://api.example.com

# .env (committed, shared defaults)
NEXT_PUBLIC_APP_NAME=My App
```

**Loading order** (with `NEXTJS_ENV=development`):
1. `.env.development.local`
2. `.env.local`
3. `.env.development`
4. `.env`

### Production Environment Variables

Set via Cloudflare dashboard or CLI:

```bash
# Via Wrangler
wrangler secret put API_SECRET
# Enter secret when prompted

# Via dashboard
# Workers & Pages > your-worker > Settings > Variables
```

**For Workers Builds** (CI/CD):
Set "Build variables and secrets" in dashboard for SSG builds.

### Environment Variable Access

```typescript
// Server-side only (not inlined)
const secret = process.env.API_SECRET;

// Public (inlined in client bundle)
const publicUrl = process.env.NEXT_PUBLIC_API_URL;
```

## Static Asset Caching

Configure caching headers for static assets:

### public/_headers

```
# Cache immutable static assets forever
/_next/static/*
  Cache-Control: public, max-age=31536000, immutable

# Cache public assets for 1 hour
/*
  Cache-Control: public, max-age=3600

# Cache fonts
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
```

This file is deployed with your app and configures Cloudflare's CDN caching.

### Why This Matters

- `/_next/static/*` files have content hashes and never change
- Without proper headers, browsers re-validate on every request
- `immutable` tells browsers to never revalidate

## TypeScript Types

### Generate Types for Bindings

```bash
# Generate cloudflare-env.d.ts with binding types
npx wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts
```

**package.json script**:

```json
{
  "scripts": {
    "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
  }
}
```

### Example Generated Types

```typescript
// cloudflare-env.d.ts
interface CloudflareEnv {
  MY_KV: KVNamespace;
  MY_BUCKET: R2Bucket;
  DB: D1Database;
  MY_DO: DurableObjectNamespace;
  AI: Ai;
  IMAGES: Fetcher;
  WORKER_SELF_REFERENCE: Fetcher;
  ASSETS: Fetcher;
  API_SECRET: string;
  ENVIRONMENT: string;
}
```

### Using in Code

```typescript
import { getCloudflareContext } from "@opennextjs/cloudflare";

export async function GET() {
  // TypeScript knows about all bindings
  const { env } = getCloudflareContext();
  
  // Auto-complete for env.MY_KV, env.DB, etc.
  const value = await env.MY_KV.get("key");
  
  return Response.json({ value });
}
```

## Custom Worker Entry Point

Override the generated worker.js with custom handlers:

```typescript
// custom-worker.ts
// @ts-ignore - .open-next/worker.js is generated at build time
import { default as handler } from "./.open-next/worker.js";

export default {
  fetch: handler.fetch,
  
  async scheduled(event: ScheduledEvent, env: CloudflareEnv, ctx: ExecutionContext) {
    // Custom cron job logic
    console.log("Cron triggered:", new Date(event.scheduledTime));
  },
  
  async queue(batch: MessageBatch, env: CloudflareEnv, ctx: ExecutionContext) {
    // Custom queue consumer
    for (const message of batch.messages) {
      console.log("Processing message:", message.body);
      message.ack();
    }
  }
} satisfies ExportedHandler<CloudflareEnv>;

// Re-export Durable Objects if using DO caching
// @ts-ignore
export { DOQueueHandler, DOShardedTagCache, BucketCachePurge } from "./.open-next/worker.js";
```

Update wrangler.jsonc:

```jsonc
{
  "main": "./custom-worker.ts"
}
```

## Environment-Specific Configuration

### Multiple Environments

```jsonc
{
  "name": "my-app",
  
  "env": {
    "staging": {
      "name": "my-app-staging",
      "vars": {
        "ENVIRONMENT": "staging"
      },
      "routes": [
        { "pattern": "staging.example.com/*", "zone_name": "example.com" }
      ],
      "d1_databases": [
        { "binding": "DB", "database_id": "staging-db-id" }
      ]
    },
    
    "production": {
      "name": "my-app-production",
      "vars": {
        "ENVIRONMENT": "production"
      },
      "routes": [
        { "pattern": "example.com/*", "zone_name": "example.com" }
      ],
      "d1_databases": [
        { "binding": "DB", "database_id": "prod-db-id" }
      ]
    }
  }
}
```

Deploy to specific environment:

```bash
npx opennextjs-cloudflare deploy --env staging
npx opennextjs-cloudflare deploy --env production
```

## Configuration Validation

### Check Configuration

```bash
# Validate wrangler.jsonc
npx wrangler deploy --dry-run

# Check bundle size before deploying
npx @opennextjs/cloudflare build
# Look at .open-next/worker.js size
```

### Common Validation Errors

**Missing nodejs_compat**:
```
Error: node:buffer is not available
```
Fix: Add `"nodejs_compat"` to `compatibility_flags`

**Wrong WORKER_SELF_REFERENCE**:
```
Error: Service binding 'WORKER_SELF_REFERENCE' not found
```
Fix: Ensure `service` matches `name` in wrangler.jsonc

**Old compatibility_date**:
```
Error: FinalizationRegistry is not defined
```
Fix: Update `compatibility_date` to `2025-05-05` or later

## Best Practices

1. **Use JSONC format** - Supports comments and JSON schema validation
2. **Enable observability** - Critical for debugging production issues
3. **Set head_sampling_rate: 1** - Full trace sampling during development
4. **Keep .open-next/ in .gitignore** - Don't commit build output
5. **Generate types after binding changes** - Run `cf-typegen` script
6. **Use environment variables for secrets** - Never hardcode in source
7. **Configure static asset caching** - Add `public/_headers` file
8. **Test with preview** - Use `npm run preview` before deploying
9. **Use wrangler >= 3.99.0** - Required for Next.js support
10. **Document custom bindings** - Comment your wrangler.jsonc

## Configuration Checklist

Starting a new OpenNext project? Ensure you have:

- [ ] `wrangler.jsonc` with `nodejs_compat` flag
- [ ] `compatibility_date` >= `2024-09-23`
- [ ] `WORKER_SELF_REFERENCE` service binding matches `name`
- [ ] `open-next.config.ts` with cache strategy
- [ ] `.dev.vars` with `NEXTJS_ENV=development`
- [ ] `next.config.ts` with `initOpenNextCloudflareForDev()`
- [ ] `public/_headers` for static asset caching
- [ ] `.gitignore` includes `.open-next/`
- [ ] `package.json` scripts for preview/deploy
- [ ] TypeScript types generated with `cf-typegen`

## Related Documentation

- [../SKILL.md](../SKILL.md) - Main OpenNext skill overview
- [caching.md](caching.md) - Complete caching configuration
- [database-orm.md](database-orm.md) - Database and ORM setup
- [troubleshooting.md](troubleshooting.md) - Common issues and fixes
