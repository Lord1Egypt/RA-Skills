---
number: 2150
title: Local locale with global messages
category: Q&A
created: 2025-04-02
url: "https://github.com/intlify/vue-i18n/discussions/2150"
upvotes: 1
comments: 0
answered: false
---

# Local locale with global messages

How can I use vue-i18n global messages but with a local locale?
The only variant that works for me
```ts
const { t } = useI18n({
  useScope: 'local',
  inheritLocale: false,
  locale: 'es',
  messages: {
    es: {
        eggs: 'huevos',
    },
  },
});
```

And no other combination of params
I can't use it without `messages` option.

```vue
const { t } = useI18n({ locale: 'es', inheritLocale: false, useScope: 'local' })

<div>
    <h1>{{ t('eggs') }}</h1> // <-- still using en locale
```


```ts
export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: enMessages,
    es: esMessages, // <-- contains required translations
  },
});
```


What's wrong? 