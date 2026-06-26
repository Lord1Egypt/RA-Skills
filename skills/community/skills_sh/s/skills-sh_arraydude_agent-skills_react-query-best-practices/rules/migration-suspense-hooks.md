---
title: New Dedicated Suspense Hooks
impact: HIGH
impactDescription: new API for suspense mode
tags: migration, v5, suspense, useSuspenseQuery
---

## New Dedicated Suspense Hooks

In v5, suspense mode uses dedicated hooks instead of the `suspense` option. This provides better TypeScript inference since data is guaranteed to be defined.

**v4 (before):**

```typescript
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  suspense: true,
});

// data is TData | undefined (TypeScript doesn't know suspense guarantees data)
```

**v5 (after):**

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

const { data } = useSuspenseQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});

// data is TData (guaranteed by suspense, TypeScript knows this)
```

**Available suspense hooks in v5:**
- `useSuspenseQuery` - Single query with suspense
- `useSuspenseInfiniteQuery` - Infinite query with suspense
- `useSuspenseQueries` - Multiple queries with suspense

**Benefits:**
- Better TypeScript support (data is never undefined)
- Clearer intent in code
- No need for `suspense: true` option
