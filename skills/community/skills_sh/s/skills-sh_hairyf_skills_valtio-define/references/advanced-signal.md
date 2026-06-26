---
name: advanced-signal
description: JSX signal component for inline reactive values
---

# $signal

JSX component that renders reactive values inline. Useful for simple reactive expressions without creating separate components.

## Usage

```tsx
import { defineStore } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0 }),
  getters: {
    doubled() { return this.count * 2 },
  },
})

function App() {
  return (
    <div>
      Count: {store.$signal(state => state.count)}
      {' '}
      Doubled: {store.$signal(state => state.doubled)}
    </div>
  )
}
```

## Key Points

* **Inline Reactivity**: Renders reactive values directly in JSX
* **Automatic Updates**: Component re-renders when accessed state changes
* **Access to State and Getters**: Function receives full state including getters
* **No Hook Required**: Can be used outside of React components (though typically used inside)

## When to Use

**Use $signal when:**
* Simple inline reactive expressions
* Don't want to extract to separate component
* Displaying computed values inline

**Use useStore when:**
* Need multiple state values
* Need to pass state to child components
* More complex component logic

## Pattern Comparison

```tsx
// Using $signal
<div>
  {store.$signal(s => s.count)}
</div>

// Using useStore (more flexible)
function Component() {
  const state = useStore(store)
  return <div>{state.count}</div>
}
```
