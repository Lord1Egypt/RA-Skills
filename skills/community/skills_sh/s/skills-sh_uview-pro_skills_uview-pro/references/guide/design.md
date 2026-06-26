---
name: "design"
description: ":::tip 说明. Invoke when user needs guidance on design."
url: "https://uviewpro.cn/zh/guide/design.html"
triggers: ["design","设计"]
---

# 设计理念

:::tip 说明
`uView Pro` 的设计理念来源于 `uView 1.x` 和实际项目，由于之前使用 uniapp 开发的项目大多都是 uniapp + Vue2 + uView 1.x，想开始新项目使用 Vue3 时，却没有找到顺手的 UI 组件库，所以萌生了重构 `uView UI 1.x` 的想法，在 Vue3 的基础上重构了 `uView 1.8.8`，这才诞生了 `uView Pro`。

`uView Pro` 的设计理念是：保持 `uView UI 1.x` 简洁的设计理念，使用 Vue3 的语法全面重构每一个组件，并保持现有 API，可以让你无缝切换！
:::

## 导航栏

uniapp 可以通过配置`pages.json`生成原生元素的导航栏，简要说明如下：

- 优点是可以快速渲染，配置便捷，还可以带入一部分原生内容(针对 App Store)
- 缺点是配置不够灵活，遮罩无法覆盖导航栏等

建议：

- 如果开发者使用 nuve，可以直接自定义导航栏，无需使用 uniapp 自带的
- 如果是普通的 vue 页面，直接使用 uniapp 自带导航栏。如果自带的不能满足，条件允许就用`subNVue`绘制，否则就用普通元素绘制

说明：uni 官方有关于导航栏的详细说明，请参见[自定义导航栏](https://uniapp.dcloud.io/collocation/pages?id=customnav)

## 关于 nvue

nvue 源自于 uniapp 引入的阿里 weex 开源原生渲染引擎，单 weex 来说，是不推荐使用的，因为它没有周边的生态和第三方的功能。  
uniapp 引入 weex 之后，一直在整合，但也没有对 weex 进行定制开发，在 APP 端某些需要性能相关的可以使用 nvue，以下是我们对 nvue 的一些见解：

- nvue 具有媲美`react native`的性能，uniapp 一直在打通 vue 和 nvue 的壁垒
- nvue 页面中还不能像写 vue 一样便利，比如对样式的限制，api 还不能和 vue 完全互通等

建议：uniapp 一直在强化 vue，重心不在 nvue，如果不是特别复杂的应用，可以直接使用 vue 开发，应用的首页(V3 版本)使用`nvue`，渲染的速度会有显著的提升，
如果有需要进一步了解，请参见[nvue 开发与 vue 开发的常见区别](https://uniapp.dcloud.io/use-weex?id=nvue开发与vue开发的常见区别)

## 关于单位

我们在 web 中，常用的是`px`，`rem`等单位，`rem`在 uniapp 中不推荐使用，我们分别做如下阐述：

web 中：
可以使用`px`，它属于静态单位，它的最终呈现尺寸不会和屏幕尺寸有关系

uniapp 中(vue 和 nvue)：  
`px`属于静态单位，uni 中还有`upx`和`rpx`单位，`upx`为 uniapp 成立之初的动态单位，后来各家小程序跟随微信小程序，都使用
`rpx`单位，使它成为了既定的事实标准，uniapp 也就提倡并官宣使用`rpx`单位，但是`upx`也一样能使用，和`rpx`效果相同。  
另外：uniapp，vh 和 vw 也完全可以使用的，一般我们需要让某个元素高度铺满整个屏幕时，可以设置高度为`100vh`。

weex 中：
这里说的是阿里的 weex，而不是 uniapp 改良后的 nvue 版本中的 weex，它的`px`单位和 uniapp 中的`rpx`或者`upx`是一样的，也属于
动态单位，它自创了个`wx`单位，和 web 中的`px`一样，属于静态单位。  
说明：uniapp 的 nvue 版本中，虽然也是引入 weex，但是改良后，没有了`wx`，`nvue`的`rpx`(`upx`)与`px`和 uniapp 的 vue 版本单位效果一致。

建议：开发中，只需谨记两个单位，`px`和`rpx`，一般情况下，我们推荐字体和宽高等，都使用`rpx`单位，如果真的需要固定尺寸，就是用`px`。
如果关于各单位和他们的由来历史，还需要进一步了解，可以参见[尺寸单位](https://uniapp.dcloud.io/frame?id=尺寸单位)

## 布局

为兼容多端运行，我们建议开发者使用`flex`，不要使用`float`布局。移动端使用`flex`是没有顾虑的，而`flex`布局，可以达到事半功倍的效果。  
如果不熟悉`flex`，可以参考[阮一峰的 flex 教程](http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)
