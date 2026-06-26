---
title: Refetch Triggers
impact: HIGH
impactDescription: data freshness
tags: cache, refetch, windowFocus, reconnect
---

## Refetch Triggers

Keep refetch triggers enabled in production. They're features, not bugs.

**Incorrect (over-disabling):**

```typescript
useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  refetchOnMount: false,
  refetchOnWindowFocus: false,
  refetchOnReconnect: false,
  staleTime: Infinity,
});
// Data never updates automatically!
```

**Correct (appropriate configuration):**

```typescript
// Most queries: keep defaults
useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  staleTime: 1000 * 60 * 5, // 5 minutes
  // refetchOnWindowFocus: true (default)
  // refetchOnMount: true (default)
});

// Only disable for truly static or WebSocket-managed data
useQuery({
  queryKey: ['automations', id],
  queryFn: () => fetchAutomation(id),
  staleTime: Infinity,
  refetchOnWindowFocus: false, // WebSocket handles this
});
```
