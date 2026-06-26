---
number: 2055
title: v-t decrepetation warning after 11.0.0 in console but no usages can be found
category: Q&A
created: 2024-12-25
url: "https://github.com/intlify/vue-i18n/discussions/2055"
upvotes: 2
comments: 2
answered: false
---

# v-t decrepetation warning after 11.0.0 in console but no usages can be found

After upgraded to v11.0.0. Got following console message, pretty annoying, but the strange part is, there's no `v-t` unsage in my project. Any hints I can locate where's the cause?

> [intlify] 'v-t' has been deprecated in v11. Use translate APIs ('t' or '$t') instead.




---

## Top Comments

**@Safirion**:

I don't use v-t in my project either but I get this warning too. 

Moreover


I may have misunderstood the vue-i18n documentation but does this mean that the vuejs option API will no longer be supported by this plugin in next releases ?

Also, I don't understand why there is mention of "legacy" vs "composition" mode in vue-i18n. Since the option API  is not deprecated in vuejs, it seems essential to me to keep it working in vue-i18n.

**@pzgz**:

repo owner has fixed the issue in 11.0.1, thanks a lot