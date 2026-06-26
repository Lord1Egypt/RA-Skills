---
title: Tracked Properties
impact: LOW
impactDescription: reduces unnecessary re-renders
tags: query, optimization, rerender
---

## Tracked Properties

React Query tracks which properties you access during render. Only destructure what you need.

**Incorrect (rest spread tracks all fields):**

```typescript
// Tracks ALL fields, defeats optimization
const { data, ...rest } = useQuery({...});
```

**Correct (explicit destructuring):**

```typescript
// Only tracks data and isError
const { data, isError } = useQuery({...});
```

The component won't re-render when untracked fields like `isFetching` change.
