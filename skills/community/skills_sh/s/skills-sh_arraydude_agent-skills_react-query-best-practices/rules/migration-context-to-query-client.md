---
title: Custom context Prop Replaced by queryClient Argument
impact: LOW
impactDescription: breaking change for apps with multiple QueryClients
tags: migration, v5, context, queryClient, micro-frontend
---

## Custom context Prop Replaced by queryClient Argument

In v5, the `context` option was removed. Pass a custom `QueryClient` instance directly as the second argument to hooks instead.

**Why:** Custom contexts existed mainly for micro-frontend isolation. Passing the client explicitly is more direct, type-safe, and avoids React context plumbing.

**v4 (before):**

```typescript
const customContext = React.createContext<QueryClient | undefined>(undefined);

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  context: customContext,
});
```

**v5 (after):**

```typescript
import { customQueryClient } from './my-client';

useQuery(
  { queryKey: ['todos'], queryFn: fetchTodos },
  customQueryClient,
);
```
