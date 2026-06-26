---
name: core-use-snapshot
description: React hook to create render-optimized snapshots that only re-render when accessed properties change
---

# useSnapshot

`useSnapshot` is a React hook that creates a render-optimized snapshot of proxy state. It wraps Valtio's `snapshot()` with access tracking, ensuring components only re-render when properties they actually accessed have changed.

## Usage

### Basic Usage

```tsx
import { proxy, useSnapshot } from 'valtio'

const state = proxy({ count: 0, text: 'hello' })

function Counter() {
  const snap = useSnapshot(state)
  return (
    <div>
      {snap.count}
      <button onClick={() => ++state.count}>+1</button>
    </div>
  )
}
```

### Read from Snapshots, Mutate via Proxy

**Rule:** Read from snapshots in render, mutate via proxy in callbacks:

```tsx
function Counter() {
  const snap = useSnapshot(state)
  return (
    <div>
      {/* ✅ Read from snapshot */}
      {snap.count}
      <button
        onClick={() => {
          // ✅ Read and mutate via proxy in callbacks
          if (state.count < 10) {
            ++state.count
          }
        }}
      >
        +1
      </button>
    </div>
  )
}
```

## Parent/Child Components

### Passing Snapshots

When passing snapshots to child components, both parent and children re-render when the snapshot changes:

```tsx
const state = proxy({
  books: [
    { id: 1, title: 'b1' },
    { id: 2, title: 'b2' },
  ],
})

function AuthorView() {
  const snap = useSnapshot(state)
  return (
    <div>
      {snap.books.map((book) => (
        <Book key={book.id} book={book} />
      ))}
    </div>
  )
}

function BookView({ book }) {
  // book is a snapshot - read-only
  return <div>{book.title}</div>
}
```

### Child Components Making Mutations

If child components need to mutate, pass the proxy instead:

```tsx
function AuthorView() {
  const snap = useSnapshot(state)
  return (
    <div>
      {snap.books.map((book, i) => (
        <Book key={book.id} book={state.books[i]} />
      ))}
    </div>
  )
}

function BookView({ book }) {
  // book is the proxy - can create snapshot and mutate
  const snap = useSnapshot(book)
  return (
    <div onClick={() => book.updateTitle()}>
      {snap.title}
    </div>
  )
}
```

### Passing Both Snapshot and Proxy

You can pass both for convenience:

```tsx
function AuthorView() {
  const snap = useSnapshot(state)
  return (
    <div>
      {snap.books.map((book, i) => (
        <Book
          key={book.id}
          bookProxy={state.books[i]}
          bookSnapshot={book}
        />
      ))}
    </div>
  )
}
```

## Nested Snapshots

You can create snapshots from nested proxies:

```tsx
function ProfileName() {
  // Create snapshot from nested proxy
  const snap = useSnapshot(state.profile)
  return <div>{snap.name}</div>
}
```

## Gotchas

### Don't Replace Child Proxies

Replacing a child proxy breaks the snapshot reference:

```ts
// ❌ Wrong - breaks snapshot
const childState = state.profile
state.profile = { name: 'new name' }
// childState still points to old proxy

// ✅ Correct - access via parent snapshot
const snap = useSnapshot(state)
return <div>{snap.profile.name}</div>

// ✅ Or destructure from snapshot
const { profile } = useSnapshot(state)
return <div>{profile.name}</div>
```

## Dev Mode Debug Values

In development, `useSnapshot` uses React's `useDebugValue` to show which fields were accessed:

```tsx
// In React DevTools, you'll see which fields trigger re-renders
const snap = useSnapshot(state)
// Debug value shows: ['count', 'text']
```

**Note:** The debug value shows fields from the *previous* render, and getter calls aren't included (but are correctly tracked internally).

## Key Points

- `useSnapshot()` creates render-optimized snapshots
- Read from snapshots in render, mutate via proxy in callbacks
- Only re-renders when accessed properties change
- Pass snapshots for read-only children, proxies for mutating children
- Can create snapshots from nested proxies
- Don't replace child proxy references - access via parent snapshot
- Works with React Suspense (snapshots throw promises)

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/basic/useSnapshot
- https://github.com/pmndrs/valtio
-->
