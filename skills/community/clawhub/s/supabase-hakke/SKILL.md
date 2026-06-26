---
name: supabase-hakke
description: Supabase integration for Hakke Studio projects. Auth, database, storage, edge functions. Use with vercel skill for full-stack deployment.
metadata:
  version: "1.1.0"
  author: "Bastian Berrios (SAURON)"
  requires: ["vercel"]
  tools: ["exec"]
  philosophy: "Type-safe, RLS-first, production-ready"
  tags: ["hakke", "supabase", "nextjs", "saas", "multi-tenant"]
---

# Supabase for Hakke Studio

Supabase integration específica para proyectos de Hakke Studio.

## Proyectos Actuales

| Proyecto | Supabase URL | Uso |
|----------|--------------|-----|
| **hakke-app** | `https://[project].supabase.co` | SaaS multi-tenant |

## CLI Installation

```bash
# Supabase CLI (ya instalado)
supabase --version

# Si no está instalado
npm install -g supabase
```

## Authentication

### Login to Supabase

```bash
supabase login
```

This opens browser for OAuth login with `contacto@hakke.cl`.

### Link Project

```bash
cd /home/bastianberrios/proyectos/HAKKE/hakke-app
supabase link --project-ref <project-id>
```

---

## Database Operations

### Generate Types

```bash
supabase gen types typescript --local > lib/supabase/database.types.ts
```

### Create Migration

```bash
supabase migration new <migration_name>
```

### Apply Migration

```bash
supabase db push
```

### Reset Database (DEV ONLY)

```bash
supabase db reset
```

---

## Auth Operations

### Get API Keys

```bash
supabase status
```

Returns:
- `anon key` - Public key (client-side)
- `service_role key` - Secret key (server-side ONLY)

### Create User (Admin)

```sql
-- In Supabase Dashboard SQL Editor
INSERT INTO auth.users (email, encrypted_password, email_confirmed_at)
VALUES (
  'user@example.com',
  crypt('password123', gen_salt('bf')),
  NOW()
);
```

---

## RLS (Row Level Security)

### Enable RLS

```sql
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
```

### Create Policy

```sql
-- Users can only see their own data
CREATE POLICY "Users can view own data"
ON users
FOR SELECT
USING (auth.uid() = id);

-- Users can update own data
CREATE POLICY "Users can update own data"
ON users
FOR UPDATE
USING (auth.uid() = id);
```

---

## Storage Operations

### Create Bucket

```sql
-- In Supabase Dashboard SQL Editor
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', false);
```

### Storage Policy

```sql
-- Users can upload to own folder
CREATE POLICY "Users can upload avatars"
ON storage.objects
FOR INSERT
WITH CHECK (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);
```

---

## Edge Functions

### Create Function

```bash
supabase functions new <function-name>
```

### Deploy Function

```bash
supabase functions deploy <function-name>
```

### Invoke Function

```bash
curl -i -L --request POST 'https://<project>.supabase.co/functions/v1/<function-name>' \
  --header 'Authorization: Bearer <anon-key>' \
  --header 'Content-Type: application/json' \
  --data '{"name":"Functions"}'
```

---

## Multi-Tenant SaaS (hakke-app)

### Architecture

```
┌─────────────────────────────────────────┐
│           hakke-app (SaaS)              │
├─────────────────────────────────────────┤
│  tenants table (multi-tenant)           │
│  - id, slug, name, plan                 │
│  - owner_id (FK → auth.users)           │
│  - subscription_status                  │
├─────────────────────────────────────────┤
│  Row Level Security (RLS)               │
│  - tenant_id = current_tenant()         │
└─────────────────────────────────────────┘
```

### Tenant Isolation

```sql
-- Function to get current tenant
CREATE OR REPLACE FUNCTION current_tenant_id()
RETURNS uuid AS $$
BEGIN
  RETURN (auth.jwt()->>'tenant_id')::uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- RLS Policy example
CREATE POLICY "Users can only see own tenant data"
ON appointments
FOR ALL
USING (tenant_id = current_tenant_id());
```

### Subscription Management

```sql
-- Check subscription status
CREATE OR REPLACE FUNCTION has_active_subscription()
RETURNS boolean AS $$
DECLARE
  tenant_record tenants%ROWTYPE;
BEGIN
  SELECT * INTO tenant_record
  FROM tenants
  WHERE id = current_tenant_id();
  
  RETURN tenant_record.subscription_status = 'active';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

---

## Common Queries

### List Tables

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

### Describe Table

```sql
SELECT
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'users';
```

### Check RLS

```sql
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
```

---

## Environment Variables

### .env.local

```bash
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
```

### .env.example (commit to git)

```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
```

---

## Client Setup

### Server Client (Next.js)

```typescript
// lib/supabase/server.ts
import { createClient } from '@supabase/supabase-js';
import { cookies } from 'next/headers';

export function createServerClient() {
  const cookieStore = cookies();
  
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      auth: {
        persistSession: false,
      },
    }
  );
}
```

### Browser Client (Next.js)

```typescript
// lib/supabase/client.ts
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

---

## Troubleshooting

### Connection Issues

```bash
# Check if Supabase is accessible
curl -I https://<project>.supabase.co/rest/v1/

# Expected: 401 Unauthorized (means API is working, just need auth)
```

### RLS Not Working

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Check policies
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE schemaname = 'public';
```

### Auth Issues

```bash
# Check if user exists
supabase auth list

# Check logs
supabase logs auth
```

---

## Integration with Vercel

### Deploy with Vercel

```bash
# In hakke-app directory
vercel

# Add env vars in Vercel Dashboard or CLI
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add SUPABASE_SERVICE_ROLE_KEY
```

---

## Best Practices

| Practice | Why |
|----------|-----|
| **RLS always on** | Security first |
| **Service key server-only** | Never expose to client |
| **Type generation** | Type-safe queries |
| **Migrations in git** | Reproducible DB |
| **Separate anon/service keys** | Principle of least privilege |

---

## Resources

- Docs: https://supabase.com/docs
- Dashboard: https://supabase.com/dashboard
- CLI Reference: https://supabase.com/docs/reference/cli
- SQL Editor: Dashboard → SQL Editor
- Logs: Dashboard → Logs

---

*Supabase Hakke v1.1.0 - Production-ready for Hakke Studio*
