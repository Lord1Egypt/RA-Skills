---
name: features-component-overview
description: uni-app 组件入门、基础组件分类、easycom、扩展组件
---

# 组件概述

组件是视图层的基本单元，带标签、属性、事件。**标签与属性名小写，单词用连字符 `-` 连接**。事件用 Vue 的 `@` 绑定（如 `@change="handler"`），不要用小程序式的 bindchange。

## 公共属性

所有组件支持：`id`、`ref`、`class`、`style`、`hidden`、`data-*`、`@*`（事件）。  
布尔属性只要写上即为 true，未写为 false；属性值为变量时加冒号 `:prop="var"`。

## 基础组件

内置，无需导入与注册，直接使用。与小程序规范接近，分类包括：

- **视图容器**：view、scroll-view、swiper、movable-area、movable-view、cover-view、cover-image
- **基础内容**：icon、text、rich-text、progress
- **表单**：button、checkbox、editor、form、input、label、picker、picker-view、radio、slider、switch、textarea
- **导航**：navigator
- **媒体**：audio、camera、image、video、live-player、live-pusher
- **地图**：map
- **画布**：canvas
- **其它**：web-view、ad、page-meta、navigation-bar 等

不要用 HTML 标签（div/span/a/img），非 H5 端会被编译成 view/text/navigator/image，建议直接写 uni 组件名。

## easycom（推荐）

目录为 `components/组件名/组件名.vue`（或 uni_modules）且组件名与目录名一致时，**无需 import 与注册**，模板中可直接使用。  
可在 pages.json 的 `easycom.custom` 中自定义规则。打包时会按需剔除未使用组件。

## 扩展组件

非基础组件均为扩展组件，需安装并引用（或符合 easycom 目录）。  
若不符合 easycom，需在页面中 import 并在 components 中注册。  
uni-ui、插件市场组件多支持 easycom；原生组件、nvue、datacom、uniCloud 等有单独说明，见官方「组件」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/component/README
- https://uniapp.dcloud.net.cn/component/vue-component
-->
