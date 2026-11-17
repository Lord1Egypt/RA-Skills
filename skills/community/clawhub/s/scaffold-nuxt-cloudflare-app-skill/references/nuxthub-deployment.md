# NuxtHub v0.10.x — deployment specifics

Adapted from [onmax/nuxt-skills](https://github.com/onmax/nuxt-skills)'s `nuxthub` skill ([SKILL.md](https://github.com/onmax/nuxt-skills/blob/main/skills/nuxthub/SKILL.md), [references/providers.md](https://github.com/onmax/nuxt-skills/blob/main/skills/nuxthub/references/providers.md), [references/wrangler-templates.md](https://github.com/onmax/nuxt-skills/blob/main/skills/nuxthub/references/wrangler-templates.md)) — check that source for anything not covered here or for newer NuxtHub releases.

## `npx nuxthub deploy` is deprecated

As of NuxtHub v0.10, the NuxtHub CLI's own deploy command and NuxtHub Admin (the hosted dashboard) are being phased out (Admin sunsets 2025-12-31). **Use `wrangler deploy` instead** — this confirms/matches SKILL.md §7: NuxtHub is the bindings/runtime layer, Wrangler is the deploy mechanism, full stop.

## Two ways to configure Cloudflare resources

**Auto-generated `wrangler.json`** (NuxtHub's default): declare resources directly in the `hub` block of `nuxt.config.ts` and NuxtHub writes `wrangler.json` from it at build time — no hand-maintained `wrangler.jsonc` needed for a simple, single-environment app:

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  hub: {
    db: {
      dialect: 'sqlite',
      driver: 'd1',
      connection: { databaseId: '<database-id>' }
    },
    kv: { driver: 'cloudflare-kv-binding', namespaceId: '<kv-namespace-id>' },
    cache: { driver: 'cloudflare-kv-binding', namespaceId: '<cache-namespace-id>' },
    blob: { driver: 'cloudflare-r2', bucketName: '<bucket-name>' }
  }
})
```

A shorthand also exists for the common case where you just want local dev emulation + let NuxtHub manage the rest: `hub: { db: 'sqlite', kv: true, blob: true, cache: true }`.

**Manual `wrangler.jsonc`** (what this skill defaults to): needed for anything auto-generation doesn't cover — `observability`, custom `migrations_table`/`migrations_dir`, and multi-environment (`env.preview`) setups. Required binding names NuxtHub expects if you hand-write them:

| Feature | Binding name | Type |
|---|---|---|
| Database | `DB` | D1 |
| Key-value | `KV` | KV Namespace |
| Cache | `CACHE` | KV Namespace |
| Blob storage | `BLOB` | R2 Bucket |

Advanced escape hatch if neither the `hub` block nor a full manual `wrangler.jsonc` fits: `nitro.cloudflare.wrangler` in `nuxt.config.ts` accepts the same keys (`d1_databases`, `kv_namespaces`, `r2_buckets`, `compatibility_flags`, ...) inline.

## Creating the actual Cloudflare resources

```bash
npx wrangler d1 create <app-name>-db              # → database_id
npx wrangler kv namespace create KV               # → id, if KV is in scope
npx wrangler kv namespace create CACHE            # → id, if the cache feature is in scope
npx wrangler r2 bucket create <app-name>-bucket   # → bucket name (no id needed), if Blob is in scope
```

## Preview/staging environments — build-time selection

NuxtHub's Cloudflare integration reads a `CLOUDFLARE_ENV` environment variable at **build** time to pick which named environment's config applies, in addition to (not instead of) Wrangler's own `--env` flag at **deploy** time — pass both for clarity:

```bash
# Production
npx nuxi build
npx wrangler deploy

# Preview/staging
CLOUDFLARE_ENV=preview npx nuxi build
npx wrangler deploy --env preview
```

This pairs with the `env.preview` block already shown in `wrangler.example.jsonc` — a separate `database_id` (and `KV`/`CACHE`/`BLOB` ids if those are in scope) per environment, since Wrangler bindings are not inherited between environments.

## Database migrations — use the `nuxt db` CLI, not raw `drizzle-kit`

NuxtHub wraps Drizzle Kit with its own Nuxt CLI subcommand (backed by `@nuxthub/db`, listed as a devDependency alongside `drizzle-kit`/`better-sqlite3`):

```bash
npx nuxt db generate                  # generate migrations from server/db/schema.ts
npx nuxt db migrate                   # apply pending migrations
npx nuxt db sql "SELECT * FROM users" # run raw SQL
npx nuxt db squash                    # squash migrations into one
```

Output lands in the same `server/db/migrations/sqlite/` + `meta/_journal.json` shape Drizzle Kit always produces — `nuxt db` is a thinner CLI over the same tool, not a different migration format. Migrations also auto-apply during `nuxi dev`/`nuxi build` unless `hub.db.applyMigrationsDuringBuild: false` is set (this skill's default — see SKILL.md §6).

## Runtime imports: `hub:db` / `hub:kv` / `hub:blob`

Current NuxtHub versions expose virtual-module imports:

```ts
import { db, schema } from 'hub:db'   // equivalently `import { db, schema } from '@nuxthub/db'`
import { kv } from 'hub:kv'
import { blob } from 'hub:blob'
```

`db`/`kv`/`blob` are also auto-imported server-side, so an explicit import often isn't even necessary. Older NuxtHub composables (`hubDatabase()`, `hubKV()`, `hubBlob()`) predate this and may still appear in examples elsewhere — prefer the `hub:*` imports for anything scaffolded fresh.

## Deprecated Cloudflare-specific features (v0.10)

Don't scaffold new code against these — `hubAI()` (use the AI SDK's Workers AI provider instead), `hubBrowser()` (use Puppeteer), `hubVectorize()` (use Vectorize directly).
