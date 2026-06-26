# Jotai Core API Reference

> Source: https://jotai.org/docs

## Table of Contents

1. [atom](#atom)
2. [useAtom / useAtomValue / useSetAtom](#hooks)
3. [Store](#store)
4. [Provider](#provider)

---

## atom

### Basic Patterns

```typescript
import { atom } from 'jotai'

// 1. Primitive atom - holds a simple value
const countAtom = atom(0)
const textAtom = atom('hello')
const userAtom = atom<User | null>(null)

// 2. Read-only derived atom
const doubleCountAtom = atom((get) => get(countAtom) * 2)

// 3. Read-write derived atom
const doubleCountAtom = atom(
  (get) => get(countAtom) * 2,
  (get, set, newValue: number) => set(countAtom, newValue / 2)
)

// 4. Write-only atom (action atom)
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1)
})
```

### Important: Reference Equality

Atom configs can be created anywhere, but reference equality matters:

```typescript
// ❌ BAD: Creates new atom on every render
function Component() {
  const myAtom = atom(0) // New atom each render!
  const [value] = useAtom(myAtom)
}

// ✅ GOOD: Stable reference outside component
const myAtom = atom(0)
function Component() {
  const [value] = useAtom(myAtom)
}

// ✅ GOOD: useMemo for dynamic atoms
function Component({ id }) {
  const itemAtom = useMemo(() => atom(items[id]), [id])
  const [value] = useAtom(itemAtom)
}
```

### onMount

Initialize logic when atom is first subscribed:

```typescript
const countAtom = atom(0)
countAtom.onMount = (setAtom) => {
  const id = setInterval(() => setAtom((c) => c + 1), 1000)
  return () => clearInterval(id) // cleanup
}
```

### debugLabel

```typescript
countAtom.debugLabel = 'count'
```

---

## Hooks

### useAtom

Combined read and write:

```typescript
const [value, setValue] = useAtom(countAtom)
```

### useAtomValue

Read-only (prevents unnecessary re-renders when you don't need setter):

```typescript
const value = useAtomValue(countAtom)
```

### useSetAtom

Write-only (prevents re-renders when value changes):

```typescript
const setValue = useSetAtom(countAtom)
```

---

## Store

### createStore

```typescript
import { createStore } from 'jotai'

const store = createStore()

// Read value
const count = store.get(countAtom)

// Set value
store.set(countAtom, 10)

// Subscribe to changes
const unsub = store.sub(countAtom, () => {
  console.log('countAtom changed:', store.get(countAtom))
})
```

### getDefaultStore

Access the default store (provider-less mode):

```typescript
import { getDefaultStore } from 'jotai'

const store = getDefaultStore()
store.set(countAtom, 5)
```

---

## Provider

### Basic Usage

```typescript
import { Provider } from 'jotai'

function App() {
  return (
    <Provider>
      <MyComponent />
    </Provider>
  )
}
```

### With Custom Store

```typescript
const myStore = createStore()

function App() {
  return (
    <Provider store={myStore}>
      <MyComponent />
    </Provider>
  )
}
```

### Multiple Providers

Providers can be nested for different subtrees:

```typescript
function App() {
  return (
    <Provider>
      <GlobalUI />
      <Provider>
        <IsolatedFeature />
      </Provider>
    </Provider>
  )
}
```

### Provider-less Mode

Works without Provider using default store (not recommended for SSR):

```typescript
// Just use atoms directly - no Provider needed
function App() {
  const [count] = useAtom(countAtom)
  return <div>{count}</div>
}
```

### useStore Hook

Access the current store in components:

```typescript
import { useStore } from 'jotai'

function Component() {
  const store = useStore()
  // Direct store access when needed
}
```
