---
number: 2236
title: From vue 3.5.0 on, types for $t, $d, etc. are no longer recognised correctly
type: other
state: open
created: 2025-07-23
url: "https://github.com/intlify/vue-i18n/issues/2236"
reactions: 5
comments: 3
labels: "[Status: Review Needed]"
---

# From vue 3.5.0 on, types for $t, $d, etc. are no longer recognised correctly

### Reporting a bug?

From Vue 3.5.0 onwards, the type definitions from vue-i18n no longer display correctly in both PHPStorm 2015.1.3 and VSCode 1.102.0. In my testing I have used the reproduction minimal started with all dependencies updated to their most recent versions as of writing, except for `vue`.

#### Situation with `"vue": "3.4.38"`:

<img width="1326" height="1047" alt="Image" src="https://github.com/user-attachments/assets/f0ff4210-6293-4b1d-8fe8-522ff574ae13" />

<img width="1160" height="760" alt="Image" src="https://github.com/user-attachments/assets/cac1f990-c628-4fca-b817-aed966ab3742" />

#### Situation with `"vue": "3.5.0"` (same with `3.5.0-alpha.1`):

<img width="1326" height="1047" alt="Image" src="https://github.com/user-attachments/assets/5c9f0e68-a403-422b-a626-b890565446b5" />

<img width="1160" height="760" alt="Image" src="https://github.com/user-attachments/assets/9197f259-bb9a-401a-82bb-66a1325a8048" />

### Expected behavior

See previous

### Reproduction

https://github.com/pindab0ter/vitejs-vite-gfrx6w

The latest commit is with the earliest stable version causing the issue (`"vue": "3.5.0"`). The commit before that is in a state with the expected behavior (`"vue": "3.4.38"`).

### System Info

...

---

## Top Comments

**@BobbieGoede** [maintainer] (+2):

WebStorm is using an older version of `@vue/language-server`, configuring it to use the latest version may resolve type issues, see https://youtrack.jetbrains.com/issue/WEB-73932/vue-language-server-3.0.0-Support

I'm not sure whether the same applies to PHPStorm, but if it too uses an older version of Vue Language Server, then types may not work as expected.

**@juntaosun**:

+1，Starting from vue-i18n version 12, it is completely unusable. 
`
vue-i18n  
$t('')  
`

**@starNGC2237**:

same，Webstorm，Vue 3.5.18，Vue-i18n 11.1.11