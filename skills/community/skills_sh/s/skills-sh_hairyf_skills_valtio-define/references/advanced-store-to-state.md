---
name: advanced-store-to-state
description: Convert store state to React useState-like hooks
---

# storeToState and storeToStates

Convert store state to React hooks similar to `useState`, providing a more React-idiomatic API for individual state properties.

## storeToState

Returns a `[state, setter]` tuple for a single store key:

```tsx
import { defineStore, storeToState } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0, name: 'test' }),
})

function Counter() {
  const [count, setCount] = storeToState(store, 'count')
  const [name, setName] = storeToState(store, 'name')

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(prev => prev + 1)}>Functional</button>
      <div>Count: {count}</div>
      <input value={name} onChange={e => setName(e.target.value)} />
    </div>
  )
}
```

**Key Points:**
* Returns `[value, setter]` tuple like `useState`
* Setter accepts value or updater function: `setCount(5)` or `setCount(prev => prev + 1)`
* Component re-renders when the specific key changes
* Type-safe with proper inference

## storeToStates

Returns an object with all store keys mapped to `[state, setter]` tuples:

```tsx
import { storeToStates } from 'valtio-define'

function Component() {
  const {
    count: [count, setCount],
    name: [name, setName],
    user: [user, setUser],
  } = storeToStates(store)

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <div>Count: {count}</div>
      <div>Name: {name}</div>
      <div>User: {user.name}</div>
    </div>
  )
}
```

**Key Points:**
* Destructure all state properties at once
* Each property gets its own `[value, setter]` tuple
* Useful when accessing multiple store properties
* Preserves correct types for each property

## When to Use

**Use storeToState/storeToStates when:**
* Prefer `useState`-like API
* Need fine-grained reactivity (only re-render when specific key changes)
* Working with form inputs or controlled components

**Use useStore when:**
* Need access to getters
* Simpler API is preferred
* Accessing multiple properties (less boilerplate)

## Pattern Comparison

```tsx
// storeToState - useState-like
const [count, setCount] = storeToState(store, 'count')

// useStore - simpler but re-renders on any accessed property change
const state = useStore(store)
// Use store.$patch or actions to update
```
