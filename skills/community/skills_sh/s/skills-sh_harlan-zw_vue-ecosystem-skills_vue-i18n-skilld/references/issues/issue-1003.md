---
number: 1003
title: `i18n.global.locale` type definiton wrong
type: other
state: open
created: 2022-05-08
url: "https://github.com/intlify/vue-i18n/issues/1003"
reactions: 4
comments: 16
labels: "[ p4-important, typescript]"
---

# `i18n.global.locale` type definiton wrong

### Reporting a bug?

When I implemented a function to globally switch locale as follows:
<img width="409" alt="截屏2022-05-07 下午11 31 39" src="https://user-images.githubusercontent.com/15679461/167280563-b0d39325-3257-464e-88f2-d97002f7b75b.png">

The type definition for `i18n.global.locale` is wrong:
<img width="591" alt="截屏2022-05-07 下午11 32 31" src="https://user-images.githubusercontent.com/15679461/167280585-e5b1d0ff-83dc-4008-86b8-a9a595a9ba2e.png">

By printing out the console, I was able to see that `i18n.global.locale` should be a computed value


### Expected behavior

TypeScript not throw error

### Reproduction

Type definition problem

### System Info

```shell
System:
  OS: macOS 12.3.1
  CPU: (8) x64 Intel(R) Core(TM) i5-8259U CPU @ 2.30GHz
  Memory: 171.65 MB / 16.00 GB
  Shell: 5.8 - /bin/zsh
Binaries:
  Node: 16.13.2 - ~/.nvm/versions/node/v16.13.2/bin/node
  Yarn: 1.22.10 - /usr/local/bin/yarn
  npm: 8.6.0 - ~/.nvm/versions/node/v16.13.2/bin/npm
  Watchman: 2021.10.18.00 - /usr/local/bin/watchman
Browsers:
  Brave Browser: 91.1.26.77
  Chrome: 101.0.4951.54
  Safari: 15.4

"vue": "^3.2.25",
"vue-i18n": "^9.1.10",
"@intlify/vite-plugin-vue-i18n": "^3.4.0",
"@vitejs/plugin-vue": "^2.3.1",
```...