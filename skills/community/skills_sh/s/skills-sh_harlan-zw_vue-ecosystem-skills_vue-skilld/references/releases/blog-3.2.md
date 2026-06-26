---
version: 3.2
title: "Vue 3.2 Released!"
date: 2021-08-05
url: https://blog.vuejs.org/posts/vue-3-2
source: blog-release
---

# Vue 3.2 Released!

Vue 3.2 Released! | The Vue Point

[![logo](/logo.svg)The Vue Point](/)

GitHubSource· [RSS Feed](/feed.rss)· Vuejs.org →

<dl><dt>Published on</dt>
<dd>August 5, 2021</dd>
</dl>

# Vue 3.2 Released!

<dl><dt>Authors</dt>
<dd>

- <dl><dt>Name</dt><dd>Evan You</dd><dt>Twitter</dt><dd>@youyuxi</dd></dl>

</dd></dl>

We are excited to announce the release of Vue.js 3.2 "Quintessential Quintuplets"! This release includes many significant new features and performance improvements, and contains no breaking changes.

---

## New SFC Features [](#new-sfc-features)

Two new features for Single File Components (SFCs, aka `.vue` files) have graduated from experimental status and are now considered stable:

- `<script setup>` is a compile-time syntactic sugar that greatly improves the ergonomics when using Composition API inside SFCs.
- `<style> v-bind` enables component state-driven dynamic CSS values in SFC `<style>` tags.

Here is an example component using these two new features together:

vue

```
<script setup>
import { ref } from 'vue'

const color = ref('red')
</script>

<template>
  <button @click="color = color === 'red' ? 'green' : 'red'">
    Color is: {{ color }}
  </button>
</template>

<style scoped>
button {
  color: v-bind(color);
}
</style>
```

Try it out in the SFC Playground, or read their respective documentations:

- `<script setup>`
- `<style> v-bind`

Building on top of `<script setup>`, we also have a new RFC for improving the ergonomics of ref usage with compiler-enabled sugar - please share your feedback here.

## Web Components [](#web-components)

Vue 3.2 introduces a new `defineCustomElement` method for easily creating native custom elements using Vue component APIs:

js

```
import { defineCustomElement } from 'vue'

const MyVueElement = defineCustomElement({
  // normal Vue component options here
})

// Register the custom element.
// After registration, all \`<my-vue-element>\` tags
// on the page will be upgraded.
customElements.define('my-vue-element', MyVueElement)
```

This API allows developers to create Vue-powered UI component libraries that can be used with any framework, or no framework at all. We have also added a new section in our docs on consuming and creating Web Components in Vue.

## Performance Improvements [](#performance-improvements)

3.2 includes some significant performance improvements to Vue's reactivity system, thanks to the great work by @basvanmeurs. Specifically:

- More efficient ref implementation (~260% faster read / ~50% faster write)
- ~40% faster dependency tracking
- ~17% less memory usage

The template compiler also received a number of improvements:

- ~200% faster creation of plain element VNodes
- More aggressive constant hoisting [1] [2]

Finally, there is a new `v-memo` directive that provides the ability to memoize part of the template tree. A `v-memo` hit allows Vue to skip not only the Virtual DOM diffing, but the creation of new VNodes altogether. Although rarely needed, it provides an escape hatch to squeeze out maximum performance in certain scenarios, for example large `v-for` lists.

The usage of `v-memo`, which is a one-line addition, places Vue among the fastest mainstream frameworks in js-framework-benchmark:

![benchmark](/bench.png)

## Server-side Rendering [](#server-side-rendering)

The `@vue/server-renderer` package in 3.2 now ships an ES module build which is also decoupled from Node.js built-ins. This makes it possible to bundle and leverage `@vue/server-renderer` for use inside non-Node.js runtimes such as CloudFlare Workers or Service Workers.

We also improved the streaming render APIs, with new methods for rendering to the Web Streams API. Check out the documentation of `@vue/server-renderer` for more details.

## Effect Scope API [](#effect-scope-api)

3.2 introduces a new Effect Scope API for directly controlling the disposal timing of reactive effects (computed and watchers). It makes it easier to leverage Vue's reactivity API out of a component context, and also unlocks some advanced use cases inside components.

This is low-level API largely intended for library authors, so it's recommended to read the feature's RFC for the motivation and use cases of this feature.

---

For a detailed list of all changes in 3.2, please refer to the full changelog.

## Next Article

[Vue 3 as the New Default](/posts/vue-3-as-the-new-default)

## Previous Article

[Reflections for 2020-2021](/posts/hello-2021)

[← Back to the blog](/)