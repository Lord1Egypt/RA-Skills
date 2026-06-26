# Pipeline Authoring Reference

## Builders

All builders are exported from `'skelm'` (or `'@skelm/core'`).

### `pipeline(def)`

```ts
pipeline({
  id: string                                  // required; stable, kebab-case
  description?: string
  version?: string
  input?: SkelmSchema<TInput>                 // optional; validated at run start when present
  output?: SkelmSchema<TOutput>               // optional; validated after finalize
  steps: Step[]                               // ordered; run sequentially
  finalize?: (ctx: Context<TInput>) => TOutput | Promise<TOutput>
})
```

`SkelmSchema` is structurally compatible with Zod schemas; importing zod and passing `z.object({...})` works.

### `code(def)` — deterministic step

```ts
code({
  id: string
  run: (ctx: Context) => TOutput | Promise<TOutput>
  retry?: RetryPolicy
})
```

Access prior step outputs: `ctx.steps['step-id']` (cast to the output type). Access run metadata: `ctx.run.runId`, `ctx.run.pipelineId`, `ctx.run.startedAt`.

### `llm(def)` — single-shot inference

```ts
llm({
  id: string
  prompt: string | ((ctx: Context) => string)
  system?: string | ((ctx: Context) => string)
  backend?: string                // overrides config default
  model?: string
  output?: ZodSchema<TOutput>    // structured output
  temperature?: number
  maxTokens?: number
  retry?: RetryPolicy
})
```

### `agent(def)` — full agentic loop

See [agent-step.md](agent-step.md) for the full reference.

### `parallel(def)` — concurrent children

```ts
parallel({
  id: string
  steps: Step[]                       // must have unique ids within this block
  waitFor?: 'all' | 'any' | { atLeast: number }   // default: 'all'
  onError?: 'fail' | 'continue' | 'partial'        // default: 'fail'
})
```

Output is an object keyed by child step id. Access via `ctx.steps['parallel-id']`.

### `forEach(def)` — map over a collection

```ts
forEach({
  id: string
  items: (ctx: Context) => readonly unknown[]
  step: (item: unknown, index: number) => Step
  concurrency?: number              // default: unbounded
})
```

Output is an array of child step outputs in order.

### `branch(def)` — discriminator-driven routing

```ts
branch({
  id: string
  on: (ctx: Context) => string      // returns one of the case keys
  cases: Record<string, Step>
  default?: Step
})
```

### `loop(def)` — bounded iteration

```ts
loop({
  id: string
  while: (ctx: Context) => boolean | Promise<boolean>
  maxIterations: number             // required; prevents infinite loops
  step: Step
})
```

### `wait(def)` — pause until resumed

```ts
wait({
  id: string
  message?: string | ((ctx: Context) => string)
  timeoutMs?: number
  output?: ZodSchema<TOutput>
})
```

Resume via `POST /runs/:id/resume` on the gateway HTTP surface.

### `pipelineStep(def)` — nested pipeline

```ts
pipelineStep({
  id: string
  pipeline: Pipeline<TInput, TOutput>
  input?: TInput | ((ctx: Context) => TInput)
})
```

### `idempotent(def)` — cached step

```ts
idempotent({
  id: string
  key: string | ((ctx: Context) => string)    // cache key
  step: Step
  ttlMs?: number                               // cache TTL; default: unlimited
})
```

---

## Multi-step example

```ts
import { code, pipeline } from 'skelm'
import { z } from 'zod'

export default pipeline({
  id: 'multi-step',
  input: z.object({ task: z.string().min(1) }),
  output: z.object({ report: z.string() }),
  steps: [
    code({
      id: 'parse',
      run: (ctx) => ({ task: (ctx.input as { task: string }).task.trim() }),
    }),
    code({
      id: 'summarize',
      run: (ctx) => {
        const { task } = ctx.steps['parse'] as { task: string }
        return { summary: `Summary of: ${task}` }
      },
    }),
  ],
  finalize: (ctx) => {
    const { task } = ctx.steps['parse'] as { task: string }
    const { summary } = ctx.steps['summarize'] as { summary: string }
    return { report: `${task}: ${summary}` }
  },
})
```

---

## RetryPolicy

```ts
interface RetryPolicy {
  maxAttempts: number             // total attempts including first
  delayMs?: number                // base delay between retries (ms)
  backoffMultiplier?: number      // exponential multiplier; default 1 (linear)
}
```

---

## Context shape

```ts
interface Context<TInput = unknown> {
  input: TInput
  steps: Record<string, unknown>    // keyed by step id
  run: RunMetadata                  // runId, pipelineId, startedAt
  signal: AbortSignal
  state: State                      // per-run KV + streams
  threads: ThreadHost               // conversation thread tracking
  workspace?: WorkspaceHandle       // path + mode when workspace is provisioned
  item?: unknown                    // current forEach item
  secrets?: { get(name: string): string | undefined }
  exec?: ExecFn                     // spawn external process (gated by allowedExecutables)
  get<T>(stepId: string): T | undefined  // typed alias for ctx.steps[id]
}
```

Cast step outputs: `ctx.steps['my-step'] as MyType` or `ctx.get<MyType>('my-step')`.

---

## `check()` — test assertion step (v0.4.3)

`check()` is a `code()` wrapper purpose-built for test pipelines. Thrown errors become `TestResult { status: 'fail', message }` instead of aborting the pipeline. Always sets `continueOnError: true` implicitly.

```ts
import { check, pipeline } from 'skelm'
import { summarizeChecks, testExecPermissions } from '@skelm/core/testing'

export default pipeline({
  id: 'my-section',
  steps: [
    check({
      id: 'healthcheck',
      permissions: testExecPermissions,
      run: async (ctx) => {
        const r = await ctx.exec!({ command: 'curl',
          args: ['-sf', 'http://localhost:4001/healthz'], throwOnNonZero: true })
        return JSON.parse(r.stdout)
      },
    }),
  ],
  finalize: (ctx) => summarizeChecks('my-section', ['healthcheck'], ctx, Date.now()),
})
```

**Testing exports from `@skelm/core/testing`** (safe in `skelm run` workflows):
- `check(def)` — also exported from `'skelm'` directly
- `TestResult`, `SectionResult`, `SummaryReport` — typed shapes
- `summarizeChecks(sectionId, checkIds, ctx, startedAt)` — per-section finalize helper
- `summarizeSections(sectionIds, ctx, startedAt)` — orchestrator finalize helper
- `testExecPermissions` — preset `AgentPermissions` for `skelm`, `node`, `curl`, `gh`, `git`, `pnpm`, etc.
- `probeHttp({ id, url, timeoutMs?, pollMs? })` — polls URL until ready, returns a `CodeStep`
- `gatewayFixture({ port, dataDir?, configFile? })` — `.start()` and `.stop()` code steps

**Backend contract suite** (vitest-only — do NOT import in `skelm run` workflows):
```ts
import { fixtureBackend, runBackendContract } from '@skelm/core/testing/contract'
```

---

## `invoke(def)` — invoke a registered pipeline (v0.4.x)

```ts
invoke({
  id: string
  pipelineId: string              // resolved via pipelineRegistry at runtime
  input?: TInput | ((ctx) => TInput)
  state?: StateConfig
  retry?: RetryPolicy
  continueOnError?: boolean
  when?: WhenPredicate
})
```

Used in orchestrator pipelines to call sub-pipelines by id. The gateway wires `pipelineRegistry` automatically.

---

## `when` predicate

Every step builder accepts `when?: (ctx: Context) => boolean | Promise<boolean>`. When it returns `false` the step is skipped — `StepResult` has `status: 'skipped'`, `ctx.steps[id]` is `undefined` for later steps.

```ts
code({
  id: 'codex-check',
  when: () => process.env.SKELM_CODEX_INTEGRATION === '1',
  run: async (ctx) => { /* ... */ },
})
```
