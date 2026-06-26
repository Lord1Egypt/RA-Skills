---
title: Add indexes for foreign keys in PostgreSQL
impact: HIGH
impactDescription: Improves query performance and prevents slow lookups on foreign keys
tags: postgresql, prisma, supabase, drizzle, migrations, indexes, foreign-keys
---

When adding a foreign key constraint in PostgreSQL, always add a corresponding index.

Bad:

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user_id
FOREIGN KEY (user_id) REFERENCES users(id);
```

Good:

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user_id
FOREIGN KEY (user_id) REFERENCES users(id);
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id);
```
