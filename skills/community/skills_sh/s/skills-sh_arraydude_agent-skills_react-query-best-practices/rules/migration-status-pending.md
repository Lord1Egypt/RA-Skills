---
title: Status "loading" Renamed to "pending"
impact: HIGH
impactDescription: breaking change, find-replace required across all queries
tags: migration, v5, status, isPending, isLoading
---

## Status "loading" Renamed to "pending"

In v5, the query status `'loading'` was renamed to `'pending'`, and the derived flag `isLoading` was redefined. The previous `isInitialLoading` is now `isLoading`.

**Why:** The status `'pending'` more accurately reflects that the query has no data yet (it isn't necessarily fetching). `isLoading` now means "pending AND fetching", matching the common intuition.

**v4 (before):**

```typescript
const { status, isLoading, isInitialLoading } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

if (status === 'loading') return <Spinner />;
if (isInitialLoading) return <Spinner />;
```

**v5 (after):**

```typescript
const { status, isPending, isLoading } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

if (status === 'pending') return <Spinner />;
// isLoading in v5 === isInitialLoading in v4 (pending AND fetching)
if (isLoading) return <Spinner />;
```

**Migration checklist:**
- Replace `status === 'loading'` with `status === 'pending'`
- Replace `isInitialLoading` with `isLoading`
- Audit existing `isLoading` usage — semantics changed (now requires fetching too)
- Mutations: `isLoading` → `isPending`
