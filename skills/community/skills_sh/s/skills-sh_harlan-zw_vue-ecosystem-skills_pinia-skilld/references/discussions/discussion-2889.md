---
number: 2889
title: useLocalStorage or useSessionStorage inside pinia store always rewrite refs to default using nuxt
category: Help and Questions
created: 2025-01-15
url: "https://github.com/vuejs/pinia/discussions/2889"
upvotes: 0
comments: 1
answered: true
---

# useLocalStorage or useSessionStorage inside pinia store always rewrite refs to default using nuxt

### Reproduction

https://codesandbox.io/p/devbox/yjgfrk

### Steps to reproduce the bug

1. Go to sandbox
2. Edit refs using the inputs
3. Reload the preview 

### Expected behavior

It should persists data

### Actual behavior

Inside a pinia store, firstly it has the good value then it initializes again and overrides with the default one.

### Additional information

The goal I try to achieve is to persists data for a session and keep my store synced.

---

## Accepted Answer

**@posva** [maintainer]:

You probably need `skipHydrate`

- https://pinia.vuejs.org/cookbook/composables.html
- https://masteringpinia.com/blog/my-top-5-tips-for-using-pinia