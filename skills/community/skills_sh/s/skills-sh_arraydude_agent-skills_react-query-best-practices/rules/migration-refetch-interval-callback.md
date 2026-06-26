---
title: refetchInterval Callback Signature Changed
impact: LOW
impactDescription: breaking change for dynamic polling intervals
tags: migration, v5, refetchInterval, polling
---

## refetchInterval Callback Signature Changed

In v5, the `refetchInterval` callback receives only the `query` object — no longer `(data, query)`. Read `data` from `query.state.data`.

**Why:** Aligns with other callback signatures (e.g. `refetchOnWindowFocus`) and removes the data/query staleness mismatch that could occur when the two arguments disagreed.

**v4 (before):**

```typescript
useQuery({
  queryKey: ['job', id],
  queryFn: () => fetchJob(id),
  refetchInterval: (data, query) =>
    data?.status === 'done' ? false : 5000,
});
```

**v5 (after):**

```typescript
useQuery({
  queryKey: ['job', id],
  queryFn: () => fetchJob(id),
  refetchInterval: (query) =>
    query.state.data?.status === 'done' ? false : 5000,
});
```
