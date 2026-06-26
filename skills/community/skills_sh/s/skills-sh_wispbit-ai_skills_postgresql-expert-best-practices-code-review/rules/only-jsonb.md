---
title: Always use JSONB in PostgreSQL
impact: MEDIUM
impactDescription: Enables indexing and efficient querying of JSON data
tags: postgresql, prisma, supabase, drizzle, migrations, data-types
---

Always use `jsonb` instead of `json` data type when creating columns in PostgreSQL databases.

Bad:

```sql
ALTER TABLE users
ADD COLUMN properties json;
```

Good:

```sql
ALTER TABLE users
ADD COLUMN properties jsonb;
```
