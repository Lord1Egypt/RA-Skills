---
number: 18193
title: "Upgrading webdependencies - Quasar and Node.Js 16 to Node.JS 22: class qualifiers are not added and HTML tag stil have <q-xxxx ...> instead off just HTML tag?"
category: General - Components / Directives / etc
created: 2025-12-04
url: "https://github.com/quasarframework/quasar/discussions/18193"
upvotes: 1
comments: 0
answered: false
---

# Upgrading webdependencies - Quasar and Node.Js 16 to Node.JS 22: class qualifiers are not added and HTML tag stil have <q-xxxx ...> instead off just HTML tag?

Hello,

I'm upgrading the application from Node.Js 16 to Node.Js 22. I'm also upgrading the quasar dependencies:
"@quasar/extras": "^1.16.3" to "1.17.0"
"quasar": "2.11.10", to version "2.18.6"
We are using quasar as a plugin with Webpack in Vue 3.x. There is Quasar.conf.js created, which is importing app-main.scss. The quasar.fonf.js is imported in the main.ts ("import "./quasar-conf";). 
My feeling is that after the upgrade of Node.JS and quasar, that quasar is not right loaded or...?

But now the css classes are not added like the quasar component <q header .../> 
With Node.Js22/quasar 2.18.6 and I look in the 'Inspector' of the browser console than I see at the class element:
`<q-header id="app" class="test-env text-white" .... />... </q-header>`

In the version with Node.j...