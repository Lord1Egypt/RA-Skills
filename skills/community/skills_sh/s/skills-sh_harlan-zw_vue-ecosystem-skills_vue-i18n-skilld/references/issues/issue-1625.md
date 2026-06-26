---
number: 1625
title: "setLocaleMessage throws Error \"Cannot assign to read only ...\""
type: other
state: open
created: 2023-11-02
url: "https://github.com/intlify/vue-i18n/issues/1625"
reactions: 2
comments: 0
labels: "[Status: Review Needed]"
---

# setLocaleMessage throws Error "Cannot assign to read only ..."

### Reporting a bug?

I am trying to implement a HMR functionality wich updates the messages part of the plugin. I am using Quasar with Vite and this is my i18n.js boot file:

```
import { createI18n } from 'vue-i18n';
import * as messages from '../lang/index.js';

const i18n = createI18n({
  locale: 'de',
  globalInjection: true,
  messages,
});

export default ({ app }) => {
  app.use(i18n);
};

// HMR implementation for messages
if (import.meta.hot) {
  import.meta.hot.accept('../lang/index.js', async (updatedMessages) => {
    for (const locale of Object.keys(updatedMessages)) {
      i18n.global.setLocaleMessage(locale, updatedMessages[locale]);
    }
  });
}
```

If I update a lang file and the HMR part kicks in, I am getting the following error:
```
vue-i18n.mjs:662 Uncaught (in promise) TypeError: Cannot assign to read only property 'de' of object '[object Module]'
    at Object.setLocaleMessage (vue-i18n.mjs:662:25)
    at Object.setLocaleMessage (vue-i18n.mjs:1139:26)
    at i18n.js?t=1698933754785:23:16
    at client.ts:438:51
    at client.ts:351:7
    at client.ts:206:57
    at Array.forEach (<anonymous>)
    at queueUpdate (client.ts:206:35)
```...