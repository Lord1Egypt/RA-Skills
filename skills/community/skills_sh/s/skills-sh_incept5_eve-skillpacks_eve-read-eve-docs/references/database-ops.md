# Database Operations

## Use When
- You need to provision, inspect, or manage environment databases.
- You need to run migrations, SQL queries, or schema inspections.
- You need managed DB status, credential rotation, or scaling.
- You need to set up RLS policies with group-aware helpers.

## Load Next
- `references/manifest.md` for managed DB declaration in `x-eve.role: managed_db`.
- `references/deploy-debug.md` for environment-level diagnostics.
- `references/secrets-auth.md` for DB credential secrets and interpolation.

## Ask If Missing
- Confirm the environment name and project context.
- Confirm access mode: `--env` (API-proxied) or `--url` (direct connection).
- Confirm whether this is a managed DB or a self-hosted database.

## Managed DB Provisioning

Declare a managed database in the manifest:

```yaml
services:
  db:
    x-eve:
      role: managed_db
      managed:
        class: db.p1
        engine: postgres
        engine_version: "16"
        extensions: [postgis, pgvector, pg_trgm]
```

Provisioning occurs automatically when an environment is deployed. Managed DB services are not rendered into K8s manifests.

### Managed Extensions

Plain declarable extensions are `postgis`, `pgvector`, `pg_trgm`, `btree_gist`, `hstore`, and `citext`.

```bash
eve db extensions list --env <name> [--project <id>]
```

Notes:
- Eve installs declared extensions through the managed-DB reconciler as the backing instance admin, before app migration jobs run.
- `pgvector` is the manifest name; PostgreSQL reports the installed extension as `vector`.
- Removing an extension from the manifest does not drop it from an existing DB. Extension removal is sticky in v1.
- `pg_cron` is provider-gated: it is declarable only when the platform sets `EVE_MANAGED_DB_ENABLED_PRELOAD_EXTENSIONS=pg_cron` and the backing Postgres has `shared_preload_libraries=pg_cron`.
- `pg_cron` follows the AWS RDS model: Eve installs it in the instance admin database (`postgres`) and tenant DB scheduling is a platform-admin operation.
- `timescaledb` is still not declarable on AWS RDS; it needs a Timescale-capable provider model first.

### Tiers

| Class | Description |
|---|---|
| `db.p1` | Starter (shared resources) |
| `db.p2` | Standard (dedicated CPU) |
| `db.p3` | Performance (dedicated CPU + memory) |

### Interpolation

Reference managed DB values in environment blocks:

```yaml
environment:
  DATABASE_URL: ${managed.db.url}
  DB_HOST: ${managed.db.host}
  DB_PASSWORD: ${managed.db.password}
```

Available fields: `url`, `host`, `port`, `database`, `username`, `password`.

## TLS Trust (Managed DB)

Cloud managed DB tenant URLs default to `sslmode=verify-full`. The platform owns CA distribution: when the worker deploys an environment that uses a cloud managed DB, it creates a namespace `ConfigMap/eve-db-trust`, mounts the provider CA bundle at `/etc/eve/trust/ca-bundle.pem`, and injects `NODE_EXTRA_CA_CERTS` and `PGSSLROOTCERT` into every app pod and job pod.

What this means for app code:

- **Do not** set `ssl: { rejectUnauthorized: false }` on your DB client. The pod already trusts the managed DB CA.
- **Do not** strip `sslmode` from `${managed.db.url}`. Connect with the URL as-is.
- A plain `new Pool({ connectionString: process.env.DATABASE_URL })` is the supported pattern.
- Local managed DBs continue to use `sslmode=disable` and need no trust material.
- Migration jobs (`x-eve.role: job`) get the same trust injection as long-lived Deployments — migrations against a `verify-full` tenant work without app changes.

The previous URL-rewriting `sslmode` resolver was removed; tenant URLs are preserved as-is and inherit `sslmode` from `DATABASE_URL`. If a managed DB connection fails TLS verification, treat it as a platform issue (`eve job logs` on the deploy job will show the trust ConfigMap step) rather than working around it in app code.

## Status + Credential Rotation

```bash
eve db status --env <name>                          # Managed DB status and tenant readiness
eve db rotate-credentials --env <name>              # Rotate managed DB credentials
eve db extensions list --env <name>                 # List installed DB extensions
```

Always check `eve db status` before relying on managed values. Rotation replaces credentials and updates the stored secret -- redeploy services to pick up new values.

## Migrations

### Create a Migration

```bash
eve db new <description> [--path db/migrations]
```

Creates `YYYYMMDDHHmmss_description.sql` in `db/migrations/` (default).

### Run Migrations

```bash
eve db migrate --env <name> [--path db/migrations]          # API-proxied
eve db migrate --url <postgres-url> [--path db/migrations]  # Direct connection
```

### List Applied

```bash
eve db migrations --env <name>
```

### Conventions

- Migration files: `YYYYMMDDHHmmss_description.sql` format.
- Default path: `db/migrations/` relative to project root.
- Migrations run sequentially by timestamp.
- Use `--url` mode with `@eve/migrate` library for direct operations.
- `EVE_DB_URL` env var (or `.env` file) is fallback for `sql` and `migrate`.

### Pipeline Step

The migrate step must run **after deploy** — the managed DB is provisioned during deploy and does not exist before then. Use `action.type: job` referencing the `migrate` service:

```yaml
pipelines:
  deploy:
    steps:
      - name: build
        action: { type: build }
      - name: release
        depends_on: [build]
        action: { type: release }
      - name: deploy
        depends_on: [release]
        action: { type: deploy }
      - name: migrate
        depends_on: [deploy]
        action: { type: job, service: migrate }
```

**Common mistake**: Running `migrate` before `deploy`. This will fail because the managed DB doesn't exist until the first deploy provisions it.

### Complete Working Example (based on eden)

A fully working manifest with managed DB, migrations, and pipeline — copy and adapt:

```yaml
name: my-app
schema: eve/compose/v2
registry: "eve"

services:
  api:
    build:
      context: ./apps/api
      dockerfile: ./apps/api/Dockerfile
    ports: [3000]
    environment:
      NODE_ENV: production
      DATABASE_URL: ${managed.db.url}

  migrate:
    image: public.ecr.aws/w7c4v0w3/eve-horizon/migrate:latest
    environment:
      DATABASE_URL: ${managed.db.url}
      MIGRATIONS_DIR: /migrations
    x-eve:
      role: job
      files:
        - source: db/migrations
          target: /migrations

  db:
    x-eve:
      role: managed_db
      managed:
        class: db.p1
        engine: postgres
        engine_version: "16"

environments:
  sandbox:
    pipeline: deploy

pipelines:
  deploy:
    steps:
      - name: build
        action: { type: build }
      - name: release
        depends_on: [build]
        action: { type: release }
      - name: deploy
        depends_on: [release]
        action: { type: deploy }
      - name: migrate
        depends_on: [deploy]
        action: { type: job, service: migrate }
```

Local docker-compose.yml for parity:

```yaml
services:
  db:
    image: postgres:16-alpine
    ports: ["5432:5432"]
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

  migrate:
    image: ghcr.io/eve-horizon/eve-migrate:latest
    environment:
      DATABASE_URL: postgres://app:app@db:5432/myapp
    volumes:
      - ./db/migrations:/migrations:ro
    depends_on:
      db: { condition: service_healthy }

volumes:
  pgdata:
```

First migration file (`db/migrations/20260312000000_initial_schema.sql`):

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE items (
  id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id     TEXT        NOT NULL,
  name       TEXT        NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER trg_items_updated_at
  BEFORE UPDATE ON items
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE items ENABLE ROW LEVEL SECURITY;

CREATE POLICY items_org_isolation ON items
  USING (org_id = current_setting('app.org_id', true))
  WITH CHECK (org_id = current_setting('app.org_id', true));
```

Create new migrations with `eve db new <description>`, then apply with `docker compose run --rm migrate` locally or let the pipeline handle it on deploy.

## Schema Inspection + RLS

```bash
eve db schema --env <name> [--project <id>]         # Show DB schema
eve db schema --url <postgres-url>                  # Direct connection

eve db rls --env <name>                             # RLS policies + group context diagnostics
eve db rls init --with-groups [--out <path>] [--force]  # Scaffold group-aware RLS helpers
```

`rls` shows resolved principal, org, project, env, group IDs, and permissions for the current session. Useful for debugging why RLS policies are not matching.

`rls init --with-groups` scaffolds these SQL functions to `db/rls/helpers.sql`:
- `app.current_user_id()`
- `app.current_group_ids()`
- `app.has_group()`

Apply the output SQL to your target DB, then reference helpers in RLS policies.

## SQL Access

```bash
eve db sql --env <name> --sql "SELECT count(*) FROM users"         # Read-only (default)
eve db sql --env <name> --sql "UPDATE users SET active = true" --write  # Mutations
eve db sql --env <name> --file ./query.sql                         # From file
eve db sql --env <name> --sql "SELECT * FROM users WHERE id = $1" \
  --params '["user_abc"]'                                          # Parameterized
eve db sql --url <postgres-url> --sql "SELECT 1"                   # Direct connection
```

| Access Mode | Flag | Default |
|---|---|---|
| Read-only | (none) | Yes |
| Read-write | `--write` | No |
| Parameterized | `--params '["arg"]'` | No |
| From file | `--file <path>` | No |
| Direct | `--url <postgres-url>` | No |

Both `--env` (API-proxied) and `--url` (direct) modes are supported for all `sql` operations.

## Scaling, Reset, Wipe, Destroy

```bash
eve db scale --env <name> --class db.p2             # Scale to higher tier
eve db reset --env <name> --force [--no-migrate]    # Drop + recreate schema, re-apply migrations
eve db reset --env <name> --force --danger-reset-production  # Required for production envs
eve db wipe --env <name> --force                    # Reset schema WITHOUT re-applying migrations
eve db destroy --env <name> --force                 # Destroy managed DB entirely
```

- `reset` drops all schemas except `pg_catalog` and `information_schema`, then re-applies migrations.
- `--no-migrate` (or use `wipe`) skips migration re-apply after schema drop.
- `--danger-reset-production` is required when resetting production environments via the API.
- `destroy` is irreversible -- removes the managed tenant entirely.

## Admin APIs

| Endpoint | Method | Purpose |
|---|---|---|
| `/admin/managed-db/instances` | GET | List all managed DB instances |
| `/admin/managed-db/instances` | POST | Register a new instance |
| `/admin/managed-db/instances/:id` | GET | Instance details |
| `/projects/:id/envs/:env/db/managed` | GET | Tenant status |
| `/projects/:id/envs/:env/db/managed/rotate` | POST | Rotate credentials |
| `/projects/:id/envs/:env/db/managed/scale` | POST | Scale tier |
| `/projects/:id/envs/:env/db/managed` | DELETE | Destroy tenant |

## CLI Quick Reference

| Intent | Command |
|---|---|
| Check managed DB readiness | `eve db status --env <name>` |
| List installed extensions | `eve db extensions list --env <name>` |
| View schema | `eve db schema --env <name>` |
| Run read-only query | `eve db sql --env <name> --sql "..."` |
| Run mutation | `eve db sql --env <name> --sql "..." --write` |
| Create migration | `eve db new <description>` |
| Apply migrations | `eve db migrate --env <name>` |
| List applied migrations | `eve db migrations --env <name>` |
| Inspect RLS policies | `eve db rls --env <name>` |
| Scaffold RLS helpers | `eve db rls init --with-groups` |
| Rotate credentials | `eve db rotate-credentials --env <name>` |
| Scale tier | `eve db scale --env <name> --class db.p2` |
| Reset schema | `eve db reset --env <name> --force` |
| Wipe without remigrate | `eve db wipe --env <name> --force` |
| Destroy managed DB | `eve db destroy --env <name> --force` |
