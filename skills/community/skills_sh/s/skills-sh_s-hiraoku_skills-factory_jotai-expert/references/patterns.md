# Jotai Design Patterns

> Source: https://jotai.org/docs

## Table of Contents

1. [Atom Organization](#atom-organization)
2. [Action Atoms](#action-atoms)
3. [Async Patterns](#async-patterns)
4. [Testing](#testing)
5. [TypeScript Patterns](#typescript-patterns)
6. [SSR & Framework Integration](#ssr--framework-integration)
7. [Debugging](#debugging)

---

## Atom Organization

### By Feature/Domain

```
src/
├── features/
│   ├── auth/
│   │   ├── atoms.ts         # userAtom, sessionAtom, etc.
│   │   ├── actions.ts       # loginAtom, logoutAtom
│   │   └── selectors.ts     # isLoggedInAtom, userNameAtom
│   ├── todos/
│   │   ├── atoms.ts
│   │   ├── actions.ts
│   │   └── selectors.ts
│   └── settings/
│       └── atoms.ts
└── store/
    └── index.ts             # createStore, Provider setup
```

### Naming Conventions

```typescript
// Primitive atoms: noun + Atom
const countAtom = atom(0)
const userAtom = atom<User | null>(null)
const todosAtom = atom<Todo[]>([])

// Derived/selector atoms: descriptive name + Atom
const isLoggedInAtom = atom((get) => get(userAtom) !== null)
const completedTodosAtom = atom((get) => get(todosAtom).filter(t => t.done))
const todoCountAtom = atom((get) => get(todosAtom).length)

// Action atoms: verb + Atom
const incrementAtom = atom(null, (get, set) => set(countAtom, get(countAtom) + 1))
const loginAtom = atom(null, async (get, set, credentials) => { /* ... */ })
const addTodoAtom = atom(null, (get, set, text: string) => { /* ... */ })
```

---

## Action Atoms

### Write-Only Actions

```typescript
// Simple action
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1)
})

// Action with parameter
const addTodoAtom = atom(null, (get, set, text: string) => {
  set(todosAtom, [...get(todosAtom), { id: Date.now(), text, done: false }])
})

// Action affecting multiple atoms
const resetAllAtom = atom(null, (get, set) => {
  set(countAtom, 0)
  set(todosAtom, [])
  set(userAtom, null)
})
```

### Async Actions

```typescript
const fetchUserAtom = atom(null, async (get, set, userId: string) => {
  set(loadingAtom, true)
  try {
    const response = await fetch(`/api/users/${userId}`)
    const user = await response.json()
    set(userAtom, user)
    set(errorAtom, null)
  } catch (error) {
    set(errorAtom, error.message)
  } finally {
    set(loadingAtom, false)
  }
})

// Usage
const fetchUser = useSetAtom(fetchUserAtom)
await fetchUser('123')
```

### Actions with Return Values

```typescript
const submitFormAtom = atom(null, async (get, set, formData: FormData) => {
  const response = await fetch('/api/submit', {
    method: 'POST',
    body: formData,
  })
  const result = await response.json()
  set(resultAtom, result)
  return result // Can return values
})

// Usage
const submit = useSetAtom(submitFormAtom)
const result = await submit(formData)
```

---

## Async Patterns

### Pattern 1: Suspense

```typescript
const userAtom = atom(async () => {
  const res = await fetch('/api/user')
  return res.json()
})

function UserProfile() {
  const user = useAtomValue(userAtom) // Suspends until resolved
  return <div>{user.name}</div>
}

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <UserProfile />
    </Suspense>
  )
}
```

### Pattern 2: Loadable (No Suspense)

```typescript
import { loadable } from 'jotai/utils'

const userAtom = atom(async () => {
  const res = await fetch('/api/user')
  return res.json()
})

const loadableUserAtom = loadable(userAtom)

function UserProfile() {
  const userLoadable = useAtomValue(loadableUserAtom)

  switch (userLoadable.state) {
    case 'loading':
      return <Spinner />
    case 'hasError':
      return <Error message={userLoadable.error.message} />
    case 'hasData':
      return <div>{userLoadable.data.name}</div>
  }
}
```

### Pattern 3: Manual Loading State

```typescript
const userAtom = atom<User | null>(null)
const loadingAtom = atom(false)
const errorAtom = atom<string | null>(null)

const fetchUserAtom = atom(null, async (get, set, id: string) => {
  set(loadingAtom, true)
  set(errorAtom, null)
  try {
    const res = await fetch(`/api/users/${id}`)
    set(userAtom, await res.json())
  } catch (e) {
    set(errorAtom, e.message)
  } finally {
    set(loadingAtom, false)
  }
})

function UserProfile() {
  const user = useAtomValue(userAtom)
  const loading = useAtomValue(loadingAtom)
  const error = useAtomValue(errorAtom)

  if (loading) return <Spinner />
  if (error) return <Error message={error} />
  if (!user) return null
  return <div>{user.name}</div>
}
```

### Pattern 4: Refresh/Invalidation

```typescript
const refreshCountAtom = atom(0)

const dataAtom = atom(async (get) => {
  get(refreshCountAtom) // Dependency for refresh
  const res = await fetch('/api/data')
  return res.json()
})

const refreshAtom = atom(null, (get, set) => {
  set(refreshCountAtom, (c) => c + 1)
})

// Usage
const refresh = useSetAtom(refreshAtom)
<button onClick={refresh}>Refresh</button>
```

---

## Testing

### Basic Component Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Provider } from 'jotai'

test('counter increments', async () => {
  render(
    <Provider>
      <Counter />
    </Provider>
  )

  expect(screen.getByText('Count: 0')).toBeInTheDocument()
  fireEvent.click(screen.getByText('Increment'))
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})
```

### Testing with Initial Values

```typescript
import { useHydrateAtoms } from 'jotai/utils'

function HydrateAtoms({ initialValues, children }) {
  useHydrateAtoms(initialValues)
  return children
}

test('counter at max value', () => {
  render(
    <Provider>
      <HydrateAtoms initialValues={[[countAtom, 100]]}>
        <Counter />
      </HydrateAtoms>
    </Provider>
  )

  expect(screen.getByText('Count: 100')).toBeInTheDocument()
})
```

### Testing Atoms Directly

```typescript
import { createStore } from 'jotai'

test('derived atom calculates correctly', () => {
  const store = createStore()

  store.set(priceAtom, 100)
  store.set(quantityAtom, 5)

  expect(store.get(totalAtom)).toBe(500)
})
```

---

## TypeScript Patterns

### Basic Type Inference

```typescript
// Types are inferred automatically
const countAtom = atom(0)              // Atom<number>
const textAtom = atom('')              // Atom<string>
const userAtom = atom<User | null>(null) // Explicit for null

// Derived atoms infer from read function
const doubleAtom = atom((get) => get(countAtom) * 2) // Atom<number>
```

### Explicit Typing

```typescript
// Three type parameters: Value, Args (tuple), Result
const actionAtom = atom<null, [string, number], Promise<void>>(
  null,
  async (get, set, name: string, age: number) => {
    // ...
  }
)
```

### Extract Atom Value Type

```typescript
import { ExtractAtomValue } from 'jotai'

const userAtom = atom<User>({ name: '', email: '' })

type UserType = ExtractAtomValue<typeof userAtom> // User

function processUser(user: ExtractAtomValue<typeof userAtom>) {
  // ...
}
```

### Typed Atom Families

```typescript
type TodoId = string

const todoFamily = atomFamily((id: TodoId) =>
  atom<Todo>({ id, text: '', done: false })
)

// Or with async
const userFamily = atomFamily((userId: string) =>
  atom<Promise<User>>(async () => {
    const res = await fetch(`/api/users/${userId}`)
    return res.json()
  })
)
```

---

## SSR & Framework Integration

### Next.js App Router

```typescript
// app/providers.tsx
'use client'

import { Provider } from 'jotai'

export function Providers({ children }) {
  return <Provider>{children}</Provider>
}

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

### Hydration from Server

```typescript
// Server component passes initial data
// app/page.tsx
async function getData() {
  const res = await fetch('/api/data')
  return res.json()
}

export default async function Page() {
  const initialData = await getData()
  return <ClientComponent initialData={initialData} />
}

// Client component hydrates atom
'use client'
import { useHydrateAtoms } from 'jotai/utils'

function ClientComponent({ initialData }) {
  useHydrateAtoms([[dataAtom, initialData]])
  const data = useAtomValue(dataAtom)
  return <div>{/* ... */}</div>
}
```

---

## Debugging

### Debug Labels

```typescript
const countAtom = atom(0)
countAtom.debugLabel = 'count'

// Or use SWC/Babel plugin for automatic labels
// .swcrc
{
  "jsc": {
    "experimental": {
      "plugins": [["@swc-jotai/debug-label", {}]]
    }
  }
}
```

### React DevTools

```typescript
// Atoms show in React DevTools via useDebugValue
// useAtom automatically integrates
```

### Redux DevTools

```typescript
import { useAtomsDevtools } from 'jotai-devtools'

function AtomsDevtools() {
  useAtomsDevtools('my-app')
  return null
}

function App() {
  return (
    <Provider>
      <AtomsDevtools />
      <MyApp />
    </Provider>
  )
}
```

### Detect Mutations

```typescript
import { freezeAtom } from 'jotai/utils'

const userAtom = freezeAtom(atom({ name: 'John' }))

// This will throw in development:
// user.name = 'Jane' // Error: Cannot assign to read only property
```
