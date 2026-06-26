# Tools

Tools are functions that AI models can call during conversations to perform actions, retrieve information, or interact with external systems based on user requests.

## Overview

Tools enable you to:

- Give AI capabilities like searching, creating records, sending messages
- Perform actions autonomously based on conversation context
- Access external APIs and integrations
- Retrieve and process data for the AI to use
- Guide AI behavior with signals and structured outputs

## File Location

- **Location**: `src/tools/*.ts`
- **Auto-registration**: Available to AI via the `execute()` function
- **Export pattern**: Both `export const` and `export default` work
  - **`export const`** (Recommended): Enables direct imports and passing to `execute()` as tools
  - **`export default`**: Simpler for single-tool files

## Basic Tool Structure

```typescript
import { Autonomous, z } from '@botpress/runtime'

// Option 1: Named export (recommended)
export const searchDocs = new Autonomous.Tool({
  name: 'searchDocs',
  description: 'Search documentation for answers to user questions',

  input: z.object({
    query: z.string().describe('The search query'),
    maxResults: z.number().default(5).describe('Maximum results to return'),
  }),

  output: z.string(),

  handler: async ({ query, maxResults }) => {
    const results = await searchDocumentation(query, maxResults)
    return results.join('\n\n')
  },
})

// Option 2: Default export (also valid)
export default new Autonomous.Tool({
  name: 'searchDocs',
  // ... same configuration
})
```

**Why use `export const`?**

- Enables direct imports: `import { searchDocs } from "./tools/searchDocs"`
- Can pass directly to `execute()`: `tools: [searchDocs]`
- Better for tool composition and reusability

> A `Tool`/`Autonomous.Tool` is already a tool — pass it directly (`tools: [myTool]`). Do **not** call `.asTool()` on it; `.asTool()` only adapts an **Action** into a tool.

## Tool Properties

| Property              | Type                  | Required    | Description                                              |
| --------------------- | --------------------- | ----------- | -------------------------------------------------------- |
| **name**              | `string`              | Yes         | Unique TypeScript-compatible identifier                  |
| **description**       | `string`              | Recommended | Helps AI understand when and how to use the tool         |
| **input**             | `z.ZodType`           | No          | Zod schema for input validation (defaults to `z.any()`)  |
| **output**            | `z.ZodType`           | No          | Zod schema for output validation (defaults to `z.any()`) |
| **handler**           | `function`            | Yes         | Async function implementing tool logic                   |
| **aliases**           | `string[]`            | No          | Alternative names the AI can use to call this tool       |
| **metadata**          | `Record<string, any>` | No          | Custom information for tool categorization               |
| **staticInputValues** | `object`              | No          | Pre-set parameter values                                 |
| **retry**             | `function`            | No          | Custom retry logic for failures                          |

## Tool Handler Syntax

Tools receive input directly (not wrapped in `{ input }`) and can use global runtime proxies such as `user`, `bot`, `adk`, and `actions`. For optional per-request values like `conversation` or `message`, use the Context API.

```typescript
import { Autonomous, z, user, adk, context } from '@botpress/runtime'

// ✅ Tools can destructure input parameters directly
export default new Autonomous.Tool({
  name: 'createCharacter',
  description: 'Create a new character with name and race',

  input: z.object({
    name: z.string().describe('Character name'),
    race: z.enum(['human', 'elf', 'dwarf']),
    background: z.enum(['warrior', 'ranger']).optional(),
  }),

  output: z.string(),

  // Handler destructures input directly
  handler: async ({ name, race, background }) => {
    // Direct access to user state
    user.state.characterName = name
    user.state.race = race
    user.state.background = background

    // Use ADK utilities
    const stats = await adk.zai.extract(
      `Create character stats for ${name} the ${race}`,
      z.object({
        courage: z.number().min(0).max(100),
        wisdom: z.number().min(0).max(100),
      })
    )

    user.state.courage = stats.courage
    user.state.wisdom = stats.wisdom

    return `Created ${name} the ${race}!`
  },
})

// ✅ Can also receive input as single parameter
export const simpleSearch = new Autonomous.Tool({
  name: 'search',
  description: 'Search knowledge bases',
  input: z.string().describe('The query to search for').min(1).max(1024),
  output: z.string(),

  handler: async (query) => {
    const results = await performSearch(query)
    return results
  },
})

// ✅ Method syntax with context parameter
export const anotherTool = new Autonomous.Tool({
  name: 'anotherTool',
  input: z.object({ param: z.string() }),
  output: z.string(),

  async handler(input, ctx) {
    // ctx.callId - unique identifier for this execution
    console.log(`Processing call: ${ctx.callId}`)
    return `Processed ${input.param}`
  },
})
```

**Key Differences from Actions:**

| Feature           | Actions                         | Tools                                                    |
| ----------------- | ------------------------------- | -------------------------------------------------------- |
| Input parameter   | `{ input, client }` wrapper     | Direct input or destructuring                            |
| Context access    | Via imports or context API      | Via imports (automatically available)                    |
| Typical use       | Internal functions, any context | AI-callable, conversation context                        |
| Handler signature | `handler({ input, client })`    | `handler(input, ctx?)` or `handler({ ...fields }, ctx?)` |

## Accessing Context in Tools

Tools can use global runtime proxies directly, but conversation-specific values should be loaded through `context.get(...)`:

```typescript
import { Autonomous, z, user, bot, adk, actions, context } from '@botpress/runtime'

export default new Autonomous.Tool({
  name: 'upgradeUser',
  description: 'Upgrade user to pro tier',
  input: z.object({}),
  output: z.string(),

  handler: async (input) => {
    // Direct access to context
    const userName = user.state.name
    const currentTier = user.tags.tier
    const conversation = context.get('conversation', { optional: true })

    // Update user state and tags
    user.tags.tier = 'pro'
    bot.state.totalUpgrades += 1

    // Call integration actions
    await actions.slack.sendMessage({
      channel: 'upgrades',
      text: `${userName} upgraded from ${currentTier} to pro`,
    })

    return `Upgraded ${userName} to pro tier`
  },
})
```

**Commonly used in tools:**

- `user` - Current user (`.state`, `.tags`)
- `bot` - Bot object (always available)
- `adk` - ADK utilities (`adk.zai.extract()`, etc.)
- `actions` - All available actions

Use `context.get("conversation", { optional: true })` or `context.get("message", { optional: true })` when you need those per-request values.

For complete context access details including `client`, `citations`, availability rules, and all context keys, see **[Context API](./context-api.md)**.

## Using ThinkSignal

`ThinkSignal` allows tools to return results with additional instructions for the AI. When thrown, it provides context that guides how the AI should use the information.

```typescript
import { Autonomous, z } from '@botpress/runtime'

export default new Autonomous.Tool({
  name: 'searchKnowledge',
  description: 'Search the knowledge base',
  input: z.string().describe('Search query'),
  output: z.string(),

  handler: async (query) => {
    const results = await knowledgeBase.search(query)

    // Handle no results case
    if (!results.length) {
      throw new Autonomous.ThinkSignal(
        'No results found',
        'No results were found. Try rephrasing or ask something else. Do NOT make up an answer.'
      )
    }

    // Format results for AI consumption
    const formatted = results.map((r, i) => `[${i + 1}] ${r.title}\n${r.content}`).join('\n\n')

    // Return results with instructions for the AI
    throw new Autonomous.ThinkSignal('Search complete - use these results to answer', formatted)
  },
})
```

**ThinkSignal parameters:**

- **First argument**: Brief status message for logs
- **Second argument**: Detailed content/instructions for the AI

**When to use ThinkSignal:**

- Providing search results with guidance
- Handling edge cases (no results, errors)
- Guiding AI behavior based on outcomes
- Passing contextual information to the AI

## Advanced Tool Properties

### Aliases

Provide alternative names for the tool:

```typescript
export default new Autonomous.Tool({
  name: 'searchDocumentation',
  aliases: ['search_docs', 'findDocs', 'lookupDocs'],
  description: 'Search documentation',
  handler: async (query) => {
    /* ... */
  },
})
```

### Static Input Values

Pre-set parameter values for specialized tool variants:

```typescript
const baseSearchTool = new Autonomous.Tool({
  name: 'search',
  input: z.object({
    query: z.string(),
    category: z.string(),
  }),
  handler: async ({ query, category }) => {
    /* ... */
  },
})

// Create specialized version with pre-set category
const productSearchTool = baseSearchTool.with({
  staticInputValues: { category: 'products' },
})
```

### Custom Retry Logic

Handle failures with custom retry behavior:

```typescript
export default new Autonomous.Tool({
  name: 'externalAPI',
  description: 'Call external API',
  input: z.object({ endpoint: z.string() }),
  output: z.any(),

  retry: async ({ input, attempt, error }) => {
    if (attempt < 3 && error?.code === 'RATE_LIMIT') {
      await new Promise((r) => setTimeout(r, 1000 * attempt))
      return true // Retry
    }
    return false // Don't retry
  },

  handler: async ({ endpoint }) => {
    const response = await fetch(endpoint)
    return await response.json()
  },
})
```

## Autonomous Namespace

The `Autonomous` namespace provides types and utilities for AI-powered autonomous execution.

### Autonomous.Tool

```typescript
export const Tool = LlmzTool
export type Tool = InstanceType<typeof Tool>
```

### Autonomous.Model Type

Type for specifying AI models:

```typescript
import { defineConfig } from '@botpress/runtime'

export default defineConfig({
  name: 'my-agent',
  defaultModels: {
    autonomous: 'openai:gpt-4o',
    zai: 'openai:gpt-4o-mini',
  },
})

// With fallback chain
export default defineConfig({
  defaultModels: {
    autonomous: ['openai:gpt-4o', 'anthropic:claude-3-5-sonnet'],
    zai: 'openai:gpt-4o-mini',
  },
})
```

**Model format:** `"provider:model-name"`

**Common providers:**

- `openai:gpt-4o`, `openai:gpt-4o-mini`
- `anthropic:claude-3-5-sonnet`
- `cerebras:gpt-oss-120b`

### Autonomous.Hooks Interface

Advanced hooks for controlling AI execution behavior:

```typescript
export type Hooks = {
  onBeforeTool?: (event: {
    iteration: Iteration
    tool: Autonomous.Tool
    input: any
    controller: AbortController
  }) => Promise<{ input?: any } | void>

  onAfterTool?: (event: {
    iteration: Iteration
    tool: Autonomous.Tool
    input: any
    output: any
    controller: AbortController
  }) => Promise<{ output?: any } | void>

  onBeforeExecution?: (iteration: Iteration, controller: AbortController) => Promise<{ code?: string } | void>

  onExit?: <T = unknown>(result: ExitResult<T>) => Promise<void> | void

  onTrace?: (props: { trace: Trace; iteration: number }) => void

  onIterationEnd?: (iteration: Iteration, controller: IterationController) => void | Promise<void>
}
```

**Example - Logging tool calls:**

```typescript
await execute({
  instructions: 'Help the user',
  tools: [searchTool, createTicketTool],
  hooks: {
    onBeforeTool: async ({ tool, input }) => {
      console.log(`Calling tool: ${tool.name}`, input)
    },
    onAfterTool: async ({ tool, output }) => {
      console.log(`Tool ${tool.name} returned:`, output)
    },
  },
})
```

**Example - Modifying tool inputs:**

```typescript
await execute({
  instructions: 'Search for information',
  tools: [searchTool],
  hooks: {
    onBeforeTool: async ({ tool, input }) => {
      if (tool.name === 'search') {
        return {
          input: {
            ...input,
            query: `${input.query} site:docs.example.com`,
          },
        }
      }
    },
  },
})
```

### Autonomous.Exit - Structured AI Exits

Exits provide type-safe, structured ways for AI to return different outcomes:

```typescript
import { Autonomous, z } from '@botpress/runtime'

const SearchExit = new Autonomous.Exit({
  name: 'search_complete',
  description: 'Search completed successfully',
  schema: z.object({
    results: z.array(z.string()),
    count: z.number(),
  }),
})

const NoResultsExit = new Autonomous.Exit({
  name: 'no_results',
  description: 'No results found for the query',
})

// Use exits in execute()
const result = await execute({
  instructions: 'Search and return appropriate exit',
  exits: [SearchExit, NoResultsExit],
})

// Type-safe handling
if (result.is(SearchExit)) {
  console.log(`Found ${result.output.count} results`)
} else if (result.is(NoResultsExit)) {
  console.log('No results found')
}
```

### Other Autonomous Exports

**Signal Classes:**

```typescript
export const ThinkSignal = _ThinkSignal
export const SnapshotSignal = _SnapshotSignal
```

**Type Exports:**

```typescript
export type Iteration = InstanceType<typeof LlmzIteration>;
export type ExecuteResult = Awaited<ReturnType<Execute>>;
export type Trace = /* various trace types */;
export type IterationController = /* controller interface */;
```

> **Note:** See [Using ThinkSignal](#using-thinksignal) section for detailed usage examples.

## Best Practices

1. **Clear descriptions**: Help AI understand when to use the tool
2. **Use `.describe()` on inputs**: Clarify parameter purposes for AI
3. **Provide context in output**: Return informative strings or objects
4. **Handle edge cases**: Use ThinkSignal for no-result or error scenarios
5. **Keep handlers focused**: One tool = one capability
6. **Test independently**: Tools can be tested outside of conversations

**Example - Production-Ready Tool:**

```typescript
export default new Autonomous.Tool({
  name: 'createSupportTicket',
  description: 'Create a support ticket for user issues or requests',

  input: z.object({
    title: z.string().min(5).max(100).describe('Brief ticket title'),
    description: z.string().min(10).max(2000).describe('Detailed issue description'),
    priority: z.enum(['low', 'medium', 'high', 'urgent']).default('medium').describe('Ticket priority level'),
    category: z.enum(['bug', 'feature', 'question', 'other']).describe('Issue category'),
  }),

  output: z.object({
    ticketId: z.string(),
    url: z.string(),
  }),

  handler: async ({ title, description, priority, category }) => {
    // Validate user has permission
    if (user.tags.tier === 'free' && priority === 'urgent') {
      throw new ThinkSignal(
        'Priority upgrade needed',
        'Urgent priority is only available for premium users. Would you like to upgrade?'
      )
    }

    // Create ticket with context
    const ticket = await actions.helpdesk.createTicket({
      title,
      description: `User: ${user.id}\nCategory: ${category}\n\n${description}`,
      priority,
      metadata: {
        userId: user.id,
        conversationId: conversation?.id,
      },
    })

    // Update user state
    user.state.lastTicketId = ticket.id
    user.state.lastTicketCreated = new Date().toISOString()

    return {
      ticketId: ticket.id,
      url: `https://support.example.com/ticket/${ticket.id}`,
    }
  },
})
```

## Troubleshooting

### Common Issues

1. **Tool not available to AI**
   - Check file is in `src/tools/` directory
   - Ensure tool is exported as default or named export
   - Verify tool is included in `execute()` tools array

2. **"user is not defined" or context errors**
   - **Cause**: Trying to access conversation context outside of conversation
   - **Solution**: Use optional chaining (`user?.state`) or `context.get("user", { optional: true })`
   - **Note**: Tools are typically called from conversations, so context is usually available

3. **Type errors with inputs/outputs**
   - Verify Zod schemas match actual data
   - Use `.optional()` for optional fields
   - Check for typos in property names

4. **State properties undefined**
   - **Cause**: State properties must be defined in `agent.config.ts` schemas
   - **Solution**: Add properties to `user.state` or `bot.state` schema in config

5. **AI not calling tool correctly**
   - Improve tool `description` to clarify when it should be used
   - Add detailed `.describe()` to all input parameters
   - Use clear, descriptive parameter names
   - Consider using ThinkSignal to guide AI behavior

6. **ThinkSignal not working as expected**
   - **Issue**: ThinkSignal must be thrown, not returned
   - **Wrong**: `return new ThinkSignal(...)`
   - **Correct**: `throw new ThinkSignal(...)`

## See Also

- [Actions](./actions.md) - Strongly-typed internal functions
- [Conversations](./conversations.md) - Using tools in conversation handlers
- [Autonomous Execution](./autonomous-execution.md) - Objects, Exits, hooks, and full `execute()` API
- [Context API](./context-api.md) - Access runtime context and services
