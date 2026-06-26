---
number: 18194
title: "quasar-config.ts: \"Vue: Cannot find module #q-app/wrappers or its corresponding type declarations.\""
category: General - Components / Directives / etc
created: 2025-12-05
url: "https://github.com/quasarframework/quasar/discussions/18194"
upvotes: 2
comments: 0
answered: false
---

# quasar-config.ts: "Vue: Cannot find module #q-app/wrappers or its corresponding type declarations."

I'm the whole day bussy to find out, and I'm looking at the quasar 'playground'.  
I've inherited a project which started in 2018 I believe, so it is not the state of art...? 

The main problem is I think, that quasar is not loaded. The HTML tags keep the quasar component sign like:
<q-header class="..."...>...</q-header>  instead of <header class="..." ...>...</header>. And also not all the class definitions are added to the class attributes.

Now I want to upgrade Node.Js version 16 ==> version 22 and the dependencies including quasar 2.11.x to 2.18.6. 
It is made with Vue 3.5.25, webpack 5.103.0. (not with Vite)

This is my quasar-conf.ts:

...