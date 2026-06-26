---
title: remove() Method Removed from useQuery
impact: MEDIUM
impactDescription: breaking change, refactor required where used
tags: migration, v5, remove, removeQueries
---

## remove() Method Removed from useQuery

In v5, the `remove()` method on the `useQuery` result was removed. Use `queryClient.removeQueries()` instead.

**Why:** `remove()` removed the query from the cache without notifying observers, leading to inconsistent state. The explicit `removeQueries` call clarifies intent and runs through the standard cache mutation flow.

**v4 (before):**

```typescript
const query = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

const handleReset = () => {
  query.remove();
};
```

**v5 (after):**

```typescript
const queryClient = useQueryClient();
const query = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

const handleReset = () => {
  queryClient.removeQueries({ queryKey: ['todos'] });
};
```
