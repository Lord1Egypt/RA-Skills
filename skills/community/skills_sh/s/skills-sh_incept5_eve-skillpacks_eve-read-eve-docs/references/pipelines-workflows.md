# Pipelines + Workflows (Current)

## Use When
- You need to define, run, inspect, or debug pipeline and workflow automation.
- You need trigger wiring for environment deploy and event-based job orchestration.
- You need guidance on build-release-deploy and promotion patterns.

## Load Next
- `references/events.md` if the trigger source is webhook or scheduled.
- `references/builds-releases.md` for image/release semantics and diagnostics.
- `references/cli.md` for pipeline/workflow execution commands.

## Ask If Missing
- Confirm pipeline/workflow name, target env, and repo ref/hash.
- Confirm whether you want standard pipeline execution or direct deploy mode.
- Confirm which inputs/outputs are required before creating or re-running steps.

## Pipelines (Manifest)

Pipelines are ordered steps that expand into a job graph. Define them in `.eve/manifest.yaml`.

```yaml
pipelines:
  deploy-test:
    trigger:
      github:
        event: push
        branch: main
    steps:
      - name: build
        action: { type: build }
      - name: unit-tests
        script: { run: "pnpm test", timeout_seconds: 1800 }
      - name: deploy
        depends_on: [build, unit-tests]
        action: { type: deploy }
```

### Canonical Pipeline Pattern

The standard build-release-deploy pipeline:

```yaml
steps:
  - name: build
    action: { type: build }
    # Creates BuildSpec + BuildRun, outputs build_id + image_digests
  - name: release
    depends_on: [build]
    action: { type: release }
    # References build_id, uses digest-based image refs from BuildArtifacts
  - name: deploy
    depends_on: [release]
    action: { type: deploy, env_name: staging }
```

When a project includes persistent DB state, the deploy pipeline must run migrations before deploy:

```yaml
steps:
  - name: build
    action: { type: build }
  - name: release
    depends_on: [build]
    action: { type: release }
  - name: migrate
    depends_on: [release]
    action:
      type: job
      service: migrate
  - name: deploy
    depends_on: [migrate]
    action: { type: deploy, env_name: sandbox }
```

Place a `migrate` service in `services` with `x-eve.role: job`, and make `deploy` depend on it.
That ensures `presence/projects/other-schema` tables are created before pods start serving traffic.

### Step Output Linking

Understand how data flows between pipeline steps:

- The `build` action creates BuildSpec and BuildRun records. On success, it emits `build_id` and `image_digests` as step outputs.
- BuildRuns produce BuildArtifacts containing per-service image digests (`sha256:...`).
- The `release` action automatically receives `build_id` from the upstream build step. It derives `image_digests_json` from BuildArtifacts, ensuring immutable digest-based image references.
- The `deploy` action references images by digest for deterministic, reproducible deployments.

This chain ensures that what was built is exactly what gets released and deployed -- no tag mutation, no ambiguity.

### Step Types

- **action**: built-in actions (`build`, `release`, `deploy`, `run`, `job`, `create-pr`, `notify`, `env-ensure`, `env-delete`)
- **script**: shell command executed by worker (`run` or `command` + `timeout_seconds`)
- **agent**: AI agent job (prompt-driven)
- **run**: shorthand for `script.run`

Script steps and `action: { type: run }` commands run durably: the
orchestrator submits the job to the worker with a short request, the worker
executes bash in the background, and completion is reported with runner events.
Long-running commands do not depend on an open HTTP request between
orchestrator and worker.

Timeout source order:
- pipeline/workflow `script:` or shorthand `run`: `script.timeout_seconds`
  persisted as `jobs.script_timeout_seconds`, then `jobs.hints.timeout_seconds`,
  then the 30-minute default.
- pipeline `action: { type: run }`: `action.timeout_seconds`, then
  `action.timeout`, then `jobs.hints.timeout_seconds`, then the 30-minute
  default.

Worker stdout/stderr are streamed into attempt logs while the process runs.
The worker stores a bounded tail for the final step output and drains excess
output after the per-stream cap (`EVE_SCRIPT_OUTPUT_CAP_BYTES`, default 10 MiB)
with an `output_truncated` warning.

Pipeline root and step definitions can declare `toolchains` with valid values
`python`, `media`, `rust`, `java`, and `kotlin`. Script, shorthand `run`,
agent, and `action: { type: run }` steps resolve `step.toolchains >
pipeline.toolchains > []`; the resolved value is stored on
`jobs.hints.toolchains` and provisioned before bash or harness launch. Other
action types cannot declare step-level toolchains, and `action.toolchains` is
rejected. If provisioning fails, the attempt fails with
`result_json.error_code = "toolchain_unavailable"`; inspect
`runtime_meta.toolchains` with `eve job diagnose <job-id>`.

Pipeline root and step definitions can also declare `env_overrides` for
`action: { type: run }` steps. The persisted action-run job receives the merged
map with step keys overriding pipeline keys; other action types ignore
`env_overrides` because they are platform operations rather than user shell.
`${secret.KEY}` values are resolved in memory before bash starts, and the job
row keeps the raw placeholder text for audit.

### Pipeline Runs

- A run creates one job per step with dependencies wired from `depends_on`.
- Run IDs: `prun_xxx`.
- Pipeline runs use the job-graph expander by default.
- `eve pipeline run --only <step>` runs a subset of steps.
- A failed job marks the run as failed and cascades cancellation to dependents.
- Cancelled jobs are terminal and unblock downstream jobs.
- Effective `env_name` resolution: `request.env_name` > `pipeline.env` > null. If
  the pipeline definition declares `env: staging` and the caller omits
  `--env`, the run and its `deploy`/`job` steps inherit `staging`. Without this
  fallback, env-bound steps fail with `Job action requires env_name`.

### CLI

```bash
eve pipeline list [project]
eve pipeline show <project> <name>
eve pipeline run <name> --ref <sha> --env <env> --inputs '{"k":"v"}' --repo-dir ./my-app
eve pipeline runs [project] --status <status>
eve pipeline show-run <pipeline> <run-id>
eve pipeline approve <run-id>
eve pipeline cancel <run-id> [--reason <text>]
eve pipeline logs <pipeline> <run-id> [--step <name>]
```

Notes:
- `--ref` must be a 40-character SHA, or a ref resolved against `--repo-dir`/cwd.

### Auto-Trigger Environment-Linked Pipelines

When an environment references a pipeline (`environments.<env>.pipeline: deploy`) and that pipeline has no explicit `trigger` block, the platform creates an implicit trigger: the pipeline fires automatically on `github.push` to the project's default branch.

Environments can override the branch with `environments.<env>.branch`. Set `auto_deploy: false` to disable implicit triggering for a specific environment.

If the pipeline already has an explicit `trigger` block, the implicit trigger is skipped (user controls triggering).

### Env Deploy as Pipeline Alias

If `environments.<env>.pipeline` is set, `eve env deploy <env> --ref <sha>` triggers the pipeline.
Use `--direct` to bypass. `--ref` must be a 40-character SHA, or a ref resolved
against `--repo-dir`/cwd.

### Promotion Pattern

1. Deploy to test (creates release):
   `eve env deploy test --ref <sha>`
2. Resolve release:
   `eve release resolve vX.Y.Z`
3. Deploy to staging/production with:
   `eve env deploy staging --ref <sha> --inputs '{"release_id":"rel_xxx"}'`

This enables build-once, deploy-many promotion workflows without rebuilding images.

## Pipeline Logs and Streaming

### Snapshot Logs

View build and execution logs (not just metadata) with timestamps and step name prefixes:

```bash
eve pipeline logs <pipeline> <run-id>                  # All step logs
eve pipeline logs <pipeline> <run-id> --step <name>    # Single step
```

### Live Streaming

Stream logs in real time via SSE:

```bash
eve pipeline logs <pipeline> <run-id> --follow                   # All steps
eve pipeline logs <pipeline> <run-id> --follow --step <name>     # Single step
```

Output format:

```
[14:23:07] [build] Cloning repository...
[14:23:09] [build] buildkit addr: tcp://buildkitd.eve.svc:1234
[14:23:15] [build] [api] #5 [dependencies 1/4] COPY pnpm-lock.yaml ...
[14:24:01] [deploy] Deployment started; waiting up to 180s
[14:24:12] [deploy] Deployment status: 1/1 ready
```

For script and `action: { type: run }` steps, stdout/stderr lines appear as
attempt log entries before the command exits. Use `--follow` when supervising a
long-running shell command; a quiet but still-running command remains active
until its configured timeout.

### Failure Hints

When a build step fails, the CLI automatically shows:
- The error type and classification
- An actionable hint (e.g., `Run 'eve build diagnose bld_xxx'`)
- The build ID for cross-referencing

### Pipeline-to-Build Linkage

Pipeline steps of type `build` create build specs and runs. On failure:
1. The pipeline step error includes the build ID.
2. The CLI prints a hint to run `eve build diagnose <build_id>`.
3. Build diagnosis shows the full buildkit output and the failed Dockerfile stage.

## Workflow Definitions

Workflows are defined in the manifest and invoked as jobs. For pack distribution, also define workflows in `eve/workflows.yaml` and reference it from `eve/pack.yaml` via `imports.workflows`. Pack workflows are merged with manifest workflows at sync time — pack definitions take precedence on name collision.

```yaml
workflows:
  nightly-audit:
    db_access: read_only
    hints:
      gates: ["remediate:proj_xxx:staging"]
    steps:
      - agent:
          prompt: "Audit error logs and summarize anomalies"
```

### Workflow Files and Prompt Files

Large workflows can be split into repo-local files. Keep one directory per
workflow and reference it from the manifest:

```text
.eve/workflows/
  acme-make-plan/
    workflow.yaml
    prompts/
      plan.md
      review.md
```

```yaml
workflows:
  acme-make-plan:
    $ref: .eve/workflows/acme-make-plan
```

If `$ref` points to a directory, `eve project sync` and
`eve manifest validate` load `workflow.yaml` or `workflow.yml` from that
directory. `$ref` may also point directly to a YAML workflow file. References
are expanded before sync; the API stores the expanded workflow and rejects
unresolved `$ref` values.

In `workflow.yaml`, use `agent.prompt_file` for long Markdown prompts:

```yaml
steps:
  - name: plan
    agent:
      name: acme-planner
      prompt_file: prompts/plan.md
```

Prompt files are resolved relative to the workflow file directory, read
verbatim, and expanded into `agent.prompt`.

### Multi-Step Workflow Expansion

Workflows compile to a full job DAG at invocation time. A multi-step workflow creates 1 root container job + N child step jobs with dependency ordering.

```yaml
workflows:
  ingestion-pipeline:
    env: local
    with_apis:
      - service: coordinator
        description: Coordinator API for orchestration
    steps:
      - name: prepare
        script:
          run: "eve job list --json"
          timeout_seconds: 60
      - name: ingest
        depends_on: [prepare]
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

**How it works:**
- Each step becomes a child job under the root workflow job.
- Workflow-level `env:` is persisted on the root job and every step job. It also
  scopes env-sensitive API and app-link resolution; workflows without `env:` keep
  the previous unscoped behavior.
- `depends_on: [step_names]` wires dependency as `blocks` relations -- the scheduler respects them.
- Each step must define exactly one execution kind: `agent`, `script`, or
  shorthand `run`. `script` and `run` steps create worker-executed script jobs
  with `script_command` and optional `script_timeout_seconds`. Execution is
  durable and streams stdout/stderr to attempt logs like pipeline script steps.
- Workflow `script:` and `run` steps receive `EVE_APP_LINK_*` env vars for
  project app-link subscriptions that declare `inject_into.jobs: true`, using the
  same short-lived token minting as direct jobs. Logs include injected key names
  only; scripts must redact token values if they print diagnostics.
- Per-step agent, harness, and toolchain resolution is supported. Script and
  shorthand `run` steps resolve `step.toolchains > workflow.toolchains > []`;
  agent steps resolve `step.toolchains > agent config toolchains >
  workflow.toolchains > []`. Workflow `action` steps remain unsupported and
  cannot declare toolchains.
- `with_apis` can be set at the workflow level (applies to all steps) or per step.
- `env_overrides` can be set at the workflow level and per step, then overridden
  at invocation time with `--env-override`.
- When a service declares `x-eve.cli`, agents also get the CLI binary on `$PATH`. See `references/app-cli.md`.

### Resource Propagation Between Steps

All workflow steps receive the invocation `resource_refs` by default, including
steps with `depends_on`. Resources are hydrated into `.eve/resources/` in each
step's workspace automatically.

Control access with `resource_refs` at workflow level or step level:

```yaml
workflows:
  create-design:
    resource_refs: inherit   # optional default; "all" is an alias
    steps:
      - name: read-sources
        agent: { name: designer }
      - name: publish
        depends_on: [read-sources]
        resource_refs: none
        agent: { name: publisher }

  scoped-review:
    resource_refs: [brief, design-system]
    steps:
      - name: review
        agent: { name: reviewer }
```

Accepted values:
- `inherit` / `all`: pass all invocation refs.
- `none`: pass no invocation refs.
- string array: pass refs whose `name`, `label`, `mount_path`, `uri`, or `metadata.name` matches a selector.
- object form: `{ mode: selected, include: [...] }`.

Step-level `resource_refs` overrides workflow-level `resource_refs`. The root
workflow job still records the full invocation refs for audit. The invoke
response includes `step_jobs[].resource_refs` with the effective mode, source
(`default`, `workflow`, or `step`), inherited count, selected count, selectors,
and missing selectors.

### Step Git Controls

Workflow steps can declare per-step `git` controls (workspace ref, branch,
commit, push behavior). Workflow-level `git` is the default; step-level `git`
overrides individual fields. String fields (`ref`, `branch`, `commit_message`,
`remote`) accept `${inputs.<name>}` and `${event.payload.<dotted.path>}`
template expressions.

```yaml
workflows:
  branch-per-pr:
    inputs:
      pr_number:
        from: event.payload.pull_request.number
    git:
      ref_policy: explicit
      remote: origin
    steps:
      - name: prepare
        agent: { name: preparer }
        git:
          branch: "review/pr-${inputs.pr_number}"
          create_branch: if_missing
          commit: manual
      - name: publish
        depends_on: [prepare]
        agent: { name: publisher }
        git:
          push: on_success
          commit_message: "chore: review notes for PR #${inputs.pr_number}"
```

Available fields (all optional): `ref`, `ref_policy` (`auto` | `env` |
`project_default` | `explicit`), `branch`, `create_branch` (`never` |
`if_missing` | `always`), `commit` (`never` | `manual` | `auto` | `required`),
`commit_message`, `push` (`never` | `on_success` | `required`), `remote`.

Workflow retry replays already-materialized step git controls verbatim, so
retried steps land on the same branch and ref the original step used.

### Workflow Env Overrides

Workflow agent, script, and shorthand `run` steps can receive secret-backed
environment overrides without hand-building a job DAG. The effective step-job
`env_overrides` object is merged by key with this precedence: invocation request
> step YAML > workflow YAML.

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

```bash
eve workflow run research --env-override WEB_SEARCH_API_KEY='${secret.WEB_SEARCH_API_KEY}'
eve workflow invoke research --env-override MODE=diagnostic
eve harness validate --project <project> --workflow research --env-override MODE=diagnostic
```

The schema is the same as direct job `env_overrides`: keys must be
`UPPER_SNAKE_CASE`, reserved Eve runtime variables cannot be overridden, values
may contain `${secret.KEY}` placeholders only, and unsupported `${env.X}` style
expressions are rejected. `eve manifest validate --validate-secrets` and
`eve project sync --validate-secrets` include workflow env override secret refs
in missing-secret reports.

At execution time, resolved values are injected into the agent harness or bash
environment. Missing secret placeholders fail the step before bash/harness
execution with `missing_secret_override`; logs preserve the missing key names,
while `eve job show <job> --json` still returns the unresolved placeholders.

### Workflow Token Scope (Scoped Job Tokens)

Workflow and step `scope` blocks narrow a step job's API authority and org
filesystem mount, so a step granted `cloud_fs:read` can only read the specific
mounts/prefixes the scope allows. Supported axes match access binding scope
JSON: `orgfs`, `orgdocs`, `envdb`, and `cloud_fs`.

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

**Propagation chain** (parallels `env_overrides`): workflow `scope` → step
`scope` → invocation `scope` (API body or `WorkflowInvokeRequest.scope`). All
three are intersected per executable step job and persisted as
`jobs.token_scope`; empty intersections fail closed. The orchestrator uses the
same scope to mint the job token and to materialize the step's `.org` mount.

Request-supplied scope requires `jobs:harness_override`. There is no
`eve workflow run --scope-*` or `eve job create --scope-*` flag yet — use the
manifest `scope` block or the workflow invoke API body. `eve manifest validate`
rejects malformed `scope` payloads at sync time.

#### Scope narrows; permission grants

`scope` is a *narrowing* mechanism, not a granting one. The step's job token
needs the underlying resource permission for the scope to be exercisable:

| Axis declared in `scope` | Permission the step's agent must declare |
|---|---|
| `orgfs.allow_prefixes` | `orgfs:read` (and `orgfs:write` if the step writes) |
| `orgfs.read_only_prefixes` | `orgfs:read` |
| `orgdocs.allow_prefixes` | `orgdocs:read` (and `orgdocs:write` if the step writes) |
| `envdb.{schemas,tables}` | `envdb:read` / `envdb:write` |
| `cloud_fs.allow_mount_ids` | `cloud_fs:read` (and `cloud_fs:write` if the step writes) |

These permissions are **not** in `DEFAULT_AGENT_PERMISSIONS` — declare them on
the step's agent in `agents.yaml` under `access.permissions` (see
`references/agents-teams.md` § Agent Permissions). A workflow that declares
`scope.orgfs.allow_prefixes` without a matching `orgfs:read` on the agent
produces a correctly-scoped token that has no permission to act, and orgfs API
calls fail with `Missing required permission: orgfs:read`.

Example pairing:

```yaml
# agents.yaml
agents:
  reviewer:
    skill: review
    access:
      permissions: [orgfs:read]   # required to exercise the workflow scope

# workflows section
workflows:
  scoped-review:
    scope:
      orgfs:
        allow_prefixes: [/groups/projects/proj-a/**]
    steps:
      - name: review
        agent: { name: reviewer }
```

See `references/jobs.md` for the per-job `token_scope` view and
`references/manifest.md` for the manifest field shape.

#### Per-step `permissions:` for non-agent steps

Pipeline `script:` and `action: { type: run }` steps, plus workflow `script:`,
`run:`, and `agent:` steps, accept a `permissions: [...]` list with the same ergonomics as
`scope:`. The expander resolves it (step-level wins over
pipeline/workflow-level), persists it on `jobs.token_permissions`, and
the script/action-run executors mint `EVE_JOB_TOKEN` with that exact list
plus `~/.eve/credentials.json` so the Eve CLI authenticates inside the
step. When the step does not declare `permissions:`, the executor falls
back to its default (broad for `script:`, narrow read-only for
`action: { type: run }` — see `references/secrets-auth.md`).

```yaml
pipelines:
  scoped-jobs-only:
    permissions: [jobs:read]      # pipeline-level default
    steps:
      - name: list-jobs
        script:
          run: eve job list --project $EVE_PROJECT_ID --json

      - name: post-thread
        permissions: [jobs:read, threads:write]   # narrow override
        action:
          type: run
          command: |
            eve thread post coord:job:$EVE_PARENT_JOB_ID --message "step done"
```

The expander rejects any permission the invoking actor does not hold
(`assertActorCanGrantPermissions`) — workflow authors can narrow but
never escalate.

### Prior Step Result Injection

When a workflow step has `depends_on`, the orchestrator injects the completed dependency's `result_text` into the step's job description at dispatch time. This means downstream agents receive upstream outputs without making API calls.

- Injected as a `## Prior Step Results` section in the job description
- Each prior step's result appears under a `### Step: <name> (<job_id>)` heading
- Capped at 50KB per step to avoid prompt bloat
- If a step has multiple dependencies, all completed results are included

### Per-Step `with_apis` Overrides

Individual workflow steps can override the workflow-level `with_apis` declaration:

```yaml
workflows:
  pipeline:
    with_apis:
      - service: coordinator
        description: Coordinator API for orchestration
    steps:
      - name: ingest
        agent: { name: ingestion }
        # Inherits with_apis from workflow level
      - name: transform
        with_apis:
          - service: coordinator
            description: Coordinator API for orchestration
          - service: analytics
            description: Analytics API for data processing
        agent: { name: transformer }
        # Uses its own with_apis, overriding workflow level
```

Steps without their own `with_apis` inherit from the workflow level.

### Non-Chat Workflow Notifications

Workflow steps that need to announce completion to Slack should use
`eve notifications send`; do not read integrations or handle raw Slack bot
tokens in the job:

```bash
eve notifications send \
  --project <project_id_or_slug> \
  --channel eve-horizon-notifications \
  --message "Published PR: https://github.com/org/repo/pull/123"
```

The command calls `POST /projects/:project_id/notifications/send` and requires
the step's job token to include `notifications:send`. Grant that permission to
the publishing agent in `agents.yaml`:

```yaml
agents:
  publisher:
    access:
      permissions:
        - notifications:send
```

**Validation rules** (enforced by `eve manifest validate` and `eve project sync`):
- Duplicate step names → error.
- Cyclic dependencies → error (reports the cycle path).
- Invalid `depends_on` references (non-existent step name) → error.
- Trigger with no recognized type key → warning.
- Invalid GitHub event type (not `push` or `pull_request`) → warning.
- Unknown system event type → warning (advisory, custom events allowed).
- Cron trigger with missing schedule → warning.

Trigger validation runs during `eve project sync` (not just `eve manifest validate`), so malformed triggers are surfaced immediately.

### Conditional Steps

Steps can declare a `condition` that's evaluated when dependencies complete. If false, the step is skipped without running an agent.

```yaml
workflows:
  smart-edit:
    steps:
      - name: triage
        agent: { name: fast-triage }
      - name: deep-analysis
        depends_on: [triage]
        condition: "triage.status == 'complex'"
        agent: { name: deep-analyzer }
```

**Condition format:** `step_name.status == 'value'` or `step_name.status != 'value'`.
Evaluates against `result_json.eve.status` of the referenced step.

**Rules:**
- Referenced step must exist in the workflow and be in `depends_on`
- Skipped steps are marked `done` with `close_reason: 'condition_not_met'`
- Downstream steps that depend on a skipped step still become eligible
- Condition validation runs at sync time (format, reference, dependency checks)

**Use case — triage escalation:** A fast agent (low reasoning) classifies task complexity. An expert agent (high reasoning) only runs for complex tasks. Simple tasks are handled entirely by the triage step.

### Step-Level Harness and harness_options

Workflow steps can override harness selection and pass per-step harness tuning
without referencing a named profile. Useful for inline prompts that need a
specific model or `reasoning_effort` for one step only.

```yaml
workflows:
  triage-then-fix:
    steps:
      - name: triage
        harness: claude
        harness_options:
          model: claude-haiku-4
          reasoning_effort: minimal
        agent:
          name: triager
      - name: fix
        depends_on: [triage]
        harness: claude
        harness_options:
          model: claude-opus-4
          reasoning_effort: high
        agent:
          name: fixer
```

Step-level `harness` and `harness_options` take precedence over agent-resolved
values, matching the override pattern used by `toolchains`. `harness_options`
accepts arbitrary keys (`model`, `reasoning_effort`, `temperature`, …) that the
selected harness understands. For dynamic per-invocation selection (templated
from `${inputs.*}` or event payload), see the next section.

### Per-Step Harness Overrides (Template Expressions)

Workflow steps can choose their brain per-invocation using `${inputs.<key>}` and
`${event.payload.<path>}` template expressions. Useful when the same workflow
must run with a different model/harness depending on who triggered it.

```yaml
workflows:
  classify:
    # Declare workflow inputs. `from:` pulls from the triggering event's payload;
    # `default:` is used when the payload field is absent.
    inputs:
      brain:
        from: event.payload.meta.brain
        default: planner
    steps:
      - name: classify
        agent:
          name: classifier
        # Templated reference to a named profile in x-eve.agents.profiles.
        harness_profile: "${inputs.brain}"

  per-brand:
    inputs:
      brand:
        from: event.payload.meta.brand
    steps:
      - name: run
        agent:
          name: worker
        # Inline bundle — per-field templates. Unknown-ref fields fall back to
        # the agent's default profile at dispatch with a warning log.
        harness_profile_override:
          harness: zai
          model: "glm-4.6-${inputs.brand}"
```

**Grammar (intentionally tiny):**
- `${inputs.<key>}` — a single declared input or a caller-supplied ad-hoc input.
- `${event.payload.<dotted.path>}` — walks the event's raw payload.
- No operators, no function calls, no array indexing.

**Precedence at dispatch:** `harness_profile_override` (workflow_template) beats
`harness_profile` (string_ref) beats the agent's declared `harness_profile`
(agent_default). The `harness_profile_source` enum on `jobs` and `job_attempts`
records which branch applied.

**Validation:**
- `eve manifest validate` / `eve project sync` reject malformed templates and
  `${inputs.<undeclared>}` references at sync time.
- Event-payload refs are accepted structurally — the payload shape is only known
  at runtime, so missing fields cause a fallback (with a warning log), not an
  error.

**Response format** includes `step_jobs`:

```json
{
  "job_id": "proj-abc12345",
  "status": "active",
  "step_jobs": [
    {
      "job_id": "proj-abc12345.1",
      "step_name": "ingest",
      "resource_refs": {"mode": "inherit", "source": "default", "count": 2, "inherited_count": 2}
    },
    {
      "job_id": "proj-abc12345.2",
      "step_name": "extract",
      "depends_on": ["ingest"],
      "resource_refs": {"mode": "inherit", "source": "default", "count": 2, "inherited_count": 2}
    },
    {
      "job_id": "proj-abc12345.3",
      "step_name": "review",
      "depends_on": ["extract"],
      "resource_refs": {"mode": "none", "source": "step", "count": 0, "inherited_count": 2}
    }
  ]
}
```

**Job tree view** (`eve job tree`):

```
[*] proj-abc12345 [Workflow] ingestion-pipeline
|- [-] proj-abc12345.1 [ingestion-pipeline] ingest
|- [-] proj-abc12345.2 [ingestion-pipeline] extract
|- [-] proj-abc12345.3 [ingestion-pipeline] review
```

### Workflow Hints

Workflow definitions may include a `hints` block. These hints are merged into the job at invocation time (API, CLI, or event triggers). Use hints for:

- **Remediation gates**: control which environments a workflow can remediate. Pattern: one gate per environment.
  ```yaml
  hints:
    gates: ["remediate:proj_abc123:staging"]
  ```
- **Timeouts**: set execution time limits for the workflow job.
- **Harness preferences**: specify model/harness settings that override project defaults for this workflow.

### Invocation

- Invoking a workflow creates a **job** with workflow metadata in `hints`.
- `wait=true` returns `result_json` with a 60s timeout.

### Workflow CLI

```bash
eve workflow list [project]
eve workflow show <project> <name>
eve workflow run <project> <name> --input '{"k":"v"}' --env-override KEY=VALUE
eve workflow invoke <project> <name> --input '{"k":"v"}' --env-override KEY=VALUE
eve workflow retry <root-job-id> --failed
eve workflow retry <root-job-id> --from <step-name>
eve workflow logs <job-id>
eve notifications send --project <project> --channel <name-or-id> --message <text>
```

Workflow retry is a recovery path for terminal multi-step workflow roots. It
clones already-materialized current step jobs, so original input values, git
controls, resource refs, harness settings, and API hints are preserved.
`--failed` retries failed/upstream-failed current steps; `--from <step-name>`
retries that step and downstream dependents. Superseded jobs remain in the tree
with retry metadata, while replacement jobs receive rewired dependency edges so
prior-step result injection reads from the correct predecessor.

## Triggers

Both pipelines and workflows can include a `trigger` block. The orchestrator matches incoming events and creates pipeline runs or workflow jobs.

### Generic Event Triggers

Workflows and pipelines can trigger on any event source and type:

```yaml
trigger:
  event:
    source: app
    type: document.uploaded
```

- `source` (required): matches `event.source` (e.g., `app`, `app_link`, `runner`, `chat`, `github`)
- `type` (optional): matches `event.type` exactly; omit to match all events from that source

When a workflow is triggered by an event, the event payload is forwarded as workflow input. The input JSON is included in child job descriptions so step agents can see what triggered them.

### App Trigger (Shorthand)

For app-sourced events, use the `app` trigger as a shorthand:

```yaml
trigger:
  app:
    event: question.answered
```

This is equivalent to `event: { source: app, type: question.answered }`. Both formats work; use whichever reads better in context.

### App-Link Trigger (Cross-Project Events)

For events delivered from a producer project through `x-eve.app_links`, use the
`app_link` trigger:

```yaml
trigger:
  app_link:
    alias: observation
    type: app.observation.created
```

This matches consumer-side events with `source=app_link`, filters by the
consumer-local subscription alias, and optionally filters by event type. See
`references/events.md` and `references/manifest.md` for the app-link contract.

### GitHub Push Triggers

```yaml
trigger:
  github:
    event: push
    branch: main
```

Branch patterns support wildcards (e.g., `release/*`, `*-prod`).

### GitHub Pull Request Triggers

```yaml
trigger:
  github:
    event: pull_request
    action: [opened, synchronize]
    base_branch: main
```

Supported PR actions: `opened`, `synchronize`, `reopened`, `closed`.
Base branch filtering supports wildcard patterns.

### PR Preview Deployment Example

Deploy a preview environment on PR open/update, clean up on close:

```yaml
pipelines:
  pr-preview:
    trigger:
      github:
        event: pull_request
        action: [opened, synchronize]
        base_branch: main
    steps:
      - name: create-preview-env
        action:
          type: env-ensure
          with:
            env_name: ${{ env.pr_${{ github.pull_request.number }} }}
            kind: preview
      - name: deploy
        depends_on: [create-preview-env]
        action:
          type: deploy
          with:
            env_name: ${{ env.pr_${{ github.pull_request.number }} }}

  pr-cleanup:
    trigger:
      github:
        event: pull_request
        action: closed
        base_branch: main
    steps:
      - name: cleanup-env
        action:
          type: env-delete
          with:
            env_name: ${{ env.pr_${{ github.pull_request.number }} }}
```

### Trigger Observability

Every event records why each candidate trigger did or did not fire. Use this to
diagnose "the event arrived but nothing ran":

```bash
eve event show <event-id>
# Triggers:    matched 1 of 3 evaluated
#   ✓ workflow:ingestion-pipeline
#   ✗ workflow:alignment-check  (type_mismatch)
#   ✗ pipeline:deploy           (branch_mismatch)
```

Events carry `trigger_match_count` and `triggers_evaluated[{type, name, matched,
reason}]`. Common reasons: `source_mismatch`, `type_mismatch`,
`branch_mismatch`, `action_mismatch`, `no_trigger`, `manual_trigger`. See
`references/events.md` for the full schema.

Trigger validation also runs during `eve project sync` (not just
`eve manifest validate`), so unrecognized trigger types, invalid GitHub events,
unknown system events, and missing cron schedules surface as warnings the
moment they're synced.

## API Endpoints

```
GET  /projects/{project_id}/pipelines
GET  /projects/{project_id}/pipelines/{name}

# Pipeline runs
POST /projects/{project_id}/pipelines/{name}/run
GET  /projects/{project_id}/pipelines/{name}/runs
GET  /projects/{project_id}/pipelines/{name}/runs/{run_id}
POST /pipeline-runs/{run_id}/approve
POST /pipeline-runs/{run_id}/cancel
GET  /pipeline-runs/{run_id}/stream
GET  /pipeline-runs/{run_id}/steps/{name}/stream

# Workflows
GET  /projects/{project_id}/workflows
GET  /projects/{project_id}/workflows/{name}
POST /projects/{project_id}/workflows/{name}/invoke?wait=true|false
POST /projects/{project_id}/notifications/send
```
