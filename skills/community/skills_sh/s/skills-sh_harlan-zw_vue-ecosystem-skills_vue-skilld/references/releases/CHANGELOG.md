# 3.6.0-beta.6 (2026-02-12)


### Bug Fixes

* **compiler-vapor:** always keyed if fragment when the branch can change (9f7d73d)
* **compiler-vapor:** handle invalid table nesting with dynamic child (#14394) (cd00cb8), closes #14392
* **compiler-vapor:** keep literal interpolation in component slot templates (#14405) (c18e1e2)
* **compiler-vapor:** properly handling of class and style bindings on SVG (#14383) (3019448), closes #14382
* **runtime-vapor:** guard attrs proxy traps for symbol keys (#14447) (1219d7d)
* **runtime-vapor:** guard default slot for createPlainElement (#14422) (6a64941)
* **runtime-vapor:** isolate slotProps per fragment in v-for slots (#14406) (9db9f1e), closes #14397
* **runtime-vapor:** stabilize KeepAlive cache keys with branch-scoped composite keys (d207e9e)
* **runtime-vapor:** update setCurrentBranchKey to return previous key and handle context correctly (c9e52bc)
* **teleport:** ignore to prop changes while disabled (#14438) (102b32b)
* **teleport:** optimize props handling and prevent unnecessary updates (#14440) (90ea8ce), closes #14438
* **templateRef:** don't update setup ref for useTemplateRef key (#14444) (ccd1ddf)
* **templateRef:** avoid setting direct ref of useTemplateRef in dev (#14442) (78eb86c)

### Features

* **compiler-vapor:** add keyed block handling for dynamic keys (862ab17)



# 3.6.0-beta.5 (2026-01-30)

### Bug Fixes

- **runtime-vapor:** preserve slot owner to ensure correct scopeId inheritance for nested components within v-for loops with slots. (#14353) (cb2a17c)
- **transition:** add key for transition if-branches (#14374) (e08308e), closes #14368
- **vapor:** properly move vapor component / slot (#14363) (b0c04eb)
- **vapor:** support directives on vapor components in vdom parent (#14355) (9add6d7)

# 3.6.0-beta.4 (2026-01-23)

### Bug Fixes

- **compile-vapor:** optimize always close tag on rightmost (0db578b)
- **compiler-vapor:** allow multiple children in Transition v-if branch elements (#14317) (212bee4), closes #14316
- **compiler-vapor:** do not escape quotes in root-level text nodes (#14310) (3fc8e4a), closes #14309
- **compiler-vapor:** prevent end tag omission for scope boundary elements (3d550db)
- **keep-alive:** fix caching nested dynamic fragments (#14307) (bd9aa97)
- **runtime-core:** queue mounted hooks added during mount (#14349) (d3b1de3)
- **runtime-dom:** ensure css vars deps tracking when component has no DOM on mount (#14299) (084389e)
- **runtime-vapor:** handle component scopeid on nested slot (#14326) (7324791)
- **runtime-vapor:** prevent v-for crash on looping through null or undefined array (#14328) (e77b6e1)
- **teleport:** apply css vars after hydration (#14343) (b117d11)
- **transition:** handle transition on pre-resolved async components (#14314) (9d30aff)
- **vapor:** refined inline-block nesting check for html abbreviation (9220643)

# 3.6.0-beta.3 (2026-01-12)

### Bug Fixes

- **compiler-vapor:** support `v-if` and `v-for` on the same `<template>` element by correctly wrapping structural directives. (#14289) (ea1c978)
- **keep-alive:** improve KeepAlive caching behavior for async components by re-evaluating caching after resolution (#14285) (6fc638f)
- **runtime-vapor:** prevent event handler execution during emits lookup (#14281) (15f6652), closes #14218 #14280
- **teleport:** handle css var update on nested fragment (#14284) (9bb5046)

### Features

- **runtime-vapor:** allow VDOM components to directly invoke vapor slots via `slots.name()` (#14273) (6ffd55a)
- **vapor:** support rendering VNodes in dynamic components (#14278) (b074a81)

# 3.6.0-beta.2 (2026-01-04)

### Bug Fixes

- **compiler-sfc:** avoid duplicated unref import for vapor mode (#14267) (f9e87ce), closes #14265
- **compiler-vapor:** avoid cache declarations for call expression member access (#14245) (cef372b), closes #14244
- **compiler-vapor:** cache optional call expression (#14246) (7a0cbc0)
- **runtime-core:** support `uid` key for `useInstanceOption` (#14272) (55bdced), closes vuejs/rfcs#814
- **runtime-vapor:** correctly check slot existence in ownKeys (#14252) (1d376e0)
- **runtime-vapor:** handle css vars work with empty VaporFragment (#14268) (8aa3714), closes #14266
- **templateRef:** handling template ref on vdom child with insertion state (#14243) (cc872d6), closes #14242

# 3.6.0-beta.1 (2025-12-23)

Vue 3.6 is now entering beta phase as we have completed the intended feature set for Vapor Mode as outlined in the roadmap! Vapor Mode now has feature parity with all stable features in Virtual DOM mode. Suspense is not supported in Vapor-only mode, but you can render Vapor components inside a VDOM Suspense.

3.6 also includes a major refactor of `@vue/reactivity` based on alien-signals, which significantly improves the reactivity system's performance and memory usage.

For more details about Vapor Mode, see [About Vapor Mode](#about-vapor-mode) section at the end of this release note.

### Features

- **runtime-vapor:** support render block in createDynamicComponent (#14213) (ddc1bae)

### Performance Improvements

- **runtime-vapor:** implement dynamic props/slots source caching (#14208) (1428c06)

### Bug Fixes

- **compiler-vapor:** camelize kebab-case component event handlers (#14211) (b205408)
- **compiler-vapor:** merge component v-model onUpdate handlers (#14229) (e6bff23)
- **compiler-vapor:** wrap handler values in functions for dynamic v-on (#14218) (1e3e1ef)
- **hmr:** suppress `provide()` warning during HMR updates for mounted instances (#14195) (d823d6a)
- **keep-alive:** preserve fragment's scope only if it include a component that should be cached (26b0b37)
- **runtime-core:** remove constructor props for defineComponent (#14223) (ad0a237)
- **runtime-vapor:** implement v-once caching for props and attrs (#14207) (be2b79d)
- **runtime-vapor:** optimize prop handling in VaporTransitionGroup using Proxy (0ceebeb)
- **transition:** move kept-alive node before v-show transition leave finishes (e393552)
- **transition:** optimize prop handling in VaporTransition using Proxy (b092624)
- **transition:** prevent unmounted block from being inserted after transition leave (f9a9fad)

### About Vapor Mode

Vapor Mode is a new compilation mode for Vue Single-File Components (SFC) with the goal of reducing baseline bundle size and improved performance. It is 100% opt-in, and supports a subset of existing Vue APIs with mostly identical behavior.

Vapor Mode has demonstrated the same level of performance with Solid and Svelte 5 in 3rd party benchmarks.

#### General Stability Notes

Vapor Mode is feature-complete in Vue 3.6 beta, but is still considered unstable. For now, we recommend using it for the following cases:

- Partial usage in existing apps, e.g. implementing a perf-sensitive sub page in Vapor Mode.
- Build small new apps entirely in Vapor Mode.

#### Opting in to Vapor Mode

Vapor Mode only works for Single File Components using `<script setup>`. To opt-in, add the `vapor` attribute to `<script setup>`:

```vue
<script setup vapor>
// ...
</script>
```

Vapor Mode components are usable in two scenarios:

1. Inside a Vapor app instance create via `createVaporApp`. Apps created this way avoids pulling in the Virtual DOM runtime code and allows bundle baseline size to be drastically reduced.

2. To use Vapor components in a VDOM app instance created via `createApp`, the `vaporInteropPlugin` must be installed:

   ```js
   import { createApp, vaporInteropPlugin } from "vue";
   import App from "./App.vue";

   createApp(App)
     .use(vaporInteropPlugin) // enable vapor interop
     .mount("#app");
   ```

   A Vapor app instance can also install `vaporInteropPlugin` to allow vdom components to be used inside, but it will pull in the vdom runtime and offset the benefits of a smaller bundle.

#### VDOM Interop Limitations

When the interop plugin is installed, Vapor and non-Vapor components can be nested inside each other. This currently covers standard props, events, and slots usage, but does not yet account for all possible edge cases. For example, there will most likely still be rough edges when using a VDOM-based component library in Vapor Mode.

A know issue is that vapor slots cannot be rendered with `slots.default()` inside a VDOM component. `renderSlot` must be used instead. [Example]

This is expected to improve over time, but in general, we recommend having distinct "regions" in your app where it's one mode or another, and avoid mixed nesting as much as possible.

In the future, we may provide support tooling to enforce Vapor usage boundaries in codebases.

#### Feature Compatibility

By design, Vapor Mode supports a **subset** of existing Vue features. For the supported subset, we aim to deliver the exact same behavior per API specifications. At the same time, this means there are some features that are explicitly not supported in Vapor Mode:

- Options API
- `app.config.globalProperties`
- `getCurrentInstance()` returns `null` in Vapor components
- `@vue:xxx` per-element lifecycle events

Custom directives in Vapor also have a different interface:

```ts
type VaporDirective = (
  node: Element | VaporComponentInstance,
  value?: () => any,
  argument?: string,
  modifiers?: DirectiveModifiers,
) => (() => void) | void;
```

`value` is a reactive getter that returns the binding value. The user can set up reactive effects using `watchEffect` (auto released when component unmounts), and can optionally return a cleanup function. Example:

```ts
const MyDirective = (el, source) => {
  watchEffect(() => {
    el.textContent = source();
  });
  return () => console.log("cleanup");
};
```

#### Behavior Consistency

Vapor Mode attempts to match VDOM Mode behavior as much as possible, but there could still be minor behavior inconsistencies in edge cases due to how fundamentally different the two rendering modes are. In general, we do not consider a minor inconsistency to be breaking change unless the behavior has previously been documented.

# 3.6.0-alpha.7 (2025-12-12)

### Bug Fixes

- **hmr:** handle reload for template-only components switching between vapor and vdom (bfd4f18)
- **hmr:** refactor scope cleanup to use reset method for stale effects management (918b50f)
- **hmr:** track original `__vapor` state during component mode switching (#14187) (158e706)
- **runtime-vapor:** enable injection from VDOM parent to slotted Vapor child (#14167) (2f0676f)
- **runtime-vapor:** track and restore slot owner context for DynamicFragment rendering (#14193) (79aa9db), closes #14192
- **runtime-vapor:** use computed to cache the result of dynamic slot function to avoid redundant calls. (#14176) (92c2d8c)

### Features

- **runtime-vapor:** implement `defineVaporCustomElement` type inference (#14183) (6de8f68)
- **runtime-vapor:** implement `defineVaporComponent` type inference (#13831) (9d9efd4)

# 3.6.0-alpha.6 (2025-12-04)

### Bug Fixes

- **compiler-vapor:** enhance v-slot prop destructuring support (#14165) (5db15cf)
- **compiler-vapor:** only apply v-on key modifiers to keyboard events (#14136) (8e83197)
- **compiler-vapor:** prevent `_camelize` from receiving nullish value for dynamic `v-bind` keys with `.camel` modifier. (#14138) (313d172)
- **compiler-vapor:** prevent nested components from inheriting parent slots (#14158) (0668ea3)
- **compiler-vapor:** support merging multiple event handlers on components (#14137) (f2152d2)
- **KeepAlive:** correct condition for caching inner blocks to handle null cases (71e2495)
- **KeepAlive:** remove unnecessary null check in getInnerBlock call (50602ec)
- **runtime-vapor:** add dev-only warning for non-existent property access during render (#14162) (9bef3be)
- **runtime-vapor:** expose raw setup state to devtools via `devtoolsRawSetupState` (0ab7e1b)
- **templateRef:** prevent duplicate onScopeDispose registrations for dynamic template refs (#14161) (750e7cd)
- **TransitionGroup:** simplify dev-only warning condition for unkeyed children (e70ca5d)

### Features

- **runtime-vapor:** support attrs fallthrough (#14144) (53ab5d5)
- **runtime-vapor:** support custom directives on vapor components (#14143) (e405557)
- **suspense:** support rendering of Vapor components (#14157) (0dcc98f)
- **vapor:** implement `v-once` support for slot outlets (#14141) (498ce69)

# 3.6.0-alpha.5 (2025-11-25)

### Bug Fixes

- **compiler-vapor:** handle `TSNonNullExpression` and improve expression processing (#14097) (092c73a)
- **compiler-vapor:** improve expression caching for shared member roots (#14132) (25ec4f4)
- **compiler-vapor:** prevent duplicate processing of member expressions in expression analysis (#14105) (35d135e)
- **runtime-vapor:** prevent infinite recursion in `vShow`'s `setDisplay` when handling Vapor components. (005ba04)
- **vapor:** more accurate fallthrough attr support (#13972) (584f25f)
- **runtime-vapor:** prevent fragment `updated` hooks from running before the fragment is mounted. (#14123) (b07fa60)

### Features

- **vapor:** support `v-bind()` in CSS (#12621) (b9dca57)

# 3.6.0-alpha.4 (2025-11-14)

### Bug Fixes

- **compiler-vapor:** handle boolean as constant node (#13994) (c1f2289)
- **compiler-vapor:** handle numbers as static text (#13957) (4b9399a)
- **compiler-vapor:** wrap event handler in parentheses for TSExpression (#14061) (0f4edb4)
- **runtime-dom:** useCssModule vapor support (#13711) (abe8fc2)
- **runtime-vapor:** force defer mount when teleport has insertion state (#14049) (b005811)
- **runtime-vapor:** preserve correct parent instance for slotted content (#14095) (fe3a998)
- **transition-group:** support reusable transition group (#14077) (171f3f5)
- **vapor:** v-model and v-model:model co-usage (#13070) (bf2d2b2)

### Features

- **compiler-vapor:** handle asset imports (#13630) (7d4ab91)
- **vapor:** implement defineVaporCustomElement (#14017) (615db5e)
- **runtime-vapor:** dynamic component fallback work with dynamic slots (#14064) (f4b3613)
- **vapor:** support svg and MathML (#13703) (f0d0cfd)
- **vapor:** dom event error handling (#13769) (d2eebe4)

# 3.6.0-alpha.3 (2025-11-06)

### Bug Fixes

- **compiler-vapor:** adjust children generation order for hydration (#13729) (248b394)
- **compiler-vapor:** escape html for safer template output (#13919) (3c31b71)
- **compiler-vapor:** treat template v-for with single component child as component (#13914) (3b5e13c)
- **hmr:** properly stop render effects during hmr re-render (#14023) (34c6ebf)
- **runtime-vapor:** sync parent component block reference during HMR reload (#13866) (b65a6b8)
- **runtime-vapor:** apply v-show to vdom child (#13767) (def21b6), closes #13765
- **runtime-vapor:** fix readonly warning when useTemplateRef has same variable name as template ref (#13672) (e56997f), closes #13665
- **runtime-vapor:** handle vapor attrs fallthrough to vdom component (#13551) (5ce227b)
- **runtime-vapor:** pass plain object props to createVNode during vdom interop (#13382) (6c50e20), closes #14027
- **runtime-vapor:** properly handle consecutive prepend operations with insertionState (#13558) (6a801de), closes #13764
- **runtime-vapor:** properly handle fast remove in keyed diff (07fd7e4)
- **runtime-vapor:** remove v-cloak and add data-v-app after app mount (#14035) (172cb8b)
- **runtime-vapor:** resolve multiple vFor rendering issues (#13714) (348ffaf)
- **runtime-vapor:** setting innerHTML should go through trusted types (#13825) (23bc91c)
- **runtime-vapor:** setting innerHTML should go through trusted types (#14000) (a3453e3)
- **runtime-vapor:** avoid unnecessary block movement in renderList (#13722) (c4f41ee)
- **runtime-core:** handle next host node for vapor component (#13823) (96ca3b0), closes #13824

### Features

- **compiler-vapor:** support keys and nonKeys modifier for component event (#13053) (a697871)
- **hydration:** hydrate vapor async component (#14003) (1e1e13a)
- **hydration:** hydrate VaporTeleport (#14002) (a886dfc)
- **hydration:** hydrate VaporTransition (#14001) (f1fcada)
- **runtime-vapor:** add support for async components in VaporKeepAlive (#14040) (e4b147a)
- **runtime-vapor:** add support for v-once (#13459) (ff5a06c)
- **runtime-vapor:** add withVaporCtx helper to manage currentInstance context in slot blocks (#14007) (d381c2f)
- **runtime-vapor:** v-html and v-text work with component (#13496) (7870fc0)
- **runtime-vapor:** vapor transition work with vapor async component (#14053) (0f4d7fb)
- **runtime-vapor:** vapor transition work with vapor keep-alive (#14050) (c6bbc4a)
- **runtime-vapor:** vapor transition work with vapor teleport (#14047) (d14c5a2)
- **vapor:** defineVaporAsyncComponent (#13059) (6ec403f)
- **vapor:** forwarded slots (#13408) (2182e88)
- **vapor:** hydration (#13226) (d1d35cb)
- **vapor:** set scopeId (#14004) (5bdcd81)
- **vapor:** template ref vdom interop (#13323) (436eda7)
- **vapor:** vapor keepalive (#13186) (35475c0)
- **vapor:** vapor teleport (#13082) (7204cb6)
- **vapor:** vapor transition + transition-group (#12962) (bba328a)

# 3.6.0-alpha.2 (2025-07-18)

### Bug Fixes

- **compiler-vapor:** handle empty interpolation (#13592) (d1f2915)
- **compiler-vapor:** handle special characters in cached variable names (#13626) (a5e106d)
- **compiler-vapor:** selectors was not initialized in time when the initial value of createFor source was not empty (#13642) (f04c9c3)
- **reactivity:** allow collect effects in EffectScope (#13657) (b9fb79a), closes #13656
- **reactivity:** remove link check to align with 3.5 (#13654) (3cb27d1), closes #13620
- **runtime-core:** use \_\_vapor instead of vapor to identify Vapor components (#13652) (ad21b1b)
- **runtime-vapor:** component emits vdom interop (#13498) (d95fc18)
- **runtime-vapor:** handle v-model vdom interop error (#13643) (2be828a)
- **runtime-vapor:** remove access globalProperties warning (#13609) (fca74b0)

# 3.6.0-alpha.1 (2025-07-12)

### Features

- **vapor mode** (#12359) (bfe5ce3)

  Please see [About Vapor Mode](#about-vapor-mode) section below for details.

### Performance Improvements

- **reactivity:** refactor reactivity core by porting alien-signals (#12349) (313dc61)

### Bug Fixes

- **css-vars:** nullish v-bind in style should not lead to unexpected inheritance (#12461) (c85f1b5), closes #12434 #12439 #7474 #7475
- **reactivity:** ensure multiple effectScope `on()` and `off()` calls maintains correct active scope (#12641) (679cbdf)
- **reactivity:** queuing effects in an array (#13078) (826550c)
- **reactivity:** toRefs should be allowed on plain objects (ac43b11)
- **scheduler:** improve error handling in job flushing (#13587) (94b2ddc)
- **scheduler:** recover nextTick from error in post flush cb (2bbb6d2)

### About Vapor Mode

Vapor Mode is a new compilation mode for Vue Single-File Components (SFC) with the goal of reducing baseline bundle size and improved performance. It is 100% opt-in, and supports a subset of existing Vue APIs with mostly identical behavior.

Vapor Mode has demonstrated the same level of performance with Solid and Svelte 5 in 3rd party benchmarks.

#### General Stability Notes

Vapor Mode is available starting in Vue 3.6 alpha. Please note it is still incomplete and unstable during the alpha phase. The current focus is making it available for wider stability and compatibility testing. For now, we recommend using it for the following cases:

- Partial usage in existing apps, e.g. implementing a perf-sensitive sub page in Vapor Mode.
- Build small new apps entirely in Vapor Mode.

We do not recommend migrating existing components to Vapor Mode yet.

#### Pending Features

Things that do not work in this version yet:

- SSR hydration\* (which means it does not work with Nuxt yet)
- Async Component\*
- Transition\*
- KeepAlive\*
- Suspense

Features marked with \* have pending PRs which will be merged during the alpha phase.

#### Opting in to Vapor Mode

Vapor Mode only works for Single File Components using `<script setup>`. To opt-in, add the `vapor` attribute to `<script setup>`:

```vue
<script setup vapor>
// ...
</script>
```

Vapor Mode components are usable in two scenarios:

1. Inside a Vapor app instance create via `createVaporApp`. Apps created this way avoids pulling in the Virtual DOM runtime code and allows bundle baseline size to be drastically reduced.

2. To use Vapor components in a VDOM app instance created via `createApp`, the `vaporInteropPlugin` must be installed:

   ```js
   import { createApp, vaporInteropPlugin } from "vue";
   import App from "./App.vue";

   createApp(App)
     .use(vaporInteropPlugin) // enable vapor interop
     .mount("#app");
   ```

   A Vapor app instance can also install `vaporInteropPlugin` to allow vdom components to be used inside, but it will pull in the vdom runtime and offset the benefits of a smaller bundle.

#### VDOM Interop Limitations

When the interop plugin is installed, Vapor and non-Vapor components can be nested inside each other. This currently covers standard props, events, and slots usage, but does not yet account for all possible edge cases. For example, there will most likely still be rough edges when using a VDOM-based component library in Vapor Mode.

This is expected to improve over time, but in general, we recommend having distinct "regions" in your app where it's one mode or another, and avoid mixed nesting as much as possible.

In the future, we may provide support tooling to enforce Vapor usage boundaries in codebases.

#### Feature Compatibility

By design, Vapor Mode supports a **subset** of existing Vue features. For the supported subset, we aim to deliver the exact same behavior per API specifications. At the same time, this means there are some features that are explicitly not supported in Vapor Mode:

- Options API
- `app.config.globalProperties`
- `getCurrentInstance()` returns `null` in Vapor components
- Implicit instance properties like `$slots` and `$props` are not available in Vapor template expressions
- `@vue:xxx` per-element lifecycle events

Custom directives in Vapor also have a different interface:

```ts
type VaporDirective = (
  node: Element | VaporComponentInstance,
  value?: () => any,
  argument?: string,
  modifiers?: DirectiveModifiers,
) => (() => void) | void;
```

`value` is a reactive getter that returns the binding value. The user can set up reactive effects using `watchEffect` (auto released when component unmounts), and can optionally return a cleanup function. Example:

```ts
const MyDirective = (el, source) => {
  watchEffect(() => {
    el.textContent = source();
  });
  return () => console.log("cleanup");
};
```

#### Behavior Consistency

Vapor Mode attempts to match VDOM Mode behavior as much as possible, but there could still be minor behavior inconsistencies in edge cases due to how fundamentally different the two rendering modes are. In general, we do not consider a minor inconsistency to be breaking change unless the behavior has previously been documented.

## Previous Changelogs

### 3.5.x (2024-04-29 - 2025-06-18)

See [3.5 changelog](./changelogs/CHANGELOG-3.5.md)

### 3.4.x (2023-10-28 - 2024-08-15)

See [3.4 changelog](./changelogs/CHANGELOG-3.4.md)

### 3.3.x (2023-02-05 - 2023-12-29)

See [3.3 changelog](./changelogs/CHANGELOG-3.3.md)

### 3.2.x (2021-07-16 - 2023-02-02)

See [3.2 changelog](./changelogs/CHANGELOG-3.2.md)

### 3.1.x (2021-05-08 - 2021-07-16)

See [3.1 changelog](./changelogs/CHANGELOG-3.1.md)

### 3.0.x (2019-12-20 - 2021-04-01)

See [3.0 changelog](./changelogs/CHANGELOG-3.0.md)
