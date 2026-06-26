---
number: 8956
title: QField does not emit native events
type: bug
state: open
created: 2021-04-19
url: "https://github.com/quasarframework/quasar/issues/8956"
reactions: 7
comments: 5
labels: "[kind/bug , Qv2 ]"
---

# QField does not emit native events

**Describe the bug**
QField does not emit its own click event. In vue 2 this could be resolved by using `@click.native`. In vue 3, the native modifier is deprecated in favor of automated attribute fallthrough. 
Attribute fallthrough is blocked by the `inheritAttrs: false` setting on QField. This leaves us with no elegant approach to setting a click handler on q-field elements.

Technically, the workaround below works, but it's rather hacky.
```
const fieldRef = ref<QField>();
onMounted(() => { fieldRef.value.$el.onclick = () => emit('click'); });
```

**Codepen/jsFiddle/Codesandbox (required)**
https://codepen.io/steersbob/pen/QWdVxNE?editors=101

**To Reproduce**
Steps to reproduce the behavior:
1. Click on the field

**Expected behavior**
The notification to be shown.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Platform (please complete the following information):**
Quasar Version: 2.0.0-beta.12
@quasar/app Version: 3.0.0-beta.13
Quasar mode:
  - [x] SPA
  - [x] SSR
  - [x] PWA
  - [x] Electron
  - [x] Cordova
  - [x] Capacitor
  - [x] BEX

Tested on:
  - [x] SPA
  - [ ] SSR
  - [ ] PWA
  - [ ] Electron
  - [ ] Cordova
  - [ ] Capacitor
  - [ ] BEX

OS: Ubuntu 20.04
Node: 14
NPM: 6.14
Yarn: N/A
Browsers: any
iOS: N/A
Android: N/A
Electron: N/A

**Additional context**
I'm not entirely sure whether this should be classified as bug...