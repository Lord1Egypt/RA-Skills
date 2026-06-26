---
title: Query Callbacks Removed from useQuery
impact: HIGH
impactDescription: breaking change, refactor required
tags: migration, v5, onSuccess, onError, onSettled, callbacks
---

## Query Callbacks Removed from useQuery

In v5, the `onSuccess`, `onError`, and `onSettled` callbacks were removed from `useQuery`. Use `useEffect` or handle in the component instead.

**Why removed:** These callbacks had subtle timing issues and didn't play well with React's concurrent features. They also encouraged mixing data fetching with side effects.

**v4 (before):**

```typescript
useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  onSuccess: (data) => {
    console.log('User loaded:', data);
    analytics.track('user_loaded');
  },
  onError: (error) => {
    toast.error(error.message);
  },
});
```

**v5 (after):**

```typescript
const { data, error } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

useEffect(() => {
  if (data) {
    console.log('User loaded:', data);
    analytics.track('user_loaded');
  }
}, [data]);

useEffect(() => {
  if (error) {
    toast.error(error.message);
  }
}, [error]);
```

**Note:** Mutation callbacks (`onSuccess`, `onError`, `onSettled`) are still available on `useMutation`.
