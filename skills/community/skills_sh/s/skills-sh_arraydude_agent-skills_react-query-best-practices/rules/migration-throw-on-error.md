---
title: useErrorBoundary Renamed to throwOnError
impact: MEDIUM
impactDescription: breaking change, find-replace required
tags: migration, v5, useErrorBoundary, throwOnError, errorBoundary
---

## useErrorBoundary Renamed to throwOnError

In v5, the `useErrorBoundary` option was renamed to `throwOnError` on both queries and mutations.

**Why:** "useErrorBoundary" sounded like a hook, which conflicted with React conventions. `throwOnError` describes what the option actually does — re-throw the error so a surrounding boundary catches it — and works across frameworks (Solid, Vue) without React-specific terminology.

**v4 (before):**

```typescript
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  useErrorBoundary: true,
});

useMutation({
  mutationFn: postTodo,
  useErrorBoundary: (error) => error.status >= 500,
});
```

**v5 (after):**

```typescript
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  throwOnError: true,
});

useMutation({
  mutationFn: postTodo,
  throwOnError: (error) => error.status >= 500,
});
```

**Migration:** Find-replace `useErrorBoundary` → `throwOnError` across the codebase.
