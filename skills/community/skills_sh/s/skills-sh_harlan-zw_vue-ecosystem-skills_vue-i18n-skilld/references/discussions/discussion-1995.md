---
number: 1995
title: Is there an alternative of v-html when i'm using Rich text
category: Q&A
created: 2024-10-22
url: "https://github.com/intlify/vue-i18n/discussions/1995"
upvotes: 2
comments: 0
answered: false
---

# Is there an alternative of v-html when i'm using Rich text

I come from the React ecosystem, and when I see `v-html`, I think of `dangerouslySetInnerHTML`.

Usually, I work with `i18next` or `next-intl`, which have features like:

- Rich Text in Next-Intl
- Trans Component in React I18n

But in Vue I18n, I found only:

- HTML Message Syntax

I'm thinking I could find this implementation, for example:

```vue
<script>
const messages = {
  en: {
    message: {
      hello: 'hello <br> world'
    }
  }
}
</script>

<template>
    <p>{{ t.rich("hello", { br: h("br") }) }}</p>
</template>
```
What do you think about this implementation?