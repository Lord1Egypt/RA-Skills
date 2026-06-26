# Events + Triggers (Current)

## Use When
- You need to configure, inspect, or reason about event sources and payloads.
- You need trigger wiring for webhook, webhook replacement, or automation hooks.
- You need to map events to pipeline/jobs and automation workflows.

## Load Next
- `references/pipelines-workflows.md` for trigger-to-run mapping and dependencies.
- `references/gateways.md` for chat-originated events and provider signatures.
- `references/cli.md` for live event/pipeline inspection commands.

## Ask If Missing
- Confirm event source (`github`, `slack`, `cron`, etc.) and target project.
- Confirm required webhook signatures or integration credentials are available.
- Confirm whether you need one-time replay or persistent subscription behavior.

## Event Model

Events are stored in Postgres and routed by the orchestrator.

Core fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | TypeID (`evt_xxx`) |
| `project_id` | string | Owning project |
| `type` | string | Namespaced event type (e.g., `github.push`) |
| `source` | enum | Event origin (see sources below) |
| `status` | enum | `pending` → `processing` → `completed` / `failed` |
| `payload_json` | object | Event-specific data (varies by type) |
| `env_name` | string? | Target environment |
| `ref_sha` | string? | Git commit SHA |
| `ref_branch` | string? | Git branch name |
| `actor_type` | enum? | `user`, `system`, or `app` |
| `actor_id` | string? | Actor identifier |
| `dedupe_key` | string? | Idempotency key (prevents duplicate processing) |

## Event Sources

`github`, `slack`, `cron`, `manual`, `app`, `app_link`, `system`, `runner`, `chat`, `auth`

## Event Type Catalog

### GitHub Events

| Type | Trigger | Payload |
|------|---------|---------|
| `github.push` | Push to branch | `{ ref, commits, repository, sender, head_commit }` |
| `github.pull_request` | PR lifecycle | `{ action, number, pull_request: { head, base, title, ... } }` |

Delivered via webhook: `POST /integrations/github/events/{project_id}`. Signature verified with `X-Hub-Signature-256`.

**Quick setup:** `eve github setup --project proj_xxx` provisions the webhook secret and auto-creates the GitHub webhook via `gh` CLI (or prints manual instructions). Use `eve github test` to fire a synthetic push event and verify triggers.

### Slack Events

| Type | Trigger | Payload |
|------|---------|---------|
| `slack.message` | Message in channel | `{ text, channel, user, ts, thread_ts }` |
| `slack.app_mention` | @eve mention | `{ text, channel, user, ts }` |

Delivered via gateway: `POST /gateway/providers/slack/webhook` (or legacy `POST /integrations/slack/events`). Signature verified with Slack signing secret.

### System Events (Auto-Emitted)

| Type | Trigger | Payload |
|------|---------|---------|
| `system.job.failed` | Job execution failure | `{ job_id, attempt_id, error_message, error_code, exit_code }` |
| `system.job.attempt.completed` | Job attempt succeeded or failed | `{ job_id, attempt_id, assignee, thread_id, execution_type, status, duration_ms }` |
| `system.pipeline.failed` | Pipeline run failure | `{ run_id, pipeline_name, error_message, error_code, exit_code }` |
| `system.doc.created` | Org doc created | `{ org_id, project_id, doc_id, doc_version_id, path, version, content_hash, mutation_id, request_id, metadata }` |
| `system.doc.updated` | Org doc updated | `{ org_id, project_id, doc_id, doc_version_id, path, version, content_hash, mutation_id, request_id, metadata }` |
| `system.doc.deleted` | Org doc deleted | `{ org_id, project_id, doc_id, path, version, content_hash, mutation_id, request_id, metadata }` |
| `system.doc.ingest` | Ingest upload confirmed | `{ org_id, project_id, ingest_id, file_name, mime_type, size_bytes, storage_key, title, callback_url }` |
| `system.resource.hydration.started` | Worker begins resource hydration | `{ job_id, attempt_id, resource_count }` |
| `system.resource.hydration.completed` | Worker completes hydration | `{ job_id, attempt_id, resolved_count, missing_optional_count, failed_required_count, resources[] }` |
| `system.resource.hydration.failed` | Worker hydration failed | `{ job_id, attempt_id, resolved_count, missing_optional_count, failed_required_count, resources[] }` |

These are emitted automatically by the orchestrator. `job.failed` and `pipeline.failed` fire on failures for self-healing automation. `job.attempt.completed` fires on every attempt completion (success or failure) and is the primary trigger for post-session workflows like the learning loop.

Doc events are emitted by the org docs API. Hydration events are emitted by the worker before harness launch.

### Auth Events

Auth-policy actions emit events on the project's event spine. Operators can
subscribe webhooks to `auth.*` for real-time visibility into who's joining
which org and through which policy.

| Type | Trigger | Payload |
|------|---------|---------|
| `auth.domain_signup.invite_created` | Magic-link send for an email matching a `x-eve.auth.org_access.domain_signup` rule writes a one-shot org_invites row | `{ org_id, email_domain, matched_rule, email_hash }` |
| `auth.domain_signup.member_attached` | SSO callback consumes a `source: domain_signup` invite and upserts the user as `member` of the matched rule's `target_org` | `{ org_id, user_id, email_domain, email_hash }` |
| `auth.action_link.wrap_redeemed` | A magic-link/invite wrap is consumed by a human POST on the SSO `/m/:wrap` confirmation interstitial | `{ org_id, email_hash, kind: 'magic_link' \| 'invite', get_count, latency_ms }` |

`org_id` on both events is the matched rule's `target_org` (v2 schema; one project can route to multiple orgs depending on which rule fires). `matched_rule` on `invite_created` is the rule's domain pattern (e.g. `"*.acme.com"` for a wildcard hit on `eu.acme.com`), distinct from `email_domain` (the actual address's domain).

`email_hash` is a truncated SHA-256 of the lowercased email (`sha256:<12 hex chars>`) so the audit payload identifies retries without leaking raw addresses in webhook deliveries or stdout. The full email never appears at INFO log level.

### Webhook Events

Org and project webhooks can subscribe to event types emitted by the API. The
webhook system stores deliveries and supports replay of failed or filtered
deliveries.

### LLM Usage Events

Harnesses emit `llm.call` events after each provider call. These events contain
usage-only metadata (token counts, model identifiers) and are used for receipts
and live cost tracking. No prompt or response content is included.

### Cron Events

| Type | Trigger | Payload |
|------|---------|---------|
| `cron.tick` | Schedule fires | `{ schedule, trigger_name }` |

### Manual / App Events (Custom)

| Type | Trigger | Payload |
|------|---------|---------|
| `manual.*` | User-created via CLI/API | Any JSON |
| `app.*` | Application-emitted | Any JSON |

Custom events use any `type` string. No schema enforcement — payload can be arbitrary JSON.

### App-Link Events

Producer projects can export event feeds through `x-eve.app_links.exports`.
When a producer event matches an active consumer subscription, the orchestrator
creates a consumer-side event with:

| Field | Value |
|-------|-------|
| `source` | `app_link` |
| `type` | Same as the producer event type |
| `dedupe_key` | `app_link:<subscription_id>:<source_event_id>` |
| `payload_json.producer_event_id` | Original producer event ID |
| `payload_json.producer_project_id` | Producer project ID |
| `payload_json.producer_env_name` | Producer event env |
| `payload_json.producer_export_name` | Exported feed name |
| `payload_json.link_alias` | Consumer-local alias |
| `payload_json.original` | Original producer payload |

Deliveries are tracked in `app_link_event_deliveries` and retried by the event
router if consumer event creation fails.

## API + CLI

```bash
# List events (filterable)
eve event list [project] --type github.push --source github --status completed

# Show event details
eve event show <event-id>

# Emit a custom event
eve event emit --type manual.test --source manual --payload '{"k":"v"}'
eve event emit --type app.deploy-check --source app --env staging --branch main

# System events: type is auto-prefixed with source
# --type doc.ingest --source system → stored as system.doc.ingest
eve event emit --type doc.ingest --source system --payload '{"ingest_id":"ing_xxx","file_name":"doc.pdf"}'
```

**Event type auto-prefixing**: When `--source` is `system`, `github`, or `slack`, the CLI
auto-prefixes the type if it doesn't already start with `{source}.`. For example,
`--type doc.ingest --source system` becomes `system.doc.ingest`. This matches the
internal convention where events are stored with fully-qualified types.

API endpoints:

```
POST /projects/{project_id}/events         # Create event
GET  /projects/{project_id}/events         # List events (filters: type, source, status)
GET  /projects/{project_id}/events/{id}    # Get event details
```

## Trigger Evaluation Metadata

Events record trigger evaluation results for observability:

| Field | Type | Description |
|-------|------|-------------|
| `trigger_match_count` | int? | Number of triggers that matched (0 = no match, null = not yet processed) |
| `triggers_evaluated` | json? | Array of `{type, name, matched, reason?}` for each trigger checked |

```bash
# Show trigger evaluation details
eve event show <event-id>
# Output includes:
#   Triggers:    matched 1 of 3 evaluated
#   Trigger Evaluations:
#     ✓ workflow:ingestion-pipeline
#     ✗ workflow:alignment-check (type_mismatch)
#     ✗ pipeline:deploy (source_mismatch)
```

This makes it immediately clear whether an event triggered anything and exactly why other triggers didn't match. Mismatch reasons include: `source_mismatch`, `type_mismatch`, `branch_mismatch`, `action_mismatch`, `no_trigger`, `manual_trigger`.

## Trigger Routing

The orchestrator polls pending events, matches them against manifest triggers, and creates pipeline runs or workflow jobs.

Claiming mechanics use `FOR UPDATE SKIP LOCKED`, so multiple orchestrator
instances can process the queue without double-claiming.

Events can include a `dedupe_key`; the API checks for an existing event with
the same key before creating a new record.

### How Triggers Work

1. Event arrives in the events table (status: `pending`)
2. Orchestrator polls every ~5 seconds
3. Loads project manifest and checks all pipeline/workflow triggers
4. If a trigger matches, creates a pipeline run or workflow job
5. Marks event as `completed` (or `failed`)

### Trigger Types

Triggers are defined in the manifest under `pipelines.<name>.trigger` or `workflows.<name>.trigger`.

#### GitHub Trigger

```yaml
trigger:
  github:
    event: push              # "push" or "pull_request"
    branch: main             # Branch pattern (supports wildcards)
```

```yaml
trigger:
  github:
    event: pull_request
    action: [opened, synchronize, reopened]   # PR actions to match
    base_branch: main                          # Target branch filter
```

Supported PR actions: `opened`, `synchronize`, `reopened`, `closed`.
Branch patterns: exact (`main`), prefix wildcards (`release/*`), suffix wildcards (`*-prod`).

#### Slack Trigger

```yaml
trigger:
  slack:
    event: message           # Slack event type
    channel: C123ABC         # Channel ID
```

#### System Trigger (Self-Healing)

```yaml
trigger:
  system:
    event: job.failed        # "job.failed" or "pipeline.failed"
    pipeline: deploy         # Optional: scope to specific pipeline
```

Use system triggers to build automated remediation flows. When a job or pipeline fails, the system event triggers a recovery pipeline or workflow.

#### Cron Trigger

```yaml
trigger:
  cron:
    schedule: "0 */6 * * *"  # Standard cron expression
```

#### App Trigger (Application Events)

```yaml
trigger:
  app:
    event: document.uploaded  # Matches event.type from source=app
```

Use app triggers for event-driven workflows within your application. Emit events via the API (`eve event emit --source app --type document.uploaded`) and the orchestrator auto-dispatches matching workflows.

#### App-Link Trigger (Cross-Project Events)

```yaml
trigger:
  app_link:
    alias: observation        # Consumer-local x-eve.app_links.consumes alias
    type: app.observation.created
```

The `app_link` trigger is a shorthand for consumer-side events with
`source=app_link`. It can filter by subscription alias and event type.

#### Generic Event Trigger

```yaml
trigger:
  event:
    source: app              # Any event source (app, runner, chat, etc.)
    type: document.uploaded   # Optional type filter
```

The generic `event` trigger matches any event source+type combination. Use this when your events come from non-standard sources. The `app` trigger is a shorthand for `event.source: app`.

#### Manual Trigger (No Auto-Trigger)

```yaml
trigger:
  manual: true               # Only runs when explicitly invoked
```

### Complete Trigger Example

```yaml
pipelines:
  ci:
    trigger:
      github:
        event: pull_request
        action: [opened, synchronize]
        base_branch: main
    steps:
      - name: test
        script: { run: "pnpm test" }

  deploy:
    trigger:
      github:
        event: push
        branch: main
    steps:
      - name: build
        action: { type: build }
      - name: deploy
        depends_on: [build]
        action: { type: deploy, env_name: staging }

  self-heal:
    trigger:
      system:
        event: job.failed
        pipeline: deploy
    steps:
      - name: diagnose
        agent: { prompt: "Diagnose the failed deploy and suggest a fix" }

workflows:
  process-upload:
    trigger:
      app:
        event: document.uploaded
    steps:
      - name: ingest
        agent: { prompt: "Process the uploaded document" }
```
