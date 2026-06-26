---
name: define-store
description: Core API for creating reactive stores with state, actions, and getters
---

# defineStore

Creates a reactive store factory similar to Pinia, built on top of Valtio.

## Usage

```tsx
import { defineStore } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0, name: 'test' }),
  actions: {
    increment() {
      this.count++
    },
    setName(name: string) {
      this.name = name
    },
  },
  getters: {
    doubled() {
      return this.count * 2
    },
  },
})
```

## Key Points

* **State**: Can be an object or a factory function `() => S`. Factory functions are useful for creating fresh state instances.
* **Actions**: Methods that have access to `this` bound to the store state. Actions are automatically bound and accessible directly on the store instance.
* **Getters**: Computed properties that automatically track dependencies. Accessible as properties on the store state.
* **Type Safety**: Full TypeScript support with proper inference for state, actions, and getters.

## Store Instance

The returned store instance provides:

* Direct access to state properties: `store.count`
* Direct access to actions: `store.increment()`
* Direct access to getters: `store.doubled`
* Internal methods prefixed with `$`: `$state`, `$patch`, `$subscribe`, etc.

## State Factory vs Object

```tsx
// Factory function - creates fresh state each time
const store1 = defineStore({
  state: () => ({ count: 0 }),
})

// Object - shared state reference
const store2 = defineStore({
  state: { count: 0 },
})
```

Use factory functions when you need multiple independent store instances. Use objects for singleton stores.
