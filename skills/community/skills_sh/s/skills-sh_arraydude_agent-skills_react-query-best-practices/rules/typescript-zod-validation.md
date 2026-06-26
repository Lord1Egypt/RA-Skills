---
title: Runtime Validation with Zod
impact: HIGH
impactDescription: catches API contract violations
tags: typescript, zod, validation, runtime
---

## Runtime Validation with Zod

Replace type assertions with runtime validation.

```typescript
import { z } from 'zod';

const todoSchema = z.object({
  id: z.number(),
  title: z.string(),
  done: z.boolean(),
  createdAt: z.string().transform(s => new Date(s)),
});

const todosSchema = z.array(todoSchema);

type Todo = z.infer<typeof todoSchema>;

async function fetchTodos(): Promise<Todo[]> {
  const response = await fetch('/api/todos');
  const data = await response.json();
  return todosSchema.parse(data); // Runtime validation
}
```

**Benefits:**
- Catches data shape mismatches at runtime
- Failed validation triggers React Query error state
- Single source of truth for types
- Type inference flows automatically
