---
number: 2972
title: State not updating in Unit Tests when it's set in onmounted
category: Help and Questions
created: 2025-04-14
url: "https://github.com/vuejs/pinia/discussions/2972"
upvotes: 1
comments: 1
answered: true
---

# State not updating in Unit Tests when it's set in onmounted

### Reproduction

https://codesandbox.io/p/github/Yodablues/test-pinia-not-updating/main?import=true

### Steps to reproduce the bug

I've created a codesandbox showing how this doesn't seem to work correctly. In it, I have App.vue with a onBeforeMounted hook calling an action to set some state in pinia. Then in another lifecycle hook, we check the state and it is undefined. Am i just doing this test wrong?


1. Mount your component and have a lifecycle hook set to modify the pinia state.
2. in the next lifecycle hook, notice the state isn't updated.

### Expected behavior

The pinia state should be updated.

### Actual behavior

The state is not updated.

### Additional information

_No response_

---

## Accepted Answer

**@posva** [maintainer]:

You need to pass `stubActions: false` to your test. https://pinia.vuejs.org/cookbook/testing.html#Customizing-behavior-of-actions