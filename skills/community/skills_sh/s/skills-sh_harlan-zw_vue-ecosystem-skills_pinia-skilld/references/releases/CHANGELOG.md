### 3.0.4 (2025-11-05)

### Features

- **warn:** detect global context on the server side (#2983) (be9e356)

### Bug Fixes

- incorrect supported values in package.json (5cc55c2)

### 3.0.3 (2025-06-04)

No code changes.

### 3.0.2 (2025-04-09)

### Bug Fixes

- fix `obj.hasOwnProperty` in `shouldHydrate`

### 3.0.1 (2025-02-12)

### Bug Fixes

- avoid including devtools code in builds (d3b24a3), closes #2910

## 3.0.0 (2025-02-11)

###  BREAKING CHANGES

- We now use the native `Awaited` introduced in TS 4.5. This shouldn't affect you.
- `PiniaStorePlugin` is now removed. Use `PiniaPlugin` instead.
- `defineStore({ id: 'id' })` is now removed. Use `defineStore('id')` instead
- The new version of Vue Devtools is too large to be included in the iife version and has been removed. It must now be included manually (depending on your workflow)

### Code Refactoring

- remove deprecated alias (87c6182)
- remove internal type `_Awaited` (ce48ec4)
- remove support for `id` as a property (24b2b89)

### 2.3.1 (2025-01-20)

### Bug Fixes

- **types:** support for Vue 2.7 (d14e1a7)

## 2.3.0 (2024-12-04)

### Features

- writable `computed`s to be picked up by `mapWritableState` (#2847) (0fa633e)

### Bug Fixes

- avoid npm bug when resolving optional deps (#2841) (1e45f33)

### 2.2.8 (2024-11-28)

### Features

- deprecate old defineStore (d1858e8)

### Bug Fixes

- avoid immediate computing with `storeToRefs` (67d3109), closes #2812
- **types:** unwrap refs in `mapWritableState` for setup stores (#2805) (ea14e53), closes #2804

### 2.2.7 (2024-11-27)

### Bug Fixes

- **devtools:** avoid running outside of browsers (eb5e6fd), closes #2843

### 3.0.1 (2025-02-12)

### Bug Fixes

- avoid including devtools code in builds (d3b24a3), closes #2910

## 3.0.0 (2025-02-11)

This version of Pinia has no new features, it drops support for Vue 2 and other deprecated APIs. It should be an straightforward upgrade for most users! 

See the migration guide for help.

###  BREAKING CHANGES

- We now use the native `Awaited` introduced in TS 4.5, so you need at least TS 4.5 to use Pinia 3.0. That being said, it's always better to have an up to date version of TS.
- `PiniaStorePlugin` is now removed. Use `PiniaPlugin` instead.
- `defineStore({ id: 'id' })` is now removed. Use `defineStore('id')` instead
- Pinia is now published as a `type: module` package but it still provides CJS versions dist files

### Code Refactoring

- remove deprecated aliases (87c6182)
- remove internal type `_Awaited` (ce48ec4)
- remove support for `id` as a property in `defineStore` (24b2b89)

### 2.3.1 (2025-01-20)

### Bug Fixes

- **types:** support for Vue 2.7 (d14e1a7)

## 2.3.0 (2024-12-04)

This version requires at least Vue 2.7. On January 2025, Pinia 3.0 will drop support for Vue 2 (which already reached EOL last year). If you need support or help migrating, you can book help with Eduardo (@posva).

### Features

- writable `computed`s to be picked up by `mapWritableState` (#2847) (0fa633e)

### Bug Fixes

- avoid npm bug when resolving optional deps (#2841) (1e45f33)

## 2.2.8 (2024-11-28)

### Features

- deprecate old defineStore (d1858e8)

### Bug Fixes

- avoid immediate computing with `storeToRefs` (67d3109), closes #2812
- **types:** unwrap refs in `mapWritableState` for setup stores (#2805) (ea14e53), closes #2804

## 2.2.7 (2024-11-27)

### Bug Fixes

- **devtools:** avoid running outside of browsers (eb5e6fd), closes #2843

## 2.2.6 (2024-11-03)

No code changes in this release

## 2.2.5 (2024-10-29)

### Bug Fixes

- keep no side effect comment when minifying (a31fb87)
- reference the store directly in storeToRefs to ensure correct reactivity after HMR (#2795) (254eec7)
- **types:** handle union types in generic parameter (#2794) (ecc7449), closes #2785
- up minimum peer dep of Vue (5404d3e), closes #2797

### Features

- **nuxt:** do not serialize skipHydrate properties (e645fc1)

## 2.2.4 (2024-10-01)

### Bug Fixes

- **types:** allow writable getters with storeToRefs (b464a1f), closes #2767

## 2.2.3 (2024-09-30)

### Bug Fixes

- **types:** allow writable getters (94f5a63), closes #2767
- **types:** Don't double UnwrapRef in setup stores (#2771) (5ad1765), closes #2770
- **types:** storeToRefs with nested refs (#2659) (623e5a0)

## 2.2.2 (2024-08-15)

### Features

- improve tree shaking on `defineStore` (#2740) (3069105)

## 2.2.1 (2024-08-06)

### Bug Fixes

- **types:** breaking type with auto imported components (#2730) (82ca41c)

# 2.2.0 (2024-07-26)

### Bug Fixes

- **types:** require unwrapped state in patch (c38fa0d)

### Features

- add `action` helper to consistently `$onAction` (a8526fc)
- **devtools:** expose selected store as global variable (#2692) (e0a7351)

## 2.1.8-beta.0 (2024-04-17)

### Bug Fixes

- **devtools:** Do not patch mocked actions (#2300) (069ffd1)
- support webpack minification (57914b5), closes #1143
- **types:** fix storeToRefs state return type (#2574) (#2604) (c8f727a)
- **types:** mapHelpers with getters types (#2571) (#2576) (ea5c974)
- **types:** use declare module vue (8a6ce86)

### Features

- disposePinia (bb8bf60), closes vuejs/pinia#2453

## 2.1.7 (2024-04-04)

### Bug Fixes

- support webpack minification (57914b5), closes #1143
- **types:** fix storeToRefs state return type (#2574) (#2604) (c8f727a)
- **types:** mapHelpers with getters types (#2571) (#2576) (ea5c974)
- **types:** use declare module vue (8a6ce86)

### Features

- disposePinia (bb8bf60), closes vuejs/pinia#2453

## 2.1.7 (2023-10-13)

### Bug Fixes

- **devtools:** correctly load initial states (9d49e30)

### Features

- **types:** SetupStoreDefinition (391f9ac)
- **warn:** improve getActivePinia warning (4640f09)

## 2.1.6 (2023-07-26)

### Bug Fixes

- **devtools:** preserve store reactivity (709ed3b)

## 2.1.5 (2023-07-26)

### Bug Fixes

- **devtools:** correctly load the state (beff091)
- **devtools:** wrong toast message (#2290) (dfc04d3)

## 2.1.4 (2023-06-14)

### Bug Fixes

- **devtools:** group setup store sync actions mutations (683efe1)

## 2.1.3 (2023-05-18)

### Bug Fixes

- **types:** revert declare module vue (3000161)

## 2.1.2 (2023-05-18)

- Force vue-demi version

## 2.1.1 (2023-05-17)

### Bug Fixes

- expect Vue 3.3 (b8fb165)

# 2.1.0 (2023-05-17)

 This **requires** Vue 3.3 or latest vue-demi (for Vue 2)

### Bug Fixes

- **types:** use declare module vue (b7f97dd)

### Features

- allow app injections in setup stores (6a71019), closes #1784
- **devtools:** allow resetting setup stores from inspector (971dcdb), closes #2189

### Reverts

- Revert "chore: tmp upgrade to beta" (2337130)

## 2.0.36 (2023-05-08)

### Features

- **dx:** throw an error if store id is missing (#2167) (b74eb4f)
- **warn:** improve warning message (73518b3)

## 2.0.35 (2023-04-20)

### Bug Fixes

- **types:** typescript 5.0 acceptHMRUpdate error (#2098) (#2152) (1469971)

### Features

- **types:** improve setActivePinia types (1650c6e)

## 2.0.34 (2023-04-07)

No changes in this release

## 2.0.33 (2023-03-06)

### Bug Fixes

- allow `$reset` to be overridden by plugins (#2054) (709e2b1)

## 2.0.32 (2023-02-21)

### Bug Fixes

- **types:** mapWritableState array (a7ad90d), closes #2014

## 2.0.31 (2023-02-20)

### Bug Fixes

- **types:** mapWritableState array (07eaf99), closes #2014

## 2.0.30 (2023-02-01)

### Bug Fixes

- avoid spread operator even in devtools code (d2a4def), closes #1885

## 2.0.29 (2023-01-15)

### Bug Fixes

- **types:** type storeToRefs getters as ComputedRef (#1898) (dcf7ef0)

## 2.0.28 (2022-12-09)

### Bug Fixes

- avoid missing injection not found warn in edge Vue 2 edge case (#1849) (78ec9a1), closes #1650

## 2.0.27 (2022-11-27)

- api docs changes

## 2.0.26 (2022-11-23)

### Bug Fixes

- **types:** support older ts versions (78fb214), closes #1818

## 2.0.25 (2022-11-21)

### Bug Fixes

- **types:** implemented a workaround to be TS 4.9.x compatible (#1818) (c42a54c)

## 2.0.24 (2022-11-17)

## 2.0.23 (2022-10-08)

### Bug Fixes

- **devtools:** init `_customProperties` for devtools (#1704) (8c1dfce)

## 2.0.22 (2022-09-06)

### Features

- **ssr:** handle Maps and Sets (f9843eb), closes #1608

## 2.0.21 (2022-08-26)

### Bug Fixes

- **build:** remove problematic browser export (6efa780), closes #1593

## 2.0.20 (2022-08-19)

- **build**: support vue 2 devtools flag

## 2.0.19 (2022-08-18)

### Bug Fixes

- **devtools:** use flag to include devtools (4e92c36)

## 2.0.18 (2022-08-10)

### Bug Fixes

- **ie:** completely skip devtools in dev for IE (ca73db9), closes #1440

## 2.0.17 (2022-07-25)

### Bug Fixes

- **devtools:** state formatting (b01f5c2), closes #1358
- setupStore getter types (#1430) (#1444) (6be93f2)

### Features

- **devtools:** allow resetting fromp pinia inspector (cee0e16)

## 2.0.16 (2022-07-12)

### Bug Fixes

- add missing require in exports (96c0dbc)

## 2.0.15 (2022-07-11)

### Features

- warn when a getter conflicts with the state (#1356) (667b81d)

## 2.0.14 (2022-05-05)

### Bug Fixes

- avoid multiple subscriptions with empty promises (6c17168), closes #1129
- correctly detect option stores (11b92fd), closes #1272
- **devtools:** remove in tests environment (4aeb0a5)

## 2.0.13 (2022-03-31)

### Bug Fixes

- avoid prototype pollution (e4858f9)
- **vue2:** use toRefs in storeToRefs (0f24ad2), closes #852

### Features

- update devtools-api (5334222)

## 2.0.12 (2022-03-14)

### Bug Fixes

- **devtools:** avoid error in getters (a64c19d), closes #1062
- **types:** exclude internal properties from store (f8f944f), closes #1013

### Features

- **devtools:** allow disable logs (43f690f)
- **devtools:** use api.now() (836ab86)
- up vue-devtools (e8e5f28)
- **warn:** avoid vue 2 bug storeToRefs() (f692fdf), closes #852

## 2.0.11 (2022-01-30)

### Bug Fixes

- **types:** custom Awaited for TS 4.x (7fcb62e), closes #1006

## 2.0.10 (2022-01-27)

### Bug Fixes

- check HTMLAnchorElement in saveAs for mini-program (#966) (#967) (85daefb)
- **subscriptions:** allow removing subscriptions inside them (#990) (465d222)
- **types:** custom Awaited for TS 4.x (7c51126), closes #957

## 2.0.9 (2021-12-24)

### Features

- **types:** support IDE features for store context (#924) (4733f49)

## 2.0.8 (2021-12-20)

### Bug Fixes

- **subscribe:** avoid $subscriptions with $patch (3bfe9e5), closes #908

## 2.0.7 (2021-12-20)

### Bug Fixes

- allow using multiple `$onAction`, **ignore returned value** (4dc1f1b), closes #893
- **subscribe:** direct mutation should not trigger detached subscriptions (a9ef6b6), closes #908

### Features

- update devtools-api (ca26686)

## 2.0.6 (2021-12-04)

### Bug Fixes

- downgrade peerdep requirement for ts (100a60d), closes #874

## 2.0.5 (2021-12-01)

### Bug Fixes

- accept reactive with storeToRefs (3a2a334), closes #799
- shouldHydrate if not in skipHydrateMap (#846) (bcc44bc)

## 2.0.4 (2021-11-19)

### Features

- **devtools:** allow resetting directly from devtools (44fa896)
- **devtools:** display all getters in pinia root (ce8f1e5)

## 2.0.3 (2021-11-10)

- Updated peer deps for composition api and vue devtools

## 2.0.2 (2021-11-03)

### Bug Fixes

- **types:** for devtools-api (d856d5d)
- **types:** remove dependency on Vue 3 only Plugin type (ee358a6)

## 2.0.1 (2021-11-03)

This release correctly removes the deprecated APIs as advertised in v2. The documentation contains a list of all the deprecations compared to v0.x.

### Bug Fixes

- use assign instead of spread for older browsers (51cf9b6)

### Features

- **warn:** improve getActivePinia warn (6a0a209)

# 2.0.0 (2021-10-27)

  

### Bug Fixes

- **devtools:** root store access #732 (90d2c35)
- **plugins:** ensure plugins are used only once (#745) (150fdfc)
- **ssr:** make skipHydrate compatible with @vue/composition-api (71448b0)

### BREAKING CHANGES

All deprecated API have been removed.

# 2.0.0-rc.15 (2021-10-25)

### Bug Fixes

- **types:** remove unused option hydrate for setup stores (37d07fb)

### Code Refactoring

- **ssr:** pass storeState instead of store to hydrate (c85edac)

### Features

- **ssr:** add skipHydrate to skip hydration on specific refs (55deedb)

### BREAKING CHANGES

- **ssr:** the `hydrate()` option for stores defined with the
  options api no longers passes the whole store instance. Instead, it
  passes the `storeState` so it can be directly modified. This is because
  it was currently necessary to hydrate the store by setting properties
  onto `store.$state`. This change makes it impossible to make the mistake
  anymore.

```diff
 defineStore('main', {
   state: () => ({
     customRef: useLocalStorage('key', 0)
   }),
-  hydrate(store) {
-    store.$state.customRef = useLocalStorage('key', 0)
+  hydrate(storeState) {
+    storeState.customRef = useLocalStorage('key', 0)
   }
 })
```

# 2.0.0-rc.14 (2021-10-19)

Readme update

# 2.0.0-rc.13 (2021-10-12)

- bump vue-devtools-api version

# 2.0.0-rc.12 (2021-10-07)

### Features

- proper check of computed requiring @vue/composition-api@1.2.3 (b099ef4)
- **warn:** log store id with class constructor warning (#702) (39eee6a)

# 2.0.0-rc.11 (2021-10-03)

### Bug Fixes

- **build:** expose mjs correctly (2e9fe33)
- export the module version in mjs (cffc313)
- **types:** correctly type global extensions (cdbdba5), closes #630
- **warn:** avoid toRefs warning for Vue 2 (c174fe1), closes #648

# 2.0.0-rc.10 (2021-09-30)

### Bug Fixes

- **ssr:** always call setActivePinia (83d7d2f), closes #665
- use assign to set $state (f3a732f), closes #682
- fix mjs, cjs versions for webpack based builds

### Features

- **warn:** incorrect state value #641 (#646) (6fd3883)

# 2.0.0-rc.9 (2021-09-12)

### Bug Fixes

- correct store in getters vue 2 (3d4080b)
- **vue2:** delay getters until stores are ready when cross using them (ed48b00)
- **vue2:** fix isComputed check for getters (307078b)

# 2.0.0-rc.8 (2021-09-06)

### Bug Fixes

- correctly set the store properties in Vue 2 (9e40309), closes #657

# 2.0.0-rc.7 (2021-09-03)

### Bug Fixes

- **ssr:** properly hydrate setup stores (4fbacfc)

### Features

- add typedoc (b98e23d)
- allow stores to be cross used (cda3658)
- deprecate PiniaPlugin in favor of PiniaVuePlugin (c0495c0)
- support TS 4.4 (#656) (39b2e15)

# 2.0.0-rc.6 (2021-08-19)

Fix missing types.

# 2.0.0-rc.5 (2021-08-19)

### Bug Fixes

- **ssr:** convert hydrated state to refs (3f186a2), closes #619

### Features

- destroy a store with $dispose (#597) (a563e6a)
- expose getActivePinia (8b8d0c1)
- **testing:** add testing package (fc05376)

# 2.0.0-rc.4 (2021-08-09)

If you are using Vue 2, make sure your `@vue/composition-api` version is at least `1.1.0`, which is currently under the npm dist tag `next`, which means it has to be installed with `npm install @vue/composition-api@next`.

### Bug Fixes

- **types:** unwrap computed in store getters (35d4f59), closes #602 #603

# 2.0.0-rc.3 (2021-08-05)

### Bug Fixes

- set initial state in prod (f8e3c83), closes #598

# 2.0.0-rc.2 (2021-08-04)

This version supports Vue 2! Here is an example using Vue 2 and Vite for an optimal DX. **Note this version requires Vue Devtools 6**, and more specifically, they don't work with the current `@vue/devtools-api` (`6.0.0-beta.15`) because they require this unreleased fix. To get all the goodness pinia has to offer **for Vue 2**, you will need to clone `vuejs/devtools`, run `yarn && yarn run build` and then _load an unpacked extension_ on a Chromium browser (after activating the developer mode in the extension panel). If you are using Vue 3, you can still use the Vue Devtools 6 regularly.

### Bug Fixes

- **devtools:** grouping of actions (3d760f1)
- **devtools:** reflect changes on HMR (aebc9a0)

### Features

- add support for Vue 2 (e1ea1c8)
- enable devtools with Vue 2 (08cdff5)

# 2.0.0-rc.1 (2021-07-30)

Posted <https://github.com/vuejs/pinia/issues/592> to help people installing or upgrading Pinia.

### Bug Fixes

- collect reactive effects ran in plugins (54cee00)
- **devtools:** update when custom properties change (7dcb71e)
- **store:** keep original refs with $reset (a7dadff), closes #593

# 2.0.0-rc.0 (2021-07-28)

## Required Vue version 

This release requires Vue 3.2.0, which is currently only available under the `beta` dist tag (`npm i vue@beta` or `yarn add vue@beta` + the corresponding packages like `@vue/compiler-sfc@beta`).

Follow the instructions at <https://github.com/vuejs/pinia/issues/592> if you need help updating your package versions.

It contains major improvements:

- Performance: Pinia now uses `effectScope()`, effectively reducing memory consumption and removing the drawbacks mentioned in the Plugin section about `useStore()` creating multiple store instances (still sharing the state).
- Devtools: Many improvements over the information displayed in devtools as well as a few bugfixes
- HMR (Hot Module Replacement): You can now modify your stores without reloading the page and losing the state, making development much easier. Until 3.2.0 (stable) is released, you can find an example in the playground. After that, you can read up to date instructions in the documentation.
- Setup syntax: You can now define stores with a function instead of options. This enables more complex patterns. See an example in the playground. Setup Stores are unable to group actions like Option Stores due to their very permissive syntax.
- Option syntax: we can now pass the `id` as the first parameter. This syntax is preferred over the object syntax to be consistent with the Setup syntax.

### Bug Fixes

- avoid modifying options argument (59ac9b9)
- **devtools:** avoid grouping patches and mutations with finished actions (18a87fe)
- **errors:** allow async errors to propagate (17ee4e8), closes #576
- **ssr:** delay getters read (2f3bd53)
- **types:** actual generic store (e4c541f)
- **types:** stricter types for mapState (f702356)

### Features

- allow actions to be destructured (859d094)
- **devtools:** display pinia without stores (ca59257)
- **devtools:** show hot update in timeline (3b9ed17)
- **types:** add StorState, StoreGetters, and StoreActions helpers (47c0610)

### BREAKING CHANGES

- **types:** The existing `Store<Id, S, G, A>` types was trying to be generic when no types were specified but failing at it. Now, `Store` without any type will default to an empty Store. This enables a stricter version of `defineStore` when any of state, getters, and actions are missing. If you were using `Store` as a type, you should now use `StoreGeneric` instead, which also replaces `GenericStore` (marked as deprecated).

```diff
-function takeAnyStore(store: Store) {}
+function takeAnyStore(store: StoreGeneric) {}
```

- **types** The existing `DefineStoreOptions` is no longer the one that should be extended to add custom options unless you only want them to be applied to Option Stores. Use `DefineStoreOptionsBase` instead.

# 2.0.0-beta.5 (2021-07-10)

### Bug Fixes

- **devtools:** avoid infinite loop when cross using stores (55c651d), closes #541
- **devtools:** avoid warning (399a930)
- **types:** forbid non existant access in getters and actions (2ee058e)

### Features

- mark testing as internal (18c8ed6)
- **testing:** add createTestingPinia (120ac9d)
- **testing:** allow stubing $patch (10bef8a)
- **testing:** allows faking an app (0d00a27)
- **testing:** bypass useStore(pinia) (5a52fb3)

### Performance Improvements

- use esm version of file-saver (49d1e38)

# 2.0.0-beta.3 (2021-06-18)

### Bug Fixes

- **patch:** avoid merging reactive objects (a6a75e8), closes #528

### Features

- **devtools:** display custom properties (fd901cd)

# 2.0.0-beta.2 (2021-06-03)

### Bug Fixes

- **devtools:** register stores (5fcca78)

# 2.0.0-beta.1 (2021-06-03)

### Bug Fixes

- **types:** fix extension for TS 4.3 (aff5c1e)

### Features

- remove deprecated APIs (239aec5)
- **devtools:** add root state (a75be78)
- **devtools:** import/export global state (b969f2a)
- **devtools:** load/save state (9b503d6)

# 2.0.0-alpha.19 (2021-05-20)

### Bug Fixes

- **devtools:** use older js (e35da3b)

# 2.0.0-alpha.18 (2021-05-17)

### Bug Fixes

- **types:** correct subtype Store (48523da), closes #500
- **types:** export types (befc132)

# 2.0.0-alpha.17 (2021-05-17)

### Bug Fixes

- **types:** forbid non existent keys on store (e747cba)
- **types:** patch should unwrap refs (b82eafc)
- **types:** unwrap refs passed to state (b2d3ac9), closes #491

### Features

- **devtools:** add more data to actions (e8f4b0e)
- **devtools:** allow editing state (0bbbd69)
- **devtools:** allow editing stores from components (b808fbc)
- **devtools:** display only relevant stores (58f0af6)
- **devtools:** group action and their changes (ecd993a)
- **types:** allow defining custom state properties (17fcbca)
- **types:** infer args and returned value for onAction (f3b3bcf)
- subscribe to actions with `$onAction` (c9ce6ea), closes #240

### Performance Improvements

- **devtools:** avoid multiple subscriptions (ea62f1d)

### BREAKING CHANGES

- The `type` property of the first parameter of `store.$subscribe()` has slightly changed. **In most scenarios this shouldn't affect you** as the possible values for `type` were including emojis (a bad decision...) and they are now using an enum without emojis. Emojis are used only in devtools to give a mental hint regarding the nature and origin of different events in the timeline.

- In `store.$subscribe()`'s first argument, the `storeName` property has been deprecated in favor of `storeId`.

# 2.0.0-alpha.16 (2021-05-04)

### Bug Fixes

- **devtools:** add all stores (2a8515c), closes #472

### Features

- **devtools:** display getters in components (810b969)

# 2.0.0-alpha.15 (2021-05-04)

### Bug Fixes

- **devtools:** fix devtools attach (017795a)

# 2.0.0-alpha.14 (2021-05-03)

### Features

- **devtools:** work with stores added before app.use (#444) (21f917f)
- **devtools:** add getters to devtools (c4bf761)
- mark getters as readonly (fcbeb95)
- **plugins:** allow chaining (3a49d34)
- **mapHelpers:** warn on array mapStores (d385bd9)
- pass options to context in plugins (c8ad19f)
- **types:** expose PiniaPluginContext (94d12e7)
- add plugin api wip (50bc807)
- **plugins:** allow void return (5ef7140)
- **plugins:** pass a context object to plugins instead of app (bcb4ec3)
- add plugin api wip (b5c928d)

### Performance Improvements

- **store:** reuse store instances when possible (14f5a5f)

### BREAKING CHANGES

- **store:** getters now receive the state as their first argument and it's properly typed so you can write getters with arrow functions:

  ```js
  defineStore({
    state: () => ({ n: 0 }),
    getters: {
      double: (state) => state.n * 2,
    },
  })
  ```

  To access other getters, you must still use the syntax that uses `this` **but it is now necessary to explicitly type the getter return type**. The same limitation exists in Vue for computed properties and it's a known limitation in TypeScript:

  ```ts
  defineStore({
    state: () => ({ n: 0 }),
    getters: {
      double: (state) => state.n * 2,
      // the `: number` is necessary when accessing `this` inside of
      // a getter
      doublePlusOne(state): number {
        return this.double + 1
      },
    },
  })
  ```

  For more information, refer to the updated documentation for getters.

- **plugins:** To improve the plugin api capabilities, `pinia.use()`
  now receives a context object instead of just `app`:

  ```js
  // replace
  pinia.use((app) => {})
  // with
  pinia.use(({ app }) => {})
  ```

  Check the new documentation for Plugins!

# 2.0.0-alpha.13 (2021-04-10)

### Bug Fixes

- **subscribe:** remove subscription when unmounted (10e1c30)

### Features

- **types:** fail on async patch (c254a8a)

# 2.0.0-alpha.12 (2021-04-09)

### Bug Fixes

- **store:** avoid multiple subscriptions call (71404cb), closes #429 #430

# 2.0.0-alpha.11 (2021-04-09)

### Bug Fixes

- **types:** enable autocomplete in object (b299ff0)

### Features

- mapWritableState (3218bdb)
- **mapState:** accept functions (e2f2b92)
- **mapStores:** allow custom suffix (c957fb9)
- **types:** allow extending mapStores suffix (f14c7b9)
- add mapActions (b5d27fb)
- add mapStores (d3d9327)
- mapState with array (0e05811)
- mapState with object (06805db)
- **types:** expose DefineStoreOptions (c727070)

# 2.0.0-alpha.10 (2021-04-01)

### Features

- **patch:** allow passing a function (8d545e4)
- **types:** generics on PiniaCustomProperties (36129cf)

# 2.0.0-alpha.9 (2021-03-31)

### Bug Fixes

- **types:** pass custom properties to stores (d26df6e)

# 2.0.0-alpha.8 (2021-03-29)

### Bug Fixes

- use assign instead of spread (b2bb5ba)
- **cjs:** ensure dev checks on cjs build (a255735)

### Features

- **devtools:** logo and titles (0963fd0)

# 2.0.0-alpha.7 (2021-01-21)

### Bug Fixes

- resilient _VUE_DEVTOOLS_TOAST_ (#334) (c0cacd2)

### Features

- enable calling `useStore()` in client (c949b80)
- store plugins (f027bf5)

# 2.0.0-alpha.6 (2020-12-31)

### Bug Fixes

- correct lifespan of stores (483335c), closes #255

### Features

- **types:** export used types (dc56fba), closes #315

### BREAKING CHANGES

- `setActiveReq()` has been renamed to
  `setActivePinia()`. And now receives the application's pinia as the
  first parameter instead of an arbitrary object (like a Node http
  request). **This affects particularly users doing SSR** but also
  enables them to write universal code.

# 2.0.0-alpha.5 (2020-10-09)

### Code Refactoring

- prefix store properties with \$ (#254) (751f286)

### BREAKING CHANGES

- all store properties (`id`, `state`, `patch`, `subscribe`, and `reset`) are now prefixed with `$` to allow properties defined with the same type and avoid types breaking. Tip: you can refactor your whole codebase with F2 (or right-click + Refactor) on each of the store's properties

# 2.0.0-alpha.4 (2020-09-29)

### Bug Fixes

- detach stores creation from currentInstance (dc31736)

# 2.0.0-alpha.3 (2020-09-28)

### Code Refactoring

- rename createStore to defineStore (a9ad160)

### Features

- deprecation message createStore (3054251)
- **ssr:** support ssr (59709e0)

### BREAKING CHANGES

- renamed `createStore` to `defineStore`. `createStore`
  will be marked as deprecated during the alpha releases and then be
  dropped.

# 2.0.0-alpha.2 (2020-09-25)

### Features

- add devtools support (849cb3f)

# 2.0.0-alpha.1 (2020-09-22)

### Features

- access the state and getters through `this` (#190) (6df18ef)
- merge all properties under this (d5eaac1)

### BREAKING CHANGES

- `state` properties no longer need to be accessed through `store.state`
- `getters` no longer receive parameters, access the store instance via `this`:
  directly call `this.myState` to read state and other getters. **Update 2021-04-02**: `getters` receive the state again as the first parameter
