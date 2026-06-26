# Data Fetching with TanStack Query

This guide covers data fetching patterns for ADK frontend applications using TanStack Query. It also introduces TanStack DB Collections as an advanced, optional layer for real-time UIs.

## Table of Contents

- [TanStack Query Setup](#tanstack-query-setup)
- [Basic Queries (useQuery)](#basic-queries-usequery)
- [Mutations (useMutation)](#mutations-usemutation)
- [Advanced: TanStack DB Collections](#advanced-tanstack-db-collections)
- [Optimistic Actions Pattern](#optimistic-actions-pattern)
- [Collection Features](#collection-features)
- [Best Practices](#best-practices)

## TanStack Query Setup

### Installation

```bash
pnpm add @tanstack/react-query
# For advanced collections (optional)
pnpm add @tanstack/db @tanstack/query-db-collection
```

### QueryClient Configuration

Create a query client instance with sensible defaults:

**File: `src/lib/query-client.ts`**

```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
    },
  },
})
```

### Provider Setup

Wrap your application with `QueryClientProvider`:

**File: `src/main.tsx`**

```typescript
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/query-client";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Your app components */}
    </QueryClientProvider>
  );
}
```

## Basic Queries (useQuery)

### Querying Bot Tables

Use `useQuery` to fetch data from your bot's tables via your service layer:

```typescript
import { useQuery } from "@tanstack/react-query";
import { listTickets } from "../services/tickets";

function TicketList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["tickets"],
    queryFn: async () => {
      return listTickets({
        filter: { state: "open" },
        limit: 100,
      });
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data.rows.map((ticket) => (
        <li key={ticket.id}>{ticket.title}</li>
      ))}
    </ul>
  );
}
```

> **Note:** Service functions wrap `client.findTableRows()` — there is no `listTableRows` method on the client.

### Query Keys

Query keys uniquely identify queries and control caching:

```typescript
// Static key
queryKey: ['tickets']

// Dynamic key with parameters
queryKey: ['ticket', ticketId]

// Complex key with filters
queryKey: ['tickets', { status: 'open', limit: 50 }]
```

**Rules:**

- Include all parameters that affect the data
- Use array format for nested dependencies
- Keep keys consistent across your app

### Refetch Strategies

Control when queries refetch:

```typescript
const { data } = useQuery({
  queryKey: ['tickets'],
  queryFn: fetchTickets,
  refetchInterval: 3000, // Refetch every 3 seconds
  refetchOnWindowFocus: true, // Refetch when window regains focus
  staleTime: 5000, // Consider data fresh for 5 seconds
})
```

## Mutations (useMutation)

### Calling Bot Actions

Use `useMutation` to trigger bot actions:

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { sendMessage } from "../services/message";

function SendMessageForm({ ticketId }: { ticketId: string }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (message: string) => {
      return sendMessage({
        ticketId,
        body: message,
        agentId: currentUser.agentId,
        messageType: "comment",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["messages", ticketId] });
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        mutation.mutate(formData.get("message") as string);
      }}
    >
      <input name="message" />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Sending..." : "Send"}
      </button>
      {mutation.isError && <div>Error: {mutation.error.message}</div>}
    </form>
  );
}
```

> **Important:** The correct `callAction` signature is `{ type: "actionName", input: {...} }`. Do **not** use `{ type: "action", action: "actionName", input: {...} }`.

### Optimistic Updates (onMutate)

Update UI immediately before the server responds:

```typescript
const mutation = useMutation({
  mutationFn: sendMessage,
  onMutate: async (newMessage) => {
    await queryClient.cancelQueries({ queryKey: ['messages', ticketId] })

    const previousMessages = queryClient.getQueryData(['messages', ticketId])

    queryClient.setQueryData(['messages', ticketId], (old: any) => ({
      ...old,
      rows: [...old.rows, newMessage],
    }))

    return { previousMessages }
  },
  onError: (err, newMessage, context) => {
    queryClient.setQueryData(['messages', ticketId], context?.previousMessages)
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['messages', ticketId] })
  },
})
```

### Invalidation and Refetching

After mutations, invalidate affected queries:

```typescript
// Invalidate specific query
queryClient.invalidateQueries({ queryKey: ['tickets'] })

// Invalidate all queries starting with "ticket"
queryClient.invalidateQueries({ queryKey: ['ticket'] })

// Refetch immediately
queryClient.refetchQueries({ queryKey: ['tickets'] })
```

## Advanced: TanStack DB Collections

> **Note:** TanStack DB Collections are an **advanced, optional** layer. Start with plain `useQuery` + `useMutation` — add Collections only if you need real-time local-first features.

### What are Collections?

**TanStack DB Collections** provide:

- **Autocompleted local state**: Instant UI updates before server confirmation
- **Automatic server sync**: Background synchronization with your bot's tables
- **Query-like API**: Built on TanStack Query with additional mutation features
- **Optimistic actions**: First-class support for optimistic updates

Collections are ideal for real-time interfaces like chat applications, dashboards, and collaborative tools.

### Installation

```bash
pnpm add @tanstack/db @tanstack/query-db-collection
```

### createCollection Pattern

Basic collection setup:

```typescript
import { createCollection } from '@tanstack/db'
import { queryCollectionOptions } from '@tanstack/query-db-collection'
import { queryClient } from './lib/query-client'
import { listTickets } from './services/tickets'

export const ticketsCollection = createCollection(
  queryCollectionOptions({
    queryKey: ['tickets'],
    queryFn: async () => {
      return listTickets({
        filter: { state: { $in: ['open', 'snoozed'] } },
        limit: 1000,
        orderBy: 'updatedAt',
        orderDirection: 'desc',
      })
    },
    queryClient,
    refetchInterval: 3000,
    select: (data) => data.rows,
    getKey: (item) => item.id,
  })
)
```

### Different Refetch Intervals

Not all data needs the same refresh rate:

```typescript
// Active data the user is watching — fast refresh
export const activeTicketsCollection = createCollection(
  queryCollectionOptions({
    queryKey: ['active-tickets'],
    queryFn: async () => listTickets({ filter: { state: { $in: ['open', 'snoozed'] } } }),
    queryClient,
    refetchInterval: 1000 * 3, // 3 seconds
    select: (data) => data.rows,
    getKey: (item) => item.id,
  })
)

// Closed items — slow refresh
export const closedTicketsCollection = createCollection(
  queryCollectionOptions({
    queryKey: ['closed-tickets'],
    queryFn: async () => listTickets({ filter: { state: 'closed' } }),
    queryClient,
    refetchInterval: 1000 * 30, // 30 seconds
    select: (data) => data.rows,
    getKey: (item) => item.id,
  })
)
```

### Parameterized Collections

**Messages for a specific ticket**, with factory pattern:

```typescript
function createMessagesCollection(ticketId?: string) {
  return createCollection(
    queryCollectionOptions({
      queryKey: ['messages', ticketId],
      enabled: !!ticketId,
      queryFn: async () => {
        if (!ticketId) return { rows: [] }
        return listMessages(ticketId, {
          limit: 1000,
          orderBy: 'createdAt',
          orderDirection: 'asc',
        })
      },
      queryClient,
      refetchInterval: 1000, // 1 second for chat messages
      select: (data) => data.rows,
      getKey: (item) => item.id,
    })
  )
}

// Cache collections by ID to avoid recreating
const messagesCollections = new Map()

export function getTicketMessagesCollection(ticketId?: string) {
  const cacheKey = ticketId || '__undefined__'
  if (!messagesCollections.has(cacheKey)) {
    messagesCollections.set(cacheKey, createMessagesCollection(ticketId))
  }
  return messagesCollections.get(cacheKey)
}
```

**Key features:**

- Factory function for dynamic parameters
- Map-based caching prevents duplicate collections
- `enabled` flag prevents premature fetching
- Very fast refetch (1 second) for chat messages

## Optimistic Actions Pattern

> **Note:** `createOptimisticAction` is a **custom pattern** you define in your project. It is not part of the TanStack Query API. It combines `useMutation`-style logic with Collection inserts for instant UI updates.

### How It Works

Optimistic actions combine instant UI updates with server synchronization:

1. **onMutate**: Updates UI immediately with predicted state
2. **mutationFn**: Sends request to server
3. **Auto-refetch**: Syncs real server state after success

### Example: sendNewMessage

```typescript
export const sendNewMessage = createOptimisticAction<{
  message: string
  agentId: string
  ticketId: string
  messageType: 'comment' | 'note'
  attachmentUrls?: string[]
  attachmentFiles?: Array<{
    content_type: string
    data: string
    name: string
  }>
}>({
  onMutate: (props) => {
    // Step 1: Insert optimistic entry — instant UI update
    getTicketMessagesCollection(props.ticketId).insert(
      {
        id: Math.floor(Math.random() * 1000000000), // Temporary ID
        content: props.message,
        author: { id: props.agentId, type: 'agent' },
        attachments: [],
        computed: {},
        ticketId: props.ticketId,
        type: props.messageType,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        details: {},
        external_id: undefined,
        messageId: '',
        redacted: false,
        state: 'sent',
      },
      { optimistic: true }
    )
  },
  mutationFn: async (props) => {
    // Step 2: Send real API call
    await sendMessage({
      agentId: props.agentId,
      body: props.message,
      ticketId: props.ticketId,
      messageType: props.messageType,
      attachmentUrls: props.attachmentUrls,
      attachmentFiles: props.attachmentFiles,
    })

    // Step 3: Refetch to get real server state
    await getTicketMessagesCollection(props.ticketId).utils.refetch()
  },
})
```

**How it works:**

1. **User sends message** → Calls `sendNewMessage.mutate({ message: "Hello", ... })`
2. **onMutate fires immediately** → Message appears in UI instantly with temporary ID
3. **mutationFn sends to server** → Actual API call happens in background
4. **Refetch after success** → Real message data replaces optimistic version
5. **If error occurs** → Optimistic message automatically removed

### Using Optimistic Actions

```typescript
import { sendNewMessage } from "./collections";

function ChatInput({ ticketId, agentId }: Props) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    sendNewMessage.mutate({
      message,
      agentId,
      ticketId,
      messageType: "comment",
    });
    setMessage("");
  };

  return (
    <div>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

## Collection Features

### Auto-Refetching

Control update frequency based on data characteristics:

```typescript
// Real-time data (chat messages, notifications)
refetchInterval: 1000 // 1 second

// Frequently changing data (active tickets)
refetchInterval: 1000 * 3 // 3 seconds

// Background updates (analysis, reports)
refetchInterval: 1000 * 5 // 5 seconds

// Slow-changing data (closed items, archives)
refetchInterval: 1000 * 30 // 30 seconds

// Very slow changes (admin lists, settings)
refetchInterval: 1000 * 60 * 5 // 5 minutes
```

**Guidelines:**

- Faster = better UX, but higher server load
- Match interval to actual update frequency
- Consider user expectations (chat vs. analytics)

### Getting Unique Keys

Collections need unique identifiers for tracking changes:

```typescript
getKey: (item) => item.id // Use ID field
getKey: (item) => item.key // Use key field
getKey: (item) => `${item.type}-${item.id}` // Composite key
```

### Dynamic Collections

Create collections based on runtime parameters:

```typescript
// Factory function
function createMessagesCollection(ticketId?: string) {
  return createCollection(
    queryCollectionOptions({
      queryKey: ['messages', ticketId],
      enabled: !!ticketId,
      queryFn: async () => {
        if (!ticketId) return { rows: [] }
        return listMessages(ticketId)
      },
      // ... other options
    })
  )
}

// Caching factory results
const collectionsCache = new Map()

export function getMessagesCollection(ticketId?: string) {
  const cacheKey = ticketId || '__undefined__'
  if (!collectionsCache.has(cacheKey)) {
    collectionsCache.set(cacheKey, createMessagesCollection(ticketId))
  }
  return collectionsCache.get(cacheKey)
}

// Usage
const messages = getMessagesCollection(ticketId).useQuery()
```

### Collection Utilities

Collections expose useful utilities:

```typescript
const collection = ticketsCollection

// Manual refetch
await collection.utils.refetch()

// Insert item
collection.insert(newItem, { optimistic: true })

// Get current data
const data = collection.utils.getData()
```

## Best Practices

### Query Key Conventions

Organize keys hierarchically:

```typescript
// Good: Hierarchical, predictable
;['tickets'][('tickets', 'open')][('tickets', ticketId)][('tickets', ticketId, 'messages')][ // All tickets // Open tickets // Single ticket // Ticket messages
  // Bad: Flat, hard to invalidate
  'openTickets'
]['ticketMessages123']
```

### Refetch Intervals (Active vs Background)

Choose intervals based on context:

```typescript
// Active/foreground data
refetchInterval: 1000 * 3 // 3 seconds

// Background data
refetchInterval: 1000 * 30 // 30 seconds

// Or use focus-aware intervals
refetchInterval: (query) => {
  return document.hasFocus() ? 1000 * 3 : 1000 * 30
}
```

### Optimistic Updates for Instant UX

When to use optimistic updates:

**Good candidates:**

- Chat messages
- Status changes
- Simple data updates
- High-confidence success rate

**Avoid for:**

- Complex validations
- Server-side computations
- Critical operations (payments)
- Uncertain outcomes

### Error Boundaries

Wrap components using queries/collections:

```typescript
import { ErrorBoundary } from "react-error-boundary";

function App() {
  return (
    <ErrorBoundary
      fallback={<div>Something went wrong</div>}
      onError={(error) => {
        console.error("Query error:", error);
      }}
    >
      <TicketList />
    </ErrorBoundary>
  );
}
```

### Loading States

Handle loading and error states consistently:

```typescript
function TicketList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["tickets"],
    queryFn: () => listTickets({ filter: { state: "open" } }),
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data?.rows.length) return <EmptyState />;

  return (
    <ul>
      {data.rows.map((item) => (
        <TicketItem key={item.id} ticket={item} />
      ))}
    </ul>
  );
}
```

### TypeScript Types

Define types for your data:

```typescript
import { z } from 'zod'

const ticketSchema = z.object({
  id: z.number(),
  title: z.string(),
  status: z.enum(['open', 'closed', 'snoozed']),
  updatedAt: z.string(),
})

type Ticket = z.infer<typeof ticketSchema>
```

### Separation of Concerns

Organize data fetching separately from UI:

```
src/
├── services/          # API calls to bot
│   ├── tickets.ts
│   └── messages.ts
├── collections/       # TanStack collections (optional)
│   └── index.ts
├── components/        # UI components
│   ├── TicketList.tsx
│   └── MessageThread.tsx
└── lib/
    ├── query-client.ts
    └── bot-client.ts
```

**Services layer:**

```typescript
// services/tickets.ts
export async function listTickets(params: ListParams) {
  return client.findTableRows({
    table: 'TicketsTable',
    ...params,
  })
}
```

**Component layer:**

```typescript
// components/TicketList.tsx
import { listTickets } from '../services/tickets'

export function TicketList() {
  const { data } = useQuery({
    queryKey: ['tickets'],
    queryFn: () => listTickets({ limit: 100 }),
  })
  // ...
}
```

---

## Summary

**TanStack Query** provides a solid foundation for data fetching in ADK frontends:

- **useQuery**: Fetch and cache data from bot tables (via `findTableRows`)
- **useMutation**: Trigger bot actions (via `callAction`) with invalidation
- **Optimistic updates**: Instant UI feedback before server confirmation

**TanStack DB Collections** (advanced/optional) add features for real-time interfaces:

- **Autocompleted state**: Local changes sync automatically
- **createCollection**: Simplified setup with query-like API
- **Optimistic actions**: First-class support via custom `createOptimisticAction` pattern
- **Factory patterns**: Dynamic collections with caching

Choose the right tool:

- **Basic queries** → `useQuery` + `useMutation`
- **Real-time dashboards** → TanStack DB Collections
- **Chat interfaces** → Collections + optimistic actions
- **Background sync** → Longer refetch intervals

---

## See Also

- **[Service Layer](./service-layer.md)** — Building the service functions used by queries
- **[Calling Actions](./calling-actions.md)** — Detailed `callAction` patterns
- **[Real-Time Updates](./realtime-updates.md)** — Polling strategies and performance
- **[State Management](./state-management.md)** — When to use Zustand vs TanStack Query
- **[Botpress Client](./botpress-client.md)** — Client setup and management
