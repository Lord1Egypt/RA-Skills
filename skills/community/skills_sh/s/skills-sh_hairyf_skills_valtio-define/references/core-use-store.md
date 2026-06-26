---
name: use-store
description: React hook for accessing store state in components
---

# useStore

React hook that returns a reactive snapshot of the store state. Automatically re-renders components when accessed state changes.

## Usage

```tsx
import { defineStore, useStore } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0 }),
  actions: {
    increment() { this.count++ },
  },
  getters: {
    doubled() { return this.count * 2 },
  },
})

function Counter() {
  const state = useStore(store)
  
  return (
    <div>
      <div>Count: {state.count}</div>
      <div>Doubled: {state.doubled}</div>
      <button onClick={store.increment}>Increment</button>
    </div>
  )
}
```

## Key Points

* **Reactive**: Component automatically re-renders when accessed state properties change.
* **Snapshot**: Returns a snapshot (read-only) of the state. Use actions or `$patch` to modify state.
* **Getters Included**: Getters are automatically included in the returned snapshot.
* **Actions Not Included**: Actions are not included in the snapshot - access them directly from the store instance.

## Accessing Actions

Actions must be accessed from the store instance, not from the snapshot:

```tsx
function Component() {
  const state = useStore(store)
  
  // ✅ Correct - access action from store
  <button onClick={store.increment}>Increment</button>
  
  // ❌ Wrong - actions not in snapshot
  // <button onClick={state.increment}>Increment</button>
}
```

## Type Inference

The hook properly infers types including state, getters, and actions:

```tsx
const state = useStore(store)
// state.count: number
// state.doubled: number
// state.increment: undefined (actions not in snapshot)
```
