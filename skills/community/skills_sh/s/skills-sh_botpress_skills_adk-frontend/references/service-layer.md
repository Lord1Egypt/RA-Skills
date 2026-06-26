# Service Layer Pattern

## Why Create a Service Layer?

A service layer sits between your UI components and the raw Botpress client, providing:

**Abstraction**: Hide low-level client APIs behind domain-specific functions

- UI calls `listTickets()` instead of `client.findTableRows({ table: "..." })`
- Changes to table names or structure only affect the service layer

**Type Safety**: Strong typing for inputs and outputs

- Extract types from action/table definitions
- TypeScript catches errors at compile time
- IntelliSense guides developers

**Reusability**: Share logic across components

- `getTicketById()` used by multiple views
- Consistent query patterns (filters, pagination)
- Single source of truth for API calls

**Testability**: Mock services instead of the entire client

- Test UI logic without real API calls
- Inject fake data easily
- Faster test execution

**Maintainability**: Centralized business logic

- One place to add logging, error handling, caching
- Easier to refactor
- Self-documenting through function names

---

## Pattern: One Service Per Domain

Organize services by domain model, not by operation type:

```
services/
├── tickets.ts        # All ticket operations
├── messages.ts       # Message queries and operations
├── message.ts        # Single message sending (could merge with messages.ts)
├── users.ts          # User management
└── tags.ts           # Tag operations (if separate domain)
```

**Each service handles:**

- Queries (reading from tables)
- Commands (calling actions)
- Type definitions for that domain

**Example layout:**

- `tickets.ts` (~150 lines): List, get, assign, snooze, open, close, update tags
- `messages.ts` (~45 lines): List messages, get latest message
- `message.ts` (~10 lines): Send single message

---

## Wrapping client.callAction()

Actions are backend operations exposed to the frontend. Wrap them with domain-specific function signatures.

### Basic Pattern

```typescript
export async function assignUserToTicket(input: AssignTicketAction['input']) {
  const result = await client.callAction({
    type: 'assignTicket',
    input,
  })
  return result.output as AssignTicketAction['output']
}
```

**Key points**:

- Function name is domain-specific (`assignUserToTicket`)
- Input type extracted from action definition (`AssignTicketAction["input"]`)
- Output type extracted and cast (`AssignTicketAction["output"]`)
- `type` matches backend action name (`"assignTicket"`) — **not** `{ type: "action", action: "..." }`

### Pattern with Custom Parameters

Sometimes you want friendlier parameters than the raw action input:

```typescript
type SnoozeTicketParams = {
  ticketId: string
  snoozeUntil: string | null
  agentId: string
}

export async function snoozeTicket({ ticketId, snoozeUntil, agentId }: SnoozeTicketParams) {
  const result = await client.callAction({
    type: 'snoozeTicket',
    input: {
      ticketId,
      agentId,
      snoozeUntil,
    },
  })
  return result.output as SnoozeTicketAction['output']
}
```

**Why custom params?**

- UI calls `snoozeTicket({ ticketId, ... })` — cleaner
- Maps to backend's expected field names
- Can add validation, defaults, transformations

### Pattern for Multiple Operations

```typescript
type OpenTicketParams = {
  ticketId: string
  agentId: string
}

export async function openTicket({ ticketId, agentId }: OpenTicketParams) {
  const result = await client.callAction({
    type: 'openTicket',
    input: { ticketId, agentId },
  })
  return result.output as OpenTicketAction['output']
}

type CloseTicketParams = {
  ticketId: string
  agentId: string
}

export async function closeTicket({ ticketId, agentId }: CloseTicketParams) {
  const result = await client.callAction({
    type: 'closeTicket',
    input: { ticketId, agentId },
  })
  return result.output as CloseTicketAction['output']
}
```

**Pattern emerges**: Similar operations share structure, just different action types.

### Pattern with Optional Fields

```typescript
type UpdateTicketTagsParams = {
  ticketId: string
  agentId: string
  tagsToAdd?: string[]
  tagsToRemove?: string[]
}

export async function updateTicketTags({ ticketId, agentId, tagsToAdd, tagsToRemove }: UpdateTicketTagsParams) {
  const result = await client.callAction({
    type: 'updateTicketTags',
    input: {
      ticketId,
      agentId,
      tagsToAdd,
      tagsToRemove,
    },
  })
  return result.output as UpdateTicketTagsAction['output']
}
```

**Optional fields**: TypeScript handles `undefined` gracefully, backend ignores them.

### Minimal Example

```typescript
export async function sendMessage(input: SendMessageAction['input']) {
  const client = getApiClient({ botId, workspaceId })
  const result = await client.callAction({ type: 'sendMessage', input })
  return result.output as SendMessageAction['output']
}
```

**When to use minimal pattern**: When the action input is already clean, no mapping needed.

---

## Wrapping client.findTableRows()

Table queries benefit from domain-specific functions with common filters and typing.

### Basic List Pattern

```typescript
type ListTicketsParams = Pick<
  Parameters<typeof client.findTableRows>[0],
  'filter' | 'group' | 'limit' | 'offset' | 'orderBy' | 'orderDirection' | 'search'
>

type TicketRow = BaseTableRow & TicketTableRow

export async function listTickets(params: ListTicketsParams) {
  const result = await client.findTableRows({
    table: 'TicketsTable',
    ...params,
  })
  return {
    ...result,
    rows: result.rows as TicketRow[],
  }
}
```

**Key points**:

- `Pick` utility extracts allowed parameters from client method signature
- `TicketRow` type combines base table fields with domain-specific fields
- Hardcoded table name — UI doesn't need to know this
- Type-cast rows to domain type

> **Note:** The `BaseTableRow` type has `id: number` (not `string`) and uses camelCase timestamps: `createdAt` and `updatedAt`.

### Get By ID Pattern

```typescript
export async function getTicketById(ticketId: string) {
  const result = await client.findTableRows({
    table: 'TicketsTable',
    filter: { ticketId },
    limit: 1,
  })
  if (!result.rows.length) {
    throw new Error(`Ticket with ID ${ticketId} not found`)
  }
  return result.rows[0] as BaseTableRow & TicketTableRow
}
```

**Pattern**:

- Simple parameter (just the ID)
- Filter to single row
- Error if not found
- Return single typed row (not array)

### Aggregation Pattern (GROUP BY)

```typescript
type TicketCountByState = Record<'open' | 'closed' | 'snoozed', number>

export async function getTicketCountsByState(filter?: Record<string, unknown>) {
  const result = await client.findTableRows({
    table: 'TicketsTable',
    group: {
      state: 'key',
      ticketId: ['count'],
    },
    filter,
  })

  const counts: TicketCountByState = {
    open: 0,
    closed: 0,
    snoozed: 0,
  }

  result.rows.forEach((row) => {
    const state = row.state as 'open' | 'closed' | 'snoozed'
    counts[state] = (row as unknown as { ticketIdCount: number }).ticketIdCount
  })

  return counts
}
```

**Aggregation pattern**:

- Use `group` parameter for SQL-like GROUP BY
- Field name + `"key"` groups by that field
- Field name + `["count"]` counts rows per group
- API returns counts as `{fieldName}Count` (camelCase)
- Transform raw rows into friendlier data structure

### List with Defaults Pattern

```typescript
type ListMessagesParams = Pick<
  Parameters<typeof client.findTableRows>[0],
  'filter' | 'group' | 'limit' | 'offset' | 'orderBy' | 'orderDirection' | 'search'
>

type MessageRow = BaseTableRow & MessageTableRow

export async function listMessages(
  ticketId: string,
  { orderBy = 'createdAt', orderDirection = 'asc', limit = 1000, ...params }: ListMessagesParams
) {
  const result = await client.findTableRows({
    table: 'MessagesTable',
    filter: { ticketId },
    orderBy,
    orderDirection,
    limit,
    ...params,
  })
  return {
    ...result,
    rows: result.rows as MessageRow[],
  }
}
```

**Pattern**:

- First parameter is required filter (ticketId)
- Second parameter is optional query params with defaults
- Merge params with defaults and required filters

### Get Latest Pattern

```typescript
export async function getLatestMessageInTicket(ticketId: string) {
  const result = await client.findTableRows({
    table: 'MessagesTable',
    filter: { ticketId, type: 'comment' },
    orderBy: 'createdAt',
    orderDirection: 'desc',
    limit: 1,
  })
  if (!result.rows.length) {
    throw new Error(`No messages found for ticket with ID ${ticketId}`)
  }
  return result.rows[0] as BaseTableRow & MessageTableRow
}
```

**Pattern**:

- Combine filter + orderBy desc + limit 1
- Returns single row (most recent)
- Error if empty

---

## Input/Output Typing

Type safety comes from extracting types from your action and table definitions.

### Action Types

```typescript
// In your types file (e.g., types/index.ts)
import type { BotActionDefinitions } from '@botpress/runtime/_types/actions'

export type SendMessageAction = BotActionDefinitions['sendMessage']
export type AssignTicketAction = BotActionDefinitions['assignTicket']
export type SnoozeTicketAction = BotActionDefinitions['snoozeTicket']
export type OpenTicketAction = BotActionDefinitions['openTicket']
export type CloseTicketAction = BotActionDefinitions['closeTicket']
export type UpdateTicketTagsAction = BotActionDefinitions['updateTicketTags']
```

**Then in services**:

```typescript
import type {
  AssignTicketAction,
  SnoozeTicketAction,
  OpenTicketAction,
  CloseTicketAction,
  UpdateTicketTagsAction,
} from '../types'

export async function assignUserToTicket(input: AssignTicketAction['input']) {
  // ...
  return result.output as AssignTicketAction['output']
}
```

### Table Types

```typescript
// In your types file
import type { TableDefinitions } from '@botpress/runtime/_types/tables'

// BaseTableRow: id is number, timestamps are camelCase
export type BaseTableRow = { id: number; createdAt: string; updatedAt: string }
export type TicketTableRow = TableDefinitions['TicketsTable']['Output']
export type MessageTableRow = TableDefinitions['MessagesTable']['Output']
```

**Then in services**:

```typescript
import type { BaseTableRow, TicketTableRow } from '../types'

type TicketRow = BaseTableRow & TicketTableRow

export async function listTickets(params: ListTicketsParams) {
  const result = await client.findTableRows({ table: 'TicketsTable', ...params })
  return {
    ...result,
    rows: result.rows as TicketRow[],
  }
}
```

### Parameter Types

Extract types from client methods using TypeScript utilities:

```typescript
type ListTicketsParams = Pick<
  Parameters<typeof client.findTableRows>[0],
  'filter' | 'group' | 'limit' | 'offset' | 'orderBy' | 'orderDirection' | 'search'
>
```

**What this does**:

- `Parameters<typeof client.findTableRows>[0]` — get first parameter type
- `Pick<..., "filter" | "group" | ...>` — extract specific fields
- Result: Type-safe parameter object matching client API

---

## Best Practices

### Consistent Naming

**Good**:

- `listTickets()` — returns array
- `getTicketById()` — returns single item or throws
- `createTicket()` — creates new
- `updateTicket()` — modifies existing
- `deleteTicket()` — removes

**Conventions**:

- `list*` for queries returning arrays
- `get*` for queries returning single items
- `create*`, `update*`, `delete*` for mutations
- `*ById` when taking ID parameter

### Error Handling

```typescript
if (!result.rows.length) {
  throw new Error(`Ticket with ID ${ticketId} not found`)
}
```

**When to throw**:

- Expected single item, got none
- Invalid parameters (validate before API call)
- Business rule violations

**When to return empty**:

- List queries (return `[]` if no results)
- Optional lookups (return `null` or `undefined`)

### Reusable Utilities

```typescript
async function findOne<T>(table: string, filter: Record<string, unknown>): Promise<T> {
  const result = await client.findTableRows({ table, filter, limit: 1 })
  if (!result.rows.length) {
    throw new Error(`No row found in ${table} with filter ${JSON.stringify(filter)}`)
  }
  return result.rows[0] as T
}

// Then use in services
export async function getTicketById(ticketId: string) {
  return findOne<TicketRow>('TicketsTable', { ticketId })
}
```

**Reusable patterns**:

- `findOne()` — Get single row or throw
- `findMany()` — Get array with defaults
- `callTypedAction()` — Wrapper for action calls with logging
- `withRetry()` — Retry failed API calls

### Client Initialization

```typescript
// Module-level client: When all functions use same config
import { getApiClient } from '../stores/clientsStore'
const client = getApiClient({ botId, workspaceId })

// Or per-function client: When config might vary
export async function sendMessage(input: SendMessageAction['input']) {
  const client = getApiClient({ botId, workspaceId })
  // ...
}
```

> **Tip:** If your project uses the ADK-generated `.adk/client.ts`, you can use `createAdkClient` for a typed wrapper that exposes actions as direct methods.

### Type Organization

```typescript
// Group related types together
type ListTicketsParams = Pick<...>;
type TicketRow = BaseTableRow & TicketTableRow;

// Define custom param types inline near the function
type SnoozeTicketParams = {
  ticketId: string;
  snoozeUntil: string | null;
  agentId: string;
};
```

**Organization**:

- Import shared types from types file
- Define query params at module level
- Define custom params near function that uses them

---

## Summary Checklist

When creating a service layer:

- [ ] One service file per domain model
- [ ] Client initialized at module level or per-function
- [ ] Import action/table types from generated definitions
- [ ] Type query parameters using `Pick<Parameters<...>>`
- [ ] Wrap `client.callAction()` with domain-specific function names
- [ ] Use `{ type: "actionName", input: {...} }` signature (not `{ type: "action", action: "..." }`)
- [ ] Cast action outputs to typed results
- [ ] Wrap `client.findTableRows()` with domain-specific queries
- [ ] Type-cast table rows to domain types (`id: number`, `createdAt`/`updatedAt`)
- [ ] Use custom param types when action inputs need mapping
- [ ] Throw errors for "get by ID" when not found
- [ ] Return empty arrays for list queries with no results
- [ ] Add defaults for common query parameters (limit, orderBy)
- [ ] Extract reusable patterns into utility functions
- [ ] Follow consistent naming conventions (list*, get*, create\*, etc.)

**Result**: Type-safe, testable, maintainable service layer that hides Botpress client complexity from UI code.

---

## See Also

- **[Calling Actions](./calling-actions.md)** — Detailed action calling patterns
- **[Type Generation](./type-generation.md)** — How types are generated and imported
- **[Botpress Client](./botpress-client.md)** — Client setup and management
- **[Data Fetching](./data-fetching.md)** — Using services with TanStack Query
- **[Overview](./overview.md)** — Architecture and key concepts
