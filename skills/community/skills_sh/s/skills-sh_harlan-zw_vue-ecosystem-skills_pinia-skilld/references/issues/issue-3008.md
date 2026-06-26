---
number: 3008
title: Pinia 3.0.3 is not compitable with Nuxt 4.0
type: other
state: closed
created: 2025-07-16
url: "https://github.com/vuejs/pinia/issues/3008"
reactions: 8
comments: 3
---

# Pinia 3.0.3 is not compitable with Nuxt 4.0

### Reproduction

Upgrade to Nuxt 4.0

### Steps to reproduce the bug

Hi!

For some reason Pinia is no longer compitable with Nuxt 4.0 that while there were no issues with its Alpha counter part.

 WARN  Module pinia is disabled due to incompatibility issues:                                                                                              
 - [nuxt] Nuxt version ^3.15.0 is required but currently using 4.0.0


### Expected behavior

The module should work without warning or getting disabled.

### Actual behavior

The module gets disabled

### Additional information

pinia: 3.0.3
nuxt: 4.0.0

---

## Top Comments

**@GalacticHypernova**:

I opened a PR for Nuxt v4 support.

In the meantime, those who want to use Pinia with v4 can change `node_modules\@pinia\nuxt\dist\module.mjs` from:
```ts
const module = defineNuxtModule({
  meta: {
    name: "pinia",
    configKey: "pinia",
    compatibility: {
      nuxt: "^3.15.0 || ^4.0.0-0"
    }
  },
  ...
```

To:
```ts
const module = defineNuxtModule({
  meta: {
    name: "pinia",
    configKey: "pinia",
    compatibility: {
      nuxt: "^3.15.0 || ^4.0.0"
    }
  },
  ...
```