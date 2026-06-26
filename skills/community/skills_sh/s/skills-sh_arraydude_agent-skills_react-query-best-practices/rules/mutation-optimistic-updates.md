---
title: Optimistic Updates
impact: HIGH
impactDescription: instant perceived performance
tags: mutation, optimistic, rollback
---

## Optimistic Updates

Show success immediately, rollback on failure.

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,

  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos', newTodo.id] });

    // Snapshot previous value
    const previousTodo = queryClient.getQueryData(['todos', newTodo.id]);

    // Optimistically update
    queryClient.setQueryData(['todos', newTodo.id], newTodo);

    // Return context for rollback
    return { previousTodo };
  },

  onError: (err, newTodo, context) => {
    // Rollback on error
    if (context?.previousTodo) {
      queryClient.setQueryData(
        ['todos', newTodo.id],
        context.previousTodo
      );
    }
  },

  onSettled: () => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Good candidates:**
- Toggle actions (like/unlike, done/undone)
- Simple field updates
- High-confidence mutations

**Avoid for:**
- Complex operations that might fail
- Actions requiring server-side validation
