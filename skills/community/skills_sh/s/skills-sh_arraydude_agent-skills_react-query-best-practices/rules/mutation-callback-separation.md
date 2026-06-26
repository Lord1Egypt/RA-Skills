---
title: Callback Separation Pattern
impact: MEDIUM
impactDescription: separation of concerns
tags: mutation, callback, hook, component
---

## Callback Separation Pattern

Place query logic in hook, UI effects in component.

**Custom hook - query-related logic:**

```typescript
export function useUpdateTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateTodo,
    onSuccess: (data) => {
      // Query cache updates here
      queryClient.setQueryData(['todos', data.id], data);
      queryClient.invalidateQueries({ queryKey: ['todos', 'list'] });
    },
    onError: (error) => {
      // Logging here
      console.error('Update failed:', error);
    },
  });
}
```

**Component - UI effects:**

```typescript
function TodoEditor() {
  const { mutate } = useUpdateTodo();

  const handleSave = () => {
    mutate(todoData, {
      onSuccess: () => {
        toast.success('Saved!');
        closeModal();
      },
      onError: () => {
        toast.error('Save failed');
      },
    });
  };
}
```

This pattern keeps hooks reusable and components focused on UI concerns.
