# Manifest (Current)

## Use When
- You need to author, validate, or review `.eve/manifest.yaml`.
- You need to configure services, environments, pipelines, or harness defaults.
- You need to prepare manifest changes for deployable, reproducible builds.

## Load Next
- `references/pipelines-workflows.md` for pipeline/job wiring in manifests.
- `references/secrets-auth.md` for secret declaration and resolution order.
- `references/overview.md` for core platform concepts before editing complex files.

## Ask If Missing
- Confirm target manifest path and environment names.
- Confirm whether managed DBs, external services, or custom ingress are required.
- Confirm any required repository path, branch, or org/project identifiers.

The manifest (`.eve/manifest.yaml`) is the single source of truth for builds, deploys, pipelines, and workflows.
Schema is Compose-like with Eve extensions under `x-eve`.

## Minimal Example

The simplest possible deployable project. Uses the Eve-native registry so `image` fields are auto-derived from service keys:

```yaml
schema: eve/compose/v2
project: my-app

registry: "eve"

services:
  app:
    build:
      context: .
    ports: ["3000"]
    x-eve:
      ingress:
        public: true

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
        action: { type: deploy, env_name: sandbox }
```

Deploy with two commands:

```bash
eve project sync --dir .
eve env deploy sandbox --ref main
```

## Full Example

A complete manifest showing the standard SPA + API + managed DB pattern with eve-migrate, nginx reverse proxy, and the canonical pipeline:

```yaml
schema: eve/compose/v2
project: my-project

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
      CORS_ORIGIN: "https://my-project.eve.example.com"
    # No x-eve.ingress — API is internal, reached via web's /api/ proxy

  web:
    build:
      context: ./apps/web
      dockerfile: ./apps/web/Dockerfile
    ports: [80]
    environment:
      API_SERVICE_HOST: ${ENV_NAME}-api
    depends_on:
      api:
        condition: service_healthy
    x-eve:
      ingress:
        public: true
        port: 80
        alias: my-project

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
        extensions: [postgis, pgvector, pg_trgm]

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
        action:
          type: job
          service: migrate
      - name: smoke-test
        depends_on: [migrate]
        script:
          run: ./scripts/smoke-test.sh
          timeout: 300
```

Key patterns:
- **`eve-migrate`** for database migrations — plain SQL files mounted via `x-eve.files`. Runs after deploy because the managed DB must be provisioned first.
- **nginx reverse proxy** on the web service proxies `/api/` to the internal API via `API_SERVICE_HOST: ${ENV_NAME}-api` (k8s service DNS). No CORS, no hard-coded hostnames.
- **`${managed.db.url}`** — connection string injected by Eve for managed databases.
- **`managed.extensions`** — optional managed Postgres extensions. Plain extensions are `postgis`, `pgvector`, `pg_trgm`, `btree_gist`, `hstore`, and `citext`. `pgvector` installs as PostgreSQL extension `vector`; extension removal is sticky and does not run `DROP EXTENSION`. `pg_cron` is provider-gated and only validates when the platform enables `EVE_MANAGED_DB_ENABLED_PRELOAD_EXTENSIONS=pg_cron` and preloads it on the backing Postgres; Eve installs it in the instance admin database (`postgres`) per the AWS RDS model. `timescaledb` is not declarable on AWS RDS.
- **Smoke test** validates the deployed services end-to-end before pipeline success.

## Top-Level Fields

```yaml
schema: eve/compose/v2          # optional schema identifier
name: my-project                # project name (preferred)
description: "Short description" # optional project description
project: my-project             # legacy alias for name (either works)
registry:                        # optional container registry
services:                        # required
environments:                    # optional
pipelines:                       # optional
workflows:                       # optional
versioning:                      # optional
x-eve:                           # optional Eve extensions
```

Use `name` as the top-level project identifier. `project` is accepted as a legacy alias but `name` is preferred for new manifests.

Unknown fields are allowed for forward compatibility.

### Project Branding And Auth (`x-eve.branding`, `x-eve.auth`)

Project-level branding is used by app invite emails, app-scoped magic-link emails, and branded SSO login pages. It is synced onto the project record by `eve project sync`:

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    app_logo_url: "https://sandbox.acme.example/assets/logo.svg"
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
    reply_to_email: "support@acme.example"
    support_email: "support@acme.example"
    support_url: "https://acme.example/help"
```

`app_name` is required when `branding` is present (≤60 chars, no newlines). Logo/support URLs must be valid URLs; only HTTPS logo URLs are emitted into Phase 1 emails. `primary_color` must be a six-digit hex like `#1f6feb`. `email_from_name`, `reply_to_email`, and `support_email` set the `From:`/`Reply-To:` headers on app-scoped mail while keeping the platform sender address.

Apps can opt into passwordless login with:

```yaml
x-eve:
  auth:
    login_method: magic_link          # password_or_magic_link | password | magic_link
    self_signup: false
    invite_requires_password: false
```

When `login_method: magic_link`, app SSO hides password login and signup and sends branded magic-link email through Eve API. When `login_method: password_or_magic_link`, password login remains visible and the secondary magic-link request still goes through Eve API for branding and app self-signup enforcement. With `self_signup: false`, unknown emails get generic success but no GoTrue call/email. With `invite_requires_password: false`, invite acceptance establishes the SSO session and redirects to the app without `/set-password`.

Apps can also opt into app-scoped org access and in-app admin invites:

```yaml
x-eve:
  auth:
    login_method: magic_link
    self_signup: false
    invite_requires_password: false
    org_access:
      mode: allowlist                  # project_org | allowlist
      allowed_orgs:
        - org_customer123              # org IDs or slugs; sync stores canonical IDs
        - customer-slug
      invite:
        enabled: true
        admin_roles: [admin, owner]
        invited_role: member           # fixed to member
```

Default `org_access.mode` is `project_org`, which limits SSO/app SDK access to the project owner org. `allowlist` lets a project-owned app serve specific customer orgs. `invite.enabled` allows org admins/owners in those app-allowed orgs to call `POST /auth/app-invites`; app-facing invites always create regular members and use the same project branding as invite/magic-link emails.

#### `x-eve.auth.org_access.domain_signup`

Pre-approve email domains so anyone with a matching address can sign in via magic link without a per-user invite. Each rule maps one domain pattern to one target org, so a single project can serve multiple customer orgs from one manifest.

```yaml
x-eve:
  auth:
    login_method: magic_link
    invite_requires_password: false
    org_access:
      mode: allowlist
      allowed_orgs: [org_Acme, org_Partner, org_Retailer, org_Partner]
      domain_signup:
        enabled: true
        domains:
          - domain: example.com
            target_org: org_Acme
            role: member                    # optional; defaults to 'member'
          - domain: partner.example
            target_org: org_Partner
          - domain: retailer.example
            target_org: org_Retailer
          - domain: partner.example
            target_org: org_Partner
          - domain: "*.partner.example"         # wildcard matches subdomains, not the apex
            target_org: org_Partner
```

**v2 schema (2026-05-12, breaking change).** `domains` is now a list of rule objects. The v1 list-of-strings shape and the block-level `target_org`/`role` fields are gone; manifest sync rejects them.

Rules:

- `enabled: true` requires at least one rule in `domains`.
- Each rule must declare both `domain` and `target_org`. `role` is optional and defaults to `member` (the only allowed value in v2; reserved for future expansion).
- `target_org` must be in the project's effective `allowed_orgs`. Manifest sync resolves slugs to canonical org IDs and rejects rules whose target isn't allowed.
- Duplicate `domain:` keys within one block are rejected.
- Domain patterns are lowercased and IDN-normalized (punycode) at parse time.
- `*.acme.com` matches `eu.acme.com` and `sub.eu.acme.com` but **not** bare `acme.com`. Declare both as separate rules if both should match.
- Invalid with `login_method: password`. `magic_link` and `password_or_magic_link` are both valid.
- Declaring `free-mail.example` (or any free-email provider) emits a manifest coherence warning per rule — the effect is unbounded for that target org.
- No DNS proof. The operator declares; the platform trusts.

Eligibility precedence on `POST /auth/magic-link`:

1. Known user with allowed-org or project membership → branded send.
2. Pending *explicit* (admin-issued) invite → generic success, no email; the invite remains the entry point.
3. Email's domain matches one rule (first-match in declaration order, no implicit longest-match) → write a one-shot `org_invites` row tagged `app_context.source: domain_signup`, `app_context.org_id: <matched rule.target_org>`, `app_context.matched_rule: <domain pattern>` and send branded magic link. The SSO callback consumes the invite and upserts membership into that org.
4. Otherwise, fall through to legacy `self_signup`, then to generic success.

Two audit events flow through the event spine: `auth.domain_signup.invite_created` (creation) and `auth.domain_signup.member_attached` (callback consumption). The creation event payload includes `org_id`, `email_domain`, `matched_rule` (the rule pattern that fired), and a truncated `email_hash`.

Public `/auth/app-context` exposes only `auth.org_access.domain_signup_enabled` (bool). Use `GET /auth/app-context/admin?project_id=...` with a project-admin token to see each rule (`domain`, `target_org`, `role`), or run `eve project auth-context <project_id>` (the CLI tries the admin endpoint first and renders one line per rule as `<domain> -> <target_org> (<role>)`).

#### `x-eve.auth.allowed_redirect_origins`

Apps deployed on custom domains (off-cluster) must declare which origins SSO is
allowed to redirect back to after invite redemption or magic-link callback.
Without this, the SSO broker drops the redirect target and lands the user on
the SSO root.

```yaml
x-eve:
  auth:
    login_method: magic_link
    allowed_redirect_origins:
      - https://sandbox.acme.example
      - https://app.example.com
```

Rules:

- Entries are **origins only**: `scheme://host[:port]`. Paths, query strings,
  fragments, and userinfo are rejected at manifest-validate time.
- `https://` is required, except for local development (`localhost`, loopback
  IPs, `*.lvh.me`) which may use `http://`.
- The SSO broker accepts `redirect_to` and CORS origins matching any entry by
  exact origin (scheme + host + port).

You usually do not need to declare this for apps whose own custom domains are
already registered through `services.<name>.x-eve.ingress.domains`. Eligible
custom domains owned by the project are auto-included in the resolved
allowlist. If your manifest is in a branding-only project that redirects into a
sibling org's deployed app, set `org_access.mode: allowlist` and list the
sibling org under `allowed_orgs` — the sibling's eligible custom domains are
auto-included too.

Inspect the resolved list (manifest ∪ own custom domains ∪ cross-org domains)
with `eve project auth-context <project_id>`.

See `references/secrets-auth.md` for SSO endpoints, app context resolution,
and the `eve org invite` / `POST /auth/app-invites` flows that consume these
fields. `references/integrations.md` covers the per-org OAuth configs that
back app-branded mail delivery, and `references/deploy-debug.md` covers the
custom-domain lifecycle (`pending_dns` → `active`) that feeds the
auto-included redirect origins.

## Workflow References

For large workflows, keep `.eve/manifest.yaml` small and reference repo-local
workflow files:

```yaml
workflows:
  acme-make-plan:
    $ref: .eve/workflows/acme-make-plan
```

Recommended layout:

```text
.eve/workflows/acme-make-plan/
  workflow.yaml
  prompts/
    plan.md
    review.md
```

When `$ref` points to a directory, `eve project sync` and
`eve manifest validate` load `workflow.yaml` or `workflow.yml` from that
directory. `$ref` can also point directly to a `.yaml` or `.yml` workflow
file. References are resolved locally by the CLI before sync; direct API sync
rejects unresolved `$ref` values.

Workflow files can keep long prompts in Markdown files:

```yaml
steps:
  - name: plan
    agent:
      name: acme-planner
      prompt_file: prompts/plan.md
```

`prompt_file` paths are resolved relative to the workflow file directory, read
verbatim, and expanded into `agent.prompt` in the stored manifest.

## Registry

```yaml
registry: "eve"   # Default Eve-managed registry
```

Use `registry: "eve"` unless your app must publish to a BYO registry.

For a private custom registry, switch to full object form:

```yaml
registry:
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth:
    username_secret: REGISTRY_USERNAME
    token_secret: REGISTRY_PASSWORD
```

The deployer uses these secrets to create Kubernetes `imagePullSecrets` for private BYO registries. See container registry reference for setup details.

String modes:
```yaml
registry: "eve"   # Use Eve-managed registry (default)
registry: "none"  # Disable registry handling
registry:           # BYO registry (full object; see above)
```

## Services (Compose-Style)

```yaml
services:
  api:
    build:
      context: ./apps/api
    # image omitted (auto-derived as "api" when build is present)
    ports: [3000]
    environment:
      NODE_ENV: production
    depends_on:
      db:
        condition: service_healthy
    x-eve:
      ingress:
        public: true
        port: 3000
        timeout: 300s
        max_body_size: 10m
      api_spec:
        type: openapi
        spec_url: /openapi.json
```

Supported Compose fields: `image`, `build`, `environment`, `ports`, `depends_on`, `healthcheck`, `volumes`.

**Image auto-derivation**: When a service has `build` config and a `registry` is configured, the `image` field is optional. With Eve-managed default (`registry: "eve"`), platform derives the image name from the service key (for example, service `app` becomes `image: app`) and prefixes it at build time with the managed registry host.

### Eve Service Extensions (`x-eve`)

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | `component` (default), `worker`, `job`, or `managed_db` |
| `ingress` | object | `{ public: true\|false, port: number, alias?: string, domains?: string[], timeout?: string, max_body_size?: string }` |
| `api_spec` | object | Single API spec registration |
| `api_specs` | array | Multiple API spec registrations |
| `cli` | object | App CLI declaration (see CLI Declaration below) |
| `external` | boolean | External dependency (not deployed) |
| `connection_url` | string | Connection string for external services |
| `worker_type` | string | Worker pool type for this service |
| `files` | array | Mount source files into container |
| `storage` | object | Persistent volume configuration |
| `managed` | object | Managed DB config (requires `role: managed_db`) |
| `object_store` | object | App object store bucket declarations |
| `networking` | object | `{ egress: 'nat' \| 'stable' }` (default `nat`). See Stable Egress below. |
| `permissions` | array | Additional permissions for the service's `EVE_SERVICE_TOKEN` |
| `audit_log_table` | string | Optional table queried by `eve env diagnose --request` |
| `request_id_column` | string | Optional request ID column for audit logs (default `request_id`) |

Notes:
- `x-eve.role: job` makes a service runnable as a one-off job (migrations, seeds).
- `x-eve.role: managed_db` marks a service as a platform-provisioned database.
- `spec_url` can be relative (resolved against service URL) or absolute.
- `spec_path` is supported only for local `file://` repos.
- If a service exposes ports and the cluster domain is configured, Eve creates ingress by default. Set `x-eve.ingress.public: false` to disable.
- `ingress.alias` creates a vanity hostname: `{alias}.{domain}` instead of the default `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`. Useful for user-facing apps that need a clean URL.
- `ingress.domains` brings your own domain names (e.g., `["limelee.com", "www.limelee.com"]`). Declare it either on the base service or in `environments.<env>.overrides.services.<svc>.x-eve.ingress.domains`. `eve project sync` registers both forms; a hostname declared in exactly one env override is bound to that env during sync. Each domain gets a separate K8s Ingress with per-domain TLS via cert-manager HTTP-01. Max 10 per service. Domains under the platform domain are rejected — use `alias` instead. All three ingress types (primary, alias, custom domain) coexist and route to the same backend.
- `ingress.timeout` sets nginx-ingress request/response timeout for the service's primary, alias, and custom-domain ingresses. Use lowercase durations such as `30s`, `5m`, or `30m`. Default: `EVE_DEFAULT_INGRESS_TIMEOUT=300s`; range: `1s`-`30m`. Use Eve jobs for longer batch work.
- `ingress.max_body_size` sets nginx-ingress request body size for the same ingress set. Use lowercase sizes such as `512k`, `10m`, or `1g`. Default: `EVE_DEFAULT_INGRESS_MAX_BODY_SIZE=10m`; range: `1k`-`1g`. Use signed uploads/object storage for larger payloads.
- Timeout/body-size annotations are emitted only for `EVE_DEFAULT_INGRESS_CLASS=nginx` or `nginx-ingress`. Traefik/unknown classes keep routing behavior and skip L7 tuning; explicit tuning logs a deploy warning. Confirm live values with `eve env diagnose <project> <env>` or `.http_ingress[]`.
- **Domain ownership is env-scoped with first-bind-wins**: a hostname declared in the base manifest is claimed by the **first environment to deploy with it**. A hostname declared in exactly one env override is sync-bound to that env. Hostnames declared in multiple env overrides keep first-bind-wins and sync warns instead of guessing. Use `eve domain transfer <host> --to <env>` + redeploys to move ownership, or `eve domain register <host> --project <id> --service <svc> --env <env>` for imperative reservations.
- `audit_log_table` is optional. When set, `eve env diagnose --request <id>` runs a read-only query against that table using `request_id_column` and returns matching rows verbatim. Query failures become warnings in the diagnose response.

### Managed DB Services

```yaml
services:
  db:
    x-eve:
      role: managed_db
      managed:
        class: db.p1
        engine: postgres
        engine_version: "16"
        extensions: [postgis, pgvector]
```

Supported plain extensions are `postgis`, `pgvector`, `pg_trgm`, `btree_gist`, `hstore`, and `citext`. `pg_cron` is provider-gated; `timescaledb` is still not declarable on AWS RDS.
Preload-required candidates such as `pg_cron` and `timescaledb` are not declarable yet.

### App Object Store Buckets (`x-eve.object_store`)

Declare S3-compatible buckets for a service. Eve provisions each bucket at
deploy time and injects env vars for the resolved env-wide credential binding.

```yaml
services:
  api:
    x-eve:
      object_store:
        isolation: auto             # auto (default) | irsa | shared
        buckets:
          - name: uploads          # logical name → env var suffix
            visibility: private    # private (default) | public
            cors:
              origins: ["https://app.example.com"]
              methods: [GET, PUT, HEAD, DELETE]
              max_age_seconds: 3600
            lifecycle:
              abort_incomplete_uploads_days: 7
          - name: assets
            visibility: public
```

Buckets are provisioned during deploy, tracked in environment diagnostics with
`isolation_mode`, and fail deploy if the platform cannot create the bucket,
apply public-read policy, or resolve the requested credential binding. Eve
reconciles one binding per env across app services and job services. Local k3d
MinIO uses server-wide CORS (`MINIO_API_CORS_ALLOW_ORIGIN=*`) instead of the S3
per-bucket CORS API. Wildcard CORS works for browser presigned URL flows;
restrictive origins are recorded in diagnostics but are not enforced per bucket
by local MinIO.

Static-key env vars for local MinIO or explicit `shared` mode:
- `STORAGE_ENDPOINT` — MinIO/S3 endpoint
- `STORAGE_REGION`
- `STORAGE_ACCESS_KEY_ID` / `STORAGE_SECRET_ACCESS_KEY` — storage credentials injected for the app
- `STORAGE_BUCKET_<NAME>` — physical bucket name (e.g. `eve-org-myorg-myapp-test-uploads` locally or `demo-eve-app-myorg-myapp-test-uploads` on staging)
- `STORAGE_FORCE_PATH_STYLE` — `true` for MinIO, omitted for AWS S3

IRSA env vars for AWS:
- `STORAGE_ENDPOINT`
- `STORAGE_REGION`
- `STORAGE_AUTH_MODE=irsa`
- `AWS_REGION`
- `STORAGE_BUCKET_<NAME>`

IRSA pods do not receive `STORAGE_ACCESS_KEY_ID` or
`STORAGE_SECRET_ACCESS_KEY`; AWS SDKs use the annotated Kubernetes service
account.

Visibility `public` sets the bucket ACL for anonymous GET access (suitable for static assets).

Isolation resolution:
- `auto` resolves to IRSA when the worker has AWS OIDC/IAM configuration,
  otherwise to `minio-static-key` on local MinIO or `shared` when only static
  app keys are available.
- `irsa` fails fast on non-IRSA clusters.
- `shared` uses static app credentials, resolving to `minio-static-key` on
  local MinIO.

AWS IRSA creates one IAM role per org/project/env and fully replaces its
`app-bucket-access` inline policy with the declared physical bucket names.

### Stable Egress (`x-eve.networking.egress`)

Opt a service into platform-managed stable egress. Use when an app needs
**endpoint-independent UDP source-port mappings** — typically camera relays,
peer-to-peer / hole-punched UDP protocols, STUN-discovered NAT traversal, or
vendors that won't tolerate the cluster NAT Gateway's symmetric port
rewriting.

```yaml
services:
  api:
    x-eve:
      networking:
        egress: stable      # 'nat' (default) | 'stable'
```

| Value | Behavior |
|-------|----------|
| `nat` (default) | Existing path: AWS NAT Gateway on EKS, normal local networking on k3d. |
| `stable` | EKS only: the deployer schedules the pod onto the dedicated `eve.io/egress-pool=stable` node group with `hostNetwork: true` and `dnsPolicy: ClusterFirstWithHostNet`. Traffic exits via the node's own public IPv4 / Internet Gateway, with 1:1 NAT that preserves the kernel-chosen source port across destinations. On k3d, accepted and logged as a no-op. |

**Pod shape on EKS when opted in (no sidecar, no Secret):**
- `hostNetwork: true`, `dnsPolicy: ClusterFirstWithHostNet`.
- `nodeSelector: { eve.io/egress-pool: stable }` and a matching toleration.
- App container gets `EVE_NETWORK_EGRESS=stable`.
- Single container, no extra volumes, no privileged caps.

**Phase 1 limits (deployer fail-fasts at render time):**
- `replicas` must be `1`. Multi-replica hostNetwork services need pod
  anti-affinity + cluster-wide port-collision validation, which is Phase 2.
- Service ports must be **outside** the Kubernetes NodePort range
  (30000–32767). The EKS node SG opens that range from `0.0.0.0/0` for NLB
  traffic, so a hostNetwork pod listening there would be unintentionally
  public.

**Operational notes:**
- Each opt-in pod inherits the IP of the egress node it's scheduled on.
  Phase 1 ships a single-AZ, single-instance pool — node replacement /
  upgrade gives a new public IP. Apps that rely on STUN auto-reconnect
  (vendor-x-class) tolerate this; vendors that allow-list source IPs do not.
  Phase 2 introduces a pre-allocated EIP pool.
- `NetworkPolicy` does not apply to hostNetwork pods — closed-egress
  policies on the namespace are silently bypassed.
- Verify with `eve env diagnose <project> <env>` (the rendered pod has
  `hostNetwork: true` + the `eve.io/egress-pool` selector) and the
  `udp-diag.py` helper in `deployment-instance-repo/scripts/stable-egress/`
  (run inside the pod; same-socket STUN should report
  `endpoint-independent (good)`).

### Service Token Permissions

Every deployed service receives an auto-injected `EVE_SERVICE_TOKEN` with **read-only defaults**. Services that need write access must declare additional permissions:

```yaml
services:
  api:
    x-eve:
      permissions: [jobs:write, events:write, threads:write]
```

**Default permissions** (always included, no declaration needed):
`projects:read`, `jobs:read`, `threads:read`, `envs:read`, `secrets:read`, `builds:read`, `pipelines:read`, `agents:read`, `events:read`

**Common write permissions to opt in to:**

| Permission | Use Case |
|-----------|----------|
| `jobs:write` | Create or update jobs (e.g., trigger workflows) |
| `events:write` | Emit app events (e.g., `question.answered`) |
| `threads:write` | Create or reply to threads |
| `envdb:write` | Write to managed databases via API |
| `notifications:send` | Send Slack channel notifications via `eve notifications send` (see `references/integrations.md`) |

Declared permissions are **merged** with defaults — you only need to list the additional write scopes your service needs.

### API Spec Schema

```yaml
api_spec:
  type: openapi              # openapi | postgrest | graphql
  spec_url: /openapi.json    # relative to service URL, or absolute
  spec_path: ./openapi.yaml  # local file path (file:// repos only)
  name: my-api               # optional display name
  auth: eve                  # eve (default) | none
  on_deploy: true            # refresh on deploy (default: true)
```

Multiple specs:

```yaml
api_specs:
  - type: openapi
    spec_url: /openapi.json
  - type: graphql
    spec_url: /graphql
```

### CLI Declaration

Declare a domain-specific CLI that agents use instead of raw REST calls:

```yaml
x-eve:
  api_spec:
    type: openapi
  cli:
    name: eden                  # binary name on $PATH (lowercase alphanumeric + hyphens)
    bin: cli/bin/eden            # path relative to repo root (repo-bundled mode)
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | CLI binary name. Lowercase alphanumeric + hyphens (`^[a-z][a-z0-9-]*$`). Must be unique per project. |
| `bin` | string | Yes (repo mode) | Path to executable, relative to repo root. |
| `image` | string | Yes (image mode) | Docker image containing CLI binary. |
| `description` | string | No | Brief description shown in agent instruction block. |

**Distribution modes:**

- **Repo-bundled** (primary): CLI is a pre-built single-file executable in the repo (e.g., esbuild bundle). Platform runs `chmod +x` and adds to PATH after clone. Zero additional latency.
- **Image-based**: CLI is distributed via Docker init container (same pattern as toolchains). Platform pulls the image and copies the binary to a shared volume. Adds 2-5s startup latency.

**Auto-discovery**: The platform automatically scans the manifest for services with `x-eve.cli` or `x-eve.api_spec` and injects them into every agent job. No explicit `with_apis` needed — just declare the CLI here and all agents get it on PATH.

When app APIs are resolved (via auto-discovery or explicit `with_apis`), the agent receives:
- The CLI on `$PATH` (ready to run)
- `EVE_APP_API_URL_{SERVICE}` env var (for CLI internal use)
- `EVE_JOB_TOKEN` for auth (CLI reads this automatically)
- A CLI-first instruction block: "Use `eden --help` to see all commands"

See `references/app-cli.md` for the full implementation guide including bundling, env var contract, and testing patterns.

### Cross-Project App Links (`x-eve.app_links`)

App links let one project consume another project's API, image-mode CLI, and
application events without shared long-lived secrets. Producers declare exports;
consumers declare subscriptions.

Producer example:

```yaml
x-eve:
  app_links:
    exports:
      apis:
        observation:
          service: api
          cli: obs
          scopes: [observations:read, deployments:read]
          consumers:
            - project: consumer
              scopes: [observations:read]
              envs: [staging]
      events:
        observation-feed:
          types: [app.observation.created]
          consumers:
            - project: consumer
              types: [app.observation.created]
```

Consumer example:

```yaml
x-eve:
  app_links:
    consumes:
      observation:
        project: producer
        api: observation
        environment: same
        scopes: [observations:read]
        events:
          feed: observation-feed
          types: [app.observation.created]
        inject_into:
          services: [worker]
          jobs: true
```

Rules:
- Project refs can be project IDs (`proj_...`) or same-org project slugs.
- Producer API exports must reference an existing service with `x-eve.api_spec` or `x-eve.api_specs`.
- If an export names `cli`, that service's `x-eve.cli.name` must match and `x-eve.cli.image` is required. Cross-project CLIs use image mode because consumers do not have the producer repo checked out.
- Consumer requested `scopes` and event `types` must be subsets of the active producer grant.
- `environment: same` maps consumer env names to the same producer env names. A concrete value pins `producer_env_name`.
- `inject_into.services` injects app-link env vars into deployed consumer services.
- `inject_into.jobs: true` injects app-link env vars into direct jobs and
  workflow step jobs, including worker-executed `script:` and `run` steps.
  `eve job create --with-links alias1,alias2` can request explicit links for a
  direct job; workflows do not add a separate app-link grammar.
- Local k3d meshes should use one shared env name across all projects, normally
  `environments.local`. `eve local mesh up` fails fast if a project in the
  workspace does not declare the workspace env.
- For local mesh work, workspace project names are Eve project slugs and should
  match `project` refs in producer/consumer app-link blocks.

Injected surfaces receive:
- `EVE_APP_LINK_<ALIAS>_API_URL`
- `EVE_APP_LINK_<ALIAS>_TOKEN`
- `EVE_APP_LINK_<ALIAS>_SCOPES`
- `EVE_APP_LINK_<ALIAS>_PROJECT`
- `EVE_APP_LINK_<ALIAS>_ENV`
- `EVE_APP_LINK_<ALIAS>_CLI` when an exported CLI image is mounted

Diagnostics:

```bash
eve app-links list --project <project>
eve app-links plan --project <consumer> --file .eve/manifest.yaml
eve app-links explain --consumer <consumer> --alias observation
```

### Toolchain Declarations

Agents can declare toolchains they need. Inline agent-runtime and worker
script/action-run jobs provision toolchains on demand before launching the
harness or shell, keeping base runtime images small while making language
runtimes available deterministically.

```yaml
# In eve/agents.yaml
version: 1
agents:
  data-analyst:
    name: Data Analyst
    skill: analyze-data
    harness_profile: claude-sonnet
    toolchains: [python]           # python + uv available at runtime

  doc-processor:
    name: Document Processor
    skill: process-documents
    harness_profile: claude-sonnet
    toolchains: [media]            # ffmpeg + whisper available at runtime

  full-stack:
    name: Full Stack Dev
    skill: full-stack-dev
    harness_profile: claude-opus
    toolchains: [python, rust, java]  # multi-toolchain
```

Available toolchains: `python`, `media`, `rust`, `java`, `kotlin`.

Workflow steps can override agent toolchain defaults:

```yaml
workflows:
  process-document:
    steps:
      - name: process
        agent: doc-processor
        toolchains: [media, python]  # override agent default
```

Toolchain precedence: workflow step `toolchains` > agent `toolchains` > none.

Each toolchain is a small container image (~50-300MB) extracted into
`/opt/eve/toolchains/{name}/`. Inline runtimes use `crane` and the shared
toolchain cache, then prepend toolchain `bin` dirs to `PATH` and inject
per-toolchain `env.sh` variables (for example `JAVA_HOME`, `RUSTUP_HOME`).
Runner-pod mode uses init containers and reports the same
`runtime_meta.toolchains` shape.

Agents without `toolchains` run on the base runtime. If provisioning fails, the
attempt fails with `result_json.error_code = "toolchain_unavailable"`; inspect
`eve job diagnose <job-id>` for `runtime_meta.toolchains` and provisioning logs.
The `full` image (~2.6GB, all toolchains baked in) remains available via
`EVE_WORKER_VARIANT=full` for worker deployments that still need it.

### Cloud FS Mounts

Manifest can reference cloud filesystem mounts (Google Drive) connected at the org level. Cloud FS mounts are managed via the `eve cloud-fs` CLI, not declared in the manifest directly.

```bash
# Mount a Google Drive folder
eve cloud-fs mount \
  --provider google-drive \
  --folder-id <drive-folder-id> \
  --mode read_write \
  --label "Engineering Shared Drive"

# List mounts
eve cloud-fs list

# Browse files in a mount
eve cloud-fs ls / --mount <mount-id>
eve cloud-fs ls /subfolder --mount <mount-id>          # alias: browse

# Search across mounts
eve cloud-fs search <query> [--mount <mount-id>]

# Show mount details
eve cloud-fs show <mount-id>

# Update mount settings
eve cloud-fs update <mount-id> --mode read_only

# Remove a mount
eve cloud-fs unmount <mount-id>                        # aliases: remove, delete
```

Mounts are stored in the `cloud_fs_mounts` table, scoped to org (or optionally project). Each mount links an integration's OAuth credentials to a provider folder with configurable mode (`read_only`, `write_only`, `read_write`) and optional auto-indexing into org docs.

Requires a Google Drive integration connection first (`eve integrations connect google-drive`). See Per-Org OAuth Configs below.

### Per-Org OAuth Configs

Each org brings its own OAuth app credentials for external providers (Google Drive, Slack). No cluster-level OAuth secrets required.

```bash
# View setup instructions (shows redirect URI to register)
eve integrations setup-info google-drive
eve integrations setup-info slack

# Register OAuth app credentials for your org
eve integrations configure google-drive \
  --client-id "xxx.apps.googleusercontent.com" \
  --client-secret "GOCSPX-xxx"

eve integrations configure slack \
  --client-id "12345.67890" \
  --client-secret "abc123" \
  --signing-secret "def456" \
  --app-id "A0123ABC"

# View current config (secrets redacted)
eve integrations config google-drive

# Remove config
eve integrations unconfigure google-drive

# Then connect as before (uses per-org credentials)
eve integrations connect google-drive
```

One OAuth app config per provider per org. Multiple connections (integrations) share the same app config. The platform stores credentials in `oauth_app_configs` and uses them for all OAuth authorize, callback, and token refresh flows. Cluster-level `EVE_GOOGLE_CLIENT_*` / `EVE_SLACK_CLIENT_*` env vars are deprecated.

### Files Mount

Mount source files from the repo into the container:

```yaml
x-eve:
  files:
    - source: ./config/app.conf    # relative path in repo
      target: /etc/app/app.conf    # absolute path in container
```

### Persistent Storage

```yaml
x-eve:
  storage:
    mount_path: /data
    size: 10Gi
    access_mode: ReadWriteOnce     # ReadWriteOnce | ReadWriteMany | ReadOnlyMany
    storage_class: standard        # optional
    name: my-data                  # optional PVC name
```

### Healthcheck

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 5s
  timeout: 3s
  retries: 3
  start_period: 10s
```

### Dependency Conditions

```yaml
depends_on:
  db:
    condition: service_healthy     # service_started | service_healthy | started | healthy
```

## Platform Environment Variables

Eve automatically injects these variables into all deployed services:

| Variable | Description |
|----------|-------------|
| `EVE_API_URL` | Internal cluster URL for server-to-server calls (e.g., `http://eve-api:4701`) |
| `EVE_PUBLIC_API_URL` | Public ingress URL for browser-facing apps (e.g., `https://api.eve.example.com`) |
| `EVE_SSO_URL` | SSO broker URL for user authentication (e.g., `https://sso.eve.example.com`) |
| `EVE_PROJECT_ID` | The project ID (e.g., `proj_01abc123...`) |
| `EVE_ORG_ID` | The organization ID (e.g., `org_01xyz789...`) |
| `EVE_ENV_NAME` | The environment name (e.g., `staging`, `production`) |

Job runners also receive `EVE_ENV_NAMESPACE`, but service containers do not.
Services can override these values by defining them explicitly in their `environment` section.

**Which API URL to use:**

- Use `EVE_API_URL` for backend/server-side calls from your container to the Eve API (internal cluster networking).
- Use `EVE_PUBLIC_API_URL` for browser/client-side calls or any code running outside the cluster.

```javascript
// Server-side: call Eve API from your backend
const eveApiUrl = process.env.EVE_API_URL;

// Client-side: expose to browser for frontend API calls
const publicApiUrl = process.env.EVE_PUBLIC_API_URL;
```

## Environments

```yaml
environments:
  staging:
    pipeline: deploy
    pipeline_inputs:
      smoke_test: true
    approval: required
    overrides:
      services:
        api:
          environment:
            NODE_ENV: staging
    workers:
      - type: default
        service: worker
        replicas: 2
```

### Environment Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `persistent` (default) or `temporary` |
| `kind` | string | `standard` (default) or `preview` (PR envs) |
| `pipeline` | string | Pipeline name to trigger on deploy |
| `pipeline_inputs` | object | Inputs passed to pipeline (CLI `--inputs` wins on conflict) |
| `approval` | string | `required` to gate deploys |
| `overrides` | object | Compose-style service overrides |
| `workers` | array | Worker pool configuration |
| `labels` | object | Metadata (PR info for preview envs) |

### Environment Pipeline Behavior

When `pipeline` is configured for an environment, `eve env deploy <env> --ref <sha>` triggers a pipeline run instead of performing a direct deployment. This enables:

- Consistent build/test/deploy workflows across environments
- Promotion patterns where staging/production reuse releases from test
- Environment-specific pipeline inputs and approval gates

To bypass the pipeline and perform a direct deployment, use `--direct`:

```bash
eve env deploy staging --ref 0123456789abcdef0123456789abcdef01234567 --direct
```

### Promotion Example

Define environments that share a pipeline but vary in inputs and approval gates:

```yaml
environments:
  test:
    pipeline: deploy-test
  staging:
    pipeline: deploy
    pipeline_inputs:
      smoke_test: true
  production:
    pipeline: deploy
    approval: required
```

Deploy flow:

```bash
# Build + test + release in test
eve env deploy test --ref 0123456789abcdef0123456789abcdef01234567

# Promote to staging (reuse release, no rebuild)
eve release resolve v1.2.3  # Get release_id from test
eve env deploy staging --ref 0123456789abcdef0123456789abcdef01234567 --inputs '{"release_id":"rel_xxx"}'

# Promote to production (approval required)
eve env deploy production --ref 0123456789abcdef0123456789abcdef01234567 --inputs '{"release_id":"rel_xxx"}'
```

This pattern enables build-once, deploy-many promotion workflows without rebuilding images.

## Pipelines (Steps)

```yaml
pipelines:
  deploy-test:
    steps:
      - name: migrate
        action: { type: job, service: migrate }
      - name: deploy
        depends_on: [migrate]
        action: { type: deploy }
```

Step types: `action`, `script`, `agent`, or shorthand `run`.

Pipeline `toolchains` can be declared at pipeline root or step level. Valid
values are `python`, `media`, `rust`, `java`, and `kotlin`. Script, shorthand
`run`, agent, and `action: { type: run }` steps resolve `step.toolchains >
pipeline.toolchains > []`. Non-run actions cannot declare step-level
toolchains, and `action.toolchains` is rejected. The resolved value is stored on
`jobs.hints.toolchains`, provisioned before execution, and reported in
`runtime_meta.toolchains`.

See `references/pipelines-workflows.md` for step types, triggers, and the canonical build-release-deploy pattern.

## Workflows

```yaml
workflows:
  nightly-audit:
    db_access: read_only
    hints:
      gates: ["remediate:proj_xxx:staging"]
    steps:
      - name: prepare
        script:
          run: "eve job list --json"
          timeout_seconds: 60
      - agent:
          prompt: "Audit error logs"
```

Workflow invocation creates a root container job with the workflow hints merged,
then creates one child job per step. Each step must define exactly one execution
kind: `agent`, `script`, or shorthand `run`. `script` and `run` workflow steps
materialize as worker-executed script jobs. Workflow `action` steps are reserved
for future support and are rejected at invoke time.

Workflow `toolchains` can be declared at workflow root or step level. Script and
shorthand `run` steps resolve `step.toolchains > workflow.toolchains > []`.
Agent steps resolve `step.toolchains > agent config toolchains >
workflow.toolchains > []`. The resolved value is stored on
`jobs.hints.toolchains`, provisioned before execution, and appears in
`runtime_meta.toolchains` through `eve job diagnose`.

### Multi-Step Workflow Syntax

Workflows support multi-step DAGs that expand into child jobs at invocation time:

```yaml
workflows:
  ingestion-pipeline:
    with_apis:
      - service: coordinator
        description: Coordinator API for orchestration
    steps:
      - name: ingest
        agent:
          name: ingestion
      - name: extract
        depends_on: [ingest]
        agent:
          name: extraction
      - name: review
        depends_on: [extract]
        agent:
          name: reviewer
```

| Field | Type | Description |
|-------|------|-------------|
| `steps[].name` | string | Unique step identifier (required when using `depends_on`) |
| `steps[].depends_on` | string[] | Step names this step blocks on |
| `steps[].condition` | string | Conditional execution: `step_name.status == 'value'` or `!= 'value'` (skip step if false) |
| `steps[].agent` | object | Agent ref: `name`, optional `prompt`/`prompt_file`, `harness`, `harness_profile`, `toolchains` |
| `steps[].script` | object | Worker-executed script step; accepts `run` or `command` plus optional `timeout`/`timeout_seconds` |
| `steps[].run` | string | Shorthand for `steps[].script.run`; creates a script child job |
| `steps[].toolchains` | string[] | Step-level toolchains (`python`, `media`, `rust`, `java`, `kotlin`) |
| `steps[].harness` | string | Step-level harness override (takes precedence over agent-resolved value) |
| `steps[].harness_options` | object | Step-level harness options: `model`, `reasoning_effort`, `temperature` (passthrough) |
| `steps[].harness_profile` | string | Named profile reference; supports `${inputs.<key>}` template expressions |
| `steps[].harness_profile_override` | object | Inline profile override: `{ harness, model?, reasoning_effort?, variant?, temperature? }` |
| `steps[].git` | object | Step git controls (`ref`, `ref_policy`, `branch`, `create_branch`, `commit`, `push`, `remote`); overrides workflow-level `git` |
| `steps[].resource_refs` | string \| string[] \| object | Step resource policy; overrides workflow-level policy |
| `steps[].env_overrides` | object | Step env overrides; merged over workflow-level defaults |
| `steps[].scope` | object | Step job token scope; intersected with workflow/invocation scope |
| `inputs` | object | Workflow-level named inputs. Each entry: `{ from?: 'event.payload.<path>', default?: any }` |
| `env` | string | Workflow environment name; persisted on root/step jobs and used to resolve env-scoped APIs and app links |
| `git` | object | Default job git controls inherited by steps unless overridden |
| `resource_refs` | string \| string[] \| object | Default invocation resource policy for all workflow steps |
| `env_overrides` | object | Default env overrides applied to every workflow step |
| `scope` | object | Default job token scope applied to every workflow step |
| `toolchains` | string[] | Default toolchains for workflow steps |
| `with_apis` | object[] | API specs attached to the workflow — `{ service, description }` (workflow-level or per-step) |
| `db_access` | string | `read_only` or `read_write` |
| `hints` | object | Merged into the root job at invocation time (gates, timeouts, harness prefs) |
| `trigger` | object | Event trigger for automatic invocation (see `references/pipelines-workflows.md`) |

`resource_refs` controls which invocation resources are hydrated into each
step workspace:

```yaml
workflows:
  create-design:
    resource_refs: inherit  # default; "all" also works
    steps:
      - name: read-sources
        agent: { name: designer }
      - name: publish
        depends_on: [read-sources]
        resource_refs: none
        agent: { name: publisher }

  scoped-review:
    resource_refs:
      mode: selected
      include: [brief, design-system]
    steps:
      - name: review
        agent: { name: reviewer }
```

Allowed values:
- `inherit` / `all`: pass all invocation refs to each step.
- `none`: pass no invocation refs.
- string array: select refs by `name`, `label`, `mount_path`, `uri`, or `metadata.name`.
- object form: `{ mode: selected, include: [...] }`.

Step-level policy overrides workflow-level policy. If omitted everywhere, every
step inherits all invocation refs, including dependent steps.

`env_overrides` can be declared at workflow level and step level. Invocation
flags from `eve workflow run|invoke --env-override KEY=VALUE` are merged in at
run time. Precedence is invocation > step YAML > workflow YAML. Values may be
literals or `${secret.KEY}` placeholders; unsupported `${env.X}` style
expressions and reserved Eve runtime variables are rejected. The merged object is
persisted on each executable step job, not on the root workflow container job.
Secret placeholders are resolved only inside worker or agent-runtime before the
harness process starts.

Workflow and step `scope` blocks narrow the job token and org filesystem mount.
Supported axes are `orgfs`, `orgdocs`, `envdb`, and `cloud_fs`:

```yaml
workflows:
  scoped-review:
    scope:
      orgfs:
        allow_prefixes: [/groups/projects/proj-a/**]
    steps:
      - name: review
        agent: { name: reviewer }
        scope:
          cloud_fs:
            allow_mount_ids: [mount_a]
```

Workflow, step, and invocation scopes are intersected for each executable step
job and persisted as `jobs.token_scope`. Request-supplied scope requires
`jobs:harness_override`. There is no CLI `--scope-*` flag yet.

```yaml
workflows:
  research:
    env_overrides:
      WEB_SEARCH_API_KEY: ${secret.WEB_SEARCH_API_KEY}
    steps:
      - name: search
        agent: { name: researcher }
      - name: publish
        depends_on: [search]
        env_overrides:
          PUBLISH_API_KEY: ${secret.PUBLISH_API_KEY}
        agent: { name: publisher }
```

**Conditional steps and step-level harness**:

```yaml
workflows:
  triage-and-deepen:
    inputs:
      model:
        from: event.payload.meta.brand
        default: claude
    steps:
      - name: triage
        agent: { name: fast-triage }
        harness: claude
        harness_options:
          model: sonnet
          reasoning_effort: medium
      - name: deep-analysis
        depends_on: [triage]
        condition: "triage.status == 'complex'"
        harness_profile: ${inputs.model}
        agent: { name: deep-analyzer }
```

`condition` format is `step_name.status == 'value'` or `!= 'value'`, evaluated
against `result_json.eve.status` of the referenced step (which must be in
`depends_on`). Skipped steps count as `done` for downstream resolution. Step
`harness`/`harness_options`/`harness_profile` override agent-resolved values
and may carry `${inputs.<key>}` template expressions that resolve at
invocation time.

**Validation** (`eve manifest validate` and `eve project sync` check workflows):
- Duplicate step names → error.
- Cyclic dependencies → error (reports cycle path).
- Invalid `depends_on` references → error.
- Trigger with no recognized type → warning.
- Invalid GitHub event type → warning.
- Unknown system event type → warning.
- Cron trigger with missing schedule → warning.
- Invalid condition format → error.
- Condition references non-existent step → error.
- Condition step not in `depends_on` → error.

**Pack workflow merging**: When packs define workflows, they are merged into the
repo manifest before sync (single POST). Pack workflows overlay repo-manifest
workflows — pack definitions take precedence on name collision.

See `references/pipelines-workflows.md` for expansion behavior, response format, and job tree view.

## Secret Requirements and Validation

Declare required secrets at the top level or per pipeline step:

```yaml
x-eve:
  requires:
    secrets: [GITHUB_TOKEN, REGISTRY_TOKEN]

pipelines:
  ci-cd-main:
    steps:
      - name: integration-tests
        script:
          run: "pnpm test"
        requires:
          secrets: [DATABASE_URL]
```

Validate secrets before syncing:

```bash
eve project sync --validate-secrets     # Warn on missing secrets
eve project sync --strict               # Fail on missing secrets
eve manifest validate                   # Schema + secret validation without syncing
```

Use `eve manifest validate` for pre-flight checks against a local manifest or the latest synced version. Required keys follow standard scope resolution rules.
`${secret.KEY}` references in workflow-level or step-level `env_overrides` are included in the same validation.

### Platform-Injected Environment Variables

The deployer automatically injects these env vars into every deployed service.
**Do NOT redeclare them as `${secret.*}` in the manifest** — that overrides the
platform value with an empty string when the secret isn't configured.

| Variable | Value | Notes |
|----------|-------|-------|
| `EVE_API_URL` | Platform API URL (K8s in-cluster) | Auto-resolved |
| `EVE_PROJECT_ID` | Project TypeID | Auto-resolved |
| `EVE_ORG_ID` | Org TypeID | Auto-resolved |
| `EVE_ENV_NAME` | Environment name (e.g., `sandbox`) | Auto-resolved |
| `EVE_SERVICE_TOKEN` | 90-day JWT (type: `service`) | Minted per-deploy, refreshed automatically |
| `EVE_PUBLIC_API_URL` | Public API URL (if configured) | Optional |
| `EVE_SSO_URL` | SSO URL (if configured) | Optional |

The service token carries **read-only default permissions** (`projects:read`,
`jobs:read`, `threads:read`, etc.). Apps that need write access must declare
additional permissions via `x-eve.permissions` — see [Service Token Permissions](#service-token-permissions).

User-defined env vars in the manifest override platform vars, so only declare
`EVE_*` vars if you need a different value than the platform default.

### Secret Interpolation

Interpolate secrets in environment variables:

```yaml
environment:
  DATABASE_URL: postgres://user:${secret.DB_PASSWORD}@db:5432/app
```

Also supported (runtime interpolation): `${ENV_NAME}`, `${PROJECT_ID}`, `${ORG_ID}`, `${ORG_SLUG}`, `${COMPONENT_NAME}`, `${SSO_URL}`, `${secret.KEY}`, `${managed.<service>.<field>}`.

### Internal Service URLs

Apps with multiple services often need to call their own API internally (e.g., to emit events back to themselves). Use `${ENV_NAME}` with K8s service DNS naming:

```yaml
environment:
  MY_API_URL: "http://${ENV_NAME}-api:3000"
```

The pattern is `${ENV_NAME}-{service_key}:{port}`. This resolves to the in-cluster service address — no ingress, no CORS, no public exposure. Essential for apps that trigger workflows via their own API.

## Manifest Defaults (`x-eve.defaults`)

Default job settings applied on creation (job fields override defaults). Default environment should be **staging** unless explicitly overridden:

```yaml
x-eve:
  defaults:
    env: staging
    harness: mclaude
    harness_profile: primary-orchestrator
    harness_options:
      model: opus-4.5
      reasoning_effort: high
    hints:
      permission_policy: auto_edit
      resource_class: job.c1
      max_cost:
        currency: usd
        amount: 5
      max_tokens: 200000
    git:
      ref_policy: auto
      branch: job/${job_id}
      create_branch: if_missing
      commit: manual
      push: never
    workspace:
      mode: job
```

`hints` can include budgeting and accounting fields such as `resource_class`,
`max_cost`, and `max_tokens`. These map to scheduling hints and per-attempt
budget enforcement.

## Project Agent Profiles (`x-eve.agents`)

Define harness profiles used by orchestration skills:

```yaml
x-eve:
  agents:
    version: 1
    availability:
      drop_unavailable: true
    profiles:
      primary-reviewer:
        - harness: mclaude
          model: opus-4.5
          reasoning_effort: high
        - harness: codex
          model: gpt-5.2-codex
          reasoning_effort: x-high
```

For pack-distributed profiles, define them in `eve/x-eve.yaml` and import via `pack.yaml`:

```yaml
# eve/x-eve.yaml
version: 1
agents:
  profiles:
    coordinator:
      - harness: claude
        model: sonnet
        reasoning_effort: medium
    expert:
      - harness: claude
        model: sonnet
        reasoning_effort: high
```

Profiles in `eve/x-eve.yaml` are distributed with the pack. Profiles in the manifest are project-local only.

## AgentPacks (`x-eve.packs` + `x-eve.install_agents`)

AgentPacks import agent/team/chat config and skills from pack repos. Packs are
resolved by `eve agents sync` and locked in `.eve/packs.lock.yaml`.

```yaml
x-eve:
  install_agents: [claude-code, codex, gemini-cli]  # defaults to [claude-code]
  packs:
    - source: ./skillpacks/my-pack
    - source: eve-horizon/eve-skillpacks
      ref: 0123456789abcdef0123456789abcdef01234567
    - source: ./skillpacks/claude-only
      install_agents: [claude-code]
```

Notes:
- Remote pack sources require a 40-char git SHA `ref`.
- Packs can be full AgentPacks (`eve/pack.yaml`) or skills-only packs.
- Local packs use relative paths (resolved from repo root).

### Full AgentPack Descriptor (`eve/pack.yaml`)

A full AgentPack declares its resources via an `imports` map and optional gateway defaults:

```yaml
# eve/pack.yaml
version: 1
id: my-pack
imports:
  agents: eve/agents.yaml
  teams: eve/teams.yaml
  workflows: eve/workflows.yaml
  chat: eve/chat.yaml
  x_eve: eve/x-eve.yaml
gateway:
  default_policy: none
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | number | Schema version (currently `1`) |
| `id` | string | Unique pack identifier |
| `imports` | object | Map of resource type to relative YAML file path |
| `imports.agents` | string | Agent definitions file |
| `imports.teams` | string | Team definitions file |
| `imports.workflows` | string | Workflow definitions (merged with manifest workflows at sync) |
| `imports.chat` | string | Chat route definitions |
| `imports.x_eve` | string | Harness profiles and agent config |
| `gateway` | object | Gateway defaults for the pack |
| `gateway.default_policy` | string | Default gateway policy for pack agents (`none`, `discoverable`, `routable`) |

All `imports` paths are relative to the pack root. Only declare the imports your pack needs — all fields are optional.

### Pack Lock File

`.eve/packs.lock.yaml` tracks resolved state:

```yaml
resolved_at: "2026-02-09T..."
project_slug: myproject
packs:
  - id: pack-id
    source: eve-horizon/eve-skillpacks
    ref: 0123456789abcdef0123456789abcdef01234567
    pack_version: 1
effective:
  agents_count: 5
  teams_count: 2
  routes_count: 3
  profiles_count: 4
```

### Pack Overlay Customization

Local YAML overlays pack defaults using deep merge + `_remove`:

```yaml
# In local agents.yaml
version: 1
agents:
  pack-agent:
    harness_profile: my-override       # override pack default
  unwanted-agent:
    _remove: true                       # remove from pack
```

### Pack CLI

```bash
eve packs status [--repo-dir <path>]           # Show lockfile + drift
eve packs resolve [--dry-run] [--repo-dir <path>]  # Preview resolution
```

## Project Bootstrap

Bootstrap creates a project + environments in a single API call:

```bash
eve project bootstrap --name my-app --repo-url https://github.com/org/repo \
  --environments staging,production
```

API: `POST /projects/bootstrap` with body:
- `org_id`, `name`, `repo_url`, `branch` (required)
- `slug`, `description`, `template`, `packs`, `environments` (optional)

Idempotent — re-calling with the same name returns the existing project.

## Ingress Defaults

If a service exposes ports and the cluster domain is configured, Eve creates ingress by default.
Set `x-eve.ingress.public: false` to disable.

URL pattern: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`

### Custom Domains

Bring your own domain by adding `domains` to the ingress config:

```yaml
services:
  web:
    x-eve:
      ingress:
        public: true
        alias: myapp              # myapp.eve.example.com (platform subdomain)
        domains:
          - myapp.com             # custom domain (A record)
          - www.myapp.com         # custom domain (CNAME)
```

Env-specific domains belong in environment service overrides:

```yaml
environments:
  sandbox:
    overrides:
      services:
        web:
          x-eve:
            ingress:
              domains:
                - sandbox.myapp.com
```

**Lifecycle**: `pending_dns` → `dns_verified` → `cert_provisioning` → `active`. Domains are auto-registered during `eve project sync`; env-override domains declared in exactly one env are also bound to that env during sync. After setting up DNS, run `eve domain verify <hostname>` — it performs real DNS resolution server-side and transitions the status to `dns_verified`. Redeploy to create the Ingress and provision the TLS cert. Use `eve domain register <host> --project <id> --service <svc> --env <env>` for manual reservations that are not in the manifest.

**DNS**: Apex domains (`myapp.com`) require an A record pointing to the platform ingress IP. Subdomains (`www.myapp.com`) can use a CNAME to the platform ingress hostname.

**TLS**: Custom domains use `cert-manager.io/cluster-issuer` (HTTP-01 challenge), NOT the platform wildcard cert (`EVE_DEFAULT_TLS_SECRET`). The ClusterIssuer must support HTTP-01 challenges.

## Public TCP Ingress

Use service `x-eve.tcp_ingress` for raw L4 TCP protocols such as device
trackers. This is separate from HTTP ingress and renders a Kubernetes
`Service` of type `LoadBalancer` labelled `eve.tcp_ingress=true`.

```yaml
services:
  device-edge:
    image: ghcr.io/acme/device-edge:latest
    ports: [33400, 33500]
    x-eve:
      tcp_ingress:
        hostname: trackers
        allow_cidrs:
          - 0.0.0.0/0
        listeners:
          - name: a1-gt06
            port: 33400
          - name: mictrack-mt700
            port: 33500
```

Rules:
- `listeners` is required and supports 1-20 entries.
- Listener names must be lowercase alphanumeric with hyphens.
- Each listener `port` must also appear in top-level service `ports`.
- Listener ports cannot use the Kubernetes NodePort range `30000-32767`.
- `allow_cidrs` is optional and becomes `loadBalancerSourceRanges`.
- `hostname` is an optional platform alias under `EVE_TCP_INGRESS_HOSTED_ZONE`
  or `EVE_DEFAULT_DOMAIN`; without it Eve advertises a generated service host.

TCP aliases share the same global claim and reserved-name rules as HTTP ingress
aliases. A manifest cannot declare the same alias for both HTTP and TCP.

The app container receives `EVE_TCP_PUBLIC_HOST` plus listener-specific env vars:
`EVE_TCP_LISTENER_<NAME>_PORT` and `EVE_TCP_LISTENER_<NAME>_HOST`, where hyphens
in `<NAME>` are converted to underscores and the value is uppercased.

Providers:
- `EVE_TCP_INGRESS_PROVIDER=none`: validate only; render no public TCP service.
- `EVE_TCP_INGRESS_PROVIDER=klipper`: local k3d/k3s LoadBalancer.
- `EVE_TCP_INGRESS_PROVIDER=aws-nlb`: internet-facing AWS NLB; requires the AWS
  Load Balancer Controller.

Diagnostics:

```bash
eve env diagnose <project> <env>                       # TCP Ingress table
eve env diagnose <project> <env> --json | jq '.tcp_ingress'
eve tcp-ingress test <project> <env> --listener a1-gt06
```

For local k3d, create the cluster with the raw TCP ports mapped:

```bash
./bin/eh k8s start --tcp-ports 33400,33500 --recreate
```

## App Undeploy & Delete

Full lifecycle operations for environments, projects, and orgs.

### Environment Undeploy

Take an environment offline without losing config. Tears down K8s resources but preserves the environment record for redeployment.

```bash
eve env undeploy <env> --project <id>
eve env show <project> <env> --json   # Verify deploy_status = 'undeployed'
```

Redeploy later with `eve env deploy <env> --ref <sha>`. The `deploy_status` field tracks state: `unknown`, `deployed`, `undeployed`, `deploying`, `undeploying`, `failed`.

### Project Delete

```bash
eve project delete <project>           # Soft-delete (sets deleted_at)
eve project delete <project> --hard    # Hard-delete: cascades through all resources
eve project delete <project> --hard --force  # Continue on partial failures
```

Hard delete sequence: undeploy all environments, delete environments (triggers managed DB cleanup), cascade-delete jobs/pipeline-runs/releases/builds/agents/teams/threads, delete project record.

### Org Delete

```bash
eve org delete <org>                   # Soft-delete
eve org delete <org> --hard --force    # Full tenancy teardown
```

Cascades through all projects and environments in the org.

### Resource Cleanup

Individual resource delete and prune commands:

```bash
eve build delete <id>                  # Delete a single build
eve build prune --project <id> --keep 10  # Keep last N, delete rest
eve release delete <id>
eve release prune --project <id> --keep 10
eve pipeline delete <name> --project <id>
eve agents delete <name> --project <id>
eve thread delete <id>
```
