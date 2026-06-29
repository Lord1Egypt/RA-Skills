---
name: "popup"
description: "Popup 弹出层 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Popup 弹出层 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/popup.html"
---

---

## [#](#popup-弹出层) Popup 弹出层 [![](https://www.uviewui.com/common/to_api.png)](#api)

弹出层容器，用于展示弹窗、信息提示等内容，支持上、下、左、右和中部弹出。组件只提供容器，内部内容由用户自定义。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   弹出层的内容通过`slot`传入，由用户自定义
-   通过`show`绑定一个布尔值的变量控制弹出层的打开和收起

```
<template>
	<view>
		<u-popup :show="show" @close="close" @open="open">
            <view>
                <text>出淤泥而不染，濯清涟而不妖</text>
            </view>
		</u-popup>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>
<script>
	export default {
      data() {
        return {
          show: false
        }
      },
      methods: {
        open() {

        },
        close() {
          this.show = false

        }
      }
	}
</script>
```

### [#](#设置弹出层的方向) 设置弹出层的方向

-   可以通过`mode`参数设置，可以设置为`left`、`top`、`right`、`bottom`、`center`

```
<template>
	<u-popup :show="show" mode="top"  @close="close" @open="open">
        <view>
            <text>人生若只如初见，何事秋风悲画扇</text>
        </view>
	</u-popup>
</template>
<script>
  export default {
    data() {
      return {
        show: false
      }
    },
    methods: {
      open() {

      },
      close() {
        this.show = false

      }
    }
  }
</script>
```

### [#](#设置弹出层的圆角) 设置弹出层的圆角

需要将`round`设置为圆角值(仅对`mode = top | bottom | center`有效)。

```
<template>
	<u-popup :show="show" :round="10" mode="top" @close="close" @open="open">
		<view>
            <text>人生若只如初见，何事秋风悲画扇</text>
		</view>
	</u-popup>
</template>
<script>
  export default {
    data() {
      return {
        show: false
      }
    },
    methods: {
      open() {

      },
      close() {
        this.show = false

      }
    }
  }
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/popup/popup.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/popup/popup.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| show | 是否展示弹窗 | Boolean | false | true |
| overlay | 是否显示遮罩 | Boolean | true | false |
| mode | 弹出方向 | String | bottom | top / right / bottom / center |
| duration | 遮罩打开或收起的动画过渡时间，单位ms | String | Number | 300 | \- |
| closeable | 是否显示关闭图标 | Boolean | false | true |
| overlayStyle | 遮罩自定义样式，一般用于修改遮罩颜色，如：{background: 'rgba(3, 100, 219, 0.5)'} | Object | String | \- | \- |
| overlayOpacity | 遮罩透明度，`0-1`之间，勿与`overlayStyle`共用 | Number | String | 0.5 | \- |
| closeOnClickOverlay | 点击遮罩是否关闭弹窗（注意：关闭事件需要自行处理，只会在开启closeOnClickOverlay后点击遮罩层执行close回调） | Boolean | true | false |
| zIndex | 弹出层的`z-index`值 | Number | String | 10075 | \- |
| safeAreaInsetBottom | 是否为留出[底部安全距离](https://www.uviewui.com/components/safeAreaInset.html) | Boolean | true | false |
| safeAreaInsetTop | 是否留出[顶部安全距离](https://www.uviewui.com/components/safeAreaInset.html)（状态栏高度） | Boolean | false | true |
| closeIconPos | 自定义关闭图标位置，top-left为左上角，top-right为右上角，bottom-left为左下角，bottom-right为右下角 | String | top-right | top-left / bottom-left / bottom-right |
| round | 设置圆角值，仅对`mode = top | bottom | center`有效 | Number | String | 0 | \- |
| zoom | 当mode=center时 是否开启缩放 | Boolean | true | false |
| bgColor | 背景色，一般用于特殊弹窗内容场景，设置为`transparent`可去除默认的白色背景 | String | \- | \- |
| customStyle | 用户自定义样式 | Object | \- | \- |

### [#](#event) Event

| 事件名 | 说明 | 回调参数 | 版本 |
| --- | --- | --- | --- |
| open | 弹出层打开 | \- | \- |
| close | 弹出层收起 | \- | \- |

← [Collapse 折叠面板](https://www.uviewui.com/components/collapse.html) [Modal 模态框](https://www.uviewui.com/components/modal.html) →


