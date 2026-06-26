---
title: Placeholder vs Initial Data
impact: MEDIUM
impactDescription: affects caching behavior
tags: query, placeholder, initial, cache
---

## Placeholder vs Initial Data

Know when to use `initialData` (persists to cache) vs `placeholderData` (temporary).

| Aspect | initialData | placeholderData |
|--------|-------------|-----------------|
| Persists to cache | Yes | No |
| Respects staleTime | Yes | No (always refetches) |
| Scope | Cache-level (shared) | Observer-level (per component) |

**initialData: pre-fill from another query's cache**

```typescript
useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetchTodo(todoId),
  initialData: () => {
    return queryClient
      .getQueryData(['todos'])
      ?.find(todo => todo.id === todoId);
  },
  initialDataUpdatedAt: () => {
    return queryClient.getQueryState(['todos'])?.dataUpdatedAt;
  },
});
```

**placeholderData: temporary data during fetch**

```typescript
useQuery({
  queryKey: ['todo', todoId],
  queryFn: () => fetchTodo(todoId),
  placeholderData: { id: todoId, title: 'Loading...', done: false },
});

// For smooth pagination transitions
useQuery({
  queryKey: ['todos', page],
  queryFn: () => fetchTodos(page),
  placeholderData: keepPreviousData,
});
```
