---
name: best-practices-state-composition
description: Split and compose proxy states for better organization
---

# State Composition

Valtio allows you to split and compose states flexibly. You can create nested states, combine separate states, and even create circular structures.

## Splitting States

You can split a state with nested objects into separate pieces:

```ts
const state = proxy({
  obj1: { a: 1 },
  obj2: { b: 2 },
})

// Split into separate proxies
const obj1State = state.obj1
const obj2State = state.obj2

// Both are proxies and can be used independently
subscribe(obj1State, () => console.log('obj1 changed'))
subscribe(obj2State, () => console.log('obj2 changed'))
```

## Combining States

You can create separate states and combine them:

```ts
const obj1State = proxy({ a: 1 })
const obj2State = proxy({ b: 2 })

// Combine into parent state
const state = proxy({
  obj1: obj1State,
  obj2: obj2State,
})

// Mutations on child states notify parent
obj1State.a = 2 // state subscribers also notified
```

This works equivalently to the nested approach above.

## Circular Structures

While less common, you can create circular structures:

```ts
const state = proxy({
  obj: { foo: 3 },
})

state.obj.bar = state.obj // Circular reference
```

## Use Cases

### Feature-Based State Organization

```ts
// Separate feature states
const authState = proxy({ user: null, token: null })
const cartState = proxy({ items: [], total: 0 })
const uiState = proxy({ theme: 'light', sidebar: true })

// Combine in app state
const appState = proxy({
  auth: authState,
  cart: cartState,
  ui: uiState,
})
```

### Modular State Management

```ts
// user.ts
export const userState = proxy({ name: '', email: '' })

// cart.ts
export const cartState = proxy({ items: [] })

// app.ts
import { userState } from './user'
import { cartState } from './cart'

export const appState = proxy({
  user: userState,
  cart: cartState,
})
```

## Key Points

- Split nested states into separate proxy references
- Combine separate states into parent state
- Mutations on child states notify parent subscribers
- Useful for feature-based organization
- Enables modular state management
- Circular structures are supported but use with caution

<!--
Source references:
- https://valtio.pmnd.rs/docs/how-tos/how-to-split-and-compose-states
- https://github.com/pmndrs/valtio
-->
