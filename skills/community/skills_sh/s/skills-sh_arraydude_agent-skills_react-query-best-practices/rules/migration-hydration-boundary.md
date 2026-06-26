---
title: Hydrate Component Renamed to HydrationBoundary
impact: MEDIUM
impactDescription: breaking change for SSR/Next.js apps
tags: migration, v5, hydrate, HydrationBoundary, ssr, nextjs
---

## Hydrate Component Renamed to HydrationBoundary

In v5, the `<Hydrate>` component was renamed to `<HydrationBoundary>`. The `useHydrate` hook was removed.

**Why:** "Hydrate" clashed with React's `hydrate` API, causing confusion and import collisions in SSR setups (especially Next.js App Router).

**v4 (before):**

```typescript
import { Hydrate, QueryClientProvider } from '@tanstack/react-query';

export function Providers({ children, dehydratedState }) {
  return (
    <QueryClientProvider client={queryClient}>
      <Hydrate state={dehydratedState}>
        {children}
      </Hydrate>
    </QueryClientProvider>
  );
}
```

**v5 (after):**

```typescript
import { HydrationBoundary, QueryClientProvider } from '@tanstack/react-query';

export function Providers({ children, dehydratedState }) {
  return (
    <QueryClientProvider client={queryClient}>
      <HydrationBoundary state={dehydratedState}>
        {children}
      </HydrationBoundary>
    </QueryClientProvider>
  );
}
```
