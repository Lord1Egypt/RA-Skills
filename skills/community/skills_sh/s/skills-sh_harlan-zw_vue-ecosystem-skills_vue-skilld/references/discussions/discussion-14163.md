---
number: 14163
title: "Source maps do not work with defineCustomElement and customElement: true"
category: Help/Questions
created: 2025-12-03
url: "https://github.com/orgs/vuejs/discussions/14163"
upvotes: 1
comments: 1
answered: false
---

# Source maps do not work with defineCustomElement and customElement: true

Hey all,

I am trying to get source maps to work in a project that is using `defineCustomElement` and `customElement: true`, so all component styling is added to the shadowRoot of the custom element. I made a small reproduction repository which you can find here https://github.com/Sanderovich/vue-3.5.25-custom-elements-sourcemap.

With `build.sourcemap` set to `true` or `inline` the source maps are not added to the inline styling in the shadowRoot. Does anybody have an idea how to fix this, or an explanation why this does not work, or did I stumble upon a bug?

---

## Top Comments

**@edison1105** [maintainer]:

It should not be supported. Currently, only the styles are added to the shadowRoot, and source maps are not included