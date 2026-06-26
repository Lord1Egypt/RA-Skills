---
name: advanced-subscribe
description: Subscribe to store state changes
---

# Store Subscriptions

Subscribe to state changes for side effects, logging, or external integrations.

## $subscribe

Subscribe to all state changes:

```tsx
const store = defineStore({
  state: () => ({ count: 0 }),
})

const unsubscribe = store.$subscribe((state, opts) => {
  console.log('State changed:', state)
  console.log('Operation:', opts)
})

// Cleanup
unsubscribe()
```

**Key Points:**
* Returns an unsubscribe function
* `opts` contains operation details: `[op: 'set' | 'delete', path: Path, value, prevValue]`
* Fires on any state mutation
* Use for global state monitoring or persistence

## $subscribeKey

Subscribe to changes of a specific state key:

```tsx
const unsubscribe = store.$subscribeKey('count', (value) => {
  console.log('Count changed:', value)
})

unsubscribe()
```

**Key Points:**
* More efficient than `$subscribe` when only watching one property
* Only fires when the specified key changes
* Useful for syncing specific state to external systems

## Usage Patterns

### Logging

```tsx
store.$subscribe((state) => {
  console.log('[Store]', state)
})
```

### External Sync

```tsx
store.$subscribeKey('user', (user) => {
  syncToBackend(user)
})
```

### Cleanup in React

```tsx
useEffect(() => {
  const unsubscribe = store.$subscribe((state) => {
    // handle change
  })
  return unsubscribe
}, [])
```
