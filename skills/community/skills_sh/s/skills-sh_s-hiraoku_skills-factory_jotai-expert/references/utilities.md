# Jotai Utilities Reference

> Source: https://jotai.org/docs/utilities

## Table of Contents

1. [Storage](#storage)
2. [Async](#async)
3. [Resettable](#resettable)
4. [Select & Focus](#select--focus)
5. [Split](#split)
6. [Family](#family)

---

## Storage

### atomWithStorage

Persist state to localStorage/sessionStorage:

```typescript
import { atomWithStorage } from 'jotai/utils'

const themeAtom = atomWithStorage('theme', 'light')
const userPrefsAtom = atomWithStorage<UserPrefs>('userPrefs', defaultPrefs)
```

Options:

```typescript
const atom = atomWithStorage('key', initialValue, storage, {
  getOnInit: true, // Read from storage on initialization
})
```

Reset to initial value:

```typescript
import { RESET } from 'jotai/utils'

const setTheme = useSetAtom(themeAtom)
setTheme(RESET) // Removes from storage, returns to initial
```

Custom storage with validation:

```typescript
import { z } from 'zod'

const schema = z.object({ name: z.string(), age: z.number() })

const customStorage = {
  getItem: (key: string, initialValue: User) => {
    const stored = localStorage.getItem(key)
    if (!stored) return initialValue
    const parsed = schema.safeParse(JSON.parse(stored))
    return parsed.success ? parsed.data : initialValue
  },
  setItem: (key: string, value: User) => {
    localStorage.setItem(key, JSON.stringify(value))
  },
  removeItem: (key: string) => localStorage.removeItem(key),
}

const userAtom = atomWithStorage('user', defaultUser, customStorage)
```

---

## Async

### loadable

Handle async atoms without Suspense:

```typescript
import { loadable } from 'jotai/utils'

const asyncAtom = atom(async () => {
  const res = await fetch('/api/data')
  return res.json()
})

const loadableAtom = loadable(asyncAtom)

function Component() {
  const data = useAtomValue(loadableAtom)

  if (data.state === 'loading') return <Spinner />
  if (data.state === 'hasError') return <Error error={data.error} />
  return <Data value={data.data} />
}
```

### unwrap

Convert async atom to sync with fallback:

```typescript
import { unwrap } from 'jotai/utils'

const asyncAtom = atom(async () => fetchData())

// Returns undefined while loading
const syncAtom = unwrap(asyncAtom)

// Returns previous value while loading
const syncAtom = unwrap(asyncAtom, (prev) => prev ?? defaultValue)
```

### atomWithObservable

For RxJS or similar:

```typescript
import { atomWithObservable } from 'jotai/utils'
import { interval } from 'rxjs'

const tickAtom = atomWithObservable(() => interval(1000))
```

---

## Resettable

### atomWithReset

```typescript
import { atomWithReset, useResetAtom, RESET } from 'jotai/utils'

const countAtom = atomWithReset(0)

function Component() {
  const [count, setCount] = useAtom(countAtom)
  const reset = useResetAtom(countAtom)

  return (
    <>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
      <button onClick={reset}>Reset</button>
      {/* Or: onClick={() => setCount(RESET)} */}
    </>
  )
}
```

### atomWithDefault

Resettable atom with dynamic initial value:

```typescript
import { atomWithDefault, RESET } from 'jotai/utils'

const baseAtom = atom(1)
const derivedAtom = atomWithDefault((get) => get(baseAtom) * 2)

// Can be overwritten
set(derivedAtom, 10)

// Reset restores to derived value
set(derivedAtom, RESET)
```

---

## Select & Focus

### selectAtom

Create read-only derived atom from a slice:

```typescript
import { selectAtom } from 'jotai/utils'

const userAtom = atom({ name: 'John', age: 30, email: 'john@example.com' })

// Only re-renders when name changes
const nameAtom = selectAtom(userAtom, (user) => user.name)

// With deep equality check
import { deepEqual } from 'fast-equals'
const profileAtom = selectAtom(
  userAtom,
  (user) => ({ name: user.name, age: user.age }),
  deepEqual
)
```

### focusAtom

Create read-write atom for a slice (requires optics-ts or jotai-optics):

```typescript
import { focusAtom } from 'jotai-optics'

const userAtom = atom({ name: 'John', address: { city: 'NYC' } })

// Read and write to nested property
const cityAtom = focusAtom(userAtom, (o) => o.prop('address').prop('city'))

function Component() {
  const [city, setCity] = useAtom(cityAtom)
  // setCity('LA') only updates address.city
}
```

---

## Split

### splitAtom

Convert array atom to atoms for each element:

```typescript
import { splitAtom } from 'jotai/utils'

const todosAtom = atom([
  { id: 1, text: 'Buy milk', done: false },
  { id: 2, text: 'Walk dog', done: true },
])

const todoAtomsAtom = splitAtom(todosAtom)

// With key extractor for stable identity
const todoAtomsAtom = splitAtom(todosAtom, (todo) => todo.id)

function TodoList() {
  const [todoAtoms, dispatch] = useAtom(todoAtomsAtom)

  return (
    <>
      {todoAtoms.map((todoAtom) => (
        <TodoItem
          key={todoAtom.toString()}
          todoAtom={todoAtom}
          onRemove={() => dispatch({ type: 'remove', atom: todoAtom })}
        />
      ))}
      <button onClick={() => dispatch({
        type: 'insert',
        value: { id: Date.now(), text: 'New', done: false }
      })}>
        Add
      </button>
    </>
  )
}

function TodoItem({ todoAtom, onRemove }) {
  const [todo, setTodo] = useAtom(todoAtom)
  // Updates only this item, no re-render of list
  return (
    <div>
      <input
        type="checkbox"
        checked={todo.done}
        onChange={(e) => setTodo({ ...todo, done: e.target.checked })}
      />
      {todo.text}
      <button onClick={onRemove}>Delete</button>
    </div>
  )
}
```

---

## Family

### atomFamily

Create parameterized atoms:

```typescript
import { atomFamily } from 'jotai/utils'

// Simple family
const todoFamily = atomFamily((id: string) => atom({ id, text: '', done: false }))

function TodoItem({ id }) {
  const [todo, setTodo] = useAtom(todoFamily(id))
  // Each id gets its own atom instance
}

// With async
const userFamily = atomFamily((userId: string) =>
  atom(async () => {
    const res = await fetch(`/api/users/${userId}`)
    return res.json()
  })
)

// With equality for object params
const itemFamily = atomFamily(
  (params: { type: string; id: number }) => atom(params),
  (a, b) => a.type === b.type && a.id === b.id
)
```
