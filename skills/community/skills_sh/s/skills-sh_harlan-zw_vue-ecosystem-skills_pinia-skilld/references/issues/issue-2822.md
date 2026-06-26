---
number: 2822
title: @pinia/nuxt 0.7.0 error with fresh Nuxt project
type: other
state: closed
created: 2024-11-05
url: "https://github.com/vuejs/pinia/issues/2822"
reactions: 6
comments: 13
---

# @pinia/nuxt 0.7.0 error with fresh Nuxt project

### Reproduction

https://codesandbox.io/p/devbox/lt39mc

### Steps to reproduce the bug

1. `npx nuxi@latest init`
2. `npx nuxi module add pinia`
3. `npm run dev`

### Expected behavior

The "Welcome to Nuxt!" page should appear.

### Actual behavior
```
500
[vite-node] [ERR_LOAD_URL] pinia

at pinia
```

### Additional information

Since Nuxt 3.14 is very new, I tried switching to 3.13 but that didn't help. Earlier versions are incompatibles due to https://github.com/vuejs/pinia/commit/3dab0a6a43f00d7a52d62d53748c7d5e0cb061ea.

Switching to `@pinia/nuxt`@`^0.5.5` fixed the issue.

---

## Top Comments

**@den15dev** (+8):

I managed to make it work after the following two steps:
1. Install @pinia/nuxt:
`npx nuxi@latest module add pinia`

2. Install pinia with the --force flag:
`npm i pinia --force`

The --force flag is important, otherwise, it will output ERESOLVE errors ("Could not resolve dependency: pinia@"*" from the root project", "Conflicting peer dependency: vue@2.6.14")

I don't want to switch to pnpm just for Pinia because I'm using Docker containers.

**@posva** [maintainer]:

I tested locally with pnpm and it works fine. Let's track this at #2820
Using `npm` seems to install `pinia` within the `@pinia/nuxt` folder and this seems to create other issues down the line  If you can, use `pnpm` instead, if not use `npm i --legacy-peer-deps` or `npm i --force pinia`

**@den15dev** (+1):

Got exactly the same issue today with Nuxt 3.13.2. Just ran `npx nuxi@latest module add pinia`, pinia 0.7.0 installed, `'@pinia/nuxt'` has been added to `modules` property of `nuxt.config.js`.

```
500
[vite-node] [ERR_LOAD_URL] pinia
at pinia
```

Downgrading to 0.6.1 didn't help.

Downgrading to 0.5.5 gave the error:
> Cannot start nuxt:  Cannot find module 'pinia/dist/pinia.mjs'