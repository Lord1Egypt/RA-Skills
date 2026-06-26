---
name: utils-devtools
description: Integrate Valtio state with Redux DevTools Extension for debugging
---

# DevTools

`devtools` integrates Valtio state with the Redux DevTools Extension, allowing you to inspect state changes, time-travel debugging, and manipulate state from the DevTools panel.

## Usage

### Basic DevTools Setup

```ts
import { proxy } from 'valtio'
import { devtools } from 'valtio/utils'

const state = proxy({ count: 0, text: 'hello' })
const unsub = devtools(state, { name: 'state name', enabled: true })
```

### Configuration Options

```ts
devtools(state, {
  name: 'MyAppState', // Name shown in DevTools
  enabled: process.env.NODE_ENV === 'development', // Enable in dev only
})
```

### Vanilla JavaScript

Works in vanilla JavaScript applications:

```ts
import { proxy, subscribe, snapshot } from 'valtio/vanilla'
import { devtools } from 'valtio/utils'

const state = proxy({ count: 0, text: 'hello' })

subscribe(state, () => {
  console.log('state mutated')
  const obj = snapshot(state)
})

devtools(state, { name: 'VanillaState' })
```

### TypeScript Support

For proper TypeScript types, install and import types:

```ts
import type {} from '@redux-devtools/extension'
import { devtools } from 'valtio/utils'

const state = proxy({ count: 0 })
devtools(state, { name: 'State' })
```

### Manipulating State from DevTools

You can dispatch JSON objects from DevTools to change state:

1. Select the state instance from the dropdown
2. Type a JSON object in the dispatch field
3. Click "Dispatch" to update the state

This is useful for testing different state values without modifying code.

## Key Points

- `devtools()` connects Valtio state to Redux DevTools Extension
- Works with plain objects and arrays
- Enable only in development for performance
- Can manipulate state from DevTools panel
- Works in both React and vanilla JavaScript
- Install `@redux-devtools/extension` types for TypeScript support

<!--
Source references:
- https://valtio.pmnd.rs/docs/api/utils/devtools
- https://github.com/pmndrs/valtio
-->
