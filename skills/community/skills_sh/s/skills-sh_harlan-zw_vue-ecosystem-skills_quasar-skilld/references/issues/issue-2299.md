---
number: 2299
title: "Feature request: ability to generate a static website"
type: other
state: closed
created: 2018-07-21
url: "https://github.com/quasarframework/quasar/issues/2299"
reactions: 49
comments: 56
---

# Feature request: ability to generate a static website

I think Quasar is almost perfect and I think adding the ability to generate a static website like Nuxt is better than maintaining a "Quasar + Nuxt starter kit" because I think Quasar gave us a freedom better than Nuxt and capabilities much better than Nuxt.

I don't expect this feature to be available in the next release I just want to see it someday available in the most perfect framework Quasar!

---

## Top Comments

**@rstoenescu** [maintainer] (+7):

Quasar is very responsive by design. It takes into account platform, screen size and more. When you prerender / create a static website you can't know beforehand anything about the client who will consume the page and that's a problem.

We've just launched SSR. Let's take it step by step. At some point I'll find a solution for this too. But don't expect it to be too soon as the focus will gradually become shipping v1.0.

**@nothingismagick** (+14):

I like the idea a lot. We are currently stabilizing and documenting the app-extension system - so I could envision a few ways to do this - probably using phantomJS or something similar

**@MohammedAl-Mahdawi** (+1):

@ExNG @panstromek I'm here talking about how Nust generate(prerender) a static website, it will not affect at all how Quasar currently works, it just an extra feature(maybe mode) that makes Quasar in my opinion "complete solution".

It just extra feature/mode so if you don't need it then don't use it, however regarding all the available tools(like Vue-press) that generate(prerender) a static website it is recommended that your website must not contain that much pages(I believe several hundred is ok) however it depends on the system specifications that you will generate the static files on, f...