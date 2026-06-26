---
title: Split unique constraints in PostgreSQL
impact: HIGH
impactDescription: Prevents blocking reads and writes during constraint creation
tags: postgresql, prisma, supabase, drizzle, migrations, constraints
---

When adding unique constraints in PostgreSQL, create the unique index concurrently first before adding the constraint to avoid blocking reads and writes.

Bad:

```sql
-- Creates a unique constraint directly, which blocks reads and writes
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);
```

Good:

```sql
-- First create a unique index concurrently (non-blocking)
CREATE UNIQUE INDEX CONCURRENTLY users_email_unique_idx ON users (email);

-- Then add the constraint using the existing index
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE USING INDEX users_email_unique_idx;
```
