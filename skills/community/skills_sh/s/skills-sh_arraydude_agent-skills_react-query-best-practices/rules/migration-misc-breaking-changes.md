---
title: Misc v5 Breaking Changes
impact: LOW
impactDescription: smaller breaking changes worth auditing
tags: migration, v5, misc, react18, retry, hashKey, isDataEqual
---

## Misc v5 Breaking Changes

A grab-bag of smaller v5 breaking changes that are easy to miss:

### React 18 minimum

v5 requires **React 18.0+** because it depends on `useSyncExternalStore`. Apps still on React 17 must upgrade React first.

### Server-side retries default to 0

When running queries on the server (SSR/RSC), the default `retry` is now `0` instead of `3`. This avoids long render delays when a backend service is down. Override per-query if needed.

### `getNextPageParam` / `getPreviousPageParam` should return `null`

Returning `undefined` to signal "no more pages" still works but is deprecated. Prefer `null`:

```typescript
// v5 preferred
getNextPageParam: (lastPage) => lastPage.nextCursor ?? null,
```

### `hashQueryKey` renamed to `hashKey`

```typescript
// v4
import { hashQueryKey } from '@tanstack/react-query';
// v5
import { hashKey } from '@tanstack/react-query';
```

It now hashes mutation keys too, hence the rename.

### `isDataEqual` removed — use `structuralSharing`

```typescript
// v4
useQuery({ queryKey, queryFn, isDataEqual: customCheck });

// v5
import { replaceEqualDeep } from '@tanstack/react-query';
useQuery({
  queryKey,
  queryFn,
  structuralSharing: (oldData, newData) =>
    customCheck(oldData, newData) ? oldData : replaceEqualDeep(oldData, newData),
});
```

### Manual `pageParam` override removed

You can no longer pass a `pageParam` to `fetchNextPage()` / `fetchPreviousPage()`. Drive page params through `getNextPageParam` / `getPreviousPageParam` only.

### `setQueryDefaults` now merges

When multiple registered defaults match a query, v5 merges them (previously the most specific won outright). Register from **most generic → most specific** so later, more-specific defaults override.
