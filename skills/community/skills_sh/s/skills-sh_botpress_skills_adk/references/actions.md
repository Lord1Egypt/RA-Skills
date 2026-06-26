# Actions

Actions are callable, strongly-typed functions that encapsulate reusable logic accessible throughout your agent. They can be invoked from workflows, conversations, other actions, or exposed as tools for AI.

## Overview

Actions enable you to:

- Create reusable business logic across your bot
- Call integration APIs with type safety
- Expose functionality as AI-callable tools
- Compose complex operations from simple functions
- Test logic independently from conversational flows

## File Location

- **Location**: `src/actions/*.ts`
- **Auto-registration**: Files in this directory automatically become available as `actions.{actionName}`
- **Export pattern**: Both `export const` and `export default` work
  - **`export const`** (Recommended): Enables direct imports and passing to `execute()` as tools
  - **`export default`**: Simpler for single-action files

## Basic Action Structure

```typescript
import { Action, z } from "@botpress/runtime";

// Option 1: Named export (recommended)
export const myAction = new Action({
  name: "myAction",
  input: z.object({
    userId: z.string(),
  }),
  output: z.object({
    data: z.string(),
    timestamp: z.string()
  }),
  handler: async ({ input, client }) {
    // Your business logic here
    const result = await fetchData(input.userId);

    return {
      data: result,
      timestamp: new Date().toISOString()
    };
  },
});

// Option 2: Default export (also valid)
export default new Action({
  name: "myAction",
  // ... same configuration
});
```

> **`output` is required.** Declare it as a bare Zui schema (`output: z.object({ ... })`), never `output: { schema: ... }`. Omitting it fails the type check (`adk check` won't catch it).

**Why use `export const`?**

- Enables direct imports: `import { myAction } from "./actions/myAction"`
- Can pass to `execute()`: `tools: [myAction.asTool()]`
- Better for action composition and reusability

## Action Properties

| Property        | Type                     | Required | Description                                                      |
| --------------- | ------------------------ | -------- | ---------------------------------------------------------------- |
| **name**        | `string`                 | Yes      | Unique alphanumeric identifier (no spaces or special characters) |
| **input**       | `z.ZodTypeAny`           | Yes      | Zod schema defining input parameters                             |
| **output**      | `z.ZodTypeAny`           | Yes      | Zod schema defining return type                                  |
| **handler**     | `function`               | Yes      | Async function implementing the action logic                     |
| **title**       | `string`                 | No       | Human-readable display name                                      |
| **description** | `string`                 | No       | Description of the action's functionality                        |
| **attributes**  | `Record<string, string>` | No       | Custom metadata for categorization                               |
| **cached**      | `boolean`                | No       | Enable caching for identical inputs (defaults to `false`)        |

## Handler Syntax

Action handlers receive a props object containing `input` and `client`. Both method syntax and arrow functions are supported.

### Method Syntax (Recommended)

```typescript
export const fetchUser = new Action({
  name: 'fetchUser',
  input: z.object({ userId: z.string() }),
  output: z.object({
    name: z.string(),
    email: z.string(),
  }),

  async handler({ input, client }) {
    // input: validated input matching your input schema
    // client: Botpress API client for making API calls
    const { user } = await client.getUser({ id: input.userId })
    return {
      name: user.name,
      email: user.tags.email,
    }
  },
})
```

### Arrow Function Syntax

```typescript
export const updateUser = new Action({
  name: 'updateUser',
  input: z.object({
    userId: z.string(),
    name: z.string(),
  }),
  output: z.object({ success: z.boolean() }),

  handler: async ({ input, client }) => {
    await client.updateUser({
      id: input.userId,
      name: input.name,
    })
    return { success: true }
  },
})
```

### Common Mistakes

```typescript
// ❌ WRONG - Destructuring input fields directly
export const fetchUser = new Action({
  name: 'fetchUser',
  input: z.object({ userId: z.string() }),
  output: z.object({ name: z.string() }),

  async handler({ userId }) {
    // ❌ Wrong! Must be { input }
    return { name: userId }
  },
})

// ✅ CORRECT - Use { input } wrapper
export const fetchUser = new Action({
  name: 'fetchUser',
  input: z.object({ userId: z.string() }),
  output: z.object({ name: z.string() }),

  async handler({ input }) {
    // ✅ Correct
    const { userId } = input // Destructure inside handler
    return { name: userId }
  },
})
```

**Key points:**

- Handler receives `{ input, client }` props object
- Both method syntax and arrow functions work
- Destructure input fields **inside** the handler body, not in the parameter
- **Actions CANNOT destructure input fields directly** (unlike Tools)
- Omit `client` if not needed: `async handler({ input })`

## Calling Actions

### From Workflows

```typescript
import { Workflow, actions } from '@botpress/runtime'

export default new Workflow({
  name: 'processOrder',
  input: z.object({ orderId: z.string() }),

  handler: async ({ input }) => {
    // Call your custom actions
    const order = await actions.fetchOrder({ orderId: input.orderId })
    const result = await actions.processPayment({ order })

    return result
  },
})
```

### From Other Actions

```typescript
import { Action, actions, z } from '@botpress/runtime'

export default new Action({
  name: 'compositeAction',
  input: z.object({ userId: z.string() }),
  output: z.object({ success: z.boolean() }),

  async handler({ input }) {
    // Compose multiple actions
    const userData = await actions.fetchUser({ userId: input.userId })
    const profile = await actions.buildProfile({ user: userData })
    return { success: true }
  },
})
```

### Integration Actions

Call integration actions from within your actions:

```typescript
import { actions } from '@botpress/runtime'

// Inside action handler
await actions.slack.sendMessage({
  channel: '#general',
  text: 'Message from bot',
})

await actions.linear.issueList({ first: 10 })
```

See **[Integration Actions](./integration-actions.md)** for complete guide.

## Accessing Additional Context

Actions can access additional runtime context through **direct imports** or the **Context API**.

Direct imports are best for the global proxies that actually exist at runtime, such as `user`, `bot`, `configuration`, and `adk`. For optional per-request values like `conversation` and `message`, use the Context API.

### Method 1: Direct Imports (Global Context Proxies)

```typescript
import { Action, z, user, bot, adk } from '@botpress/runtime'
import { context } from '@botpress/runtime'

export default new Action({
  name: 'updateUserProfile',
  input: z.object({ name: z.string() }),
  output: z.object({ success: z.boolean() }),

  async handler({ input }) {
    // Access user state directly (when in conversation context)
    user.state.profileName = input.name
    user.tags.profileComplete = 'true'

    // Access bot state
    bot.state.totalUsers += 1

    // Access conversation (when in conversation context)
    const conversation = context.get('conversation', { optional: true })
    console.log(conversation?.id)

    // Use ADK utilities
    const extracted = await adk.zai.extract(input.name, z.object({ firstName: z.string(), lastName: z.string() }))

    return { success: true }
  },
})
```

### Method 2: Context API (Explicit Retrieval)

```typescript
import { Action, z, context } from '@botpress/runtime'

export default new Action({
  name: 'checkContext',
  input: z.object({}),
  output: z.object({ hasUser: z.boolean() }),

  async handler({ input }) {
    // Optional context (may not be available in all scenarios)
    const user = context.get('user', { optional: true })
    const conversation = context.get('conversation', { optional: true })
    const message = context.get('message', { optional: true })

    // Always available
    const client = context.get('client')
    const citations = context.get('citations')

    if (user) {
      console.log(`User: ${user.id}`)
    }

    return { hasUser: !!user }
  },
})
```

**Which method to use?**

- **Direct imports**: Use for `user`, `bot`, `adk` when you know they're available (simpler syntax)
- **Context API**: Use for optional context (`user`, `conversation`, `message`) or when you need `client` and `citations`

**Always available:** `bot`, `adk`, `client`, `context`
**Conditionally available:** `user`, `conversation`, `message` (only in conversation context)

See **[Context API](./context-api.md)** for complete details on all context keys and availability.

## Advanced Action Patterns

### Pattern 1: Integration Wrapper Pattern

**Purpose:** Wrap integration actions with bot-specific logic, data transformation, and local persistence.

**When to use:**

- Syncing external resources (products, issues, orders) to local tables
- Normalizing data from different integrations
- Adding business logic or validation
- Maintaining local cache of external data

**Abstract Structure:**

```typescript
export default new Action({
  name: 'syncResource',
  description: 'Fetch and sync external resource to local storage',

  input: z.object({
    resourceId: z.string().describe('External resource identifier'),
  }),

  output: BotResourceSchema, // Your normalized schema

  async handler({ input }) {
    // 1. Call integration action
    const externalData = await actions.integration.getResource({
      id: input.resourceId,
    })

    // 2. Transform to bot schema
    const normalizedData = transformToBotSchema(externalData)

    // 3. Persist to table (prevents duplicates)
    await ResourceTable.upsertRows({
      rows: [normalizedData],
      keyColumn: 'id', // Unique identifier
    })

    // 4. Return normalized data
    return normalizedData
  },
})
```

**Real Example - Shopify: Sync Products**

```typescript
import { Action, actions, z } from '@botpress/runtime'
import { ProductsTable } from '../tables/shopify'

export default new Action({
  name: 'syncProduct',
  description: 'Sync a Shopify product to local database',

  input: z.object({
    productId: z.string().describe('Shopify product ID'),
    includeVariants: z.boolean().default(true),
  }),

  output: z.object({
    id: z.string(),
    title: z.string(),
    price: z.number(),
    inventory: z.number(),
    lastSynced: z.string(),
  }),

  async handler({ input }) {
    // 1. Fetch from Shopify
    const shopifyProduct = await actions.shopify.getProduct({
      id: input.productId,
      fields: ['id', 'title', 'variants', 'inventory'],
    })

    // 2. Transform to bot schema
    const product = {
      id: shopifyProduct.id,
      title: shopifyProduct.title,
      price: shopifyProduct.variants[0].price,
      inventory: shopifyProduct.variants.reduce((sum, v) => sum + v.inventory_quantity, 0),
      lastSynced: new Date().toISOString(),
    }

    // 3. Upsert to table
    await ProductsTable.upsertRows({
      rows: [product],
      keyColumn: 'id',
    })

    return product
  },
})
```

**Key Benefits:**

- **Consistency**: All external data follows your bot's schema
- **Performance**: Local table queries are faster than API calls
- **Reliability**: Works even if integration is temporarily unavailable
- **Extensibility**: Easy to add business logic or validation

### Pattern 2: Resource State Management

**Purpose:** Update external resource state and keep local cache in sync.

**Real Example - Linear: Update Issue Status**

```typescript
import { Action, actions, z } from '@botpress/runtime'
import { IssuesTable } from '../tables/linear'

export default new Action({
  name: 'updateIssueStatus',

  input: z.object({
    issueId: z.string(),
    stateId: z.string(),
    comment: z.string().optional(),
  }),

  output: z.object({
    id: z.string(),
    title: z.string(),
    state: z.string(),
    updatedAt: z.string(),
  }),

  async handler({ input }) {
    // 1. Update in Linear
    const issue = await actions.linear.updateIssue({
      id: input.issueId,
      stateId: input.stateId,
      ...(input.comment && {
        commentBody: input.comment,
      }),
    })

    // 2. Transform and sync to table
    const normalized = {
      id: issue.id,
      title: issue.title,
      state: issue.state.name,
      updatedAt: new Date().toISOString(),
    }

    await IssuesTable.upsertRows({
      rows: [normalized],
      keyColumn: 'id',
    })

    return normalized
  },
})
```

**When to use this pattern:**

- Tracking order fulfillment status
- Managing ticket/issue lifecycle
- Handling conversation states
- Any resource with state transitions

## Schema Design Best Practices

**Core Principles:**

```typescript
import { z } from '@botpress/runtime'

// 1. Always export both type and schema
export type Product = z.infer<typeof ProductSchema>
export const ProductSchema = z.object({
  id: z.string(),
  name: z.string(),
  price: z.number(),
})

// 2. Use .describe() on every field (helps AI tools)
const schema = z.object({
  productId: z.string().describe('Unique product identifier'),
  price: z.number().describe('Price in cents'),
  inStock: z.boolean().describe('Whether product is available'),
})

// 3. ISO strings for dates (NOT z.date())
const timeFields = z.object({
  createdAt: z.string().describe('Creation date as ISO 8601 string'),
  updatedAt: z.string().optional().describe('Last update date'),
})

// 4. Use .optional() for optional fields
const optionalFields = z.object({
  name: z.string(), // Required
  description: z.string().optional(), // Optional
  metadata: z.record(z.unknown()).optional(),
})

// 5. Use .passthrough() for external API data
const externalData = z
  .object({
    id: z.string(),
    // Allow unknown fields from external API
  })
  .passthrough()

// 6. Define nested objects explicitly
const structured = z.object({
  product: z.object({
    // ✅ Explicit structure
    id: z.string(),
    name: z.string(),
  }),
  metadata: z.record(z.unknown()), // ❌ Use only when structure is truly unknown
})
```

**Key Patterns:**

1. **Export both type and schema** - TypeScript type from `z.infer<>`
2. **Describe every field** - Helps AI tools and documentation
3. **ISO strings for dates** - Use `z.string()` not `z.date()`
4. **Optional vs nullable** - Use `.optional()` for optional fields
5. **Passthrough for external APIs** - Use `.passthrough()` when structure varies
6. **Separate schemas file** - Keep complex schemas in `src/schemas.ts`
7. **Explicit nested objects** - Define structure instead of `z.unknown()`

## Converting Actions to Tools

Actions can be converted to AI-callable tools using the `.asTool()` method. This allows AI agents to autonomously call your actions during conversations.

### Basic Usage

```typescript
import { actions, Conversation } from '@botpress/runtime'

export default new Conversation({
  handler: async ({ execute }) => {
    await execute({
      instructions: 'Help the user with their request',
      tools: [
        // Convert existing actions to tools
        actions.fetchUser.asTool(),
        actions.sendEmail.asTool(),
        actions.searchDatabase.asTool(),
      ],
    })
  },
})
```

### Tool Patterns: Blocking vs Non-Blocking

#### Pattern Comparison

| Pattern              | Returns      | Execution    | Example           |
| -------------------- | ------------ | ------------ | ----------------- |
| **Direct Action**    | Final result | Synchronous  | `fetchUser()`     |
| **Workflow Wrapper** | Workflow ID  | Asynchronous | `startIndexing()` |

#### 1. Direct Actions

Actions that complete and return results immediately:

```typescript
import { Action, z } from '@botpress/runtime'

export default new Action({
  name: 'calculateShipping',
  description: 'Calculate shipping cost for an order',

  input: z.object({
    weight: z.number(),
    destination: z.string(),
  }),

  output: z.object({
    cost: z.number(),
    estimatedDays: z.number(),
  }),

  async handler({ input }) {
    // Business logic that completes immediately
    const baseRate = 5.99
    const perKg = 2.5
    const cost = baseRate + input.weight * perKg

    const estimatedDays = input.destination === 'domestic' ? 3 : 7

    return { cost, estimatedDays }
  },
})

// Use as tool - AI can call this during conversation
await execute({
  instructions: 'Help the user with shipping',
  tools: [actions.calculateShipping.asTool()],
})
```

#### 2. Workflow Wrappers

Actions that start workflows and return workflow ID:

```typescript
import { Action, z } from '@botpress/runtime'
import { DataAnalysisWorkflow } from '../workflows/data-analysis'

export default new Action({
  name: 'startDataAnalysis',
  description: 'Start data analysis workflow',

  input: z.object({
    datasetId: z.string(),
  }),

  output: z.object({
    workflowId: z.string(),
  }),

  async handler({ input }) {
    // Calls workflow.start() - returns immediately
    const instance = await DataAnalysisWorkflow.start({
      datasetId: input.datasetId,
    })
    return { workflowId: instance.id }
  },
})

// Companion action to check status
export const checkAnalysisStatus = new Action({
  name: 'checkAnalysisStatus',
  description: 'Check workflow status',

  input: z.object({
    workflowId: z.string(),
  }),

  output: z.object({
    status: z.string(),
  }),

  async handler({ input, client }) {
    const { workflow } = await client.getWorkflow({ id: input.workflowId })
    return { status: workflow.status }
  },
})

// Use both as tools
await execute({
  instructions: 'Help the user',
  tools: [actions.startDataAnalysis.asTool(), actions.checkAnalysisStatus.asTool()],
})
```

### Custom Tool Conversion

```typescript
// Basic conversion
const shippingTool = actions.calculateShipping.asTool()

// With custom description
const analysisTool = actions.startDataAnalysis.asTool({
  description: 'Analyze dataset and return workflow ID',
})
```

> **See Also:** [Exposing Workflows as Tools](./workflows.md#exposing-workflows-as-tools-non-blocking-pattern) for comprehensive workflow wrapper patterns and tracking examples.

## Best Practices

1. **Use descriptive names**: `fetchUserProfile` not `getUser`
2. **Validate inputs thoroughly**: Use Zod's validation features
3. **Handle errors gracefully**: Catch and wrap errors with context
4. **Keep actions focused**: One action = one responsibility
5. **Document complex logic**: Add comments for non-obvious operations
6. **Use caching wisely**: Enable `cached: true` for deterministic operations

```typescript
export default new Action({
  name: 'fetchUserProfile',
  description: 'Fetches complete user profile with preferences',

  input: z.object({
    userId: z.string().uuid(), // Validate UUID format
    includePreferences: z.boolean().default(false),
  }),

  output: z.object({
    user: z.object({
      id: z.string(),
      name: z.string(),
      email: z.string().email(),
    }),
    preferences: z
      .object({
        language: z.string(),
        timezone: z.string(),
      })
      .optional(),
  }),

  cached: true, // Cache for performance

  async handler({ input, client }) {
    // Validate user exists
    const { user } = await client.getUser({ id: input.userId })
    if (!user) {
      throw new Error(`User ${input.userId} not found`)
    }

    // Conditionally fetch preferences
    const preferences = input.includePreferences ? await fetchUserPreferences(input.userId) : undefined

    return {
      user: {
        id: user.id,
        name: user.name,
        email: user.tags.email,
      },
      preferences,
    }
  },
})
```

## Common Patterns

### Composition Pattern

Combine multiple actions for complex operations:

```typescript
export default new Action({
  name: 'processOrder',
  input: z.object({ orderId: z.string() }),
  output: z.object({ success: z.boolean() }),

  async handler({ input }) {
    // Compose multiple actions
    const order = await actions.fetchOrder({ id: input.orderId })
    const validated = await actions.validateOrder({ order })

    if (validated.isValid) {
      await actions.chargePayment({
        amount: order.total,
        customerId: order.customerId,
      })
      await actions.sendConfirmation({ order })
      await actions.updateInventory({ items: order.items })
    }

    return { success: validated.isValid }
  },
})
```

### Error Recovery Pattern

Handle failures gracefully with retries:

```typescript
export default new Action({
  name: 'resilientFetch',
  input: z.object({ url: z.string().url() }),
  output: z.object({ data: z.unknown() }),

  async handler({ input }) {
    const maxRetries = 3
    let lastError

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const response = await fetch(input.url)
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        return { data: await response.json() }
      } catch (error) {
        lastError = error
        if (attempt < maxRetries) {
          // Exponential backoff
          await new Promise((r) => setTimeout(r, 1000 * Math.pow(2, attempt)))
        }
      }
    }

    throw new Error(`Failed after ${maxRetries} attempts: ${lastError.message}`)
  },
})
```

## Troubleshooting

### Common Issues

1. **"Cannot destructure property" error**
   - **Cause**: Destructuring input fields directly in Action handler parameter
   - **Wrong**: `async handler({ userId }) { ... }`
   - **Correct**: `async handler({ input }) { const { userId } = input; ... }`
   - **Note**: Tools can destructure directly, but Actions cannot

2. **"user is not defined" or context errors**
   - **Cause**: Accessing conversation context outside of conversation context
   - **Solution**: Use `context.get("user", { optional: true })` to check availability
   - **Note**: `user`, `conversation`, `message` are only available in conversation contexts

3. **Action not found**
   - Verify file is in `src/actions/` directory
   - Check import: `import { actions } from "@botpress/runtime"`
   - Ensure action name matches file export

4. **Type errors with inputs/outputs**
   - Verify Zod schemas match actual data
   - Use `.optional()` for optional fields
   - Check for typos in property names

5. **State properties undefined**
   - **Cause**: State properties must be defined in `agent.config.ts` schemas
   - **Solution**: Add properties to `user.state` or `bot.state` schema in config
   - **Example**: Can't use `user.state.characterName` unless defined in config

6. **Caching issues**
   - **Issue**: Cached results not updating when expected
   - **Solution**: Only use `cached: true` for deterministic functions
   - **Tip**: Avoid caching for time-sensitive or user-specific data

## See Also

- [Tools](./tools.md) - AI-callable tools for autonomous execution
- [Workflows](./workflows.md) - Multi-step processes with state management
- [Context API](./context-api.md) - Access runtime context and services
- [Integration Actions](./integration-actions.md) - Using integration actions
- [Patterns & Common Mistakes](./patterns-mistakes.md) - Best practices for Zod schemas
