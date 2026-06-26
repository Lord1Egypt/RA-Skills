# Context API Reference

Access runtime services like the Botpress client and citations manager within your ADK handlers.

## Quick Start

```typescript
import { context } from '@botpress/runtime'

// Get Botpress client
const client = context.get('client')

// Get citations manager
const citations = context.get('citations')

// Use services
const { passages } = await client.searchFiles({
  query: 'search term',
  withContext: true,
})
```

## Overview

The `context` API provides access to runtime services within your ADK handlers (actions, tools, workflows, conversations, triggers). The ADK automatically sets up context for you - you just need to call `context.get()` to access services.

**Available in:**

- Action handlers
- Tool handlers
- Workflow handlers
- Conversation handlers
- Trigger handlers

## Primary Context Keys

These are the context keys you'll commonly use as an ADK developer:

### client

The Botpress API client for your bot. Use this to interact with Botpress services like files, tables, messages, etc.

```typescript
const client = context.get('client')

// Search files/knowledge base
const { passages } = await client.searchFiles({
  query: 'search query',
  tags: { type: 'knowledge' },
  withContext: true,
})

// Create message
await client.createMessage({
  conversationId,
  type: 'text',
  payload: { text: 'Hello!' },
})

// Query tables (low-level client API)
const { rows } = await client.tables.findMany({
  table: 'users',
  filter: { email: { eq: 'user@example.com' } },
})
```

> **Note:** For table operations, prefer using the direct Table class methods (e.g., `UsersTable.findRows()`) over `client.tables.*`. The Table class provides better type safety and a cleaner API. See [Tables documentation](./tables.md) for details.

**Type:** `BotSpecificClient<TBot>`

### citations

Citation manager for tracking sources in AI responses. Essential for RAG implementations.

```typescript
const citations = context.get('citations')

// Register a source
const { tag } = citations.registerSource({
  url: 'https://docs.example.com/page',
  title: 'Documentation Page',
  favicon: 'https://docs.example.com/favicon.ico',
})

// Use in response
const response = `According to the documentation${tag}, the answer is...`
```

**Type:** `CitationsManager`

See **[Knowledge Bases](./knowledge-bases.md)** for complete citation examples with RAG.

## Optional Context Keys

These keys may or may not be available depending on the handler context. Always use `{ optional: true }` when accessing them.

### user

Current user object (available in conversation handlers).

```typescript
const user = context.get('user', { optional: true })

if (user) {
  console.log(user.id)
  console.log(user.name)
  console.log(user.tags)
}
```

**Type:** `User | null`

### conversation

Current conversation object. Available optionally in Actions, Tools, and Triggers when they are invoked within a conversation context.

> **Note:** In `Conversation` handlers, the `conversation` object is already provided as a handler parameter — use that directly instead of `context.get("conversation")`.

```typescript
// In Actions, Tools, or Triggers — use context.get() with { optional: true }
const conversation = context.get('conversation', { optional: true })

if (conversation) {
  console.log(conversation.id)
  console.log(conversation.tags)
}

// In Conversation handlers — use the handler parameter directly
// async handler({ conversation }) { ... }
```

**Type:** `Conversation | null`

> Tools and Actions **cannot send messages** — the `conversation` here is read-only (no `.send()`). Return data from the Tool/Action and let the `Conversation` handler send it.

### message

Incoming message (when triggered by a message event).

```typescript
const message = context.get('message', { optional: true })

if (message?.type === 'text') {
  console.log(message.payload.text)
}
```

**Type:** `AnyIncomingMessage<TBot> | null`

### event

Incoming event (available in trigger handlers).

```typescript
const event = context.get('event', { optional: true })

if (event) {
  console.log(`Event type: ${event.type}`)
  console.log(event.payload)
}
```

**Type:** `AnyIncomingEvent<TBot> | null`

See **[Triggers](./triggers.md)** for event handling examples.

### workflow

Current workflow instance (available in workflow handlers).

```typescript
const workflow = context.get('workflow', { optional: true })

if (workflow) {
  console.log(`Workflow ID: ${workflow.id}`)
  console.log(`Conversation ID: ${workflow.conversationId}`)
}
```

**Type:** `Workflow | null`

See **[Workflows](./workflows.md)** for workflow context examples.

### workflowControlContext

Workflow control operations (available in workflow handlers).

```typescript
const control = context.get('workflowControlContext', { optional: true })

if (control) {
  // Access workflow controls
  await control.ack()
  control.complete({ result: 'success' })
}
```

**Type:** `WorkflowControlContext | null`

### chat

Chat instance for accessing conversation transcripts (available in conversation handlers).

```typescript
const chat = context.get('chat', { optional: true })

if (chat) {
  // Fetch conversation transcript
  const transcript = await chat.fetchTranscript()
  console.log(`Messages: ${transcript.length}`)
}
```

**Type:** `BotpressChat | null`

See **[Conversations](./conversations.md)** for chat context examples.

## Less Common Keys

These are available but less frequently needed:

### cognitive

AI model client for direct LLM operations. Most of the time you'll use `execute()` instead.

```typescript
const cognitive = context.get('cognitive')

const response = await cognitive.generateText({
  model: 'openai:gpt-4o',
  messages: [{ role: 'user', content: 'Hello' }],
})
```

**Type:** `Cognitive`

**Note:** Usually you'll use `execute()` for AI interactions rather than calling cognitive directly.

### logger

Structured logger for the current bot.

```typescript
const logger = context.get('logger')

logger.info('Processing request')
logger.error('Failed to process', { error })
logger.debug('Debug info', { data })
```

**Type:** `BotLogger`

### botId

Current bot identifier.

```typescript
const botId = context.get('botId')
console.log(`Running in bot: ${botId}`)
```

**Type:** `string`

## Using context.get()

### Basic Syntax

```typescript
context.get<T extends keyof BotContext>(
  key: T,
  opts?: { optional?: boolean }
): Required<BotContext>[T]
```

### Required Keys

```typescript
// Will throw if not available (use for keys that should always exist)
const client = context.get('client')
const citations = context.get('citations')
```

### Optional Keys

```typescript
// Returns null if not available (use for conditional keys)
const user = context.get('user', { optional: true })
const conversation = context.get('conversation', { optional: true })

if (user && conversation) {
  // Both available
} else {
  // Handle missing context
}
```

## Common Patterns

### Conditional User Context

```typescript
export const myAction = new Action({
  async handler({ input }) {
    const client = context.get('client')
    const user = context.get('user', { optional: true })

    if (user) {
      // Personalized response
      console.log(`Processing for user ${user.id}`)
    } else {
      // Generic response
      console.log('Processing without user context')
    }

    return await client.doSomething()
  },
})
```

### Using Context Across Handler Types

The `context.get()` syntax is identical across all handler types (Actions, Tools, Workflows, Conversations, Triggers):

```typescript
// Same pattern everywhere
const client = context.get('client')
const citations = context.get('citations')
const user = context.get('user', { optional: true })
```

See individual documentation for handler-specific examples: **[Actions](./actions.md)**, **[Tools](./tools.md)**, **[Workflows](./workflows.md)**, **[Conversations](./conversations.md)**.

## Error Handling

### Required Keys

```typescript
// ❌ WRONG - Will throw if key doesn't exist
try {
  const user = context.get('user')
} catch (error) {
  // Hard to handle gracefully
}

// ✅ CORRECT - Use optional for conditional keys
const user = context.get('user', { optional: true })
if (!user) {
  console.log('No user context available')
  return defaultResponse
}
```

### Always-Available Keys

Keys like `client`, `citations` should always be available. If they're not, it's a framework error:

```typescript
// These should never throw in normal operation
const client = context.get('client')
const citations = context.get('citations')
```

## Best Practices

### 1. Know Which Keys Are Always Available

**Always available:**

- `client` - Botpress API client
- `citations` - Citation manager
- `cognitive` - AI model client
- `logger` - Structured logger
- `botId` - Current bot ID
  **Conditionally available (use `{ optional: true }`):**
- `user` - Only in conversation context
- `conversation` - Only in conversation context
- `message` - Only when triggered by message
- `event` - Only in trigger handlers
- `workflow` - Only in workflow handlers
- `workflowControlContext` - Only in workflow handlers
- `chat` - Only in conversation handlers

### 2. Access Context at Call Time

```typescript
// ✅ GOOD - Get context when needed
export const myAction = new Action({
  async handler({ input }) {
    const client = context.get('client') // Get when you need it
    const result = await client.searchFiles({ query: input.query })
    return result
  },
})

// ❌ BAD - Don't store context globally
let globalClient // Don't do this!

export const badAction = new Action({
  async handler({ input }) {
    globalClient = context.get('client') // Context might change
  },
})
```

### 3. Use TypeScript's Type Safety

```typescript
// TypeScript knows the types
const client = context.get('client')
// client is typed as BotSpecificClient<TBot>

const user = context.get('user', { optional: true })
// user is typed as User | null
```

## Direct Imports vs Context API

For `bot`, `user`, and `adk`, you can use direct imports instead of `context.get()`:

```typescript
import { bot, user, adk } from '@botpress/runtime'

bot.state.version // Instead of context.get("bot").state
user.state.preferredLanguage // Instead of context.get("user").state
```

See **[Actions](./actions.md)** for comparison of both approaches.

## Troubleshooting

### "Context key not found" Error

```typescript
// Error: Context key "user" not found
const user = context.get('user')
```

**Solution:** Use `{ optional: true }` for conditional keys:

```typescript
const user = context.get('user', { optional: true })
```

### "Cannot read property of undefined"

```typescript
// Error: Cannot read property 'id' of undefined
const userId = context.get('user', { optional: true }).id
```

**Solution:** Check if key exists before accessing properties:

```typescript
const user = context.get('user', { optional: true })
if (user) {
  const userId = user.id
}
```

## See Also

- **[Actions](./actions.md)** - Using context in actions
- **[Tools](./tools.md)** - Using context in tools
- **[Integration Actions](./integration-actions.md)** - Using the client for integration actions
- **[Workflows](./workflows.md)** - Workflow context
- **[Conversations](./conversations.md)** - Conversation context
- **[Knowledge Bases](./knowledge-bases.md)** - Using citations for RAG
