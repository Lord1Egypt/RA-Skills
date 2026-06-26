# Jobs Reference

## Use When
- You need to inspect job lifecycle phases, attempts, and dependencies.
- You need to tune scheduling, review, or retry behavior.
- You need to follow, stream, or debug running/failed jobs.

## Load Next
- `references/cli.md` for job list/show/follow/result commands.
- `references/pipelines-workflows.md` when jobs are part of pipeline execution.
- `references/deploy-debug.md` for infrastructure-side runtime symptoms.

## Ask If Missing
- Confirm whether you are working with a root job or child attempt.
- Confirm target job ID, org/project scope, and desired action (`list`/`show`/`follow`).
- Confirm whether you need to review dependency graph or submission state.

## Entity Model

```
Job → JobAttempt → Session → ExecutionProcess
```

- **Job**: Logical unit of work. ID: `{slug}-{hash8}` (e.g., `myproj-a3f2dd12`).
- **JobAttempt**: Isolated execution run. Has UUID `id` + job-scoped `attempt_number` (1, 2, 3...).
- **Session**: Tracks executor within an attempt. May change on reconstruction; attempt_id stays stable.
- **ExecutionProcess**: Single harness invocation within a session.

Child jobs use `{parent}.{n}` format (e.g., `myproj-a3f2dd12.1`). Max depth: 3 levels.

## Lifecycle

**Phases:** `idea` → `backlog` → `ready` → `active` → `review` → `done` | `cancelled`

Jobs default to `ready` (immediately schedulable). Priority: 0-4 (P0 highest, default 2).

**Scheduling order:** Filter phase=ready + all deps done → sort by priority (ascending) → sort by created_at (FIFO).

## API Endpoints

### Project-Scoped

```
POST /projects/{project_id}/jobs              Create job
GET  /projects/{project_id}/jobs              List jobs
GET  /projects/{project_id}/jobs/ready        Ready/schedulable jobs
GET  /projects/{project_id}/jobs/blocked      Blocked jobs
GET  /jobs                                     List jobs (admin, cross-project)
```

### Job-Scoped

```
GET    /jobs/{job_id}                          Get job
PATCH  /jobs/{job_id}                          Update job
GET    /jobs/{job_id}/tree                     Job hierarchy
GET    /jobs/{job_id}/context                  Context + derived status
GET    /jobs/{job_id}/dependencies             List dependencies
POST   /jobs/{job_id}/dependencies             Add dependency
DELETE /jobs/{job_id}/dependencies/{related}   Remove dependency
```

### Claim, Release, Attempts

```
POST /jobs/{job_id}/claim                      Claim (creates attempt, moves to active)
POST /jobs/{job_id}/release                    Release attempt
GET  /jobs/{job_id}/attempts                   List attempts
GET  /jobs/{job_id}/attempts/{n}/logs          Attempt logs
GET  /jobs/{job_id}/attempts/{n}/stream        SSE log stream for attempt
```

### Monitoring

```
GET /jobs/{job_id}/result                      Latest or attempt-specific result
GET /jobs/{job_id}/wait                        Block until completion (SSE, default 300s)
GET /jobs/{job_id}/stream                      SSE log stream for job
```

### Review Workflow

```
POST /jobs/{job_id}/submit                     Submit for review (requires summary)
POST /jobs/{job_id}/approve                    Approve (optional comment)
POST /jobs/{job_id}/reject                     Reject (requires reason)
```

### Thread Endpoints (Coordination)

```
GET  /threads/{id}/messages?since=<iso>&limit=<n>    List messages
POST /threads/{id}/messages                          Post message
```

## Resource Refs

`resource_refs` attach org documents or job attachments to a job. The worker
hydrates them into `.eve/resources/` before harness launch.

```json
[
  {
    "uri": "org_docs:/pm/features/FEAT-123.md@v4",
    "label": "Approved Plan",
    "required": true,
    "mount_path": "pm/approved-plan.md"
  }
]
```

Fields:
- `uri` (required): `org_docs:/path[@vN]` or `job_attachments:/job_id/name`
- `label` (optional): human readable
- `required` (optional, default true): fail provisioning when missing
- `mount_path` (optional): relative path under `.eve/resources/`

## CLI Quick Reference

### Create

```bash
eve job create --description "Fix the login bug"
eve job create --parent myproj-a3f2dd12 --description "Sub-task"
eve job create --description "Review" --harness mclaude --model opus-4.5 --reasoning high
eve job create --description "Fix checkout" \
  --git-ref main --git-branch job/fix-checkout \
  --git-create-branch if_missing --git-commit auto --git-push on_success

# Resource refs (org docs + attachments)
eve job create --project proj_xxx --description "Review brief" \
  --resource-refs='[{"uri":"org_docs:/pm/features/FEAT-123.md@v4","required":true,"mount_path":"pm/brief.md","label":"Approved Plan"}]'
```

Resource refs mount into `.eve/resources/` before harness start. The worker writes
`.eve/resources/index.json` and injects `EVE_RESOURCE_INDEX` for agents.

### App API Awareness

```bash
eve job create --description "Analyze data" --with-apis coordinator,analytics
eve job create --description "Analyze producer observations" --with-links observation
```

`--with-apis` is now **server-side**: the CLI passes `app_apis` in job hints
instead of generating instructions client-side. The server validates that the
named APIs exist for the project, generates the instruction block (with a
runtime-safe Node `fetch` helper using `EVE_JOB_TOKEN`), and appends it to the
job description. This ensures consistent behavior across CLI, API, workflow, and
SDK job creation paths.

`--with-links` requests named `x-eve.app_links.consumes` subscriptions for the
job. Subscriptions with `inject_into.jobs: true` are also auto-discovered for
direct jobs and workflow step jobs, including worker-executed `script:` and
`run` steps. The runtime mints short-lived app-link tokens and injects
`EVE_APP_LINK_<ALIAS>_API_URL`, `EVE_APP_LINK_<ALIAS>_TOKEN`,
`EVE_APP_LINK_<ALIAS>_SCOPES`, `EVE_APP_LINK_<ALIAS>_PROJECT`,
`EVE_APP_LINK_<ALIAS>_ENV`, and `EVE_APP_LINK_<ALIAS>_CLI` when the producer
exported an image-mode CLI. Platform status logs name injected keys only;
scripts that print diagnostics must redact token values.

### Attachments

```bash
eve job attach <job-id> --file ./report.pdf --name report.pdf
eve job attach <job-id> --stdin --name output.json --mime application/json
eve job attachments <job-id>           # List attachments
eve job attachment <job-id> <name>     # Fetch attachment content
```

### Batch Operations

```bash
eve job batch --project proj_xxx --file batch.json    # Submit batch job graph
eve job batch-validate --file batch.json              # Validate without submitting
```

### List and View

```bash
eve job list --phase active
eve job list --since 1h --stuck
eve job ready                                  # Schedulable jobs
eve job blocked                                # Waiting on deps
eve job show <job-id>
eve job current                                # From EVE_JOB_ID
eve job tree <job-id>
eve job diagnose <job-id>
```

### Update and Complete

```bash
eve job update <job-id> --phase active --priority 0
eve job close <job-id> --reason "Done"
eve job cancel <job-id> --reason "No longer needed"
```

### Monitor Execution

```bash
eve job follow <job-id>                        # Stream logs (SSE)
eve job wait <job-id> --timeout 120 --json     # Block until done
eve job watch <job-id>                         # Status polling + log streaming
eve job result <job-id> --format text           # Get result
eve job result <job-id> --attempt 2 --format json
eve job runner-logs <job-id>                    # kubectl pod logs
```

`wait` exit codes: 0=success, 1=failed, 124=timeout, 125=cancelled.

### Script and Action-Run Execution

Pipeline/workflow script jobs and pipeline `action: { type: run }` jobs are
worker-executed bash commands. The orchestrator submits these jobs to the worker
with a short request and then waits for runner events, so long-running commands
are not tied to a single open HTTP request.

Output behavior:
- stdout/stderr are appended to attempt logs while the command is still running.
- `eve job follow <job-id>` and `eve job logs <job-id> --attempt <n>` show the
  streamed entries.
- Final job results keep a bounded stdout/stderr tail for quick inspection.
- Per-stream output is capped by `EVE_SCRIPT_OUTPUT_CAP_BYTES` (default 10 MiB).
  When the cap is reached, Eve drains the process output and writes one
  `output_truncated` warning per stream.

Timeout behavior:
- Script jobs use `jobs.script_timeout_seconds` first, then
  `hints.timeout_seconds`, then the 30-minute default.
- Pipeline `action: { type: run }` jobs use `action_input.timeout_seconds`,
  then `action_input.timeout`, then `hints.timeout_seconds`, then the 30-minute
  default.
- Script timeout logs use code `script_timeout`; action-run timeout logs use
  `action_run_timeout`.
- If the worker never publishes a terminal runner event, the orchestrator marks
  the attempt failed with `poll_timeout`.

### Claim/Release (Agent Use)

```bash
eve job claim <job-id> --agent my-agent --harness mclaude
eve job release <job-id> --reason "Need info"
eve job attempts <job-id>
eve job logs <job-id> --attempt 2
```

### Review

```bash
eve job submit <job-id> --summary "Implemented fix, added tests"
eve job approve <job-id> --comment "LGTM"
eve job reject <job-id> --reason "Missing tests"
```

### Dependencies

```bash
eve job dep add <job-id> <depends-on-id>
eve job dep remove <job-id> <depends-on-id>
eve job dep list <job-id>
```

### Supervision and Thread Coordination

```bash
eve supervise                                  # Long-poll child events (current job)
eve supervise <job-id> --timeout 60
eve thread messages <thread-id> --since 5m
eve thread post <thread-id> --body '{"kind":"directive","body":"focus on auth"}'
eve thread follow <thread-id>
```

## Dependency Model

Relations between jobs: `blocked_by`, `blocks`, `waits_for`, `conditional_blocks`.

- `blocked_by[]`: Job IDs that must complete before this job starts.
- `blocks[]`: Sets the reverse relationship on blocking jobs.
- Scheduler filters out blocked jobs from the ready queue.

```bash
eve job create --description "Deploy to staging" # then:
eve job dep add <deploy-job> <build-job>
```

## Job Context

**Endpoint:** `GET /jobs/{job_id}/context` | **CLI:** `eve job current [--json|--tree]`

Response shape:

```
{ job, parent, children, relations: { dependencies, dependents, blocking },
  latest_attempt, latest_rejection_reason, blocked, waiting, effective_phase }
```

**Derived fields:**
- `blocked`: true when unresolved blocking relations exist.
- `waiting`: true when latest attempt returned `result_json.eve.status == "waiting"`.
- `effective_phase`: priority order `blocked` → `waiting` → `job.phase`.

Use `effective_phase` for display and orchestration decisions, not raw `phase`.

## Control Signals

Harnesses emit a `json-result` block. The worker extracts the **last** one and stores it as `job_attempts.result_json`.

```json-result
{
  "eve": {
    "status": "waiting",
    "summary": "Spawned 3 child jobs, added waits_for relations",
    "reason": "Waiting on child jobs to complete"
  }
}
```

**`eve.status` values:**
- `success`: Normal success path (review or done based on job settings).
- `waiting`: Attempt succeeds, job requeued to `ready`, assignee cleared. No review submission. If no blockers exist, orchestrator applies `defer_until` backoff to prevent tight loops.
- `failed`: Normal failure path.

**`eve.summary`**: Persisted to `job_attempts.result_summary` for quick visibility.

## Git Controls

Job-level git configuration governs ref resolution, branch creation, commit, and push behavior.

### Configuration Object

```json
{
  "git": {
    "ref": "main",
    "ref_policy": "auto",
    "branch": "job/${job_id}",
    "create_branch": "if_missing",
    "commit": "auto",
    "commit_message": "job/${job_id}: ${summary}",
    "push": "on_success",
    "remote": "origin"
  },
  "workspace": {
    "mode": "job",
    "key": "session:${session_id}"
  }
}
```

**Precedence:** explicit job fields → `x-eve.defaults.git` (manifest) → project defaults.

### Ref Resolution (`ref_policy`)

| Policy | Behavior |
|--------|----------|
| `auto` | env release SHA → manifest defaults → project default branch |
| `env` | Requires `env_name` + current release SHA |
| `project_default` | Always uses `project.branch` |
| `explicit` | Requires `git.ref` to be set |

### Repo Auth

- HTTPS: uses `github_token` secret (e.g., `GITHUB_TOKEN`).
- SSH: uses `ssh_key` secret via `GIT_SSH_COMMAND`.
- Missing auth fails fast with remediation hints (`eve secrets set`).

### Branch Creation (`create_branch`)

| Value | Behavior |
|-------|----------|
| `never` | Branch must already exist |
| `if_missing` | Create only when missing (default when `branch` is set) |
| `always` | Reset branch to `ref` |

### Commit Policy (`commit`)

| Value | Behavior |
|-------|----------|
| `never` | No commits |
| `manual` | Agent decides when to commit (default) |
| `auto` | Worker runs `git add -A` + commit after execution, even on failure |
| `required` | On success, fail attempt if working tree is clean |

### Push Policy (`push`)

| Value | Behavior |
|-------|----------|
| `never` | No push (default) |
| `on_success` | Push only when worker created commits in this attempt |
| `required` | Attempt push; no-op if no commits. Fail if push fails. |

Push without git credentials fails fast.

### Attempt Git Metadata (Audit)

Resolved values stored on attempt for debugging:

```json
{
  "resolved_ref": "refs/heads/main",
  "resolved_sha": "abc123",
  "resolved_branch": "job/myproj-a3f2dd12",
  "ref_source": "env_release|manifest|project_default|explicit",
  "pushed": true,
  "commits": ["def456"]
}
```

Also promoted to `JobResponse.resolved_git` from the latest successful attempt.

## Harness Selection

Target a harness directly or via a project profile (`x-eve.agents`):

| Flag | Purpose |
|------|---------|
| `--harness` | Harness name (mclaude, codex, gemini, zai) |
| `--profile` | Profile from `x-eve.agents` |
| `--variant` | Config overlay preset |
| `--model` | Model override |
| `--reasoning` | Effort: low, medium, high, x-high |

### Per-Job Harness & Env Overrides

Per-invocation overrides let consumer apps pick a different brain (model, endpoint,
BYOK credentials, reasoning) for one job without mutating shared `x-eve.yaml`.

Job columns (migration `00090_per_job_harness_overrides.sql`):

- `harness_profile_override` (JSONB) — inline bundle `{harness, model, reasoning_effort, variant?, temperature?}`
- `env_overrides` (JSONB) — env values, may contain `${secret.KEY}` placeholders (kept verbatim until spawn)
- `harness_profile_source` — `agent_default | string_ref | inline_override | workflow_template`
- `harness_profile_hash` — stable hash of the normalized override (no plaintext secrets)

Same `_source` and `_hash` columns are mirrored on `job_attempts` for routing logs and
analytics. Direct job creation projects the effective profile into the legacy
`jobs.harness` + `jobs.harness_options` columns before insert so the orchestrator
actually runs the requested profile.

**Precedence:** `workflow_template > inline_override > string_ref > agent_default`.
A job containing both `harness_profile` (string ref) and `harness_profile_override`
emits a single `harness.profile.conflict` warning log; inline wins.

**Validation rules** (enforced in shared resolver + DTO):

- `env_overrides` keys must match `^[A-Z_][A-Z0-9_]*$`; reject reserved keys/prefixes
  (`EVE_*`, `PATH`, `HOME`, `SHELL`, `USER`, `TMPDIR`, `NODE_OPTIONS`,
  `CLAUDE_CONFIG_DIR`, `CODEX_HOME`).
- Values may contain literals plus `${secret.KEY}` placeholders only — other `${...}`
  expressions are rejected.
- Total `env_overrides` JSON ≤ 4 KB.
- Overrides are **create-only**; once an attempt exists they cannot be patched.

**Permissions:** `jobs:harness_override` is required on any create that includes
override fields. `secrets:read` is additionally required when `env_overrides`
contains `${secret.KEY}` references. Both are enforced on direct job creation,
chat dispatch (against the resolved Eve principal), and the validate endpoint.

**Secret interpolation flow:** API stores placeholders intact → orchestrator forwards
unchanged → shared invoke module resolves at spawn time against already-resolved
project secrets via `interpolateEnvOverrides()` → resolved values merged into
`adapterEnv` after reserved-key strip. Missing references fail fast with
`error_code = missing_secret_override` before harness launch. Resolved plaintext
never appears in job rows, attempts, receipts, or execution logs. Chat-triggered
jobs that fail with `missing_secret_override` post a structured error back to the
originating chat thread (and coordination thread for team dispatch) via
`EveMessageRelay.deliverProvisioningError`.

**Routing log attribution:** the orchestrator's `routing` execution log records
`harness_profile_name`, `harness_profile_source`, `harness_profile_hash`,
`effective_harness`, `effective_model`, and `effective_effort` so receipts and
analytics can group cost by harness profile.

**Chat hint propagation:** chat requests (`/chat/route`, `/chat/dispatch`,
`/chat/simulate`) accept a typed `hints` object carrying
`harness_profile_override` + `env_overrides`. A legacy `metadata.hints` alias
is bridged for gateway payloads. All 8 chat dispatch sites — direct agent,
direct team lead + relay/fanout/council members, route → agent, route → team
lead variants — propagate overrides into every lead and child job, listener jobs
included. The override snapshot is also written to thread metadata
(`threads.metadata.harness_overrides`) on the chat and coordination threads,
with placeholders intact.

**Workflow templating:** workflow steps may set `harness_profile` or
`harness_profile_override` with `${inputs.<key>}` and
`${event.payload.<dotted.path>}` template expressions. `workflow.inputs.<name>`
declarations bind those inputs (with optional `from: event.payload.<path>` and
`default:`). The expression engine is intentionally tiny — no operators, no
function calls. Manifest sync rejects malformed templates and undeclared
`${inputs.*}` references; missing event payload fields at runtime fall back to
the agent default with a warning, not an error. See pipelines-workflows.md for
the workflow-side coverage.

CLI flags on `eve job create` (and via API as `harness_profile_override` /
`env_overrides`):

```bash
eve job create --description "..." \
  --harness-override-file ./overrides.json \
  --env-override ANTHROPIC_BASE_URL='${secret.EDEN_TEST_BASE_URL}' \
  --env-override OPENAI_BASE_URL='${secret.EDEN_OPENAI_URL}'
```

`--env-override` is repeatable. `eve job show <id> --json` returns the
override and env placeholders verbatim.

### Per-Job Token Scope

Job tokens carry an explicit resource scope, not just permission names. The
scope is persisted on `jobs.token_scope` (migration `00096_jobs_token_scope.sql`)
and signed into the JWT, so the on-disk `.org` mount and the API authority
match. `NULL` token scope means no narrowing (legacy permission-name-only
behavior).

Supported axes:

```json
{
  "orgfs":   { "allow_prefixes": ["/groups/projects/proj-a/**"] },
  "orgdocs": { "read_only_prefixes": ["/briefs/**"] },
  "envdb":   { "schemas": ["public"], "tables": ["public.jobs"] },
  "cloud_fs":{ "allow_mount_ids": ["mount_a"] }
}
```

Enforcement happens at every layer that handles the job token — API
(`ScopedAccessService` for orgfs/orgdocs/envdb/cloud_fs), orchestrator (mount
materialization), worker and agent-runtime (workspace `.org` symlinks), and
cloud-fs controller (per-mount checks).

**Propagation chain** (parallels `env_overrides`): workflow-level `scope` →
step-level `scope` → workflow invoke request `scope` are **intersected** for
each executable step job and persisted as `jobs.token_scope`. Invocation
scope may narrow but never widen the manifest. Request-supplied `scope`
requires `jobs:harness_override`. There is no `eve job create --scope-*` or
`eve workflow run --scope-*` flag yet — declare scope in the workflow/step
manifest or the API body. See `references/pipelines-workflows.md` for the
workflow-side coverage and `references/secrets-auth.md` for the permission
model.

`eve job show <id> --json` surfaces the resolved scope under `token_scope`.

### Per-Job Token Permissions

Sibling field to `token_scope`. Pipeline `script:` and `action: { type: run }`
steps (and workflow agent steps that opt in) can declare a per-step
`permissions: [...]` list in the manifest. The expander resolves it
(step-level wins over pipeline/workflow-level) and persists it on
`jobs.token_permissions` (migration `00099_jobs_token_permissions.sql`).
`NULL` means "use the executor's default":

| Execution type | Default | Source |
| --- | --- | --- |
| `agent` | `DEFAULT_AGENT_PERMISSIONS` | `packages/shared/src/permissions.ts` |
| `script` | `DEFAULT_SCRIPT_JOB_PERMISSIONS` | `packages/shared/src/permissions.ts` |
| `action: { type: run }` | `DEFAULT_ACTION_RUN_JOB_PERMISSIONS` (least-privilege) | `packages/shared/src/permissions.ts` |

The script and action-run executors mint `EVE_JOB_TOKEN` with the resolved
list, write `~/.eve/credentials.json` into a workspace-local HOME, and
sanitise the env so `EVE_INTERNAL_API_KEY` does not leak into user shell.

The expander also rejects any permission the invoking actor does not
themselves hold (`assertActorCanGrantPermissions`), so workflow authors
can narrow but not escalate.

`eve job show <id> --verbose` and `eve job diagnose <id>` render a
`Token:` block with both `Permissions:` and `Scope:`. `diagnose` adds
`⚠ scope.* set but permissions[] missing X` warnings for obvious
misalignments.

## Scheduling Hints

Preferences (not requirements) that influence scheduling:

| Hint | Description |
|------|-------------|
| `worker_type` | e.g., `default`, `gpu` |
| `permission_policy` | `yolo` (default), `auto_edit`, `never` |
| `timeout_seconds` | Execution timeout hint. Script jobs prefer `script_timeout_seconds`; `action: { type: run }` jobs prefer `action_input.timeout_seconds` / `action_input.timeout`; this hint is the fallback before the 30-minute default |
| `max_cost` | Authoritative per-attempt budget cap; prefer this over token caps |
| `max_tokens` | Coarse guardrail; cache-read tokens are discounted by rate-card weight when cheaper than input tokens |
| `toolchains` | Resolved toolchains for agent, workflow/pipeline script, shorthand `run`, or pipeline `action: { type: run }` jobs. Runtime provisioning details appear in `runtime_meta.toolchains` and `eve job diagnose <id>` |

Budget-configured attempts emit `budget.summary` on completion and
`budget.exceeded` when enforcement fires. Inspect them with
`eve job logs <id> --json` or `eve job diagnose <id> --json`. Both rows retain
`total_tokens` and add `weighted_tokens`, `cache_read_tokens`,
`cache_read_token_weight`, and `cache_read_tokens_excluded`.

## Coordination Threads

Team dispatches create coordination threads with key `coord:job:{parent_job_id}`. Thread ID stored in `hints.coordination.thread_id`.

Child agents receive `EVE_PARENT_JOB_ID` to derive the coordination key. On attempt completion, the orchestrator auto-posts a status summary to the thread.

**Inbox file:** `.eve/coordination-inbox.md` is regenerated from recent thread messages at job start.

**Message kinds:** `status` (auto summary), `directive` (lead→member), `question` (member→lead), `update` (progress).

## Agent Environment Variables

Injected by the worker during execution:

- `EVE_PROJECT_ID` — current project
- `EVE_JOB_ID` — current job
- `EVE_ATTEMPT_ID` — current attempt UUID
- `EVE_AGENT_ID` — agent identifier
- `EVE_PARENT_JOB_ID` — parent job (for coordination)

## Agent-Native Job Monitoring

### Event→Job Linkage

When the orchestrator processes an event and creates a workflow job, it writes the `job_id` back to the event record. Use `eve event show <event-id>` to see which job an event triggered. This enables tracing from event source through to job execution.

### Workflow-Aware List Filtering

```bash
eve job list --label workflow:ingestion-pipeline --root   # Root workflow jobs only
eve job list --type agent --since 1h                      # Filter by job type
eve job list --dead-letters                                # Failed (not cancelled) jobs
eve job list --disposition failed                          # Explicit disposition filter
```

Flags: `--label`, `--type`, `--root` (root jobs only, excludes children), `--dead-letters` (shorthand for `--phase cancelled --disposition failed`), `--disposition` (`failed` | `cancelled` | `upstream_failed`).

### Summary Follow Mode

```bash
eve job follow <job-id> --summary
eve job logs <job-id> --summary
```

`--summary` emits only actionable lines: phase transitions, permission rejections, periodic LLM cost/token aggregates, tool names (no I/O), eve-message blocks, errors, and a final summary footer with totals (LLM calls, tokens in/out, cost, tool uses). Cuts hundreds of raw JSONL lines to ~20 lines.

### Active-Job Observability

For active jobs, the CLI now exposes the same signals operators previously had to cross-check in kubectl:

- `eve job diagnose <job-id>` includes the latest attempt pod name from `runtime_meta`, best-effort live pod health from agent-runtime status, and the most recent harness heartbeat age.
- For classified failures, `diagnose` renders `result_json.error_code` such as
  `toolchain_unavailable`, `attempt_init_timeout`, `attempt_startup_timeout`,
  `attempt_timeout`, or `attempt_stale`.
- For declared toolchains, `diagnose` renders `runtime_meta.toolchains`
  (`execution_mode`, `requested`, `resolved`, `missing`, `source`) and recent
  provisioning log lines.
- `eve job follow <job-id>` warns after 60s and 120s of silence. If heartbeat lifecycle events are still arriving, it reports the harness as alive but quiet; otherwise it warns that the run may have stalled.
- `eve agents runtime-status --org <org-id>` now shows stale pods and active-job counts in the tabular output.
- `eve system status` now renders agent-runtime health alongside API, orchestrator, worker, and queue state when the backend returns it.

## Production Hardening

### Content-Hash Deduplication (Ingest)

`eve ingest confirm` checks the S3 ETag as a content fingerprint. If an identical file was already confirmed in the same project, it returns the existing record (`deduplicated: true`) instead of firing a new processing event. Use `--force` to skip the dedup check.

### Failure Disposition (Dead Letters)

Jobs have a `failure_disposition` field distinguishing intentional cancellation from exhausted-retry failure:

| Value | Meaning |
|-------|---------|
| `cancelled` | Explicitly cancelled by user/API |
| `failed` | Failed after exhausting retries |
| `upstream_failed` | Cascaded failure from upstream dependency |

Query dead letters: `GET /projects/{id}/jobs?phase=cancelled&failure_disposition=failed`

### Auto-Retry with Backoff

Configure retry policy via hints or CLI:

```bash
eve job create --description "Process data" --retry-max 3 --retry-backoff 30
```

Policy fields (in `hints.retry`):
- `max_attempts` — max attempts before permanent failure (default: 1 = no retry)
- `backoff_seconds` — base delay (default: 60)
- `backoff_multiplier` — exponential multiplier (default: 2)
- `retryable_errors` — error codes eligible for retry (default: `['attempt_timeout', 'attempt_stale']`)

On failure, the orchestrator checks the retry policy. If retries remain and the error is retryable, it creates a new attempt with `trigger_type = 'auto_retry'` and sets `defer_until` for backoff. When retries are exhausted, the job gets `failure_disposition = 'failed'`.

Manual workflow-step retry is separate from per-job auto-retry. Use
`eve workflow retry <root-job-id> --failed` after a workflow root reaches a
terminal state and a failed/upstream-failed tail should be retried without
rerunning successful predecessor steps. Use `--from <step-name>` to rerun a
named step and its downstream dependents. Eve creates replacement child jobs,
marks the replaced step jobs superseded in `hints`, and rewires dependencies to
the current replacement jobs.

Workflow steps support retry in the manifest:

```yaml
steps:
  - name: ingest
    agent: doc-processor
    retry:
      max_attempts: 3
      backoff_seconds: 30
      retryable_errors: [attempt_timeout, attempt_stale]
```

### Cost Tracking

```bash
eve analytics cost-by-agent --window 7d
```

Groups cost by agent across all projects in the org. Shows attempts, total cost, and token counts per agent.

### Per-Phase Latency in Diagnostics

`eve job diagnose` now shows a latency waterfall from existing lifecycle execution logs:

```
Latency Breakdown:
  provision/clone     12,340ms  ████████░░░░░░░░  14%
  provision/setup      2,100ms  █░░░░░░░░░░░░░░░   2%
  invoke/harness      71,200ms  ████████████████  82%
  cleanup/workspace    1,400ms  █░░░░░░░░░░░░░░░   2%
  ────────────────────────────
  Total               87,040ms
```

The same diagnostic view now adds:
- pod health correlation for active jobs when the latest attempt includes `runtime_meta.pod_name`
- heartbeat-aware stuck detection (`Harness alive` vs `No harness heartbeat`)
- pre-harness startup timing visibility, including clone/setup work that previously required pod logs

### Routing Decision Logging

A structured `routing` execution log is written at claim time, capturing harness selection, target (agent-runtime vs worker), budget config, and selection source. Visible in `eve job diagnose` and `eve job logs`.

The routing log payload includes harness-profile attribution: `harness_profile_name`,
`harness_profile_source` (`agent_default | string_ref | inline_override |
workflow_template`), `harness_profile_hash` (no plaintext secrets), plus
`effective_harness`, `effective_model`, and `effective_effort`. The same
attribution is mirrored on `job_attempts.harness_profile_source` /
`harness_profile_hash` so analytics can group cost by profile without scanning
log JSON.

### Recovery & Resilience

Every job assignee — not just `orchestrator` — is in scope for the watchdog:

- `recoverAttemptInitTimeouts` fails attempts that were claimed but never
  reached runtime acceptance (`execution_started_at IS NULL`) within
  `EVE_ORCH_ATTEMPT_INIT_TIMEOUT_SECONDS` (default 300s). Durable code:
  `attempt_init_timeout`.
- `recoverAttemptStartupTimeouts` fails accepted attempts that never emitted
  `lifecycle_harness_start` within
  `EVE_ORCH_ATTEMPT_STARTUP_TIMEOUT_SECONDS` (default 600s). Durable code:
  `attempt_startup_timeout`.
- Stale/hard-timeout recovery stores `attempt_stale` or `attempt_timeout` in
  `result_json.error_code`.
- `recoverActiveJobsWithTerminatedAttempts` periodic sweep catches jobs left
  `active` after their attempts were finalized externally (pod drain, recovery,
  agent-runtime restart). Sweep grace period via `EVE_ORCH_TERMINATED_GRACE_SECONDS`
  (default 30s); recovery completes in ~35s instead of 30 minutes.
- `processJob` and its error-handler path now transition job phase even when the
  attempt was finalized externally, so `attemptSucceeded` is set for the
  ingest-sync `finally` block.
- Agent-runtime has a graceful-shutdown handler: on `SIGTERM`, all running
  attempts are marked failed with `error_code = pod_terminated` and the pod
  status is set to `draining` so no new work routes there. K8s manifest sets
  `preStop: sleep 5` and `terminationGracePeriodSeconds: 120s`.
- Agent-runtime auto-discovers orgs from the API (DB fallback) on startup and
  re-discovers every 5 minutes. The placeholder `org_default` is gone; the
  heartbeat endpoint returns 404 (not 500) when an org is missing, so silent FK
  failures no longer mask unregistered pods.

### Action vs Ad-Hoc Env Gates

`defaults.env` no longer forces every ad-hoc agent job to acquire an exclusive
environment mutex. The env gate now requires `action_type` (`deploy`, `build`,
`migrate`) before serializing on environment. Ad-hoc agent jobs keep `env_name`
for API resolution but run in parallel. Workflow / pipeline action jobs are
unchanged.

### Job List Defaults

`eve job list` returns newest-first by default — recent jobs are no longer
hidden behind page boundaries. The build step auto-syncs the manifest from the
cloned repo when the manifest hash changes, so workflow trigger definitions
stay current after each deploy without a separate `eve project sync`.

### Job Completion Event

The orchestrator emits `system.job.attempt.completed` on every attempt finish
path — success, failure, and orchestrator error. Payload:

```json
{
  "job_id": "myproj-a3f2dd12",
  "attempt_id": "att_...",
  "assignee": "my-agent",
  "thread_id": "thr_...",
  "execution_type": "agent",
  "status": "succeeded|failed",
  "duration_ms": 12345
}
```

Use this event to drive post-session learning workflows. The event is registered
in `KNOWN_SYSTEM_EVENTS`, so `eve agents sync` / manifest validation accepts
`trigger.system.event: job.attempt.completed` without warnings. Carryover
context now also materializes the `user` memory category alongside `learnings`,
`decisions`, `runbooks`, `context`, and `conventions` — for per-user preferences
that should ride forward to the next session.

### Auto-Expiry for Stale Documents

Org documents with `expires_at` are automatically transitioned to `expired` status by a background loop (every 15 minutes). After a grace period (default 7 days, configurable via `EVE_DOC_EXPIRY_GRACE_DAYS`), expired documents are archived (content cleared, metadata preserved).

## Per-Job HOME Isolation

Each job attempt gets an isolated HOME directory at `/tmp/eve/agent-homes/<attemptId>/home/`. The worker overrides `HOME` and sets `EVE_JOB_USER_HOME` in the harness environment. Pre-created directories:

- `.config/eve/` — Eve CLI credentials
- `.config/gh/` — GitHub CLI auth
- `.claude/` — Claude config
- `.eve/harnesses/` — Harness config

All directories are mode 0700. Cleaned up after the attempt completes. This prevents agents from reading credentials written for other jobs or the host system.

## Not Yet Implemented

- Workspace reuse (`workspace.mode=job|session|isolated`). Today every attempt gets a fresh workspace.
- Disk LRU/TTL cleanup policies.
- Review semantics that compute diffs for branch-based jobs.
