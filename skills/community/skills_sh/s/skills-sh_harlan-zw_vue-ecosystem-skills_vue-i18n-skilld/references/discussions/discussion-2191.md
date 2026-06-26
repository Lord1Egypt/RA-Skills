---
number: 2191
title: Should I use $t() or t()? (same for $d/d, $n/n)
category: Q&A
created: 2025-05-26
url: "https://github.com/intlify/vue-i18n/discussions/2191"
upvotes: 1
comments: 1
answered: true
---

# Should I use $t() or t()? (same for $d/d, $n/n)

Hi!
I'm a bit confused because in my context (composition API) it seems like I can use either `$t` or `t` (same for `$d`/`d` and `$n`/`n`). I did not find anything in the docs that encourages or discourages the use of one form or the other. The docs only states that `t` (exported by `useI18n()`) can only be used in Composition API.
But is there a benefit or a drawback of using one method or the other? I would like to use only one of them throughout my code.

The only difference I see is that some API available in `$n` is missing in `n` (this `{{ $n(987654321, 'currency', { notation: 'compact' }) }}` cannot be written with `n`), but I think it's not a design choice, rather an overlook.

Thanks!



---

## Accepted Answer

`$t()` only uses messages and the locale from the global composer instance, whereas `t()` returned by `useI18n()` depends on the options passed to `useI18n()`, so it can be either use the global composer instance or local/component specific composer instance.

So if you want to use component specific messages or change the locale in one component without doing it for all, then you'll want to use the `useI18n()` approach. If you only use global stuff you can pick whichever style you like best.

Footnote: `$t()` is injected through Vue's `app.config.globalProperties`, which according to this https://github.com/vuejs/core/pull/13360 won't be supported in vapor mode (vapor mode is unreleased so things may still change), so if you are planning to use Vue's vapor mode in the future, using the `useI18n()` approach is probably better.