# Schema and RLS Guidance

Use this reference when designing tables or reviewing Supabase Row Level Security. Prefer the user's migration framework or database client for project migrations. For old-skill compatibility, `scripts/supabase_dataplane.py` can execute SQL through the Supabase REST `/pg/query` endpoint.

## Schema Defaults

- Table and column names: `snake_case`
- Primary key: `id bigserial primary key` or `id uuid primary key default gen_random_uuid()`
- Timestamps: prefer `timestamptz`
- JSON: prefer `jsonb`
- Index names: `ix_<table>_<column>`
- Unique constraint names: `uq_<table>_<column>`

Safe additive changes:

```sql
alter table public.posts add column if not exists tags text[];
alter table public.posts add column if not exists view_count integer not null default 0;
create index if not exists ix_posts_created_at on public.posts(created_at desc);
```

Risky changes that need explicit review:

- Dropping columns or tables
- Changing column types
- Shortening string length
- Adding non-null columns without defaults
- Adding unique constraints when existing data may conflict

## RLS Rules

Enable RLS for every table that is reachable through Supabase APIs:

```sql
alter table public.posts enable row level security;
```

Common policy shapes:

```sql
create policy "posts_allow_public_read" on public.posts
  for select using (true);

create policy "posts_auth_insert" on public.posts
  for insert with check (auth.role() = 'authenticated');
```

For user-owned rows:

```sql
alter table public.notes add column if not exists user_id uuid not null default auth.uid();

create policy "notes_owner_select" on public.notes
  for select using (auth.uid() = user_id);

create policy "notes_owner_insert" on public.notes
  for insert with check (auth.uid() = user_id);
```

Check current RLS state:

```sql
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public'
order by tablename;
```

Run a check through the preserved data-plane command when needed:

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query "select schemaname, tablename, rowsecurity from pg_tables where schemaname = 'public' order by tablename"
```
