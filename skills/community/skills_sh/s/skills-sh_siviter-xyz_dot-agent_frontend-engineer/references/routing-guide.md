# Routing Guide

## TanStack Router - Folder-Based

- Directory: `routes/my-route/index.tsx`
- Lazy load components
- Use `createFileRoute`
- Breadcrumb data in loader

## Example

```typescript
import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));

export const Route = createFileRoute('/my-route/')({
    component: MyPage,
    loader: () => ({ crumb: 'My Route' }),
});
```
