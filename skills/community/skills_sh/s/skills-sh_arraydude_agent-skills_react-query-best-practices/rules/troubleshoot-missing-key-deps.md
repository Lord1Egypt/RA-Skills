---
title: Missing Query Key Dependencies
impact: CRITICAL
impactDescription: causes cache collisions
tags: troubleshoot, keys, dependencies, cache
---

## Missing Query Key Dependencies

Always include all queryFn parameters in the query key.

**Incorrect (filters not in key):**

```typescript
const [filters, setFilters] = useState({ status: 'active' });

useQuery({
  queryKey: ['todos'], // Missing filters!
  queryFn: () => fetchTodos(filters),
});
```

**Problems:**
- Cache collision between different filter states
- Stale closure bugs
- Race conditions

**Correct (include all dependencies):**

```typescript
useQuery({
  queryKey: ['todos', filters],
  queryFn: () => fetchTodos(filters),
});
```

**Use query key factories for consistency:**

```typescript
const todoKeys = {
  list: (filters: Filters) => ['todos', 'list', filters] as const,
};

// Usage
useQuery({
  queryKey: todoKeys.list(filters),
  queryFn: () => fetchTodos(filters),
});
```
