---
title: Select Option for Transformations
impact: MEDIUM
impactDescription: enables partial subscriptions
tags: query, select, transform, optimization
---

## Select Option for Transformations

Use the `select` option for data transformations. It only runs when data exists and enables render optimizations.

**Incorrect (transform in queryFn):**

```typescript
useQuery({
  queryKey: ['todos'],
  queryFn: async () => {
    const todos = await fetchTodos();
    return todos.filter(todo => !todo.done); // Runs every time
  },
});
```

**Correct (use select option):**

```typescript
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => data.filter(todo => !todo.done),
});

// Components only re-render when selected slice changes
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => data.length, // Only re-render when count changes
});
```

For expensive transforms, stabilize with useCallback:

```typescript
const selectActiveTodos = useCallback(
  (data: Todo[]) => data.filter(todo => !todo.done),
  []
);

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: selectActiveTodos,
});
```
