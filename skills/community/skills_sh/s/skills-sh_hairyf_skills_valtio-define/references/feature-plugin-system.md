---
name: feature-plugin-system
description: Plugin system for extending store functionality
---

# Plugin System

Extend store functionality with plugins. Plugins can be registered globally (applies to all stores) or per-store.

## Global Plugin Registration

Register plugins globally to apply to all stores:

```tsx
import valtio from 'valtio-define'
import { persistent } from 'valtio-define/plugins'

// Register globally - applies to all stores
valtio.use(persistent())
```

**Key Points:**
* Plugins registered globally apply to all stores created after registration
* Use for cross-cutting concerns (logging, persistence, etc.)
* Plugins are reactive - new plugins are automatically applied to existing stores

## Per-Store Plugin Registration

Register plugins for a specific store:

```tsx
import { defineStore } from 'valtio-define'
import { persistent } from 'valtio-define/plugins'

const store = defineStore({
  state: () => ({ count: 0 }),
})

// Register plugin for this specific store only
store.use(persistent())
```

**Key Points:**
* Only affects the specific store instance
* Useful for store-specific functionality
* Can combine with global plugins

## Plugin Context

Plugins receive a context object with store and options:

```tsx
type PluginContext<S extends object> = {
  store: Store<S, Actions<S>, Getters<S>>
  options: StoreDefine<S, ActionsTree, Getters<S>>
}
```

**Key Points:**
* `store`: Full store instance with all methods (`$state`, `$patch`, `$subscribe`, etc.)
* `options`: Original store definition passed to `defineStore`
* Plugins can access and modify store behavior

## Creating Custom Plugins

```tsx
import type { Plugin } from 'valtio-define'

function myPlugin() {
  return ({ store, options }: PluginContext) => {
    // Access store methods
    store.$subscribe((state) => {
      console.log('State changed:', state)
    })

    // Access store options
    if (options.myOption) {
      // Do something
    }
  }
}

// Extend types for plugin options
declare module 'valtio-define/types' {
  export interface StoreDefine<S extends object, A extends ActionsTree, G extends Getters<any>> {
    myOption?: boolean
  }
}

// Use the plugin
valtio.use(myPlugin())

// Or per-store
const store = defineStore({
  state: () => ({ count: 0 }),
  myOption: true,
})
store.use(myPlugin())
```

## Plugin Best Practices

* **Idempotent**: Plugins should be safe to apply multiple times (use WeakSet to track)
* **Type Safety**: Extend `StoreDefine` interface for typed options
* **Side Effects**: Plugins can set up subscriptions, modify state, etc.
* **Cleanup**: Return cleanup functions if needed (store.$subscribe returns unsubscribe)
