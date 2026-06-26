---
number: 2379
title: "Using Laravel-style `:dot-notated` replacements instead of `{brackets}` without `messageCompiler` workaround?"
category: Q&A
created: 2026-01-22
url: "https://github.com/intlify/vue-i18n/discussions/2379"
upvotes: 1
comments: 1
answered: true
---

# Using Laravel-style `:dot-notated` replacements instead of `{brackets}` without `messageCompiler` workaround?

Does Vue I18n support Laravel-styled `:dot_notated` replacement placeholders? I checked the documentation but couldn’t find anything suggesting that Vue I18n can handle this format natively.

Since my translation files come from Laravel, I would prefer not to rewrite all placeholders to {key} just to satisfy the Vue I18n syntax. I ended up implementing a custom messageCompiler to support `:key` replacements, but this feature is currently marked as experimental.

...

---

## Accepted Answer

The documented format is the only supported one, if you want a different format you'll need to use a custom message compiler (like you already did) or find another library that already does what you want.