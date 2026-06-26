---
title: Single Object Signature Required
impact: HIGH
impactDescription: breaking change, all positional-arg calls must be rewritten
tags: migration, v5, signature, useQuery, useMutation
---

## Single Object Signature Required

In v5, all hooks and `queryClient` methods accept a single object argument. The legacy positional-argument overloads (e.g. `useQuery(key, fn, options)`) were removed.

**Why:** v4 supported both the positional and object forms, doubling the API surface and confusing TypeScript inference. v5 commits to one signature, simplifying types and docs.

**v4 (before):**

```typescript
useQuery(['todos'], fetchTodos, { staleTime: 5000 });

useMutation(postTodo, {
  onSuccess: () => queryClient.invalidateQueries(['todos']),
});

queryClient.invalidateQueries(['todos'], { exact: true });
queryClient.fetchQuery(['todo', id], () => fetchTodo(id));
```

**v5 (after):**

```typescript
useQuery({ queryKey: ['todos'], queryFn: fetchTodos, staleTime: 5000 });

useMutation({
  mutationFn: postTodo,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});

queryClient.invalidateQueries({ queryKey: ['todos'], exact: true });
queryClient.fetchQuery({ queryKey: ['todo', id], queryFn: () => fetchTodo(id) });
```

**Migration tip:** The official codemod handles most cases — run `npx jscodeshift@latest ./src/ --extensions=ts,tsx --transform=./node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads/remove-overloads.cjs`.
