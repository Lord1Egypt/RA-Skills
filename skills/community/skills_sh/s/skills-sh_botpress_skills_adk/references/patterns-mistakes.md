# Patterns & Common Mistakes

Common patterns to follow and mistakes to avoid when building with the ADK.

## Common Mistakes

### Import Errors

#### Wrong Import Sources

```typescript
// ❌ WRONG - Never import from these
import { z } from 'zod'
import { Action } from '@botpress/sdk'
import { Workflow } from '@botpress/cli'

// ✅ CORRECT - Always import from @botpress/runtime
import { z, Action, Workflow, Conversation } from '@botpress/runtime'
```

**Why this matters:**

- `z` from `@botpress/runtime` is Botpress's internal fork of Zod (based on Zod 3.x)
- Importing from `zod` directly can cause compatibility issues
- ADK primitives (Action, Tool, Workflow, etc.) must come from `@botpress/runtime`

**Zod Version Compatibility Note:**
Botpress uses Zod 3.x internally. If adding `zod` to your project dependencies (e.g., for frontend code), use version `3.23.8` or compatible 3.x. Zod 4.x has breaking changes and is NOT compatible with the ADK.

#### Dynamic Imports

```typescript
// ❌ AVOID - Dynamic imports can cause issues
const { myAction } = await import('./actions/myAction')

// ✅ PREFER - Static imports
import { myAction } from './actions/myAction'
```

### Shipping a bundled data file

To ship a data table your code reads at runtime (menu, catalog, pricing rules), **import the JSON statically** — the bundler inlines it into the build:

```typescript
import menu from './data/menu.json' // ✅ inlined at build time
```

Don't reach for `fs.readFile` (the file isn't on disk at runtime → ENOENT), `import.meta`/`fileURLToPath` (undefined in the bundle → throws), or `assets.get()` (returns a URL, not the file's contents). All three pass `adk check` and `tsc` but crash only at runtime.

### Handler Syntax

#### Action Handlers

Action handlers receive a props object with `input` and `client`. Both arrow functions and method syntax work fine — the handler type is `(props: ActionHandlerProps) => Promise<...>`.

```typescript
// ✅ CORRECT - Method syntax
export const myAction = new Action({
  async handler({ input }) {
    return { data: input.userId }
  },
})

// ✅ ALSO CORRECT - Arrow function syntax
export const myAction = new Action({
  handler: async ({ input }) => {
    return { data: input.userId }
  },
})
```

#### Tool Handlers

```typescript
// ✅ Tools use arrow functions
export const myTool = new Autonomous.Tool({
  handler: async ({ query, limit }) => {
    return searchResults
  },
})
```

### Event Handling Mistakes

#### Receiving a pushed event — subscribe to `chat:custom`, not a made-up name

An event pushed into a conversation (e.g. an order shipped, a status update relayed in) arrives as `chat:custom`. A handler subscribed to a domain-specific name never fires.

```typescript
// ❌ WRONG - pushed event is chat:custom, so this never fires
events: ['claimUpdate'],

// ✅ CORRECT - branch on type === 'event', read event.payload.payload
events: ['chat:custom'],
```

The camelCase rule applies only to events you define/emit, not to receiving. See [conversations.md → Custom & Proactive Events](./conversations.md#custom--proactive-events).

### Conversation Routing Mistakes

#### Don't hand-roll natural-language parsing

Keyword/regex/exact-string matching on what a user types misses real phrasings, so whole flows silently fail. Route natural language to `execute()`; reserve exact-string branching for explicit slash-commands and structured event `type`s.

```typescript
// ❌ WRONG - misses "can you sum this up?", "tl;dr", ...
if (message?.payload.text.includes('summarize')) {
  /* ... */
}

// ✅ CORRECT - the model interprets intent; extract fields with zai
await execute({ instructions: 'Summarize the conversation for the user' })
```

### State Management Mistakes

#### Conversation State Access

Conversations receive `state` as a destructured handler parameter. Do **not** use `this.state`.

```typescript
// ❌ WRONG - this.state does not exist
export const Chat = new Conversation({
  state: z.object({ count: z.number().default(0) }),
  async handler({ message }) {
    this.state.count += 1 // ❌ Wrong!
  },
})

// ✅ CORRECT - Use the state parameter
export const Chat = new Conversation({
  state: z.object({ count: z.number().default(0) }),
  handler: async ({ message, state }) => {
    state.count += 1 // ✅ Destructured from handler props
  },
})
```

#### State Reference vs Value

```typescript
// ❌ WRONG - Passing state reference to async function
handler: async ({ step, state }) => {
  const results = await processItems(state.items)
  // state.items may have changed while processItems was running
  state.items.push('new-item') // processItems might see this!
}

// ✅ CORRECT - Pass a copy of the value
handler: async ({ step, state }) => {
  const itemsCopy = [...state.items]
  const results = await processItems(itemsCopy)
  state.items.push('new-item') // safe, doesn't affect processItems
}

// ✅ CORRECT - Extract values before async operation
handler: async ({ step, state }) => {
  const currentCount = state.count // Primitive - safe
  const currentItems = [...state.items] // Array - needs spread
  const currentConfig = { ...state.config } // Object - needs spread

  await step('process', async () => {
    return await processData(currentCount, currentItems, currentConfig)
  })
}
```

**Rules of thumb:**

- **Primitives** (string, number, boolean): Can pass directly
- **Arrays**: Use spread `[...state.items]` or `Array.from()`
- **Objects**: Use spread `{ ...state.config }` or `structuredClone()`
- **Deep objects**: Use `JSON.parse(JSON.stringify())` or `structuredClone()`

### Workflow Step Mistakes

#### Dynamic Step Names

```typescript
// ❌ WRONG - Dynamic step names break resume
for (let i = 0; i < items.length; i++) {
  await step(`process-${i}`, async () => {
    await processItem(items[i])
  })
}

// ✅ CORRECT - Single step with loop
await step('process-all', async () => {
  for (const item of items) {
    await processItem(item)
  }
})

// ✅ CORRECT - Or use step.map
await step.map('process-items', items, async (item) => {
  return processItem(item)
})
```

#### Missing Await on Steps

```typescript
// ❌ WRONG - Missing await
const result = step('fetch', async () => {
  return fetchData()
})

// ✅ CORRECT - Always await steps
const result = await step('fetch', async () => {
  return fetchData()
})
```

### Table Column Mistakes

#### Searchable Column Syntax

```typescript
// ❌ WRONG - .searchable() is not a Zod method
columns: {
  content: z.string().searchable()
}

// ✅ CORRECT - Object notation for searchable
columns: {
  content: {
    schema: z.string(),
    searchable: true,
  },
}
```

### Conversation ID Mistakes

```typescript
// ❌ WRONG - Missing conversationId prevents communication
await MyWorkflow.start({
  userId: user.id,
  data: 'some data',
})

// ✅ CORRECT - Include conversationId for messaging
await MyWorkflow.start({
  conversationId: conversation.id,
  userId: user.id,
  data: 'some data',
})
```

---

## Common Patterns

### Workflow Request Pattern

Request data from user during workflow execution:

```typescript
export const MyWorkflow = new Workflow({
  name: 'interactive',
  requests: {
    topic: z.object({ topic: z.string() }),
  },
  handler: async ({ step, input }) => {
    const { topic } = await step.request('topic', 'What is the topic of the question?')
    console.log(`Topic identified: ${topic}`)
  },
})
```

### RAG with Citations

Use citations to track sources for AI-generated responses:

```typescript
import { Autonomous, context } from '@botpress/runtime'

const SearchTool = new Autonomous.Tool({
  name: 'search',
  input: z.string(),
  output: z.string(),
  handler: async (query) => {
    const client = context.get('client')
    const citations = context.get('citations')

    const { passages } = await client.searchFiles({
      query,
      tags: { type: 'knowledge', kb: ['myKB'] },
    })

    const message = ['Here are the search results:']
    const { tag: example } = citations.registerSource({})

    for (const p of passages) {
      const { tag } = citations.registerSource({ file: p.file.key })
      message.push(`<${tag} file="${p.file.key}">`)
      message.push(`**${p.file.tags.title}**`)
      message.push(p.content)
      message.push(`</${tag}>`)
    }

    throw new Autonomous.ThinkSignal(
      `When answering, MUST add inline citations (eg: "The price is $10${example} ...")`,
      message.join('\n')
    )
  },
})
```

### Context Access Patterns

The context API provides access to runtime services within handlers.

#### Basic Context Usage

```typescript
import { context } from '@botpress/runtime'

export const myAction = new Action({
  handler: async ({ input }) => {
    const client = context.get('client')
    const cognitive = context.get('cognitive')
    const logger = context.get('logger')

    const { passages } = await client.searchFiles({ query: input.query })
    logger.info('Search completed', { resultCount: passages.length })
    return { results: passages }
  },
})
```

#### Optional Context Keys

```typescript
export const myAction = new Action({
  handler: async ({ input }) => {
    const user = context.get('user', { optional: true })
    const conversation = context.get('conversation', { optional: true })

    if (user && conversation) {
      console.log(`User ${user.id} in conversation ${conversation.id}`)
    } else {
      console.log('Processing without user context')
    }
  },
})
```

#### Common Context Keys

**Always Available:**

- `client` — Botpress API client
- `cognitive` — AI model client
- `logger` — Structured logger
- `botId` — Current bot ID
- `configuration` — Bot configuration
- `runtime` — Runtime environment info

**Conditionally Available:**

- `user` — Current user (in conversation handlers)
- `conversation` — Current conversation (in conversation handlers, not to be used within a conversation object: use the `conversation` parameter instead)
- `message` — Incoming message (when triggered by message)
- `event` — Incoming event (when triggered by event)
- `workflow` — Current workflow (in workflow handlers)
- `integrations` — Installed integrations

#### Context in Different Handler Types

| Handler           | Key context keys                                                       |
| ----------------- | ---------------------------------------------------------------------- |
| **Actions**       | `client`, `cognitive`, `logger`, `botId`, `configuration`              |
| **Tools**         | `client`, `cognitive`, `citations`, `logger`, `user`?, `conversation`? |
| **Workflows**     | `client`, `workflow`, `workflowControlContext`, `logger`               |
| **Conversations** | `client`, `user`, `conversation`, `message`, `event`?, `logger`        |
| **Triggers**      | `client`, `event`, `logger`                                            |

---

## File Naming Conventions

```
// Actions: camelCase
src/actions/fetchUser.ts
src/actions/validateOrder.ts

// Tools: camelCase
src/tools/searchDocs.ts
src/tools/createTicket.ts

// Workflows: camelCase
src/workflows/onboardUser.ts
src/workflows/processPayment.ts

// Tables: PascalCase
src/tables/Users.ts
src/tables/Orders.ts
src/tables/AuditLog.ts

// Conversations: camelCase (prefer lowercase)
src/conversations/chat.ts
src/conversations/slack.ts

// Triggers: camelCase (prefer lowercase)
src/triggers/userCreated.ts
src/triggers/linear.ts

// Knowledge: descriptive
src/knowledge/documentation.md
src/knowledge/policies/privacy.md
```

### Export Naming

```typescript
// Actions
export const fetchUser = new Action({ name: 'fetchUser' })

// Workflows
export const OnboardingWorkflow = new Workflow({ name: 'onboarding' })

// Tables
export const UsersTable = new Table({ name: 'users' })

// Conversations
export const Chat = new Conversation({ channel: 'chat.channel' })

// Triggers - use default export
export default new Trigger({ name: 'userEvents' })
```

---

## Best Practices Summary

### DO's

1. Import from `@botpress/runtime`
2. Use `state` parameter in conversation handlers (not `this.state`)
3. Pass state values by copy, not reference
4. Use stable step names in workflows
5. Always await step functions
6. Pass `conversationId` to workflows that communicate
7. Use object notation for searchable columns
8. Provide defaults in state schemas
9. Handle errors gracefully
10. Prefer parameter destructuring in handlers when available

### DON'Ts

1. Don't import from `zod` or `@botpress/sdk` directly
2. Don't use `this.state` in conversations (use the `state` parameter)
3. Don't pass state references to async functions (copy arrays/objects)
4. Don't use dynamic step names
5. Don't forget to await steps
6. Don't start workflows without `conversationId` if they need to message
7. Don't use `.searchable()` chain notation
8. Don't hardcode secrets in configuration
9. Don't use dynamic imports unless necessary

---

## Debugging Tips

### Check Imports

```bash
# Find incorrect imports
grep -r "from \"zod\"" src/
grep -r "from \"@botpress/sdk\"" src/
```

### Debug State Access

```typescript
// In conversations - use state parameter
handler: async ({ state }) => {
  console.log('Conversation state:', JSON.stringify(state, null, 2))
}

// In workflows - use state parameter
handler: async ({ state }) => {
  console.log('Workflow state:', JSON.stringify(state, null, 2))
}
```

### Trace Workflow Steps

```typescript
handler: async ({ step }) => {
  console.log('Starting workflow')

  const result = await step('step1', async () => {
    console.log('Executing step1')
    return 'data'
  })

  console.log('Step1 result:', result)
}
```

---

## See Also

- [./actions.md](./actions.md) — Action handler reference
- [./conversations.md](./conversations.md) — Conversation handlers
- [./workflows.md](./workflows.md) — Workflow patterns
- [./tables.md](./tables.md) — Table column syntax
- [./context-api.md](./context-api.md) — Context API details
- [./advanced-patterns.md](./advanced-patterns.md) — Guardrails, admin auth, observability
