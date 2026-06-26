---
number: 1954
title: "Production build error :("
category: Q&A
created: 2024-09-16
url: "https://github.com/intlify/vue-i18n/discussions/1954"
upvotes: 4
comments: 0
answered: false
---

# Production build error :(

I’ve implemented Vue 3 with Vite and integrated vue-i18n for internationalization . Everything works perfectly in my local development environment, including language files and I18n functionality, without any errors.

However, when I deploy the project to the server and run yarn build, the build process completes without any issues, but when I load the app in the browser, I encounter several errors. The errors include multiple instances of the following:

`SyntaxError: 23 (at @intlify-2rgc3MTt.js:sourcemap:112:17)
    at createCompileError (@intlify-2rgc3MTt.js:sourcemap:112:17)
    at createCoreError (@intlify-2rgc3MTt.js:sourcemap:1646:10)
    at resolveLocale (@intlify-2rgc3MTt.js:sourcemap:1669:13)
    at getLocale (@intlify-2rgc3MTt.js:sourcemap:1649:67)
    at translate (@in...