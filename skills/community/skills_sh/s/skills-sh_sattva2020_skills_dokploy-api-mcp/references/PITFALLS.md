# Dokploy Deployment Pitfalls

Real-world issues encountered during production deployments and their solutions.

## 1. Empty `public/` Directory — Docker COPY Fails

**Error:**
```
COPY --from=builder /app/public ./public
ERROR: "/app/public": not found
```

**Cause:** Git does not track empty directories. If `public/` has no files, it won't exist after `git clone`.

**Fix:** Add `RUN mkdir -p public` in the Dockerfile builder stage:
```dockerfile
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN mkdir -p public          # <-- add this
RUN npm run build
```

## 2. Neon HTTP Driver vs Standard PostgreSQL

**Error:**
```
Health check: {"database": "error", "redis": "ok"}
```

**Cause:** `@neondatabase/serverless` with `drizzle-orm/neon-http` driver communicates via HTTPS to Neon's proxy endpoint. Dokploy PostgreSQL is a standard container — it speaks the PostgreSQL wire protocol on port 5432, not HTTPS.

**Fix:** Switch to `postgres` (postgres.js) package:
```typescript
// Before (broken with standard PG)
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
const sql = neon(env.DATABASE_URL);
export const db = drizzle(sql, { schema });

// After (works with any PostgreSQL)
import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";
const sql = postgres(env.DATABASE_URL, { max: 10 });
export const db = drizzle(sql, { schema });
```

**Note:** If your app also deploys to Neon (e.g. Vercel), consider using `postgres` everywhere — it works with both Neon and standard PostgreSQL.

## 3. Clerk `publishableKey` Validation During Build

**Error:**
```
@clerk/clerk-react: Missing publishableKey
```

**Cause:** `ClerkProvider` validates `publishableKey` format at render time. During `next build` in Docker, environment variables are placeholders or empty. Static page generation triggers ClerkProvider rendering.

**Fix (two-part):**

1. Add `export const dynamic = "force-dynamic"` to root layout to prevent SSG:
```typescript
// src/app/layout.tsx
export const dynamic = "force-dynamic";
```

2. Conditionally skip ClerkProvider during build:
```typescript
const isBuildPhase =
  process.env.BUILDING === "1" ||
  process.env.NEXT_PHASE === "phase-production-build";

export default function RootLayout({ children }) {
  if (isBuildPhase) {
    return <html>...</html>;  // no ClerkProvider
  }
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}>
      <html>...</html>
    </ClerkProvider>
  );
}
```

3. Set `BUILDING=1` in Dockerfile builder stage (absent in runner):
```dockerfile
FROM base AS builder
ENV BUILDING=1
RUN npm run build
```

## 4. Database Migrations in Next.js Standalone Output

**Error:**
```
Container exit code 1 — crash loop
```

**Cause:** Next.js `output: "standalone"` only traces modules imported by the app. A standalone `migrate.mjs` script that imports `drizzle-orm/postgres-js/migrator` can't resolve the module because it's not in the traced `node_modules`.

**Fix:** Run migrations via an in-app API endpoint instead of a standalone script:

```typescript
// src/app/api/migrate/route.ts
import { db } from "@/db";
import { sql } from "drizzle-orm";
import { readFileSync, existsSync } from "fs";
import { join } from "path";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  // Protect with a secret token
  const authHeader = req.headers.get("authorization");
  const expectedToken = process.env.TOKEN_ENCRYPTION_KEY;
  if (!expectedToken || authHeader !== `Bearer ${expectedToken}`) {
    return Response.json({ error: "Unauthorized" }, { status: 401 });
  }

  const migrationsDir = join(process.cwd(), "drizzle");
  const journalPath = join(migrationsDir, "meta", "_journal.json");
  if (!existsSync(journalPath)) {
    return Response.json({ error: "No migration journal found" }, { status: 404 });
  }

  // ... read journal, execute SQL statements, track applied migrations
}
```

**Important:** The `drizzle/` directory must be:
1. Not in `.gitignore` (so migration SQL files are committed)
2. Copied in Dockerfile: `COPY --from=builder /app/drizzle ./drizzle`

Trigger migration after deploy:
```bash
curl -X POST "https://app-domain/api/migrate" \
  -H "Authorization: Bearer ${TOKEN_ENCRYPTION_KEY}"
```

## 5. Build Logs — WebSocket Only

**Problem:** After triggering a deploy via API, you want to read build logs programmatically.

**Reality:** Dokploy streams build logs via WebSocket only. These endpoints do NOT exist:
- ~~`deployment.readBuildLog`~~
- ~~`deployment.readLog`~~
- ~~`deployment.getLog`~~
- ~~`application.readStdoutLogs`~~
- ~~`application.readBuildLog`~~
- ~~`docker.getContainerLogs`~~

**Workaround:**
1. Poll `deployment.all` for status changes (`running` → `done`/`error`)
2. Use the Dokploy Dashboard UI to view build logs
3. Use the MCP server (`@sattva/dokploy-mcp`) which may handle WebSocket internally

## 6. External Database Port Unreachable

**Problem:** Set `externalPort: 25432` on PostgreSQL via API, but can't connect from outside.

**Cause:** VPS firewall (iptables/ufw/cloud security group) blocks the port.

**Fix:** Use internal Docker network hostnames instead:
```
# Internal connection (from app container to DB container)
postgresql://user:pass@postgres-appname-randomid:5432/dbname

# NOT external (may be blocked)
postgresql://user:pass@vps-ip:25432/dbname
```

Internal hostnames follow the pattern: `<appName>` from Dokploy (visible in service details).

## 7. drizzle/ Directory in .gitignore

**Problem:** Dockerfile has `COPY --from=builder /app/drizzle ./drizzle` but the directory is empty in the container.

**Cause:** `.gitignore` contains `drizzle/`, so migration files aren't committed.

**Fix:** Remove `drizzle/` from `.gitignore` and commit migration files:
```bash
# Remove from .gitignore
# Then commit migration files
git add drizzle/
git commit -m "track drizzle migration files"
```

## 8. SSL Certificate Errors

**Problem:** `curl` fails with SSL error after setting up a domain.

**Cause:** Let's Encrypt certificate hasn't been provisioned yet, or Traefik needs DNS to be properly pointed.

**Fix:**
1. Ensure DNS A-record points to VPS IP
2. Wait for Traefik to auto-provision Let's Encrypt cert
3. Use `curl -sk` for testing (skip verification)
4. Check Traefik dashboard if certificate isn't provisioning

## 9. BullMQ/Redis Connection During Build

**Error:**
```
Redis connection refused during next build
```

**Cause:** BullMQ eagerly creates Redis connections on module import. During Docker build, Redis is unavailable.

**Fix:** Lazy-initialize BullMQ queues:
```typescript
let _queue: Queue | null = null;

export function getQueue() {
  if (!_queue && !isBuildPhase) {
    _queue = new Queue("tasks", { connection: redisConfig });
  }
  return _queue;
}
```

## 10. Traefik v3 Breaking Changes (Dokploy v0.25+)

**Problem:** After Dokploy upgrade to v0.25+, custom Traefik middleware configs stop working or routing breaks.

**Cause:** Dokploy v0.25 upgraded to Traefik v3. Key breaking changes:
- `PathPrefix` middleware syntax changed
- Some deprecated v2 labels no longer work
- `entryPoints` naming may differ

**Fix:**
1. Check current Traefik config via `application.readTraefikConfig`
2. Update labels to Traefik v3 syntax:
```yaml
# Traefik v2 (old)
- "traefik.http.routers.app.rule=PathPrefix(`/api`)"
# Traefik v3 (new) — same syntax but verify middlewares
- "traefik.http.routers.app.rule=PathPrefix(`/api`)"
```
3. Review middleware configs — some v2 middleware plugins may need updates
4. Use `settings.readMiddlewareTraefikConfig` and `settings.updateMiddlewareTraefikConfig` MCP tools to inspect/fix global middleware
5. If Traefik dashboard is needed: use `settings.toggleDashboard` MCP tool

## 11. Stripe SDK Initialization During Build

**Error:**
```
Stripe requires a secret key
```

**Cause:** Stripe SDK validates the secret key on instantiation. During build, the key is a placeholder.

**Fix:** Lazy-initialize Stripe:
```typescript
let _stripe: Stripe | null = null;

export function getStripe() {
  if (!_stripe) {
    _stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
  }
  return _stripe;
}
```
