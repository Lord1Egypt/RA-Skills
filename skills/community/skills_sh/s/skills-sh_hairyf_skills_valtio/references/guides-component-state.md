---
name: guides-component-state
description: Isolate component state using useRef to create reusable component-level state
---

# Component State

To isolate component state for reusability, Valtio state must live in the React lifecycle. Wrap a `proxy` in a `useRef` and pass it via props or context.

## Usage

### Using Context

```tsx
import { createContext, useContext, useRef } from 'react'
import { proxy, useSnapshot } from 'valtio'

const MyContext = createContext()

const MyProvider = ({ children }) => {
  // Create proxy in useRef to isolate per-instance
  const state = useRef(proxy({ count: 0 })).current
  return <MyContext.Provider value={state}>{children}</MyContext.Provider>
}

const MyCounter = () => {
  const state = useContext(MyContext)
  const snap = useSnapshot(state)
  return (
    <>
      {snap.count} <button onClick={() => ++state.count}>+1</button>
    </>
  )
}
```

### Using Props

```tsx
function Parent() {
  const state = useRef(proxy({ count: 0 })).current
  return <Child state={state} />
}

function Child({ state }) {
  const snap = useSnapshot(state)
  return <div>{snap.count}</div>
}
```

## Alternatives

### use-constant

If you prefer a more explicit API:

```tsx
import useConstant from 'use-constant'

const MyProvider = ({ children }) => {
  const state = useConstant(() => proxy({ count: 0 }))
  return <MyContext.Provider value={state}>{children}</MyContext.Provider>
}
```

### Custom Hook

Create a custom hook that combines context and snapshot:

```tsx
const MyContext = createContext()

const MyProvider = ({ children }) => {
  const state = useRef(proxy({ count: 0 })).current
  return <MyContext.Provider value={state}>{children}</MyContext.Provider>
}

function useMyState() {
  const state = useContext(MyContext)
  const snap = useSnapshot(state)
  return { state, snap }
}

// Usage
function MyComponent() {
  const { state, snap } = useMyState()
  return <div>{snap.count}</div>
}
```

## Key Points

- Use `useRef(proxy(...)).current` to create component-scoped state
- Pass via context or props for component isolation
- Each component instance gets its own state
- Useful for reusable components that need isolated state
- Consider `use-constant` or custom hooks for cleaner APIs

<!--
Source references:
- https://valtio.pmnd.rs/docs/guides/component-state
- https://github.com/pmndrs/valtio
-->
