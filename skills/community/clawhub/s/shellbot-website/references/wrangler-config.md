# Wrangler Configuration Reference

## Config Formats

Wrangler supports TOML and JSON/JSONC. **If both exist, JSON takes precedence.** Pick one.

### TOML (wrangler.toml)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-30"
compatibility_flags = ["nodejs_compat"]
```

### JSONC (wrangler.jsonc)

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-30",
  "compatibility_flags": ["nodejs_compat"]
}
```

The JSONC format supports schema-driven autocomplete in editors.

## Core Settings

| Field | Description |
|-------|-------------|
| `name` | Worker name (used in URLs and dashboard) |
| `main` | Entry point file |
| `compatibility_date` | API version date (use latest stable) |
| `compatibility_flags` | Feature flags (e.g., `nodejs_compat` for Node.js APIs) |
| `account_id` | Optional, auto-detected from token |
| `workers_dev` | Enable `*.workers.dev` subdomain (default: true) |

## Bindings

### D1 Database

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

Access in code: `env.DB.prepare("SELECT * FROM users").all()`

### KV Namespace

```toml
[[kv_namespaces]]
binding = "CACHE"
id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Access in code: `env.CACHE.get("key")`, `env.CACHE.put("key", "value")`

### R2 Bucket

```toml
[[r2_buckets]]
binding = "ASSETS"
bucket_name = "my-bucket"
```

Access in code: `env.ASSETS.get("file.png")`, `env.ASSETS.put("file.png", data)`

### Queues

```toml
# Producer
[[queues.producers]]
binding = "QUEUE"
queue = "my-queue"

# Consumer
[[queues.consumers]]
queue = "my-queue"
max_batch_size = 10
max_batch_timeout = 5
```

### Durable Objects

```toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

### Service Bindings

```toml
[[services]]
binding = "AUTH_SERVICE"
service = "auth-worker"
```

### Analytics Engine

```toml
[[analytics_engine_datasets]]
binding = "ANALYTICS"
```

### Vectorize

```toml
[[vectorize]]
binding = "VECTOR_INDEX"
index_name = "my-index"
```

## Environment Variables

```toml
[vars]
API_URL = "https://api.example.com"
DEBUG = "false"
```

Secrets (set via `wrangler secret put`, not in config):
```typescript
// Access in code the same as vars
const apiKey = env.API_KEY;
```

## Environments

```toml
name = "my-worker"
main = "src/index.ts"

# Default environment vars
[vars]
API_URL = "https://api.example.com"

# Production overrides
[env.production]
vars = { API_URL = "https://api.example.com" }

[env.production.d1_databases]
# Can override bindings per environment

# Staging overrides
[env.staging]
vars = { API_URL = "https://staging.example.com" }
```

Deploy to environment: `wrangler deploy -e production`

## Static Assets

```toml
[assets]
directory = "./public"
binding = "ASSETS"
```

For frameworks like Next.js (via OpenNext):

```toml
name = "my-site"
main = ".open-next/worker.js"
compatibility_date = "2024-12-30"
compatibility_flags = ["nodejs_compat"]

[assets]
directory = ".open-next/assets"
binding = "ASSETS"
```

## Routes & Custom Domains

```toml
# Route patterns
[[routes]]
pattern = "example.com/*"
zone_id = "your-zone-id"

# Multiple routes
[[routes]]
pattern = "www.example.com/*"
zone_id = "your-zone-id"

# Zone name instead of ID
[[routes]]
pattern = "api.example.com/*"
zone_name = "example.com"
```

## Cron Triggers

```toml
[triggers]
crons = ["*/5 * * * *", "0 0 * * *"]
```

Handle in code:
```typescript
export default {
  async scheduled(event, env, ctx) {
    // Runs on schedule
  }
};
```

## Compatibility Flags

Common flags:

| Flag | Purpose |
|------|---------|
| `nodejs_compat` | Enable Node.js built-in APIs |
| `streams_enable_constructors` | Enable TransformStream constructors |
| `transformstream_enable_standard_constructor` | Standard TransformStream |

## Limits

| Resource | Free | Paid |
|----------|------|------|
| Requests | 100K/day | Unlimited |
| CPU time | 10ms | 30s (50ms default) |
| Memory | 128MB | 128MB |
| Script size | 1MB | 10MB |
| KV reads | 100K/day | 10M/month |
| D1 rows read | 5M/day | 25B/month |
| R2 Class A ops | 1M/month | 10M/month |

## Configuration Tips

- Set `compatibility_date` to the date you start the project, update periodically
- Use `nodejs_compat` flag for most projects (enables `Buffer`, `crypto`, etc.)
- Keep secrets out of config — use `wrangler secret put`
- Use JSONC format for editor autocomplete via `$schema`
- Test locally with `wrangler dev` before deploying
