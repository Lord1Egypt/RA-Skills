---
name: core-proxy
description: Create proxy state objects that track changes and notify subscribers
---

# Proxy

The `proxy` function creates a reactive state object that tracks changes to the original object and all nested objects, notifying listeners when any part is modified.

## Usage

### Basic Proxy

```ts
import { proxy } from 'valtio'

const state = proxy({ count: 0, text: 'hello' })
```

### Mutating State

You can mutate the proxy like a normal JavaScript object:

```ts
// Direct mutation
state.count = 1
state.text = 'world'

// Array mutations
state.items = []
state.items.push({ id: 1, name: 'Item' })

// Nested mutations
state.user.name = 'John'
```

### Mutations Outside Components

One of Valtio's key benefits is mutating state outside React components:

```ts
const state = proxy({ count: 0 })

// Mutate from anywhere - timers, event handlers, etc.
setInterval(() => {
  ++state.count
}, 1000)

// Mutate in module scope
export const increment = () => {
  ++state.count
}
```

## Optimizations

### No-op Updates

Updates that set a property to the same value are ignored:

```ts
const state = proxy({ count: 0 })
state.count = 0 // No effect, subscribers not notified
```

### Batching

Multiple changes in the same event loop tick are batched together:

```ts
const state = proxy({ count: 0, text: 'hello' })
// Subscribers notified once after both mutations
state.count = 1
state.text = 'world'
```

## Nested Proxies

Proxies can be nested and updated as a whole:

```ts
const personState = proxy({ name: 'Timo', role: 'admin' })
const authState = proxy({ status: 'loggedIn', user: personState })

// Mutating nested proxy updates parent
authState.user.name = 'Nina' // authState subscribers notified
```

## Promises in Proxies

Promises can be values in proxies and will be resolved in `snapshot` calls:

```ts
const state = proxy({
  data: new Promise((resolve) => 
    setTimeout(() => resolve('Boom!'), 3000)
  ),
})
```

## Classes

Classes can be proxied, maintaining methods and getters:

```ts
class User {
  first = null
  last = null
  constructor(first: string, last: string) {
    this.first = first
    this.last = last
  }
  greet() {
    return `Hi ${this.first}!`
  }
  get fullName() {
    return `${this.first} ${this.last}`
  }
}

const state = proxy(new User('Timo', 'Kivinen'))
state.first = 'Nina' // Updates tracked
```

## Gotchas

### Don't Reassign the Proxy

Reassigning the proxy to a new object breaks reactivity:

```ts
let state = proxy({ user: { name: 'Timo' } })

// ❌ Wrong - breaks reactivity
state = { user: { name: 'Nina' } }

// ✅ Correct - mutate properties
state.user.name = 'Nina'
```

### Unproxied Objects

Some objects cannot be proxied (use `ref()` for these):

```ts
// ❌ These won't work - changes won't be tracked
const state = proxy({
  chart: d3.select('#chart'),
  component: React.createElement('div'),
  map: new Map(), // Use proxyMap instead
  storage: localStorage,
})

// ✅ Use ref() for unproxied objects
import { proxy, ref } from 'valtio'
const state = proxy({
  nativeMap: ref(new Map()),
})
```

## Key Points

- `proxy()` creates reactive state that tracks all nested changes
- Mutate like normal JavaScript objects
- Updates are batched in the same event loop tick
- Same-value assignments are ignored (no-op)
- Nested objects become proxies automatically
- Classes, promises, and most serializable objects work
- Use `ref()` for objects that can't be proxied (Maps, Sets, DOM elements)

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/basic/proxy
- https://github.com/pmndrs/valtio
-->
