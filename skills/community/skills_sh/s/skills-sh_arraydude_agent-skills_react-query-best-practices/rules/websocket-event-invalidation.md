---
title: Event-Based Invalidation
impact: HIGH
impactDescription: simple, predictable
tags: websocket, invalidation, realtime
---

## Event-Based Invalidation

Push lightweight events from backend, not full data objects.

```typescript
// Backend sends events like:
// { "entity": ["automations", "list"] }
// { "entity": ["automations", "detail"], "id": "abc123" }

function useWebSocketSync() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const socket = connectWebSocket();

    socket.on('invalidate', (event) => {
      queryClient.invalidateQueries({
        queryKey: event.entity,
      });
    });

    return () => socket.disconnect();
  }, [queryClient]);
}
```

**Example pattern (entity-specific WebSocket handler):**

```typescript
const handleMessage = useCallback((message: WebSocketMessage) => {
  switch (message.type) {
    case 'AUTOMATION_UPDATED':
      queryClient.invalidateQueries({
        queryKey: ['automations', message.automationId],
      });
      break;

    case 'AUTOMATION_STATUS_CHANGED':
      // Direct cache update for frequent status changes
      queryClient.setQueryData(
        ['automations', message.automationId],
        (old) => old ? { ...old, status: message.status } : old
      );
      break;

    case 'AUTOMATION_LIST_CHANGED':
      queryClient.invalidateQueries({
        queryKey: ['automations', 'list'],
      });
      break;
  }
}, [queryClient]);
```
