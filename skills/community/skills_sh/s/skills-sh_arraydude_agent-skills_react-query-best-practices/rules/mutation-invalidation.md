---
title: Query Invalidation
impact: CRITICAL
impactDescription: ensures data consistency
tags: mutation, invalidation, sync, cache
---

## Query Invalidation

Invalidate related queries after mutations to trigger refetches.

**Incorrect (manual refetch):**

```typescript
const { mutate } = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    // Manual refetch - doesn't work well with multiple components
    refetch();
  },
});
```

**Correct (invalidate queries):**

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: () => {
    // Marks queries as stale, triggers refetch for active ones
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Await invalidation to keep button disabled:**

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: async () => {
    // Keep isPending true until refetch completes
    await queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});

<Button disabled={mutation.isPending}>Save</Button>
```
