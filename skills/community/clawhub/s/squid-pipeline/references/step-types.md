# Step Types — Full Reference

## run

```yaml
- id: build
  type: run
  run: docker build -t ${args.image} .
  timeout: 300
  cwd: /project
  env: { NODE_ENV: production }
  retry: 3
```

Stdout captured as `$build.stdout`. If valid JSON, also `$build.json`. Interpolate with `${args.key}`, `${stepId.json.field}`.

## spawn

```yaml
# Simple
- id: analyze
  type: spawn
  spawn: "Analyze the codebase"

# Full
- id: architect
  type: spawn
  spawn:
    task: |
      Design architecture for: ${args.feature}
      Output JSON: { files: [], interfaces: [], tests: [] }
    agent: claude-code            # openclaw | claude-code | opencode | custom
    model: claude-sonnet-4-6
    thinking: high                # off | low | high (OpenClaw only)
    cwd: ${args.repo}
    timeout: 300
    # OpenClaw-specific:
    agentId: architect-agent
    runtime: subagent             # subagent | acp
    mode: run                     # run (ephemeral) | session (persistent)
    sandbox: inherit              # inherit | require
    attachments:
      - name: spec.md
        content: "..."
        encoding: utf8            # utf8 | base64
        mimeType: text/markdown
```

Pipeline default: `agent: claude-code` at root applies to all spawns. Override per step.

## gate

```yaml
# Simple
- id: approve
  type: gate
  gate: "Deploy to production?"

# Full with structured input + identity
- id: config
  type: gate
  gate:
    prompt: "Configure deployment"
    preview: $build.json           # data shown to approver
    items: $test.json.results      # list of items shown
    timeout: 3600                  # auto-reject after N seconds
    autoApprove: false             # only for dev/CI

    # Structured input (form fields, not just yes/no)
    input:
      - name: env
        type: select              # string | number | boolean | select
        label: Target environment
        description: Where to deploy
        options: ["staging", "prod"]
        required: true            # default: true
      - name: replicas
        type: number
        default: 2
      - name: version
        type: string
        validation: "^\\d+\\.\\d+$"  # regex pattern
      - name: migrate
        type: boolean
        default: false

    # Caller identity
    approvers: ["admin", "lead"]        # suggested approvers
    requiredApprovers: ["lead", "sre"]  # MUST be one of these to approve
    allowSelfApproval: false            # pipeline initiator cannot approve
```

- Halts with **8-char short ID** (e.g., `a1b2c3d4`) for chat platforms + full resume token
- Access input: `$config.json.input.env`, `$config.json.input.replicas`
- Access identity: `$config.json.approvedBy`
- Input validated: type, required, regex, select options

## parallel

```yaml
- id: build-all
  type: parallel
  parallel:
    maxConcurrent: 3
    failFast: true               # abort all on first failure (default: true)
    merge: object                # object | array | first
    branches:
      backend:
        - id: api
          type: run
          run: npm run build:api
      frontend:
        - id: ui
          type: run
          run: npm run build:ui
```

- `merge: object` -> `{ "backend": result, "frontend": result }`
- `merge: array` -> `[result1, result2]`
- `merge: first` -> only first branch's result

## loop

```yaml
- id: process
  type: loop
  loop:
    over: $data.json.items        # REQUIRED — must resolve to array
    as: item                      # variable name (default: "item")
    index: i                      # index variable (default: "index")
    maxConcurrent: 4              # parallel iterations (default: 1)
    maxIterations: 1000           # safety limit (default: 1000)
    collect: results              # output key name
    steps:
      - id: handle
        type: spawn
        spawn:
          task: "Process: ${item.name}"
          timeout: 60
```

Use `$item`/`$index` inside loop. Output is array of iteration results.

## branch

```yaml
- id: route
  type: branch
  branch:
    conditions:                   # top-to-bottom, first match wins
      - when: $test.json.failures > 0
        steps:
          - id: fix
            type: spawn
            spawn: "Fix: ${test.json.failures}"
      - when: $test.json.coverage < 80
        steps:
          - id: more-tests
            type: spawn
            spawn: "Add tests for coverage"
    default:
      - id: ok
        type: transform
        transform: '{"passed": true}'
```

Conditions support: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`, `$ref.field`, literals.

## transform

```yaml
# Extract a value
- id: extract
  type: transform
  transform: $fetch.json.data.url

# JSON template
- id: shape
  type: transform
  transform: '{"env": "${args.env}", "v": "${build.json.version}"}'

# String interpolation
- id: msg
  type: transform
  transform: "Deployed ${args.image} to ${args.env}"
```

No execution — pure data shaping.

## pipeline

```yaml
# Simple
- id: build
  type: pipeline
  pipeline: ./stages/build.yaml

# Full
- id: build
  type: pipeline
  pipeline:
    file: ./stages/build.yaml    # relative to THIS pipeline's file
    args:
      target: $args.env          # $refs resolved in parent context
      data: $fetch.json
    env: { VERBOSE: "1" }
    cwd: /workspace
```

- Sub-pipeline output = step output (`$build.json`)
- Gates propagate up — parent halts too
- File path relative to **parent pipeline's directory**, not cwd
- Each sub-pipeline is standalone and independently testable

## Common Step Options

Apply to ANY step type:

```yaml
- id: deploy
  type: run
  run: kubectl apply -f deploy.yaml
  description: "Deploy to production"        # label for viz/logs
  when: $approve.approved && $test.json.pass  # conditional execution
  timeout: 300                                # seconds
  cwd: /project                               # working directory
  env: { NODE_ENV: production }               # step-level env

  retry:                                      # automatic retry
    maxAttempts: 3
    backoff: exponential-jitter               # fixed | exponential | exponential-jitter
    delayMs: 1000
    maxDelayMs: 30000
    retryOn: ["ECONNRESET", "timeout"]

  restart:                                    # jump back to earlier step
    step: write                               # target step ID (must be earlier)
    when: $review.json.score < 80             # condition to trigger
    maxRestarts: 3                            # safety limit
```

### when expressions

- References: `$step.approved`, `$step.skipped`, `$step.json.field`
- Comparisons: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logic: `&&` (AND), `||` (OR), `!` (NOT)
- Literals: `true`, `false`, numbers, `"quoted strings"`

## Events / Observability

Every step emits lifecycle events. Pass a `PipelineEventEmitter` to capture them.

```typescript
import { createEventEmitter, runPipeline, parseFile } from "squid";

const events = createEventEmitter();
events.on("*", (e) => console.log(`[${e.type}] ${e.stepId}`));
events.on("gate:waiting", (e) => slack.send(`Approve: ${e.data?.prompt}`));
events.on("step:error", (e) => pagerduty.trigger(`${e.stepId}: ${e.data?.error}`));

await runPipeline(parseFile("pipeline.yaml"), { events });
```

**Event types**: `pipeline:start`, `pipeline:complete`, `pipeline:error`, `step:start`, `step:complete`, `step:error`, `step:skip`, `step:retry`, `gate:waiting`, `gate:approved`, `gate:rejected`, `spawn:start`, `spawn:complete`.

**OTel fields**: `traceId` (= runId), `spanId`, `parentSpanId`, `timestamp`, `pipelineId`, `runId`, `stepId`, `stepType`, `duration`, `data`.

See `examples/observability.yaml` for a full example.
