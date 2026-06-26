---
name: utils-ref
description: Create unproxied references for objects that cannot or should not be proxied
---

# Ref

`ref` allows you to nest objects in a `proxy` that are not wrapped in an inner proxy and therefore not tracked. Use this for objects that cannot be proxied or when you need unproxied references.

## Usage

### Basic ref

```ts
import { proxy, ref } from 'valtio'

const store = proxy({
  users: [
    { id: 1, name: 'Juho', uploads: ref([]) },
  ],
})
```

### Mutating ref Values

Once wrapped in `ref`, mutate without reassigning:

```ts
// ✅ Do mutate
store.users[0].uploads.push({ id: 1, name: 'file.jpg' })

// ✅ Do reset
store.users[0].uploads.splice(0)

// ❌ Don't reassign
store.users[0].uploads = [] // Breaks the ref
```

### Common Use Cases

#### Native Maps and Sets

```ts
import { proxy, ref } from 'valtio'
import { proxyMap } from 'valtio/utils'

const state = proxy({
  // Use ref for native Map if you don't need reactivity
  nativeMap: ref(new Map()),
  // Or use proxyMap if you need reactivity
  reactiveMap: proxyMap(),
})
```

#### DOM Elements

```ts
const state = proxy({
  element: ref(document.getElementById('app')),
})
```

#### React Elements

```ts
const state = proxy({
  component: ref(React.createElement('div')),
})
```

## When to Use ref

Use `ref` when:
- Object cannot be proxied (Map, Set, DOM elements, etc.)
- You don't need reactivity for that object
- You want to preserve object identity

Don't use `ref` as the only state in a proxy (defeats the purpose of using Valtio).

## Key Points

- `ref()` wraps objects to prevent proxying
- Mutate ref values directly, don't reassign the ref
- Use for native Maps/Sets, DOM elements, React elements
- Use `proxyMap`/`proxySet` if you need reactivity
- Don't use `ref` as the only state in a proxy

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/advanced/ref
- https://github.com/pmndrs/valtio
-->
