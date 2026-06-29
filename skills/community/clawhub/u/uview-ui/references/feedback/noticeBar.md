---
name: "noticeBar"
description: "NoticeBar 滚动通知 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs NoticeBar 滚动通知 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/noticeBar.html"
---

---

## [#](#noticebar-滚动通知) NoticeBar 滚动通知 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件用于滚动通告场景，有多种模式可供选择

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`text`参数设置需要滚动的内容

```
<template>
	<view>
      <u-notice-bar :text="text1"></u-notice-bar>
    </view>
</template>

<script>
	export default {
		data() {
			return {
              text1: 'uView UI众多组件覆盖开发过程的各个需求，组件功能丰富，多端兼容。让您快速集成，开箱即用'
			}
		}
	}
</script>
```

### [#](#可关闭) 可关闭

通过`mode`配置为`closable`让右侧显示关闭按钮

```
<template>
  <view>
    <u-notice-bar :text="text1" mode="closable"></u-notice-bar>
  </view>
</template>

<script>
  export default {
    data() {
      return {
        text1: 'uView UI众多组件覆盖开发过程的各个需求，组件功能丰富，多端兼容。让您快速集成，开箱即用'
      }
    }
  }
</script>
```

### [#](#配置滚动速度和跳转) 配置滚动速度和跳转

-   `speed`可配置横向滚动速度
-   `url`可配置跳转

```
<template>
  <view>
    <u-notice-bar :text="text1" mode="closable" speed="250" url="/pages/componentsB/tag/tag"></u-notice-bar>
  </view>
</template>

<script>
  export default {
    data() {
      return {
        text1: 'uView UI众多组件覆盖开发过程的各个需求，组件功能丰富，多端兼容。让您快速集成，开箱即用'
      }
    }
  }
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/noticeBar/noticeBar.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/noticeBar/noticeBar.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| text | 显示的内容，`direction`为`column`时要求为数组， 为`row`时要求为字符串 | Array | String | \- | \- |
| direction | 通告滚动模式，row-横向滚动，column-竖向滚动 | String | row | column |
| step | direction = row时，是否使用步进形式滚动 | Boolean | false | true |
| icon | 是否显示左侧的音量图标 | String | volume | \- |
| mode | 通告模式，link-显示右箭头，closable-显示右侧关闭图标 | String | \- | link / closable |
| color | 文字颜色 | String | #f9ae3d | \- |
| bgColor | 背景颜色 | String | #fdf6ec | \- |
| speed | 水平滚动时的滚动速度，即每秒滚动多少px(rpx)，这有利于控制文字无论多少时，都能有一个恒定的速度 | String | Number | 80 | \- |
| fontSize | 字体大小 | String | Number | 14 | \- |
| duration | 滚动一个周期的时间长，单位ms | String | Number | 2000 | \- |
| disableTouch | 是否禁止用手滑动切换（目前HX2.6.11，只支持App 2.5.5+、H5 2.5.5+、支付宝小程序、字节跳动小程序） | Boolean | true | false |
| url | 跳转的页面路径 | String | \- | \- |
| linkType | 页面跳转的类型 | String | navigateTo | \- |

### [#](#events) Events

详细解释见上方说明

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| click | 点击通告文字触发 | index: 点击的text的索引 | \- |
| close | 点击右侧关闭图标触发 | \- | \- |

← [Toast 消息提示](https://www.uviewui.com/components/toast.html) [Notify 消息提示](https://www.uviewui.com/components/notify.html) →


