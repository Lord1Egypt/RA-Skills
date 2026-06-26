# Eve Horizon Overview

## Use When
- You need first-time orientation for Eve Horizon concepts and IDs.
- You need to confirm which entry doc and environment context to load first.
- You need an overall roadmap of commands and reference selection before deep dives.

## Load Next
- `references/cli.md` for interface and command-level tasks.
- `references/manifest.md` for architecture-to-config mapping.
- `references/jobs.md` or `references/pipelines-workflows.md` for execution and automation tasks.

## Ask If Missing
- Confirm whether the user is on staging, local docker, or k3s/k3d stack.
- Confirm whether local repos are synced and whether `./bin/eh status` has been run.
- Confirm the target org/project context before giving prescriptive commands.

## Load Eve Docs First

Before any work on or with Eve Horizon, load this skill:

```
/eve-read-eve-docs
```

Then review the references that match your task. Start here for architecture and conventions; open `references/cli.md`, `references/manifest.md`, or `references/jobs.md` for specifics.

## Check Environment Status

Before ANY build, test, or development activity, run:

```bash
./bin/eh status
```

This shows what environments are running, the correct `EVE_API_URL` for each, port configuration, and multi-instance isolation status. Never assume URLs or ports.

### Environment Access

| Environment | API URL | When to Use |
|---|---|---|
| K8s (k3d) | `http://api.eve.lvh.me` | Manual tests, deployment testing |
| Docker Compose | `http://localhost:4801` | Integration tests, quick dev loop |
| Local pnpm dev | `http://localhost:4801` | Hot-reload development |
| Staging | `https://api.eve.example.com` | Production-like testing |

No port-forwarding required for K8s -- all services are accessible via Ingress.

### No Direct AWS Infrastructure Changes

All AWS infrastructure changes must go through Terraform in the `deployment-instance-repo` repo. Never run AWS CLI commands that mutate infrastructure (security groups, IAM, DNS, EKS, ASGs, etc.). Terraform is authoritative -- out-of-band changes are silently reverted on the next `terraform apply`.

If staging infra is broken (API unreachable, SG rules wrong, DNS misconfigured):

1. Diagnose with read-only commands (curl, dig, AWS CLI reads are fine).
2. Fix in `../deployment-instance/terraform/aws/`.
3. Run `terraform plan` then `terraform apply` from that repo.
4. Verify the plan shows "No changes" after apply.

If you lack access to the infra repo, escalate to the user -- do not apply a quick fix via AWS CLI.

### Staging Kubeconfig Safety

When operating the hosted staging EKS cluster:

- **Only** use `../deployment-instance/config/kubeconfig.yaml` as kubeconfig.
- Prefer running operations from `../deployment-instance` via `./bin/eve-infra ...`.
- **Never** use `~/.kube/eve-hosted.yaml` or the implicit default kube context for staging.
- If direct `kubectl` is unavoidable, always pass both `--kubeconfig ../deployment-instance/config/kubeconfig.yaml` and `--context arn:aws:eks:eu-west-1:<aws-account-id>:cluster/<cluster-name>`.

## Developer Quick Start

```bash
./bin/eh status                                    # 0. Check what's running
./bin/eh k8s start && ./bin/eh k8s deploy          # 1. Start k3d cluster + deploy
export EVE_API_URL=http://api.eve.lvh.me           # 2. Set API URL
eve org ensure test-org --slug test-org             # 3. Use the CLI
./bin/eh k8s stop                                  # 4. Clean up
```

## Current State (Implemented)

**Phase**: Pre-MVP (K8s runtime + agent runtime + chat gateway + builds/deploy pipeline + auth/RBAC complete).

**What exists**: monorepo with 6 services (API, orchestrator, worker, agent runtime, gateway, SSO). Database with orgs, projects, environments, jobs, attempts, agents, teams, threads, integrations, schedules. Full auth stack (SSH login, web auth via GoTrue + SSO broker, service principals, custom roles, access groups, project role resolution). RBAC with policy-as-code and default-deny data plane. Persistent environment deployment to K8s with manifest variable interpolation, HTTP ingress routing, and public TCP ingress for raw protocols. First-class builds (BuildKit), releases, and pipelines (build -> release -> deploy). Job execution with mclaude/claude/zai/gemini/code/codex harnesses via `eve-agent-cli`. BYOK inference model (apps and agents bring their own LLM API keys via secrets; no platform-managed models or inference proxy). Provider registry + model discovery. Agent/team/thread primitives with repo-first sync and AgentPacks (`x-eve.packs`). Chat gateway with Slack + Nostr integration. Agent runtime (primary harness executor for all agent jobs; org-scoped warm pods). Org filesystem sync + org docs. Document ingestion (file upload -> event -> agent processing -> structured output in org docs; content deduplication via fingerprint). Cloud FS integration (Google Drive per-org OAuth, agent file tools). Per-org OAuth credentials (orgs bring their own Google/Slack app credentials via `oauth_app_configs`). Private endpoints (Tailscale networking for reaching private services from cluster pods). App CLI framework (typed CLI wrappers for agent-to-app API interactions, reducing LLM call waste). Cost tracking (execution receipts, resource classes, budgets, balance ledger, OpenCost-backed environment cost snapshots, and daily Sentinel cost summaries). Production hardening (content dedup, dead letter handling, per-phase latency diagnostics, routing decision logging, cost breakdown by agent/team, automatic retry policies, document expiration). Analytics, webhooks, and supervision primitives. Agent app API access (server-side `app_apis` in job hints, `@eve-horizon/auth` SDK). Workflow expansion into job DAGs with `depends_on` step dependencies. Org-aware auth SDK (memberships, org switching, project role resolution via `@eve-horizon/auth-react`). CLI as npm package (`@eve-horizon/cli`) and local `./bin/eh` helpers. K8s local stack via k3d.

### Pre-Deployment Phase

No deployments to production. No real users. No backwards compatibility concerns. This means:

1. **Simplify aggressively** -- if something can be simpler, make it simpler.
2. **Refactor without fear** -- no migrations to maintain, no users to break.
3. **Delete ruthlessly** -- dead code, unused abstractions, speculative features.
4. **Question everything** -- every abstraction must earn its place.

## What Eve Horizon Is

Eve Horizon is a **job-first platform** that runs AI-powered skills against Git repos:

- **CLI-first**: humans and agents use the same CLI against the API.
- **Job-centric**: all work is tracked as jobs with phases, priorities, and dependencies.
- **Event-driven**: automation routes through an event spine in Postgres.
- **Skills-based**: reusable capabilities live as `SKILL.md` files in repos; preferred flow via AgentPacks.
- **Isolated execution**: each job attempt runs in a fresh workspace with a cloned repo.
- **BYOK inference**: no managed models or inference proxy -- harnesses call providers directly via secrets.
- **Auth-complete**: SSH login, web auth (GoTrue + SSO), service principals, custom roles, access groups, policy-as-code.
- **Document ingestion**: file upload -> event -> agent processing -> structured output in org docs.
- **Cloud FS**: Google Drive integration with per-org OAuth, agent file tools.
- **Private endpoints**: Tailscale networking makes private services reachable from cluster pods.
- **Staging-first**: default guidance targets staging; local dev is opt-in.

## Architecture Summary

```
User -> CLI -> API -> Orchestrator --+--> Agent Runtime --> Harness -> Agent
         |      |            |      |    (all agent jobs)
Chat -> Gateway +         Postgres  |
                                    +--> Worker
                                         (builds, deploys, pipelines, scripts)

ONLY URL needed: EVE_API_URL
CLI is a thin wrapper; all control flows through the API.
```

**Services** (6 in the monorepo):

- **API**: single gateway for org/project/job CRUD, secrets, events, runs, auth.
- **Orchestrator**: polls ready jobs, routes to agent-runtime or worker based on job type.
- **Agent Runtime**: executes ALL agent/harness jobs (chat, manual, scheduled) in org-scoped warm pods.
- **Worker**: executes pipeline actions, scripts, and builds -- does NOT run agent jobs.
- **Gateway**: routes inbound messages from Slack/Nostr to agents.
- **SSO**: GoTrue + SSO broker for web authentication.

**Key flows**:

1. Create job -> API validates -> stored in DB.
2. Orchestrator claims ready jobs -> routes by execution type.
3. Agent jobs -> Agent Runtime invokes harness (mclaude/claude/zai/gemini/code/codex) -> streams JSONL logs.
4. Chat flow: Slack -> Gateway -> API routes -> jobs + threads -> Agent Runtime executes.
5. Build flow: pipeline step -> Worker -> BuildKit -> push images -> release -> deploy to K8s namespace.
6. HITL review -> continue or complete.

## Key Decisions

| Decision | Rationale |
|---|---|
| 6 harnesses via eve-agent-cli | Uniform invocation for mclaude/claude/zai/gemini/code/codex |
| Job (not Task) terminology | Avoids collision with cc-mirror's Task tools |
| NestJS for backend | Clean architecture, TypeScript native |
| Hierarchical job IDs | `{slug}-{hash8}` root, `{parent}.{n}` children |
| Phase-based job lifecycle | idea -> backlog -> ready -> active -> review -> done |
| Single repo per project | Simplifies execution and config |
| CLI as thin REST wrapper | Single source of truth, no DB bypass |
| API as single gateway | CLI needs only `EVE_API_URL` |
| K8s runtime via k3d | Production-like local testing, runner pods for isolation |
| Agent runtime runs ALL agent jobs | Primary harness executor; worker is for builds/pipelines only |
| Chat gateway + Slack mapping | Multi-tenant `team_id -> org_id` routing |
| Repo-first agents sync | Deterministic config via `--ref` |
| Two-repo deploy model | Source builds images, infra repo applies K8s manifests |
| BuildKit-first builds | Replaced kaniko; reliable in-cluster container builds |
| BYOK inference (no managed models) | Harnesses call providers directly via secrets; no proxy layer |
| Per-org OAuth credentials | Orgs bring own Google/Slack app credentials; no cluster-level secrets |
| Private endpoints (Tailscale) | K8s pods reach Tailscale-only services via egress proxy |
| GoTrue + SSO broker | Web auth via Supabase-compatible auth, dual-mode API auth |
| Default-deny data plane | Members/agents/users need explicit group-scoped grants |

## Conventions

- **Org/Project IDs**: `org_xxx`, `proj_xxx` (TypeID format).
- **Job IDs**: `{slug}-{hash8}` for root jobs (e.g., `myproj-a3f2dd12`).
- **Job phases**: `idea` -> `backlog` -> `ready` -> `active` -> `review` -> `done`/`cancelled`.
- **Priority**: 0-4 (P0=critical, P4=backlog, default=2).
- **K8s namespaces**: `eve-{orgSlug}-{projectSlug}-{envName}` for deployments.

### IDs and Formats

| Entity | Format | Example |
|---|---|---|
| Org ID | `org_...` | `org_abc123` |
| Project ID | `proj_...` | `proj_def456` |
| Job ID (root) | `{slug}-{hash8}` | `myproj-a3f2dd12` |
| Job ID (child) | `{parent}.{n}` | `myproj-a3f2dd12.1` |
| Build ID | `bld_...` | `bld_xyz789` |
| Release ID | `rel_...` | `rel_uvw012` |
| Managed DB Instance | `mdbi_...` | `mdbi_01abc` |
| Managed DB Tenant | `mdbt_...` | `mdbt_01def` |
| Event ID | `evt_...` | `evt_ghi345` |
| Pipeline Run ID | `prun_...` | `prun_jkl678` |
| Service Principal | `sp_...` | `sp_abc123` |
| SP Token | `spt_...` | `spt_def456` |
| Access Role | `role_...` | `role_ghi789` |
| Access Binding | `bind_...` | `bind_jkl012` |
| Attempt | UUID + `attempt_number` | (1, 2, 3...) |

## Development Workflow

### Environment Status First

Always start here:

```bash
./bin/eh status
export EVE_API_URL=http://api.eve.lvh.me     # for k8s
export EVE_API_URL=http://localhost:4801      # for docker/dev
```

### Build and Test

```bash
pnpm install          # Refresh workspace links
pnpm build            # Full build (all packages and apps)
pnpm test             # Unit tests (fast, no external deps)
./bin/eh test integration   # Integration tests (docker DB + local processes)
```

### Hot-Reload Development

```bash
./bin/eh start local    # DB container + local node processes (hot-reload)
./bin/eh start docker   # All services in containers
./bin/eh k8s start && ./bin/eh k8s deploy   # K8s stack (manual testing)
./bin/eh stop           # Stop current mode
```

Modes are exclusive -- starting a different mode stops the current one.

### Manual Testing (Observable Tests)

For k8s stack testing, use manual test scenarios with parallel job watching. Read `tests/manual/README.md` before running.

```bash
./bin/eh status                    # Must show k8s cluster "running"
eve system health --json           # Must return {"status":"ok"}
eve org ensure "manual-test-org" --slug manual-test-org --json
eve secrets import --org org_manualtestorg --file manual-tests.secrets
# Run scenarios from tests/manual/scenarios/
eve job follow <job-id>            # Stream logs in real-time
```

### CLI-First Debugging

Debug via the Eve CLI first. Always. Our clients do not have kubectl access -- replicate their experience. Every debugging gap is a product improvement opportunity.

**Debugging ladder**:

| Priority | Tool | When to Use |
|---|---|---|
| 1st | `eve` CLI | Always start here -- job status, logs, diagnose |
| 2nd | `./bin/eh status` | Environment health, connectivity |
| 3rd | `kubectl` | Only when CLI is insufficient -- then file an issue |

**CLI debugging commands**:

```bash
eve system health --json
eve job list --all --phase active
eve job show <id> --verbose
eve job follow <id>               # Stream harness logs
eve job logs <id>                 # Historical logs
eve job result <id>               # Exit status + outputs
eve job diagnose <id>             # Full diagnostic dump
eve env show <project> <env>      # Deployment health
```

### Build/Deploy Debugging Ladder

| Priority | Command | What It Shows |
|---|---|---|
| 1st | `eve pipeline logs <pipeline> <run-id> --follow` | Real-time streaming of all steps |
| 2nd | `eve pipeline logs <pipeline> <run-id>` | Snapshot with inline errors + hints |
| 3rd | `eve build diagnose <build_id>` | Full build state (last 30 lines of buildkit output) |
| 4th | `eve env diagnose <project> <env>` | K8s deployment diagnostics |
| 5th | `eve job diagnose <job_id>` | Full job execution details |

Pipeline build failures include the build ID in error output. Use `eve build diagnose <build_id>` to see the failed Dockerfile stage.

### Multi-Instance Support

Eve Horizon supports multiple repo checkouts running integration tests in parallel:

| Resource | Isolation | Shared |
|---|---|---|
| Docker Compose | Per-instance (via `EVE_INSTANCE` prefix) | -- |
| Postgres | Per-instance volume | -- |
| Ports | Per-instance (via `base_port`) | -- |
| k3d Cluster | -- | Shared (one `eve-local` cluster) |

Default ports: API=4801, Orchestrator=4802, DB=4803, Worker=4811. Config stored in `.eve-horizon.yaml` (gitignored). Check `./bin/eh status` for k8s ownership status before touching the shared cluster.

## Testing Architecture

Three-tier test pyramid:

| Tier | Type | What It Tests | Environment | Command |
|---|---|---|---|---|
| 1 | Unit | Pure logic, validators | None | `pnpm test` |
| 2 | Integration | API, job flows, secrets | Docker DB + local pnpm | `./bin/eh test integration` |
| 3 | Manual | Happy paths, real repos | K8s stack | See `tests/manual/` |

Integration tests use API endpoints, not direct DB queries. Test and dev use separate databases (`eve` for dev, `eve_test` for integration).

## Sister Repositories

| Repo | Expected Path | Purpose |
|---|---|---|
| deployment-instance-repo | `../deployment-instance` | K8s manifests, kustomize overlays, deploy automation |
| eve-horizon-starter | `../eve-horizon-starter` | Starter template for new Eve projects |
| eve-horizon-fullstack-example | `../eve-horizon-fullstack-example` | Example fullstack app for deployment testing |
| eve-skillpacks | `../eve-skillpacks` | Published skill packs referenced by `skills.txt` |

Agents are free to make changes, commit, and push to `main` in these repos without explicit approval -- this is part of the normal development flow.

### Skillpacks Sync Obligation

When platform behavior changes in eve-horizon, the corresponding reference file in `eve-skillpacks/eve-work/eve-read-eve-docs/references/` must be updated. If `eve-read-eve-docs` is outdated, agents will make incorrect assumptions. See the `eve-docs-upkeep` skill for the full audit checklist.

## Eve Dashboard (System App)

Eve ships a first-party web dashboard (`apps/dashboard`) — a single-shell SSO-authenticated UI with real-time job/phase views, environment health, spending, and admin surfaces. It is built and deployed through the same build/release/deploy pipeline as customer apps.

This proves the **system app pattern**: platform-shipped apps go through the standard publish-images CI matrix and infra-repo overlays, with a single platform version tag from `config/platform.yaml`. New system apps follow the checklist in `eve-horizon/docs/system-apps.md`. See `references/deploy-debug.md` for the deployment flow and the `eve-fullstack-app-design` skill for design guidance.

## Build -> Release -> Deploy

The standard deployment flow:

1. **Build**: create container images from source code (BuildKit-based).
2. **Release**: capture a deployable snapshot (SHA + manifest + digests).
3. **Deploy**: apply release to an environment.

Staging deploys use a **two-repo model**: source repo (`eve-horizon`) builds and pushes images on `release-v*` tags, then dispatches to the infra repo (`deployment-instance-repo`) which applies K8s manifests.

Pipelines orchestrate these steps as a job graph. See `references/builds-releases.md`.

## Event Spine

Events are stored in Postgres and routed by the orchestrator:

| Source | Description |
|---|---|
| `github` | Webhook events (push, pull_request) |
| `slack` | Chat messages and app mentions |
| `cron` | Scheduled triggers |
| `system` | Auto-emitted failure events (job.failed, pipeline.failed) |
| `runner` | Worker execution events (started, progress, completed, failed) |
| `manual` | User-created via CLI/API |
| `app` | Application-emitted |
| `chat` | Chat system events |

Triggers in the manifest map events to pipeline runs or workflow jobs. See `references/events.md`.

## Agents, Teams, and Chat

- **Agents**: defined in `agents.yaml`, synced via `eve agents sync`.
- **Teams**: defined in `teams.yaml`, coordinate multiple agents (fanout/council/relay).
- **Chat routing**: defined in `chat.yaml`, maps messages to agents via regex patterns.
- **Slack**: `@eve <agent-slug> <command>` routing.
- **Nostr**: relay-based subscription transport.

See `references/agents-teams.md`.

## Skills System

Reusable capabilities installed via `skills.txt` manifest:

- `SKILL.md` files with frontmatter metadata.
- Installed to `.agents/skills/` at clone time (legacy: `.agent/skills/`).
- Workers run `.eve/hooks/on-clone.sh` to install skills.
- Preferred flow: AgentPacks via `x-eve.packs` + `.eve/packs.lock.yaml`.

See `references/skills-system.md`.

## Key Rules

- **CLI only needs `EVE_API_URL`**; everything routes through the API.
- **Default to staging** for user guidance unless explicitly asked for local dev.
- **Pipelines and workflows are manifest-defined** and materialize into jobs.
- **Git controls live on jobs** (ref, branch, commit/push policies).
- **Agent slugs are org-unique** (enforced at sync time).
- **Secrets scopes stack**: project > user > org > system.
- **Service principals** provide machine identity for app backends (scoped JWT tokens).
- **Custom roles** are additive overlays on member/admin/owner (no deny rules).
- **Policy-as-code** via `.eve/access.yaml` enables reviewable, CI-friendly access config.
- **Fail fast on provisioning errors** -- swallow no errors, fix root causes.

## Reference Index

| Topic | Reference File |
|---|---|
| CLI commands | `references/cli.md` |
| Manifest schema | `references/manifest.md` |
| Events + triggers | `references/events.md` |
| Jobs | `references/jobs.md` |
| Builds + releases | `references/builds-releases.md` |
| Agents, teams, chat | `references/agents-teams.md` |
| Pipelines + workflows | `references/pipelines-workflows.md` |
| Secrets + auth | `references/secrets-auth.md` |
| Skills system | `references/skills-system.md` |
| Deploy + debug | `references/deploy-debug.md` |
| Harnesses | `references/harnesses.md` |
| Gateway plugins | `references/gateways.md` |
| Observability + cost | `references/observability.md` |
| Database operations | `references/database-ops.md` |
| Troubleshooting | `references/troubleshooting.md` |
| App CLIs | `references/app-cli.md` |
| Eve SDK | `references/eve-sdk.md` |
| Auth SDK | `references/auth-sdk.md` |
| Integrations | `references/integrations.md` |
| Object store + filesystem | `references/object-store-filesystem.md` |
| Document ingest | `references/ingest.md` |

**Note:** These references are distilled from the Eve Horizon system docs. For narrative walkthroughs and tutorials, see the [eve-horizon](https://github.com/eve-horizon/eve-horizon) repository docs.
