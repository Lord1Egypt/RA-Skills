---
total: 69
---

# Docs Index

- [Getting Started](./getting-started.md): Install pinia with your favorite package manager:
- [Pinia](./index.md)
- [Introduction](./introduction.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ecf274c2f339c6860e36b"
mp-link="https://masteringpinia.com/lessons/the-what-and-why-of-st...

## cookbook (11)

- [Dealing with Composables](./cookbook/composables.md): Composables are functions that leverage Vue Composition API to encapsulate and reuse stateful logic. Whether you write your own, you use external l...
- [Composing Stores](./cookbook/composing-stores.md): Composing stores is about having stores that use each other, and this is supported in Pinia. There is one rule to follow:
- [HMR (Hot Module Replacement)](./cookbook/hot-module-replacement.md): Pinia supports Hot Module replacement so you can edit your stores and interact with them directly in your app without reloading the page, allowing ...
- [Cookbook](./cookbook/index.md)
- [Migrating from 0.0.7](./cookbook/migration-0-0-7.md): The versions after 0.0.7: 0.1.0, and 0.2.0, came with a few big breaking changes. This guide helps you migrate whether you use Vue 2 or Vue 3. The ...
- [Migrating from 0.x (v1) to v2](./cookbook/migration-v1-v2.md): Starting at version 2.0.0-rc.4, pinia supports both Vue 2 and Vue 3! This means, all new updates will be applied to this version 2 so both Vue 2 an...
- [Migrating from v2 to v3](./cookbook/migration-v2-v3.md): Pinia v3 is a boring major release with no new features. It drops deprecated APIs and updates major dependencies. It only supports Vue 3. If you ar...
- [Migrating from Vuex ≤4](./cookbook/migration-vuex.md): Although the structure of Vuex and Pinia stores is different, a lot of the logic can be reused. This guide serves to help you through the process a...
- [Usage without setup()](./cookbook/options-api.md): Pinia can be used even if you are not using the composition API (if you are using Vue <2.7, you still need to install the @vue/composition-api plug...
- [Testing stores](./cookbook/testing.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/65f9a9c10bfab01f414c25dc"
title="Watch a free video of Mastering Pinia about testing stores"
/>
- [VS Code Snippets](./cookbook/vscode-snippets.md): These are some snippets that I use in VS Code to make my life easier.

## core-concepts (6)

- [Actions](./core-concepts/actions.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-actions"
title="Learn all about actions in Pinia"
/>
- [Getters](./core-concepts/getters.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-getters"
title="Learn all about getters in Pinia"
/>
- [Defining a Store](./core-concepts/index.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ecff2e4c322668b0a17af"
mp-link="https://masteringpinia.com/lessons/quick-start-with-pinia...
- [Using a store outside of a component](./core-concepts/outside-component-usage.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ed1ec4c2f339c6860fd06"
mp-link="https://masteringpinia.com/lessons/how-does-usestore-work...
- [Plugins](./core-concepts/plugins.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/What-is-a-pinia-plugin"
title="Learn all about Pinia plugins"
/>
- [State](./core-concepts/state.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-state"
title="Learn all about state in Pinia"
/>

## ssr (2)

- [Server Side Rendering (SSR)](./ssr/index.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/ssr-friendly-state"
title="Learn about SSR best practices"
/>
- [Nuxt](./ssr/nuxt.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/ssr-friendly-state"
title="Learn about SSR best practices"
/>

## zh/api/enums (1)

- [Enumeration: MutationType %{#enumeration-mutationtype}%](./zh/api/enums/pinia.MutationType.md): API 文档 / pinia / MutationType

## zh/api (1)

- [API 文档 %{#api-documentation}%](./zh/api/index.md): API 文档

## zh/api/interfaces (21)

- [接口：ModuleOptions](./zh/api/interfaces/pinia_nuxt.ModuleOptions.md): API 文档 / @pinia/nuxt / ModuleOptions
- [接口：TestingOptions %{#interface-testingoptions}%](./zh/api/interfaces/pinia_testing.TestingOptions.md): API 文档 / @pinia/testing / TestingOptions
- [接口：TestingPinia %{#interface-testingpinia}%](./zh/api/interfaces/pinia_testing.TestingPinia.md): API 文档 / @pinia/testing / TestingPinia
- [接口：_StoreOnActionListenerContext<Store, ActionName, A> %{#interface-storeonactionlistenercontext-store-actionname-a}%](./zh/api/interfaces/pinia._StoreOnActionListenerContext.md): API 文档 / pinia / StoreOnActionListenerContext
- [接口：_StoreWithState<Id, S, G, A> %{#interface-storewithstate-id-s-g-a}%](./zh/api/interfaces/pinia._StoreWithState.md): API 文档 / pinia / StoreWithState
- [接口：_SubscriptionCallbackMutationBase %{#interface-subscriptioncallbackmutationbase}%](./zh/api/interfaces/pinia._SubscriptionCallbackMutationBase.md): API 文档 / pinia / SubscriptionCallbackMutationBase
- [接口：DefineSetupStoreOptions<Id, S, G, A> %{#interface-definesetupstoreoptions-id-s-g-a}%](./zh/api/interfaces/pinia.DefineSetupStoreOptions.md): API 文档 / pinia / DefineSetupStoreOptions
- [接口：DefineStoreOptions<Id, S, G, A> %{#interface-definestoreoptions-id-s-g-a}%](./zh/api/interfaces/pinia.DefineStoreOptions.md): API 文档 / pinia / DefineStoreOptions
- [接口：DefineStoreOptionsBase<S, Store> %{#interface-definestoreoptionsbase-s-store}%](./zh/api/interfaces/pinia.DefineStoreOptionsBase.md): API 文档 / pinia / DefineStoreOptionsBase
- [接口：DefineStoreOptionsInPlugin<Id, S, G, A> %{#interface-definestoreoptionsinplugin-id-s-g-a}%](./zh/api/interfaces/pinia.DefineStoreOptionsInPlugin.md): API 文档 / pinia / DefineStoreOptionsInPlugin
- [接口：MapStoresCustomization %{#interface-mapstorescustomization}%](./zh/api/interfaces/pinia.MapStoresCustomization.md): API 文档 / pinia / MapStoresCustomization
- [接口：Pinia %{#interface-pinia}%](./zh/api/interfaces/pinia.Pinia.md): API 文档 / pinia / Pinia
- [接口：PiniaCustomProperties<Id, S, G, A> %{#interface-piniacustomproperties-id-s-g-a}%](./zh/api/interfaces/pinia.PiniaCustomProperties.md): API 文档 / pinia / PiniaCustomProperties
- [接口：PiniaCustomStateProperties<S> %{#interface-piniacustomstateproperties-s}%](./zh/api/interfaces/pinia.PiniaCustomStateProperties.md): API 文档 / pinia / PiniaCustomStateProperties
- [接口：PiniaPlugin %{#interface-piniaplugin}%](./zh/api/interfaces/pinia.PiniaPlugin.md): API 文档 / pinia / PiniaPlugin
- [接口：PiniaPluginContext<Id, S, G, A> %{#interface-piniaplugincontext-id-s-g-a}%](./zh/api/interfaces/pinia.PiniaPluginContext.md): API 文档 / pinia / PiniaPluginContext
- [接口：StoreDefinition<Id, S, G, A> %{#interface-storedefinition-id-s-g-a}%](./zh/api/interfaces/pinia.StoreDefinition.md): API 文档 / pinia / StoreDefinition
- [接口：StoreProperties<Id> %{#interface-storeproperties-id}%](./zh/api/interfaces/pinia.StoreProperties.md): API 文档 / pinia / StoreProperties
- [接口：SubscriptionCallbackMutationDirect %{#interface-subscriptioncallbackmutationdirect}%](./zh/api/interfaces/pinia.SubscriptionCallbackMutationDirect.md): API 文档 / pinia / SubscriptionCallbackMutationDirect
- [接口：SubscriptionCallbackMutationPatchFunction %{#interface-subscriptioncallbackmutationpatchfunction}%](./zh/api/interfaces/pinia.SubscriptionCallbackMutationPatchFunction.md): API 文档 / pinia / SubscriptionCallbackMutationPatchFunction
- [接口：SubscriptionCallbackMutationPatchObject<S> %{#interface-subscriptioncallbackmutationpatchobject-s}%](./zh/api/interfaces/pinia.SubscriptionCallbackMutationPatchObject.md): API 文档 / pinia / SubscriptionCallbackMutationPatchObject

## zh/api/modules (3)

- [模块: @pinia/nuxt %{#module-pinia-nuxt}%](./zh/api/modules/pinia_nuxt.md): API 文档 / @pinia/nuxt
- [模块：@pinia/testing %{#module-pinia-testing}%](./zh/api/modules/pinia_testing.md): API 文档 / @pinia/testing
- [模块：pinia %{#module-pinia}%](./zh/api/modules/pinia.md): API 文档 / pinia

## zh/cookbook (10)

- [处理组合式函数 %{#dealing-with-composables}%](./zh/cookbook/composables.md): 组合式函数是利用 Vue 组合式 API 来封装和复用有状态逻辑的函数。无论你是自己写，还是使用外部库，或者两者都有，你都可以在 pinia store 中充分发挥组合式函数的力量。
- [组合式 Store %{#composing-stores}%](./zh/cookbook/composing-stores.md): 组合式 store 是可以相互使用，Pinia 当然也支持它。但有一个规则需要遵循：
- [HMR (Hot Module Replacement) %{#hmr-hot-module-replacement}%](./zh/cookbook/hot-module-replacement.md): Pinia 支持热更新，所以你可以编辑你的 store，并直接在你的应用中与它们互动，而不需要重新加载页面，允许你保持当前的 state、并添加甚至删除 state、action 和 getter。
- [手册 %{#cookbook}%](./zh/cookbook/index.md)
- [Migrating from 0.0.7 %{#migrating-from-0-0-7}%](./zh/cookbook/migration-0-0-7.md): The versions after 0.0.7: 0.1.0, and 0.2.0, came with a few big breaking changes. This guide helps you migrate whether you use Vue 2 or Vue 3. The ...
- [从 0.x (v1) 迁移至 v2 %{#migrating-from-0-x-v1-to-v2}%](./zh/cookbook/migration-v1-v2.md): 从 2.0.0-rc.4 版本开始，pinia 同时支持 Vue 2 和 Vue 3！这意味着，v2 版本的所有更新，将会让 Vue 2 和 Vue 3 的用户都受益。如果你使用的是 Vue 3，这对你来说没有任何改变，因为你已经在使用 rc 版本，你可以查看发布日志来了解所有更新的详细解释。...
- [从 Vuex ≤4 迁移 %{#migrating-from-vuex-≤4}%](./zh/cookbook/migration-vuex.md): 虽然 Vuex 和 Pinia store 的结构不同，但很多逻辑都可以复用。本指南的作用是帮助你完成迁移，并指出一些可能出现的常见问题。
- [不使用 setup() 的用法 %{#usage-without-setup}%](./zh/cookbook/options-api.md): 即使你没有使用组合式 API，也可以使用 Pinia(如果你使用 Vue 2，你仍然需要安装 @vue/composition-api 插件)。虽然我们推荐你试着学习一下组合式 API，但对你和你的团队来说目前可能还不是时候，你可能正在迁移一个应用，或者有其他原因。你可以试试下面几个函数：
- [store 测试 %{#testing-stores}%](./zh/cookbook/testing.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/65f9a9c10bfab01f414c25dc"
title="Watch a free video of Mastering Pinia about testing stores"
/>
- [VS Code 代码片段](./zh/cookbook/vscode-snippets.md): 有一些代码片段可以让你在 VS Code 中更轻松地使用 Pinia。

## zh/core-concepts (6)

- [Action %{#actions}%](./zh/core-concepts/actions.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-actions"
title="Learn all about actions in Pinia"
/>
- [Getter %{#getters}%](./zh/core-concepts/getters.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-getters"
title="Learn all about getters in Pinia"
/>
- [定义 Store %{#defining-a-store}%](./zh/core-concepts/index.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ecff2e4c322668b0a17af"
mp-link="https://masteringpinia.com/lessons/quick-start-with-pinia...
- [在组件外使用 store %{#using-a-store-outside-of-a-component}%](./zh/core-concepts/outside-component-usage.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ed1ec4c2f339c6860fd06"
mp-link="https://masteringpinia.com/lessons/how-does-usestore-work...
- [插件 %{#plugins}%](./zh/core-concepts/plugins.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/What-is-a-pinia-plugin"
title="Learn all about Pinia plugins"
/>
- [State %{#state}%](./zh/core-concepts/state.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/the-3-pillars-of-pinia-state"
title="Learn all about state in Pinia"
/>

## zh (3)

- [开始](./zh/getting-started.md): 用你喜欢的包管理器安装 pinia：
- [Pinia](./zh/index.md)
- [简介 %{#introduction}%](./zh/introduction.md): <MasteringPiniaLink
href="https://play.gumlet.io/embed/651ecf274c2f339c6860e36b"
mp-link="https://masteringpinia.com/lessons/the-what-and-why-of-st...

## zh/ssr (2)

- [服务端渲染 (SSR) %{#server-side-rendering-ssr}%](./zh/ssr/index.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/ssr-friendly-state"
title="Learn about SSR best practices"
/>
- [Nuxt %{#nuxt}%](./zh/ssr/nuxt.md): <MasteringPiniaLink
href="https://masteringpinia.com/lessons/ssr-friendly-state"
title="Learn about SSR best practices"
/>
