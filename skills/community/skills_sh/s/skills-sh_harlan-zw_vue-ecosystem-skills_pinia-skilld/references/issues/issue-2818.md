---
number: 2818
title: Pinia devtools will not call `setupDevtoolsPlugin` until `useStore` is called
type: other
state: open
created: 2024-11-01
url: "https://github.com/vuejs/pinia/issues/2818"
reactions: 2
comments: 1
labels: "[contribution welcome,  pkg:devtools]"
---

# Pinia devtools will not call `setupDevtoolsPlugin` until `useStore` is called

### Reproduction

N/A

### Steps to reproduce the bug

There is a related issue https://github.com/vuejs/devtools/issues/672

The reproduction steps are there.

### Expected behavior

Call `setupDevtoolsPlugin` immediately instead of calling it after `useStore`. otherwise devtools cannot read `settings` at mounted.

### Actual behavior

Call `setupDevtoolsPlugin` after someone calls `useStore`

### Additional information

_No response_