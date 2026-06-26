# Botpress Client Integration

## Overview

The Botpress Client (`@botpress/client`) is the official TypeScript client for interacting with the Botpress API. In frontend applications, you'll use it to call bot actions, query tables, manage conversations, and more.

This guide covers client setup, the recommended client management pattern using Zustand, and practical examples for production applications.

---

## Installing @botpress/client

```bash
npm install @botpress/client
# or
pnpm add @botpress/client
# or
yarn add @botpress/client
```

**Additional packages for AI operations:**

```bash
npm install @botpress/zai @botpress/cognitive
```

---

## Client Initialization

The Botpress Client requires four key parameters:

```typescript
import { Client } from '@botpress/client'

const client = new Client({
  apiUrl: 'https://api.botpress.cloud',
  workspaceId: 'your-workspace-id',
  token: 'your-personal-access-token',
  botId: 'your-bot-id', // Optional - needed for bot-specific operations
})
```

**Configuration Parameters:**

- **apiUrl**: Base URL for Botpress Cloud API (always `https://api.botpress.cloud` for production)
- **workspaceId**: Your Botpress workspace identifier
- **token**: Personal Access Token (PAT) for authentication
- **botId**: (Optional) Specific bot ID - required for bot-scoped operations like calling actions or querying bot tables

---

## Client Management Pattern

### Why Use a Client Store?

In production applications, you'll need multiple client instances:

1. **Workspace-scoped client** - For workspace-level operations (no botId)
2. **Bot-scoped clients** - For each bot you interact with (with botId)

Creating a new client for every API call is inefficient. Instead, use a **client caching pattern** with Zustand to:

- Reuse client instances
- Manage authentication centrally
- Handle multiple bots cleanly
- Avoid configuration duplication

---

## Recommended clientsStore Pattern

Here's a complete production-ready implementation for `stores/clientsStore.ts`:

```typescript
import { create } from 'zustand'
import { Client as APIClient } from '@botpress/client'
import { Zai } from '@botpress/zai'
import { Cognitive } from '@botpress/cognitive'
import { getPat } from '../lib/auth'

const API_BASE_URL = 'https://api.botpress.cloud'
const DEFAULT_API_CLIENT_KEY = 'DEFAULT_API_CLIENT'

type getApiClientProps = { botId?: string; workspaceId: string } | { botId?: never; workspaceId?: string }

type ClientsState = {
  APIClients: Record<string, APIClient>
  getAPIClient: (props?: getApiClientProps) => APIClient
  addAPIClient: (key: string, client: APIClient) => void
}

const useClientsStore = create<ClientsState>()((set, get) => ({
  APIClients: {},
  getAPIClient: (props) => {
    const key = props?.botId ? `${props.workspaceId}-${props.botId}` : (props?.workspaceId ?? DEFAULT_API_CLIENT_KEY)
    const client = get().APIClients[key]

    if (client) {
      return client
    }

    const newClient = new APIClient({
      apiUrl: API_BASE_URL,
      workspaceId: props?.workspaceId,
      token: getPat() ?? '',
      botId: props?.botId,
    })

    set((state) => ({
      APIClients: { ...state.APIClients, [key]: newClient },
    }))

    return newClient
  },
  addAPIClient: (key, client) =>
    set((state) => ({
      APIClients: { ...state.APIClients, [key]: client },
    })),
}))

export const getApiClient = (props?: getApiClientProps) => useClientsStore.getState().getAPIClient(props)

export const getZaiClient = (workspaceId: string, botId: string) => {
  const timeout = 5 * 60 * 1000 // 5 minutes
  const client = new APIClient({
    // We create a new client from scratch here because we need to override the default timeout for Zai
    ...getApiClient({ workspaceId, botId }).config,
    timeout,
  })

  const cognitive = new Cognitive({ client, timeout, __experimental_beta: true })

  return new Zai({
    modelId: 'fast',
    client: cognitive,
  })
}
```

### How the Client Store Works

**1. Client Caching (lines 13-19)**

```typescript
type ClientsState = {
  APIClients: Record<string, APIClient> // Cache of client instances by key
  getAPIClient: (props?: getApiClientProps) => APIClient
  addAPIClient: (key: string, client: APIClient) => void
}
```

The store maintains a `Record<string, APIClient>` where each key is a unique client identifier.

**2. Dynamic Client Keys (lines 21-23)**

```typescript
const key = props?.botId
  ? `${props.workspaceId}-${props.botId}` // Bot-scoped: "ws123-bot456"
  : (props?.workspaceId ?? DEFAULT_API_CLIENT_KEY) // Workspace-scoped: "ws123" or "DEFAULT"
```

Keys are generated based on scope:

- With `botId`: `"workspaceId-botId"` (e.g., `"ws_abc123-bot_xyz789"`)
- Without `botId`: `"workspaceId"` (e.g., `"ws_abc123"`)
- No parameters: `"DEFAULT_API_CLIENT"` (fallback)

**3. Client Reuse (lines 24-28)**

```typescript
const client = get().APIClients[key]

if (client) {
  return client // Return cached client if exists
}
```

Before creating a new client, check if one exists for this key.

**4. Lazy Client Creation (lines 30-41)**

```typescript
const newClient = new APIClient({
  apiUrl: API_BASE_URL,
  workspaceId: props?.workspaceId,
  token: getPat() ?? '',
  botId: props?.botId,
})

set((state) => ({
  APIClients: { ...state.APIClients, [key]: newClient },
}))

return newClient
```

If no cached client exists:

1. Create new client with configuration
2. Store it in the cache
3. Return it

**5. Helper Export (line 49)**

```typescript
export const getApiClient = (props?: getApiClientProps) => useClientsStore.getState().getAPIClient(props)
```

Exposes `getApiClient` as a standalone function (non-reactive) for use outside React components.

---

## Using the Client

### Calling Bot Actions

```typescript
import { getApiClient } from '@/stores/clientsStore'

// Get bot-scoped client
const client = getApiClient({
  workspaceId: 'ws_abc123',
  botId: 'bot_xyz789',
})

// Call an action
const result = await client.callAction({
  type: 'lookupOrder',
  input: {
    orderId: 'ORD-12345',
  },
})

console.log(result.output) // { order: { ... } }
```

**Key Points:**

- Actions require a bot-scoped client (with `botId`)
- Use `callAction()` method
- Input must match action's Zui schema
- Output is strongly typed if using generated types

### Querying Tables

```typescript
import { getApiClient } from '@/stores/clientsStore'

const client = getApiClient({
  workspaceId: 'ws_abc123',
  botId: 'bot_xyz789',
})

// Find table rows
const { rows } = await client.findTableRows({
  table: 'customers',
  filter: {
    email: 'user@example.com',
  },
})

console.log(rows) // [{ id: "...", email: "user@example.com", ... }]
```

**Table Operations:**

- `findTableRows()` - Query with filters
- `getTableRow()` - Get by ID
- `upsertTableRows()` - Create or update (plural)
- `deleteTableRows()` - Delete by filter/IDs (plural)

### Workspace-Level Operations

```typescript
import { getApiClient } from '@/stores/clientsStore'

// Get workspace-scoped client (no botId)
const client = getApiClient({
  workspaceId: 'ws_abc123',
})

// List all bots in workspace
const { bots } = await client.listBots()

console.log(bots) // [{ id: "bot_1", name: "Support Bot" }, ...]
```

---

## Type Safety

**Using Generated Types:**

```typescript
import type { AdkClient } from './.adk/client' // Generated by adk dev

const client = getApiClient({ workspaceId, botId }) as Client

// Now actions are fully typed
const result = await client.lookupOrder({
  orderId: 'ORD-123', // TypeScript knows this is required
})

// result.order is typed
console.log(result.order.status) // "shipped" | "pending" | etc.
```

**Best Practice:** Always use generated types from `adk dev` for full type safety.

---

## Error Handling

### Common Error Scenarios

```typescript
import { getApiClient } from '@/stores/clientsStore'

async function callBotAction(workspaceId: string, botId: string) {
  try {
    const client = getApiClient({ workspaceId, botId })

    const result = await client.callAction({
      type: 'lookupOrder',
      input: { orderId: 'ORD-123' },
    })

    return result.output
  } catch (error: any) {
    // Network errors
    if (error.code === 'ECONNREFUSED') {
      console.error('Cannot connect to Botpress API')
      return null
    }

    // Authentication errors
    if (error.status === 401) {
      console.error('Invalid or expired token')
      // Redirect to login
      return null
    }

    // Bot not found
    if (error.status === 404) {
      console.error('Bot not found:', botId)
      return null
    }

    // Action not found or input validation error
    if (error.status === 400) {
      console.error('Invalid action call:', error.message)
      return null
    }

    // Unknown error
    console.error('Unexpected error:', error)
    throw error
  }
}
```

**Error Status Codes:**

- `401` - Authentication failed (invalid/expired token)
- `403` - Forbidden (insufficient permissions)
- `404` - Resource not found (bot, action, table row)
- `400` - Bad request (invalid input, validation error)
- `500` - Server error
- `ECONNREFUSED` - Network error (cannot reach API)

---

## Advanced: Zai and Cognitive Clients

### What are Zai and Cognitive?

- **Cognitive** (`@botpress/cognitive`) - Low-level client for raw LLM API calls
- **Zai** (`@botpress/zai`) - High-level AI operations library (extract, check, summarize, etc.)

Both are built on top of the Botpress Client but require extended timeouts for AI operations.

### The getZaiClient Pattern

```typescript
export const getZaiClient = (workspaceId: string, botId: string) => {
  const timeout = 5 * 60 * 1000 // 5 minutes

  // Create a new client with extended timeout
  // Note: We create from scratch because client.config only contains apiUrl/headers/timeout,
  // not auth credentials. Pass all params explicitly.
  const client = new APIClient({
    apiUrl: API_BASE_URL,
    workspaceId,
    botId,
    token: getPat() ?? '',
    timeout, // Override timeout for AI operations
  })

  // Create Cognitive client
  const cognitive = new Cognitive({
    client,
    timeout,
    __experimental_beta: true, // Enable beta features
  })

  // Create Zai client
  return new Zai({
    modelId: 'fast', // Use "fast" model (or "smart" for complex tasks)
    client: cognitive,
  })
}
```

**Why Extended Timeout?**

AI operations (especially with large documents or complex extractions) can take minutes. The default client timeout (30s) is too short.

### Using Zai for AI Operations

```typescript
import { getZaiClient } from '@/stores/clientsStore'

const zai = getZaiClient('ws_abc123', 'bot_xyz789')

// Extract structured data
const result = await zai.extract({
  from: 'John Smith is 35 years old and lives in New York.',
  to: z.object({
    name: z.string(),
    age: z.number(),
    city: z.string(),
  }),
})

console.log(result) // { name: "John Smith", age: 35, city: "New York" }
```

**Zai Operations:**

- `extract()` - Pull structured data from text using schemas
- `check()` - Validate content (sentiment, criteria)
- `text()` - Generate content from prompts
- `summarize()` - Handle documents of any size
- `filter()` - Query arrays with natural language

**See Also:** The ADK skill's [zai-agent-reference.md](../../adk/references/zai-agent-reference.md) for all Zai operations and edge cases, and [zai-complete-guide.md](../../adk/references/zai-complete-guide.md) for the full developer guide.

---

## Best Practices

### 1. Always Use the Client Store

```typescript
// ✅ CORRECT - Reuse cached clients
import { getApiClient } from '@/stores/clientsStore'
const client = getApiClient({ workspaceId, botId })

// ❌ WRONG - Creates new client every time
import { Client } from '@botpress/client'
const client = new Client({ apiUrl, workspaceId, token, botId })
```

### 2. Use Workspace-Scoped Clients When Appropriate

```typescript
// ✅ CORRECT - No botId for workspace operations
const client = getApiClient({ workspaceId })
const { bots } = await client.listBots()

// ❌ WRONG - Unnecessary botId
const client = getApiClient({ workspaceId, botId: 'bot_123' })
const { bots } = await client.listBots() // botId ignored but wasteful
```

### 3. Handle Authentication Centrally

```typescript
// ✅ CORRECT - getPat() handles token retrieval/refresh
const client = new APIClient({
  apiUrl: API_BASE_URL,
  workspaceId,
  token: getPat() ?? '',
  botId,
})

// ❌ WRONG - Hardcoded token
const client = new APIClient({
  apiUrl: API_BASE_URL,
  workspaceId,
  token: 'bp_pat_abc123...', // Will expire!
  botId,
})
```

### 4. Use Extended Timeouts for AI Operations

```typescript
// ✅ CORRECT - Use getZaiClient for AI operations
const zai = getZaiClient(workspaceId, botId)
const result = await zai.extract({ from: largeDocument, to: schema })

// ❌ WRONG - Regular client will timeout on long operations
const client = getApiClient({ workspaceId, botId })
// client.someAIOperation() - likely to timeout
```

### 5. Always Type-Check Inputs

```typescript
import { z } from '@botpress/runtime'

// ✅ CORRECT - Validate input before calling
const orderSchema = z.object({
  orderId: z.string(),
})

const input = orderSchema.parse(userInput) // Throws if invalid
const result = await client.callAction({
  type: 'lookupOrder',
  input,
})

// ❌ WRONG - No validation
const result = await client.callAction({
  type: 'lookupOrder',
  input: userInput, // Might be invalid!
})
```

### 6. Handle Errors Gracefully

```typescript
// ✅ CORRECT - Specific error handling
try {
  const result = await client.callAction({ ... });
  return result.output;
} catch (error: any) {
  if (error.status === 401) {
    redirectToLogin();
  } else if (error.status === 404) {
    showNotFoundError();
  } else {
    showGenericError();
  }
  return null;
}

// ❌ WRONG - No error handling
const result = await client.callAction({ ... }); // Will crash on error
```

---

## Summary

**Key Takeaways:**

1. Use `@botpress/client` for all Botpress API interactions
2. Implement a Zustand store for client caching and reuse
3. Use bot-scoped clients (with `botId`) for bot operations
4. Use workspace-scoped clients (no `botId`) for workspace operations
5. Use `getZaiClient` with extended timeouts for AI operations
6. Always handle errors (network, auth, validation)
7. Use generated types for type safety

**Client Store Pattern Benefits:**

- Single source of truth for client configuration
- Automatic client caching and reuse
- Clean separation of workspace vs. bot-scoped operations
- Centralized authentication handling
- Easy to test and mock

**Reference Implementation:**
The `clientsStore.ts` pattern shown above (~66 lines) is production-tested and handles all common scenarios. Use it as a template for your own applications.
