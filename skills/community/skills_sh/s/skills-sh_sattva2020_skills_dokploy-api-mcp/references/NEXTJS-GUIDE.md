# Deploying Next.js to Dokploy

Step-by-step guide for deploying Next.js 14/15 (App Router) applications to Dokploy, covering all known pitfalls.

**Note:** This guide applies to both Next.js 14 and 15. Next.js 15 changed `params` to async in dynamic routes and uses React 19, but the Dokploy deployment process is identical.

## Prerequisites

- Dokploy instance with PostgreSQL and Redis services created
- Application created in Dokploy with Git source connected
- Domain configured and DNS pointed to VPS IP

## Dockerfile Template

```dockerfile
FROM node:20-alpine AS base

# --- Dependencies ---
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# --- Builder ---
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Create public/ dir (Git doesn't track empty directories)
RUN mkdir -p public

# Build-phase flags
ENV NEXT_TELEMETRY_DISABLED=1
ENV BUILDING=1
ENV NODE_OPTIONS="--max-old-space-size=4096"

RUN npm run build

# --- Runner ---
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy build output
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy migration files (if using Drizzle)
COPY --from=builder /app/drizzle ./drizzle

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

## next.config.js Requirements

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",  // REQUIRED for Docker deployment
};

module.exports = nextConfig;
```

## Environment Variables

Set in Dokploy Dashboard → Application → Environment:

```bash
# Database (use internal Docker hostname)
DATABASE_URL=postgresql://user:pass@postgres-appname-id:5432/dbname

# Redis (use internal Docker hostname)
REDIS_URL=redis://:password@redis-appname-id:6379

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# App
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NODE_ENV=production

# Other secrets
TOKEN_ENCRYPTION_KEY=your-secret
STRIPE_SECRET_KEY=sk_...
ANTHROPIC_API_KEY=sk-ant-...
```

**Important:** Use internal Docker network hostnames for database/Redis connections (not `localhost` or external IP).

## Build-Phase Guards

Modules that connect to external services (DB, Redis, Stripe, etc.) must not run during `next build`.

### Pattern: Build-Phase Detection

```typescript
const isBuildPhase =
  process.env.BUILDING === "1" ||
  process.env.NEXT_PHASE === "phase-production-build";
```

### Database Connection

```typescript
import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";

const isBuildPhase = process.env.BUILDING === "1";

const sql = postgres(env.DATABASE_URL, {
  max: isBuildPhase ? 0 : 10,  // zero connections during build
});

export const db = drizzle(sql, { schema });
```

### ClerkProvider (Root Layout)

```typescript
// src/app/layout.tsx
export const dynamic = "force-dynamic";

const isBuildPhase =
  process.env.BUILDING === "1" ||
  process.env.NEXT_PHASE === "phase-production-build";

export default function RootLayout({ children }) {
  const inner = (
    <html lang="en">
      <body>
        <ThemeProvider>
          <TRPCProvider>{children}</TRPCProvider>
        </ThemeProvider>
      </body>
    </html>
  );

  if (isBuildPhase) return inner;

  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}>
      {inner}
    </ClerkProvider>
  );
}
```

### BullMQ Queues

```typescript
let _queue: Queue | null = null;

export function getQueue() {
  if (!_queue && process.env.BUILDING !== "1") {
    _queue = new Queue("tasks", { connection: redisConfig });
  }
  return _queue;
}
```

### Stripe

```typescript
let _stripe: Stripe | null = null;

export function getStripe() {
  if (!_stripe) {
    _stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
  }
  return _stripe;
}
```

## Environment Validation

If using Zod for env validation (`src/lib/env.ts`), provide build-phase defaults:

```typescript
const isBuildPhase =
  process.env.BUILDING === "1" ||
  process.env.NEXT_PHASE === "phase-production-build";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string(),
  // ... other vars
});

// During build, provide placeholder defaults
const buildDefaults = isBuildPhase ? {
  DATABASE_URL: "postgresql://build:build@localhost:5432/build",
  REDIS_URL: "redis://localhost:6379",
  CLERK_SECRET_KEY: "sk_test_build_placeholder",
  // ... etc
} : {};

export const env = envSchema.parse({
  ...buildDefaults,
  ...process.env,
});
```

## Database Migrations

### Option A: In-App API Endpoint (Recommended)

Create `src/app/api/migrate/route.ts` that reads Drizzle migration files and executes them. Protected by a secret token.

Trigger after deploy:
```bash
curl -X POST "https://your-domain.com/api/migrate" \
  -H "Authorization: Bearer ${TOKEN_ENCRYPTION_KEY}"
```

### Option B: Standalone Script with CMD

**WARNING:** This approach has issues with Next.js `output: "standalone"` because the standalone output only traces modules imported by the app. External scripts can't access `drizzle-orm/postgres-js/migrator` or similar modules.

If you still want to try:
```dockerfile
COPY --from=builder /app/migrate.mjs ./
CMD ["sh", "-c", "node migrate.mjs && node server.js"]
```

The `migrate.mjs` must use only the `postgres` package directly (no drizzle-orm imports):
```javascript
import postgres from "postgres";
import { readFileSync, existsSync } from "fs";

const sql = postgres(process.env.DATABASE_URL, { max: 1 });
// ... manually read and execute SQL files from ./drizzle/
```

### Option C: Dokploy Pre-Deploy Command

If Dokploy supports pre-deploy hooks (check dashboard), you can run migrations there.

## .gitignore Checklist

Ensure these are NOT in `.gitignore` (needed for deployment):

```
# These MUST be tracked:
# drizzle/          ← migration SQL files
# public/           ← static assets (or use mkdir in Dockerfile)

# These SHOULD be ignored:
.next/
node_modules/
.env
.env.local
```

## Health Check Endpoint

Create `src/app/api/health/route.ts` for monitoring:

```typescript
export const dynamic = "force-dynamic";

export async function GET() {
  const checks = { database: "ok", redis: "ok" };
  try {
    await db.execute(sql`SELECT 1`);
  } catch { checks.database = "error"; }
  try {
    await redis.ping();
  } catch { checks.redis = "error"; }

  const healthy = Object.values(checks).every(v => v === "ok");
  return Response.json(
    { status: healthy ? "healthy" : "degraded", checks },
    { status: healthy ? 200 : 503 }
  );
}
```

## Deployment Checklist

1. [ ] `output: "standalone"` in next.config.js
2. [ ] `RUN mkdir -p public` in Dockerfile
3. [ ] `BUILDING=1` env var in builder stage
4. [ ] Build-phase guards on DB, Redis, Stripe, BullMQ, Clerk
5. [ ] `drizzle/` tracked in Git (not in .gitignore)
6. [ ] Internal Docker hostnames for DB/Redis connections
7. [ ] Domain DNS A-record pointing to VPS IP
8. [ ] All env vars set in Dokploy Dashboard
9. [ ] Health endpoint created and accessible
10. [ ] Database migrations ready (API endpoint or script)
