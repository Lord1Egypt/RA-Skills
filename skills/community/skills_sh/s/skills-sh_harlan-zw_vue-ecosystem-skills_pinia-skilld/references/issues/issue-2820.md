---
number: 2820
title: Pinia nuxt version 0.6.0+ causes error when used with pnpm monorepo
type: bug
state: closed
created: 2024-11-01
url: "https://github.com/vuejs/pinia/issues/2820"
reactions: 15
comments: 30
labels: "[bug, has workaround,   pkg:nuxt]"
---

# Pinia nuxt version 0.6.0+ causes error when used with pnpm monorepo

### Reproduction

https://stackblitz.com/~/github.com/kalvenschraut/pinia-nuxt-pnpm-monorepo-issue

### Steps to reproduce the bug

To see issue do
```shell
pnpm install
pnpm --filter website1 run dev
```

can then downgrade @pinia/nuxt to 0.5.5 and run same commands to see it working. Can also upgrade to 0.6.1 to verify still not working
```shell
pnpm update @pinia/nuxt@0.5.5 -r
pnpm --filter website1 run dev
```


### Expected behavior

Page to load and show the users name from the user store

### Actual behavior




### Additional information

In prod builds on my personal site where I first initial saw this was seeing vueDemi.effectScope is not a function error. Downgrading back to 0.5.5 for now until direction can be given

---

## Top Comments

**@posva** [maintainer] (+3):

I did some research, and the problem persists even with upgraded Nuxt and pnpm. The cause of the problem is the removal of the alias for pinia in https://github.com/vuejs/pinia/commit/65031ee77ed46a34bc2359223e24c7944e840819
I needed that change to work in other scenarios so I will investigate this further. In the meantime, here is a workaround: add an alias to your nuxt.config so pinia is resolved correctly:

```ts
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const rootDir = fileURLToPath(new URL('../..', import.meta.url))

export default defineNuxtConfig({
  modules: [ '@pinia/nuxt'],
  alias: {
   pinia: path.resolve(rootDir, 'node_modules/pinia/dist/pinia.mjs')
  }
});
```...

**@posva** [maintainer] (+2):

@rylanharper @maxdzin just thumbs up the issue, that way mantainers can sort issues and find the most searched ones  

**@posva** [maintainer]:

Using the `shamefully-hoist=false` also works