# Eve Horizon Platform Primitives

Distillation of the platform primitives available for agent-native app building.

## Jobs

The fundamental unit of work. Create, orchestrate, and compose into hierarchies.

- `eve job create` — Create a job with optional parent and dependencies
- `eve job dep add` — Wire dependency edges between jobs
- Depth propagation: child jobs inherit and increment depth from parents
- Parallel decomposition: break work into concurrent sub-jobs
- Control signals: `json-result` with `eve.status` ("success", "failed", "waiting")
- Supervision: `eve supervise` monitors job trees with long-poll child events
- Coordination threads: `coord:job:{parent_job_id}` for lead/child messaging

### Job Attachments (Emerging)

Pass structured context between agents without file gymnastics:

```
POST   /jobs/:id/attachments           — attach a document
GET    /jobs/:id/attachments           — list attachments
GET    /jobs/:id/attachments/:att_id   — get content
DELETE /jobs/:id/attachments/:att_id   — remove
```

Use attachments for plans, architecture reports, code insights — any structured document that needs to flow between jobs. Text-only (markdown, JSON, YAML). For binary content, store a URL reference.

## Agents & Teams

Define personas, dispatch modes, and chat routing.

- `agents.yaml` — Declare agent personas with skills, model, system prompt
- `teams.yaml` — Group agents into teams with routing rules
- Chat gateway routes messages to agents by slug
- Dispatch modes: `fanout`, `council`, `relay` (sequential delegation)
- Warm pods: pre-provisioned containers per org for reduced cold-start
- Service principals for machine-to-machine agent access

## Pipelines & Workflows

Deterministic sequences and on-demand functions.

- Pipelines: ordered steps with `action`, `script`, or `agent` types
- Built-in actions: `build`, `release`, `deploy`, `run`, `job`, `create-pr`
- Workflows: reusable functions triggered by events or manual invocation
- Both defined in `.eve/manifest.yaml`
- Pipeline logs: `eve pipeline logs <name> <run-id> --follow` for real-time streaming

## Gateway

Multi-provider chat with agent discovery.

- Routes messages to agents by slug
- Providers: Slack (webhook), Nostr (subscription), extensible
- Slack: `app_mention` for commands, `message` for channel/thread listeners
- Nostr: Kind 4 (encrypted DMs), Kind 1 (public mentions), NIP-04 decryption
- Gateway discovery policy controls agent visibility per provider
- New agents are instantly addressable once declared

## Builds & Releases

Immutable artifacts with promotion workflows.

- `eve build create` + `eve build run` — Build container images
- Digest-based artifacts ensure immutability across environments
- Release references `build_id` for exact artifact tracking
- Build once → promote staging → production with identical images
- Image tagging: `:local` for dev, git SHA or semver for pipelines

## Skills

Knowledge distribution and progressive disclosure.

- AgentPacks (preferred): declared in `x-eve.packs` in manifest, resolved to `packs.lock.yaml`
- `skills.txt` — Legacy skill source declaration per project
- Skills installed to `.agent/skills/` on clone
- Progressive disclosure: index skills route to detailed skills
- Skill packs group related skills by domain (eve-work, eve-se, eve-design)

## Events

Automation triggers and event spine.

- Event-driven pipeline/workflow triggers (GitHub, Slack, cron, system, manual, app)
- System auto-emits `system.job.failed` and `system.pipeline.failed` for self-healing
- Custom event types for app-specific automation
- Orchestrator polls pending events every ~5 seconds

## Managed Resources

Platform-provided infrastructure.

- DBaaS: Managed Postgres provisioning via `managed_db` in manifest
- Container registry: Native image storage with `registry.host` in manifest
- Secret management: `eve secrets set/list/delete` with environment scoping
- Platform env vars: `EVE_API_URL`, `EVE_PUBLIC_API_URL`, `EVE_PROJECT_ID`, `EVE_ORG_ID`, `EVE_ENV_NAME`

## Service Account Authentication (Emerging)

Backend-to-API auth for agentic apps:

```bash
eve auth create-service-account --name "my-backend" --scopes "jobs:create,jobs:read"
# Returns: eve_svc_xxxxxxxxxxxx
```

Every app with a backend needs this. Scoped permissions, auditable, standard pattern. Currently use `eve auth mint` as the interim path.

## Org Document Store (Emerging)

Persistent org-wide knowledge that survives job boundaries:

```
POST   /orgs/:id/docs                — write a document
GET    /orgs/:id/docs?path=/reports/ — list by path
GET    /orgs/:id/docs/:path          — read content
PATCH  /orgs/:id/docs/:path          — search/replace editing
DELETE /orgs/:id/docs/:path          — delete
GET    /orgs/:id/docs/search?q=...   — full-text search
```

DB-backed (Postgres) with full-text search. Agents accumulate architecture reports, risk assessments, team conventions — knowledge that persists across jobs and projects.

## Cross-Project Queries (Emerging)

Org-level intelligence without N+1 API calls:

```
GET /orgs/:id/jobs?status=open       — jobs across all projects
GET /orgs/:id/jobs/stats             — aggregate counts
GET /orgs/:id/agents                 — all agents across projects
```

Enables portfolio-level views for PM apps, dashboards, and any org-level tool.

## Web Chat for Agentic Apps

Two mechanisms for different needs:

### Mechanism A: Gateway Provider (Simple)
Web app connects directly to Eve gateway via WebSocket. Zero backend work. Best for chat widgets, admin consoles, quick tools.

### Mechanism B: Backend-Proxied (Full Control)
App backend calls Eve internal chat API (`/internal/orgs/:id/chat/route`). Enriches messages with app context, stores conversations in own DB. Best for production SaaS, apps with rich domain models.

**Decision tree**: If your app needs to intercept, enrich, or store conversations → use B. Otherwise → use A.

## Priority Ranking (Platform Investment)

| Priority | Primitive | Status |
|----------|-----------|--------|
| **Now** | Job Attachments | Schema defined, needs API endpoints |
| **Now** | Service Account Auth | Interim: `eve auth mint` |
| **Phase 1** | Org Document Store | Design complete |
| **Phase 1** | Cross-Project Queries | Data exists, needs exposure |
| **Phase 2** | Project Bootstrapping API | Wraps existing CLI commands |
| **Phase 2** | Spec Format (conventions) | Emerges from job attachments |
| **Phase 3** | Webhooks / Event Callbacks | Replace polling in production |
| **Phase 3** | WebChat Gateway Provider | When multiple apps need simple chat |
