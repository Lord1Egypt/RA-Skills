---
number: 1901
title: How to handle longer texts with mixed HTML
category: Q&A
created: 2024-07-19
url: "https://github.com/intlify/vue-i18n/discussions/1901"
upvotes: 3
comments: 0
answered: false
---

# How to handle longer texts with mixed HTML

How do you store i18n values that are longer-form .. ie paragraphs, lists etc. say 3 paragraphs with links and some list items, if we want to avoid storing HTML inside our `messages`.

We've followed the vue-i18n locale messages pattern in the past but it seems odd to have soemthing like:

```
<p>`$t('app.introText.paragraph1')</p>
<p>`$t('app.introText.paragraph2')</p>
<ul>
  <li><p>`$t('app.introText.list1item1')</p></li>
  <li><p>`$t('app.introText.list1item2')</p></li>
</ul>
```

Using arrays in messages is maybe a little more maintainable/less weird:

```
<p v-for="p in $tm('app.introTextParagraphs')">{{ p }}</p>
<p>`$t('app.introText.paragraph2')</p>
<ul if="$te('app.introTextList1')>
  <li v-for="item in $tm('app.introTextList1')">{{ item }}</li>
</ul>
```

Bu...