---
title: Status Check Order
impact: MEDIUM
impactDescription: proper stale-while-revalidate UX
tags: query, status, loading, error
---

## Status Check Order

Check data availability FIRST, following the stale-while-revalidate philosophy.

**Incorrect (error blocks stale data):**

```typescript
function TodoList() {
  const { data, error, isPending } = useQuery({...});

  if (isPending) return <Loading />;
  if (error) return <Error />;  // Hides stale data on background refetch error
  return <List items={data} />;
}
```

**Correct (show stale data during background errors):**

```typescript
function TodoList() {
  const { data, error, isPending } = useQuery({...});

  // Data first - show stale data during background refetch errors
  if (data) {
    return <List items={data} />;
  }

  // Then error (only when no data available)
  if (error) {
    return <Error message={error.message} />;
  }

  // Finally loading (initial load only)
  if (isPending) {
    return <Skeleton />;
  }
}
```

This ensures users see cached content even when background refetches fail.
