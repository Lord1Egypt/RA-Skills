---
name: "transition"
description: "Transition 动画 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Transition 动画 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/transition.html"
---

---

## [#](#transition-动画) Transition 动画 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件用于组件的动画过渡效果。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

通过slot传入内容，默认使用的是`fade`效果

```
<template>
    <u-transition :show="show">
        <view class="transition"></view>
    </u-transition>
</template>

<script>
    export default {
        data() {
            return {
                show: true
            }
        }
    }
</script>
```

### [#](#动画模式) 动画模式

通过`mode`传入效果模式，目前支持：

-   `fade` 淡入
-   `fade-up` 上滑淡入
-   `fade-down` 下滑淡入
-   `fade-left` 左滑淡入
-   `fade-right` 右滑淡入
-   `slide-up` 上滑进入
-   `slide-down` 下滑进入
-   `slide-left` 左滑进入
-   `slide-right` 右滑进入
-   `zoom-in` 缩放
-   `zoom-out` 缩放

```
<template>
    <u-transition :show="show" mode="zoom-in">
        <view class="transition"></view>
    </u-transition>
</template>

<script>
    export default {
        data() {
            return {
                show: true
            }
        }
    }
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/transition/transition.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/transition/transition.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| show | 是否展示组件 | Boolean | false | true |
| mode | 使用的动画模式 | String | fade | true |
| duration | 动画的执行时间，单位ms | String | Number | 300 | \- |
| timingFunction | 使用的动画过渡函数，见上方说明 | String | ease-out | \- |
| customStyle | 自定义样式 | Object | \- | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| beforeEnter | 进入前触发 | \- |
| enter | 进入中触发 | \- |
| afterEnter | 进入后触发 | \- |
| beforeLeave | 离开前触发 | \- |
| leave | 离开中触发 | \- |
| afterLeave | 离开后触发 | \- |

← [Link 超链接](https://www.uviewui.com/components/link.html)


