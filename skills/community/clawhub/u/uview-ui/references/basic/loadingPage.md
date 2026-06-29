---
name: "loadingPage"
description: "LoadingPage 加载页 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs LoadingPage 加载页 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/loadingPage.html"
---

---

## [#](#loadingpage-加载页) LoadingPage 加载页 [![](https://www.uviewui.com/common/to_api.png)](#api)

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

```
<template>
	<view>
		<u-loading-page></u-loading-page>
	</view>
</template>
```

### [#](#显示或隐藏) 显示或隐藏

`loading`可以指定是否显示加载页

```
<u-loading-page :loading="true"></u-loading-page>
```

### [#](#文字内容) 文字内容

`loading-text`可以指定提示内容

```
<u-loading-page loading-text="loading..."></u-loading-page>
```

### [#](#动画模式) 动画模式

`loading-mode`可以指定加载动画的模式, 默认为`circle`

```
<u-loading-page loading-mode="spinner"></u-loading-page>
<u-loading-page loading-mode="semicircle"></u-loading-page>
```

### [#](#动画图片) 动画图片

`image`可以指定文字上方用于替换loading动画的图片

```
<u-loading-page image="/static/logo.png"></u-loading-page>
```

### [#](#文字颜色) 文字颜色

`color`可以指定文字颜色

```
<u-loading-page color="#666"></u-loading-page>
```

### [#](#文字大小) 文字大小

`font-size`可以指定文字大小

```
<u-loading-page font-size="24"></u-loading-page>
```

### [#](#图标大小) 图标大小 2.0.32

`icon-size`可以指定图标大小

```
<u-loading-page icon-size="36"></u-loading-page>
```

### [#](#背景颜色) 背景颜色

`bg-color`可以指定背景颜色

```
<u-loading-page bg-color="#e8e8e8"></u-loading-page>
```

### [#](#图标颜色) 图标颜色

`loading-color`可以指定加载中图标的颜色

```
<u-loading-page loading-color="#000000"></u-loading-page>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/loading-page/loading-page.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/loading-page/loading-page.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| loadingText | 提示内容 | String | Number | 正在加载 | \- |
| image | 文字上方用于替换loading动画的图片 | String | \- | \- |
| loadingMode | 加载动画的模式 | String | circle | spinner \\ semicircle |
| loading | 是否加载中 | boolean | false | true |
| bgColor | 背景颜色 | String | #ffffff | \- |
| color | 文字颜色 | String | #C8C8C8 | \- |
| fontSize | 文字大小 | String | Number | 19 | \- |
| iconSize 2.0.32 | 图标大小 | String | Number | 28 | \- |
| loadingColor | 加载中图标的颜色 | String | #C8C8C8 | \- |

← [LoadingIcon 加载动画](https://www.uviewui.com/components/loadingIcon.html) [Form 表单](https://www.uviewui.com/components/form.html) →


