---
name: advanced-renderjs
description: uni-app renderjs 简介、视图层 JS、App 端操作 DOM、echarts 等
---

# renderjs 简介

renderjs 是运行在**视图层**的 JS，**仅支持 App-vue 与 H5**；小程序不支持（微信可用 wxs 替代）。主要作用：1）降低逻辑层与视图层通信损耗，提升交互性能；2）在视图层操作 DOM，运行依赖 window/document 的库（如 echarts、three.js）。

## 使用方式

在 `<script>` 上增加 **module** 与 **lang="renderjs"**，例如：

```html
<script module="test" lang="renderjs">
  export default {
    mounted() { /* 可操作 DOM */ },
    methods: { /* 视图层方法 */ }
  }
</script>
```

逻辑层与视图层通过 **change:propName** 等机制传数据；视图层可用 **this.$ownerInstance.callMethod()** 调用逻辑层 methods（仅选项式 methods）。数据建议一次性从逻辑层传到视图层，避免频繁通信导致卡顿。

## 注意事项

- 仅支持**内联**使用，不要直接引用大型类库，推荐动态创建 script 引用。
- 可使用 Vue 组件生命周期（如 mounted），**不可**使用 App、Page 生命周期。
- **App 端**：可访问 DOM/BOM，**不可**直接访问逻辑层数据，**不可**使用 uni 接口（如 uni.request）。资源路径相对项目根目录。
- **H5 端**：逻辑层与视图层同环境，相当于 mixin，可直接访问逻辑层数据。
- Vue3 项目不支持 `<script setup>` 的 renderjs 写法。

## 典型场景

App 端使用 **echarts 完整版**、**three.js**、**f2** 等需操作 canvas/DOM 的库时，在视图层用 renderjs 运行，避免逻辑层与视图层频繁通信。示例见插件市场「renderjs 版 echart」。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/renderjs
-->
