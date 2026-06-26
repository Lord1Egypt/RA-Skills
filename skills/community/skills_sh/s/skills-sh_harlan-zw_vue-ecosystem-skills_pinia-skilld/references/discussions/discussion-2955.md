---
number: 2955
title: Reset Pinia
category: Help and Questions
created: 2025-03-25
url: "https://github.com/vuejs/pinia/discussions/2955"
upvotes: 1
comments: 1
answered: true
---

# Reset Pinia

Hey,

In short: can we reset the Pinia repo completely?
I know that we can remove all data from the Pinia store, e.g. reset to initial values. But can we reinitiate the `defineStore` function after that, e.g. execute it again?

Thanks!



---

## Accepted Answer

**@posva** [maintainer]:

You will need to dispose of all stores. Currently this is only doable through an internal pinia._s property.
It can also be implemented by collecting all store references in a pinia plugin (no need of an internal property )