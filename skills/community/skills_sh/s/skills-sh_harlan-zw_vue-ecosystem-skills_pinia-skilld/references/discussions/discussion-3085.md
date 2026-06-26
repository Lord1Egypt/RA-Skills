---
number: 3085
title: @pinia/nuxt - No Active Pinia - Advanced Implementation from another plugin
category: Help and Questions
created: 2025-12-08
url: "https://github.com/vuejs/pinia/discussions/3085"
upvotes: 1
comments: 3
answered: true
---

# @pinia/nuxt - No Active Pinia - Advanced Implementation from another plugin

### Reproduction

https://github.com/components-web-app/cwa-nuxt-module/tree/dev

### Steps to reproduce the bug

When running my application I have a module, it adds plugin and it creates many stores that are needed.

https://github.com/components-web-app/cwa-nuxt-module/blob/dev/src/runtime/plugin.ts

It was all working fine until recent updates either within Nuxt or this module.

The `CWA` class creates a sub-class of storage where all the store definitions are created. Before they are created I've confirmed and there is an active pinia instance.

When I am trying to access the stores now, I get `"getActivePinia()" was called but there was no active Pinia. `

...

---

## Accepted Answer

**@posva** [maintainer]:

See https://github.com/vuejs/pinia/pull/2915, you can always getActivePinia() in a different hook, save it, and then set it again after pinia nuxt but you will suffer from the same problem as #2915 