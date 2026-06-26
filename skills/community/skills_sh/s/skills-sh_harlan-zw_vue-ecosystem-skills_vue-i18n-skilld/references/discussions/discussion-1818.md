---
number: 1818
title: Any way to disable this new warning message for vue-i18n-bridge v10 not being released?
category: Q&A
created: 2024-04-23
url: "https://github.com/intlify/vue-i18n/discussions/1818"
upvotes: 3
comments: 0
answered: false
---

# Any way to disable this new warning message for vue-i18n-bridge v10 not being released?

This message seems to have no way to silence it and just creates a ton of noise in dev and unit testing specifically, which causes it to output every time vue-i18n-bridge is initialized (which is a lot).

```
stderr | initDev (file:/app/node_modules/vue-i18n-bridge/dist/vue-i18n-bridge.mjs:46:17)
vue-i18n-bridge v10 will not be released, since vue-i18n-bridge is for Vue 2, which is already past EOL.
```

Is there really no way to disable this? I can't seem to find any way since it seems forced when in dev.