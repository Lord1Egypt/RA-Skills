# Local Development

Local development should not depend on GitHub, Vercel, or Supabase cloud preview branches.

## Expected Workflow

```bash
supabase start
supabase db reset
npm run dev:local
```

This runs the app against local Docker Supabase.

## What `dev:local` Should Do

`dev:local` should:

1. Read local Supabase credentials from `supabase status -o json`.
2. Update only the Supabase env keys in `.env.local`.
3. Preserve all unrelated `.env.local` values.
4. Start the local dev server.

Typical package scripts:

```json
{
  "dev:local": "tsx scripts/supabase/use-branch-env.ts local && next dev",
  "env:local": "tsx scripts/supabase/use-branch-env.ts local"
}
```

## Keys The Helper May Update

```text
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
```

If the target project uses different names, update `branching-config.json`.

## Authoring Migrations

To generate a migration from local schema changes made in Studio or SQL:

```bash
npm run db:diff
```

To pull remote schema into committed migrations and regenerate types:

```bash
npm run db:pull
```

## Migration Testing

Before pushing a branch with database changes:

```bash
supabase db reset
npm run db:types
npm run dev:local
```

Use local Supabase to catch migration ordering, seed, generated type, and auth/storage assumptions before creating a shared preview database.

## Limitations

- Google OAuth may not work locally unless local callback URLs are configured.
- Webhooks from external services usually need a tunnel.
- Local data is disposable unless backed up.
- Local Auth users are separate from cloud Auth users.

