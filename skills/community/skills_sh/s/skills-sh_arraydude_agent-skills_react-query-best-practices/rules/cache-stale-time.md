---
title: Setting staleTime
impact: HIGH
impactDescription: reduces unnecessary refetches
tags: cache, staleTime, configuration
---

## Setting staleTime

Set appropriate `staleTime` based on how often your data changes.

**Recommended defaults:**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2, // 2 minutes
      gcTime: 1000 * 60 * 5,    // 5 minutes (formerly cacheTime)
      retry: 3,
    },
  },
});
```

**Per-query overrides:**

```typescript
// Frequently changing data
useQuery({
  queryKey: ['notifications'],
  queryFn: fetchNotifications,
  staleTime: 1000 * 30, // 30 seconds
});

// Rarely changing data
useQuery({
  queryKey: ['config'],
  queryFn: fetchConfig,
  staleTime: 1000 * 60 * 30, // 30 minutes
});

// WebSocket-managed data
useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: Infinity, // Manual invalidation via WebSocket
});
```
