---
number: 4314
title: defineCustomElement without shadowDom
type: feature
state: closed
created: 2021-08-11
url: "https://github.com/vuejs/core/issues/4314"
reactions: 63
comments: 32
labels: "[:sparkles: feature request, :cake: p2-nice-to-have, scope: custom elements]"
---

# defineCustomElement without shadowDom

### What problem does this feature solve?
With the 3.2 release we can now define customElement using Vue but it uses a shadowRoot. It could be nice to be able to create custom element without this shadowRoot so It can use the app CSS (even if it means loosing the slot capability)

### What does the proposed API look like?
To avoid breaking changes we could use an option for defineCustomElement

```
const MyVueElement = defineCustomElement({
  // normal Vue component options here
}, {
  shadowRoot: false
})
```



---

## Top Comments

**@gnuletik** (+14):

@jsbaguette, you can copy the `apiCustomElement.ts` file from my PR if you need it.

You just need to replace an import in this file : 
```diff
- import { hydrate, render } from '.'
+ import { hydrate, render } from '@vue/runtime-dom'
```

And install an extra dependency : 
```
npm install --save html-parsed-element
```

Then, you can import this local file in your codebase.
```diff
- import { defineCustomElement } from 'vue'
+ import { defineCustomElement } from './localApiCustomElement.ts'
```

We use it in production.

EDIT:
...

**@dbaumannlt** (+12):

@yyx990803  This is a critical feature for my current client. We are developing web components that will be served by a Content Management System where the CSS will be included in the header of the page. Not being able to pierce the veil of the shadow root is a show stopper. We are currently using Vue 2 with the following package https://github.com/karol-f/vue-custom-element.

The author has indicated that they are not creating a Vue 3 compatible package because defineCustomElement is provided Vue3. Please provide this support in Vue 3.

**@catsmeatman** (+12):

Please merge this PR. It's very useful function. 