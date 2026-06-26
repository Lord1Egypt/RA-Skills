---
number: 2894
title: "Initialization ordering: can I manually initialize Pinia instance **before** Vue app instance is created?"
category: Help and Questions
created: 2025-01-22
url: "https://github.com/vuejs/pinia/discussions/2894"
upvotes: 1
comments: 2
answered: true
---

# Initialization ordering: can I manually initialize Pinia instance **before** Vue app instance is created?

I'm migrating a legacy Vue 3 + Vuex app to Pinia, but I stuck in the initialization ordering. This is this the simplified example:

```ts
// main.ts
import App from './ui/App.vue'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useMyStore } from './ui/store'   // Vuex stores / Pinia stores

const pinia = createPinia()
const myStore = useMyStore()
const app = createApp(App)    // App.vue  -> import { apiManager } from 'singleton.ts' -> `apiManager` also uses `useMyStore()` in './ui/store'
app.use(pinia)     // Too late... Can this Pinia instance be initialized earlier?
app.mount('#vue-app')
```

- `App.vue` uses `apiManager` in `singleton.ts`
- `apiManager` in `singleton.ts` uses `useMyStore` in './ui/store'
- (`apiManager` is responsible to fe...

---

## Accepted Answer

**@posva** [maintainer]:

See https://pinia.vuejs.org/core-concepts/outside-component-usage.html#Using-a-store-outside-of-a-component. In short, put your pinia in a different file and import it in those singletons and pass it explicitly to the `useStore()` functions.

```ts
// src/pinia.ts
export const pinia = createPinia()
```

```ts
// src/singleton.ts
import { useStore } from './stores/store.ts
import { pinia } from './pinia.ts

useStore(pinia)
```