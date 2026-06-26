---
title: Fetch Not Rejecting on Errors
impact: HIGH
impactDescription: silent failures
tags: troubleshoot, fetch, error, http
---

## Fetch Not Rejecting on Errors

The fetch API doesn't reject on HTTP errors.

**Incorrect (404 treated as success):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: () => fetch('/api/user').then(res => res.json()),
});
// error is always null even on 404!
```

**Correct (check response.ok):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: async () => {
    const res = await fetch('/api/user');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    return res.json();
  },
});
```

**Or use axios (rejects automatically):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user'],
  queryFn: () => axios.get('/api/user').then(res => res.data),
});
```
