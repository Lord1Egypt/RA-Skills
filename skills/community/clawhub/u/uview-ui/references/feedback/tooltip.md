---
name: "tooltip"
description: "Tooltip 长按提示 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Tooltip 长按提示 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/tooltip.html"
---

---

## [#](#tooltip-长按提示) Tooltip 长按提示 [![](https://www.uviewui.com/common/to_api.png)](#api)

Tooltip组件主要用于长按操作，类似微信的长按气泡

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用.

说明

由于安卓`nvue`下，`overflow`属性不支持`visible`值，故此组件暂不支持安卓`nvue`环境。

```
<template>
    <u-tooltip text="复制" overlay></u-tooltip>
</template>
```

### [#](#下方显示) 下方显示

```
<template>
    <u-tooltip text="下方显示" direction="bottom"></u-tooltip>
</template>
```

### [#](#扩展按钮) 扩展按钮

```
<template>
    <u-tooltip text="扩展显示" :buttons="['扩展']"></u-tooltip>
</template>
```

### [#](#高亮选中文本背景色) 高亮选中文本背景色

```
<template>
    <u-tooltip text="高亮选中文本背景色" :buttons="['扩展']" bgColor="#e3e4e6"></u-tooltip>
</template>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/tooltip/tooltip.vue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/tooltip/tooltip.vue)

### [#](#api) API

### [#](#tooltip-props) Tooltip Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| text | 需要显示的提示文字 | String | Number | \- | \- |
| copyText | 点击复制按钮时，复制的文本，为空则使用text值 | String | Number | \- | \- |
| size | 文本大小 | String | Number | 14 | \- |
| color | 字体颜色 | String | #606266 | \- |
| bgColor | 弹出提示框时，文本的背景色 | String | transparent | \- |
| direction | 弹出提示的方向，top-上方，bottom-下方 | String | top | bottom |
| zIndex | 弹出提示的z-index，nvue无效 | String | Number | 10071 | \- |
| showCopy | 是否显示复制按钮 | Boolean | true | false |
| buttons | 扩展的按钮组 | Array | \- | \- |
| overlay | 是否显示透明遮罩以防止触摸穿透 | Boolean | true | false |
| showToast | 是否显示复制成功或者失败的`toast` | Boolean | true | false |

### [#](#tooltip-events) Tooltip Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击触发事件 | index，被点击按钮的索引 |

← [CountTo 数字滚动](https://www.uviewui.com/components/countTo.html) [ActionSheet 操作菜单](https://www.uviewui.com/components/actionSheet.html) →


