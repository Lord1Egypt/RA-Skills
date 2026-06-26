# Eve Horizon Storage Primitives Reference

Complete inventory of storage systems available to agents on Eve Horizon, with CLI commands, API endpoints, and design considerations.

## 1. Workspace Files

**Scope**: Job
**Lifetime**: Job duration (unless committed to git)
**Access**: Agent running the job

The git repo checkout at `$EVE_REPO_PATH`. Workspace mode controls sharing:

| Mode | Behavior |
|------|----------|
| `job` | Fresh checkout per job (default) |
| `session` | Shared across jobs using the same `workspace-key` |
| `isolated` | No git state, pure scratch space |

```bash
eve job create --workspace-mode session --workspace-key "my-session"
```

Convention: write agent scratch to `.eve/` (gitignored). Committed files persist in the repo.

## 2. Job Attachments

**Scope**: Job (readable by any job with the ID)
**Lifetime**: Permanent (attached to job record)
**Access**: Any agent with the job ID

Named binary blobs attached to a job record.

```bash
# Write
eve job attach <job-id> --name <name> [--content <text>] [--file <path>] [--content-type <type>]

# Read
eve job attachments <job-id>                    # list metadata
eve job attachment <job-id> <name> [--out <path>]  # retrieve content
```

API:
```
POST /jobs/:id/attachments
GET  /jobs/:id/attachments
GET  /jobs/:id/attachments/:attachment_id
```

## 3. Threads

**Scope**: Project or Org
**Lifetime**: Permanent
**Access**: RBAC (user tokens) or job tokens (project-scoped)

Message sequences for continuity and coordination.

### Project Threads
```bash
eve thread messages <thread-id> --since 10m
eve thread post <thread-id> --body '{"kind":"update","body":"progress note"}'
eve thread follow <thread-id>     # poll every ~3s
```

### Org Threads
```bash
eve thread list --org <org-id>
eve thread show --org <org-id> --id <thread-id>
eve thread messages <thread-id> --org <org-id> --since 10m
eve thread post <thread-id> --body '{"kind":"directive","body":"instructions"}'
```

### Coordination Threads
Auto-created for team dispatches. Key: `coord:job:{parent_job_id}`.

Child agents derive the key from `$EVE_PARENT_JOB_ID`. End-of-attempt summaries are posted automatically. The coordination inbox (`.eve/coordination-inbox.md`) is regenerated at job start.

### Message Kinds
| Kind | Purpose |
|------|---------|
| `status` | Automatic end-of-attempt summary |
| `directive` | Lead-to-member instruction |
| `question` | Member-to-lead question |
| `update` | Progress update from member |

### Distillation
```bash
# Distill thread into knowledge
eve thread distill <thread-id> --org <org-id> [--to <path>] [--agent <slug>] [--category <name>] [--key <key>]
```

### Listener Subscriptions
```
@eve agents listen <agent-slug>    # subscribe agent to channel/thread
@eve agents unlisten <agent-slug>
@eve agents listening              # list active listeners
```

## 4. Resource Refs

**Scope**: Job
**Lifetime**: Job duration (references resolved at hydration)
**Access**: Agent running the job

Versioned pointers to org documents, mounted into job workspaces.

```bash
eve job create \
  --resource-refs='[{"uri":"org_docs:/path/to/doc.md@v3","label":"Input","mount_path":"inputs/doc.md"}]'
```

URI scheme: `org_docs:/path@version`. Hydration emits events:
- `system.resource.hydration.started`
- `system.resource.hydration.completed`
- `system.resource.hydration.failed`

## 5. Org Document Store

**Scope**: Org
**Lifetime**: Permanent, versioned
**Access**: Org membership (+ access groups for fine-grained control)

Versioned, searchable document store scoped to the organization.

```bash
# CRUD
eve docs write --org <org-id> --path /path/to/doc.md --file ./content.md
eve docs read --org <org-id> --path /path/to/doc.md
eve docs delete --org <org-id> --path /path/to/doc.md

# List and search
eve docs list --org <org-id> --prefix /agents/
eve docs search --org <org-id> --query "keyword"

# Version history
eve docs versions --org <org-id> --path /path/to/doc.md

# Lifecycle
eve docs stale --org <org-id> [--overdue-by 7d] [--prefix /agents/]
eve docs review --org <org-id> --path <path> --next-review 30d
```

Events emitted: `system.doc.created`, `system.doc.updated`, `system.doc.deleted`.

API:
```
POST   /orgs/:org_id/docs
GET    /orgs/:org_id/docs
GET    /orgs/:org_id/docs/:doc_id
PUT    /orgs/:org_id/docs/:doc_id
DELETE /orgs/:org_id/docs/:doc_id
GET    /orgs/:org_id/docs/search?q=<query>
```

## 6. Org Filesystem

**Scope**: Org
**Lifetime**: Permanent
**Access**: Org permissions (orgfs scope with access groups); agents access `.org/` via workspace mount

Shared per-org file storage with two access paths: agents read/write `.org/` directly in their job workspace (mounted in both agent-runtime and worker execution paths), and developers sync to local machines via the CLI.

### Agent Workspace Access

Agents see `.org/` in their workspace during job execution. Both agent-runtime (warm pods) and worker (runner pods) execution paths mount the org filesystem.

```bash
# Read shared org files
cat .org/shared/runbook.md

# Write agent-scoped files
mkdir -p .org/agents/reviewer/findings/
echo '{"patterns": [...]}' > .org/agents/reviewer/findings/sprint-42.json

# List available org content
ls .org/
```

The mount is scoped by the user's RBAC bindings (`allow_prefixes`, `read_only_prefixes`). `$EVE_ORG_ROOT` points to the mount path.

### CLI Sync (Developer Machines)

```bash
# Setup
eve fs sync init --org <org-id> --local ~/Eve/acme --mode two-way
  # Modes: two-way | push-only | pull-only
  # Optional: --include '**/*.md' --exclude '**/node_modules/**'

# Operations
eve fs sync status --org <org-id>
eve fs sync logs --org <org-id> --follow
eve fs sync pause --org <org-id>
eve fs sync resume --org <org-id>
eve fs sync disconnect --org <org-id>
eve fs sync mode --org <org-id> --set pull-only

# Conflict resolution
eve fs sync conflicts --org <org-id>
eve fs sync resolve --org <org-id> --conflict <id> --strategy pick-remote

# Diagnostics
eve fs sync doctor --org <org-id>

# Share tokens
eve fs share <path> --org <org-id> [--expires 7d] [--label "description"]
eve fs shares --org <org-id>
eve fs revoke <token> --org <org-id>

# Public paths
eve fs publish <path-prefix> --org <org-id> [--label "description"]
eve fs public-paths --org <org-id>
```

Event types: `file.created`, `file.updated`, `file.deleted`, `file.renamed`, `conflict.detected`, `conflict.resolved`.

SSE stream: `GET /orgs/:org_id/fs/events/stream?after_seq=<n>`

Default includes: `**/*.md`, `**/*.mdx`, `**/*.txt`, `**/*.yaml`, `**/*.yml`.

## 7. Managed Databases

**Scope**: Environment
**Lifetime**: Permanent (until environment destroyed)
**Access**: Workers via injected credentials; CLI via `eve db`

Postgres instances declared in the manifest and provisioned per environment.

```yaml
# eve.yaml
services:
  db:
    x-eve:
      role: managed_db
      managed:
        class: db.p1
        engine: postgres
        engine_version: "16"
```

```bash
# Query
eve db sql --env <env> --sql "SELECT * FROM agent_memory WHERE key = 'patterns'"
eve db sql --env <env> --sql "INSERT INTO ..." --write

# Schema
eve db schema --env <env>
eve db migrate --env <env>
eve db new create_agent_memory

# RLS (row-level security with group awareness)
eve db rls --env <env>
eve db rls init --with-groups  # scaffold group-aware policies
```

## 8. Secrets

**Scope**: System / Org / User / Project
**Lifetime**: Until rotated or deleted
**Access**: Resolution hierarchy (project → user → org → system)

Encrypted credential storage. Not for agent memory — for API keys, tokens, and credentials.

```bash
eve secrets set MY_KEY myvalue --scope project --project <id>
eve secrets show MY_KEY --project <id>
eve secrets import --org <org-id> --file ./secrets.env
eve secrets validate --project <id>
```

## 9. Event Spine

**Scope**: Project or Org
**Lifetime**: Permanent (event records)
**Access**: RBAC

Pub/sub event bus for reactive workflows. Not a storage primitive per se, but critical for memory-aware architectures.

```bash
eve event emit --type=<type> --source=<source> --payload '<json>'
eve event list [--type <type>] [--source <source>] [--status <status>]
eve event show <event-id>
```

Event types relevant to memory:
- `system.doc.created/updated/deleted` — org document mutations
- `system.resource.hydration.*` — resource ref resolution
- `runner.*` — job lifecycle events
- Custom `agent.memory.*` types for agent-specific notifications

## 10. Skills and Skillpacks

**Scope**: Org or global (via skillpack repos)
**Lifetime**: Permanent, version-controlled
**Access**: Skill installation and loading

The highest-fidelity memory: distilled workflows encoded as agent instructions. See `eve-skill-distillation` for creation workflow.

```bash
eve skills install ../eve-skillpacks/eve-work/
```

## 11. Container Registry

**Scope**: Project
**Lifetime**: Permanent (image tags)
**Access**: Project membership

Store and retrieve container images. Not directly a memory primitive, but relevant for agents that build and deploy.

```bash
eve registry push --tag <tag>
eve registry images
eve registry tags <image>
```

## 12. Agent KV Store

**Scope**: Org (agent-scoped, namespace-partitioned)
**Lifetime**: Until TTL expires or explicitly deleted
**Access**: Agent (via `--agent` flag)

Lightweight key-value storage for operational state. Each key is scoped to an agent slug and namespace. Values are JSONB. Optional TTL for automatic expiration.

```bash
# Set
eve kv set --org <org-id> --agent <slug> --key <key> --value <json-or-string> [--namespace <ns>] [--ttl <seconds>]

# Get
eve kv get --org <org-id> --agent <slug> --key <key> [--namespace <ns>]

# List keys in namespace
eve kv list --org <org-id> --agent <slug> [--namespace <ns>] [--limit <n>]

# Batch get
eve kv mget --org <org-id> --agent <slug> --keys a,b,c [--namespace <ns>]

# Delete
eve kv delete --org <org-id> --agent <slug> --key <key> [--namespace <ns>]
```

API:
```
PUT    /orgs/:org_id/agents/:slug/kv/:namespace/:key
GET    /orgs/:org_id/agents/:slug/kv/:namespace/:key
GET    /orgs/:org_id/agents/:slug/kv/:namespace
POST   /orgs/:org_id/agents/:slug/kv/:namespace/mget
DELETE /orgs/:org_id/agents/:slug/kv/:namespace/:key
```

Database table: `agent_kv` (id, org_id, agent_slug, namespace, key, value JSONB, ttl_seconds, expires_at).

Use for: feature flags, rate counters, workflow state machines, deduplication keys. Namespace `default` is used when `--namespace` is omitted.

## 13. Agent Memory Namespaces

**Scope**: Org (agent-scoped or shared)
**Lifetime**: Permanent (with optional review dates and expiration)
**Access**: Agent (via `--agent` flag or `--shared`)

Curated knowledge entries stored under agent-scoped paths. Each entry has a category, key, content body, and optional metadata (confidence, tags, lifecycle fields).

```bash
# Set (create or update)
eve memory set --org <org-id> (--agent <slug>|--shared) --category <category> --key <key> \
  (--file <path>|--stdin|--content <text>) \
  [--confidence <0-1>] [--tags a,b] [--review-in <duration>] [--expires-in <duration>]

# Get
eve memory get --org <org-id> (--agent <slug>|--shared) --key <key> [--category <cat>]

# List
eve memory list --org <org-id> (--agent <slug>|--shared) [--category <cat>] [--tags a,b] [--limit <n>]

# Delete
eve memory delete --org <org-id> (--agent <slug>|--shared) --category <cat> --key <key>

# Search across memory
eve memory search --org <org-id> --query <text> [--agent <slug>] [--limit <n>]
```

API:
```
POST   /orgs/:org_id/agents/:slug/memory          (set)
GET    /orgs/:org_id/agents/:slug/memory/:key      (get)
GET    /orgs/:org_id/agents/:slug/memory            (list)
DELETE /orgs/:org_id/agents/:slug/memory/:key       (delete)
GET    /orgs/:org_id/memory/search?q=<query>        (cross-agent search)
```

Categories: `learnings`, `decisions`, `runbooks`, `context`, `conventions`.

Namespace convention: `/agents/{slug}/memory/{category}/{key}.md` or `/agents/shared/memory/...`

Use for: accumulated expertise, decision logs with confidence scores, operational runbooks, context that should persist across sessions.

## 14. Unified Search

**Scope**: Org
**Lifetime**: N/A (read-only query)
**Access**: Org membership

Single query across multiple storage systems.

```bash
eve search --org <org-id> --query <text> [--sources memory,docs,threads,attachments,events] [--limit <n>] [--agent <slug>]
```

API:
```
GET /orgs/:org_id/search?q=<query>&sources=<csv>&limit=<n>&agent=<slug>
```

Sources: `memory`, `docs`, `threads`, `attachments`, `events`.

Use for: finding relevant prior knowledge before starting work. Combines results from multiple storage systems into a single ranked response.

## Comparison Matrix

| Primitive | Scope | Searchable | Versioned | Structured | Event-Driven |
|-----------|-------|------------|-----------|------------|-------------|
| Workspace | Job | No | Via git | Files | No |
| Attachments | Job | By name | No | Key-value | No |
| Threads | Project/Org | By time | No | Messages | No |
| Resource Refs | Job | No | Yes (pinned) | URI | Yes |
| Org Docs | Org | Yes (text) | Yes | Markdown | Yes |
| Org Filesystem | Org | No* | Via events | Files (`.org/` mount) | Yes |
| Managed DB | Environment | Yes (SQL) | No | Tables | No |
| Secrets | Multi-scope | By key | No | Key-value | No |
| Event Spine | Project/Org | By type/time | No | JSON | Yes (core) |
| Skills | Global | No | Via git | Markdown | No |
| KV Store | Org (agent) | By key | No | Key-value | No |
| Memory | Org (agent) | Yes (text) | No | Categories | No |
| Unified Search | Org | Yes (cross-source) | N/A | Mixed | No |

*Org Filesystem search requires local tooling or combining with org docs.
