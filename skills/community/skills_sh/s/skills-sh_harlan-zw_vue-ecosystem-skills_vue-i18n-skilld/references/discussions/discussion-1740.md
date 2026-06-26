---
number: 1740
title: how can I retrieve current locale with specified types from useI18n? (typescript support)
category: Q&A
created: 2024-02-15
url: "https://github.com/intlify/vue-i18n/discussions/1740"
upvotes: 4
comments: 0
answered: false
---

# how can I retrieve current locale with specified types from useI18n? (typescript support)

I'm implementing vue-i18n `9.9.1` in a nuxt 3 app, where I have two locales with it's corresponding setup. 

That's the i18n implementation:

```typescript
import { createI18n } from 'vue-i18n';

import en from '../locales/en.json';
import es from '../locales/es.json';

export default defineNuxtPlugin(({ vueApp }) => {
    const i18n = createI18n<[typeof en], 'es' | 'en'>({
        legacy: false,
        globalInjection: true,
        locale: 'en',
        messages: {
            en,
            es,
        },
    });
    vueApp.use(i18n);
});
``` 


Then in a view, I would like to call for an API, sending the current locale of the page.

```typescript
import { useI18n } from 'vue-i18n';
const { locale } = useI18n();

const article = await API.getArticle('whatever', locale.value);
// That makes typescript complains on locale.value because it's not of type 'en' | 'es'

```...