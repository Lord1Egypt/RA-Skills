---
title: Infinite staleTime for WS Data
impact: HIGH
impactDescription: prevents redundant fetches
tags: websocket, staleTime, configuration
---

## Infinite staleTime for WS Data

When WebSocket handles updates, disable automatic refetching.

```typescript
// Queries updated via WebSocket
useQuery({
  queryKey: ['automations', automationId],
  queryFn: () => fetchAutomation(automationId),
  staleTime: Infinity, // Manual invalidation via WebSocket
  refetchOnWindowFocus: false,
});
```

**Global configuration for WS-managed apps:**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity, // For apps fully managed by WebSocket
    },
  },
});
```

The WebSocket event handler will call `invalidateQueries` when data changes on the server.
