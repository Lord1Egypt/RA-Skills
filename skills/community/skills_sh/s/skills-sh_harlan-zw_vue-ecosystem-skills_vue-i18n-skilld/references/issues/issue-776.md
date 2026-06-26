---
number: 776
title: Cannot silence fallback warnings like on V8
type: question
state: open
created: 2021-11-08
url: "https://github.com/intlify/vue-i18n/issues/776"
reactions: 4
comments: 13
labels: "[good first issue, help wanted, Type: Documentation,  p1-chore]"
---

# Cannot silence fallback warnings like on V8

### Reporting a bug

By default when fallbacking fail, two warnings are printed
e.g
```
[intlify] Fall back to translate 'bf.headerBar.homeSearchBarPlaceholder' key with 'en' locale
[intlify] Not found 'bf.headerBar.homeSearchBarPlaceholder' key in 'en' locale messages.
```
The documentation clearly state:
> To suppress these warnings (**while keeping those which warn of the total absence of translation for the given key**) set silentTranslationWarn: true, and silentFallbackWarn: true when initializing the createI18n.


Since the failing fallback warnings are **much** too noisy, I want to silence them, but **keep** other i18n warnings.
Unfortunately, it seems that those booleans ha...