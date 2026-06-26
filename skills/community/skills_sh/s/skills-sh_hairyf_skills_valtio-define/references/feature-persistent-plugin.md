---
name: feature-persistent-plugin
description: Persist store state to storage (localStorage, sessionStorage, etc.)
---

# Persistent Plugin

Persist store state to storage and automatically restore it on initialization.

## Basic Usage

First, register the plugin globally:

```tsx
import valtio from 'valtio-define'
import { persistent } from 'valtio-define/plugins'

valtio.use(persistent())
```

Then configure persistence in your store:

```tsx
import { defineStore } from 'valtio-define'

const store = defineStore({
  state: () => ({ count: 0, name: 'test' }),
  persist: {
    key: 'my-store',
    storage: localStorage,
    paths: ['count'], // Only persist 'count'
  },
})
```

## Auto-Generated Key

If `persist` is `true`, a unique key is auto-generated using `structure-id`:

```tsx
const store = defineStore({
  state: () => ({ count: 0 }),
  persist: true, // Auto-generates key
})
```

**Key Points:**
* Key is based on store structure (state shape)
* Same structure = same key (useful for singleton stores)
* Different structures = different keys

## Configuration Options

```tsx
interface PersistentOptions<S extends object> {
  key?: string           // Storage key (required if persist is object)
  storage?: Storage       // Storage implementation (defaults to localStorage)
  paths?: DeepKeys<S>[]   // Specific paths to persist (defaults to all)
}
```

### Custom Storage

```tsx
const customStorage = {
  getItem: async (key: string) => {
    // Async storage
    return await fetch(`/api/storage/${key}`).then(r => r.text())
  },
  setItem: async (key: string, value: string) => {
    await fetch(`/api/storage/${key}`, {
      method: 'POST',
      body: value,
    })
  },
}

const store = defineStore({
  state: () => ({ count: 0 }),
  persist: {
    key: 'my-store',
    storage: customStorage,
  },
})
```

### Selective Persistence

Only persist specific state paths:

```tsx
const store = defineStore({
  state: () => ({
    count: 0,
    name: 'test',
    user: { id: 1, email: 'test@example.com' },
  }),
  persist: {
    key: 'my-store',
    paths: ['count', 'user.email'], // Only persist these
  },
})
```

**Key Points:**
* `paths` supports nested paths using dot notation
* Omit `paths` to persist all state
* Only specified paths are saved and restored

## Storage Interface

```tsx
interface Storage {
  getItem: (key: string) => Awaitable<any>
  setItem: (key: string, value: any) => Awaitable<void>
  [key: string]: any
}
```

**Key Points:**
* `getItem` and `setItem` can be async (return Promises)
* Plugin handles both sync and async storage
* Defaults to `localStorage` if available

## Behavior

* **Initialization**: State is restored from storage when store is created
* **Auto-Save**: State changes are automatically saved to storage
* **Selective Updates**: Only specified paths (if configured) are saved
* **Async Support**: Handles async storage operations gracefully

## Common Patterns

### Session Storage

```tsx
const store = defineStore({
  state: () => ({ count: 0 }),
  persist: {
    key: 'my-store',
    storage: sessionStorage,
  },
})
```

### Multiple Stores

```tsx
// Each store gets its own key
const store1 = defineStore({
  state: () => ({ count: 0 }),
  persist: { key: 'store-1' },
})

const store2 = defineStore({
  state: () => ({ name: 'test' }),
  persist: { key: 'store-2' },
})
```
