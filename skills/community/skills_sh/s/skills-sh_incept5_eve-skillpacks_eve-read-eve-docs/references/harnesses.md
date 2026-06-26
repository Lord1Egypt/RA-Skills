# Harness Execution Reference

## Use When
- You need to choose or compare available harnesses and profiles.
- You need workspace, permission, or sandbox guidance for job execution.
- You need to trace how Eve invokes harness binaries during execution.

## Load Next
- `references/jobs.md` for execution lifecycle and attempt scheduling.
- `references/cli.md` for harness-specific profile commands.
- `references/secrets-auth.md` for credentials and secret injection.

## Ask If Missing
- Confirm target harness and repo path for execution.
- Confirm permission policy and sandbox mode requirements (`inline` vs `runner`).
- Confirm available secrets/toolchain constraints for command execution.

Eve executes AI work through **harnesses** -- thin adapters that wrap AI coding CLIs
(Claude Code, Gemini CLI, Codex, etc.) behind a uniform invocation contract. All model
access is BYOK: harnesses and apps bring their own API keys via secrets and call
providers directly. Eve never proxies inference traffic. This reference covers the full
lifecycle: invocation, workspace setup, authentication, per-harness configuration,
policy controls, and introspection.

---

## Invocation Flow

Both the worker and agent-runtime execute jobs through a shared invoke module
(`packages/shared/src/invoke/`). Agent jobs route to the agent-runtime; builds,
deploys, pipelines, and scripts route to the worker. The shared module provides
full feature parity across both runtimes.

Every job attempt follows a two-stage pipeline:

```
HarnessInvocation
  { attemptId, jobId, projectId, text, workspacePath, repoUrl, harness, toolchains }
        |
        v
InvokeService.execute()  (worker or agent-runtime, both using shared invoke module)
  1. prepareWorkspace()          -- mkdir + git clone/copy
  2. writeCarryoverContext()     -- memory, docs, parent attachments
  3. stageAttachments()          -- download chat files to workspace
  4. writeSecurityClaudeMd()     -- security policy to CLAUDE_CONFIG_DIR
  5. resolveWorkerAdapter()      -- look up WorkerHarnessAdapter by name
  6. adapter.buildOptions(ctx)   -- resolve auth, config dirs, env
  7. BudgetEnforcer.start()      -- enforce max_tokens/max_cost via llm.call tracking
  8. executeEveAgentCli()        -- spawn eve-agent-cli, stream JSON to execution_logs
        |
        v
eve-agent-cli
  1. resolveCliAdapter(harness)  -- look up CliHarnessAdapter by name
  2. adapter.buildCommand(ctx)   -- binary + args + env; map permission policy to flags
  3. spawn(binary, args, {cwd: repoPath, env})
     -- run the harness CLI, normalize output to JSON events
```

The worker never calls harness binaries directly. It always goes through `eve-agent-cli`,
which owns argument construction, permission mapping, and output normalization.

### Shared Invoke Module

Agent-execution features live in `packages/shared/src/invoke/` and are imported by
both worker and agent-runtime. Key modules:

| Module                   | Purpose                                              |
|--------------------------|------------------------------------------------------|
| `budget-enforcement.ts`  | BudgetEnforcer: max_tokens/max_cost, llm.call tracking, kill |
| `carryover-context.ts`   | Write memory, docs, parent attachments to workspace  |
| `security-policy.ts`     | Build and write security CLAUDE.md                   |
| `result-extraction.ts`   | Extract result text, JSON, token usage, error messages |
| `attachment-staging.ts`  | Stage chat file attachments into workspace           |
| `coordination.ts`        | Write coordination inbox and thread context           |
| `workspace-hooks.ts`     | Run acquire/release hooks                            |
| `workspace-secrets.ts`   | Resolve, materialize, and clean up secrets           |
| `eve-message-relay.ts`   | EveMessageRelay: deliver to chat + coordination thread |
| `resource-hydration.ts`  | Hydrate resources with lifecycle events              |
| `harness-lifecycle.ts`   | Log harness start/end events                         |
| `toolchain-cache.ts`     | Provision declared toolchains into runtime PATH/env   |
| `codex-auth.ts`          | Write-back refreshed Codex auth tokens               |

New agent-execution features go in the shared module, never in a single runtime.

---

## Harness Naming and Aliases

| Harness    | Binary    | Aliases  | Notes                                               |
|------------|-----------|----------|-----------------------------------------------------|
| `mclaude`  | `mclaude` | --       | cc-mirror Claude variant                             |
| `claude`   | `claude`  | --       | Official @anthropic-ai/claude-code                   |
| `zai`      | `zai`     | --       | cc-mirror Z.ai variant                               |
| `gemini`   | `gemini`  | --       | @google/gemini-cli                                   |
| `code`     | `code`    | `coder`  | @just-every/code. Use `coder` on host to avoid VS Code clash |
| `codex`    | `codex`   | --       | @openai/codex                                        |

Do not parse `harness:variant` syntax. Use `harness_options.variant` instead.

---

## Workspace Directory Structure

```
$WORKSPACE_ROOT/                       # e.g. /opt/eve/workspaces
  {attemptId}/                         # unique per attempt
    repo/                              # cloned/copied repository
      AGENTS.md                        # project memory for agents
      CLAUDE.md                        # Claude-specific instructions
      .agents/skills/                   # installed skills (gitignored)
      .agents/harnesses/<harness>/      # per-harness config (optional)
      .claude/skills/                  # symlink or overrides (gitignored)
```

| Variable        | Value                              | Description                        |
|-----------------|------------------------------------|------------------------------------|
| `workspacePath` | `$WORKSPACE_ROOT/{attemptId}`      | Root workspace for this attempt    |
| `repoPath`      | `$workspacePath/repo`              | Cloned repository                  |
| `cwd` (harness) | `$repoPath`                        | Working directory for execution    |

The harness runs with `cwd = repoPath` so it sees AGENTS.md, CLAUDE.md, and project files.

### Environment Contract

- `EVE_WORKSPACE_ROOT` -- root for all workspaces (e.g. `/opt/eve/workspaces`)
- `EVE_CACHE_ROOT` -- shared cache for package managers and build artifacts
- Processes run as UID 1000 (non-root); workspace dirs are writable
- Cache directories are shared across attempts for efficiency
- Credentials and config injected via secrets/config maps

---

## Repository Preparation

The worker requires `repoUrl` for every job. Preparation depends on URL type:

**Remote URL** (https://, git://):
- If `job.git` is set, use **GitWorkspace**: shallow clone of the resolved ref,
  fetch-based checkout, branch creation if requested.
- Otherwise, legacy shallow clone: `git clone --depth 1 --branch <branch> <url>`.

**Local URL** (file://):
- Copy directory with `fs.cp`. Branch is ignored. Dev/test only.
- Not supported in k8s runtime or push-required workflows.

### Git Controls

When a job has `git` configuration, the worker:

1. Resolve the ref per `git.ref_policy` (env release -> manifest defaults -> project branch).
2. Create or check out a branch per `git.branch` and `git.create_branch`.
3. Apply commit and push policies **after** execution:
   - `commit=auto` -- `git add -A` and commit any changes, even on failed attempts.
   - `commit=required` -- fail on success if the working tree is clean.
   - `push=on_success` or `push=required` -- push only when the worker created commits.
4. Store resolved metadata on the attempt (`job_attempts.git_json`).

---

## Worker Image and Toolchains

The default worker image is `base` (~800MB), which includes Node.js, git, gh, kubectl,
kaniko, buildctl, and all harness binaries (claude-code, codex, gemini-cli, cc-mirror,
code, bd, skills). Most agent jobs need nothing beyond this.

### Toolchain-on-Demand

Toolchains (Python, Rust, Java, Kotlin, ffmpeg/whisper) are delivered as init containers
rather than baked into the worker image. This replaces the previous `full` image (2.6GB)
approach.

Available toolchains:

| Toolchain | Contents                                     | Approx Size |
|-----------|----------------------------------------------|-------------|
| `python`  | Python 3, pip, venv, uv                      | ~100MB      |
| `media`   | ffmpeg, whisper-cli, ggml-small.en model     | ~300MB      |
| `rust`    | rustup, stable toolchain, rustfmt, clippy    | ~400MB      |
| `java`    | Temurin JDK 21                               | ~300MB      |
| `kotlin`  | kotlinc 2.0.21 + bundled JDK 21             | ~350MB      |

Init containers copy toolchain payloads from small single-purpose images into
`/opt/eve/toolchains/{name}/`. The entrypoint extends `PATH` from `EVE_TOOLCHAIN_PATHS`
and sources per-toolchain `env.sh` files for variables like `JAVA_HOME` and `CARGO_HOME`.

### Declaring Toolchains

Agents declare required toolchains in their config:

```yaml
# eve/agents.yaml
agents:
  data-analyst:
    name: Data Analyst
    skill: analyze-data
    harness_profile: claude-sonnet
    toolchains: [python]

  doc-processor:
    name: Document Processor
    skill: process-documents
    harness_profile: claude-sonnet
    toolchains: [media]
```

Workflows can override the agent default:

```yaml
# eve/workflows.yaml
workflows:
  process-document:
    trigger:
      system.event: doc.ingest
    steps:
      - name: process
        agent: doc-processor
        toolchains: [media, python]    # override agent default
```

Toolchain precedence: workflow step `toolchains` overrides agent `toolchains` overrides
empty (base-only). The `full` image remains available via `EVE_WORKER_VARIANT=full` for
backwards compatibility.

### Inline Runtime Provisioning

Worker script/action-run jobs and the default inline agent-runtime path provision
declared toolchains on demand before launching bash or the harness. Provisioning
uses `EVE_TOOLCHAIN_ROOT`, `EVE_TOOLCHAIN_IMAGE_PREFIX`,
`EVE_TOOLCHAIN_IMAGE_TAG`, and local `EVE_TOOLCHAIN_REGISTRY_INSECURE=true`
when reading the in-cluster registry. The returned toolchain `bin` paths are
prepended to `PATH`, and each `env.sh` overlay is injected before user
`env_overrides` are applied.

If provisioning fails, the attempt fails before harness spawn with
`result_json.error_code = "toolchain_unavailable"`. Inspect
`eve job diagnose <job-id>` for `runtime_meta.toolchains` and toolchain
provisioning log lines.

### Runner Pod Injection

For K8s runner pods, the orchestrator generates init containers from the `toolchains`
array. Each init container copies its payload into a shared `emptyDir` volume mounted
at `/opt/eve/toolchains/`. On nodes with a persistent toolchain cache (node-local PVC),
init containers skip the copy if the cached version matches. Runner pods also report
the same `runtime_meta.toolchains` block, with `source: init_container`.

---

## Disk Management

Operator knobs (env vars):

| Variable                    | Purpose                                    |
|-----------------------------|--------------------------------------------|
| `EVE_WORKSPACE_MAX_GB`      | Total workspace budget per instance        |
| `EVE_WORKSPACE_MIN_FREE_GB` | Hard floor; refuse new claims if below     |
| `EVE_WORKSPACE_TTL_HOURS`   | Idle TTL for job worktrees                 |
| `EVE_SESSION_TTL_HOURS`     | Idle TTL for session workspaces            |
| `EVE_MIRROR_MAX_GB`         | Cap for bare mirrors                       |

Policies: LRU eviction when over budget. TTL cleanup for idle worktrees. Mirror
maintenance via `git fetch --prune` and periodic `git gc --prune=now`. Fail-fast on
low disk (emit system event; do not start new attempts).

K8s: per-attempt PVCs are deleted after completion. Session-scoped PVCs use TTL cleanup.

---

## Authentication

### Claude-Based Harnesses (mclaude, claude)

Claude auth is selected by the shared runtime selector:

1. Scope specificity wins: `project > org > user > system`.
2. Within the same scope, `ANTHROPIC_API_KEY` wins over `CLAUDE_CODE_OAUTH_TOKEN`.
3. Across scopes, a more-specific setup-token beats a broader API key.

Setup-tokens (`sk-ant-oat01-*`) are materialized to:
`$EVE_JOB_USER_HOME/.claude-runtime/<claude|mclaude>/<variant-or-default>/.credentials.json`.
This path is outside `repoPath`; credentials are never written under
`.agent/harnesses/*`. After `env_overrides`, the runtime scrubs conflicting Claude
auth env vars. OAuth tokens remain env-based and emit a warning.

Diagnostics:
- `claude_auth_selected`: redacted key/scope/token-class/materialization info.
- `claude_auth_failed`: emitted once on `apiKeySource: none` or 401/invalid credentials.

Verify managed auth with:

```bash
eve auth verify --harness claude --project proj_xxx --json
```

### Zai Harness

Requires `Z_AI_API_KEY`. The worker maps this to `ANTHROPIC_API_KEY` at spawn time.
The Docker image strips `ANTHROPIC_API_KEY` from zai's settings.json so the runtime
value takes precedence.

`ANTHROPIC_BASE_URL` precedence for zai adapter:
1. `ANTHROPIC_BASE_URL`
2. `Z_AI_BASE_URL` (fallback)

### Gemini Harness

Uses `GEMINI_API_KEY` or `GOOGLE_API_KEY`. No special credential setup.

### Code / Codex Harnesses

Docker entrypoint writes OpenAI OAuth to `~/.code/auth.json` and `~/.codex/auth.json`.
Format: `{ "tokens": { "access_token": "...", "refresh_token": "...", "id_token": "...", "account_id": "..." } }`

Eve automatically writes back refreshed Code/Codex tokens after each invocation. If the
`auth.json` changed during the session, the new value is patched to the originating secret
scope (user/org/project). Write-back failures are non-fatal (logged as warning).

To initially register tokens, re-auth with `codex auth` / `code auth`, then run `eve auth sync`.

---

## Token Lifecycle Management

### Claude Tokens

Claude setup-tokens (`sk-ant-oat01-*`) are long-lived and preferred for managed
jobs. Other `sk-ant-*` tokens are treated as short-lived OAuth tokens.

Token types detected by `eve auth creds` and `eve auth sync`:

| Token prefix | Type | Lifetime |
|---|---|---|
| `sk-ant-oat01-` | `setup-token` | Long-lived (preferred) |
| Other `sk-ant-*` | `oauth` | ~15h (short-lived) |

`eve auth sync` warns when syncing a short-lived OAuth token (any Claude token not starting
with `sk-ant-oat01-`), recommending a setup-token for long-running jobs.

### Codex/Code OAuth Tokens

Codex and Code CLI store OAuth tokens in `auth.json` under `~/.codex/` or `~/.code/`. The
CLI may refresh these tokens automatically during a session.

**Write-back flow:**

1. Before invocation: worker captures the base64-encoded `auth.json` and its originating secret scope.
2. After invocation: worker reads `auth.json` from disk (picks freshest across `~/.code` and `~/.codex`).
3. If the base64 differs (token was refreshed), the new value is written back to the originating secret via `PATCH /internal/secrets/:scope_type/:scope_id/CODEX_AUTH_JSON_B64`.
4. Write-back failures are non-fatal (logged as `warn`).

This keeps tokens fresh across jobs without manual re-sync.

---

## Harness Config Root

Per-harness configuration lives in a single root with subfolders:

```
.agents/harnesses/
  <harness>/
    config.toml|json|yaml
    variants/
      <variant>/
        config.toml|json|yaml
```

Resolution: `EVE_HARNESS_CONFIG_ROOT` (if set) -> `<repo>/.agents/harnesses/<harness>`.
If a `variants/<variant>` directory exists, it overlays the base config.

---

## Adding a New BYOK Model

1. **Rate card** — `packages/shared/src/pricing/default-rate-card.ts`:
   add entry under `llm.byok.<provider>.<model-id>`, update effective date.
2. **Model examples** — `packages/shared/src/harnesses/capabilities.ts`:
   update `model_examples` for the relevant harness (recommended default first).
3. **Env example** — `.env.example`: update the suggested model if it's the new default.
4. **Model normalization** — `packages/shared/src/pricing/model-normalization.ts`:
   add rules if provider uses non-standard suffixes.
5. **Harness CLI normalization** — `packages/shared/src/harnesses/model-aliases.ts`:
   add aliases when a model has multiple user-facing forms (e.g. `opus4.7`,
   `opus-4-7`, `claude-opus-4-7`) that should all resolve to the harness's
   own short alias. Per-job + chat-hint model overrides flow through the
   normalizer before reaching the harness CLI.

### Currently Registered Models

Default rate card (`DEFAULT_RATE_CARD_EFFECTIVE_AT = 2026-04-29`):

| Provider  | Models                                                                                              |
|-----------|-----------------------------------------------------------------------------------------------------|
| anthropic | `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-opus-4-5`, `claude-sonnet-4-5`, `claude-haiku-4-5`, `claude-sonnet-4` |
| openai    | `gpt-5.5`, `o3`                                                                                     |
| zai       | `glm-5`, `glm-5-code`                                                                               |

`claude-opus-4-7` priced at $5/$25 in/out per million tokens, $0.50 cache_read,
$6.25 cache_write (matches 4.6). `gpt-5.5` priced at $5/$30 in/out, $0.50
cache_read, $30 reasoning.

Pinned harness binary versions (worker + agent-runtime Dockerfiles): cc-mirror
2.1.0, claude-code 2.1.123, codex 0.125.0, gemini-cli 0.40.0,
just-every/code 0.6.96, pi 0.70.6, skills 1.5.3.

---

## Per-Harness CLI Arguments

### mclaude / claude

```
mclaude --print --verbose --output-format stream-json \
  --model sonnet --permission-mode default "<prompt>"
```

- Config dir: `<config root>/mclaude` or `$CLAUDE_CONFIG_DIR`
- Model: `$CLAUDE_MODEL` or `sonnet` (default fallback changed from `opus` to `sonnet`)
- Skills: mclaude installs from `skills.txt` into `.agents/skills/` at runtime
- Model aliases: `opus4.7`, `opus-4-7`, `opus-4.7`, `claude-opus-4-7` (and the
  `anthropic/` provider-prefixed variants) all normalize to Claude Code's `opus`
  alias via `normalizeClaudeCodeModelAlias`. Per-job and chat-hint model
  overrides feed through this normalizer before reaching the harness CLI.

### zai

```
zai --print --verbose --output-format stream-json \
  --model <model> --permission-mode default "<prompt>"
```

- Config dir: `<config root>/zai` or `$CLAUDE_CONFIG_DIR`
- Model: `$ZAI_MODEL` or `$CLAUDE_MODEL`

### gemini

```
gemini --output-format stream-json \
  --model <model> --approval-mode default "<prompt>"
```

Uses `--approval-mode` instead of `--permission-mode`.

### code / coder / codex

```
code --ask-for-approval on-request --model <model> \
  --profile <variant> exec --json --skip-git-repo-check "<prompt>"
```

- Config dir: `<config root>/code` (or `/codex`) or `$CODEX_HOME`
- Auth: `auth.json` in config dir (from `CODEX_AUTH_JSON_B64` or `CODEX_OAUTH_*` vars)
- Reasoning: `code` uses `--reasoning <effort>`. `codex` uses
  `-c model_reasoning_effort="<effort>"` (config override) instead, because the
  codex CLI no longer accepts `--reasoning` as a top-level flag. The
  `eve-agent-cli` adapter switches automatically based on `ctx.harness`.

---

## Permission Policies

| Policy      | mclaude/claude/zai                    | gemini                     | code/codex                      |
|-------------|---------------------------------------|----------------------------|---------------------------------|
| `default`   | `--permission-mode default`           | `--approval-mode default`  | `--ask-for-approval on-request` |
| `auto_edit` | `--permission-mode acceptEdits`       | `--approval-mode auto_edit`| `--ask-for-approval on-failure` |
| `never`     | `--permission-mode dontAsk`           | (fallback to default)      | `--ask-for-approval never`      |
| `yolo`      | `--dangerously-skip-permissions`      | `--yolo`                   | `--ask-for-approval never`      |

Sandbox flags applied automatically by `eve-agent-cli`:
- Claude/mclaude/zai: `--add-dir <workspace>`
- Code/Codex: `--sandbox workspace-write -C <workspace>`
- Gemini: `--sandbox`

---

## Reasoning Effort

Jobs pass `harness_options.reasoning_effort` (`low`, `medium`, `high`, `x-high`).

| Harness family     | Mechanism         | Notes                                  |
|--------------------|-------------------|----------------------------------------|
| mclaude/claude/zai | thinking tokens   | Maps effort level to token budget      |
| code/codex         | `--reasoning`     | Passes effort level as CLI flag        |
| gemini             | passthrough       | Effort level passed directly           |

---

## Project Harness Profiles

Define named profiles in the manifest under `x-eve.agents`:

```yaml
x-eve:
  agents:
    version: 1
    availability:
      drop_unavailable: true       # drop entries for unavailable harnesses
    profiles:
      primary-coder:
        - harness: codex
          model: gpt-5.2-codex
          reasoning_effort: high
      primary-reviewer:
        - harness: mclaude
          model: opus-4.5
          reasoning_effort: high
        - harness: codex
          model: gpt-5.2-codex
          reasoning_effort: x-high
      planning-council:
        - profile: primary-planner  # reference another profile
```

Reference profiles in jobs via `harness_profile` to avoid hardcoding harness choices.
Skills should always reference profiles, not specific harnesses.

### Profile Resolution for Chat-Routed Jobs

Harness profiles resolve correctly for chat-routed jobs. The ChatService resolves
`harness_profile` names to concrete harness + harness_options using the project's
`x_eve_yaml` (from agent config, synced via `eve agents sync`). This applies to all
chat job creation paths: direct agent routing, team lead/coordinator jobs, team relay
and fanout member jobs, and direct slug routing.

### Profile Resolution Source

Profiles are read from `agent_config.x_eve_yaml` (set during agents sync), not from
`manifest.manifest_yaml`. The manifest contains `x-eve.packs` but not profiles. For
backwards compatibility, resolution falls back to the manifest if agent config is absent.

---

## Harness Auth Status (Introspection)

**API:**
- `GET /harnesses` -- list all harnesses with auth status
- `GET /harnesses/{name}` -- single harness details
- `POST /projects/{project_id}/harness-profile/validate` -- dry-run an inline harness profile override and/or env overrides against project auth and secret availability without creating a job

**Response shape:**
```json
{ "name": "mclaude", "aliases": [], "description": "...",
  "variants": [{ "name": "default", "description": "...", "source": "config" }],
  "auth": { "available": true, "reason": "...", "instructions": [] },
  "capabilities": {
    "supports_model": true, "model_examples": ["opus", "opus4.7", "opus-4-7", "sonnet", "haiku"],
    "reasoning": { "supported": true, "levels": ["low","medium","high","x-high"],
                   "mode": "thinking_tokens" }
  }
}
```

### Validate Endpoint

`POST /projects/{project_id}/harness-profile/validate` — verifies that an
inline `harness_profile_override` and/or `env_overrides` would dispatch
successfully against the project. **Performs no inference**; no harness binary
is invoked.

**Request:**
```json
{
  "harness_profile_override": { "harness": "zai", "model": "glm-5", "reasoning_effort": "medium" },
  "env_overrides": {
    "ANTHROPIC_BASE_URL": "${secret.EDEN_TEST_BASE_URL}",
    "OPENAI_BASE_URL": "${secret.EDEN_OPENAI_URL}"
  }
}
```

**Response shape:**
```json
{
  "ok": true,
  "harness": {
    "requested": "Zai",
    "canonical": "zai",
    "auth": { "available": true, "reason": null, "instructions": [] }
  },
  "env_overrides": [
    { "key": "ANTHROPIC_BASE_URL", "secret_ref": "EDEN_TEST_BASE_URL",
      "status": "resolved", "scope": "project", "hint": null },
    { "key": "OPENAI_BASE_URL", "secret_ref": "EDEN_OPENAI_URL",
      "status": "missing", "scope": null,
      "hint": "Run: eve secrets set EDEN_OPENAI_URL <value> --project <id>" }
  ],
  "warnings": []
}
```

The endpoint does NOT return a would-be argv. Argv preview was deliberately
removed from the API surface — the API's answer is `{harness_known, auth_ok,
secrets_resolve}`. Wizards that need argv preview should call
`eve-agent-cli --build-command-only` on the caller's machine.

Per-secret reports include the resolved scope (`system | org | user | project`)
so callers can tell whether a value comes from a higher precedence tier than
expected. Permission gate matches direct job creation:
`jobs:harness_override` (always) + `secrets:read` (when placeholders are
present).

**CLI:**
- `eve harness list` -- auth availability
- `eve harness list --capabilities` -- auth + model + reasoning support
- `eve harness validate --project <id> --profile-file profile.json` -- validate an inline profile override
- `eve harness validate --project <id> --env-override KEY=${secret.NAME}` -- validate secret-backed env overrides
- `eve harness validate --project <id> --workflow <name> [--env-override KEY=VALUE]` -- validate each workflow step's merged env overrides without creating jobs
- `eve agents config --json` -- project policy + profile resolution

The `--workflow` mode merges workflow-level + step-level + invocation-level
`env_overrides` in that precedence and validates each step independently. Exit
code is 2 on any failure so CI can gate deploys on it.

### Per-Job Harness Override Flow

End-to-end resolution lives in
`packages/shared/src/harnesses/profile-resolver.ts` and replaces the previous
duplicated logic in `chat.service.ts` and `workflows.service.ts`:

```
sources           ──►  resolveHarnessProfile()  ──►  ResolvedProfile
                          (single shared module)        ↓
agent_default                                       harness, harness_options,
string_ref                                          env_overrides,
inline_override                                     profile_name,
workflow_template                                   profile_hash, source,
                                                    warnings[]
```

Precedence: `workflow_template > inline_override > string_ref > agent_default`.
Conflicts emit a single `harness.profile.conflict` warning log; inline wins.

**End-to-end path** (Phases 1–4):

1. **API** validates DTO (`InlineProfileBundleSchema` + `EnvOverridesSchema`),
   permission-checks `jobs:harness_override` (+ `secrets:read` for `${secret.*}`
   refs), and stores the raw bundle on `jobs.harness_profile_override` /
   `jobs.env_overrides`. Direct job creation also projects the effective
   profile into the legacy `jobs.harness` + `jobs.harness_options` columns
   before insert.
2. **Orchestrator** forwards `env_overrides` and override fields unchanged on
   the invocation payload, plus writes attribution to the routing execution log
   and `job_attempts.harness_profile_source` / `harness_profile_hash`.
3. **Shared invoke** (worker + agent-runtime, single module) resolves
   `${secret.KEY}` placeholders against already-resolved project secrets via
   `interpolateEnvOverrides()`. Missing keys throw
   `error_code = missing_secret_override` before harness launch; resolved
   values merge into `adapterEnv` after the reserved-key strip in env-builder.
4. **Chat hints** (Phase 3): `ChatHintsSchema` accepts the same
   `harness_profile_override` + `env_overrides` on `/chat/route`,
   `/chat/dispatch`, and `/chat/simulate`. A legacy `metadata.hints` alias is
   bridged. All 8 chat dispatch sites propagate overrides to lead + child
   jobs, and listener jobs. Override snapshot is written to
   `threads.metadata.harness_overrides` (chat + coordination threads),
   placeholders intact. On `missing_secret_override` failure,
   `EveMessageRelay.deliverProvisioningError` posts a structured error back to
   the originating thread.
5. **Workflow templates** (Phase 4): step-level `harness_profile` and
   `harness_profile_override` accept `${inputs.<key>}` and
   `${event.payload.<dotted.path>}` expressions. Manifest sync rejects
   malformed templates and undeclared `${inputs.*}` references. Missing event
   payload fields at runtime fall back to the agent default with a warning.

Receipts (`packages/shared/src/pricing/receipt/`) carry `harness_profile_*`
metadata so cost analytics can group by profile (e.g. `cost-by-harness-profile`)
in addition to the existing `cost-by-agent`.

---

## eve-agent-cli Arguments

```
eve-agent-cli \
  --harness <harness>           # mclaude, claude, zai, gemini, code, codex
  --permission <policy>         # default, auto_edit, never, yolo
  --output-format stream-json
  --workspace <workspacePath>
  --prompt "<text>"
  [--variant <variant>]         # optional harness variant
  [--model <model>]             # optional model override
  [--build-command-only]        # print the would-be exec argv and exit; no spawn
```

`--build-command-only` is the client-side companion to the API validate
endpoint: it prints exactly what would be executed (binary + args + env-bound
flags) without actually spawning the harness. Useful for wizards or local
debugging — the API itself does not return argv.

---

## Execution Logging

All harness output is logged to the `execution_logs` table:

| Type           | Description                                           |
|----------------|-------------------------------------------------------|
| `event`        | Normalized harness event (assistant, tool_use, tool_result, etc.) |
| `system`       | System events (init, completed)                       |
| `system_error` | Stderr output                                         |
| `parse_error`  | Failed to parse JSON line from harness                |
| `spawn_error`  | Failed to spawn harness process                       |

---

## Environment Variables Reference

### Auth Variables

| Variable                       | Description                                    |
|--------------------------------|------------------------------------------------|
| `ANTHROPIC_API_KEY`            | Claude API key; wins only within same secret scope |
| `CLAUDE_CODE_OAUTH_TOKEN`      | Claude setup-token or OAuth token secret       |
| `CLAUDE_OAUTH_EXPIRES_AT`      | Optional OAuth expiry metadata                 |
| `Z_AI_API_KEY`                 | API key for zai harness                        |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | API key for Gemini                        |
| `CODEX_AUTH_JSON_B64`          | Base64-encoded auth.json for Code/Codex        |
| `CODEX_OAUTH_ACCESS_TOKEN`     | OAuth access token for Code/Codex              |
| `CODEX_OAUTH_REFRESH_TOKEN`    | OAuth refresh token for Code/Codex             |
| `CODEX_OAUTH_ID_TOKEN`         | OAuth ID token for Code/Codex                  |
| `CODEX_OAUTH_ACCOUNT_ID`       | Account ID for Code/Codex                      |

### Config + Worker Variables

| Variable                       | Description                                    |
|--------------------------------|------------------------------------------------|
| `EVE_HARNESS_CONFIG_ROOT`      | Override repo `.agent/harnesses` root          |
| `CLAUDE_CONFIG_DIR`            | Config directory for Claude-based harnesses    |
| `CLAUDE_MODEL`                 | Default model for Claude harnesses             |
| `ZAI_MODEL`                    | Model override for zai                         |
| `CODEX_HOME`                   | Config directory for Code/Codex                |
| `CLAUDE_CODE_TEAM_NAME`        | Set to attemptId for tracking                  |
| `WORKSPACE_ROOT` / `EVE_WORKSPACE_ROOT` | Root directory for workspaces        |
| `EVE_CACHE_ROOT`               | Shared cache directory                         |
| `EVE_AGENT_CLI_PATH`           | Override path to eve-agent-cli binary          |
| `EVE_TOOLCHAIN_PATHS`          | Colon-separated paths to mounted toolchain bins |
| `EVE_TOOLCHAIN_IMAGE_PREFIX`   | Image prefix for toolchain init containers     |
| `EVE_TOOLCHAIN_IMAGE_TAG`      | Image tag for toolchain init containers        |
