# Calling Bot Actions from Frontend

This guide shows how to call ADK bot actions from your frontend application with production-ready patterns and examples.

## Overview

When you define an Action in your bot (e.g., `/actions/sendMessage.ts`), you can call it from your frontend using the Botpress client. The ADK automatically generates TypeScript types for all your actions, providing end-to-end type safety.

## The client.callAction() Signature

The `callAction()` method is the primary interface for executing bot actions from your frontend:

```typescript
const result = await client.callAction({
  type: "actionName",    // The name of your action (string)
  input: { ... }         // Typed input object matching your action's schema
});

// result.output contains the typed output from your action
```

**Key Points:**

- `type`: Must match the `name` field in your Action definition
- `input`: Must match the input schema defined in your Action (Zod schema)
- Returns: `{ output: TypedOutput }` where output type is inferred from your Action definition

## Setting Up the Client

First, create an API client instance with bot and workspace credentials:

```typescript
const client = new APIClient({
  apiUrl: 'https://api.botpress.cloud',
  workspaceId: props?.workspaceId,
  token: getPat() ?? '',
  botId: props?.botId,
})
```

## Type-Safe Action Calls

The ADK generates type definitions for all your actions, enabling full TypeScript support.

### Using BotActionDefinitions

```typescript
import type { BotActionDefinitions } from '@botpress/runtime/_types/actions'

// Extract specific action types for your bot's actions
export type SendMessageAction = BotActionDefinitions['sendMessage']
export type GetUserAction = BotActionDefinitions['getUser']
export type UpdateStatusAction = BotActionDefinitions['updateStatus']
export type CreateTicketAction = BotActionDefinitions['createTicket']
export type CloseTicketAction = BotActionDefinitions['closeTicket']
export type AssignAgentAction = BotActionDefinitions['assignAgent']
```

Each action type contains:

- `input`: The expected input schema type
- `output`: The returned output schema type

### Input/Output Type Inference

TypeScript automatically infers the correct types when you use these definitions:

```typescript
// ✅ TypeScript knows exactly what input fields are required
async function sendMessage(input: SendMessageAction['input']) {
  const result = await client.callAction({ type: 'sendMessage', input })
  // ✅ TypeScript knows the structure of result.output
  return result.output as SendMessageAction['output']
}
```

## Common Patterns

### 1. Simple Action Call: sendMessage

```typescript
export async function sendMessage(input: SendMessageAction['input']) {
  const client = getApiClient({ botId, workspaceId })
  const result = await client.callAction({ type: 'sendMessage', input })
  return result.output as SendMessageAction['output']
}
```

**Breakdown:**

- Creates a service wrapper function for reusability
- Uses typed input parameter for compile-time safety
- Casts output to maintain type information throughout the app
- Simple, direct action call with no additional logic

### 2. Conditional Action: assignTicket

```typescript
// If ticket is unassigned, assign it to current agent first
if (!ticket?.assignedTo?.id && currentUser?.agentId) {
  await assignTicketToAgent({
    agentId: currentUser.agentId,
    assigneeId: currentUser.agentId,
    ticketId: ticketId,
  })
}
```

**Breakdown:**

- Checks condition before calling action (only if unassigned)
- Part of a larger mutation workflow (called within `mutationFn`)
- Uses await to ensure assignment completes before continuing
- No error handling here - errors bubble up to mutation error handler

### 3. Service Wrapper Pattern: closeTicket

```typescript
type CloseTicketParams = {
  ticketId: string
  agentId: string
}

export async function closeTicket({ ticketId, agentId }: CloseTicketParams) {
  const result = await client.callAction({
    type: 'closeTicket',
    input: {
      ticketId: ticketId,
      agentId,
    },
  })
  return result.output as CloseTicketAction['output']
}
```

**Breakdown:**

- Defines custom params type for better API ergonomics
- Maps friendly parameter names to action input field names
- Centralizes client creation and action calling logic
- Type-casts output for downstream type safety

### 4. Nullable Input Fields: snoozeTicket

```typescript
type SnoozeTicketParams = {
  ticketId: string
  snoozeUntil: string | null // ← Can be null to unsnooze
  agentId: string
}

export async function snoozeTicket({ ticketId, snoozeUntil, agentId }: SnoozeTicketParams) {
  const result = await client.callAction({
    type: 'snoozeTicket',
    input: {
      ticketId: ticketId,
      agentId,
      snoozeUntil, // ← Passing null clears the snooze
    },
  })
  return result.output as SnoozeTicketAction['output']
}
```

**Breakdown:**

- Demonstrates nullable fields (snooze vs unsnooze behavior)
- Same action handles two use cases based on null value
- Type system ensures null handling is explicit

### 5. Optional Array Inputs: updateTicketTags

```typescript
type UpdateTicketTagsParams = {
  ticketId: string
  agentId: string
  tagsToAdd?: string[] // ← Optional fields
  tagsToRemove?: string[] // ← Optional fields
}

export async function updateTicketTags({ ticketId, agentId, tagsToAdd, tagsToRemove }: UpdateTicketTagsParams) {
  const result = await client.callAction({
    type: 'updateTicketTags',
    input: {
      ticketId: ticketId,
      agentId,
      tagsToAdd, // ← May be undefined
      tagsToRemove, // ← May be undefined
    },
  })
  return result.output as UpdateTicketTagsAction['output']
}
```

**Breakdown:**

- Both optional parameters allow flexible tag operations
- Can add tags only, remove tags only, or both in one call
- Undefined values are handled gracefully by the action
- Clean API that matches user intent

## Calling Actions in React Components

### With useMutation (Recommended)

React Query's `useMutation` provides loading states, error handling, and optimistic updates.

```typescript
const { mutate: send, isPending: isLoading } = useMutation({
  mutationFn: async (params: {
    content: string;
    type: "comment" | "note";
    attachmentUrls?: string[];
    attachmentFiles?: Array<{
      content_type: string;
      data: string;
      name: string;
    }>;
  }) => {
    // If ticket is unassigned, assign it to current agent first
    if (!ticket?.assignedTo?.id && currentUser?.agentId) {
      await assignTicketToAgent({
        agentId: currentUser.agentId,
        assigneeId: currentUser.agentId,
        ticketId: ticketId,
      });
    }

    return sendNewMessage({
      agentId: currentUser?.agentId ?? "",
      message: params.content,
      ticketId,
      messageType: params.type,
      attachmentUrls: params.attachmentUrls,
      attachmentFiles: params.attachmentFiles,
    });
  },
  onSuccess: () => {
    setMessage("");
    setFiles([]);
    queryClient.invalidateQueries({ queryKey: ["ticket", ticketId] });
  },
});

// Later in component...
<Button
  onClick={handleSendMessage}
  disabled={isLoading || !hasContent}
>
  <Send className="h-4 w-4" />
</Button>
```

**Breakdown:**

- `mutationFn`: Async function containing action call(s)
- `isPending`: Automatically tracks loading state for UI
- `onSuccess`: Callback for cache invalidation and UI updates
- Destructure `mutate` as `send` for cleaner component code
- Use `isLoading` to disable buttons during execution

### Direct Calls (For Non-Reactive Scenarios)

When you don't need loading states or mutations, call service functions directly:

```typescript
// In an event handler
const handleClose = async () => {
  try {
    await closeTicket({
      ticketId,
      agentId: currentUser.id,
    })
    // Update local state or redirect
    navigate('/tickets')
  } catch (error) {
    toast.error('Failed to close ticket')
  }
}
```

**When to use direct calls:**

- One-off operations without loading states
- Background operations that don't affect UI
- Server-side rendering contexts
- Utility functions outside components

## Error Handling

### Try/Catch Pattern

**Basic service-level error handling:**

```typescript
export async function assignUserToConversation(input: AssignToConversationAction['input']) {
  try {
    const result = await client.callAction({
      type: 'assignConversation',
      input,
    })
    return result.output as AssignToConversationAction['output']
  } catch (error) {
    console.error('Failed to assign conversation:', error)
    throw error // Re-throw for component-level handling
  }
}
```

### Mutation Error Handling

**Component-level error handling with useMutation:**

```typescript
const { mutate, isPending, error } = useMutation({
  mutationFn: async (params) => {
    return closeTicket(params);
  },
  onError: (error) => {
    // Show user-friendly error message
    toast.error("Failed to close ticket. Please try again.");
    console.error("Close ticket error:", error);
  },
  onSuccess: () => {
    toast.success("Ticket closed successfully");
    queryClient.invalidateQueries({ queryKey: ["tickets"] });
  },
});

// Display error in UI
{error && (
  <div className="text-red-500 text-sm mt-2">
    {error.message}
  </div>
)}
```

### User Feedback Best Practices

```typescript
const { mutate: snooze, isPending } = useMutation({
  mutationFn: snoozeTicket,
  onMutate: () => {
    // Show immediate feedback
    toast.loading('Snoozing ticket...', { id: 'snooze' })
  },
  onSuccess: () => {
    toast.success('Ticket snoozed', { id: 'snooze' })
  },
  onError: (error) => {
    toast.error(`Failed: ${error.message}`, { id: 'snooze' })
  },
})
```

## Optimistic Updates

Optimistic updates provide instant UI feedback by updating the cache before the server responds.

### Example: sendNewMessage with Optimistic Insert

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
    // Optimistic guess at the change - insert immediately into UI
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
        details: {},
        externalId: undefined,
        messageId: '',
        redacted: false,
        state: 'sent',
        updatedAt: new Date().toISOString(),
      },
      { optimistic: true } // ← Marks this as optimistic
    )
  },
  mutationFn: async (props) => {
    // Send the intent to the server
    await sendMessage({
      agentId: props.agentId,
      body: props.message,
      ticketId: props.ticketId,
      messageType: props.messageType,
      attachmentUrls: props.attachmentUrls,
      attachmentFiles: props.attachmentFiles,
    })
    // Refetch to replace optimistic data with server data
    await getTicketMessagesCollection(props.ticketId).utils.refetch()
  },
})
```

**Breakdown:**

1. **onMutate**: Immediately inserts a temporary message into the UI
2. **mutationFn**: Sends the real message to the server
3. **Refetch**: Replaces optimistic data with server response
4. If server call fails, optimistic update is automatically rolled back

**Benefits:**

- UI feels instant and responsive
- No waiting for server round-trip
- Automatic rollback on errors
- Better user experience on slow connections

### Standard useMutation Optimistic Pattern

```typescript
const { mutate: updateTags } = useMutation({
  mutationFn: updateTicketTags,
  onMutate: async (variables) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['ticket', variables.ticketId] })

    // Snapshot previous value
    const previous = queryClient.getQueryData(['ticket', variables.ticketId])

    // Optimistically update
    queryClient.setQueryData(['ticket', variables.ticketId], (old: any) => ({
      ...old,
      tags: [
        ...(old.tags || []).filter((tag: string) => !variables.tagsToRemove?.includes(tag)),
        ...(variables.tagsToAdd || []),
      ],
    }))

    return { previous } // Return context for rollback
  },
  onError: (err, variables, context) => {
    // Rollback on error
    if (context?.previous) {
      queryClient.setQueryData(['ticket', variables.ticketId], context.previous)
    }
  },
  onSettled: (data, error, variables) => {
    // Always refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['ticket', variables.ticketId] })
  },
})
```

## Chaining Multiple Actions

### Sequential Calls

When actions depend on each other, use `await`:

```typescript
mutationFn: async (params) => {
  // First action: Assign ticket
  if (!ticket?.assignedTo?.id && currentUser?.agentId) {
    await assignTicketToAgent({
      agentId: currentUser.agentId,
      assigneeId: currentUser.agentId,
      ticketId: ticketId,
    })
  }

  // Second action: Send message (depends on assignment)
  return sendNewMessage({
    agentId: currentUser?.agentId ?? '',
    message: params.content,
    ticketId,
    messageType: params.type,
    attachmentUrls: params.attachmentUrls,
    attachmentFiles: params.attachmentFiles,
  })
}
```

**When to use sequential:**

- Second action needs data from first action's output
- Actions have side effects that must complete in order
- Business logic requires specific sequence

### Parallel Calls with Promise.all

When actions are independent, run them simultaneously:

```typescript
mutationFn: async ({ ticketId, agentId, newTags, messageContent }) => {
  // Both actions can run in parallel
  const [tagResult, messageResult] = await Promise.all([
    updateTicketTags({
      ticketId,
      agentId,
      tagsToAdd: newTags,
    }),
    sendMessage({
      agentId,
      body: messageContent,
      ticketId: ticketId,
      messageType: 'comment',
    }),
  ])

  return { tagResult, messageResult }
}
```

**Benefits:**

- Faster execution (runs in parallel)
- Reduced total latency
- All-or-nothing atomicity (if one fails, both fail)

**When to use parallel:**

- Actions are completely independent
- No shared state or dependencies
- Want to minimize total execution time

### Complex Example: Multi-Step Workflow

```typescript
mutationFn: async ({ ticketId, agentId, resolution }) => {
  // Step 1: Update tags to mark as resolved
  await updateTicketTags({
    ticketId,
    agentId,
    tagsToAdd: ['resolved', resolution.category],
  })

  // Step 2: Send resolution message
  await sendMessage({
    agentId,
    body: resolution.message,
    ticketId: ticketId,
    messageType: 'comment',
  })

  // Step 3: Close ticket
  const closeResult = await closeTicket({
    ticketId,
    agentId,
  })

  // Step 4: Log to analytics (fire-and-forget)
  logResolution(ticketId, resolution).catch(console.error)

  return closeResult
}
```

## Best Practices

### 1. Always Use Service Layer

**❌ Don't call actions directly in components:**

```typescript
// Bad - direct action call in component
const handleSend = async () => {
  const client = getApiClient({ botId, workspaceId })
  const result = await client.callAction({
    type: 'sendMessage',
    input: { adminId, body: message, intercomConversationId: conversationId },
  })
}
```

**✅ Do create service functions:**

```typescript
// Good - service layer
// services/message.ts
export async function sendMessage(input: SendMessageAction['input']) {
  const client = getApiClient({ botId, workspaceId })
  const result = await client.callAction({ type: 'sendMessage', input })
  return result.output as SendMessageAction['output']
}

// Component
const handleSend = async () => {
  await sendMessage({ agentId, body: message, ticketId: ticketId })
}
```

**Why:**

- Centralized client configuration
- Easier to test and mock
- Reusable across components
- Consistent error handling

### 2. Type All Inputs/Outputs

**❌ Don't use any or lose type information:**

```typescript
// Bad - no types
async function doSomething(data: any) {
  const result = await client.callAction({ type: 'someAction', input: data })
  return result.output // ← Type is unknown
}
```

**✅ Do use generated action types:**

```typescript
// Good - full type safety
async function doSomething(input: SomeAction['input']) {
  const result = await client.callAction({ type: 'someAction', input })
  return result.output as SomeAction['output']
}
```

### 3. Handle Errors Gracefully

**✅ Always provide error handling:**

```typescript
const { mutate, error } = useMutation({
  mutationFn: sendMessage,
  onError: (error) => {
    // User feedback
    toast.error('Failed to send message')
    // Logging
    console.error('Send message error:', error)
    // Optional: Sentry/analytics
    captureException(error)
  },
})
```

### 4. Show Loading States

**✅ Disable buttons during mutations:**

```typescript
const { mutate: send, isPending } = useMutation({
  mutationFn: sendMessage,
});

return (
  <Button
    onClick={() => send(messageData)}
    disabled={isPending || !hasContent}
  >
    {isPending ? "Sending..." : "Send"}
  </Button>
);
```

### 5. Provide User Feedback

**✅ Communicate action results:**

```typescript
const { mutate } = useMutation({
  mutationFn: closeTicket,
  onSuccess: () => {
    toast.success('Ticket closed')
    navigate('/tickets')
  },
  onError: (error) => {
    toast.error(`Failed: ${error.message}`)
  },
})
```

### 6. Invalidate Queries After Mutations

**✅ Keep cache fresh:**

```typescript
const { mutate } = useMutation({
  mutationFn: updateTicketTags,
  onSuccess: (data, variables) => {
    // Invalidate specific ticket
    queryClient.invalidateQueries({
      queryKey: ['ticket', variables.ticketId],
    })
    // Invalidate list views
    queryClient.invalidateQueries({
      queryKey: ['tickets'],
    })
  },
})
```

## Common Patterns Summary

| Pattern                | Use Case                           | Example                     |
| ---------------------- | ---------------------------------- | --------------------------- |
| **Simple Call**        | Single action, no dependencies     | `sendMessage()`             |
| **Conditional Call**   | Only execute if condition met      | Assign if unassigned        |
| **Service Wrapper**    | Reusable action with custom params | All service functions       |
| **Sequential Chain**   | Actions depend on each other       | Assign → Send               |
| **Parallel Execution** | Independent actions                | Tags + Message together     |
| **Optimistic Update**  | Instant UI feedback                | Message appears immediately |
| **Error Recovery**     | Rollback on failure                | Restore previous state      |

## Additional Resources

- [ADK Actions Guide](../actions.md) - Creating actions in your bot
- [Zod Schema Validation](https://zod.dev/) - Input/output schema documentation
- [React Query Mutations](https://tanstack.com/query/latest/docs/react/guides/mutations) - Advanced mutation patterns
- [TanStack DB Collections](https://tanstack.com/db/latest) - Optimistic updates with collections

## Troubleshooting

### Action not found error

```
Error: Action "myAction" not found
```

**Fix:** Ensure action name in `callAction()` matches the `name` field in your Action definition:

```typescript
// Action definition
export default new Action({ name: "sendMessage", ... });

// Frontend call - must match exactly
client.callAction({ type: "sendMessage", ... });
```

### Type mismatch errors

```
Type 'string' is not assignable to type 'number'
```

**Fix:** Check your input matches the action's Zod schema:

```typescript
// Action expects number
input: z.object({ count: z.number() })

// ✅ Correct
client.callAction({ type: 'increment', input: { count: 5 } })

// ❌ Wrong
client.callAction({ type: 'increment', input: { count: '5' } })
```

### Missing types after adding new action

**Fix:** Regenerate types by restarting `adk dev`:

```bash
# Stop dev server
# Start again to regenerate types
adk dev
```

### Authorization errors

```
Error: Unauthorized
```

**Fix:** Verify client token and permissions:

```typescript
const client = new APIClient({
  token: getPat(), // ← Ensure token is valid
  botId: '...',
  workspaceId: '...',
})
```
