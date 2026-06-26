---
name: best-practices-cross-platform
description: uni-app 跨端注意事项与常见差异（CSS、API、标签、数据绑定）
---

# 跨端注意

跨端应**按 uni 的写法和标签**开发，由框架编译到各端，而不是把 Web 习惯照搬到全平台。

## 标签与样式

- **标签**：使用 view、text、image、navigator 等，不要用 div、span、a、img。非 H5 端编译器会把部分 HTML 标签转成小程序标签，但建议直接写 uni 标签。
- **选择器**：非 H5 端不支持 `*`；页面根用 `page` 替代 `body`。
- **样式隔离**：非 H5 端默认未启用 scoped，组件/页面样式可能相互影响，需要时在 style 上加 `scoped`。
- **单位**：推荐 rpx；布局推荐 flex。nvue/快应用仅支持 flex 布局。
- **原生组件层级**：video、map、canvas 等原生组件层级高于前端组件，遮挡需用 **cover-view** / cover-image。

## JS 与 API

- **非 H5 端**无 window、document、cookie、localStorage、XMLHttpRequest 等浏览器对象；不可用 jQuery 等依赖这些的库。用 `uni.*` API 替代；App 端若要用操作 DOM 的库，可通过 **renderjs**。
- **data**：必须为**函数**返回对象（`data() { return { ... } }`），否则页面关闭后数据不销毁，再次打开会显示旧数据。
- **数据绑定**：按 Vue 2 写法，不支持小程序写法（如 `id="item-{{id}}"`），需改为 `:id="'item-' + id"`。
- **v-html**：H5 与 App-vue 支持，**小程序不支持**。

## 工程与配置

- 页面放 `pages` 下，在 pages.json 注册；自定义组件放 `components`；静态资源放 `static`。
- 小程序请求的域名需在对应平台配置白名单。
- App 端老机型 WebView 可能不支持较新 CSS，可考虑 x5 内核或放弃低版本；小程序无此问题。

## 常见异常场景

- **H5 正常、App 异常**：多为 CSS 兼容或使用了浏览器专有 API；检查是否用 cover-view 盖原生组件。
- **H5 正常、小程序异常**：v-html、未配置域名白名单、或用了小程序不支持的 API。
- **小程序/App 正常、H5 异常**：可能用了 plus、Native.js、subNVue、原生插件等仅 App 能力，或小程序专有能力（如云开发建议用跨端 uniCloud）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/matter
-->
