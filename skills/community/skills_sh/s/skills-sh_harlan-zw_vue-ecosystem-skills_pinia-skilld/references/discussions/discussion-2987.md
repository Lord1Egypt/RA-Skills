---
number: 2987
title: Issue happening when migrating from @pinia/nuxt 0.4.8 to 0.11.0
category: Help and Questions
created: 2025-05-31
url: "https://github.com/vuejs/pinia/discussions/2987"
upvotes: 4
comments: 3
answered: true
---

# Issue happening when migrating from @pinia/nuxt 0.4.8 to 0.11.0

### Reproduction

Just updated the package and when ran npm run build it starts breaking 

### Steps to reproduce the bug

we are using @pinia/nuxt which we tried to upgrade from 0.4.8 to 0.11.0 and ran npm run build and all nuxt pages are now not working and giving below error, checked all the store configurations given in pinia docs but all in vein can any one help on this 

`[request error] [unhandled] [GET] http://localhost:3000/__nuxt_error?error=true&url=%2Fen%2Fstock%2F&statusCode=500&statusMessage=Server+Error&message=Cannot+read+properties+of+undefined+(reading+%27default%27)
 TypeError: obj.hasOwnProperty is not a function
    at shouldHydrate (/home/anantsingh/Documents/BasParts/nuxter/.output/server/node_modules/pinia/dist/pinia.prod.cjs:232:40)
    ... 8 lines matching cause s...

---

## Accepted Answer

this is fixed by install pinia it was not in package.json earlier https://pinia.vuejs.org/ssr/nuxt.html 
" If you notice that pinia is not installed, please install it manually with your package manager"
```
pnpm add pinia
```