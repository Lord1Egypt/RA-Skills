---
title: Copying Query Data to State
impact: HIGH
impactDescription: breaks single source of truth
tags: troubleshoot, state, anti-pattern
---

## Copying Query Data to State

Never copy query results to local state.

**Incorrect (duplicated state):**

```typescript
const { data } = useQuery({ queryKey: ['user'], queryFn: fetchUser });
const [user, setUser] = useState(data);

useEffect(() => {
  if (data) setUser(data);
}, [data]);
```

**Why it's wrong:**
- Breaks single source of truth
- Loses automatic background updates
- Creates synchronization bugs

**Correct (use query data directly):**

```typescript
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
});

// For derived state, use select
const { data: userName } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
  select: (user) => user.name,
});
```

If you need global access, use queryClient directly:

```typescript
const userData = queryClient.getQueryData(['user']);
```
