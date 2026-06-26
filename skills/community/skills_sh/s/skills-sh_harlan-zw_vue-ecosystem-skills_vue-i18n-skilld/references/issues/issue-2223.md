---
number: 2223
title: "SyntaxError: Duplicate `useI18n` calling by local scope. Please don't call it on local scope"
type: other
state: closed
created: 2025-07-02
url: "https://github.com/intlify/vue-i18n/issues/2223"
reactions: 3
comments: 23
labels: "[ p5-urgent]"
---

# SyntaxError: Duplicate `useI18n` calling by local scope. Please don't call it on local scope

### Reporting a bug?

11.1.6 seems to have introduced a breaking change.
The update broke multiple of our projets because of https://github.com/intlify/vue-i18n/pull/2203.
We now have a blank page with this error in the console:
> SyntaxError: Duplicate useI18n calling by local scope. Please don't call it on local scope

This seems to come from `const { t } = useI18n()` inside a Pinia Store.

After a bit of bebugging, this seems to be an error on our end, but it's not clear !
Simply changing from `const { t } = useI18n();` to `const { t } = useI18n({ useScope: 'global' });` fixed the problem.
It make sense, since a composable or Pinia store don't have a <i18n> customBlock, so they don't have a local scope...

...