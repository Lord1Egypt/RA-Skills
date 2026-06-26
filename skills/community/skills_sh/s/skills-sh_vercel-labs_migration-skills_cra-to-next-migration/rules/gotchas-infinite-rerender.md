---
title: Prevent Infinite Re-render Loops
impact: HIGH
impactDescription: Object/array dependencies in useEffect cause infinite loops
tags: gotchas, performance, useEffect, useMemo, dependencies
---

## Prevent Infinite Re-render Loops

Object and array references change on every render. Using them directly as `useEffect` dependencies causes infinite re-render loops.

**Problem: Array dependency creates new reference each render**

```tsx
// BAD - New array reference every render causes infinite loop
function Component({ data }) {
  const items = data.map(d => d.id); // New array each render

  useEffect(() => {
    doSomething(items);
  }, [items]); // items reference changed -> effect runs -> re-render -> repeat

  return <List items={items} />;
}
```

**Solution 1: Memoize with useMemo**

```tsx
// GOOD - Memoized array only changes when data changes
function Component({ data }) {
  const items = useMemo(() => data.map(d => d.id), [data]);

  useEffect(() => {
    doSomething(items);
  }, [items]); // Stable reference

  return <List items={items} />;
}
```

**Solution 2: Use primitive dependency**

```tsx
// BETTER - Primitive value as dependency
function Component({ data }) {
  const itemsKey = data.map(d => d.id).join(',');

  useEffect(() => {
    const items = data.map(d => d.id);
    doSomething(items);
  }, [itemsKey, data]); // String comparison is stable

  return <List items={data.map(d => d.id)} />;
}
```

**Problem: Object state dependency**

```tsx
// BAD - Any state change triggers effect
const [state, setState] = useState({ message: '', count: 0 });

useEffect(() => {
  if (state.message) showToast(state.message);
}, [state]); // Triggers when count changes too!
```

**Solution: Depend on specific primitive**

```tsx
// GOOD - Only triggers when message changes
useEffect(() => {
  if (state.message) showToast(state.message);
}, [state.message]); // Primitive dependency
```

**Problem: Inline object in dependency**

```tsx
// BAD - New object reference every render
useEffect(() => {
  fetchData({ page, limit });
}, [{ page, limit }]); // Always new reference!
```

**Solution: Spread primitives or memoize**

```tsx
// GOOD - Primitive dependencies
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);

// OR - Memoized options object
const options = useMemo(() => ({ page, limit }), [page, limit]);
useEffect(() => {
  fetchData(options);
}, [options]);
```

**Problem: Function dependency recreated each render**

```tsx
// BAD - handleData recreated every render
function Component() {
  const handleData = (data) => process(data);

  useEffect(() => {
    fetchData().then(handleData);
  }, [handleData]); // Re-runs every render!
}
```

**Solution: useCallback or ref pattern**

```tsx
// GOOD - Stable function reference
function Component() {
  const handleData = useCallback((data) => process(data), []);

  useEffect(() => {
    fetchData().then(handleData);
  }, [handleData]);
}

// BETTER for one-time effects - Skip dependency entirely
function Component() {
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    fetchData().then(process);
  }, []); // Empty deps for one-time effect
}
```

**Quick reference: Dependency patterns**

| Dependency Type | Problem | Solution |
|-----------------|---------|----------|
| Array from `.map()` | New reference each render | `useMemo` or primitive key |
| Object state | Triggers on unrelated changes | Use specific property |
| Inline object `{}` | Always new reference | Spread primitives |
| Inline function | Always new reference | `useCallback` |
| Props that are objects | Parent re-renders cause loops | `useMemo` in parent or primitive deps |

**Debug tip:**

```tsx
// Add this to find what's causing re-renders
useEffect(() => {
  console.log('Effect triggered');
}, [suspiciousDependency]);

// Or use React DevTools Profiler to see what's changing
```
