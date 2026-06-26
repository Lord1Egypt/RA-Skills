---
name: utils-subscribe-key
description: Subscribe to changes of a specific primitive property in proxy state
---

# subscribeKey

`subscribeKey` subscribes to changes of a specific primitive property in proxy state. Useful when you only care about one property and want a simpler API than `subscribe`.

## Usage

### Basic subscribeKey

```ts
import { proxy } from 'valtio'
import { subscribeKey } from 'valtio/utils'

const state = proxy({ count: 0, text: 'hello' })

subscribeKey(state, 'count', (v) => {
  console.log('state.count changed to', v)
})

state.count = 1 // Triggers callback with value 1
state.text = 'world' // Doesn't trigger callback
```

### Unsubscribing

```ts
const unsubscribe = subscribeKey(state, 'count', (v) => {
  console.log('count:', v)
})

// Later...
unsubscribe()
```

## Use Cases

### Persisting Single Property

```ts
import { proxy } from 'valtio'
import { subscribeKey } from 'valtio/utils'

const state = proxy({
  theme: localStorage.getItem('theme') || 'light',
  count: 0,
})

subscribeKey(state, 'theme', (theme) => {
  localStorage.setItem('theme', theme)
})
```

### Side Effects for Specific Property

```ts
subscribeKey(state, 'count', (count) => {
  if (count > 10) {
    console.warn('Count exceeded limit')
  }
})
```

## Key Points

- `subscribeKey()` subscribes to a specific primitive property
- Callback receives the new value directly
- Only triggers when the specified key changes
- Returns unsubscribe function
- Simpler than `subscribe()` when watching single property
- Works with primitive values (strings, numbers, booleans)

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/utils/subscribeKey
- https://github.com/pmndrs/valtio
-->
