---
number: 1686
title: tm function causes type errors
type: bug
state: open
created: 2024-01-08
url: "https://github.com/intlify/vue-i18n/issues/1686"
reactions: 2
comments: 6
labels: "[Type: Bug, good first issue, help wanted,  p3-minor-bug, typescript]"
---

# tm function causes type errors

### Reporting a bug?

When using vue-18n with typescript I have not found a way to properly type the tm function, following https://vue-i18n.intlify.dev/guide/advanced/typescript.html as guide. See the repro that shows a working use case of using the tm + rt functions. But give the following error when vue-tsc is run `error TS2339: Property 'bar' does not exist on type 'number'. {{ rt(test.bar) }}`.
See main.ts and App.vue for the i18n impl.

### Expected behavior

The example code provided below should pass typechecking.

### Reproduction

https://stackblitz.com/edit/vitejs-vite-eac2nt?file=App.vue

### System Info

...