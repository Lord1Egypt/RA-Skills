---
number: 2246
title: "What exactly the end of \"Legacy API\" means?"
category: Q&A
created: 2025-08-01
url: "https://github.com/intlify/vue-i18n/discussions/2246"
upvotes: 1
comments: 0
answered: false
---

# What exactly the end of "Legacy API" means?

Hello,
I am trying to understand the impact of the deprecation/future removal of Legacy API on my application, from here: https://vue-i18n.intlify.dev/guide/migration/breaking11.html#deprecate-legacy-api-mode

Overall, I do a quite simple use of Vue i18n, I would say ~80%+ of my code simply uses `$t('key')`, upgrading to v9/v10/v11 as we went to Vue 3 was not a major issue.

Back to the legacy API,

My understanding is that it will work fine in applications using Vue Options API, just how we interact with Vue i18n will change. is that correct?

Going further, I could not understand if this will simply means some overloads will work differently (like the changes in v10), or if there will be a whole set of functions that will no longer work, or that I will need to update all my comp...