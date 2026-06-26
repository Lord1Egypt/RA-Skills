---
number: 8513
title: Relative publicPath with history router mode adds prefix '/' to base href
type: bug
state: open
created: 2021-02-19
url: "https://github.com/quasarframework/quasar/issues/8513"
reactions: 12
comments: 15
labels: "[kind/bug , Qv2 ]"
---

# Relative publicPath with history router mode adds prefix '/' to base href

**Describe the bug**
When setting `publicPath` to './' and using history router mode, the `base href` inserted into the html contains an extra prefix `/`.

This means that I cannot deploy my application to a dynamic environment where it will be hosted at both `www.example.com` and `www.someotherexample.com/apath`.

**To Reproduce**
Steps to reproduce the behavior:
1. Configure `vueRouterMode` to `'history'` in quasar.conf.js
2. Configure `publicPath` to `'./'`, or `'.'` or `''` in quasar.conf.js
3. Run project 

**Expected behavior**
I expect the `<base href` to contain a relative path.

**Screenshots**
<img width="345" alt="image" src="https://user-images.githubusercontent.com/502136/108566109-27395980-7306-11eb-9fb9-e2ce2f3e6770.png">


**Platform (please complete the following information):**
Quasar Version:
@quasar/app Version:
Quasar mode:
  [X] SPA
  [ ] SSR
  [ ] PWA
  [ ] Electron
  [ ] Cordova
  [ ] Capacitor
  [ ] BEX
Tested on:
  [X] SPA
  [ ] SSR
  [ ] PWA
  [ ] Electron
  [ ] Cordova
  [ ] Capacitor
  [ ] BEX
OS: Mac
Node: 10.23
NPM: 6.14.11
Yarn: Not installed
Browsers: Firefox, Chrome
iOS:
Android:
Electron:

...