---
number: 1736
title: How to use in vue plugin
category: Q&A
created: 2024-02-13
url: "https://github.com/intlify/vue-i18n/discussions/1736"
upvotes: 4
comments: 2
answered: false
---

# How to use in vue plugin

I'm working on a vue3 components library plugin. My components contain text in various places. How would i deal with i18n?

Should i always instantiate a new vue-i18n instance in my plugins install function or should i somehow check if there's already one and then somehow add the translation messages to the current instance? 

What would be the best approach to this? 

---

## Top Comments

**@thedamon**:

Never found a solution for this that feels great.

We have generally provided a dictionary and told ppl using our lib that they need to have Vue-i18n installed in their app and they need to merge our dictionary into theirs; and in our lib relied on `$t()` being there or `useI18n()` outside of components, but then we end up with a different instance and potentially different version of vue-i18n inside our components so locale would not be in sync.

We recently have tried to provide our own `createI18n` function and bundle vue-i18n into it and tell users to use that so that to decrease boile...

**@ricardo17coelho**:

I end up with a similiar approach.

I have a vue-i18n instance inside my Plugin.
This instance is only used for "dev" purposes or when i use the "global" instance in some ts/js files.
I expose a fn to "set the i18n locale" in the plugin form the app ( where the plugin is used) :
```
import { setI18nLocale } from '@deepcloud/field-validators'
import i18n from '@/plugins/i18n.ts'

// update plugins i18n locale
watchEffect(() => {
  setI18nLocale(i18n.global.locale.value)
})
```
Otherwise i'm doing the same as purposed here. The plugin, expose the messages and i'm adding the message...