---
title: Reconnection Handling
impact: MEDIUM
impactDescription: ensures consistency after disconnect
tags: websocket, reconnect, fallback
---

## Reconnection Handling

Invalidate stale queries when WebSocket reconnects.

```typescript
function useWebSocketWithReconnect() {
  const queryClient = useQueryClient();
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const socket = connectWebSocket();

    socket.on('connect', () => {
      setIsConnected(true);
      // Refresh stale data after reconnection
      queryClient.invalidateQueries({
        predicate: (query) => query.state.isInvalidated,
      });
    });

    socket.on('disconnect', () => {
      setIsConnected(false);
    });

    return () => socket.disconnect();
  }, [queryClient]);

  return isConnected;
}
```

**Fallback to polling when disconnected:**

```typescript
const { data } = useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: isWebSocketConnected ? Infinity : 0,
  refetchInterval: isWebSocketConnected ? false : 5000,
});
```
