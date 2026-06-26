---
name: features-vue-basics
description: uni-app 中 Vue 基础、单文件结构、数据绑定、事件、列表与条件渲染
---

# Vue 基础（uni-app 中）

uni-app 使用 Vue 单文件组件（SFC）：`<template>`、`<script>`、`<style>` 三个一级节点。Vue2 下 template 须有且仅有一个根节点（通常为 `<view>`）；Vue3 可多根。

## 数据绑定

- 文本：`{{ message }}`。
- 属性：`:id="dynamicId"` 或 `v-bind:attr="expr"`。布尔属性写上即为 true，不写为 false。
- 数据必须在 `data()` 函数中返回对象，不能直接 `data: { }`，否则页面关闭后数据不销毁。

## 事件

- 绑定：`@click="handler"` 或 `@click="handler(arg)"`。组件事件统一用 Vue 的 `@`，勿用小程序 bind 写法。
- 事件对象：无参时第一个参数为 event；带参时需显式传 `$event`。

## 列表渲染

- `v-for="(item, index) in list"`，建议加 `:key="index"` 或唯一 id。key 勿用 index 在动态增删时易出问题，尽量用业务唯一值。
- `<block>` 或 `<template>` 可作为无实际节点的包装，仅用于 v-if/v-for。

## 条件渲染

- `v-if` / `v-else` / `v-else-if`：条件不满足不渲染。
- `v-show`：切换 display，组件始终渲染。

## 其它

- 外部 js 用 `import` 或 `require` 引入；样式可用 `@import` 或预处理器。
- 小程序端不支持 `v-html`；数据绑定须用 Vue 写法，不支持 `id="item-{{id}}"`，需改为 `:id="'item-' + id"`。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/vue-basics
-->
