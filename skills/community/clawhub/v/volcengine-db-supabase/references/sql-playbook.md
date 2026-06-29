# SQL Playbook

Use this reference for common SQL inspection, CRUD, migration, pgvector, RLS, and RPC snippets. Execute through the preserved data-plane command when a direct SQL path is needed:

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query "select 1"
```

For larger SQL files:

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query-file ./query.sql
```

## Inspect Schema

List tables:

```bash
python3 scripts/supabase_dataplane.py list-tables --workspace-id ws-xxxx --schemas public,auth
```

Column details:

```sql
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema = 'public' and table_name = 'posts'
order by ordinal_position;
```

Indexes:

```sql
select indexname, indexdef
from pg_indexes
where schemaname = 'public' and tablename = 'posts';
```

Foreign keys:

```sql
select conname, conrelid::regclass, confrelid::regclass, pg_get_constraintdef(oid)
from pg_constraint
where contype = 'f' and connamespace = 'public'::regnamespace;
```

## CRUD

```sql
select * from public.posts order by created_at desc limit 20;

insert into public.posts (title, content, published)
values ('hello', 'first post', false)
returning *;

update public.posts
set published = true, updated_at = now()
where id = 1
returning *;

delete from public.posts
where id = 1;
```

## Migrations

Apply reviewed SQL as a tracked migration:

```bash
python3 scripts/supabase_dataplane.py apply-migration --workspace-id ws-xxxx --name create_posts --query-file ./migrations/001_create_posts.sql
```

List migration records:

```bash
python3 scripts/supabase_dataplane.py list-migrations --workspace-id ws-xxxx
```

The compatibility migration wrapper writes to `supabase_migrations.schema_migrations`, matching the old skill behavior.

## RLS Checks

```sql
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public'
order by tablename;
```

Enable RLS and add a public-read policy:

```sql
alter table public.posts enable row level security;

create policy "posts_allow_public_read" on public.posts
  for select using (true);
```

User-owned row pattern:

```sql
alter table public.notes add column if not exists user_id uuid not null default auth.uid();

create policy "notes_owner_select" on public.notes
  for select using (auth.uid() = user_id);

create policy "notes_owner_insert" on public.notes
  for insert with check (auth.uid() = user_id);
```

## pgvector

```sql
create extension if not exists vector;

create table if not exists public.documents (
  id bigserial primary key,
  content text not null,
  metadata jsonb,
  embedding vector(1536),
  created_at timestamptz not null default now()
);

create index if not exists ix_documents_embedding on public.documents
  using hnsw (embedding vector_cosine_ops);
```

Check installed extensions:

```bash
python3 scripts/supabase_dataplane.py list-extensions --workspace-id ws-xxxx
```

## TypeScript Types

Generate Supabase-style table types from `information_schema.columns`:

```bash
python3 scripts/supabase_dataplane.py generate-typescript-types --workspace-id ws-xxxx --schemas public
```
