---
number: 458
title: Incorrect type declaration file in vue-i18n@9.1.5
type: bug
state: closed
created: 2021-04-15
url: "https://github.com/intlify/vue-i18n/issues/458"
reactions: 8
comments: 2
labels: "[Type: Bug, Status: Review Needed]"
---

# Incorrect type declaration file in vue-i18n@9.1.5

Hello, in the latest version (9.1.5) of this package, the vue-i18n.d.ts file has been generated incorrectly with the following code:

`declare module '@vue/runtime-core' { ... }`

Due to this, all 'vue' and 'vue-i18n ' module exports become unusable. The current type declaration file can be seen here (jsdelivr).

**Module versions:**
 - `vue`: 3.0.11
 - `vue-i18n`: 9.1.5

Thanks in advance.