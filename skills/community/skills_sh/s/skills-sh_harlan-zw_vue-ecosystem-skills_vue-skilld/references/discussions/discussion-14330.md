---
number: 14330
title: TransitionGroup not firing v-move at array.push
category: Help/Questions
created: 2026-01-18
url: "https://github.com/orgs/vuejs/discussions/14330"
upvotes: 1
comments: 3
answered: true
---

# TransitionGroup not firing v-move at array.push

Hello everyone. Sorry for my bad English, I'm using a translator.

I'm trying to create a toasts component for Vue 3. The key is that I need new elements to be at the bottom, and older elements to fade upward when a new element is added. The entire component is positioned at the bottom left.

The problem is that v-move only starts working when the list overflows and older toasts are deleted.

As I understand it, when adding an element, I call list.push(), which doesn't change the position of the other elements but simply adds the new element to the end, so v-move doesn't work.

I'm already racking my brain trying to implement this. I've tried display flex and scaleY. Nothing works. Please help.

Link to the playground: https://play.vuejs.org/#eNqFVMlu2zAQ/ZWBcrCC2LLTtBfVMdAWQZECX...

---

## Accepted Answer

If I set the Vue version to 3.5.22 in the Playground it seems to work correctly. This seems to be a regression in 3.5.23.