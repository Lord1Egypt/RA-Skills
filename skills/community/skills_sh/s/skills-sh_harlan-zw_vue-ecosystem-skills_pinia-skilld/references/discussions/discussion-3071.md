---
number: 3071
title: @pinia/nuxt auto-import feature not working with nuxt v4
category: Help and Questions
created: 2025-11-17
url: "https://github.com/vuejs/pinia/discussions/3071"
upvotes: 5
comments: 3
answered: true
---

# @pinia/nuxt auto-import feature not working with nuxt v4

### Reproduction

https://github.com/IvanKhartov/pinia-nuxt-bug

### Steps to reproduce the bug

1. install nuxt app (v4)
2. install @pinia/nuxt module (v0.11.3)
3. add configuration into `nuxt.config.ts` - `pinia: { storesDirs: ['./app/stores/**'] }`
4. create folder `app/stores`, and any file with a simple store
5. use data from store in app.vue
6. run dev server (or build app)

### Expected behavior

- no errors, and all works.

### Actual behavior

- error: `useStore is not defined`

### Additional information

Note: for `@pinia/nuxt` v0.11.2 everything works fine

---

## Accepted Answer

  pinia: {
    storesDirs: ['./stores/**']
  }
  just write it in config. I spend 2 hours to solve it). It works for nuxt 4
