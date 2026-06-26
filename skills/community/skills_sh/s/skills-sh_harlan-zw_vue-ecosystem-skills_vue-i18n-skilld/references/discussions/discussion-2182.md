---
number: 2182
title: "“Uncaught SyntaxError: vue-i18n-bridge support Vue 2.x only” when upgrading to Vue 3 with @vue/compat"
category: Q&A
created: 2025-05-06
url: "https://github.com/intlify/vue-i18n/discussions/2182"
upvotes: 1
comments: 0
answered: false
---

# “Uncaught SyntaxError: vue-i18n-bridge support Vue 2.x only” when upgrading to Vue 3 with @vue/compat

I’m trying to upgrade my project from Vue 2.7 to Vue 3 using @vue/compat and the vue-i18n-bridge, but I got:
> Uncaught SyntaxError: vue-i18n-bridge support Vue 2.x only  
 
At runtime Vue.version is 3.5.x, but vue-i18n-bridge has this guard in vue-i18n-bridge.js:

```
const version = (Vue && Vue.version && Number(Vue.version.split('.')[0])) || -1;  
if (version !== 2) {  
  throw createI18nError(I18nErrorCodes.BRIDGE_SUPPORT_VUE_2_ONLY);  
}  
```
 
Note: I’m currently on vue-i18n@8.28.2.

How can I get the vue-i18n-bridge working under Vue 3 + @vue/compat (so that it sees “Vue 2” instead of 3)?