---
title: keepPreviousData Replaced by placeholderData Function
impact: HIGH
impactDescription: breaking change, common in pagination/filtering UIs
tags: migration, v5, keepPreviousData, placeholderData, pagination
---

## keepPreviousData Replaced by placeholderData Function

In v5, the `keepPreviousData` boolean option and `isPreviousData` flag were removed. Use `placeholderData` with the exported `keepPreviousData` identity function instead. The flag is now `isPlaceholderData`.

**Why:** `placeholderData` and `keepPreviousData` overlapped conceptually. Unifying them into one option simplifies the mental model — both "show something while we fetch" cases now go through `placeholderData`.

**v4 (before):**

```typescript
const { data, isPreviousData } = useQuery({
  queryKey: ['projects', page],
  queryFn: () => fetchProjects(page),
  keepPreviousData: true,
});
```

**v5 (after):**

```typescript
import { keepPreviousData } from '@tanstack/react-query';

const { data, isPlaceholderData } = useQuery({
  queryKey: ['projects', page],
  queryFn: () => fetchProjects(page),
  placeholderData: keepPreviousData,
});
```

**Migration:** Find `keepPreviousData: true` and replace with `placeholderData: keepPreviousData` (imported from `@tanstack/react-query`). Rename `isPreviousData` to `isPlaceholderData`.
