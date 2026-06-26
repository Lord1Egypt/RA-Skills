# Caching Reference

Complete guide to Next.js caching on Cloudflare Workers with OpenNext, including ISR, SSG, incremental cache, queues, tag cache, and cache purge configuration.

## Overview

Next.js caching on Cloudflare involves three components:

1. **Incremental Cache** - Stores cached page data and fetch responses
2. **Queue** - Handles time-based revalidation (ISR)
3. **Tag Cache** - Enables on-demand revalidation (revalidateTag/revalidatePath)

## Caching Strategies by Use Case

### Static Site (SSG Only)

No revalidation, all content generated at build time:

```typescript
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});
```

**No additional bindings needed** in wrangler.jsonc.

### Small Site with ISR

Use R2 for cache storage, DO Queue for revalidation:

```typescript
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";
import d1NextTagCache from "@opennextjs/cloudflare/overrides/tag-cache/d1-next-tag-cache";

export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  queue: doQueue,
  tagCache: d1NextTagCache,  // Only if using revalidateTag/revalidatePath
});
```

**Required bindings**:

```jsonc
// wrangler.jsonc
{
  "r2_buckets": [
    { "binding": "NEXT_INC_CACHE_R2_BUCKET", "bucket_name": "my-cache" }
  ],
  "services": [
    { "binding": "WORKER_SELF_REFERENCE", "service": "my-app" }
  ],
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_CACHE_DO_QUEUE", "class_name": "DOQueueHandler" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["DOQueueHandler"] }
  ],
  // Only if using revalidateTag/revalidatePath
  "d1_databases": [
    { "binding": "NEXT_TAG_CACHE_D1", "database_id": "your-db-id" }
  ]
}
```

### Large Site with High Traffic

Use sharded Durable Objects for tag cache, regional cache for performance:

```typescript
// open-next.config.ts
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
  cachePurge: purgeCache({ type: "durableObject" }),
});
```

**Required bindings**:

```jsonc
// wrangler.jsonc
{
  "r2_buckets": [
    { "binding": "NEXT_INC_CACHE_R2_BUCKET", "bucket_name": "my-cache" }
  ],
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_CACHE_DO_QUEUE", "class_name": "DOQueueHandler" },
      { "name": "NEXT_TAG_CACHE_DO_SHARDED", "class_name": "DOShardedTagCache" },
      { "name": "NEXT_CACHE_DO_PURGE", "class_name": "BucketCachePurge" }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": [
        "DOQueueHandler",
        "DOShardedTagCache",
        "BucketCachePurge"
      ]
    }
  ]
}
```

For cache purge, also set secrets:

```bash
wrangler secret put CACHE_PURGE_API_TOKEN  # Cloudflare API token with Cache Purge permission
wrangler secret put CACHE_PURGE_ZONE_ID    # Your zone ID
```

### Staging Environment

Use memory queue for low-traffic staging:

```typescript
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import memoryQueue from "@opennextjs/cloudflare/overrides/queue/memory-queue";

export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
  queue: memoryQueue,  // Simple, no DO required
});
```

**Warning**: Memory queue only deduplicates per-isolate. Not recommended for production.

## Incremental Cache Options

### R2 Incremental Cache (Recommended)

Cost-effective S3-compatible storage:

```typescript
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: r2IncrementalCache,
});
```

**Setup**:

```bash
# Create R2 bucket
npx wrangler r2 bucket create my-next-cache

# Add to wrangler.jsonc
{
  "r2_buckets": [
    { "binding": "NEXT_INC_CACHE_R2_BUCKET", "bucket_name": "my-next-cache" }
  ]
}
```

**Environment variable**:
- `NEXT_INC_CACHE_R2_PREFIX` - Key prefix (default: `incremental-cache`)

**Characteristics**:
- Single-region storage
- Slower than KV but cheaper
- Best with regional cache

### Workers KV Cache

Fast, globally distributed key-value store:

```typescript
import kvIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/kv-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: kvIncrementalCache,
});
```

**Setup**:

```bash
# Create KV namespace
npx wrangler kv namespace create NEXT_INC_CACHE_KV

# Add to wrangler.jsonc
{
  "kv_namespaces": [
    { "binding": "NEXT_INC_CACHE_KV", "id": "your-kv-id" }
  ]
}
```

**Characteristics**:
- Eventually consistent
- Very fast reads (Tiered Cache)
- Higher cost than R2
- **Not recommended** due to eventual consistency

### Static Assets Cache (Read-Only)

Build-time only, no revalidation:

```typescript
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});
```

**No bindings required**. Uses Workers Static Assets.

**Characteristics**:
- Read-only
- No runtime revalidation
- Perfect for pure SSG sites
- No additional costs

## Regional Cache

Improves R2 cache performance by adding a faster Cache API layer:

```typescript
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import { withRegionalCache } from "@opennextjs/cloudflare/overrides/incremental-cache/regional-cache";

export default defineCloudflareConfig({
  incrementalCache: withRegionalCache(r2IncrementalCache, {
    mode: "long-lived",
    shouldLazilyUpdateOnCacheHit: true,
    bypassTagCacheOnCacheHit: false,
  }),
});
```

### Regional Cache Modes

**short-lived**: Responses cached for up to 1 minute

```typescript
withRegionalCache(r2IncrementalCache, {
  mode: "short-lived"
})
```

**long-lived**: Fetch responses until revalidated, ISR/SSG up to 30 minutes

```typescript
withRegionalCache(r2IncrementalCache, {
  mode: "long-lived",
  shouldLazilyUpdateOnCacheHit: true,      // Default for long-lived
  bypassTagCacheOnCacheHit: false,          // Default: check tag cache
})
```

### Regional Cache Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mode` | `"short-lived"` \| `"long-lived"` | Required | Cache duration strategy |
| `shouldLazilyUpdateOnCacheHit` | boolean | `true` for long-lived | Background R2 fetch on cache hit |
| `bypassTagCacheOnCacheHit` | boolean | `false` | Skip tag cache check on hit (requires cache purge) |

**Performance tip**: Set `bypassTagCacheOnCacheHit: true` with automatic cache purge enabled for fastest responses.

## Queue Configuration

Queues handle time-based revalidation (ISR pages with `revalidate` time).

### DO Queue (Recommended)

Durable Objects-backed queue with deduplication:

```typescript
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";

export default defineCloudflareConfig({
  queue: doQueue,
});
```

**Bindings**:

```jsonc
{
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_CACHE_DO_QUEUE", "class_name": "DOQueueHandler" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["DOQueueHandler"] }
  ]
}
```

**Environment variables**:

```bash
# Max concurrent revalidations per DO instance (default: 5)
NEXT_CACHE_DO_QUEUE_MAX_REVALIDATION=10

# Revalidation timeout in ms (default: 30000)
NEXT_CACHE_DO_QUEUE_REVALIDATION_TIMEOUT_MS=60000

# Retry interval in ms (default: 5000, exponential backoff)
NEXT_CACHE_DO_QUEUE_RETRY_INTERVAL_MS=10000

# Max retry attempts (default: 3)
NEXT_CACHE_DO_QUEUE_MAX_RETRIES=5

# Disable SQLite storage (default: false)
NEXT_CACHE_DO_QUEUE_DISABLE_SQLITE=false
```

**Characteristics**:
- Up to 10 DO instances (50 concurrent revalidations max)
- Request deduplication
- Automatic retries with backoff
- Production-ready

### Queue Cache Wrapper

Reduce queue load by caching queue state:

```typescript
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";
import queueCache from "@opennextjs/cloudflare/overrides/queue/queue-cache";

export default defineCloudflareConfig({
  queue: queueCache(doQueue, {
    regionalCacheTtlSec: 5,
    waitForQueueAck: true,
  }),
});
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `regionalCacheTtlSec` | number | 5 | Cache API TTL in seconds |
| `waitForQueueAck` | boolean | `true` | Wait for queue acknowledgment before returning |

### Memory Queue (Dev/Staging Only)

Simple in-memory queue without Durable Objects:

```typescript
import memoryQueue from "@opennextjs/cloudflare/overrides/queue/memory-queue";

export default defineCloudflareConfig({
  queue: memoryQueue,
});
```

**No bindings required**.

**Warning**: Only deduplicates within single isolate. Not suitable for production.

### Direct Queue (Debugging)

No queue, immediate revalidation (wrangler dev only):

```typescript
import directQueue from "@opennextjs/cloudflare/overrides/queue/direct-queue";

export default defineCloudflareConfig({
  queue: directQueue,
});
```

**For debugging only**. Does not work in production.

## Tag Cache Configuration

Tag cache enables on-demand revalidation via `revalidateTag()` and `revalidatePath()`.

**Skip if**:
- Pages Router only (no App Router)
- Not using `revalidateTag()` or `revalidatePath()`

### D1 Next Tag Cache

D1 database for tag storage:

```typescript
import d1NextTagCache from "@opennextjs/cloudflare/overrides/tag-cache/d1-next-tag-cache";

export default defineCloudflareConfig({
  tagCache: d1NextTagCache,
});
```

**Setup**:

```bash
# Create D1 database
npx wrangler d1 create next-tag-cache

# Create table
npx wrangler d1 execute next-tag-cache --command "
CREATE TABLE IF NOT EXISTS revalidations (
  tag TEXT PRIMARY KEY,
  revalidated_at INTEGER NOT NULL
)
"

# Add to wrangler.jsonc
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

**Characteristics**:
- Simple setup
- Good for low-to-medium traffic
- D1 read limits apply

### DO Sharded Tag Cache (High Traffic)

Durable Objects with sharding for high-load applications:

```typescript
import doShardedTagCache from "@opennextjs/cloudflare/overrides/tag-cache/do-sharded-tag-cache";

export default defineCloudflareConfig({
  tagCache: doShardedTagCache({ baseShardSize: 12 }),
});
```

**Bindings**:

```jsonc
{
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_TAG_CACHE_DO_SHARDED", "class_name": "DOShardedTagCache" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["DOShardedTagCache"] }
  ]
}
```

**Options**:
- `baseShardSize` - Number of shards (default: 10, recommended: 12-24 for high traffic)

**Characteristics**:
- Better performance under load
- Horizontal scaling via sharding
- Higher cost than D1

### DO Sharded with Filter

Optimized for specific tag patterns:

```typescript
import doShardedTagCacheWithFilter from "@opennextjs/cloudflare/overrides/tag-cache/do-sharded-tag-cache-with-filter";

export default defineCloudflareConfig({
  tagCache: doShardedTagCacheWithFilter({
    baseShardSize: 12,
    filter: (tags) => tags.filter(tag => tag.startsWith("product:"))
  }),
});
```

Only specified tags go to tag cache, reducing load.

## Cache Purge (Automatic Invalidation)

Automatically purge Cloudflare Cache API when pages are revalidated.

**Required**:
- Custom domain with Cloudflare zone
- On-demand revalidation (`revalidateTag`/`revalidatePath`)
- Regional cache or cache interception enabled

### Direct Cache Purge

Direct API calls to Cloudflare:

```typescript
import { purgeCache } from "@opennextjs/cloudflare/overrides/cache-purge/index";

export default defineCloudflareConfig({
  cachePurge: purgeCache({ type: "direct" }),
});
```

**Setup**:

```bash
# Create API token with Cache Purge permission
# https://dash.cloudflare.com/profile/api-tokens

# Set secrets
wrangler secret put CACHE_PURGE_API_TOKEN
wrangler secret put CACHE_PURGE_ZONE_ID
```

**Characteristics**:
- Simple setup
- Rate limited (Cloudflare API limits)
- Suitable for low-frequency revalidation

### Durable Object Cache Purge (High Frequency)

Buffers purge requests to avoid rate limits:

```typescript
import { purgeCache } from "@opennextjs/cloudflare/overrides/cache-purge/index";

export default defineCloudflareConfig({
  cachePurge: purgeCache({ type: "durableObject" }),
});
```

**Bindings**:

```jsonc
{
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_CACHE_DO_PURGE", "class_name": "BucketCachePurge" }
    ]
  },
  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["BucketCachePurge"] }
  ]
}
```

**Environment variable**:

```bash
# Buffer time in seconds (default: 5)
NEXT_CACHE_DO_PURGE_BUFFER_TIME_IN_SECONDS=10
```

**Characteristics**:
- Buffers purges for specified time
- Batches multiple purges
- Avoids rate limits
- Recommended for high-traffic sites

## Static Assets Caching

Configure CDN caching for static files:

### public/_headers

```
# Immutable static assets - cache forever
/_next/static/*
  Cache-Control: public, max-age=31536000, immutable

# Public assets - cache for 1 hour
/*
  Cache-Control: public, max-age=3600

# Fonts - cache forever
/fonts/*
  Cache-Control: public, max-age=31536000, immutable

# Images - cache for 1 day
/images/*
  Cache-Control: public, max-age=86400
```

**Deploy**: Add file to your repository, OpenNext includes it automatically.

**Why this matters**:
- `/_next/static/*` files have content hashes
- `immutable` directive prevents revalidation
- Improves performance and reduces origin requests

## Cache Interception

Skip NextServer for cached routes to improve cold start performance:

```typescript
export default defineCloudflareConfig({
  enableCacheInterception: true,
});
```

**Benefits**:
- Faster cold starts for cached routes
- Less JavaScript execution
- Lower CPU time

**Limitations**:
- Does not work with PPR (Partial Prerendering)
- Disabled by default

**Use when**:
- Not using PPR
- Using ISR/SSG heavily
- Cold start performance is critical

## Cache Initialization

Cache must be populated during deployment:

```bash
# Automatic with preview/deploy/upload
npm run preview  # Populates local bindings
npm run deploy   # Populates remote bindings
npm run upload   # Populates remote bindings

# Manual
npx opennextjs-cloudflare populateCache local   # Local development
npx opennextjs-cloudflare populateCache remote  # Production
```

The CLI automatically populates:
- Incremental cache with build-time data
- Tag cache with build-time revalidation info

**From v1.13.0**: R2 batch uploads work automatically.

**Before v1.13.0**: Use rclone for faster R2 uploads (optional):

```bash
# Install rclone and configure
export R2_ACCESS_KEY_ID=your-access-key
export R2_SECRET_ACCESS_KEY=your-secret-key
export CLOUDFLARE_ACCOUNT_ID=your-account-id

npx opennextjs-cloudflare populateCache remote
```

## Cache Debugging

Enable debug logging:

```bash
# .env or .dev.vars
NEXT_PRIVATE_DEBUG_CACHE=1
```

Logs every cache operation with:
- Cache hits/misses
- Revalidation triggers
- Tag operations
- Storage operations

## Complete Configuration Examples

### Production-Ready Large Site

```typescript
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";
import { withRegionalCache } from "@opennextjs/cloudflare/overrides/incremental-cache/regional-cache";
import doQueue from "@opennextjs/cloudflare/overrides/queue/do-queue";
import queueCache from "@opennextjs/cloudflare/overrides/queue/queue-cache";
import doShardedTagCache from "@opennextjs/cloudflare/overrides/tag-cache/do-sharded-tag-cache";
import { purgeCache } from "@opennextjs/cloudflare/overrides/cache-purge/index";

export default defineCloudflareConfig({
  incrementalCache: withRegionalCache(r2IncrementalCache, {
    mode: "long-lived",
    bypassTagCacheOnCacheHit: true,
  }),
  queue: queueCache(doQueue, {
    regionalCacheTtlSec: 5,
    waitForQueueAck: false,
  }),
  tagCache: doShardedTagCache({ baseShardSize: 16 }),
  enableCacheInterception: true,
  cachePurge: purgeCache({ type: "durableObject" }),
});
```

```jsonc
// wrangler.jsonc
{
  "name": "my-app",
  "r2_buckets": [
    { "binding": "NEXT_INC_CACHE_R2_BUCKET", "bucket_name": "my-cache" }
  ],
  "durable_objects": {
    "bindings": [
      { "name": "NEXT_CACHE_DO_QUEUE", "class_name": "DOQueueHandler" },
      { "name": "NEXT_TAG_CACHE_DO_SHARDED", "class_name": "DOShardedTagCache" },
      { "name": "NEXT_CACHE_DO_PURGE", "class_name": "BucketCachePurge" }
    ]
  },
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": [
        "DOQueueHandler",
        "DOShardedTagCache",
        "BucketCachePurge"
      ]
    }
  ]
}
```

### Simple SSG Blog

```typescript
// open-next.config.ts
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
import staticAssetsIncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/static-assets-incremental-cache";

export default defineCloudflareConfig({
  incrementalCache: staticAssetsIncrementalCache,
  enableCacheInterception: true,
});
```

No additional bindings required.

## Best Practices

1. **Start simple** - Use Static Assets for SSG, add ISR only when needed
2. **Use regional cache with R2** - Significantly improves performance
3. **Enable cache interception** - Faster cold starts (unless using PPR)
4. **Sharded tag cache for high traffic** - Better than D1 under load
5. **Use queue cache wrapper** - Reduces queue pressure
6. **Enable automatic cache purge** - With regional cache and on-demand revalidation
7. **Monitor DO usage** - Check Durable Objects analytics in dashboard
8. **Set appropriate revalidation times** - Don't revalidate too frequently
9. **Use debug mode during development** - `NEXT_PRIVATE_DEBUG_CACHE=1`
10. **Test with preview** - Verify caching works before deploying

## Related Documentation

- [../SKILL.md](../SKILL.md) - Main OpenNext skill overview
- [configuration.md](configuration.md) - wrangler.jsonc and environment setup
- [database-orm.md](database-orm.md) - Database patterns
- [troubleshooting.md](troubleshooting.md) - Common issues
