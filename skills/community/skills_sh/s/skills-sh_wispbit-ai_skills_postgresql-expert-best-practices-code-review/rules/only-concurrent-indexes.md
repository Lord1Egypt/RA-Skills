---
title: Only concurrent indexes in PostgreSQL
impact: CRITICAL
impactDescription: Prevents blocking writes during index creation on production tables
tags: postgresql, prisma, supabase, drizzle, migrations, indexes
---

When creating indexes in PostgreSQL, always use the `CONCURRENTLY` option to prevent blocking writes during index creation.

Bad:

```sql
CREATE INDEX idx_users_email ON users(email);
```

Good:

```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```
