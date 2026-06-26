---
title: refetchPage Replaced by maxPages
impact: MEDIUM
impactDescription: breaking change for infinite queries
tags: migration, v5, infinite, refetchPage, maxPages
---

## refetchPage Replaced by maxPages

In v5, the `refetchPage` function (which let you choose which pages to refetch in an infinite query) was removed. Use the new `maxPages` option to bound the number of pages stored, so refetches stay manageable.

**Why:** Refetching only some pages caused inconsistent data. Bounding the number of pages produces predictable behavior and naturally limits work on refetch.

**v4 (before):**

```typescript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: fetchProjectsPage,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
  refetchPage: (_lastPage, index) => index < 2,
});
```

**v5 (after):**

```typescript
useInfiniteQuery({
  queryKey: ['projects'],
  queryFn: fetchProjectsPage,
  initialPageParam: 0,
  getNextPageParam: (lastPage) => lastPage.nextCursor,
  maxPages: 3,
});
```

**Note:** With `maxPages` set, fetching beyond the limit drops the oldest page. Refetches always include all stored pages.
