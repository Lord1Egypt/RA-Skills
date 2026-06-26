---
name: guides-async
description: Work with promises in proxy state and React Suspense integration
---

# Async

Valtio supports promises as values in proxies. Promises are resolved in `snapshot` calls, making them compatible with React Suspense.

## Usage

### Promises in Proxies

```ts
import { proxy, snapshot, subscribe } from 'valtio'

const state = proxy({
  count: new Promise((resolve) => 
    setTimeout(() => resolve(1), 1000)
  ),
})

// In snapshot, promise is resolved
subscribe(state, () => {
  const value = snapshot(state).count
  if (typeof value === 'number') {
    console.log(value) // 1 (after promise resolves)
  }
})
```

### React Suspense with use Hook

Valtio is compatible with React 19's `use` hook:

```tsx
import { use } from 'react' // React 19
// import { use } from 'react18-use' // React 18

const state = proxy({
  post: fetch(url).then((res) => res.json()),
})

function Post() {
  const snap = useSnapshot(state)
  // use() handles promise throwing for Suspense
  return <div>{use(snap.post).title}</div>
}

function App() {
  return (
    <Suspense fallback="Loading...">
      <Post />
    </Suspense>
  )
}
```

### Vanilla JavaScript Example

```ts
const countDiv = document.getElementById('count')
if (countDiv) countDiv.innerText = '0'

const store = proxy({
  count: new Promise((r) => setTimeout(() => r(1), 1000)),
})

subscribe(store, () => {
  const value = snapshot(store).count
  if (countDiv && typeof value === 'number') {
    countDiv.innerText = String(value)
    // Chain promises
    store.count = new Promise((r) => 
      setTimeout(() => r(value + 1), 1000)
    )
  }
})
```

## Key Points

- Promises can be values in proxy state
- Promises are resolved in `snapshot()` calls
- `snapshot()` throws promises for React Suspense
- Use React 19 `use()` hook or `react18-use` for React 18
- Works in both React and vanilla JavaScript
- Can chain promises for sequential async operations

<!--
Source references:
- https://valtio.pmnd.rs/docs/guides/async
- https://github.com/pmndrs/valtio
-->
