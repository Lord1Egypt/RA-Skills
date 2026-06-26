---
name: eve-manifest-authoring
description: Author and maintain Eve manifest files (.eve/manifest.yaml) for services, environments, pipelines, workflows, and secret interpolation. Use when changing deployment shape or runtime configuration in an Eve-compatible repo.
---

# Eve Manifest Authoring

Keep the manifest as the single source of truth for build and deploy behavior.

## Minimal skeleton (v2)

```yaml
schema: eve/compose/v2
project: my-project

registry: "eve"  # Use managed registry by default for Eve apps
services:
  api:
    build:
      context: ./apps/api           # Build context directory
      dockerfile: Dockerfile        # Optional, defaults to context/Dockerfile
    # image omitted by default; when build is present, Eve derives image name from service key
    ports: [3000]
    environment:
      NODE_ENV: production
    x-eve:
      ingress:
        public: true
        port: 3000

environments:
  staging:
    pipeline: deploy
    pipeline_inputs:
      some_key: default_value

pipelines:
  deploy:
    steps:
      - name: build
        action:
          type: build               # Builds all services with build: config
      - name: release
        depends_on: [build]
        action:
          type: release
      - name: deploy
        depends_on: [release]
        action:
          type: deploy
```

## Registry Image Labels

Some registries require package metadata for permission and ownership inheritance.
Add these labels to your Dockerfiles when supported by your registry:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/YOUR_ORG/YOUR_REPO"
LABEL org.opencontainers.image.description="Service description"
```

**Why this matters**: Metadata helps preserve repository ownership and improves traceability. The Eve builder injects these labels automatically, but including them in your Dockerfile is still recommended.

For multi-stage Dockerfiles, add the labels to the **final** stage (the production image).

## Registry Modes

```yaml
registry: "eve"     # Eve-native registry (internal JWT auth)
registry: "none"    # Disable registry handling (public images)
registry:           # BYO registry (full object — see section below)
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth: { username_secret: REGISTRY_USERNAME, token_secret: REGISTRY_PASSWORD }
```

For BYO/private registries, provide:

```yaml
registry:
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth:
    username_secret: REGISTRY_USERNAME
    token_secret: REGISTRY_PASSWORD
```

## Managed Databases

Declare platform-provisioned databases with `x-eve.role: managed_db`:

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

Not deployed to K8s — provisioned by the orchestrator on first deploy.
Reference managed values elsewhere: `${managed.db.url}`.

## Eve-Migrate for Database Migrations

Use the platform's migration runner instead of Flyway, TypeORM, or Knex. It uses plain SQL files with timestamp prefixes, tracked in `schema_migrations`:

```yaml
services:
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
```

Migration files: `db/migrations/20260312000000_initial_schema.sql`. The `x-eve.files` directive mounts them into the container at `/migrations`.

In the pipeline, the migrate step must run **after deploy** (managed DB needs provisioning):

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

For local dev, use the same image via Docker Compose for parity:

```yaml
# docker-compose.yml
services:
  migrate:
    image: ghcr.io/eve-horizon/eve-migrate:latest
    environment:
      DATABASE_URL: postgres://app:app@db:5432/myapp
    volumes:
      - ./db/migrations:/migrations:ro
    depends_on:
      db: { condition: service_healthy }
```

## Legacy manifests

If the repo still uses `components:` from older manifests, migrate to `services:`
and add `schema: eve/compose/v2`. Keep ports and env keys the same.

## Services

- Provide `image` and optionally `build` (context and dockerfile).
- Use `ports`, `environment`, `healthcheck`, `depends_on` as needed.
- Use `x-eve.external: true` and `x-eve.connection_url` for externally hosted services.
- Use `x-eve.role: job` for one-off services (migrations, seeds). For database migrations, prefer Eve's `eve-migrate` image (see below).

### Build configuration

Services with Docker images should define their build configuration:

```yaml
services:
  api:
    build:
      context: ./apps/api           # Build context directory
      dockerfile: Dockerfile        # Optional, defaults to context/Dockerfile
    # image: api      # optional if using build; managed registry derives this
    ports: [3000]
```

Note: Every deploy pipeline should include a `build` step before `release`. The build step creates tracked BuildSpec/BuildRun records and produces image digests that releases use for deterministic deployments.

## Local dev alignment

- Keep service names and ports aligned with Docker Compose.
- Prefer `${secret.KEY}` and use `.eve/dev-secrets.yaml` for local values.

## Environments, pipelines, workflows

- Link each environment to a pipeline via `environments.<env>.pipeline`.
- When `pipeline` is set, `eve env deploy <env>` triggers that pipeline instead of direct deploy.
- Use `environments.<env>.pipeline_inputs` to provide default inputs for pipeline runs.
- Override inputs at runtime with `eve env deploy <env> --ref <sha> --inputs '{"key":"value"}' --repo-dir ./my-app`.
- Use `--direct` flag to bypass pipeline and do direct deploy: `eve env deploy <env> --ref <sha> --direct --repo-dir ./my-app`.
- Pipeline steps can be `action`, `script`, or `agent`.
- Use `action.type: create-pr` for PR automation when configured.
- Workflows live under `workflows` and are invoked via CLI; `db_access` is honored.
- Workflow steps support `harness`, `harness_profile`, and `harness_options` per step (overrides agent-resolved values), `condition` for skip-if-false gating against upstream step status, and `git` controls (now correctly materialized at dispatch). See `references/manifest.md` for the full step shape.
- Workflow- and step-level `scope` blocks narrow the step job token and org filesystem mount. Supported axes: `orgfs`, `orgdocs`, `envdb`, `cloud_fs`. Step scope intersects workflow scope — invocation scope may narrow but not widen. Use it to grant a step exactly the paths/tables/mounts it needs, default-deny everything else.

```yaml
workflows:
  create-design:
    scope:
      orgfs: { allow_prefixes: [/groups/projects/proj-a/**] }
    steps:
      - name: publish
        scope:
          cloud_fs: { allow_mount_ids: [mount_a] }
        agent: { name: publisher }
```

Request-supplied `scope` (workflow invoke API body) requires `jobs:harness_override`. No `--scope-*` CLI flag yet.

## Custom Domains and Stable Egress

Bring-your-own hostnames and opt-in network shape are declared per service:

```yaml
services:
  api:
    x-eve:
      ingress:
        public: true
        port: 3000
        domains: ["app.example.com", "www.example.com"]    # max 10
      networking:
        egress: stable    # default 'nat'; opt in only when a vendor needs allowlisted source IPs
```

- `ingress.domains` are bound on first deploy: the **first env** to deploy with a hostname owns it; other envs that reference the same hostname log `owned by environment "<A>"` and skip rendering. Operate ownership with `eve domain list|verify|status|transfer|unbind|remove` (see `eve-deploy-debugging`).
- `networking.egress: stable` schedules the pod on the stable-egress node group with `hostNetwork: true`. It bypasses NAT and constrains scheduling — only opt in when needed.

See `references/manifest.md` for the full field shape (validation rules, max counts, per-env overrides).

## Project Branding And Auth

App-facing login, invite emails, and magic-link emails are project-scoped and declared in `x-eve.branding` / `x-eve.auth`. `eve project sync` writes both onto the project record; the SSO broker and Eve API mailer read from there.

### `x-eve.branding` — invite + magic-link email branding

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"                                    # required, <=60 chars
    app_logo_url: "https://app.example.com/logo.svg"          # https only on emitted mail
    primary_color: "#1f6feb"                                  # six-digit hex
    email_from_name: "ACME Portal"                              # From-name header
    reply_to_email: "support@example.com"
    support_email: "support@example.com"
    support_url: "https://example.com/help"
```

`email_from_name`, `reply_to_email`, `support_email` set headers on app-scoped mail while keeping the platform's verified sender address. Phase 1 emits logo + name + primary color in invite and magic-link templates.

### `x-eve.auth.login_method: magic_link` — passwordless apps

```yaml
x-eve:
  auth:
    login_method: magic_link            # password_or_magic_link | password | magic_link
    self_signup: false
    invite_requires_password: false
```

Opt in per project. With `magic_link`, the SSO login page hides password and signup, and Eve API sends branded magic-link mail via `POST /auth/magic-link` (not GoTrue direct), so unknown emails get generic success without creating a GoTrue user when `self_signup: false`. With `invite_requires_password: false`, invite acceptance establishes the session and skips `/set-password`. Use `password_or_magic_link` to keep password login plus a secondary branded magic-link control.

### `x-eve.auth.org_access.domain_signup` — pre-approved email domains

```yaml
x-eve:
  auth:
    org_access:
      mode: allowlist
      allowed_orgs: [org_acme, org_partner]
      domain_signup:
        enabled: true
        domains:
          - { domain: acme.com,   target_org: org_acme,  role: member }
          - { domain: partner.example,  target_org: org_partner }
          - { domain: "*.acme.com", target_org: org_acme }  # wildcard; apex needs its own rule
```

v2 shape (2026-05-12). Each `domains[]` entry is an object with its own required `target_org`; the legacy list-of-strings + block-level `target_org` is no longer accepted. Each `target_org` must already appear in `allowed_orgs`. Matching is first-rule-in-declaration-order; declare more-specific patterns first. Invalid with `login_method: password`. Free-email domains (`free-mail.example`, `outlook.com`, ...) emit a coherence warning — declaring them lets anyone on Earth join.

### `x-eve.auth.allowed_redirect_origins` — custom-domain apps

```yaml
x-eve:
  auth:
    allowed_redirect_origins:
      - https://app.example.com
      - https://www.example.com
```

Origins only — `scheme://host[:port]`. Paths, queries, fragments, and userinfo are rejected at sync. `http://` permitted only for `localhost`, loopback IPs, and `*.lvh.me`. The SSO broker also auto-includes the project's eligible `custom_domains` rows and (in `allowlist` mode) custom domains owned by `allowed_orgs` siblings, so a project with a registered custom domain does not need to repeat it here. Confirm the resolved list with `eve project auth-context <project_id>`.

See `references/manifest.md` for full validation rules (email-domain grammar, IDN normalization, duplicate detection, redirect-origin normalization).

## Service Token Permissions

Every deployed service receives an auto-injected `EVE_SERVICE_TOKEN` with **read-only defaults**. Declare any write scopes you need explicitly — anything not declared is denied:

```yaml
services:
  api:
    x-eve:
      permissions: [jobs:write, events:write, threads:write]
```

Declared permissions are **merged** with the read-only defaults; you only list what you add. Default to declaring nothing and grant write scopes one at a time as the service actually needs them. See `references/manifest.md` for the full permission catalog.

## Platform-Injected Environment Variables

Eve automatically injects these into all deployed service containers:

| Variable | Description |
|----------|-------------|
| `EVE_API_URL` | Internal cluster URL for server-to-server calls |
| `EVE_PUBLIC_API_URL` | Public ingress URL for browser-facing apps |
| `EVE_PROJECT_ID` | The project ID |
| `EVE_ORG_ID` | The organization ID |
| `EVE_ENV_NAME` | The environment name |

Use `EVE_API_URL` for backend calls from your container. Use `EVE_PUBLIC_API_URL` for
browser/client-side code. Services can override these in their `environment` section.

## Interpolation and secrets

- Env interpolation: `${ENV_NAME}`, `${PROJECT_ID}`, `${ORG_ID}`, `${ORG_SLUG}`, `${COMPONENT_NAME}`.
- Secret interpolation: `${secret.KEY}` pulls from Eve secrets or `.eve/dev-secrets.yaml`.
- Managed DB interpolation: `${managed.<service>.<field>}` resolves at deploy time.
- Use `.eve/dev-secrets.yaml` for local overrides; set real secrets via the API for production.

## Eve extensions

- Top-level defaults via `x-eve.defaults` (env, harness, harness_profile, harness_options, hints, git, workspace).
- Top-level agent policy via `x-eve.agents` (profiles, councils, availability rules).
- Agent packs via `x-eve.packs` with optional `x-eve.install_agents` defaults.
- Agent config paths via `x-eve.agents.config_path` and `x-eve.agents.teams_path`.
- Chat routing config via `x-eve.chat.config_path`.
- Service extensions under `x-eve` (ingress, role, api specs, worker pools, cli, object_store, networking, permissions).
- API specs: `x-eve.api_spec` or `x-eve.api_specs` (spec URL relative to service by default).
- App CLI: `x-eve.cli` declares an agent-friendly CLI for the service (see below).
- Toolchains: agent-level `toolchains` declarations inject on-demand runtimes (see below).
- Cloud FS mounts: configured via integrations, not the manifest (see `references/integrations.md`).
- Per-org OAuth: each org registers its own OAuth app credentials via `eve integrations configure` (see `eve-auth-and-secrets`).

Example:

```yaml
x-eve:
  agents:
    version: 1
    config_path: agents/agents.yaml
    teams_path: agents/teams.yaml
  chat:
    config_path: agents/chat.yaml
  install_agents: [claude-code, codex]
  packs:
    - source: ./skillpacks/my-pack
```

## App CLI Framework

**Recommended for every app with an API.** Wrap your service API in a CLI and register it here. Agents strongly prefer CLI commands over raw REST — CLIs handle auth, URL construction, and error formatting transparently. This is the Eve way: coding agents should build a CLI in the repo and register it in the manifest rather than having agents call APIs directly.

The platform auto-discovers services with `x-eve.cli` or `x-eve.api_spec` from the manifest and makes them available on `$PATH` for all agent jobs in the project — no explicit `with_apis` needed. Just declare the CLI here and all agents get it.

```yaml
services:
  api:
    x-eve:
      api_spec:
        type: openapi
      cli:
        name: myapp              # Binary name (goes on $PATH)
        bin: cli/bin/myapp       # Path relative to repo root (pre-bundled)
```

For compiled CLIs, use an image-based distribution:

```yaml
services:
  api:
    x-eve:
      cli:
        name: myapp
        image: ghcr.io/org/myapp-cli:latest    # Pre-built image
```

### How It Works

1. Manifest sync stores CLI metadata alongside `api_spec`.
2. Job workspace setup (after clone) runs `chmod +x` and symlinks the binary to `/usr/local/bin/`.
3. For image-based CLIs, an init container copies the binary from the image.
4. The CLI reads `EVE_APP_API_URL_{SERVICE}` and `EVE_JOB_TOKEN` (already injected) -- no manual auth or URL configuration.

### CLI naming rules

- Lowercase alphanumeric with hyphens: `[a-z][a-z0-9-]*`
- Must be unique per project
- The name becomes the command agents invoke (e.g., `eden projects list`)

## Worker Toolchain Declarations

Agents declare which runtime toolchains they need. The platform injects them as init containers -- no fat worker image required.

```yaml
# In agents.yaml
agents:
  data-analyst:
    name: Data Analyst
    skill: analyze-data
    harness_profile: claude-sonnet
    toolchains: [python]           # Needs python + uv

  doc-processor:
    name: Document Processor
    skill: process-documents
    harness_profile: claude-sonnet
    toolchains: [media]            # Needs ffmpeg + whisper
```

Available toolchains: `python`, `media`, `rust`, `java`, `kotlin`.

Workflows can override agent defaults:

```yaml
workflows:
  process-document:
    steps:
      - name: process
        agent: doc-processor
        toolchains: [media, python]  # Override: needs both
```

Toolchains are mounted at `/opt/eve/toolchains/{name}/` with binaries on `$PATH`. The default worker image is `base` (~800MB); toolchains add only what each job needs.

## Cloud FS Mounts

Google Drive folders can be mounted into the org filesystem via cloud FS integrations. Configuration is through the integrations system, not the manifest.

```bash
# Org admin registers Google Drive OAuth app credentials (BYOA)
eve integrations configure google-drive \
  --client-id "xxx.apps.googleusercontent.com" \
  --client-secret "GOCSPX-xxx"

# Connect and mount a Drive folder
eve integrations connect google-drive
eve cloud-fs mount --org org_xxx \
  --provider google-drive \
  --folder-id <drive-folder-id> \
  --label "Shared Drive"
```

Developers browse mounted content with `eve cloud-fs ls` and search it with `eve cloud-fs search`. The mount stores the provider folder ID plus an optional human-readable root-folder path hint; there is no separate CLI `--mount-path` setting.

## App Object Store

Declare app-scoped object storage buckets in the manifest. Each bucket is
provisioned per environment during deploy, tracked in `eve env diagnose`, and
credentials are injected as environment variables.

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
            cors:
              origins: ["*"]
              methods: [GET, PUT, HEAD]
              max_age_seconds: 3600
```

### Auto-Injected Storage Environment Variables

When object store buckets are provisioned, these env vars are injected into the service container:

| Variable | Description |
|----------|-------------|
| `STORAGE_ENDPOINT` | S3-compatible endpoint URL |
| `STORAGE_REGION` | Storage region |
| `STORAGE_ACCESS_KEY_ID` | App-facing access key |
| `STORAGE_SECRET_ACCESS_KEY` | App-facing secret key |
| `STORAGE_BUCKET_<NAME>` | Physical bucket name for each logical bucket |
| `STORAGE_FORCE_PATH_STYLE` | `true` for MinIO local dev, omitted for AWS S3 |

On AWS staging, apps currently share one app-bucket IAM principal scoped to
`demo-eve-app-*`. It cannot access platform internal buckets or org filesystem
buckets, but it does not isolate app buckets from each other. Per-app IRSA is
the production follow-up.

### Design Rules

- **One bucket per concern.** Separate `uploads` from `avatars` from `exports`.
- **Set visibility intentionally.** Only buckets serving public assets should be `visibility: public`.
- **Use CORS for browser uploads.** Set `cors.origins` and `cors.methods` when the frontend uploads directly via presigned URLs.
- **Bucket names must be unique** within a service. The platform derives the physical bucket name from the project, environment, and logical name.

For detailed storage layer documentation, see the `eve-read-eve-docs` skill: `references/object-store-filesystem.md`.
