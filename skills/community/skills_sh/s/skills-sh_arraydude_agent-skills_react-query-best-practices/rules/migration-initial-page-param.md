---
title: initialPageParam Required for Infinite Queries
impact: HIGH
impactDescription: breaking change, every useInfiniteQuery needs an update
tags: migration, v5, infinite, initialPageParam
---

## initialPageParam Required for Infinite Queries

In v5, every `useInfiniteQuery` must declare `initialPageParam` explicitly. Defaulting `pageParam` in the destructuring is no longer the source of truth.

**Why:** v4's pattern of `({ pageParam = 0 })` made the default invisible to React Query — it couldn't serialize, persist, or pass `pageParam` correctly without seeing it. An explicit option fixes this and improves TypeScript inference for `pageParam`.

**v4 (before):**

```typescript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: ({ pageParam = 0 }) => fetchProjects(pageParam),
  getNextPageParam: (lastPage) => lastPage.nextCursor,
});
```

**v5 (after):**

```typescript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: ({ pageParam }) => fetchProjects(pageParam),
  initialPageParam: 0,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
});
```

**Related:** `getNextPageParam` and `getPreviousPageParam` should now return `null` (not `undefined`) to indicate no more pages.
