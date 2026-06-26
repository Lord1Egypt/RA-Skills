---
number: 8105
title: `<Transition>` wrapped by `<Suspense>` breaks entirely if interrupted before it completes
type: bug
state: closed
created: 2023-04-17
url: "https://github.com/vuejs/core/issues/8105"
reactions: 41
comments: 10
labels: "[:lady_beetle:  bug, scope: transition, scope: suspense, has PR]"
---

# `<Transition>` wrapped by `<Suspense>` breaks entirely if interrupted before it completes

### Vue version

3.2.47

### Link to minimal reproduction

https://stackblitz.com/edit/github-z3ry59-hbu5x7
SFC Playground

### Steps to reproduce

```vue
<template>
  <transition name="page" mode="out-in" :duration="300">
    <Suspense>
      <component :is="Component" />
    </Suspense>
  </transition>
</template>
```

Click the button marked 'Trigger error'.

This will switch components within the Transition. On next tick, it will switch them back. (To reproduce, it's sufficient to switch them at any point before the transition has finished.)

Note that this follows the component order specified in https://vuejs.org/guide/built-ins/suspense.html#combining-with-other-components.

### What is expected?

I expect no errors.

### What is actually happening?

The following error is thrown:

```
Uncaught DOMException: Failed to execute 'insertBefore' on 'Node': The node before which the new node is to be inserted is not a child of this node.
```

In addition, the content of the Suspense slot is removed and the page remains broken.

### System Info

_No response_

### Any additional comments?

_No response_

---

## Top Comments

**@posva** [maintainer] (+6):

This rings a bell, there could be another open issue about interrupting a transition here but I couldn't find it. It looks similar to https://github.com/vuejs/core/issues/6835 but clearly not the same.

**@kikuchan** (+5):

After deep investigation, I've finally found the solution.

```js
--- packages/runtime-core/src/renderer.ts
+++ packages/runtime-core/src/renderer.ts
@@ -2035,6 +2035,7 @@ function baseCreateRenderer(
     if (needTransition) {
       if (moveType === MoveType.ENTER) {
         transition!.beforeEnter(el!)
+        if (anchor && anchor.parent !== container) anchor = null;
         hostInsert(el!, container, anchor)
         queuePostRenderEffect(() => transition!.enter(el!), parentSuspense)
       } else {
```

The `beforeEnter` internally calls `afterLeave` hooks, and it actual...

**@kikuchan** (+5):

I'm trying to explain what's going on under the hood.

For this issue, there are 2 cases:

1. In **this** case, the `activeBranch` is still in the `hiddenContainer` (I don't know if this is a valid state).
Then, `move` tries to move the `pendingBranch` where the `activeBranch` is, and it fails because the `anchor` (where the `activeBranch` was) is not in the `container`.

2. In the `!delayEnter` case, the `anchor` is properly in the `container`, but `move` triggers `transition.beforeEnter` and hooks alter the DOM tree, thus the `anchor` no longer exists in the `container` on the very ne...