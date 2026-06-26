---
title: Type Inference Strategy
impact: MEDIUM
impactDescription: cleaner code, fewer errors
tags: typescript, inference, generics
---

## Type Inference Strategy

Type the queryFn, not the hook. Let TypeScript infer.

**Incorrect (explicit generics):**

```typescript
// Unnecessary and error-prone
const { data } = useQuery<Todo[], Error>({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
```

**Correct (type the function):**

```typescript
// Type flows automatically
async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  return response.json();
}

const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
// data is Todo[] | undefined
```

**With select, inference still works:**

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (todos) => todos.length,
});
// data is number | undefined
```

Use the Query Options API for type-safe abstractions:

```typescript
const todoQueries = {
  detail: (id: number) => queryOptions({
    queryKey: ['todos', 'detail', id] as const,
    queryFn: () => fetchTodo(id),
  }),
};

// Type automatically inferred
const data = queryClient.getQueryData(todoQueries.detail(5).queryKey);
// data is Todo | undefined
```
