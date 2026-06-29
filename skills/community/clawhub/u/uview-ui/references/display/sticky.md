---
name: "sticky"
description: "Sticky 吸顶 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Sticky 吸顶 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/sticky.html"
---

---

## [#](#sticky-吸顶) Sticky 吸顶 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件与CSS中`position: sticky`属性实现的效果一致，当组件达到预设的到顶部距离时， 就会固定在指定位置，组件位置大于预设的顶部距离时，会重新按照正常的布局排列。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

说明

本组件内部通过多种手段嗅探当前运行环境是否支持`css sticky`，在`H5`，`APP-VUE`，`NVUE`，`MP-WEIIXN`，`安卓` 等环境可以进行准确判断，如果支持则使用`CSS`方案，否则使用降级的`JS`方案。

### [#](#基本使用) 基本使用

由于`css sticky`的特殊性，建议您将此组件放置在页面外层元素中，否则可能会导致`sticky`失效，以下为[MDN对sticky的解释 (opens new window)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position)：

-   元素根据正常文档流进行定位，然后相对它的最近滚动祖先（nearest scrolling ancestor）和 containing block (最近块级祖先 nearest block-level ancestor)，包括table-related元素，基于top, right, bottom, 和 left的值进行偏移。偏移值不会影响任何其他元素的位置。

```
<template>
	<view class="container">

		<u-sticky>......</u-sticky>
		<view class="container__inner">

			<u-sticky>......</u-sticky>
		</view>
	</view>
</template>
```

### [#](#吸顶距离) 吸顶距离

通过`offset-top`参数设置组件在吸顶时与顶部的距离

```
<u-sticky offset-top="200">
	<text>塞下秋来风景异，衡阳雁去无留意</text>
</u-sticky>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/sticky/sticky.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/sticky/sticky.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| offsetTop | 吸顶时与顶部的距离，单位rpx | String | Number | 0 | \- |
| customNavHeight | 导航栏高度，自定义导航栏时，需要传入此值 | String | Number | 0 | \- |
| disabled | 是否禁用吸顶功能 | Boolean | false | true |
| bgColor | 组件背景颜色 | String | #ffffff | \- |
| zIndex | 吸顶时的`z-index`值，`NVUE`无效 | String | Number | \- | \- |
| index | 自定义标识，用于区分是哪一个组件 | String | Number | \- | \- |

← [Skeleton 骨架屏](https://www.uviewui.com/components/skeleton.html) [Divider 分割线](https://www.uviewui.com/components/divider.html) →


