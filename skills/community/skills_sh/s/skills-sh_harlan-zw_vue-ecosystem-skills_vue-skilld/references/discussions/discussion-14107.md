---
number: 14107
title: Why does this work? (event-listner prop)
category: Help/Questions
created: 2025-11-17
url: "https://github.com/orgs/vuejs/discussions/14107"
upvotes: 2
comments: 1
answered: true
---

# Why does this work? (event-listner prop)

Hi I am confused over here,

I made a modal component that I can feed with function props. These can even be validated using runtime validation (as stated here). It feels like an anti-pattern as soon as you use a prop name called "onXxx" in this example, I used `onCallback`. In this example I made the prop a promise so I can showcase the ability to run async calls like this. You can even use the prop to add a conditional in the `template`-tag or in the `script`-tag

`CallbackComponent.vue`
...

---

## Accepted Answer

The template attributes all get mapped down into VNode props (not to be confused with component props). The VNode props are the properties passed into the `h()` calls in a render function.

For `v-on` (or equivalently `@`), it'll be mapped onto a VNode prop prefixed with `on`. e.g. `@click` becomes the VNode prop `onClick`. That part is documented at:

- <https://vuejs.org/guide/extras/render-function.html#v-on>

There are a few other places in the docs that allude to this, but that's probably the most explicit. You can also see this using the Vue Playground to inspect the compiled output for a template with a listener.

Inside the child component, any VNode prop can be turned into a component prop by listing it in `props` (or equivalent with `defineProps`). While it is more common for events to use `emits` (or equivalently `defineEmits`), it is also possible to use `props` for events. One use case for this is detecting whether an event listener is passed, which isn't possible ...