---
title: cacheTime Renamed to gcTime
impact: HIGH
impactDescription: breaking change, find-replace required
tags: migration, v5, cacheTime, gcTime
---

## cacheTime Renamed to gcTime

In v5, `cacheTime` was renamed to `gcTime` to better reflect its purpose: it controls when unused/inactive cache entries are garbage collected.

**v4 (before):**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      cacheTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  cacheTime: 1000 * 60 * 10, // 10 minutes
});
```

**v5 (after):**

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  gcTime: 1000 * 60 * 10, // 10 minutes
});
```

**Migration:** Find and replace all occurrences of `cacheTime` with `gcTime` in your codebase.
