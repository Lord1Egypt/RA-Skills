# Performance Optimization

## Optimization Patterns

- `useMemo`: Expensive computations (filter, sort, map)
- `useCallback`: Event handlers passed to children
- `React.memo`: Expensive components
- Debounced search (300-500ms)
- Memory leak prevention (cleanup in useEffect)

## Code Splitting

- Split code by route or feature
- Lazy load components and assets
- Use dynamic imports

## Example

```typescript
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

<Suspense fallback={<SuspenseLoader />}>
    <HeavyComponent />
</Suspense>
```
