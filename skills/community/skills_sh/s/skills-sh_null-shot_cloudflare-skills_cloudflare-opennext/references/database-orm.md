# Database and ORM Reference

Complete guide to using databases and ORMs (Drizzle, Prisma) in Next.js on Cloudflare Workers with OpenNext.

## Critical Principle: Per-Request Database Clients

**Never create global database clients in Cloudflare Workers.**

Some database adapters (like PostgreSQL) use connection pooling and will reuse connections across requests. This violates Workers' isolation model and causes errors:

```
Error: Cannot perform I/O on behalf of a different request.
```

**Solution**: Create a new database client for each request.

## Quick Reference

| Database | Recommended ORM | Pattern |
|----------|----------------|---------|
| D1 | Drizzle or Prisma | Per-request with `cache()` |
| PostgreSQL | Drizzle or Prisma | Per-request with `maxUses: 1` |
| Hyperdrive | Drizzle or Prisma | Per-request with `maxUses: 1` |
| MySQL | Drizzle | Per-request with `maxUses: 1` |

## Drizzle ORM

Drizzle is a lightweight TypeScript ORM with excellent Cloudflare Workers support.

### D1 with Drizzle

```typescript
// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { drizzle } from "drizzle-orm/d1";
import { cache } from "react";
import * as schema from "./schema/d1";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  return drizzle(env.DB, { schema });
});

// For SSG routes (Static Site Generation)
export const getDbAsync = cache(async () => {
  const { env } = await getCloudflareContext({ async: true });
  return drizzle(env.DB, { schema });
});
```

**Schema example**:

```typescript
// lib/schema/d1.ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
});

export const posts = sqliteTable("posts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: integer("user_id").notNull().references(() => users.id),
  title: text("title").notNull(),
  content: text("content").notNull(),
  published: integer("published", { mode: "boolean" }).notNull().default(false),
});
```

**Usage in route**:

```typescript
// app/api/users/route.ts
import { getDb } from "@/lib/db";
import { users } from "@/lib/schema/d1";

export async function GET() {
  const db = getDb();
  const allUsers = await db.select().from(users);
  return Response.json(allUsers);
}

export async function POST(request: Request) {
  const db = getDb();
  const body = await request.json();
  
  const [newUser] = await db
    .insert(users)
    .values({
      name: body.name,
      email: body.email,
      createdAt: new Date(),
    })
    .returning();
  
  return Response.json(newUser);
}
```

**wrangler.jsonc**:

```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "your-database-id"
    }
  ]
}
```

### PostgreSQL with Drizzle

```typescript
// lib/db.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { cache } from "react";
import * as schema from "./schema/pg";
import { Pool } from "pg";

export const getDb = cache(() => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    maxUses: 1,  // CRITICAL: Don't reuse connections across requests
  });
  return drizzle({ client: pool, schema });
});
```

**Why `maxUses: 1`**: Forces the pool to close connections after one use, preventing cross-request I/O errors.

**Schema example**:

```typescript
// lib/schema/pg.ts
import { pgTable, serial, text, timestamp, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  userId: serial("user_id").notNull().references(() => users.id),
  title: text("title").notNull(),
  content: text("content").notNull(),
  published: boolean("published").notNull().default(false),
});
```

**Environment setup**:

```bash
# .dev.vars
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

### Hyperdrive with Drizzle

Hyperdrive accelerates PostgreSQL connections from Workers:

```typescript
// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { drizzle } from "drizzle-orm/node-postgres";
import { cache } from "react";
import * as schema from "./schema/pg";
import { Pool } from "pg";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  const connectionString = env.HYPERDRIVE.connectionString;
  
  const pool = new Pool({
    connectionString,
    maxUses: 1,  // CRITICAL: Don't reuse connections
  });
  
  return drizzle({ client: pool, schema });
});

// For SSG routes
export const getDbAsync = cache(async () => {
  const { env } = await getCloudflareContext({ async: true });
  const connectionString = env.HYPERDRIVE.connectionString;
  
  const pool = new Pool({
    connectionString,
    maxUses: 1,
  });
  
  return drizzle({ client: pool, schema });
});
```

**wrangler.jsonc**:

```jsonc
{
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "your-hyperdrive-id"
    }
  ]
}
```

**Setup Hyperdrive**:

```bash
# Create Hyperdrive config
wrangler hyperdrive create my-hyperdrive \
  --connection-string="postgresql://user:pass@host:5432/db"
```

### Drizzle with Transactions

```typescript
import { getDb } from "@/lib/db";
import { users, accounts } from "@/lib/schema/pg";

export async function POST(request: Request) {
  const db = getDb();
  const body = await request.json();
  
  // Transaction ensures atomicity
  const result = await db.transaction(async (tx) => {
    const [user] = await tx
      .insert(users)
      .values({ name: body.name, email: body.email })
      .returning();
    
    await tx
      .insert(accounts)
      .values({ userId: user.id, balance: 0 });
    
    return user;
  });
  
  return Response.json(result);
}
```

### Drizzle Migrations

Create and run migrations with Drizzle Kit:

```bash
# Install drizzle-kit
npm install -D drizzle-kit

# Generate migration
npx drizzle-kit generate

# Apply to D1 (local)
wrangler d1 execute DB --local --file=./drizzle/0000_initial.sql

# Apply to D1 (remote)
wrangler d1 execute DB --remote --file=./drizzle/0000_initial.sql
```

**drizzle.config.ts**:

```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./lib/schema/d1.ts",
  out: "./drizzle",
  dialect: "sqlite",  // or "postgresql"
});
```

## Prisma ORM

Prisma provides a type-safe database client with migrations and schema management.

### Prisma Setup for OpenNext

**1. Install Prisma**:

```bash
npm install @prisma/client
npm install -D prisma @prisma/adapter-d1
```

**2. Configure next.config.ts**:

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: [
    "@prisma/client",
    ".prisma/client"
  ],
};

export default nextConfig;
```

**Why needed**: Ensures Prisma client works with Workers runtime.

**3. Configure schema.prisma**:

```prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
  // DO NOT set output directory - OpenNext patches the client
}

datasource db {
  provider = "sqlite"  // or "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  posts     Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  userId    Int
  title     String
  content   String
  published Boolean  @default(false)
  user      User     @relation(fields: [userId], references: [id])
}
```

**Important**: Do NOT set `output` in generator. OpenNext must patch the client.

### D1 with Prisma

```typescript
// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { cache } from "react";
import { PrismaClient } from "@prisma/client";
import { PrismaD1 } from "@prisma/adapter-d1";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  const adapter = new PrismaD1(env.DB);
  return new PrismaClient({ adapter });
});

// For SSG routes
export const getDbAsync = async () => {
  const { env } = await getCloudflareContext({ async: true });
  const adapter = new PrismaD1(env.DB);
  return new PrismaClient({ adapter });
};
```

**Usage**:

```typescript
// app/api/users/route.ts
import { getDb } from "@/lib/db";

export async function GET() {
  const prisma = getDb();
  const users = await prisma.user.findMany({
    include: { posts: true }
  });
  return Response.json(users);
}

export async function POST(request: Request) {
  const prisma = getDb();
  const body = await request.json();
  
  const user = await prisma.user.create({
    data: {
      name: body.name,
      email: body.email,
    }
  });
  
  return Response.json(user);
}
```

### PostgreSQL with Prisma

```typescript
// lib/db.ts
import { cache } from "react";
import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

export const getDb = cache(() => {
  const connectionString = process.env.DATABASE_URL ?? "";
  const adapter = new PrismaPg({
    connectionString,
    maxUses: 1,  // CRITICAL: Don't reuse connections
  });
  return new PrismaClient({ adapter });
});
```

**Schema** (same as above, but with `provider = "postgresql"`):

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Hyperdrive with Prisma

```typescript
// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { cache } from "react";
import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  const connectionString = env.HYPERDRIVE.connectionString;
  const adapter = new PrismaPg({
    connectionString,
    maxUses: 1,
  });
  return new PrismaClient({ adapter });
});

// For SSG routes
export const getDbAsync = async () => {
  const { env } = await getCloudflareContext({ async: true });
  const connectionString = env.HYPERDRIVE.connectionString;
  const adapter = new PrismaPg({
    connectionString,
    maxUses: 1,
  });
  return new PrismaClient({ adapter });
};
```

### Prisma Migrations

Generate and apply migrations:

```bash
# Generate migration
npx prisma migrate dev --name init

# Apply to D1 (extract SQL from migration)
# Prisma generates migrations in prisma/migrations/

# For D1, manually apply:
wrangler d1 execute DB --local --file=prisma/migrations/20240101000000_init/migration.sql
wrangler d1 execute DB --remote --file=prisma/migrations/20240101000000_init/migration.sql
```

### Prisma with Transactions

```typescript
import { getDb } from "@/lib/db";

export async function POST(request: Request) {
  const prisma = getDb();
  const body = await request.json();
  
  // Transaction with Prisma
  const user = await prisma.$transaction(async (tx) => {
    const newUser = await tx.user.create({
      data: {
        name: body.name,
        email: body.email,
      }
    });
    
    await tx.account.create({
      data: {
        userId: newUser.id,
        balance: 0,
      }
    });
    
    return newUser;
  });
  
  return Response.json(user);
}
```

## Common Patterns

### React cache() Helper

Both Drizzle and Prisma examples use React's `cache()`:

```typescript
import { cache } from "react";

export const getDb = cache(() => {
  // Create client
});
```

**Why**:
- Deduplicates client creation within the same request
- Server Components render multiple times
- `cache()` ensures only one client per request

**Only works in Server Components**. For Route Handlers and API routes, the client is created per-call anyway.

### SSG Routes (Async Context)

For Static Site Generation routes, use async context:

```typescript
// In generateStaticParams or similar
export const getDbAsync = async () => {
  const { env } = await getCloudflareContext({ async: true });
  // Create client with env
};

// Usage
export async function generateStaticParams() {
  const db = await getDbAsync();
  const products = await db.select().from(productsTable);
  
  return products.map(p => ({
    slug: p.slug,
  }));
}
```

**Warning**: During SSG, local binding values and `.dev.vars` secrets are included in the build.

### Connection Pooling

**Never use global pools**:

```typescript
// ❌ WRONG - Global pool
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export default {
  async fetch() {
    const db = drizzle({ client: pool });
    // ...
  }
};
```

**Always create per-request with `maxUses: 1`**:

```typescript
// ✅ CORRECT - Per-request pool
export const getDb = cache(() => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    maxUses: 1,
  });
  return drizzle({ client: pool });
});
```

### Query Optimization

Use Drizzle or Prisma's query builders for optimized queries:

```typescript
// Drizzle - Select specific fields
const users = await db
  .select({
    id: usersTable.id,
    name: usersTable.name,
  })
  .from(usersTable)
  .where(eq(usersTable.active, true))
  .limit(10);

// Prisma - Select specific fields
const users = await prisma.user.findMany({
  where: { active: true },
  select: { id: true, name: true },
  take: 10,
});
```

### Error Handling

```typescript
import { getDb } from "@/lib/db";

export async function GET() {
  try {
    const db = getDb();
    const users = await db.select().from(usersTable);
    return Response.json(users);
  } catch (error) {
    console.error("Database error:", error);
    return Response.json(
      { error: "Failed to fetch users" },
      { status: 500 }
    );
  }
}
```

## Database Choice Guide

### D1 (Cloudflare's SQLite)

**Use when**:
- Built-in to Cloudflare
- SQLite features sufficient
- Low latency within Cloudflare
- No external database needed

**Limits**:
- 10 GB per database
- 5 million reads/day (free), 25 million (paid)
- 100k writes/day (free), 5 million (paid)

### PostgreSQL with Hyperdrive

**Use when**:
- Need PostgreSQL features
- Existing PostgreSQL database
- Complex queries and relationships
- Want connection pooling

**Benefits**:
- Hyperdrive provides connection pooling
- Caching for performance
- Regional database support

### Direct PostgreSQL (without Hyperdrive)

**Use when**:
- Very simple queries
- Low request volume
- Already have connection pooling

**Caution**: Direct connections from Workers can be slow. Hyperdrive is recommended.

## Troubleshooting

### "Cannot perform I/O on behalf of a different request"

**Cause**: Global database client reusing connections.

**Fix**: Create client per-request with `maxUses: 1`:

```typescript
// ✅ Correct
export const getDb = cache(() => {
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    maxUses: 1,
  });
  return drizzle({ client: pool });
});
```

### Prisma Client Not Found

**Cause**: Prisma client not externalized.

**Fix**: Add to next.config.ts:

```typescript
{
  serverExternalPackages: ["@prisma/client", ".prisma/client"]
}
```

### Prisma Output Directory Issues

**Cause**: Custom output directory in schema.prisma.

**Fix**: Remove `output` from generator:

```prisma
generator client {
  provider = "prisma-client-js"
  // Do NOT set output
}
```

### D1 Migrations Not Applied

**Cause**: Migrations not run against D1 database.

**Fix**: Apply migrations:

```bash
# Drizzle
wrangler d1 execute DB --remote --file=./drizzle/0000_initial.sql

# Prisma (manually extract SQL)
wrangler d1 execute DB --remote --file=./prisma/migrations/.../migration.sql
```

## Best Practices

1. **Always use `cache()` for request-scoped clients**
2. **Set `maxUses: 1` for PostgreSQL pools**
3. **Never create global database clients**
4. **Use async context for SSG routes**
5. **Externalize Prisma client in next.config.ts**
6. **Don't set output directory in Prisma schema**
7. **Handle database errors gracefully**
8. **Use Hyperdrive for PostgreSQL when possible**
9. **Optimize queries with select specific fields**
10. **Test database connections in preview before deploy**

## Complete Examples

### Complete Drizzle + D1 Setup

```typescript
// lib/schema/d1.ts
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
});

// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { drizzle } from "drizzle-orm/d1";
import { cache } from "react";
import * as schema from "./schema/d1";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  return drizzle(env.DB, { schema });
});

// app/api/users/route.ts
import { getDb } from "@/lib/db";
import { users } from "@/lib/schema/d1";

export async function GET() {
  const db = getDb();
  const allUsers = await db.select().from(users);
  return Response.json(allUsers);
}
```

### Complete Prisma + Hyperdrive Setup

```typescript
// prisma/schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id    Int    @id @default(autoincrement())
  name  String
  email String @unique
}

// lib/db.ts
import { getCloudflareContext } from "@opennextjs/cloudflare";
import { cache } from "react";
import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";

export const getDb = cache(() => {
  const { env } = getCloudflareContext();
  const adapter = new PrismaPg({
    connectionString: env.HYPERDRIVE.connectionString,
    maxUses: 1,
  });
  return new PrismaClient({ adapter });
});

// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["@prisma/client", ".prisma/client"],
};

export default nextConfig;

// app/api/users/route.ts
import { getDb } from "@/lib/db";

export async function GET() {
  const prisma = getDb();
  const users = await prisma.user.findMany();
  return Response.json(users);
}
```

## Related Documentation

- [../SKILL.md](../SKILL.md) - Main OpenNext skill overview
- [configuration.md](configuration.md) - wrangler.jsonc and environment setup
- [caching.md](caching.md) - ISR and SSG caching strategies
- [troubleshooting.md](troubleshooting.md) - Common issues and fixes
