---
name: utils-proxy-map
description: Create observable Map-like proxies for tracking changes to Map data structures
---

# proxyMap

`proxyMap` creates a proxy that mimics native `Map` behavior while allowing Valtio to track changes. Native Maps store data in internal slots that aren't observable, so `proxyMap` is needed for reactive Map operations.

## Usage

### Basic proxyMap

```ts
import { proxyMap } from 'valtio/utils'

const state = proxyMap()
state.size // 0

state.set(1, 'hello')
state.size // 1

state.delete(1)
state.size // 0
```

### Nesting in proxy

```ts
import { proxy, useSnapshot } from 'valtio'
import { proxyMap } from 'valtio/utils'

const state = proxy({
  count: 1,
  map: proxyMap(),
})

state.map.set('key', 'value')
```

### Using Objects as Keys

When using objects as keys, wrap them with `ref()` to preserve key equality:

```ts
import { ref } from 'valtio'
import { proxyMap } from 'valtio/utils'

const state = proxyMap()

// ✅ With ref - preserves key equality
const key = ref({})
state.set(key, 'hello')
state.get(key) // 'hello'

// ❌ Without ref - key equality broken
const key2 = {}
state.set(key2, 'value')
state.get(key2) // undefined (different object reference)
```

### Checking if proxyMap

```ts
import { proxy, ref } from 'valtio'
import { proxyMap, isProxyMap } from 'valtio/utils'

const state = proxy({
  nativeMap: ref(new Map()),
  proxyMap: proxyMap(),
})

isProxyMap(state.nativeMap) // false
isProxyMap(state.proxyMap) // true
```

## When to Use

Use `proxyMap` when you need:
- Non-primitive keys (objects, arrays)
- Map-specific operations (union, intersection, etc.)
- Dynamic key structure

Use regular `proxy` with objects when:
- Keys are strings/numbers
- Simple object structure
- Better performance needed

## Key Points

- `proxyMap()` creates observable Map-like proxy
- Same API as native Map
- Use `ref()` for object keys to preserve equality
- Can be nested in `proxy` objects
- Use `isProxyMap()` to check if object is a proxyMap
- Prefer `proxy` with objects when possible (more performant)

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/utils/proxyMap
- https://github.com/pmndrs/valtio
-->
