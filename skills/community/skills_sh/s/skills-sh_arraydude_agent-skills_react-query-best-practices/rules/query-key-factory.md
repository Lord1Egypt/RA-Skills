---
title: Query Key Factory Pattern
impact: HIGH
impactDescription: enables flexible invalidation
tags: query, keys, factory, pattern
---

## Query Key Factory Pattern

Use factory functions to generate consistent query keys. Structure: generic to specific.

**Incorrect (inconsistent key strings):**

```typescript
// Scattered key definitions
useQuery({ queryKey: ['todos'] });
useQuery({ queryKey: ['todo', id] });
queryClient.invalidateQueries({ queryKey: ['todos'] }); // Might miss some
```

**Correct (centralized key factory):**

```typescript
const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filters: Filters) => [...todoKeys.lists(), filters] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: number) => [...todoKeys.details(), id] as const,
};

// Usage
useQuery({
  queryKey: todoKeys.detail(todoId),
  queryFn: () => fetchTodo(todoId),
});

// Flexible invalidation
queryClient.invalidateQueries({ queryKey: todoKeys.all });        // All todos
queryClient.invalidateQueries({ queryKey: todoKeys.lists() });    // All lists
queryClient.invalidateQueries({ queryKey: todoKeys.detail(5) });  // Specific todo
```

The hierarchical structure enables invalidating at any level of specificity.
