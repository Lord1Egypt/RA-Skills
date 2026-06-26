---
name: eve-fullstack-app-design
description: Architect a full-stack application on Eve Horizon — manifest-driven services, managed databases, build pipelines, deployment strategies, secrets, and observability. Use when designing a new app, planning a migration, or evaluating your architecture.
triggers:
  - fullstack design
  - app architecture
  - design an app
  - architect app
  - fullstack app
  - app design
  - system design eve
---

# Full-Stack App Design on Eve Horizon

Architect applications where the manifest is the blueprint, the platform handles infrastructure, and every design decision is intentional.

## When to Use

Load this skill when:
- Designing a new application from scratch on Eve
- Migrating an existing app onto the platform
- Evaluating whether your current architecture uses Eve's capabilities well
- Planning service topology, database strategy, or deployment pipelines
- Deciding between managed and external services

This skill teaches *design thinking* for Eve's PaaS layer. For CLI usage and operational detail, load the corresponding eve-se skills (`eve-manifest-authoring`, `eve-deploy-debugging`, `eve-auth-and-secrets`, `eve-pipelines-workflows`).

## The Manifest as Blueprint

The manifest (`.eve/manifest.yaml`) is the single source of truth for your application's shape. Treat it as an architectural document, not just configuration.

### What the Manifest Declares

| Concern | Manifest Section | Design Decision |
|---------|-----------------|-----------------|
| Service topology | `services` | What processes run, how they connect |
| Infrastructure | `services[].x-eve` | Managed DB, ingress, roles |
| Build strategy | `services[].build` + `registry` | What gets built, where images live |
| Release pipeline | `pipelines` | How code flows from commit to production |
| Environment shape | `environments` | Which environments exist, what pipelines they use |
| Agent configuration | `x-eve.agents`, `x-eve.chat` | Agent profiles, team dispatch, chat routing |
| Runtime defaults | `x-eve.defaults` | Harness, workspace, git policies |

**Design principle**: If an agent or operator can't understand your app's shape by reading the manifest, the manifest is incomplete.

## Service Topology

### Choose Your Services

Most Eve apps follow one of these patterns:

**API + Database** (simplest):
```
services:
  api:        # HTTP service with ingress
  db:         # managed Postgres
```

**API + Worker + Database**:
```
services:
  api:        # HTTP service (user-facing)
  worker:     # Background processor (jobs, queues)
  db:         # managed Postgres
```

**Multi-Service**:
```
services:
  web:        # Frontend/SSR
  api:        # Backend API
  worker:     # Background jobs
  db:         # managed Postgres
  redis:      # external cache (x-eve.external: true)
```

### Service Design Rules

1. **One concern per service.** Separate HTTP serving from background processing. An API service should not also run scheduled jobs.
2. **Use managed DB for Postgres.** Declare `x-eve.role: managed_db` and let the platform provision, connect, and inject credentials. No manual connection strings.
3. **Mark external services explicitly.** Use `x-eve.external: true` with `x-eve.connection_url` for services hosted outside Eve (Redis, third-party APIs).
4. **Use `x-eve.role: job` for one-off tasks.** Migrations, seeds, and data backfills are job services, not persistent processes.
5. **Expose ingress intentionally.** Only services that need external HTTP access get `x-eve.ingress.public: true`. Internal services communicate via cluster networking.
6. **Choose a hostname strategy early.** Every public service gets a generated platform URL by default. Layer on `x-eve.ingress.alias` for a friendlier platform-subdomain (`ingest.eve.example.com`), or `x-eve.ingress.domains: [limelee.com]` to bring your own domain. Custom domains are env-scoped and first-bind-wins — design which environment owns the apex (usually `production`) before declaring it. See `eve-manifest-authoring` and `eve-deploy-debugging` for declaration and DNS verification flow.

### Stable Outbound IPs (Egress)

Most apps don't care about their outbound source IP — but if you integrate with vendors that allowlist source IPs (cameras, payment processors, partner APIs with strict source-IP rules), declare opt-in stable egress at the service level. The platform schedules the pod onto a public-egress node group with `hostNetwork: true`, giving the service a stable, predictable outbound path instead of a shared NAT mapping. Treat this as a deliberate architectural choice for the one or two services that need it — not a default.

### App Object Storage

Apps that need to store files (uploads, avatars, exports) can declare object store buckets in the manifest:

```yaml
services:
  api:
    x-eve:
      object_store:
        buckets:
          - name: uploads
            visibility: private
          - name: avatars
            visibility: public
```

> **Note:** The database schema for app object stores exists, but automatic provisioning from the manifest is not yet wired. See `references/object-store-filesystem.md` for current status.

When wired, the platform injects `STORAGE_ENDPOINT`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `STORAGE_BUCKET`, and `STORAGE_FORCE_PATH_STYLE` into the service container.

**Credential isolation**: app pods receive **app-scoped** storage credentials, not platform-internal credentials. A compromised app service can't reach platform buckets or other tenants' data. Design with this boundary in mind — don't try to share credentials across apps; declare each app's buckets and let the platform issue scoped keys.

### Cloud FS / Google Drive Storage

For document-oriented storage, use cloud FS mounts. Each org connects its own Google Drive via BYOA OAuth credentials, then mounts folders into the org filesystem:

```bash
eve integrations configure google-drive --client-id "..." --client-secret "..."
eve integrations connect google-drive
eve cloud-fs mount --org org_xxx --provider google-drive --folder-id <id> --label "Shared Drive"
```

Apps can browse and search mounted Drive content through Eve's Cloud FS surface (`eve cloud-fs ls`, `eve cloud-fs search`, and the per-mount Cloud FS API routes). This is complementary to object store buckets -- use cloud FS for shared documents and collaboration, use object store for app-managed binary assets.

### Platform-Injected Variables

Every deployed service receives `EVE_API_URL`, `EVE_PUBLIC_API_URL`, `EVE_PROJECT_ID`, `EVE_ORG_ID`, and `EVE_ENV_NAME`. Use `EVE_API_URL` for server-to-server calls. Use `EVE_PUBLIC_API_URL` for browser-facing code. Design your app to read these rather than hardcoding URLs.

## Reference Architecture: SPA + API + Managed DB

The most common Eve fullstack pattern. A nginx-fronted SPA proxies API calls to an internal backend, with managed Postgres and eve-migrate for schema management.

### Service Layout

```
services:
  web:        # nginx SPA (public ingress, proxies /api/ → api service)
  api:        # NestJS/Express backend (internal, no public ingress)
  db:         # managed Postgres 16
  migrate:    # eve-migrate job (runs SQL migrations)
```

**Why nginx proxy?** The web service's nginx reverse-proxies `/api/` to the internal API service. This eliminates CORS, removes the need for hard-coded API hostnames, and gives the SPA same-origin access to the backend. The API service has no public ingress — it's only reachable inside the cluster.

### Manifest Shape

```yaml
services:
  api:
    build:
      context: ./apps/api
      dockerfile: ./apps/api/Dockerfile
    ports: [3000]
    environment:
      NODE_ENV: production
      DATABASE_URL: ${managed.db.url}
      CORS_ORIGIN: "https://myapp.eve.example.com"
    # No x-eve.ingress — API is internal only

  web:
    build:
      context: ./apps/web
      dockerfile: ./apps/web/Dockerfile
    ports: [80]
    environment:
      API_SERVICE_HOST: ${ENV_NAME}-api    # k8s service DNS for nginx proxy
    depends_on:
      api:
        condition: service_healthy
    x-eve:
      ingress:
        public: true
        port: 80
        alias: myapp                        # https://myapp.{org}-{project}-{env}.eve.example.com

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
```

### The nginx Proxy

The web service Dockerfile builds the SPA with Vite, then serves it via nginx. The nginx config uses `envsubst` to resolve `${API_SERVICE_HOST}` at container startup:

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
        proxy_pass http://${API_SERVICE_HOST}:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_buffering off;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /health {
        return 200 "ok";
        add_header Content-Type text/plain;
    }
}
```

In the manifest, `API_SERVICE_HOST: ${ENV_NAME}-api` resolves to the k8s service name (e.g., `sandbox-api`), giving nginx a stable internal DNS target.

### Eve-Migrate for Schema Management

Eve provides a purpose-built migration runner at `public.ecr.aws/w7c4v0w3/eve-horizon/migrate:latest`. It uses plain SQL files with timestamp prefixes, tracked in a `schema_migrations` table (idempotent, checksummed, transactional).

```
db/
  migrations/
    20260312000000_initial_schema.sql
    20260312100000_seed_data.sql
    20260315000000_add_status_column.sql
```

Mount migrations into the container via `x-eve.files`. The migrate step in the pipeline runs after deploy (the managed DB must be provisioned first).

**Do not use TypeORM, Knex, or Flyway migrations** — they add complexity and diverge from the Eve platform's migration tracking. The eve-migrate runner gives parity between local dev and staging.

### Multi-Stage Dockerfiles

**API Dockerfile** (NestJS/Node):

```dockerfile
FROM node:22-slim AS base
WORKDIR /app
ENV PNPM_HOME="/pnpm" PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@latest --activate

FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile 2>/dev/null || pnpm install

FROM deps AS build
COPY tsconfig.json ./
COPY src ./src
RUN pnpm build

FROM node:22-slim AS production
WORKDIR /app
RUN groupadd --gid 1000 node || true && useradd --uid 1000 --gid node --shell /bin/bash --create-home node || true
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER node
ENV NODE_ENV=production PORT=3000
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "fetch('http://localhost:3000/health').then(r => r.ok ? process.exit(0) : process.exit(1)).catch(() => process.exit(1))"
CMD ["node", "dist/main.js"]
```

**Web Dockerfile** (Vite SPA + nginx):

```dockerfile
FROM node:22-slim AS build
WORKDIR /app
ENV PNPM_HOME="/pnpm" PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile 2>/dev/null || pnpm install
COPY tsconfig.json vite.config.ts index.html ./
COPY src ./src
RUN pnpm build

FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

**Conventions**: node:22-slim base, pnpm via corepack, frozen lockfiles, non-root user (API), health checks on both services.

## Database Design

### Provisioning

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
```

Reference the connection URL in other services: `${managed.db.url}`.

### Schema Strategy

1. **Migrations are plain SQL.** Create timestamp-prefixed SQL files in `db/migrations/` (e.g., `20260312000000_initial.sql`). Run via eve-migrate (see Reference Architecture above). Never modify production schemas by hand.
2. **Design for RLS from the start.** Every table with multi-tenant data gets `org_id TEXT NOT NULL`, RLS policies, and a `DatabaseService` that sets the session context (see below). Retrofitting row-level security is painful.
3. **Inspect before changing.** Use `eve db schema` to examine current schema. Use `eve db sql --env <env>` for ad-hoc queries during development.
4. **Separate app data from agent data.** Use distinct schemas or naming conventions. App tables serve the product; agent tables serve memory and coordination (see `eve-agent-memory` for storage patterns).

### RLS + DatabaseService Pattern (NestJS)

The proven pattern for multi-tenant RLS in NestJS uses raw `pg.Pool` (not an ORM) with a request-scoped transaction wrapper:

**`db.ts`** — Pool configuration with startup health check:

```typescript
import { Pool } from 'pg';

const databaseUrl = process.env.DATABASE_URL || 'postgresql://app:app@localhost:5432/myapp';
const parsed = new URL(databaseUrl);
const isLocal = ['localhost', '127.0.0.1'].includes(parsed.hostname);

export const pool = new Pool({
  connectionString: databaseUrl,
  ssl: !isLocal ? { rejectUnauthorized: false } : undefined,
});
```

**`database.service.ts`** — Transaction wrapper with RLS context:

```typescript
import { Injectable } from '@nestjs/common';
import type { PoolClient, QueryResult, QueryResultRow } from 'pg';
import { pool } from '../db';

export interface DbContext {
  org_id: string;
  user_id?: string;
}

@Injectable()
export class DatabaseService {
  async withClient<T>(context: DbContext | null, fn: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      if (context?.org_id) {
        await client.query("SELECT set_config('app.org_id', $1, true)", [context.org_id]);
      }
      if (context?.user_id) {
        await client.query("SELECT set_config('app.user_id', $1, true)", [context.user_id]);
      }
      const result = await fn(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async query<T extends QueryResultRow>(ctx: DbContext | null, sql: string, params?: unknown[]): Promise<QueryResult<T>> {
    return this.withClient(ctx, (client) => client.query<T>(sql, params));
  }

  async queryOne<T extends QueryResultRow>(ctx: DbContext | null, sql: string, params?: unknown[]): Promise<T | null> {
    const result = await this.query<T>(ctx, sql, params);
    return result.rows[0] ?? null;
  }
}
```

**Why this pattern?**
- `set_config('app.org_id', $1, true)` is transaction-scoped — it automatically clears when the connection returns to the pool.
- Every database access goes through `withClient`, guaranteeing RLS context is set before any query.
- No ORM overhead — raw SQL gives full control over query plans and joins.
- The `DbContext` object is derived from `req.user` (set by Eve auth middleware).

**RLS policy template** (applied per table in migration SQL):

```sql
ALTER TABLE my_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY my_table_select ON my_table FOR SELECT
  USING (current_setting('app.org_id', true) IS NOT NULL
    AND org_id = current_setting('app.org_id', true));

CREATE POLICY my_table_insert ON my_table FOR INSERT
  WITH CHECK (current_setting('app.org_id', true) IS NOT NULL
    AND org_id = current_setting('app.org_id', true));

CREATE POLICY my_table_update ON my_table FOR UPDATE
  USING (current_setting('app.org_id', true) IS NOT NULL
    AND org_id = current_setting('app.org_id', true))
  WITH CHECK (current_setting('app.org_id', true) IS NOT NULL
    AND org_id = current_setting('app.org_id', true));
```

**Table conventions**: Every table gets `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, `org_id TEXT NOT NULL`, `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`, and `updated_at TIMESTAMPTZ` (with a trigger) on mutable tables. Enable `pgcrypto` extension in the first migration.

### Access Patterns

| Who Queries | How | Auth |
|-------------|-----|------|
| App service | `${managed.db.url}` in service env | Connection string injected at deploy |
| Agent via CLI | `eve db sql --env <env>` | Job token scopes access |
| Agent via RLS | SQL with `app.current_user_id()` | Session context set by runtime |

## Build and Release Pipeline

### The Canonical Flow

Every production app should follow `build → release → deploy → migrate → smoke-test`:

```yaml
pipelines:
  deploy:
    steps:
      - name: build
        action:
          type: build          # Creates BuildSpec + BuildRun, produces image digests
      - name: release
        depends_on: [build]
        action:
          type: release        # Creates immutable release from build artifacts
      - name: deploy
        depends_on: [release]
        action:
          type: deploy         # Deploys release to target environment
      - name: migrate
        depends_on: [deploy]
        action:
          type: job
          service: migrate     # Runs eve-migrate against the managed DB
      - name: smoke-test
        depends_on: [migrate]
        script:
          run: ./scripts/smoke-test.sh
          timeout: 300
```

**Why this order matters**:
- `build` produces SHA256 image digests. `release` pins those exact digests. `deploy` uses the pinned release. You deploy exactly what you built — no tag drift, no "latest" surprises.
- `migrate` runs *after* deploy because the managed DB must be provisioned first. The eve-migrate job applies any pending SQL migrations.
- `smoke-test` validates the deployed services end-to-end before the pipeline reports success.

### Registry Decisions

| Option | When to Use |
|--------|-------------|
| `registry: "eve"` | Default. Internal registry with JWT auth. Simplest setup. |
| BYO registry (GHCR, ECR) | When you need images accessible outside Eve, or have existing CI. |
| `registry: "none"` | Public base images only. No custom builds. |

For GHCR, add OCI labels to Dockerfiles for automatic repository linking:
```dockerfile
LABEL org.opencontainers.image.source="https://github.com/YOUR_ORG/YOUR_REPO"
```

### Build Configuration

Every service with a custom image needs a `build` section:

```yaml
services:
  api:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    image: ghcr.io/org/my-api
```

Use multi-stage Dockerfiles. BuildKit handles them natively. Place the OCI label on the final stage.

## Deployment and Environments

### Environment Strategy

| Environment | Type | Purpose | Pipeline |
|-------------|------|---------|----------|
| `staging` | persistent | Integration testing, demos | `deploy` |
| `production` | persistent | Live traffic | `deploy` (with promotion) |
| `preview-*` | temporary | PR previews, feature branches | `deploy` (auto-cleanup) |

Link each environment to a pipeline in the manifest:

```yaml
environments:
  staging:
    pipeline: deploy
  production:
    pipeline: deploy
```

### Deployment Patterns

**Standard deploy**: `eve env deploy staging --ref main --repo-dir .` triggers the linked pipeline.

**Direct deploy** (bypass pipeline): `eve env deploy staging --ref <sha> --direct` for emergencies or simple setups.

**Promotion**: Build once in staging, then promote the same release artifacts to production. The build step's digests carry forward, guaranteeing identical images.

### Recovery

When a deploy fails:
1. **Diagnose**: `eve env diagnose <project> <env>` — shows health, recent deploys, service status.
2. **Logs**: `eve env logs <project> <env>` — container output.
3. **Rollback**: Redeploy the previous known-good release.
4. **Reset**: `eve env reset <project> <env>` — nuclear option, reprovisions from scratch.

Design your app to be rollback-safe: migrations should be forward-compatible, and services should handle schema version mismatches gracefully during rolling deploys.

### The System App Pattern

Platform-tier and admin apps deploy through the same Eve pipeline as customer apps — no special path. The Eve Dashboard is the canonical example: it ships through the standard build → release → deploy flow, sits in the CI publish matrix alongside other apps, and consumes the same SSO + analytics APIs any customer app would. If you're building an internal admin console, a control plane for your own platform, or a system-tier surface, adopt this pattern. The win is parity: one deployment story, one auth story, one observability story across all your apps. Avoid carving out bespoke "platform-only" deploy paths — they rot and diverge.

## Per-Org OAuth for App Integrations

Apps that integrate with Google Drive, Slack, or other OAuth providers use per-org credentials (BYOA -- Bring Your Own App). Each org registers its own OAuth app, giving it control over branding, scopes, rate limits, and credential rotation.

```bash
eve integrations configure google-drive --client-id "..." --client-secret "..."
eve integrations connect google-drive
```

**Design implications**: Apps that consume Google Drive data or Slack messages should reference integration tokens through the Eve API, not store OAuth credentials themselves. The platform handles token refresh using the org's registered OAuth app credentials.

## Event Triggers for Workflows

Workflows can be triggered by platform events, enabling reactive automation:

```yaml
workflows:
  on-deploy:
    trigger:
      system.event: environment.deployed
    steps:
      - name: smoke-test
        script:
          run: ./scripts/smoke-test.sh

  on-ingest:
    trigger:
      system.event: doc.ingest.completed
    steps:
      - name: process
        agent: doc-processor
```

Event sources include: GitHub webhooks, Slack events, system events (deploy, build, ingest), cron schedules, and manual triggers. See `eve-pipelines-workflows` for trigger syntax and `references/events.md` for the full event catalog.

## App CLI Framework — The Eve Way

**Every app with an API should ship a CLI.** This is the Eve way — agents interact with app data through CLI commands, not raw REST calls. A CLI gives agents discoverable, auth-transparent, type-safe access to your app's domain. It reduces LLM calls per operation from 3-5 (curl) to 1 (CLI command), eliminates URL construction and JSON quoting, and surfaces domain-specific error messages instead of HTTP status codes.

### Why CLI-First Matters

When a coding agent needs to read or write app data, it faces a choice: construct a curl command with the right URL, auth header, and JSON body — or run `eden projects list --json`. The CLI approach wins on every dimension:

| Dimension | CLI | Raw REST |
|-----------|-----|----------|
| Auth | Invisible (`EVE_JOB_TOKEN` read automatically) | Manual header construction |
| URL | None (CLI knows the service URL) | Build from `EVE_APP_API_URL_*` |
| Discoverability | `myapp --help` | Read OpenAPI spec or docs |
| Errors | Domain-specific messages | HTTP status codes |
| LLM cost | 1 call per operation | 3-5 calls per operation |

### Declare the CLI in the Manifest

```yaml
services:
  api:
    x-eve:
      api_spec:
        type: openapi
      cli:
        name: myapp              # Binary name on $PATH
        bin: cli/bin/myapp       # Pre-bundled executable (repo-bundled mode)
```

The platform auto-discovers services with `x-eve.cli` from the manifest and makes them available on `$PATH` for all agent jobs in the project — no explicit `with_apis` needed. Just declare the CLI in the manifest and every agent gets it. Agents run `myapp --help` to discover capabilities. See `eve-manifest-authoring` for declaration details and `references/app-cli.md` for the full implementation pattern (bundling, env var contract, testing).

### Design Guidance

1. **Build the CLI early.** Don't wait until the API is "done." Start the CLI alongside the first API endpoints. Agents will use it immediately.
2. **Mirror the API surface.** Every REST endpoint should have a CLI subcommand. `GET /items` → `myapp items list`, `POST /items` → `myapp items create --file data.json`.
3. **Support `--json` everywhere.** Default output is human-readable tables; `--json` gives machine-readable output for agent pipelines.
4. **Bundle as a single file.** Use esbuild to produce a self-contained Node.js script committed to the repo. Zero startup latency.
5. **Point agent skills at the CLI.** Skill instructions should say "Use `myapp items list`", never "curl the API at..."

## Embedded Conversations

If your app has a chat surface — a sidebar pane, an inline assistant, an "ask about this object" button — use Eve's embedded conversation API and chat SDK. Don't hand-roll auth, dispatch, SSE, reconnect, or optimistic-send. The platform exposes find-or-create thread routing keyed by an app-supplied identifier (e.g. `myapp:{project_id}:{conversation_id}`), JWKS-verified browser tokens, and a replayable SSE stream — composed into `@eve-horizon/chat` and `@eve-horizon/chat-react` for ~50 lines of UI code.

**Design implications**:
- Map your product objects (a document, a project, a ticket) to Eve threads by stable key. The platform owns thread state; your app owns product projections that reference `thread_id`.
- Route through `chat.yaml`, an agent, a team, or a workflow using the same primitives external gateways use. Chat is just another dispatch target.
- Phase 1 push uses SSE with snapshot + polling catch-up; design your UI to tolerate brief reconnects rather than assuming a persistent socket.

For SDK shape and routing patterns, see `references/eve-sdk.md` in the `eve-read-eve-docs` skill.

## App Undeploy/Delete Lifecycle

Manage the full lifecycle of environments and projects:

```bash
# Undeploy services (stops pods, keeps env record and history)
eve env undeploy <project> <env>

# Delete environment entirely (cascades to managed DB, secrets)
eve env delete <project> <env>

# Delete project (cascades to all environments, artifacts, history)
eve project delete <project-id>
```

Design your app for clean teardown: migrations should be idempotent, managed DB deletion is irreversible, and pipeline history is preserved in audit logs even after environment deletion.

## Secrets and Configuration

### Scoping Model

Secrets resolve with cascading precedence: **project > user > org > system**. A project-level `API_KEY` overrides an org-level `API_KEY`.

### Design Rules

1. **Set secrets per-project.** Use `eve secrets set KEY "value" --project proj_xxx`. Keep project secrets self-contained.
2. **Use interpolation in the manifest.** Reference `${secret.KEY}` in service environment blocks. The platform resolves at deploy time.
3. **Validate before deploying.** Run `eve manifest validate --validate-secrets` to catch missing secret references before they cause deploy failures.
4. **Use `.eve/dev-secrets.yaml` for local development.** Mirror the production secret keys with local values. This file is gitignored.
5. **Never store secrets in environment variables directly.** Always use `${secret.KEY}` interpolation. This ensures secrets flow through the platform's resolution and audit chain.

### Service Tokens (Manifest-Declared, Read-Only by Default)

Services that call the Eve API on their own behalf get an auto-injected `EVE_SERVICE_TOKEN`. Permissions are declared explicitly per service in the manifest, and the default is read-only — services that need to write must opt in. Treat this as a least-privilege contract: a service shouldn't quietly gain write access by being deployed. Declare the minimum capabilities each service needs and let code review surface the deltas. See `references/secrets-auth.md` and `references/manifest.md` in `eve-read-eve-docs` for declaration syntax.

### Scoped Job Tokens (Platform-Tier Least Privilege)

For platform-tier apps that orchestrate jobs over multi-tenant resources, permission names alone are not enough — `orgfs:read` says nothing about *which prefix*. Declare resource scope on workflow steps to enforce least-privilege at the token level:

```yaml
workflows:
  scoped-review:
    scope:
      orgfs: { allow_prefixes: [/groups/projects/proj-a/**] }
    steps:
      - name: review
        agent: { name: reviewer }
        scope:
          cloud_fs: { allow_mount_ids: [mount_a] }
```

Scope axes match access bindings: `orgfs`, `orgdocs`, `envdb`, `cloud_fs`. Workflow, step, and invocation scopes are **intersected** (empty intersection fails closed) and persisted as `jobs.token_scope`. The orchestrator uses the same scope to build the workspace `.org` mount and mint the job token — the on-disk view and the API authority match. Design platform-tier workflows so each step only sees the resources it actually needs.

### Git Credentials

Agents need repository access. Set either `github_token` (HTTPS) or `ssh_key` (SSH) as project secrets. The worker injects these automatically during git operations.

## SSO Authentication

### Adding SSO to Your App

Eve provides shared auth packages that eliminate boilerplate. Add Eve SSO login in ~25 lines of code.

**Backend** (`@eve-horizon/auth`):

```typescript
import { eveUserAuth, eveAuthGuard, eveAuthConfig } from '@eve-horizon/auth';

app.use(eveUserAuth());                                     // Parse tokens (non-blocking)
app.get('/auth/config', eveAuthConfig());                   // Serve SSO discovery
app.get('/auth/me', eveAuthGuard(), (req, res) => {
  res.json(req.eveUser);                                    // { id, email, orgId, role }
});
app.use('/api', eveAuthGuard());                            // Protect all API routes
```

**Frontend** (`@eve-horizon/auth-react`):

```tsx
import { EveAuthProvider, EveLoginGate } from '@eve-horizon/auth-react';

function App() {
  return (
    <EveAuthProvider apiUrl="/api">
      <EveLoginGate>
        <ProtectedApp />
      </EveLoginGate>
    </EveAuthProvider>
  );
}
```

For authenticated API calls from components, use `createEveClient`:

```typescript
import { createEveClient } from '@eve-horizon/auth-react';
const client = createEveClient('/api');
const res = await client.fetch('/data');
```

**Custom auth gate** — When you need control over loading and login states (custom login page, richer loading UI), use `useEveAuth()` directly instead of `EveLoginGate`:

```tsx
import { EveAuthProvider, useEveAuth } from '@eve-horizon/auth-react';

function AuthGate() {
  const { user, loading, loginWithToken, loginWithSso, logout } = useEveAuth();
  if (loading) return <Spinner />;
  if (!user) return <LoginPage onSso={loginWithSso} onToken={loginWithToken} />;
  return <AppShell user={user} onLogout={logout}><Routes /></AppShell>;
}

export default function App() {
  return (
    <EveAuthProvider apiUrl={API_BASE}>
      <AuthGate />
    </EveAuthProvider>
  );
}
```

### How It Works

1. `EveAuthProvider` checks `sessionStorage` for cached token
2. If no token, probes SSO broker `/session` (root-domain cookie)
3. If SSO session exists, gets fresh Eve RS256 token
4. If no session, shows login form (SSO redirect or token paste)
5. All API requests include `Authorization: Bearer <token>`

### NestJS Backend

Apply `eveUserAuth()` as global middleware in `main.ts`. If existing controllers expect `req.user` rather than `req.eveUser`, add a thin bridge that maps Eve roles to app-specific roles in one place:

```typescript
import { eveUserAuth } from '@eve-horizon/auth';

app.use(eveUserAuth());
app.use((req, _res, next) => {
  if (req.eveUser) {
    req.user = { ...req.eveUser, role: req.eveUser.role === 'member' ? 'viewer' : 'admin' };
  }
  next();
});
```

### Auto-Injected Variables

The platform injects `EVE_SSO_URL`, `EVE_API_URL`, `EVE_ORG_ID`, and `EVE_PROJECT_ID` into deployed containers. No manual configuration needed. Use `${SSO_URL}` in manifest env blocks for frontend-accessible SSO URLs. `EVE_PROJECT_ID` is what enables the platform to scope branding, redirect allowlists, and app-scoped auth policy to your project.

### Passwordless / Magic-Link Apps

If your app's onboarding is "admin invites a user, user clicks email, user lands in app" — model it as a passwordless app. Don't build a password reset flow you don't need. Declare it in the manifest and let the platform render a branded magic-link login page:

```yaml
x-eve:
  auth:
    login_method: magic_link            # or password_or_magic_link, password
    self_signup: false                  # unknown emails return generic success, no email
    invite_requires_password: false     # invite acceptance skips /set-password
```

**Design implications:**
- Users are created through invites, not self-signup. Plan your admin invite UX accordingly.
- The magic-link email reuses the same `x-eve.branding` block as invite emails — one branding source, two email copies.
- Eve API handles eligibility (existing user, pending invite, domain signup) before any email is sent, so account-enumeration defense is preserved without app-side work.

### App Branding (Invites and Magic-Link Emails)

Per-app branding is a manifest concern, not a code concern. Declare it once and the platform applies it to invite emails, magic-link emails, and SSO login pages:

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    app_logo_url: "https://app.example.com/assets/logo.svg"
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
    reply_to_email: "support@example.com"
    support_email: "support@example.com"
    support_url: "https://example.com/help"
```

The `From:` display name and email body carry the app identity; the sender address remains the platform default (verified per-tenant `From:` is a later phase). Treat branding as a property of the project, not a per-org concern.

### App Org Access and In-App Admin Invites

By default an app is scoped to its project owner org. For multi-tenant apps that serve multiple customer orgs, declare an allowlist and (optionally) enable in-app admin invites:

```yaml
x-eve:
  auth:
    org_access:
      mode: allowlist
      allowed_orgs: [org_customer123, customer-slug]
      invite:
        enabled: true
        admin_roles: [admin, owner]
        invited_role: member          # fixed; app invites cannot create admins
```

**Design implications:**
- Backends should use `eveAppUserAuth()` (not `eveUserAuth()`) so authorization is bound to the app policy, not the project owner org. The middleware consults `GET /auth/app-access` and selects an org from `X-Eve-Org-Id`, `?eve_org_id=`, or the first allowed org.
- Build admin pages around `POST /auth/app-invites` (sends branded magic-link onboarding) instead of generic org-invite APIs. The platform enforces org role + app allowlist policy before sending.
- The React SDK exposes `useEveAppAccess()` for orgs/admin-org listings and inviting members.

### Domain-Based Signup (Path C Auto-Attach)

When an app needs to serve a whole customer email domain — "anyone with a `@yourcompany.com` address should land in `org_yourcompany` as a member" — use domain signup. Eve writes a one-shot invite on first magic-link request and auto-attaches membership when the user accepts. One project can route different domains to different orgs:

```yaml
x-eve:
  auth:
    org_access:
      mode: allowlist
      allowed_orgs: [org_acme, org_globex]
      domain_signup:
        enabled: true
        domains:
          - { domain: acme.com,   target_org: org_acme,   role: member }
          - { domain: globex.com, target_org: org_globex }
```

**Design implications:**
- Rules are walked in declaration order — first match wins. Declare more-specific patterns first.
- The trust model is "operator declares, platform trusts" — no DNS proof in v1. Declaring `free-mail.example` produces a coherence warning but is permitted.
- Explicit pending invites (Path B) always win over domain signup (Path C); existing users with allowed-org membership (Path A) get the standard branded send.
- Removing a rule stops new signups but does not retroactively remove existing memberships — plan offboarding as an explicit `eve org members remove`.
- Audit via `auth.domain_signup.invite_created` and `auth.domain_signup.member_attached` events.

### Project-Scoped Redirect Allowlist (Custom Domains)

If your app runs on its own custom domain (not under the cluster domain), declare which origins SSO may redirect to. Without this, SSO rewrites the redirect to the platform-default hostname and your branded app URL is lost:

```yaml
x-eve:
  auth:
    allowed_redirect_origins:
      - https://app.example.com
      - https://www.example.com
```

The final allowlist is the union of manifest entries, the project's own eligible custom domains, and (for `mode: allowlist`) cross-org custom domains owned by projects in `allowed_orgs`. This replaces the legacy hard-coded `EVE_DEFAULT_DOMAIN` allowlist. The platform also guarantees `SameSite=None; Secure` on SSO session cookies so cross-site `/session` probes from your custom-domain frontend carry credentials — you no longer need to configure cookie attributes yourself.

### Design Rules

1. **Use the SDK, not custom auth.** The SDK replaces ~750 lines of hand-rolled auth with ~50 lines.
2. **Non-blocking middleware first.** Use `eveUserAuth()` globally, then `eveAuthGuard()` on protected routes. This enables mixed public/private routes.
3. **The `/auth/config` endpoint is the handshake.** The frontend discovers the SSO URL by calling the backend's `eveAuthConfig()` endpoint. This decouples the frontend from platform env vars and works identically in local dev and deployed environments.
4. **Design for token staleness.** The `orgs` JWT claim reflects membership at mint time (1-day TTL). Use `strategy: 'remote'` for immediate revocation if needed.

For full SDK reference, see `references/auth-sdk.md` in the `eve-read-eve-docs` skill.

## Observability and Debugging

### The Debugging Ladder

Escalate through these stages:

```
1. Status    → eve env show <project> <env>
2. Diagnose  → eve env diagnose <project> <env>
3. Logs      → eve env logs <project> <env>
4. Pipeline  → eve pipeline logs <pipeline> <run-id> --follow
5. Recover   → eve env deploy (rollback) or eve env reset
```

Start at the top. Each stage provides more detail and more cost. Most issues resolve at stages 1-2.

### Pipeline Observability

Monitor pipeline execution in real time:

```bash
eve pipeline logs <pipeline> <run-id> --follow         # stream all steps
eve pipeline logs <pipeline> <run-id> --follow --step build  # stream one step
```

Failed steps include failure hints and link to build diagnostics when applicable.

### Build Debugging

When builds fail:

```bash
eve build list --project <project_id>
eve build diagnose <build_id>
eve build logs <build_id>
```

Common causes: missing registry credentials, Dockerfile path mismatch, build context too large.

### Health Checks

Design services with health endpoints. Eve polls health to determine deployment readiness. A deploy is complete when `ready === true` and `active_pipeline_run === null`.

## Design Checklist

**Service Topology:**
- [ ] Each service has one responsibility
- [ ] Managed DB declared for Postgres needs
- [ ] External services marked with `x-eve.external: true`
- [ ] Only public-facing services have ingress enabled
- [ ] Platform-injected env vars used (not hardcoded URLs)
- [ ] Hostname strategy chosen (generated URL, alias, or custom domain via `x-eve.ingress.domains`)
- [ ] Stable egress opted in only for services that integrate with source-IP-allowlisted vendors

**Database:**
- [ ] Migrations are plain SQL files in `db/migrations/` with timestamp prefixes
- [ ] `eve-migrate` job service declared in manifest with `x-eve.files` mount
- [ ] `DatabaseService` wraps all DB access with RLS context (`set_config`)
- [ ] RLS policies on every table with `org_id`
- [ ] `pgcrypto` extension enabled, UUID primary keys, `updated_at` triggers
- [ ] App data separated from agent data by schema or convention

**Pipeline:**
- [ ] Canonical `build → release → deploy → migrate → smoke-test` pipeline defined
- [ ] Migrate step runs after deploy (managed DB must exist first)
- [ ] Smoke test script validates deployed services end-to-end
- [ ] Registry chosen and credentials set as secrets
- [ ] OCI labels on Dockerfiles (for GHCR)
- [ ] Image digests flow through release (no tag-based deploys)

**Environments:**
- [ ] Staging and production environments defined
- [ ] Each environment linked to a pipeline
- [ ] Promotion workflow defined (build once, deploy many)
- [ ] Recovery procedure known (diagnose -> rollback -> reset)

**Secrets:**
- [ ] All secrets set per-project via `eve secrets set`
- [ ] Manifest uses `${secret.KEY}` interpolation
- [ ] `eve manifest validate --validate-secrets` passes
- [ ] `.eve/dev-secrets.yaml` exists for local development
- [ ] Git credentials (`github_token` or `ssh_key`) configured
- [ ] Service token permissions declared per service (default read-only; write opted in explicitly)

**Authentication:**
- [ ] `@eve-horizon/auth` middleware added to backend (`eveUserAuth` + `eveAuthGuard`, or `eveAppUserAuth` for multi-org apps)
- [ ] Auth config endpoint serves SSO discovery (`eveAuthConfig`)
- [ ] `@eve-horizon/auth-react` wraps frontend (`EveAuthProvider` + `EveLoginGate` or custom `useEveAuth` gate)
- [ ] `createEveClient` used for authenticated API calls from frontend
- [ ] Platform-injected auth env vars used (`EVE_SSO_URL`, `EVE_ORG_ID`, `EVE_PROJECT_ID`)
- [ ] Eve roles mapped to app roles in one place (bridge middleware), not scattered across controllers
- [ ] If passwordless: `x-eve.auth.login_method: magic_link` + `invite_requires_password: false`
- [ ] If multi-tenant: `x-eve.auth.org_access.mode: allowlist` with `allowed_orgs` declared; in-app admin invites use `POST /auth/app-invites`
- [ ] If domain-based onboarding: `domain_signup.domains` declares per-rule `target_org`; more-specific rules listed first
- [ ] If custom domain: `x-eve.auth.allowed_redirect_origins` declared; `eve project auth-context` confirms resolved allowlist
- [ ] If branded: `x-eve.branding` declared (shared by invite and magic-link emails); `From:` display name and logo set

**App CLI (the Eve way):**
- [ ] App API wrapped in a domain CLI (e.g., `eden projects list`)
- [ ] CLI declared in manifest via `x-eve.cli` with `name` and `bin`
- [ ] CLI bundled as single-file executable (esbuild for Node.js)
- [ ] CLI reads `EVE_APP_API_URL_{SERVICE}` and `EVE_JOB_TOKEN` automatically
- [ ] All CLI commands support `--json` for machine-readable output
- [ ] Agent skill references CLI commands, not raw curl/REST calls

**Observability:**
- [ ] Services expose health endpoints
- [ ] The debugging ladder is understood (status -> diagnose -> logs -> recover)
- [ ] Pipeline logs are accessible via `eve pipeline logs --follow`

## Cross-References

- **Manifest syntax and options**: `eve-manifest-authoring`
- **Deploy commands and error resolution**: `eve-deploy-debugging`
- **Secret management and access groups**: `eve-auth-and-secrets`
- **Pipeline and workflow definitions**: `eve-pipelines-workflows`
- **Local development workflow**: `eve-local-dev-loop`
- **Layering agentic capabilities onto this foundation**: `eve-agentic-app-design`
- **Auth SDK and SSO integration**: `eve-read-eve-docs` → `references/auth-sdk.md`
- **Object storage and filesystem**: `eve-read-eve-docs` → `references/object-store-filesystem.md`
- **External integrations (Slack, GitHub)**: `eve-read-eve-docs` → `references/integrations.md`
