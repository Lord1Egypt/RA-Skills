---
title: Dependent Queries with Enabled
impact: HIGH
impactDescription: prevents unnecessary fetches
tags: query, enabled, dependent, conditional
---

## Dependent Queries with Enabled

Use the `enabled` option to control when queries run.

**Incorrect (query runs with undefined params):**

```typescript
const { data: user } = useQuery({...});

// Runs immediately with undefined userId!
const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user?.id),
});
```

**Correct (enabled option controls execution):**

```typescript
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchProjects(user!.id),
  enabled: !!user?.id, // Only fetch when user is loaded
});
```

**With skipToken (v5.25+):**

```typescript
import { skipToken } from '@tanstack/react-query';

useQuery({
  queryKey: ['user', userId],
  queryFn: userId ? () => fetchUser(userId) : skipToken,
});
```
