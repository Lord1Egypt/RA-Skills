---
number: 1784
title: Pass globals compatible with Setup Stores
type: feature
state: closed
created: 2022-11-08
url: "https://github.com/vuejs/pinia/issues/1784"
reactions: 15
comments: 16
labels: "[feature request]"
---

# Pass globals compatible with Setup Stores

### What problem is this solving

Currently we can add globals to options stores with

```ts
pinia.use(() => ({ router }))
```

But this only affect option stores

### Proposed solution

Similar to `app.config.globalProperties`: https://vuejs.org/api/application.html#app-config-globalproperties

```ts
pinia.globals.router = router

import type { Router } from 'vue-router'

// typing the globals
declare module 'pinia' {
  export interface PiniaGlobals {
    router: Router
  }
}
```

Then set up stores could receive these properties as an argument:

```ts
defineStore('store', ({ router }) => {
// ...
})
```

Option stores could still use the properties through `this`.

### Describe alternatives you've considered

- Directly adding properties to `pinia` and use `getActivePinia()`. This also works with TypeScript, it not semantic though
- Ideally, users should be able to call `useRouter()` and similar composables within setup stores but this requires a way for libraries to set the active Vue App, so this requires Vue to implement some kind of `setCurrentApp(app)` (needs PR and discussion)

---

## Top Comments

**@posva** [maintainer] (+11):

A workaround to have globals used within setup stores is to pick them up from the app (if possible). here is an example with the router:

```ts
import { getActivePinia } from 'pinia'

export function useRouter() {
  return getActivePinia()?._a.config.globalProperties.$router!
}

export function useRoute() {
  return getActivePinia()?._a.config.globalProperties.$route!
}
```

These functions should work properly within a setup stores as if you were callig the original router composables within a `script setup`

**@posva** [maintainer] (+6):

Yes, you can just call useRouter() within a setup store now! There is a note about this in docs

**@posva** [maintainer] (+1):

There are discussions to make it possible to make `useRouter()` and others _just work_ within store definitions but it's still in discussion

BTW doing this

```ts
function useBarStore(context) {
  return defineStore('...', => {
  })()
}
```

should be avoided as you are not supposed to define a store with the same id multiple times.