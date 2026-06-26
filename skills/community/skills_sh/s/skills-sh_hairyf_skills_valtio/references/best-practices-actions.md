---
name: best-practices-actions
description: Organize actions for mutating proxy state - various patterns and recommendations
---

# Organizing Actions

Valtio is unopinionated about organizing actions. Here are various patterns you can use.

## Action Functions in Module (Recommended)

**Preferred for code splitting:**

```ts
import { proxy } from 'valtio'

export const state = proxy({
  count: 0,
  name: 'foo',
})

export const inc = () => {
  ++state.count
}

export const setName = (name: string) => {
  state.name = name
}
```

## Action Object in Module

```ts
import { proxy } from 'valtio'

export const state = proxy({
  count: 0,
  name: 'foo',
})

export const actions = {
  inc: () => {
    ++state.count
  },
  setName: (name: string) => {
    state.name = name
  },
}
```

## Action Methods in State

```ts
export const state = proxy({
  count: 0,
  name: 'foo',
  inc: () => {
    ++state.count
  },
  setName: (name: string) => {
    state.name = name
  },
})
```

## Action Methods Using `this`

```ts
export const state = proxy({
  count: 0,
  name: 'foo',
  inc() {
    ++this.count
  },
  setName(name: string) {
    this.name = name
  },
})
```

## Using Classes

```ts
class State {
  count = 0
  name = 'foo'
  inc() {
    ++this.count
  }
  setName(name: string) {
    this.name = name
  }
}

export const state = proxy(new State())
```

## Key Points

- Module-level functions are preferred for code splitting
- Actions can be methods on the state object
- Classes work well for organizing related state and actions
- Use `this` in methods to reference state
- Choose pattern based on your team's preferences and code splitting needs

<!--
Source references:
- https://valtio.pmnd.rs/docs/how-tos/how-to-organize-actions
- https://github.com/pmndrs/valtio
-->
