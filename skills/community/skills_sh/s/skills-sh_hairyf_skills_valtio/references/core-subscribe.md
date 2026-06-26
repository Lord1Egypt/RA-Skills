---
name: core-subscribe
description: Subscribe to proxy state changes from anywhere, including module scope and vanilla JavaScript
---

# Subscribe

`subscribe` allows you to listen to state changes from anywhere - module scope, vanilla JavaScript, or outside React components. This enables side effects, persistence, and integration with non-React code.

## Usage

### Basic Subscription

```ts
import { proxy, subscribe } from 'valtio'

const state = proxy({ count: 0 })

// Subscribe to all changes
const unsubscribe = subscribe(state, () => {
  console.log('state changed:', state)
})

// Unsubscribe when done
unsubscribe()
```

### Subscribing to Portions

You can subscribe to nested proxies:

```ts
const state = proxy({
  obj: { foo: 'bar' },
  arr: ['hello'],
})

subscribe(state.obj, () => {
  console.log('state.obj changed:', state.obj)
})

subscribe(state.arr, () => {
  console.log('state.arr changed:', state.arr)
})

state.obj.foo = 'baz' // Triggers obj subscription
state.arr.push('world') // Triggers arr subscription
```

### Module Scope Subscriptions

Subscribe in module scope for side effects:

```ts
// store.ts
import { proxy, subscribe } from 'valtio'

export const state = proxy({
  todos: [],
  filter: 'all',
})

// Persist to localStorage
subscribe(state, () => {
  localStorage.setItem('todos', JSON.stringify(state))
})

// Load initial state
const saved = localStorage.getItem('todos')
if (saved) {
  Object.assign(state, JSON.parse(saved))
}
```

### Vanilla JavaScript

Valtio works in vanilla JavaScript - import from `valtio/vanilla`:

```ts
import { proxy, subscribe, snapshot } from 'valtio/vanilla'

const state = proxy({ count: 0, text: 'hello' })

subscribe(state, () => {
  console.log('state mutated')
  const obj = snapshot(state) // Immutable object
  // Update DOM, etc.
})
```

## Advanced: Subscribe Ops

For advanced scenarios like synchronization or undo/redo, you can listen to detailed operation records:

```ts
import { subscribe } from 'valtio'

// Enable ops tracking (has small performance cost)
subscribe(
  state,
  () => {
    console.log('state changed')
  },
  { ops: true }
)
```

See [Subscribe Ops](./subscribe-ops) for more details on using operations.

## Key Points

- `subscribe()` works from anywhere - module scope, vanilla JS, outside components
- Subscribe to entire proxy or nested portions
- Returns unsubscribe function
- Useful for persistence, side effects, and non-React integration
- Import from `valtio/vanilla` for vanilla JavaScript
- Can enable ops tracking for detailed change information

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/advanced/subscribe
- https://github.com/pmndrs/valtio
-->
