# Jotai Performance Optimization Guide

> Source: https://jotai.org/docs/guides/performance

## Table of Contents

1. [Core Principles](#core-principles)
2. [Render Optimization Patterns](#render-optimization-patterns)
3. [Large Objects](#large-objects)
4. [Common Anti-Patterns](#common-anti-patterns)

---

## Core Principles

### 1. Keep Renders Cheap

Component functions must be idempotent - they will be called multiple times during render phase:

```typescript
// ❌ BAD: Heavy computation in component
function Component() {
  const [items] = useAtom(itemsAtom)
  const filtered = items.filter(heavyComputation) // Runs every render!
  return <List items={filtered} />
}

// ✅ GOOD: Computation in atom or action
const filteredItemsAtom = atom((get) => {
  return get(itemsAtom).filter(heavyComputation)
})

// ✅ GOOD: Computation in write action
const fetchAndProcessAtom = atom(null, async (get, set) => {
  const res = await fetch('/api/items')
  const computed = res.filter(heavyComputation) // Runs once
  set(itemsAtom, computed)
})
```

### 2. Granular Subscriptions

Split components so each subscribes only to what it needs:

```typescript
// ❌ BAD: One component subscribes to everything
function UserProfile() {
  const [user] = useAtom(userAtom) // Re-renders on ANY user change
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <span>Last login: {user.lastLogin}</span>
    </div>
  )
}

// ✅ GOOD: Granular components with derived atoms
const nameAtom = selectAtom(userAtom, (u) => u.name)
const emailAtom = selectAtom(userAtom, (u) => u.email)
const lastLoginAtom = selectAtom(userAtom, (u) => u.lastLogin)

function UserName() {
  const name = useAtomValue(nameAtom)
  return <h1>{name}</h1>
}

function UserEmail() {
  const email = useAtomValue(emailAtom)
  return <p>{email}</p>
}
```

### 3. Use Correct Hook

| Need | Hook | Re-renders |
|------|------|------------|
| Read only | `useAtomValue` | When value changes |
| Write only | `useSetAtom` | Never |
| Both | `useAtom` | When value changes |

```typescript
// ❌ BAD: Using useAtom when only writing
function IncrementButton() {
  const [, setCount] = useAtom(countAtom) // Re-renders unnecessarily
  return <button onClick={() => setCount((c) => c + 1)}>+</button>
}

// ✅ GOOD: useSetAtom for write-only
function IncrementButton() {
  const setCount = useSetAtom(countAtom) // Never re-renders
  return <button onClick={() => setCount((c) => c + 1)}>+</button>
}
```

---

## Render Optimization Patterns

### selectAtom - Subscribe to Specific Properties

```typescript
import { selectAtom } from 'jotai/utils'

const userAtom = atom({
  id: 1,
  name: 'John',
  profile: { bio: '...', avatar: '...' },
  settings: { theme: 'dark', language: 'en' }
})

// Only re-renders when name changes
const nameAtom = selectAtom(userAtom, (user) => user.name)

// Deep equality for object slices
import { deepEqual } from 'fast-equals'
const profileAtom = selectAtom(
  userAtom,
  (user) => user.profile,
  deepEqual
)
```

### focusAtom - Read/Write Specific Properties

```typescript
import { focusAtom } from 'jotai-optics'

const formAtom = atom({
  personal: { name: '', email: '' },
  address: { street: '', city: '', zip: '' }
})

// Individual fields - only re-renders affected components
const nameAtom = focusAtom(formAtom, (o) => o.prop('personal').prop('name'))
const emailAtom = focusAtom(formAtom, (o) => o.prop('personal').prop('email'))
const cityAtom = focusAtom(formAtom, (o) => o.prop('address').prop('city'))
```

### splitAtom - Efficient Lists

```typescript
import { splitAtom } from 'jotai/utils'

const todosAtom = atom<Todo[]>([])
const todoAtomsAtom = splitAtom(todosAtom, (todo) => todo.id)

// Each TodoItem only re-renders when its own data changes
function TodoItem({ todoAtom }: { todoAtom: PrimitiveAtom<Todo> }) {
  const [todo, setTodo] = useAtom(todoAtom)
  return (
    <input
      checked={todo.done}
      onChange={(e) => setTodo({ ...todo, done: e.target.checked })}
    />
  )
}
```

---

## Large Objects

### Strategy 1: Derived Atoms for Reads

```typescript
const largeObjectAtom = atom<LargeObject>(initialObject)

// Create derived atoms for each section
const headerAtom = atom((get) => get(largeObjectAtom).header)
const itemsAtom = atom((get) => get(largeObjectAtom).items)
const metadataAtom = atom((get) => get(largeObjectAtom).metadata)
```

### Strategy 2: focusAtom for Read/Write

```typescript
import { focusAtom } from 'jotai-optics'

const stateAtom = atom({
  users: { byId: {}, allIds: [] },
  posts: { byId: {}, allIds: [] },
  comments: { byId: {}, allIds: [] }
})

// Focused atoms for each domain
const usersAtom = focusAtom(stateAtom, (o) => o.prop('users'))
const postsAtom = focusAtom(stateAtom, (o) => o.prop('posts'))

// Further focus for specific user
const userAtom = (id: string) =>
  focusAtom(stateAtom, (o) => o.prop('users').prop('byId').prop(id))
```

### Strategy 3: Atoms-in-Atom for Dynamic Collections

```typescript
// Store atoms themselves as values
const todoAtomsAtom = atom<PrimitiveAtom<Todo>[]>([])

const addTodoAtom = atom(null, (get, set, text: string) => {
  const newTodoAtom = atom({ id: Date.now(), text, done: false })
  set(todoAtomsAtom, [...get(todoAtomsAtom), newTodoAtom])
})

// Each todo is completely independent
function TodoItem({ todoAtom }: { todoAtom: PrimitiveAtom<Todo> }) {
  const [todo, setTodo] = useAtom(todoAtom)
  // Updating this never affects other todos
}
```

---

## Common Anti-Patterns

### Anti-Pattern 1: Creating Atoms in Render

```typescript
// ❌ BAD: New atom every render
function Component() {
  const myAtom = atom(0)
  // ...
}

// ✅ GOOD: Outside component or memoized
const myAtom = atom(0)
function Component() {
  // ...
}
```

### Anti-Pattern 2: Derived Atom in Render

```typescript
// ❌ BAD: New derived atom every render
function UserName({ userAtom }) {
  const nameAtom = atom((get) => get(userAtom).name)
  const name = useAtomValue(nameAtom)
}

// ✅ GOOD: useMemo or define outside
function UserName({ userAtom }) {
  const nameAtom = useMemo(
    () => atom((get) => get(userAtom).name),
    [userAtom]
  )
  const name = useAtomValue(nameAtom)
}
```

### Anti-Pattern 3: Over-fragmenting with focusAtom

```typescript
// ❌ BAD: Too many focused atoms for frequently-updated data
// If items change together, fragmentation adds overhead
const item1Atom = focusAtom(listAtom, (o) => o.at(0))
const item2Atom = focusAtom(listAtom, (o) => o.at(1))
// ...100 more

// ✅ GOOD: For frequently-updated data, batch updates
const updateAllItemsAtom = atom(null, (get, set, newItems) => {
  set(listAtom, newItems)
})
```

### Anti-Pattern 4: Unnecessary Suspense Boundaries

```typescript
// ❌ BAD: Suspense for every async atom
function App() {
  return (
    <Suspense>
      <User />
      <Suspense>
        <Posts />
        <Suspense>
          <Comments />
        </Suspense>
      </Suspense>
    </Suspense>
  )
}

// ✅ GOOD: Strategic boundaries or loadable
function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <User />
      <Posts />
      <Comments />
    </Suspense>
  )
}
```

### When to Optimize

1. **Profile first** - Use React DevTools to identify actual re-render issues
2. **Measure impact** - Not all re-renders are problematic
3. **Evaluate update frequency**:
   - Frequent updates (typing, animations): Minimize atom splits
   - Rare updates (settings, user data): Use `selectAtom`/`focusAtom` freely
