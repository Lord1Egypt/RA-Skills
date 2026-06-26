---
number: 18111
title: `ssrContext` variables in `index.html` do not seem to be working
category: CLI - SSR mode
created: 2025-08-29
url: "https://github.com/quasarframework/quasar/discussions/18111"
upvotes: 2
comments: 0
answered: false
---

# `ssrContext` variables in `index.html` do not seem to be working

I'm following this guide https://quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr#boot-files
Based on the documentation, I should be able to use this in my boot file:

```ts
ssrContext.someProp = 'some value';
```

While this throws an error in typescript, I can use `@ts-ignore` to get around it and compile. However, if I then do this in `index.html`:

```
<% if (ctx.mode.ssr) { %>{{ someProp }} <% } %>
```

I get an error complaining that `someProp` is not defined. Yet all that I am doing is following the documentation precisely. Perhaps the documentation is out of date and there are some new requirements that I am not meeting?