---
name: features-vue-components
description: uni-app 自定义 Vue 组件、注册、slot 插槽、ref、父子通信
---

# 自定义 Vue 组件

组件放在 **components** 目录，符合 `components/组件名/组件名.vue` 时可用 **easycom** 免注册。否则需在页面中 import 并在 components 中注册。组件名可用 kebab-case 或 PascalCase；data 必须为函数。

## 插槽 slot

- 默认插槽：子组件内 `<slot></slot>`，父组件在子组件标签内写内容即可填入。
- 具名插槽：子组件 `<slot name="header">`，父组件 `<template v-slot:header>` 或 `#header`。
- 作用域插槽：子组件 `<slot :item="item">`，父组件通过 `v-slot="scope"` 使用 scope.item。详见 Vue 文档「插槽」。

## ref 与子组件实例

在子组件上写 **ref="xxx"**，在 script 中通过 **this.$refs.xxx**（选项式）或 **ref + 同名变量**（组合式）拿到子组件实例，可调用子组件方法或访问数据。子组件需通过 **defineExpose**（Vue3/uvue）或 **export default { expose: [...] }** 暴露方法或属性，否则 ref 拿到的是内部实例，暴露内容依框架版本而定。

## 父子通信

- **父 → 子**：props。子组件 props 中声明，父组件通过属性传入。
- **子 → 父**：子组件 **$emit('事件名', 参数)**，父组件 **@事件名="handler"** 接收。
- **跨级/全局**：provide/inject，或 uni.$emit / uni.$on（见「页面栈与全局通讯」）。

## 与小程序自定义组件

uni-app 主要使用 **Vue 组件**；也支持小程序自定义组件（wxcomponents 等），需按小程序规范，详见「小程序自定义组件」文档。推荐以 Vue 组件 + easycom 为主。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/vue-components
- https://uniapp.dcloud.net.cn/component/vue-component
-->
