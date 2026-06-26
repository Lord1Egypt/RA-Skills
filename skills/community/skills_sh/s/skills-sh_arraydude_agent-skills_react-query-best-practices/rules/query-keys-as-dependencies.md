---
title: Query Keys as Dependencies
impact: CRITICAL
impactDescription: prevents cache collisions and stale closures
tags: query, keys, dependencies, cache
---

## Query Keys as Dependencies

Include ALL variables used in queryFn as part of the queryKey. Query keys work like useEffect dependencies.

**Incorrect (filters not in queryKey):**

```typescript
const [filters, setFilters] = useState({ status: 'active' });

useQuery({
  queryKey: ['todos'], // Missing filters!
  queryFn: () => fetchTodos(filters),
});
```

This causes cache collisions between different filter states and stale closure bugs.

**Correct (all dependencies included):**

```typescript
useQuery({
  queryKey: ['todos', filters], // Key changes when filters change
  queryFn: () => fetchTodos(filters),
});
```

Key changes automatically trigger refetches. This is the declarative pattern React Query is built for.
