---
name: utils-proxy-set
description: Create observable Set-like proxies for tracking changes to Set data structures
---

# proxySet

`proxySet` creates a proxy that mimics native `Set` behavior while allowing Valtio to track changes. Native Sets store data in internal slots that aren't observable, so `proxySet` is needed for reactive Set operations.

## Usage

### Basic proxySet

```ts
import { proxySet } from 'valtio/utils'

const state = proxySet([1, 2, 3])

state.add(4)
state.delete(1)
state.forEach((v) => console.log(v)) // 2, 3, 4
```

### Nesting in proxy

```ts
import { proxy } from 'valtio'
import { proxySet } from 'valtio/utils'

const state = proxy({
  count: 1,
  set: proxySet(),
})

state.set.add('value')
```

### Set Operations

`proxySet` supports all native Set methods including new Set methods:

```ts
const set1 = proxySet([1, 2, 3])
const set2 = proxySet([2, 3, 4])

// Intersection
set1.intersection(set2) // Set {2, 3}

// Union
set1.union(set2) // Set {1, 2, 3, 4}

// Difference
set1.difference(set2) // Set {1}

// Symmetric difference
set1.symmetricDifference(set2) // Set {1, 4}

// Subset/superset checks
set1.isSubsetOf(set2) // false
set1.isSupersetOf(set2) // false
set1.isDisjointFrom(set2) // false
```

### Checking if proxySet

```ts
import { proxy, ref } from 'valtio'
import { proxySet, isProxySet } from 'valtio/utils'

const state = proxy({
  nativeSet: ref(new Set()),
  proxySet: proxySet(),
})

isProxySet(state.nativeSet) // false
isProxySet(state.proxySet) // true
```

## When to Use

Use `proxySet` when you need:
- Unique value storage
- Set operations (union, intersection, difference)
- Mathematical set operations

Use regular arrays when:
- Duplicates allowed
- Simple list operations
- Better performance needed

## Key Points

- `proxySet()` creates observable Set-like proxy
- Same API as native Set
- Supports all Set methods including new ones (intersection, union, etc.)
- Can be nested in `proxy` objects
- Use `isProxySet()` to check if object is a proxySet
- Prefer arrays when Set operations aren't needed (more performant)

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/utils/proxySet
- https://github.com/pmndrs/valtio
-->
