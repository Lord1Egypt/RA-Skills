# Autonomous Execution

The `execute()` function is the core of AI-powered behavior in ADK bots. It runs a code-generating LLM in a sandboxed loop: the model writes TypeScript, the runtime executes it, and the loop continues until an exit is reached or iterations are exhausted.

This reference covers **Objects, Exits, execution hooks, and configuration options**. For basic tool definition and handler patterns, see [tools.md](./tools.md).

## execute() Full API

`execute()` is provided as a parameter in conversation handlers and is also available in workflows. It accepts these properties:

```typescript
type Props = {
  /** System prompt guiding the LLM. Can be static or dynamic per iteration. */
  instructions: string | ((ctx: Context) => string | Promise<string>)

  /** AI-callable tools. See tools.md for creation patterns. */
  tools?: Tool[] | ((ctx: Context) => Tool[] | Promise<Tool[]>)

  /** Namespaced objects with properties and scoped tools. */
  objects?: Object[] | ((ctx: Context) => Object[] | Promise<Object[]>)

  /** Structured termination points. Controls how execution ends. */
  exits?: Exit[] | ((ctx: Context) => Exit[] | Promise<Exit[]>)

  /** Execution lifecycle hooks. */
  hooks?: Hooks

  /** LLM temperature (0-2). Default: 0.7 */
  temperature?: number | ((ctx: Context) => number | Promise<number>)

  /** Model or fallback chain. Uses agent config default if omitted. */
  model?: Model | Model[] | ((ctx: Context) => Model | Model[] | Promise<Model | Model[]>)

  /** Reasoning effort for models that support it. */
  reasoningEffort?: 'low' | 'medium' | 'high' | 'dynamic' | 'none'

  /** Knowledge bases for RAG. Adds a search_knowledge tool automatically. */
  knowledge?: BaseKnowledge[]

  /** Maximum iteration loops. Default: 10. Clamped to 1-100. */
  iterations?: number

  /** AbortSignal to cancel execution externally. */
  signal?: AbortSignal
}
```

Every property except `instructions` is optional. Most properties accept a **ValueOrGetter** — either a static value or a function receiving the current execution context that returns the value (optionally async). This lets you change tools, objects, or instructions between iterations based on what happened previously.

## Exits

Exits define the structured ways an execution can terminate. The LLM ends execution by writing `return { action: 'exit_name', ...data }` in its generated code.

### Creating Exits

```typescript
import { Autonomous, z } from '@botpress/runtime'

// Simple exit (no data)
const Done = new Autonomous.Exit({
  name: 'done',
  description: 'Task is complete',
})

// Exit with typed data
const TriageComplete = new Autonomous.Exit({
  name: 'triage_complete',
  description: 'Classification is done and the user has been notified.',
  schema: z.object({
    category: z.string().describe('The category the request was classified as'),
  }),
})

// Exit with aliases
const Escalate = new Autonomous.Exit({
  name: 'escalate',
  aliases: ['transfer', 'handoff'],
  description: 'Escalate to a human agent',
  schema: z.object({
    reason: z.enum(['frustrated', 'technical', 'sensitive', 'other']),
    priority: z.enum(['low', 'medium', 'high']).default('medium'),
  }),
})

// Exit with metadata for orchestration
const Handoff = new Autonomous.Exit({
  name: 'handoff_sales',
  description: 'Transfer to sales team',
  metadata: { department: 'sales', type: 'handoff' },
  schema: z.object({ reason: z.string() }),
})
```

### Exit Constructor

```typescript
new Autonomous.Exit<T>({
  name: string              // Required. Valid TypeScript identifier.
  description: string       // Required. Tells the LLM when to use this exit.
  schema?: ZuiType<T>       // Optional. Zod schema for validated return data.
  aliases?: string[]        // Optional. Alternative names the LLM can use.
  metadata?: Record<string, unknown>  // Optional. Custom data for orchestration.
})
```

### Using Exits in execute()

```typescript
export const SlackDM = new Conversation({
  channel: 'slack.dm',

  async handler({ execute }) {
    const result = await execute({
      instructions: `Classify the user's request, tell them the result, then exit.`,
      tools: [classifyRequest.asTool()],
      exits: [TriageComplete],
    })

    // Type-safe result checking
    if (result.is(TriageComplete)) {
      console.log(`Triaged as: ${result.output.category}`)
    }
  },
})
```

### Multiple Exits for Branching

```typescript
const Approved = new Autonomous.Exit({
  name: 'approved',
  description: 'Loan application approved',
  schema: z.object({ amount: z.number(), reference: z.string() }),
})

const Rejected = new Autonomous.Exit({
  name: 'rejected',
  description: 'Loan application rejected',
  schema: z.object({ reason: z.string() }),
})

const result = await execute({
  instructions: 'Review and decide on the loan application.',
  tools: [creditCheckTool, reviewTool],
  exits: [Approved, Rejected],
})

if (result.is(Approved)) {
  console.log(`Approved: $${result.output.amount} (ref: ${result.output.reference})`)
} else if (result.is(Rejected)) {
  console.log(`Rejected: ${result.output.reason}`)
}
```

### Built-in Exits

Three exits are built into the runtime. Do not redefine them.

| Exit            | When Available                             | Action Name | Purpose                                                                                            |
| --------------- | ------------------------------------------ | ----------- | -------------------------------------------------------------------------------------------------- |
| **ListenExit**  | Chat mode (conversation handlers)          | `listen`    | Pauses execution, returns control to the user. Auto-added when `execute()` runs in a conversation. |
| **ThinkExit**   | Always                                     | `think`     | LLM pauses to reflect. Triggers another iteration (does not end execution).                        |
| **DefaultExit** | Worker mode, when no custom exits provided | `done`      | Returns `{ success: true, result? }` or `{ success: false, error }`.                               |

```typescript
import { Autonomous } from '@botpress/runtime'

// Check for built-in exits
if (result.is(Autonomous.ListenExit)) {
  // Agent is waiting for user input
}

if (result.is(Autonomous.DefaultExit)) {
  if (result.output.success) {
    console.log('Result:', result.output.result)
  } else {
    console.error('Error:', result.output.error)
  }
}
```

**Chat mode behavior**: In conversation handlers, `ListenExit` is added automatically. When no custom exits are provided the LLM will use `ListenExit` to hand control back after responding. When you provide custom exits, both your exits and `ListenExit` are available.

**Worker mode behavior**: When `execute()` runs without a chat context (e.g. in a workflow or standalone), `ListenExit` is not available. If no custom exits are provided, `DefaultExit` is added automatically.

### Exit Utilities

```typescript
// Clone and rename an exit
const customExit = baseExit.clone().rename('custom')

// Deduplicate exit names
const uniqueExits = Autonomous.Exit.withUniqueNames([exit1, exit2])

// Match an exit result
if (someExit.match(exitResult)) {
  // exitResult is typed as ExitResult<T>
}
```

## Objects

Objects group related properties and tools into a namespace. The LLM sees them as TypeScript namespaces with typed constants and methods.

### Creating Objects

```typescript
import { Autonomous, z } from '@botpress/runtime'

const userProfile = new Autonomous.Object({
  name: 'user',
  description: 'Current user profile data',
  properties: [
    {
      name: 'name',
      value: 'John Doe',
      type: z.string().min(1),
      description: 'User full name',
      writable: true,
    },
    {
      name: 'email',
      value: null,
      type: z.string().email().nullable(),
      description: 'User email address',
      writable: true,
    },
    {
      name: 'id',
      value: 'user_123',
      writable: false, // Read-only — LLM cannot modify
    },
  ],
})
```

The LLM sees this as:

```typescript
export namespace user {
  const name: Writable<string> = 'John Doe'
  const email: Writable<string | null> = null
  const id: Readonly<string> = 'user_123'
}
```

### Object Constructor

```typescript
new Autonomous.Object({
  name: string                    // Required. Valid TypeScript identifier.
  description?: string            // What this object represents.
  properties?: ObjectProperty[]   // Stateful variables (max 100).
  tools?: Tool[]                  // Scoped tools (called as obj.toolName()).
  metadata?: Record<string, unknown>
})
```

### ObjectProperty

```typescript
type ObjectProperty = {
  name: string // Valid TypeScript identifier.
  value: any // Current value.
  type?: ZuiType // Zod schema for validation on write.
  description?: string // Helps the LLM understand the property.
  writable?: boolean // Default: false. If true, LLM can assign new values.
}
```

### Objects with Scoped Tools

Tools on an object are called as `objectName.toolName()` by the LLM:

```typescript
const fileSystem = new Autonomous.Object({
  name: 'fs',
  description: 'File system operations',
  tools: [
    new Autonomous.Tool({
      name: 'readFile',
      input: z.object({ path: z.string() }),
      output: z.string(),
      handler: async ({ path }) => readFileSync(path, 'utf8'),
    }),
    new Autonomous.Tool({
      name: 'writeFile',
      input: z.object({ path: z.string(), content: z.string() }),
      handler: async ({ path, content }) => writeFileSync(path, content),
    }),
  ],
})

// LLM can call: fs.readFile({ path: '/tmp/data.txt' })
// LLM can call: fs.writeFile({ path: '/tmp/out.txt', content: '...' })
```

### Dynamic Objects

Pass a function instead of an array to rebuild objects each iteration, reflecting current state:

```typescript
const memory: Record<string, any> = {}

await execute({
  instructions: 'Collect user information.',
  objects: () => [
    new Autonomous.Object({
      name: 'form',
      properties: [
        {
          name: 'name',
          value: memory.name ?? null,
          type: z.string().nullable(),
          writable: true,
        },
        {
          name: 'age',
          value: memory.age ?? null,
          type: z.number().min(0).max(150).nullable(),
          writable: true,
        },
      ],
    }),
  ],
  hooks: {
    onTrace: ({ trace }) => {
      if (trace.type === 'property') {
        memory[trace.property] = trace.value
      }
    },
  },
})
```

### Using Objects in execute()

```typescript
await execute({
  instructions: 'You have access to the user profile. Update fields as needed.',
  objects: [userProfile],
  tools: [saveProfileTool],
})
```

## Execution Hooks

Hooks let you observe and modify the execution loop. They are passed in the `hooks` property of `execute()`.

### Hook Reference

```typescript
type Hooks = {
  /** NON-BLOCKING. Called for each trace (log, tool call, LLM call, etc). */
  onTrace?: (props: { trace: Trace; iteration: number }) => void

  /** BLOCKING. Called before each iteration. Can modify iteration parameters. */
  onIterationStart?: (
    iteration: Iteration,
    controller: AbortController,
    context: Context
  ) => Promise<void | Partial<Iteration>> | void | Partial<Iteration>

  /** BLOCKING. Called after each iteration. Good for logging and cleanup. */
  onIterationEnd?: (iteration: Iteration, controller: IterationController) => void | Promise<void>

  /** BLOCKING. Called when an exit is reached. Throw to reject the exit. */
  onExit?: <T = unknown>(result: ExitResult<T>) => Promise<void> | void

  /** BLOCKING, MUTATION. Called after LLM generates code, before execution. */
  onBeforeExecution?: (iteration: Iteration, controller: AbortController) => Promise<{ code?: string } | void>

  /** BLOCKING, MUTATION. Called before any tool executes. Can modify input. */
  onBeforeTool?: (event: {
    iteration: Iteration
    tool: Tool
    input: unknown
    controller: AbortController
  }) => Promise<{ input?: unknown } | void>

  /** BLOCKING, MUTATION. Called after a tool executes. Can modify output. */
  onAfterTool?: (event: {
    iteration: Iteration
    tool: Tool
    input: unknown
    output: unknown
    controller: AbortController
  }) => Promise<{ output?: unknown } | void>
}
```

### Hook Categories

| Category                   | Hooks                                                                  | Behavior                                              |
| -------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------- |
| **Non-blocking**           | `onTrace`                                                              | Fire-and-forget. Cannot delay execution.              |
| **Blocking, mutation**     | `onIterationStart`, `onBeforeTool`, `onAfterTool`, `onBeforeExecution` | Block until resolved. Can return modified values.     |
| **Blocking, non-mutation** | `onIterationEnd`, `onExit`                                             | Block until resolved. Cannot change tool I/O or code. |

### Common Hook Patterns

**Logging tool calls:**

```typescript
await execute({
  instructions: 'Help the user',
  tools: [searchTool, ticketTool],
  hooks: {
    onBeforeTool: async ({ tool, input }) => {
      console.log(`[tool:start] ${tool.name}`, JSON.stringify(input))
    },
    onAfterTool: async ({ tool, input, output }) => {
      console.log(`[tool:end] ${tool.name}`, JSON.stringify(output))
    },
  },
})
```

**Modifying tool input (e.g. appending search scope):**

```typescript
hooks: {
  onBeforeTool: async ({ tool, input }) => {
    if (tool.name === 'search') {
      return { input: { ...input, query: `${input.query} site:docs.example.com` } }
    }
  },
}
```

**Rejecting an exit (forces the LLM to keep iterating):**

```typescript
hooks: {
  onExit: async (result) => {
    if (result.exit.name === 'done' && !result.result?.confirmed) {
      throw new Error('Must confirm before exiting')
    }
  },
}
```

**Aborting execution from a hook:**

```typescript
hooks: {
  onBeforeTool: async ({ controller }) => {
    if (shouldStop()) {
      controller.abort()
    }
  },
}
```

**Modifying generated code before execution:**

```typescript
hooks: {
  onBeforeExecution: async (iteration) => {
    // Inject a safety wrapper or strip dangerous patterns
    const modified = iteration.code?.replace(/dangerousCall\(\)/g, '/* blocked */')
    return { code: modified }
  },
}
```

**Tracking property mutations via onTrace:**

```typescript
hooks: {
  onTrace: ({ trace }) => {
    if (trace.type === 'property') {
      console.log(`${trace.object}.${trace.property} = ${trace.value}`)
    }
  },
}
```

## Execution Result

`execute()` returns an `ExecutionResult` with three possible statuses:

```typescript
const result = await execute({ instructions: '...' })

// Status checks
result.isSuccess() // Completed with an exit
result.isError() // Failed (aborted, iterations exhausted)
result.isInterrupted() // Paused with a snapshot (SnapshotSignal)

// Exit type-narrowing
result.is(MyExit) // true if exited via MyExit, narrows result.output type

// Access execution data
result.iteration // Last iteration (or null)
result.iterations // All iterations
result.output // Exit data (if success), null otherwise
result.context // Full execution context
```

### Success Result

```typescript
if (result.isSuccess()) {
  console.log('Exit:', result.result.exit.name)
  console.log('Output:', result.output)
  console.log('Code:', result.iteration.code)
}

// Typed exit checking (preferred)
if (result.is(TriageComplete)) {
  // result.output is typed as { category: string }
  console.log(result.output.category)
}
```

### Error Result

```typescript
if (result.isError()) {
  console.error('Failed:', result.error)
  // Inspect the last iteration for details
  const last = result.iteration
  if (last?.status.type === 'execution_error') {
    console.error(last.status.execution_error.message)
  }
}
```

### Interrupted Result (Snapshots)

When a tool throws `SnapshotSignal`, execution pauses and can be resumed later:

```typescript
if (result.isInterrupted()) {
  const snapshot = result.snapshot.toJSON()
  // Persist snapshot, resume later with: execute({ snapshot, ... })
}
```

## Configuration Options

### Model Selection

```typescript
await execute({
  instructions: '...',
  model: 'openai:gpt-4o', // Single model
})

await execute({
  instructions: '...',
  model: ['openai:gpt-4o', 'anthropic:claude-3-5-sonnet'], // Fallback chain
})

// Dynamic model per iteration
await execute({
  instructions: '...',
  model: (ctx) => (ctx.iteration > 2 ? 'openai:gpt-4o' : 'openai:gpt-4o-mini'),
})
```

If `model` is omitted, the `defaultModels.autonomous` value from `agent.config.ts` is used.

### Temperature

```typescript
await execute({
  instructions: '...',
  temperature: 0.1, // Low = deterministic. Default: 0.7. Range: 0-2.
})
```

### Reasoning Effort

```typescript
await execute({
  instructions: '...',
  reasoningEffort: 'high', // 'none' | 'low' | 'medium' | 'high' | 'dynamic'
})
```

- `'none'` disables reasoning for models with optional reasoning.
- `'dynamic'` lets the provider decide.
- Omitting this field disables reasoning for optional-reasoning models.

### Iteration Limit

```typescript
await execute({
  instructions: '...',
  iterations: 20, // Default: 10. Clamped to 1-100.
})
```

Each "iteration" is one LLM generation + code execution cycle. The LLM can call multiple tools in a single iteration. `ThinkExit` consumes one iteration. If iterations are exhausted without an exit, the result is an error.

### AbortSignal

```typescript
const controller = new AbortController()
setTimeout(() => controller.abort(), 30_000)

await execute({
  instructions: '...',
  signal: controller.signal,
})
```

When aborted, the current LLM generation and sandbox execution are killed immediately. The result status will be `error` with an aborted iteration.

## Dynamic Properties (ValueOrGetter)

Most `execute()` properties accept either a static value or a function that receives the execution context:

```typescript
// Static
tools: [searchTool, ticketTool]

// Dynamic — re-evaluated each iteration
tools: (ctx) => {
  if (ctx.iteration > 0) {
    return [searchTool, ticketTool, escalateTool]
  }
  return [searchTool]
}

// Async dynamic
instructions: async (ctx) => {
  const rules = await fetchRules()
  return `Follow these rules: ${rules}`
}
```

This pattern applies to `instructions`, `tools`, `objects`, `exits`, `temperature`, and `model`.

## Chat Mode vs Worker Mode

`execute()` behaves differently depending on where it runs:

| Aspect          | Chat Mode (Conversations)          | Worker Mode (Workflows, Actions)     |
| --------------- | ---------------------------------- | ------------------------------------ |
| Transcript      | LLM sees conversation history      | No transcript                        |
| ListenExit      | Auto-added                         | Not available                        |
| DefaultExit     | Not auto-added when exits provided | Auto-added when no exits provided    |
| Components      | Can yield UI components            | No component rendering               |
| Typical pattern | Open-ended conversation            | Task completion with structured exit |

In conversation handlers, `execute()` is provided as a parameter and runs in chat mode by default:

```typescript
export const Chat = new Conversation({
  channel: 'chat.channel',
  async handler({ execute }) {
    await execute({
      instructions: 'You are a helpful assistant.',
      tools: [searchTool],
    })
    // After execute(), the LLM used ListenExit to return control
  },
})
```

For lifecycle event handling (nudge/expire) in conversations, see [conversation-lifecycle.md](./conversation-lifecycle.md).

## Common Patterns

### Classify-and-exit (single-shot)

```typescript
const Category = new Autonomous.Exit({
  name: 'categorized',
  description: 'Message has been categorized',
  schema: z.object({
    category: z.enum(['billing', 'technical', 'general']),
    confidence: z.number().min(0).max(1),
  }),
})

const result = await execute({
  instructions: 'Classify the user message into a category.',
  exits: [Category],
  iterations: 3,
})

if (result.is(Category)) {
  await routeToTeam(result.output.category)
}
```

### Chaining execute() calls

```typescript
async handler({ execute }) {
  // First pass: classify
  const result = await execute({
    instructions: 'Classify the request and respond.',
    tools: [classifyTool],
    exits: [TriageComplete],
  })

  // Second pass: follow-up
  if (result.is(TriageComplete) && result.output.category === 'technical') {
    await execute({
      instructions: 'Ask for technical details and create a ticket.',
      tools: [createTicketTool],
    })
  }
}
```

### Open-ended conversation (no custom exits)

```typescript
await execute({
  instructions: 'You are an IT help desk assistant.',
  tools: [createTicket, lookupTicket, updateTicket, deleteTicket],
  knowledge: [DocsKB],
})
// LLM uses ListenExit to return control after each response
```

## Pitfalls

- **Do not redefine built-in exits.** Creating an exit named `listen`, `think`, or `done` will conflict with the built-in ListenExit, ThinkExit, and DefaultExit.
- **Exits require good descriptions.** The LLM decides which exit to use based on the `description`. Vague descriptions lead to wrong exit selection.
- **Writable properties need a schema.** If `writable: true` without `type`, the sandbox cannot validate writes and they will be unchecked.
- **Object property limit is 100.** More than 100 properties on a single object will throw.
- **ThinkExit consumes an iteration.** If your iteration limit is low and the LLM thinks frequently, it may exhaust iterations before finishing. Increase `iterations` for complex tasks.
- **Blocking hooks delay execution.** All hooks except `onTrace` are async and block the loop. Keep hook logic fast.
- **onExit throw = retry.** Throwing in `onExit` rejects the exit and the LLM gets the error as context for the next iteration. Use this deliberately.

## See Also

- [Tools](./tools.md) — Tool creation, handler syntax, ThinkSignal, advanced properties
- [Conversations](./conversations.md) — Conversation handlers, message routing, channel IDs
- [Workflows](./workflows.md) — Long-running processes, step-based execution
- [Context API](./context-api.md) — Accessing runtime services and state
- [Model Configuration](./model-configuration.md) — Model selection and defaults
- [Workflow Steps](./workflow-steps.md) — Step API reference for using execute() within workflow handlers
- [Conversation Lifecycle](./conversation-lifecycle.md) — Lifecycle events (nudge/expire) that also receive execute as a handler prop
