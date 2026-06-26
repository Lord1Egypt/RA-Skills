---
number: 3033
title: "Cannot use Pinia stores in Nuxt layers:  \"getActivePinia()\" was called but there was no active Pinia. Are you trying to use a store before calling \"app.use(pinia)\"?"
category: Help and Questions
created: 2025-09-05
url: "https://github.com/vuejs/pinia/discussions/3033"
upvotes: 1
comments: 3
answered: true
---

# Cannot use Pinia stores in Nuxt layers:  "getActivePinia()" was called but there was no active Pinia. Are you trying to use a store before calling "app.use(pinia)"?

### Reproduction

https://github.com/okainov/pinia-nuxt-layers-bug-repro

### Summary

I'm observing the issue when stores are defined and working well in the base layer (as well as in `.playground`), it does NOT work at all with the app extending the layer. The error I'm getting is 

>[]: "getActivePinia()" was called but there was no active Pinia. Are you trying to use a store before calling "app.use(pinia)"? See https://pinia.vuejs.org/core-concepts/outside-component-usage.html for help. This will fail in production.

### Steps to reproduce the bug

...

---

## Accepted Answer

While I played around with the reproducer for #3028, I was really surprised that it would work if I fix the imports thingy. So I digged deeper and seems like I found what was causing the issue

Problematic code:
```ts
import { defineStore } from 'pinia'

export const useTestStore = defineStore('test', () => {
```

Working code:
```ts
//import { defineStore } from 'pinia'

export const useTestStore = defineStore('test', () => {
```

Yes, if I remove import `defineStore` it starts working!

@posva do you really think it's not a bug? Did I miss some documentation saying "do not use imports in layers" or something similar?