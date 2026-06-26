---
number: 1779
title: How to use outside of Vue components (for example in the backend)?
category: Q&A
created: 2024-03-29
url: "https://github.com/intlify/vue-i18n/discussions/1779"
upvotes: 4
comments: 1
answered: false
---

# How to use outside of Vue components (for example in the backend)?

My app consists of different layers, the frontend Vue app, a frontend library, a Node.js backend and a utils package used by both the frontend and backend. All of these need to be internationalized, and obviously I want to use the same translation library/technology for each of them.

I wasn't able to find much documentation about how to use vue-i18n outside of Vue components, but from the TypeScript types it seems that I can probably call `i18n.global.t()` to translate messages. However, as far as I understand, calling `createI18n()` will require Vue as a dependency. This means that people who want to use my frontend library or my utils package will require Vue as a dependency even if they don't use it in their app at all. This is not ideal.

Is there a recommended way to use vue-i18n...

---

## Top Comments

**@NamesMT**:

+1 interested