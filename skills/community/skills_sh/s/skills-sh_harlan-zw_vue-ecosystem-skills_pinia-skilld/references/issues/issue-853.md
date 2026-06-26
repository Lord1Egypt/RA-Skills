---
number: 853
title: npm error when installing pinia
type: question
state: closed
created: 2021-11-29
url: "https://github.com/vuejs/pinia/issues/853"
reactions: 18
comments: 45
labels: "[help wanted, contribution welcome, upstream]"
---

# npm error when installing pinia

This issue might be a duplicate of https://github.com/posva/pinia/issues/724

I'm trying to install Pinia via npm but get a

> ERESOLVE unable to resolve dependency tree

error.

### Reproduction

- OS: Win10 and Pop!_OS 21.04
- Node version: v16.13.0
- npm version: 8.1.0
- Vue CLI version: 4.5.15
- Vue version: 3.0.0

The project setup on Win10:



I created a temporary repository showing the inial commit after creating the project with the Vue CLI

https://github.com/matthiashermsen/temp-pinia

### Steps to reproduce the behavior

1. Clone the repository
2. Run `npm install`
3. Run `npm install pinia`
4. You should get an error

### Expected behavior

It should install the package without errors.

### Actual behavior

This is the terminal error on Win10

...

---

## Top Comments

**@posva** [maintainer] (+23):

Using `--legacy-peer-deps`, npm 7, yarn, or pnpm should work as a workaround. I found https://github.com/npm/cli/issues/4104 which could be related. Any help on this is appreciated!

Edit: Apparently, this is okay from npm perspective and they expect users to use overrides to pin the vue version

**@bartenra** (+25):

```
npm install --legacy-peer-deps pinia
```

seems to work now.

**@awacode21** (+9):

Same on Mac (MacBook Pro (13-inch, M1, 2020), macOS Monterey)

...