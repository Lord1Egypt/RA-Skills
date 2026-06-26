---
name: best-practices-persistence
description: Persist proxy state to localStorage or other storage mechanisms
---

# Persisting State

Persist Valtio state to localStorage or other storage using `subscribe` to sync state changes.

## Basic localStorage Persistence

### JSON Serializable State

If your state is JSON serializable:

```ts
import { proxy, subscribe } from 'valtio'

const state = proxy(
  JSON.parse(localStorage.getItem('foo')) || {
    count: 0,
    text: 'hello',
  }
)

subscribe(state, () => {
  localStorage.setItem('foo', JSON.stringify(state))
})
```

### With Non-Serializable Values

For state with non-serializable values, exclude them during serialization:

```ts
import { proxy, subscribe } from 'valtio'

const state = proxy({
  count: 0,
  text: 'hello',
  // Non-serializable
  element: ref(document.getElementById('app')),
})

subscribe(state, () => {
  // Exclude non-serializable values
  const serializable = {
    count: state.count,
    text: state.text,
  }
  localStorage.setItem('foo', JSON.stringify(serializable))
})

// Load initial state
const saved = localStorage.getItem('foo')
if (saved) {
  const parsed = JSON.parse(saved)
  state.count = parsed.count
  state.text = parsed.text
  // Non-serializable values remain as initialized
}
```

## Using valtio-persist

For a more robust solution, use the `valtio-persist` library:

```ts
import { proxy } from 'valtio'
import { persist } from 'valtio-persist'

const state = proxy({
  count: 0,
  text: 'hello',
})

persist({
  name: 'my-state', // localStorage key
  state,
  // Optional: customize what to persist
  include: ['count', 'text'],
  // Optional: exclude certain keys
  exclude: ['temp'],
})
```

## Key Points

- Use `subscribe()` to sync state to storage
- Load initial state from storage when creating proxy
- Exclude non-serializable values during serialization
- Consider `valtio-persist` library for more features
- Works with any storage mechanism (localStorage, sessionStorage, IndexedDB, etc.)

<!--
Source references:
- https://valtio.pmnd.rs/docs/how-tos/how-to-persist-states
- https://github.com/pmndrs/valtio
-->
