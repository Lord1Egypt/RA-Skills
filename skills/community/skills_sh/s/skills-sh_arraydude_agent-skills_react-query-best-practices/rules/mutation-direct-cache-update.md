---
title: Direct Cache Updates
impact: MEDIUM
impactDescription: instant UI feedback
tags: mutation, cache, setQueryData
---

## Direct Cache Updates

Update cache directly when mutation returns updated data.

**When to use:**
- Mutation returns complete updated data
- Want to avoid extra network request
- Need instant UI update

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: (updatedTodo) => {
    // Update specific item in list
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map(todo =>
        todo.id === updatedTodo.id ? updatedTodo : todo
      )
    );

    // Also update detail cache
    queryClient.setQueryData(
      ['todos', updatedTodo.id],
      updatedTodo
    );
  },
});
```

**Combined with invalidation:**

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onSuccess: (updatedTodo) => {
    // Update the specific query immediately
    queryClient.setQueryData(['todos', updatedTodo.id], updatedTodo);

    // Invalidate lists (but don't refetch inactive ones)
    queryClient.invalidateQueries({
      queryKey: ['todos', 'list'],
      refetchType: 'active',
    });
  },
});
```
