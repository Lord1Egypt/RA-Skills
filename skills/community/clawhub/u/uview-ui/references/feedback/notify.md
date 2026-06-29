---
name: "notify"
description: "Notify 消息提示 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Notify 消息提示 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/notify.html"
---

---

## [#](#notify-消息提示) Notify 消息提示 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般用于页面顶部向下滑出一个提示，尔后自动收起的场景。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

```
<template>
	<u-notify message="Hi uView" :show="show"></u-notify>
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

### [#](#ref调用) ref调用

```
<template>
	<u-notify ref="uNotify" message="Hi uView"></u-notify>
</template>

<script>
export default {
    onReady(){
	    this.$refs.uNotify.show({
            top: 10,
            type: 'error',
            color: '#000',
            bgColor: '#e8e8e8',
            message: 'Hi uView',
            duration: 1000 * 3,
            fontSize: 20,
            safeAreaInsetTop:true
        })

    }
}
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/notify/notify.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/notify/notify.nvue)

### [#](#api) API

### [#](#methods) Methods

| 事件名 | 说明 | 类型 |
| --- | --- | --- |
| show | 显示并加载配置 | Handler |
| primary / success / warning /error | 显示当前主题消息提示 | Handler |
| close | 关闭消息提示 | Handler |

### [#](#show-methods-arguments) Show Methods Arguments

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| top | 到顶部的距离 | String | Number | 0 | \- |
| type | 主题，primary，success，warning，error | String | primary | \- |
| color | 字体颜色 | String | #ffffff | \- |
| bgColor | 背景颜色 | String | \- | \- |
| message | 展示的文字内容 | String | \- | \- |
| duration | 展示时长，为0时不消失，单位ms | String | Number | 3000 | \- |
| fontSize | 字体大小，单位rpx | String | Number | 15 | \- |
| safeAreaInsetTop | 是否留出顶部安全距离（状态栏高度） | Boolean | false | true |

### [#](#slot) Slot

| 参数 | 说明 |
| --- | --- |
| icon | 通知内容 |

← [NoticeBar 滚动通知](https://www.uviewui.com/components/noticeBar.html) [SwipeAction 滑动单元格](https://www.uviewui.com/components/swipeAction.html) →


