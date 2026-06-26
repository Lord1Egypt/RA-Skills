---
name: guides-computed-properties
description: Create computed properties using object and class getters and setters
---

# Computed Properties

Valtio supports object and class getters and setters to create computed properties. Getters are re-evaluated on each access on the proxy, but are cached in snapshots.

## Usage

### Object Getters

```ts
const state = proxy({
  count: 1,
  get doubled() {
    return this.count * 2
  },
})

console.log(state.doubled) // 2

// Getter calls on snapshot work and are cached
const snap = snapshot(state)
console.log(snap.doubled) // 2

// When count changes
state.count = 10
// Snapshot's computed property doesn't change (it's cached)
console.log(snap.doubled) // 2 (still from when snapshot was taken)
```

### Object Getters and Setters

```ts
const state = proxy({
  count: 1,
  get doubled() {
    return this.count * 2
  },
  set doubled(newValue) {
    this.count = newValue / 2
  },
})

// Setter works on proxy
state.doubled = 4
console.log(state.count) // 2

// Getter on snapshot
const snap = snapshot(state)
console.log(snap.doubled) // 4

// Setter on snapshot fails (snapshots are readonly)
// snap.doubled = 2 // Error: Cannot assign to read only property
```

### Class Getters and Setters

```ts
class Counter {
  count = 1
  get doubled() {
    return this.count * 2
  }
  set doubled(newValue) {
    this.count = newValue / 2
  }
}

const state = proxy(new Counter())
const snap = snapshot(state)

state.doubled = 4
console.log(state.count) // 2
console.log(snap.doubled) // 2 (re-evaluated, not cached like object getters)
```

## Important Restrictions

### Reference Sibling Properties Only

Getters should only reference **sibling** properties via `this`:

```ts
// ✅ OK - references sibling property
const user = proxy({
  name: 'John',
  get greetingEn() {
    return 'Hello ' + this.name
  },
})

// ✅ OK - nested but references sibling
const state = proxy({
  user: {
    name: 'John',
    get greetingEn() {
      return 'Hello ' + this.name
    },
  },
})

// ❌ WRONG - `this` points to wrong object
const state = proxy({
  user: { name: 'John' },
  greetings: {
    get greetingEn() {
      return 'Hello ' + this.user.name // `this` is `greetings`, not `state`
    },
  },
})
```

### Workarounds

#### Attach Related Object

```ts
const user = proxy({ name: 'John' })
const greetings = proxy({
  user, // Attach the user proxy
  get greetingEn() {
    return 'Hello ' + this.user.name // ✅ Works
  },
})
```

#### Use subscribe

```ts
const user = proxy({ name: 'John' })
const greetings = proxy({
  greetingEn: 'Hello ' + user.name,
})

subscribe(user, () => {
  greetings.greetingEn = 'Hello ' + user.name
})
```

## Caching with proxy-memoize

For caching getter results on the proxy itself, use `proxy-memoize`:

```ts
import { memoize } from 'proxy-memoize'

const memoizedDoubled = memoize((snap) => snap.count * 2)

const state = proxy({
  count: 1,
  text: 'hello',
  get doubled() {
    return memoizedDoubled(snapshot(state))
  },
})

// When `text` changes but `count` doesn't, memoized function won't re-execute
```

## Key Points

- Use object/class getters for computed properties
- Getters on proxy: re-evaluated each access
- Getters on snapshot: cached (object) or re-evaluated (class)
- Setters work on proxy, fail on snapshot (readonly)
- Only reference sibling properties via `this`
- Use `proxy-memoize` for caching on proxy
- Attach related objects or use `subscribe` for cross-object references

<!--
Source references:
- https://valtio.pmnd.rs/docs/guides/computed-properties
- https://github.com/pmndrs/valtio
-->
