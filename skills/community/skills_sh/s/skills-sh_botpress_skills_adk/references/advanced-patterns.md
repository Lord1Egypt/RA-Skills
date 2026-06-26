# Advanced Patterns

Production-ready patterns for building sophisticated ADK agents with guardrails, authentication, observability, and modular architecture.

## Pattern 1: Guardrails

Enforce behavioral constraints on autonomous agents to prevent unwanted actions and ensure data validation.

### Use Cases

- Ensure knowledge search before answering questions
- Validate preconditions before executing actions (e.g., credit checks before purchases)
- Prevent hallucinations by enforcing data lookup

### Implementation

```typescript
// src/conversations/extensions/guardrails.ts
import { adk, Autonomous } from '@botpress/runtime'

export const makeGuardrails = (message: any) => {
  // Use zai to determine if knowledge search is needed
  const isKnowledgeSearchAsync = adk.zai.check(message, `Is this a question that requires knowledge search?`)

  let hasSearched = false

  const onBeforeToolGuard: Autonomous.Hooks['onBeforeTool'] = async ({ iteration, tool, input, controller }) => {
    if (tool.name === 'search_knowledge') {
      hasSearched = true
    }

    const isKnowledgeSearch = await isKnowledgeSearchAsync

    if (tool.name === 'Message' && isKnowledgeSearch && !hasSearched) {
      throw new Error(`Knowledge search is required for this question. Please use "search_knowledge" first.`)
    }
  }

  return { onBeforeToolGuard }
}
```

> **Note:** `adk.zai.check()` is the recommended approach for AI-powered validation. An advanced pattern `adk.zai.learn().check()` exists for cached/reusable checks, but `adk.zai.check()` is simpler and covers most cases. See [zai-agent-reference.md](./zai-agent-reference.md) for all Zai operations and edge cases.

### Usage in Conversation

```typescript
// src/conversations/webchat.ts
import { Conversation } from '@botpress/runtime'
import { makeGuardrails } from './extensions/guardrails'

export default new Conversation({
  channel: '*',
  handler: async ({ execute, message }) => {
    const guardrail = makeGuardrails(message)

    await execute({
      instructions: `You are a helpful assistant...`,
      hooks: {
        onBeforeTool: async (props) => guardrail.onBeforeToolGuard(props),
      },
    })
  },
})
```

### Variations

**Credit Check Guardrail:**

```typescript
export const makeCreditCheckGuardrail = () => {
  let creditChecked = false

  const onBeforeToolGuard: Autonomous.Hooks['onBeforeTool'] = async ({ iteration, tool, input, controller }) => {
    if (tool.name === 'check_credit') {
      creditChecked = true
    }
    if (tool.name === 'process_payment' && !creditChecked) {
      throw new Error('Credit check must be performed before processing payment')
    }
  }

  return { onBeforeToolGuard }
}
```

**Data Validation Guardrail:**

```typescript
export const makeDataValidationGuardrail = () => {
  const onBeforeToolGuard: Autonomous.Hooks['onBeforeTool'] = async ({ iteration, tool, input, controller }) => {
    if (tool.name === 'send_email') {
      const hasValidEmail = await adk.zai.check(input, 'Does this contain a valid email address?')
      if (!hasValidEmail) {
        throw new Error('Invalid email address provided')
      }
    }
  }

  return { onBeforeToolGuard }
}
```

### Key Techniques

1. **Async Validation**: Use `adk.zai.check()` for AI-powered validation
2. **State Tracking**: Track actions with closure variables (`hasSearched`)
3. **Hook Interception**: Use `onBeforeTool` to intercept and validate tool calls
4. **Error Throwing**: Throw errors to prevent unwanted tool execution

---

## Pattern 2: Admin Mode

Implement privileged access control with temporary authentication for administrative functions.

### Use Cases

- Knowledge base re-indexing
- Agent configuration changes
- Debugging tools for support teams
- System maintenance operations

### Implementation

```typescript
// src/conversations/extensions/admin-mode.ts
import { adk, Autonomous, context, user, z } from '@botpress/runtime'

// Define user state schema for admin mode
export const AdminModeUserSchema: z.ZodRawShape = {
  admin: z
    .object({
      adminUtil: z.string().nullable().describe('Expiration date of admin status (ISO).'),
      code: z.string().nullable().describe('The admin access code.'),
      codeValidUntil: z.string().nullable().describe('Expiration date of admin code (ISO).'),
    })
    .default({ adminUtil: null, code: null, codeValidUntil: null }),
}

// Admin-only tool: refresh knowledge bases
const getIndexKnowledgeBasesTool = () => {
  const ctx = context.getAll()
  return new Autonomous.Tool({
    name: 'refreshKnowledgeBases',
    description: 'Refresh and re-index all knowledge bases.',
    output: z.string().describe('Confirmation message after refreshing.'),
    handler: async () => {
      context.enterWith(ctx) // Restore context for async operations
      await Promise.all(adk.project.knowledge.map((kb) => kb.refresh()))
      return `Started re-indexing: ${adk.project.knowledge.map((kb) => kb.name).join(', ')}`
    },
  })
}

// Generate one-time login code
const getLoginTool = () => {
  const ctx = context.getAll()
  user.state ??= {}

  const CODE_VALIDITY_DURATION_MS = 5 * 60 * 1000 // 5 minutes

  const expectedCode = user.state.admin?.code?.toLowerCase().trim()
  const codeGenerated =
    expectedCode && user.state.admin?.codeValidUntil && new Date(user.state.admin?.codeValidUntil) > new Date()

  if (codeGenerated) {
    return new Autonomous.Tool({
      name: 'loginWithCode',
      description: 'Log in as admin using an access code.',
      input: z.string().describe('The admin access code, e.g. "ABC346"'),
      output: z.boolean().describe('Returns true if login is successful.'),
      handler: async (code: string) => {
        context.enterWith(ctx)
        const providedCode = code.toLowerCase().trim()

        if (expectedCode && providedCode === expectedCode) {
          user.state.admin = {
            adminUtil: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
            code: null,
            codeValidUntil: null,
          }
          return true
        }

        throw new Autonomous.ThinkSignal('Invalid or expired admin access code')
      },
    })
  }

  return new Autonomous.Tool({
    name: 'generateLoginCode',
    description: 'Generate a one-time access code for admin login.',
    handler: async () => {
      context.enterWith(ctx)
      const generatedCode = Math.random().toString(36).substring(2, 8).toUpperCase()

      user.state.admin = {
        adminUtil: null,
        code: generatedCode,
        codeValidUntil: new Date(Date.now() + CODE_VALIDITY_DURATION_MS).toISOString(),
      }

      console.log(`Generated admin login code: ${generatedCode}`)

      throw new Autonomous.ThinkSignal(
        `An admin login code has been generated and logged in the developer console. Retrieve it from the Botpress dashboard.`
      )
    },
  })
}

function isUserAdmin() {
  return user.state.admin?.adminUtil && new Date(user.state.admin.adminUtil) > new Date()
}

export const getAdminModeObject = () =>
  new Autonomous.Object({
    name: 'admin',
    description: getAdminStatus(), // Dynamic description based on state
    tools: isUserAdmin() ? [getIndexKnowledgeBasesTool()] : [getLoginTool()],
  })
```

### Configuration in agent.config.ts

```typescript
import { z, defineConfig } from '@botpress/runtime'
import { AdminModeUserSchema } from './src/conversations/extensions/admin-mode'

export default defineConfig({
  name: 'my-agent',
  user: {
    state: z.object({}).extend(AdminModeUserSchema),
  },
})
```

### Usage in Conversation

```typescript
import { Conversation } from '@botpress/runtime'
import { getAdminModeObject } from './extensions/admin-mode'

export default new Conversation({
  channel: '*',
  handler: async ({ execute }) => {
    await execute({
      instructions: `You are a helpful assistant...`,
      objects: [getAdminModeObject()],
    })
  },
})
```

### Key Techniques

1. **Dynamic Tools**: Tools change based on authentication state
2. **Time-Based Auth**: Expiration timestamps for codes and sessions (codes: 5 min, sessions: 1 hour)
3. **Context Restoration**: `context.enterWith()` for async operations
4. **Think Signals**: Use `Autonomous.ThinkSignal` to control agent reasoning flow
5. **Console Logging**: Log codes for secure out-of-band delivery (not shown in chat)

---

## Pattern 3: Logging & Observability

Comprehensive logging and error tracking for production agents.

### Basic Trace Logging

```typescript
// src/conversations/extensions/logging.ts
import { Autonomous } from '@botpress/runtime'

export const onTraceLogging: Autonomous.Hooks['onTrace'] = ({ trace, iteration }) => {
  if (trace.type === 'code_execution_exception') {
    console.error(`Code Execution Error: ${trace.message}`, trace.stackTrace)
  }

  if (trace.type === 'tool_call' && !trace.success) {
    console.error(
      `Error during tool call to "${trace.tool_name}" with input "${JSON.stringify(trace.input)}":`,
      trace.error
    )
  }
}
```

### Usage in Conversation

```typescript
import { Conversation } from '@botpress/runtime'
import { onTraceLogging } from './extensions/logging'

export default new Conversation({
  channel: '*',
  handler: async ({ execute }) => {
    await execute({
      instructions: `You are a helpful assistant...`,
      hooks: {
        onTrace: (props) => onTraceLogging!(props),
      },
    })
  },
})
```

### Advanced: Comprehensive Trace Logging

```typescript
export const onTraceLogging: Autonomous.Hooks['onTrace'] = ({ trace, iteration }) => {
  switch (trace.type) {
    case 'code_execution_exception':
      console.error(`[CODE ERROR] ${trace.message}`, trace.stackTrace)
      break
    case 'tool_call':
      if (trace.success) {
        console.log(`[TOOL SUCCESS] ${trace.tool_name}`, trace.output)
      } else {
        console.error(`[TOOL ERROR] ${trace.tool_name}`, trace.error)
      }
      break
    case 'think':
      console.debug(`[THINK] ${trace.content}`)
      break
    default:
      console.log(`[TRACE] ${trace.type}`, trace)
  }
}
```

### Advanced: Performance Monitoring

```typescript
export const makePerformanceMonitor = () => {
  const startTime = Date.now()
  const toolMetrics = new Map<string, number[]>()

  const onBeforeTool: Autonomous.Hooks['onBeforeTool'] = async ({ iteration, tool, input, controller }) => {
    ;(tool as any)._startTime = Date.now()
  }

  const onAfterTool: Autonomous.Hooks['onAfterTool'] = async ({ tool, output }) => {
    const duration = Date.now() - ((tool as any)._startTime || 0)
    const metrics = toolMetrics.get(tool.name) || []
    metrics.push(duration)
    toolMetrics.set(tool.name, metrics)
    console.log(`[PERF] ${tool.name}: ${duration}ms`)
  }

  const onTrace: Autonomous.Hooks['onTrace'] = ({ trace, iteration }) => {
    if (trace.type === 'end') {
      console.log(`[PERF] Total conversation: ${Date.now() - startTime}ms`)
      console.log(`[PERF] Tool metrics:`, Object.fromEntries(toolMetrics))
    }
  }

  return { onBeforeTool, onAfterTool, onTrace }
}
```

### Hook Signatures Reference

| Hook           | Parameters                               | Description                 |
| -------------- | ---------------------------------------- | --------------------------- |
| `onBeforeTool` | `{ iteration, tool, input, controller }` | Fires before each tool call |
| `onAfterTool`  | `{ tool, output }`                       | Fires after each tool call  |
| `onTrace`      | `{ trace, iteration }`                   | Fires on every trace event  |

---

## Pattern 4: Extension Composition

Combine multiple extensions into a cohesive agent architecture.

```typescript
// src/conversations/webchat.ts
import { Conversation } from '@botpress/runtime'
import { WebsiteKB } from '../knowledge/website-docs'
import { getAdminModeObject } from './extensions/admin-mode'
import { makeGuardrails } from './extensions/guardrails'
import { onTraceLogging } from './extensions/logging'

export default new Conversation({
  channel: '*',
  handler: async ({ execute, message }) => {
    const guardrail = makeGuardrails(message)

    await execute({
      instructions: `You are a helpful assistant that provides accurate information.`,
      knowledge: [WebsiteKB],
      objects: [getAdminModeObject()],
      hooks: {
        onBeforeTool: async (props) => guardrail.onBeforeToolGuard(props),
        onTrace: (props) => onTraceLogging!(props),
      },
    })
  },
})
```

### Architecture

```
Conversation Handler
├── Instructions (system prompt)
├── Knowledge (RAG knowledge bases)
├── Objects (admin mode, custom tool groups)
└── Hooks
    ├── onBeforeTool (guardrails, validation)
    ├── onAfterTool (logging, cleanup)
    └── onTrace (monitoring, debugging)
```

### Multi-Extension Composition

```typescript
import { makeGuardrails } from './extensions/guardrails'
import { onTraceLogging } from './extensions/logging'
import { makePerformanceMonitor } from './extensions/performance'

export default new Conversation({
  channel: '*',
  handler: async ({ execute, message }) => {
    const guardrail = makeGuardrails(message)
    const perfMonitor = makePerformanceMonitor()

    await execute({
      instructions: `You are a documentation assistant. Always search before answering.`,
      knowledge: [DocsKB],
      objects: [getAdminModeObject()],
      hooks: {
        onBeforeTool: async (props) => {
          await guardrail.onBeforeToolGuard(props)
          await perfMonitor.onBeforeTool(props)
        },
        onAfterTool: async (props) => {
          await perfMonitor.onAfterTool(props)
        },
        onTrace: (props) => {
          onTraceLogging!(props)
          perfMonitor.onTrace(props)
        },
      },
    })
  },
})
```

### Best Practices

1. **Modular Extensions**: Separate files per concern (`guardrails.ts`, `logging.ts`, `admin-mode.ts`)
2. **Factory Functions**: Export factory functions for flexibility
3. **Hook Composition**: Combine multiple hooks in `execute()`
4. **Type-Safe Hooks**: Always type hooks via `Autonomous.Hooks["hookName"]`

```
src/conversations/
├── webchat.ts              # Main conversation handler
└── extensions/
    ├── admin-mode.ts       # Admin authentication
    ├── guardrails.ts       # Behavioral constraints
    ├── logging.ts          # Observability
    └── performance.ts      # Performance monitoring
```

---

## Pattern 5: Context Management

Properly manage async context in tool handlers and workflows.

### Problem

Tool handlers run in async contexts where the ADK runtime context (`user`, `conversation`, `client`) is not automatically available.

### Solution

Use `context.enterWith()` to restore context in async handlers:

```typescript
import { context, Autonomous } from "@botpress/runtime";

const myTool = () => {
  const ctx = context.getAll(); // Capture context at tool creation

  return new Autonomous.Tool({
    name: "myTool",
    handler: async () => {
      context.enterWith(ctx); // Restore context in async handler
      const userId = user.id;
      await client.createMessage({ ... });
    },
  });
};
```

### When to Use

- Tool handlers that access `user`, `conversation`, `client`
- Async operations within tools
- Long-running operations
- Workflows that spawn async tasks

> **Note:** Context reassignment should always use `context.enterWith()`. Do not use `context.set("key", value)` to reassign the full context — `enterWith()` atomically restores the entire context snapshot.

### Common Pitfalls

```typescript
// ❌ BAD - Context not available
handler: async () => {
  await client.createMessage({ ... }); // Error: client not available
};

// ✅ GOOD - Restore context first
const ctx = context.getAll();
handler: async () => {
  context.enterWith(ctx);
  await client.createMessage({ ... });
};
```

---

## Pattern 6: Shared Schema

Centralize Zod schemas to ensure consistency across Actions, Tables, Workflows, and validation logic.

### Central Schema Definition

```typescript
// src/schemas.ts
import { z } from '@botpress/runtime'

export type User = z.infer<typeof UserSchema>
export const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string().optional(),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
  createdAt: z.string().describe('ISO 8601 timestamp'),
})
```

### Reuse Across Components

**In Actions:**

```typescript
import { Action } from '@botpress/runtime'
import { UserSchema } from '../schemas'

export const GetUser = new Action({
  name: 'getUser',
  input: z.object({ userId: z.string() }),
  output: UserSchema,
  handler: async ({ input }) => {
    return await fetchUserFromAPI(input.userId)
  },
})
```

**In Tables:**

```typescript
import { Table } from '@botpress/runtime'
import { UserSchema } from '../schemas'

export const UsersTable = new Table({
  name: 'UsersTable',
  description: 'Store user information',
  columns: {
    email: { schema: UserSchema.shape.email, searchable: true },
    name: { schema: UserSchema.shape.name, searchable: true },
  },
})
```

**In Workflows:**

```typescript
import { Workflow } from '@botpress/runtime'
import { UserSchema, ConversationSchema } from '../schemas'

export const ProcessUser = new Workflow({
  name: 'processUser',
  input: z.object({ user: UserSchema, conversationId: z.string() }),
  state: z.object({ conversation: ConversationSchema.optional() }),
  handler: async ({ input, state, step }) => {
    console.log(`Processing user: ${input.user.email}`)
    return { userId: input.user.id }
  },
})
```

### Schema Composition

```typescript
// Base schema
export const BaseEntitySchema = z.object({
  id: z.string(),
  createdAt: z.string(),
  updatedAt: z.string(),
})

// Extend
export const ConversationSchema = BaseEntitySchema.extend({
  userId: z.string(),
  status: z.enum(['open', 'closed', 'snoozed']),
})

// Pick / Omit
export const UserSummarySchema = UserSchema.pick({ id: true, email: true, name: true })
export const PublicUserSchema = UserSchema.omit({ metadata: true })
```

### Best Practices

- Organize schemas by domain (`src/schemas/users.ts`, `src/schemas/conversations.ts`)
- Export both types and schemas (`export type User = z.infer<typeof UserSchema>`)
- Add `.describe()` annotations for documentation
- Use `.extend()`, `.pick()`, `.omit()` to build variations without duplication

---

## See Also

- [./actions.md](./actions.md) — Actions reference
- [./conversations.md](./conversations.md) — Conversation handlers
- [./workflows.md](./workflows.md) — Workflow patterns
- [./tools.md](./tools.md) — Tools reference
- [./context-api.md](./context-api.md) — Context API details
- [./agent-config.md](./agent-config.md) — Configuration reference
- [./zai-complete-guide.md](./zai-complete-guide.md) — Zai validation guide
