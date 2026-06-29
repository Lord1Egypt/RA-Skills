---
name: "line"
description: "Line 线条 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Line 线条 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/line.html"
---

---

## [#](#line-线条) Line 线条 [![](https://www.uviewui.com/common/to_api.png)](#api)

此组件一般用于显示一根线条，用于分隔内容块，有横向和竖向两种模式，且能设置0.5px线条，使用也很简单。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

组件内部有预置的参数，直接使用即可，有如下几个参数需要了解：

-   `color`为线条的颜色
-   `direction`为线条的方向，默认为横向
-   `length`参数需要特别留意，它需要带上单位，比如设置为"50%"，"500rpx"等，在线条为横向时，表现为线条的长度；在线条为竖向时，表现为线条的高度。

```
<template>
	/* 基础使用 */
	<u-line></u-line>

	/* 自定义颜色 */
	<u-line color="#2979ff"></u-line>

	/* 自定义线条方向 */
	<u-line direction="col"></u-line>

	/* 自定义线条长度 */
	<u-line length="50%"></u-line>
</template>
```

### [#](#是否虚线) 是否虚线

-   `dashed`控制线条是否虚线：

```
<template>
	<u-line dashed></u-line>
</template>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/line/line.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/line/line.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| color | 线条的颜色 | String | #d6d7d9 | \- |
| length | 长度，竖向时表现为高度，横向时表现为长度，可以为百分比，带rpx单位的值等 | String | Number | 100% | \- |
| direction | 线条的方向，`row`\-横向，`col`\-竖向 | String | row | col |
| hairline | 是否显示细边框 | Boolean | true | false |
| margin | 线条与上下左右元素的间距，字符串形式，如"30rpx"、"20rpx 30rpx"，默认单位px | String | Number | 0 | \- |
| dashed | 是否虚线，false-实线，true-虚线 | Boolean | false | true |

← [ScrollList 横向滚动列表](https://www.uviewui.com/components/scrollList.html) [Overlay 遮罩层](https://www.uviewui.com/components/overlay.html) →


