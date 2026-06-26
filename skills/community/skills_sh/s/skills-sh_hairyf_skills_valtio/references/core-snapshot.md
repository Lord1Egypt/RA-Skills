---
name: core-snapshot
description: Create immutable snapshots of proxy state for efficient comparison and React Suspense support
---

# Snapshot

`snapshot` takes a proxy and returns an immutable, frozen object unwrapped from the proxy. Snapshots use copy-on-write optimization and work with React Suspense.

## Usage

### Basic Snapshot

```ts
import { proxy, snapshot } from 'valtio'

const state = proxy({ name: 'Mika' })
const snap1 = snapshot(state) // Immutable copy
const snap2 = snapshot(state)
console.log(snap1 === snap2) // true - same reference if unchanged

state.name = 'Hanna'
const snap3 = snapshot(state)
console.log(snap1 === snap3) // false - new reference when changed
```

### Copy-on-Write Optimization

Snapshots use lazy copy-on-write, only copying changed parts:

```ts
const author = proxy({
  firstName: 'f',
  lastName: 'l',
  books: [{ title: 't1' }, { title: 't2' }],
})

const s1 = snapshot(author)
author.books[1].title = 't2b'
const s2 = snapshot(author)

console.log(s1 === s2) // false
console.log(s1.books === s2.books) // false
console.log(s1.books[0] === s2.books[0]) // true - reused unchanged
console.log(s1.books[1] === s2.books[1]) // false - new copy
```

This means snapshot cost is based on *depth* (typically low) not *breadth* (thousands of items).

## Classes

Snapshots maintain original object prototypes, so methods and getters work:

```ts
class Author {
  firstName = 'f'
  lastName = 'l'
  fullName() {
    return `${this.firstName} ${this.lastName}`
  }
}

const state = proxy(new Author())
const snap = snapshot(state)

console.log(snap instanceof Author) // true
state.firstName = 'f2'
console.log(snap.fullName()) // 'f l' - uses frozen snapshot state
```

**Note:** Getters and methods are not cached and re-evaluate on each call (but should be fast and deterministic).

## Vanilla JavaScript

In vanilla JS, `snapshot` is useful for serialization and change detection:

```ts
import { proxy, snapshot, subscribe } from 'valtio/vanilla'

const state = proxy({ count: 0, text: 'hello' })

subscribe(state, () => {
  const obj = snapshot(state) // Immutable object
  console.log(obj)
})
```

## React Suspense

Snapshots throw promises, making them compatible with React Suspense:

```tsx
const state = proxy({
  post: fetch(url).then((res) => res.json()),
})

function Post() {
  const snap = useSnapshot(state)
  // Throws promise if not resolved, Suspense handles it
  return <div>{snap.post.title}</div>
}
```

## Key Points

- `snapshot()` creates immutable, frozen copies of proxy state
- Same snapshot reference returned if proxy hasn't changed (efficient comparison)
- Copy-on-write optimization - only changed parts are copied
- Maintains object prototypes - classes, methods, getters work
- Throws promises for React Suspense support
- Useful for serialization, change detection, and vanilla JS apps
- Import from `valtio/vanilla` for non-React usage

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/advanced/snapshot
- https://github.com/pmndrs/valtio
-->
