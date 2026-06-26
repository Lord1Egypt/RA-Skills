---
number: 2322
title: export 'currentInstance' (imported as 'Vue') was not found in 'vue'
type: other
state: closed
created: 2025-11-23
url: "https://github.com/intlify/vue-i18n/issues/2322"
reactions: 8
comments: 14
resolvedIn: 11.2.2
labels: "[ p4-important]"
---

# export 'currentInstance' (imported as 'Vue') was not found in 'vue'

### Reporting a bug?

I updated the library to version 11.2.1 and I get this error. I'm using Vue 3.5.24 with webpack.

### Expected behavior

I updated the library to version 11.2.1 and I get this error. I'm using Vue 3.5.24 with webpack.

### Reproduction

no have

### System Info

```shell
windows 11, vue ^3.5.24, webpack, "vue-i18n": "^11.2.1"
```

### Screenshot



### Additional context

_No response_

### Validations

- [x] Read the Contributing Guidelines
- [x] Read the Documentation
- [x] Check that there isn't already an issue that reports the same bug to avoid creating a duplicate.
- [x] Check that this is a concrete bug. For Q&A open a GitHub Discussions

---

## Top Comments

**@kazupon** [maintainer] (+5):

I've just released v11.2.2
And, vite, webpack and rspack can built vue-i18n and works

Close

**@pzgz** (+3):

same here, ugpraded vue to `3.5.25` doesn't resolve the issue BTW. I am with macos.

**@kazupon** [maintainer]:

Hi!
I've just fixed for this PR

Before I will merge that PR, Can you try to use pre-release the below?  

```sh
npm i https://pkg.pr.new/vue-i18n@2326
```