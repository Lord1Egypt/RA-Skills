---
version: 3.3
title: "Announcing Vue 3.3"
date: 2023-05-11
url: https://blog.vuejs.org/posts/vue-3-3
source: blog-release
---

# Announcing Vue 3.3

Announcing Vue 3.3 | The Vue Point

[![logo](/logo.svg)The Vue Point](/)

GitHubSource· [RSS Feed](/feed.rss)· Vuejs.org →

<dl><dt>Published on</dt>
<dd>May 11, 2023</dd>
</dl>

# Announcing Vue 3.3

<dl><dt>Authors</dt>
<dd>

- <dl><dt>Name</dt><dd>Evan You</dd><dt>Twitter</dt><dd>@youyuxi</dd></dl>

</dd></dl>

Today we're excited to announce the release of Vue 3.3 "Rurouni Kenshin"!

This release is focused on developer experience improvements - in particular, SFC `<script setup>` usage with TypeScript. Together with the 1.6 release of Vue Language Tools (previously known as Volar), we have resolved many long-standing pain points when using Vue with TypeScript.

This post provides an overview of the highlighted features in 3.3. For the full list of changes, please consult the full changelog on GitHub.

---

Dependency Updates

When upgrading to 3.3, it is recommended to also update the following dependencies:

- volar / vue-tsc@^1.6.4
- vite@^4.3.5
- @vitejs/plugin-vue@^4.2.0
- vue-loader@^17.1.0 (if using webpack or vue-cli)

- [ + TypeScript DX Improvements](#script-setup-typescript-dx-improvements)
  - [Imported and Complex Types Support in Macros](#imported-and-complex-types-support-in-macros)
  - [Generic Components](#generic-components)
  - [More Ergonomic defineEmits](#more-ergonomic-defineemits)
  - [Typed Slots with defineSlots](#typed-slots-with-defineslots)
- [Experimental Features](#experimental-features)
  - [Reactive Props Destructure](#reactive-props-destructure)
  - [defineModel](#definemodel)
- [Other Notable Features](#other-notable-features)
  - [defineOptions](#defineoptions)
  - [Better Getter Support with toRef and toValue](#better-getter-support-with-toref-and-tovalue)
  - [JSX Import Source Support](#jsx-import-source-support)
- [Maintenance Infrastructure Improvements](#maintenance-infrastructure-improvements)

## `<script setup>` + TypeScript DX Improvements [](#script-setup-typescript-dx-improvements)

### Imported and Complex Types Support in Macros [](#imported-and-complex-types-support-in-macros)

Previously, types used in the type parameter position of `defineProps` and `defineEmits` were limited to local types, and only supported type literals and interfaces. This is because Vue needs to be able to analyze the properties on the props interface in order to generate corresponding runtime options.

This limitation is now resolved in 3.3. The compiler can now resolve imported types, and supports a limited set of complex types:

vue

```
<script setup lang="ts">
import type { Props } from './foo'

// imported + intersection type
defineProps<Props & { extraProp?: string }>()
</script>
```

Do note that complex types support is AST-based and therefore not 100% comprehensive. Some complex types that require actual type analysis, e.g. conditional types, are not supported. You can use conditional types for the type of a single prop, but not the entire props object.

- Details: PR#8083

### Generic Components [](#generic-components)

Components using `<script setup>` can now accept generic type parameters via the `generic` attribute:

vue

```
<script setup lang="ts" generic="T">
defineProps<{
  items: T[]
  selected: T
}>()
</script>
```

The value of `generic` works exactly the same as the parameter list between `<...>` in TypeScript. For example, you can use multiple parameters, `extends` constraints, default types, and reference imported types:

vue

```
<script setup lang="ts" generic="T extends string | number, U extends Item">
import type { Item } from './types'
defineProps<{
  id: T
  list: U[]
}>()
</script>
```

This feature previously required explicit opt-in, but is now enabled by default in the latest version of volar / vue-tsc.

- Discussion: RFC#436
- Related: generic `defineComponent()` - PR#7963

### More Ergonomic `defineEmits` [](#more-ergonomic-defineemits)

Previously, the type parameter for `defineEmits` only supports the call signature syntax:

ts

```
// BEFORE
const emit = defineEmits<{
  (e: 'foo', id: number): void
  (e: 'bar', name: string, ...rest: any[]): void
}>()
```

The type matches the return type for `emit`, but is a bit verbose and awkward to write. 3.3 introduces a more ergonomic way of declaring emits with types:

ts

```
// AFTER
const emit = defineEmits<{
  foo: [id: number]
  bar: [name: string, ...rest: any[]]
}>()
```

In the type literal, the key is the event name and the value is an array type specifying the additional arguments. Although not required, you can use the labeled tuple elements for explicitness, like in the example above.

The call signature syntax is still supported.

### Typed Slots with `defineSlots` [](#typed-slots-with-defineslots)

The new `defineSlots` macro can be used to declare expected slots and their respective expected slot props:

vue

```
<script setup lang="ts">
defineSlots<{
  default?: (props: { msg: string }) => any
  item?: (props: { id: number }) => any
}>()
</script>
```

`defineSlots()` only accepts a type parameter and no runtime arguments. The type parameter should be a type literal where the property key is the slot name, and the value is a slot function. The first argument of the function is the props the slot expects to receive, and its type will be used for slot props in the template. The returning value of `defineSlots` is the same slots object returned from `useSlots`.

Some current limitations:

- Required slots checking is not yet implemented in volar / vue-tsc.
- Slot function return type is currently ignored and can be `any`, but we may leverage it for slot content checking in the future.

There is also a corresponding `slots` option for `defineComponent` usage. Both APIs have no runtime implications and serve purely as type hints for IDEs and `vue-tsc`.

- Details: PR#7982

## Experimental Features [](#experimental-features)

### Reactive Props Destructure [](#reactive-props-destructure)

Previously part of the now-dropped Reactivity Transform, reactive props destructure has been split into a separate feature.

The feature allows destructured props to retain reactivity, and provides a more ergonomic way to declare props default values:

vue

```
<script setup>
import { watchEffect } from 'vue'

const { msg = 'hello' } = defineProps(['msg'])

watchEffect(() => {
  // accessing \`msg\` in watchers and computed getters
  // tracks it as a dependency, just like accessing \`props.msg\`
  console.log(\`msg is: ${msg}\`)
})
</script>

<template>{{ msg }}</template>
```

This feature is experimental and requires explicit opt-in.

- Details: RFC#502

### `defineModel` [](#definemodel)

Previously, for a component to support two-way binding with `v-model`, it needs to (1) declare a prop and (2) emit a corresponding `update:propName` event when it intends to update the prop:

vue

```

<script setup>
const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])
console.log(props.modelValue)

function onInput(e) {
  emit('update:modelValue', e.target.value)
}
</script>

<template>
  <input :value="modelValue" @input="onInput" />
</template>
```

3.3 simplifies the usage with the new `defineModel` macro. The macro automatically registers a prop, and returns a ref that can be directly mutated:

vue

```

<script setup>
const modelValue = defineModel()
console.log(modelValue.value)
</script>

<template>
  <input v-model="modelValue" />
</template>
```

This feature is experimental and requires explicit opt-in.

- Details: RFC#503

## Other Notable Features [](#other-notable-features)

### `defineOptions` [](#defineoptions)

The new `defineOptions` macro allows declaring component options directly in `<script setup>`, without requiring a separate `<script>` block:

vue

```
<script setup>
defineOptions({ inheritAttrs: false })
</script>
```

### Better Getter Support with `toRef` and `toValue` [](#better-getter-support-with-toref-and-tovalue)

`toRef` has been enhanced to support normalizing values / getters / existing refs into refs:

js

```
// equivalent to ref(1)
toRef(1)
// creates a readonly ref that calls the getter on .value access
toRef(() => props.foo)
// returns existing refs as-is
toRef(existingRef)
```

Calling `toRef` with a getter is similar to `computed`, but can be more efficient when the getter is just performing property access with no expensive computations.

The new `toValue` utility method provides the opposite, normalizing values / getters / refs into values:

js

```
toValue(1) //       --> 1
toValue(ref(1)) //  --> 1
toValue(() => 1) // --> 1
```

`toValue` can be used in composables in place of `unref` so that your composable can accept getters as reactive data sources:

js

```
// before: allocating unnecessary intermediate refs
useFeature(computed(() => props.foo))
useFeature(toRef(props, 'foo'))

// after: more efficient and succinct
useFeature(() => props.foo)
```

The relationship between `toRef` and `toValue` is similar to that between `ref` and `unref`, with the main difference being the special handling of getter functions.

- Details: PR#7997

### JSX Import Source Support [](#jsx-import-source-support)

Currently, Vue's types automatically registers global JSX typing. This may cause conflict with used together with other libraries that needs JSX type inference, in particular React.

Starting in 3.3, Vue supports specifying JSX namespace via TypeScript's jsxImportSource option. This allows the users to choose global or per-file opt-in based on their use case.

For backwards compatibility, 3.3 still registers JSX namespace globally. **We plan to remove the default global registration in 3.4.** If you are using TSX with Vue, you should add explicit `jsxImportSource` to your `tsconfig.json` after upgrading to 3.3 to avoid breakage in 3.4.

## Maintenance Infrastructure Improvements [](#maintenance-infrastructure-improvements)

This release builds upon many maintenance infrastructure improvements that allow us to move faster with more confidence:

- 10x faster builds by separating type checking from the rollup build and moving from `rollup-plugin-typescript2` to `rollup-plugin-esbuild`.
- Faster tests by moving from Jest to Vitest.
- Faster types generation by moving from `@microsoft/api-extractor` to `rollup-plugin-dts`.
- Comprehensive regression tests via ecosystem-ci - catches regressions in major ecosystem dependents before releases!

As planned, we aim to start making smaller and more frequent feature releases in 2023. Stay tuned!

## Next Article

[Vue 2 is Approaching End Of Life](/posts/vue-2-eol)

## Previous Article

[Volar: a New Beginning](/posts/volar-a-new-beginning)

[← Back to the blog](/)