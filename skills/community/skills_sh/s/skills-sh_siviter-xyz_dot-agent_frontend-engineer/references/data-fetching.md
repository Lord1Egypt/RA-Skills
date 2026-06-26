# Data Fetching

## PRIMARY PATTERN: useSuspenseQuery

- Use with Suspense boundaries
- Cache-first strategy (check grid cache before API)
- Replaces `isLoading` checks
- Type-safe with generics

## API Service Layer

- Create `features/{feature}/api/{feature}Api.ts`
- Use `apiClient` axios instance
- Centralized methods per feature
- Route format: `/form/route` (NOT `/api/form/route`)

## Example

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';

const { data } = useSuspenseQuery({
    queryKey: ['feature', id],
    queryFn: () => featureApi.getFeature(id),
});
```

## CRITICAL RULE: No Early Returns

```typescript
// ❌ NEVER - Causes layout shift
if (isLoading) {
    return <LoadingSpinner />;
}

// ✅ ALWAYS - Consistent layout
<SuspenseLoader>
    <Content />
</SuspenseLoader>
```

**Why:** Prevents Cumulative Layout Shift (CLS), better UX
