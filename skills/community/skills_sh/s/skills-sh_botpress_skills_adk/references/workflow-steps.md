# Workflow Step API

Complete reference for every method on the `step` object inside workflow handlers.

> **Prerequisites:** See [workflows.md](./workflows.md) for workflow basics — creating workflows, input/output/state schemas, request/notification definitions, instance management, and scheduling. This file covers only the step execution surface.

## Table of Contents

- [step() — Named Steps](#step--named-steps)
- [step.request() — Pause for Conversation Data](#steprequest--pause-for-conversation-data)
- [step.notify() — Send Typed Notifications](#stepnotify--send-typed-notifications)
- [step.listen() — Pause Until External Resume](#steplisten--pause-until-external-resume)
- [step.sleep() / step.sleepUntil()](#stepsleep--stepsleepuntil)
- [step.map()](#stepmap)
- [step.forEach()](#stepforeach)
- [step.batch()](#stepbatch)
- [step.executeWorkflow()](#stepexecuteworkflow)
- [step.waitForWorkflow()](#stepwaitforworkflow)
- [step.progress()](#stepprogress)
- [step.fail()](#stepfail)
- [step.abort()](#stepabort)
- [Step Execution Model](#step-execution-model)
- [Patterns](#patterns)
- [Pitfalls](#pitfalls)

---

## step() — Named Steps

The base `step()` function executes a named unit of work with automatic retry, caching, and state persistence.

### Signature

```typescript
step<T>(
  name: string,
  run: ({ attempt }: { attempt: number }) => T | Promise<T>,
  options?: { maxAttempts?: number }
): Promise<T>
```

### Parameters

| Parameter             | Type                               | Default  | Description                                                              |
| --------------------- | ---------------------------------- | -------- | ------------------------------------------------------------------------ |
| `name`                | `string`                           | required | Unique identifier within the workflow. Must be stable across executions. |
| `run`                 | `({ attempt }) => T \| Promise<T>` | required | Function to execute. Receives current attempt number (0-indexed).        |
| `options.maxAttempts` | `number`                           | `5`      | Maximum retry attempts before the step fails permanently.                |

### Behavior

- **Idempotent**: If a step with this name already completed, its cached result is returned immediately.
- **Retries**: On failure, retries with exponential backoff (up to 5s between attempts).
- **Persistence**: Completed step output is serialized and persisted in workflow state. Date objects are automatically serialized/deserialized.
- **Nesting**: Steps can contain other steps. Sub-steps get their own retry scope.

### Examples

```typescript
// Basic step — fetch and cache a value
const user = await step('fetch-user', async () => {
  return await api.getUser(input.userId)
})

// Step with retry awareness
const result = await step(
  'call-api',
  async ({ attempt }) => {
    console.log(`Attempt ${attempt}`)
    return await externalApi.call(input.data)
  },
  { maxAttempts: 3 }
)

// Nested steps — each sub-step is independently retried and cached
const processed = await step('process', async () => {
  const enriched = await step('enrich', async () => {
    return await enrichData(user)
  })
  const validated = await step('validate', async () => {
    return await validateData(enriched)
  })
  return { enriched, validated }
})
```

---

## step.request() — Pause for Conversation Data

Pauses the workflow and asks the linked conversation for typed data. The workflow enters `listening` mode until data is provided via `workflow.provide()`.

### Signature

```typescript
step.request(
  request: string,
  message: string,
  stepName?: string
): Promise<RequestPayload>
```

### Parameters

| Parameter  | Type     | Default                            | Description                                                                   |
| ---------- | -------- | ---------------------------------- | ----------------------------------------------------------------------------- |
| `request`  | `string` | required                           | Name of a request type defined in the workflow's `requests` schema.           |
| `message`  | `string` | required                           | Prompt message sent to the conversation as context.                           |
| `stepName` | `string` | defaults to the value of `request` | Custom step name. Required when the same request type is used multiple times. |

### Behavior

1. Creates a `WorkflowDataRequestEvent` on the conversation with the prompt, step name, and JSON schema.
2. Sets workflow status to `listening`.
3. Aborts the current execution. The workflow is frozen.
4. When `workflow.provide(request, data, stepName?)` is called from the conversation handler, the data is written to the step's output and the workflow resumes.
5. The returned value is validated against the request's Zod schema.

### Conversation-Side Handling

The conversation handler receives a `type === "workflow_request"` event:

```typescript
async handler({ type, request, conversation }) {
  if (type === 'workflow_request') {
    // request.workflow — the workflow instance
    // request.name — the request type name
    // request.step — the step name that is waiting
    // request.prompt — the message string

    // Provide data back to the workflow
    await request.workflow.provide(request.name, userData, request.step)
  }
}
```

### Examples

An IT request workflow — collecting multiple inputs using the same request type with custom step names:

```typescript
export const SoftwareRequestWorkflow = new Workflow({
  name: 'softwareRequest',
  input: z.object({
    requestedBy: z.string(),
    department: z.string(),
  }),
  output: z.object({
    status: z.enum(['approved', 'cancelled']),
    summary: z.string(),
  }),
  requests: {
    text_input: z.string(),
    confirmation: z.boolean(),
  },
  handler: async ({ input, step }) => {
    // Same request type, different step names — required for disambiguation
    const software = await step.request(
      'text_input',
      'Which software or tool do you need access to?',
      'collect-software'
    )

    const justification = await step.request(
      'text_input',
      'Please provide a brief business justification.',
      'collect-justification'
    )

    const manager = await step.request('text_input', 'Who is your manager?', 'collect-manager')

    // Different request type — step name defaults to 'confirmation'
    const confirmed = await step.request('confirmation', `Submit request for ${software}?`)

    if (!confirmed) {
      return { status: 'cancelled', summary: 'Cancelled by user.' }
    }

    const requestId = await step('submit-request', async () => {
      // ... create record ...
      return id
    })

    return { status: 'approved', summary: `Request ${requestId} submitted.` }
  },
})
```

### Step Name Resolution Rules

When `workflow.provide(request, data)` is called without an explicit step name:

1. If exactly one pending step matches the request type, it resolves automatically.
2. If multiple pending steps match, it throws — you must pass the step name explicitly.
3. If no pending step matches, it throws.

Always pass a custom `stepName` when using the same request type more than once.

---

## step.notify() — Send Typed Notifications

Sends a typed notification event to the linked conversation without pausing the workflow.

### Signature

```typescript
step.notify(
  notification: string,
  payload: NotificationPayload,
  stepName?: string
): Promise<void>
```

### Parameters

| Parameter      | Type     | Default                                 | Description                                                                    |
| -------------- | -------- | --------------------------------------- | ------------------------------------------------------------------------------ |
| `notification` | `string` | required                                | Name of a notification defined in the workflow's `notifications` schema.       |
| `payload`      | `object` | required                                | Payload validated against the notification's Zod schema.                       |
| `stepName`     | `string` | defaults to the value of `notification` | Custom step name. Required when emitting the same notification multiple times. |

### Behavior

- Idempotent per step name — re-executing the same step returns cached state.
- Creates a `WorkflowNotifyEvent` on the conversation.
- Does NOT pause the workflow. Execution continues immediately.
- If the workflow has no `conversationId`, the notification is silently skipped (non-fatal).
- Notification delivery failures are logged but do not fail the workflow.

### Examples

A support workflow — streaming progress updates during iteration:

```typescript
export const TicketReviewWorkflow = new Workflow({
  name: 'ticketReview',
  input: z.object({ department: z.string() }),
  output: z.object({ reviewed: z.number(), escalated: z.number(), summary: z.string() }),
  notifications: {
    progress: z.object({
      phase: z.enum(['scanning', 'reviewing', 'complete']),
      reviewed: z.number(),
      total: z.number(),
      message: z.string(),
    }),
  },
  async handler({ input, step }) {
    await step.notify(
      'progress',
      {
        phase: 'scanning',
        reviewed: 0,
        total: 0,
        message: `Scanning tickets for ${input.department}...`,
      },
      'progress-start'
    )

    const tickets = await step('fetch-tickets', async () => {
      /* ... */
    })

    await step.forEach(
      'review-tickets',
      tickets,
      async (ticket, { i }) => {
        // Process ticket...

        // Each notification needs a unique step name
        await step.notify(
          'progress',
          {
            phase: i + 1 >= tickets.length ? 'complete' : 'reviewing',
            reviewed: i + 1,
            total: tickets.length,
            message: `Reviewed ${i + 1} of ${tickets.length}...`,
          },
          `progress-ticket-${i}`
        )
      },
      { concurrency: 1 }
    )

    return { reviewed: tickets.length, escalated: 0, summary: '...' }
  },
})
```

---

## step.listen() — Pause Until External Resume

Puts the workflow into `listening` mode and pauses execution. The workflow will resume when an external event triggers it (e.g., a `WorkflowContinueEvent`).

### Signature

```typescript
step.listen(name: string): Promise<void>
```

### Behavior

- Sets workflow status to `listening`.
- Aborts the current execution.
- On resume, the step is already marked complete and execution continues past it.

Use `step.listen()` when you need a generic pause point that is not tied to a request or sleep timer. For typed data collection, use `step.request()` instead.

Note: When a workflow is in `listening` status, nudge events on the linked conversation are suppressed. See [conversation-lifecycle.md](./conversation-lifecycle.md) for details.

---

## step.sleep() / step.sleepUntil()

Pause workflow execution for a duration or until a specific date.

### Signatures

```typescript
step.sleep(name: string, ms: number): Promise<void>
step.sleepUntil(name: string, date: Date | string): Promise<void>
```

### Behavior

**step.sleep():**

- For delays >= 10 seconds (or when remaining execution time is insufficient): schedules a `WorkflowContinueEvent` with the specified delay, sets status to `listening`, and aborts. The workflow resumes automatically when the timer fires.
- For delays < 10 seconds with sufficient execution time: uses an in-memory `setTimeout`. The workflow stays active.

**step.sleepUntil():**

- Computes `ms = targetDate - now - 10s buffer` and delegates to `step.sleep()`.
- If the date is in the past (or within the 10s buffer), returns immediately.

### Examples

```typescript
// Wait 5 minutes between API calls
await step.sleep('rate-limit-pause', 5 * 60 * 1000)

// Wait until a specific deadline
await step.sleepUntil('wait-for-deadline', new Date('2025-12-31T00:00:00Z'))

// Short delay (stays in-memory, no listening mode)
await step.sleep('brief-pause', 2000)
```

---

## step.map()

Process an array of items in parallel with controlled concurrency, collecting results.

### Signature

```typescript
step.map<T, U>(
  name: string,
  items: T[],
  run: (input: T, opts: { i: number }) => Promise<U>,
  opts?: { maxAttempts?: number; concurrency?: number }
): Promise<U[]>
```

### Parameters

| Parameter          | Type                          | Default  | Description                                                    |
| ------------------ | ----------------------------- | -------- | -------------------------------------------------------------- |
| `name`             | `string`                      | required | Name for the map operation.                                    |
| `items`            | `T[]`                         | required | Array of items to process.                                     |
| `run`              | `(item, { i }) => Promise<U>` | required | Processing function per item. Receives the item and its index. |
| `opts.maxAttempts` | `number`                      | `5`      | Max retries per item.                                          |
| `opts.concurrency` | `number`                      | `1`      | Max parallel item executions.                                  |

### Behavior

- Creates a parent step named `name`, with child steps named `{name}-i0`, `{name}-i1`, etc.
- Each item is processed in its own step with independent retry logic.
- Results are returned in the same order as input items.
- If execution time runs low mid-iteration, the workflow pauses and resumes on next invocation.

### Examples

From the knowledge indexing workflow — syncing data sources in parallel:

```typescript
const workflows = await step.map(
  'index-sources',
  kb.sources,
  async (source) => {
    const workflowId = await step(
      'create-sync-workflow',
      async () =>
        await source.syncWorkflow
          .getOrCreate({
            key: `${kbName}:${source.id}`,
            input: {
              /* ... */
            },
          })
          .then((x) => x.id)
    )
    return await step.waitForWorkflow(source.id, workflowId).then((x) => x.output)
  },
  { concurrency: 10, maxAttempts: 1 }
)
```

From the directory source — deleting files with concurrency:

```typescript
const deleted = await step.map(
  'deleting removed files',
  toRemove,
  (f) =>
    client.deleteFile({ id: f.id }).then(() => ({
      file: f.id,
      name: f.key,
      hash: f.metadata?.hash || '',
      size: f.size ?? -1,
    })),
  { concurrency: 5 }
)
```

---

## step.forEach()

Process an array of items in parallel without collecting results. Identical to `step.map()` but returns `void`.

### Signature

```typescript
step.forEach<T>(
  name: string,
  items: T[],
  run: (input: T, opts: { i: number }) => Promise<void>,
  opts?: { maxAttempts?: number; concurrency?: number }
): Promise<void>
```

Use `step.forEach()` for side-effect-only operations (sending notifications, updating records). If you need the results array, use `step.map()`.

### Examples

A support workflow — reviewing tickets with side effects:

```typescript
await step.forEach(
  'review-tickets',
  tickets,
  async (ticket, { i }) => {
    if (ticket.priority === 'urgent' && ticket.status === 'open') {
      await TicketsTable.updateRows({
        rows: [{ id: ticket.id, status: 'in-progress' }],
      })
    }
  },
  { concurrency: 1 }
)
```

---

## step.batch()

Process an array of items in sequential batches. Items are grouped into fixed-size batches and each batch is processed as a single step.

### Signature

```typescript
step.batch<T>(
  name: string,
  items: T[],
  run: (batch: T[], opts: { i: number }) => Promise<void>,
  opts?: { batchSize?: number; maxAttempts?: number }
): Promise<void>
```

### Parameters

| Parameter          | Type                              | Default  | Description                                              |
| ------------------ | --------------------------------- | -------- | -------------------------------------------------------- |
| `name`             | `string`                          | required | Name for the batch operation.                            |
| `items`            | `T[]`                             | required | Full array of items.                                     |
| `run`              | `(batch, { i }) => Promise<void>` | required | Function receiving a batch slice and the starting index. |
| `opts.batchSize`   | `number`                          | `20`     | Number of items per batch.                               |
| `opts.maxAttempts` | `number`                          | `5`      | Max retries per batch.                                   |

### Behavior

- Creates a parent step named `name`, with child steps named `{name}-b1`, `{name}-b2`, etc. (1-indexed).
- Batches are processed sequentially (no concurrency between batches).
- Each batch gets independent retry logic.

### Examples

```typescript
// Bulk insert records in batches of 100
await step.batch(
  'bulk-insert',
  records,
  async (batch) => {
    await database.bulkInsert(batch)
  },
  { batchSize: 100 }
)
```

### When to Use batch vs map/forEach

| Use              | When                                                 |
| ---------------- | ---------------------------------------------------- |
| `step.batch()`   | External API accepts arrays (bulk insert, batch API) |
| `step.map()`     | Need individual results per item, want concurrency   |
| `step.forEach()` | Side effects per item, want concurrency              |

---

## step.executeWorkflow()

Start a child workflow and wait for it to complete, returning its output. Convenience wrapper around `workflow.getOrCreate()` + `step.waitForWorkflow()`.

### Signature

```typescript
step.executeWorkflow<TName, TInput, TOutput>(
  name: string,
  workflow: BaseWorkflow<TName, TInput, TOutput>,
  input?: z.infer<TInput>
): Promise<z.infer<TOutput>>
```

### Behavior

1. Generates a unique key (via `ulid()`) to ensure idempotent child workflow creation.
2. Calls `workflow.getOrCreate()` with that key.
3. Waits for the child workflow to complete via `step.waitForWorkflow()`.
4. Returns the child workflow's output.

Internally creates three sub-steps: `{name}-key`, `{name}-start`, `{name}-wait`.

### Examples

```typescript
const result = await step.executeWorkflow('run-analysis', AnalysisWorkflow, { data: input.rawData })
// result is typed as AnalysisWorkflow's output
```

---

## step.waitForWorkflow()

Wait for another workflow (by ID) to complete before continuing.

### Signature

```typescript
step.waitForWorkflow(
  name: string,
  workflowId: string
): Promise<Workflow>
```

### Behavior

- Polls the target workflow's status.
- If the target is finished (`completed`, `failed`, `cancelled`, `timedout`), returns the workflow object immediately.
- If still running, sets the current workflow to `listening` mode and restarts the step on next invocation.
- Throws if you try to wait for the same workflow (deadlock prevention).

### Examples

```typescript
// Start a child workflow manually, then wait
const child = await ChildWorkflow.getOrCreate({
  key: `child-${input.id}`,
  input: { data: input.data },
})

const finished = await step.waitForWorkflow('wait-for-child', child.id)

if (finished.status === 'completed') {
  const output = finished.output as ChildOutput
  // ...
}
```

---

## step.progress()

Record a named checkpoint without performing any action. Useful for tracking workflow execution stages.

### Signature

```typescript
step.progress(name: string): Promise<void>
```

### Behavior

- Creates a step with no output and `maxAttempts: 1`.
- The step is visible in the workflow's execution state for audit and debugging.

### Examples

```typescript
await step.progress('started-processing')
// ... do work ...
await step.progress('finished-processing')
```

---

## step.fail()

Mark the workflow as failed with a reason and stop execution immediately.

### Signature

```typescript
step.fail(reason: string): Promise<void>
```

### Behavior

- Sets the workflow's internal failed flag with the given reason.
- Creates a step named after the reason string (with `maxAttempts: 1`).
- Execution halts — code after `step.fail()` is never reached.
- The workflow status becomes `failed`.

### Examples

```typescript
if (!user.isVerified) {
  await step.fail('User verification required')
  // never reached
}
```

> `step.fail()` vs `workflow.fail()`: Both mark the workflow as failed. `step.fail()` is available on the step object. `workflow.fail()` is available on the workflow instance parameter. They achieve the same result. Prefer whichever is already in scope.

---

## step.abort()

Immediately stop workflow execution without marking it as failed.

### Signature

```typescript
step.abort(): void  // note: synchronous, throws immediately
```

### Behavior

- Sets the workflow's internal aborted flag.
- Throws a step signal to halt execution.
- The workflow remains in its current status and can be resumed later.
- This is NOT `step.fail()` — it does not mark the workflow as failed.

### Examples

```typescript
if (shouldPauseForLater) {
  step.abort()
  // never reached
}
```

---

## Step Execution Model

### Caching and Idempotency

Every step is identified by its name. When a workflow resumes:

1. Steps that already have a `finishedAt` timestamp return their cached output immediately.
2. Steps that failed with `maxAttemptsReached` re-throw their stored error.
3. Only steps that haven't completed yet actually execute their `run` function.

This means step functions can contain non-idempotent operations (API calls, database writes) and still be safe across workflow restarts — each operation runs exactly once.

### Retry Logic

Failed steps retry with exponential backoff: `min(100ms * e^attempt, 5000ms)`. After `maxAttempts` failures, the step is permanently marked as failed with the error stored in state. The error then propagates to the parent step or workflow.

### Execution Time Management

The runtime monitors remaining execution time. If less than 10 seconds remain:

- New steps will not start.
- The workflow enters a brief sleep and then aborts.
- On next invocation, execution resumes from the last incomplete step.

This prevents cascading timeout failures and ensures clean state persistence.

---

## Patterns

### Multi-Turn Data Collection (Request/Provide Cycle)

The most common multi-step pattern: workflow requests data, conversation collects it from the user, provides it back, and the workflow resumes.

```typescript
// Workflow side
export const OnboardingWorkflow = new Workflow({
  name: 'onboarding',
  requests: {
    user_input: z.string(),
    selection: z.enum(['optionA', 'optionB']),
  },
  handler: async ({ step }) => {
    const name = await step.request('user_input', 'What is your name?', 'collect-name')
    const choice = await step.request('selection', 'Pick an option:')
    return { name, choice }
  },
})

// Conversation side
export const Chat = new Conversation({
  channel: 'chat.channel',
  async handler({ type, request, conversation, message }) {
    if (type === 'workflow_request') {
      await conversation.send({ type: 'text', payload: { text: request.prompt } })
      // ... collect user's response ...
      await request.workflow.provide(request.name, userResponse, request.step)
    }
  },
})
```

### Fan-Out with Progress Notifications

Process items in parallel while streaming progress updates to the conversation:

```typescript
export const BulkProcessWorkflow = new Workflow({
  name: 'bulkProcess',
  notifications: {
    status: z.object({ processed: z.number(), total: z.number() }),
  },
  handler: async ({ input, step }) => {
    const items = await step('fetch-items', async () => {
      /* ... */
    })

    await step.forEach(
      'process',
      items,
      async (item, { i }) => {
        await processItem(item)
        await step.notify(
          'status',
          {
            processed: i + 1,
            total: items.length,
          },
          `status-${i}`
        )
      },
      { concurrency: 5 }
    )

    return { total: items.length }
  },
})
```

### Child Workflow Orchestration

Start multiple child workflows and wait for all of them:

```typescript
handler: async ({ input, step }) => {
  const results = await step.map(
    'run-children',
    input.tasks,
    async (task) => {
      return await step.executeWorkflow(`child-${task.id}`, ChildWorkflow, { data: task.data })
    },
    { concurrency: 3 }
  )
  return { results }
}
```

---

## Pitfalls

### Step names must be unique and stable

Every step in a workflow must have a unique name that does not change between executions. Dynamic step names break resume behavior.

```typescript
// WRONG — dynamic names break on resume if items change
for (const item of items) {
  await step(`process-${item.id}`, async () => {
    /* ... */
  })
}

// CORRECT — use step.map() or step.forEach() for iteration
await step.map('process-items', items, async (item) => {
  /* ... */
})
```

### step.request() needs custom stepName for repeated types

If you call `step.request()` with the same request type more than once, you MUST provide a unique `stepName`. Otherwise the provide call cannot disambiguate which step to fill.

```typescript
// WRONG — both use 'text_input' as implicit step name
const name = await step.request('text_input', 'Your name?')
const email = await step.request('text_input', 'Your email?') // conflicts!

// CORRECT — explicit step names
const name = await step.request('text_input', 'Your name?', 'collect-name')
const email = await step.request('text_input', 'Your email?', 'collect-email')
```

### step.notify() inside loops needs unique step names

Since `step.notify()` is idempotent per step name, calling it in a loop with the same step name only sends the first notification.

```typescript
// WRONG — only sends one notification
for (const item of items) {
  await step.notify('progress', { item: item.name }) // same step name each time
}

// CORRECT — unique step name per iteration
await step.forEach('process', items, async (item, { i }) => {
  await step.notify('progress', { item: item.name }, `progress-${i}`)
})
```

### step.abort() is synchronous

`step.abort()` throws immediately — it does not return a promise. Any code after it is unreachable.

```typescript
step.abort()
console.log('never printed') // unreachable
```

### step.fail() reason string becomes the step name

The `reason` argument to `step.fail()` is used as the step name. Keep it descriptive but avoid characters that would be problematic as identifiers.

### Avoid heavy computation outside steps

All work inside a workflow handler should be wrapped in steps. Code between steps runs on every resume but produces no cached state, wasting execution time.

```typescript
// WRONG — this runs on every resume
const processed = heavyComputation(input.data)
await step('use-result', async () => {
  /* ... */
})

// CORRECT — wrap in a step
const processed = await step('compute', async () => {
  return heavyComputation(input.data)
})
```

### step.sleep() threshold: 10 seconds

Sleeps under 10 seconds use in-memory `setTimeout` (workflow stays active). Sleeps of 10 seconds or more enter `listening` mode (workflow pauses and resumes via scheduled event). Plan accordingly — a 9-second sleep ties up the execution context, while a 10-second sleep frees it.

---

## See Also

- [Workflows](./workflows.md) — Workflow basics, input/output schemas, request/notification definitions
- [Conversations](./conversations.md) — Conversation-side handling of workflow requests and notifications
- [Autonomous Execution](./autonomous-execution.md) — Using execute() inside workflow handlers (worker mode)
- [Conversation Lifecycle](./conversation-lifecycle.md) — Nudge suppression during active workflow steps
