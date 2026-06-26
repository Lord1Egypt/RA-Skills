---
name: squid-pipeline
description: Create, modify, and debug agentic pipelines with Squid. Define multi-agent YAML workflows with spawn (OpenClaw, Claude Code, OpenCode), gates, parallel execution, loops, branching, restart loops, sub-pipelines, and structured approvals. Use when working with .yaml pipeline files or when the user mentions pipelines, workflows, agents, or Squid.
---

## Required Reading — Reference Files

This skill includes reference docs and working examples. **You MUST read the relevant files before generating pipelines or tests.** SKILL.md alone is not sufficient — the references contain critical syntax details.

**BEFORE creating or modifying any pipeline**, read:
- `references/step-types.md` — Full config for every step type (run, spawn, gate, parallel, loop, branch, transform, pipeline). Contains exact field names, types, and valid values.
- `references/patterns.md` — Validated workflow patterns with complete YAML examples. Use these as templates.

**BEFORE creating or modifying any test file**, read:
- `references/testing.md` — Full test file schema, mock syntax, assertion types, mode behaviors. Contains exact valid field names and values.

**BEFORE writing a pipeline that matches an example pattern**, read the matching example:
- `examples/simple-deploy.yaml` + `examples/simple-deploy.test.yaml` — Basic pipeline with tests
- `examples/multi-agent-dev.yaml` — Multi-agent with parallel branches
- `examples/iterative-refinement.yaml` — Restart loop pattern
- `examples/advanced-gates.yaml` — Structured gate input
- `examples/orchestrator.yaml` — Sub-pipeline composition

All paths are relative to this skill directory.

## Install

If Squid is not installed, install it first:

```bash
git clone https://github.com/dominno/squid.git
cd squid
npm install
npm run build
```

Then use directly:

```bash
npx squid run pipeline.yaml
npx squid test
npx squid validate pipeline.yaml
npx squid viz pipeline.yaml
npx squid init --template basic --name my-pipeline
```

Or link globally:

```bash
npm link
squid run pipeline.yaml
```

Requires **Node.js 20+**.

## Mandatory Rules

These rules are NON-NEGOTIABLE. Every pipeline you generate MUST follow all of them. Violations are bugs.

### R1: Gate before side effects
Any step that modifies external state (git push, API POST, deploy, file write to shared storage, PR creation, sending messages) MUST be preceded by a `type: gate` step. The side-effect step MUST have `when: $gate.approved` in its condition.

### R2: Every pipeline and sub-pipeline MUST set `onError`
Always set `onError: fail` (or `skip`/`continue` with justification). Never omit it — the default behavior is implicit and error-prone.

### R3: Every `spawn` step MUST specify output format and `timeout`
In the `task` field, always end with `Output JSON: { ... }` showing the exact shape. Always set `timeout` (seconds). No exceptions.

### R4: Every `run` step that calls an external API or network MUST have `retry`
Use `retry: { maxAttempts: 2, backoff: fixed }` minimum. Network calls are flaky by nature.

### R5: Every `loop` MUST have `maxIterations`
Prevents runaway execution. No exceptions.

### R6: Downstream steps MUST guard on upstream success
If step B depends on step A's output, step B MUST have a `when:` condition that checks the relevant output field. Especially critical after `restart:` loops — downstream steps must check the final approval/success state, not just whether the step ran.

### R7: `transform` steps MUST use `${ref}` interpolation in JSON templates
Inside JSON template strings, ALWAYS use `${stepId.json.field}` (curly braces), NEVER bare `$stepId.json.field`.
- Correct: `{"score": ${reviewer.json.score}, "name": "${args.name}"}`
- Wrong: `{"score": $reviewer.json.score, "name": "$args.name"}`
- Bare `$ref` only works as a standalone expression (e.g., `transform: $step.json`) or in `when:` conditions.
- Transforms do NOT support: ternary operators (`? :`), JavaScript expressions, function calls, or arithmetic. Use a `branch` step instead.

### R8: Every pipeline MUST have a `.test.yaml` covering at minimum
1. **Happy path** — all gates approved, all steps succeed
2. **Gate rejection** — verify side-effect steps are skipped
3. **Step failure** — verify error propagation
4. **Restart exhaustion** (if `restart:` is used) — verify behavior when maxRestarts is reached without meeting the threshold

### R9: `spawn` tasks that clone repos MUST use deterministic branch checkout
Never use shell inference (`git log --format=%D | grep ...`). Instead use:
- For PRs: `git fetch origin pull/{number}/head:pr-{number} && git checkout pr-{number}`
- For branches: pass the branch name explicitly via pipeline args or prior step output

### R10: No unused code or imports in scripts
Scripts MUST be clean — no unused imports, no dead code, no placeholder comments.

## Pipeline Structure

Build Squid pipelines in YAML. Every pipeline has `name`, `steps`, and required `onError` (see R2).

```yaml
name: <pipeline-name>              # REQUIRED
description: <what it does>        # REQUIRED
agent: claude-code                 # default agent adapter for spawn steps
onError: fail                      # REQUIRED (R2) — fail | skip | continue
args:
  <key>:
    default: <value>
    description: <help text>
    required: true
env:
  KEY: value

steps:
  - id: <unique-id>               # REQUIRED — unique per step
    type: <step-type>              # REQUIRED
    description: <label>           # REQUIRED
```

**Rules**: unique `id` per step, sequential execution, outputs available as `$stepId.json`.

## Step Types

| Type | Key Config | Purpose |
|------|-----------|---------|
| `run` | `run: "cmd"` | Shell command |
| `spawn` | `spawn: { task, agent, model }` | AI sub-agent |
| `gate` | `gate: { prompt, input, requiredApprovers }` | Human approval with structured input |
| `parallel` | `parallel: { branches, maxConcurrent }` | Fan-out/fan-in |
| `loop` | `loop: { over, as, steps, maxConcurrent }` | Iterate array |
| `branch` | `branch: { conditions, default }` | Conditional routing |
| `transform` | `transform: "$ref"` | Data shaping (R7: JSON templates only, no JS expressions) |
| `pipeline` | `pipeline: { file, args }` | Sub-pipeline |

**You MUST read `references/step-types.md` before using any step type** — it contains exact field names, valid values, and required options not shown above.

## Spawn — Agent Adapters

4 adapters available. Resolution order: `step.agent` → `pipeline.agent` → `SQUID_AGENT` env var → `openclaw` (default fallback).

```bash
# Set default adapter via env (overrides the openclaw fallback)
export SQUID_AGENT=claude-code     # or: openclaw, opencode
```

The `agent:` field in YAML is **optional** — only needed to override the env/fallback default. Set it per-pipeline at root, or per-step in spawn config.

### When to use which adapter

| Adapter | Best for | Requires |
|---------|----------|----------|
| `claude-code` | Code tasks (implement, fix, refactor) — runs in a repo directory | `claude` CLI installed and authenticated |
| `openclaw` | Non-code tasks (review, plan, research) — runs as OpenClaw sub-agents | OpenClaw gateway or CLI |
| `openclaw` + `runtime: acp` | Code tasks via OpenClaw's Agent Control Plane (Claude Code through OpenClaw) | OpenClaw with ACP configured |
| `opencode` | Code tasks via OpenCode CLI | `opencode` CLI installed |

### Claude Code (standalone, no OpenClaw)

```yaml
agent: claude-code                 # set as pipeline default

steps:
  - id: implement
    type: spawn
    spawn:
      task: "Implement feature X. Output JSON: {\"files_changed\": <n>}"
      agentId: code-reviewer       # optional: target a Claude Code sub-agent (defined in .claude/agents/)
      model: claude-sonnet-4-6     # optional (default: CLAUDE_MODEL env)
      timeout: 300
      cwd: /path/to/repo           # working directory for the agent
```

**Env:** `CLAUDE_MODEL` (optional default model)
**How it works:** Runs `claude --agent <agentId> -p "task" --output-format json` as subprocess (omits `--agent` if no `agentId`).
**Sub-agents:** Define agents in `.claude/agents/<name>.md` files. Use `agentId` to target them — each agent has its own system prompt, tool access, and permissions.

### OpenClaw (sub-agents)

```yaml
agent: openclaw                    # set as pipeline default (also the fallback default)

steps:
  - id: review
    type: spawn
    spawn:
      task: "Review code quality. Output JSON: {\"score\": <n>, \"issues\": [...]}"
      agentId: code-reviewer       # target specific OpenClaw agent
      thinking: high               # off | low | high
      runtime: subagent            # subagent (in-process) | acp (external Claude Code)
      timeout: 300
      # NOTE: model is set per agent in OpenClaw config, not here.
      # model: only has effect with runtime: acp (passed to Claude Code)
```

**Requires:** `openclaw` CLI installed and authenticated (`openclaw config`). Squid invokes `openclaw agent --agent <id> --message "..."` as a subprocess. The CLI uses its own stored credentials (`~/.openclaw/config.json`) — no env vars needed.
**OpenClaw-only options:** `runtime`, `mode` (run|session), `sandbox` (inherit|require), `attachments`

**When does `model:` apply?**
- `runtime: subagent` — model is **ignored**. The OpenClaw agent uses whatever model is in its own config.
- `runtime: acp` — model is **passed** to the ACP-spawned Claude Code instance.

### OpenClaw + ACP (Claude Code through OpenClaw)

Use `runtime: acp` to run Claude Code agents managed by OpenClaw's Agent Control Plane:

```yaml
- id: implement
  type: spawn
  spawn:
    task: "Implement the feature. Output JSON: {\"implemented\": true}"
    agent: openclaw
    runtime: acp                   # routes to Claude Code via OpenClaw ACP
    timeout: 600
```

### OpenCode (standalone, no OpenClaw)

```yaml
agent: opencode                    # set as pipeline default

steps:
  - id: fix
    type: spawn
    spawn:
      task: "Fix the bug. Output JSON: {\"fixed\": true}"
      model: gpt-4o               # optional
      timeout: 300
      cwd: /path/to/repo
```

**Env:** `OPENCODE_MODEL` (optional default model)
**How it works:** Runs `opencode run --message "task"` as subprocess.

### `agentId` — targeting named sub-agents

`agentId` works across adapters to target a specific named agent:

| Adapter | How `agentId` is used | Where agents are defined |
|---------|----------------------|------------------------|
| `claude-code` | Passed as `--agent <name>` to the CLI | `.claude/agents/<name>.md` files |
| `openclaw` | Passed as `--agent <name>` to the CLI | OpenClaw agent config |
| `opencode` | Not yet supported | — |

```yaml
- id: review
  type: spawn
  spawn:
    task: "Review the code. Output JSON: {\"score\": <n>}"
    agentId: code-reviewer     # targets the same agent name regardless of adapter
    timeout: 120
```

### Mixing adapters in one pipeline

```yaml
agent: claude-code                 # default for most steps

steps:
  - id: implement
    type: spawn
    spawn:
      task: "Write the code"       # uses claude-code (pipeline default)
      timeout: 300

  - id: review
    type: spawn
    spawn:
      task: "Review the code"
      agent: openclaw              # override: use OpenClaw for this step
      agentId: reviewer-agent
      timeout: 120
```

**Full adapter reference:** [docs/adapters.md](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/adapters.md) — custom adapter interface, feature comparison table, and detailed examples.

## Gate — Structured Input + Identity

```yaml
- id: deploy-config
  type: gate
  gate:
    prompt: "Configure deployment"
    input:                         # form fields, not just approve/reject
      - name: env
        type: select
        options: ["staging", "prod"]
      - name: replicas
        type: number
        default: 2
    requiredApprovers: ["lead"]    # only these IDs can approve
    allowSelfApproval: false       # initiator cannot approve
```

- Halts with 8-char **short ID** (chat-friendly) + full resume token
- Access input: `$gate.json.input.env`, `$gate.json.approvedBy`
- Input validated: type, required, regex, select options

**R1 reminder**: Every step after a gate that performs side effects MUST check `when: $gateId.approved`.

## Common Options

Apply to any step:

```yaml
when: $approve.approved && $test.json.pass   # conditional (R6: guard on upstream)
retry: { maxAttempts: 3, backoff: exponential-jitter }  # R4: required for network calls
restart: { step: write, when: $review.json.score < 80, maxRestarts: 3 }
timeout: 300
env: { KEY: value }
description: "Human-readable label"          # REQUIRED on every step
```

## Data Flow

| Pattern | Value |
|---------|-------|
| `$stepId.json` | Parsed JSON output |
| `$stepId.stdout` | Raw stdout |
| `$stepId.approved` | Gate boolean |
| `$stepId.json.input.field` | Gate structured input |
| `$args.key` | Pipeline argument |
| `$env.VAR` | Environment variable |
| `$item` / `$index` | Loop context |

Interpolation: `${args.key}`, `${stepId.json.field}` in strings.

## Key Patterns

**Plan → Gate → Execute** (R1): Always gate before side effects. No spawn/run that pushes, deploys, or mutates external state without a preceding gate.

**Parallel Agents → Review**: Fan out to specialists, then aggregate.

**Iterative Refinement**: `restart:` loops back until quality threshold met. Downstream steps MUST guard on the final result (R6) — e.g., `when: $review.json.approved`.

**Sub-Pipeline Composition**: Break large workflows into `type: pipeline` stages. Each sub-pipeline MUST set its own `onError` (R2).

**Error Handling**: `branch:` on `$step.status == "failed"` with rollback.

**Retry on network calls** (R4): Any `run` step hitting an external API (GitHub, Slack, HTTP) MUST have `retry`.

**Read `references/patterns.md` for complete YAML examples** of each pattern before implementing.

## Examples

Working pipeline examples in `examples/`:

| File | What it demonstrates |
|------|---------------------|
| `examples/simple-deploy.yaml` | Basic build → test → gate → deploy |
| `examples/orchestrator.yaml` | Sub-pipeline composition (calls sub-build, sub-test, sub-deploy) |
| `examples/multi-agent-dev.yaml` | 8 specialized agents: architect, coders, tester, reviewer, docs |
| `examples/video-pipeline.yaml` | Content creation with parallel asset generation loops |
| `examples/iterative-refinement.yaml` | Restart loop: write → review → refine until quality met |
| `examples/advanced-gates.yaml` | Structured input fields, requiredApprovers, short IDs |
| `examples/observability.yaml` | Event hooks, OTel spans, audit trails, chat notifications |
| `examples/simple-deploy.test.yaml` | YAML test file with sandbox + integration tests |
| `examples/sub-build.test.yaml` | YAML test file for sub-pipeline |

## Testing

Create `pipeline.test.yaml` alongside `pipeline.yaml`. **R8: Every pipeline MUST have tests.**

```yaml
pipeline: ./pipeline.yaml
tests:
  - name: "deploys when approved"
    mode: sandbox                  # nothing executes
    mocks:
      run:
        build: { output: { built: true } }
    gates:
      approve: true
    assert:
      status: completed
      steps:
        deploy: completed
```

Modes: `sandbox` (all mocked) | `integration` (run steps execute).
Run: `squid test` (auto-discovers) or `squid test file.test.yaml`.

### Test YAML syntax rules — MUST follow exactly

**Supported mock types — ONLY these two exist:**
```yaml
mocks:
  run:                             # Mock run steps
    stepId:
      output: { key: value }      # JSON output (parsed as $stepId.json)
      stdout: "raw text"          # Raw stdout ($stepId.stdout)
      status: completed            # "completed" | "failed" — ONLY these two values
      error: "message"
  spawn:                           # Mock spawn steps
    stepId:
      output: { key: value }      # JSON output
      status: accepted             # "accepted" | "error" — ONLY these two values
      error: "message"
```

**NEVER use these — they do NOT exist and are silently ignored:**
- `mocks.pipeline` — does NOT exist. Sub-pipeline steps run normally (their internal steps get sandbox defaults).
- `mocks.branch` — does NOT exist.
- `mocks.loop` — does NOT exist.
- `mocks.transform` — does NOT exist.
- `mocks.gate` — does NOT exist. Use `gates:` top-level key instead.

**Spawn mock status values:**
- Use `status: error` to simulate spawn failure (NOT `status: failed` — that is for run mocks only)
- Use `status: accepted` for success (default if omitted)

**Sandbox vs integration mode behavior:**
- `sandbox`: Run mocks work via `onRun` hook. **Spawn mocks are IGNORED** — spawns go to the mock adapter which always returns `{mocked: true}`. Use `integration` mode if you need spawn mocks to work.
- `integration`: Run steps execute for real (unless mocked). Spawn mocks work via `onSpawn` hook.

**Gate behavior in tests:**
- `gates: { stepId: true }` → gate approved, step status = `"completed"`, `$stepId.approved` = true
- `gates: { stepId: false }` → gate rejected, step status = `"skipped"`, `$stepId.approved` = false
- Unmocked gates are auto-approved

**Sub-pipeline steps in tests:**
- Cannot be mocked directly. The sub-pipeline file is loaded and its steps run in the current test mode.
- To control sub-pipeline behavior, mock its internal `run` steps by their step IDs, or use sandbox mode where unmocked run steps return `{sandbox: true}`.

### Required test coverage (R8):
1. Happy path — all approved, all succeed
2. Gate rejection — assert side-effect steps are `skipped`
3. No-data path — assert conditional steps are `skipped` when `when:` evaluates false
4. Restart exhaustion — if `restart:` used, test behavior when threshold is never met

**You MUST read `references/testing.md` before writing any test file** — it contains the full assertion schema and mode behavior details.

## Events / Observability

Pipeline execution emits lifecycle events for monitoring, OTel, audit trails, and chat notifications.

```typescript
import { createEventEmitter, runPipeline, parseFile } from "squid";

const events = createEventEmitter();
events.on("*", (e) => console.log(`[${e.type}] ${e.stepId}`));
events.on("gate:waiting", (e) => slack.send(`Approve: ${e.data?.prompt}`));
events.on("step:error", (e) => pagerduty.trigger(`${e.stepId}: ${e.data?.error}`));

await runPipeline(parseFile("pipeline.yaml"), { events });
```

**13 event types**: `pipeline:start/complete/error`, `step:start/complete/error/skip/retry`, `gate:waiting/approved/rejected`, `spawn:start/complete`.

**OTel-compatible**: every event has `traceId`, `spanId`, `timestamp`, `duration`.

Read `references/step-types.md` (Events section) and `examples/observability.yaml` for implementation details.

## CLI

```bash
squid run <file> [--args-json '{}'] [--dry-run] [-v]
squid test [file.test.yaml]
squid resume <file> --token <token> --approve yes|no
squid validate <file>
squid viz <file>
squid init --template basic|agent|parallel|full --name <name>
```

## Pre-Delivery Checklist

Before delivering any pipeline to the user, verify ALL items. If any item fails, fix before delivering.

- [ ] Every pipeline and sub-pipeline has `onError` set **(R2)**
- [ ] Every step has unique `id` and `description`
- [ ] Every `spawn` step specifies output format in `task` and has `timeout` **(R3)**
- [ ] Every `run` step hitting external APIs has `retry` **(R4)**
- [ ] Every step that mutates external state is preceded by a `gate` **(R1)**
- [ ] Every step after a gate checks `$gate.approved` in its `when:` **(R1)**
- [ ] Every step depending on upstream output has a `when:` guard **(R6)**
- [ ] Steps downstream of `restart:` guard on the final success/approval state **(R6)**
- [ ] Every `loop` has `maxIterations` **(R5)**
- [ ] `transform` steps use only JSON templates, no JS expressions **(R7)**
- [ ] Repo checkout uses deterministic branch refs, not shell inference **(R9)**
- [ ] `.test.yaml` covers happy path, rejection, failure, and restart exhaustion **(R8)**
- [ ] `squid validate` passes on all pipeline files
- [ ] Scripts have no unused imports or dead code **(R10)**

## Documentation Links

Full docs on GitHub (for topics not covered in this skill or its references):

| Doc | URL |
|-----|-----|
| Getting Started | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/getting-started.md |
| Step Types | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/step-types.md |
| Agent Adapters | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/adapters.md |
| Workflow Patterns | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/workflow-patterns.md |
| Testing Guide | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/testing.md |
| Lobster Migration | https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/migration.md |
| Use Case Examples | https://github.com/dominno/squid-workflows |
