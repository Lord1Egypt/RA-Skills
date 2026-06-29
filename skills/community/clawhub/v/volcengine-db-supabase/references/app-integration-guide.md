# Application Integration

Use this reference when the user needs to wire an application to a Volcengine Supabase workspace. It describes application-side patterns only; resource management should still go through `ve aidap`.

## Collect Connection Values

Use the control plane to fetch endpoint and key metadata:

```bash
ve aidap DescribeComputes --WorkspaceId ws-xxxx --BranchId br-xxxx
ve aidap DescribeWorkspaceEndpoint --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx
ve aidap DescribeAPIKeys --WorkspaceId ws-xxxx --BranchId br-xxxx
ve aidap DescribeDBAccountConnection --WorkspaceId ws-xxxx --BranchId br-xxxx --ComputeId cp-xxxx --DatabaseName appdb --AccountName app
```

For PostgreSQL workspaces, resolve the primary database `ComputeId` first and include it in endpoint and account-connection reads. Calls with only `BranchId` can fail with `InvalidParameter`.

Map the returned values into runtime configuration:

```bash
SUPABASE_URL=<workspace-api-url>
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
DATABASE_URL=<postgres-connection-url>
```

`SUPABASE_SERVICE_ROLE_KEY` and `DATABASE_URL` are backend secrets. Never expose them to frontend bundles, logs, or final summaries. If you need to hand off `DATABASE_URL`, write it to a local env file with mode `600` and report only the path.

## TypeScript Client

```bash
npm install @supabase/supabase-js
```

```typescript
import { createClient } from "@supabase/supabase-js";

export function getSupabaseClient(userToken?: string) {
  const url = process.env.SUPABASE_URL!;
  const key = process.env.SUPABASE_ANON_KEY!;
  return createClient(url, key, {
    global: userToken ? { headers: { Authorization: `Bearer ${userToken}` } } : undefined,
    auth: { autoRefreshToken: false, persistSession: false },
  });
}
```

## Python Client

```bash
pip install supabase
```

```python
import os
from supabase import create_client


def get_supabase_client():
    return create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_ANON_KEY"])
```

## Migrations and Direct SQL

Prefer the application's migration tool or a direct PostgreSQL client pointed at `DATABASE_URL` for project-owned migrations.

Examples:

```bash
umask 077
printf 'DATABASE_URL=%q\n' "$DATABASE_URL" > .aidap/ws-xxxx-postgres.env
psql "$DATABASE_URL" -f migrations/001_init.sql
psql "$DATABASE_URL" -Atc "select 1"
npx prisma migrate deploy
npx supabase db push --db-url "$DATABASE_URL"
```

For compatibility with the imported old skill, this skill also provides the old REST data-plane actions:

```bash
python3 scripts/supabase_dataplane.py execute-sql --workspace-id ws-xxxx --query "select 1"
python3 scripts/supabase_dataplane.py apply-migration --workspace-id ws-xxxx --name init --query-file migrations/001_init.sql
python3 scripts/supabase_dataplane.py generate-typescript-types --workspace-id ws-xxxx --schemas public
```

Before running migrations, confirm the target workspace, branch, database, and account.

## Storage and Edge Functions

The old skill managed Supabase Storage and Edge Functions through the Supabase REST API. Those actions are preserved in `scripts/supabase_dataplane.py`:

```bash
python3 scripts/supabase_dataplane.py create-storage-bucket --workspace-id ws-xxxx --bucket-name uploads --public
python3 scripts/supabase_dataplane.py list-storage-buckets --workspace-id ws-xxxx
python3 scripts/supabase_dataplane.py deploy-edge-function --workspace-id ws-xxxx --function-name hello --source-file ./index.ts
python3 scripts/supabase_dataplane.py list-edge-functions --workspace-id ws-xxxx
```

For application file operations, keep using the Supabase SDK with `SUPABASE_URL` and `SUPABASE_ANON_KEY` or backend-only service credentials.
