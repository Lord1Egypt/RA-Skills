---
number: 4662
title: When importing component inside custom element, style is discarded 
type: other
state: closed
created: 2021-09-23
url: "https://github.com/vuejs/core/issues/4662"
reactions: 65
comments: 87
labels: "[:exclamation: p4-important, scope: custom elements]"
---

# When importing component inside custom element, style is discarded 

### Version
3.2.14

### Reproduction link
github.com







### Steps to reproduce
```bash
git clone git@github.com:gnuletik/vue-ce-import-comp-style.git
cd vue-ce-import-comp-style
yarn run dev
```

Open browser

### What is expected?
CSS of OtherComponent.vue should be applied.
The text "It should be blue" should be blue.

### What is actually happening?
Style is not applied.

---
I tried renaming OtherComponent to OtherComponent.ce.vue, but the result is the same.

This is useful when writing a set of custom elements to have shared components between custom elements.



---

## Top Comments

**@LinusBorg** [maintainer] (+4):

We will solve this, it might take a few more days or weeks though.

**@tony19** (+4):

Also encountered this issue. Here's a couple more repros:

 * w/Vue CLI
 * w/Vite

**@raffobaffo** (+3):

I also encountered it and just worked on a fix, will create a PR soon (my first one here  )