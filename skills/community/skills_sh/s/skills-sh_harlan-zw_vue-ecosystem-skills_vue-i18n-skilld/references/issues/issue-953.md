---
number: 953
title: "error: Not available in legacy mode"
type: other
state: closed
created: 2022-03-08
url: "https://github.com/intlify/vue-i18n/issues/953"
reactions: 7
comments: 5
labels: "[Status: Review Needed]"
---

# error: Not available in legacy mode

### Reporting a bug?

version:9.2.0-beta.31

example： const { t } = useI18n();    or     const { t } = useI18n({ useScope: 'global'})

error info:
message-compiler.esm-bundler.js:54 Uncaught (in promise) SyntaxError: Not available in legacy mode
    at createCompileError (message-compiler.esm-bundler.js:54:1)
    at createI18nError (vue-i18n.esm-bundler.js:100:30)
    at useI18n (vue-i18n.esm-bundler.js:2210:1)




### Expected behavior

use example is normal

### Reproduction

1

### System Info

```shell
nothing
```


### Screenshot

nothing

### Additional context

nothing

### Validations

- [X] Read the Contributing Guidelines
- [X] Read the Documentation
- [X] Check that there isn't already an issue that reports the same bug to avoid creating a duplicate.
- [X] Check that this is a concrete bug. For Q&A open a GitHub Discussion
- [X] The provided reproduction is a minimal reproducible example of the bug.