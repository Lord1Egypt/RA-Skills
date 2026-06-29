---
name: "overlay"
description: "Overlay 遮罩层 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Overlay 遮罩层 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/overlay.html"
---

---

## [#](#overlay-遮罩层) Overlay 遮罩层 [![](https://www.uviewui.com/common/to_api.png)](#api)

创建一个遮罩层，用于强调特定的页面元素，并阻止用户对遮罩下层的内容进行操作，一般用于弹窗场景

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`show`参数配置是否显示遮罩
-   遮罩被点击时，会发送一个`click`事件，如不需要此事件，请设置`mask-click-able`参数为`false`

```
<template>
	<u-overlay :show="show" @click="show = false"></u-overlay>
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

### [#](#嵌入内容) 嵌入内容

通过默认插槽可以在遮罩层上嵌入任意内容
注意：如果不想让`slot`插槽内容的点击事件冒泡到遮罩，请给指定元素添加上`@tap.stop`

```
<template>
	<u-overlay :show="show" @click="show = false">
		<view class="warp">
			<view class="rect" @tap.stop></view>
		</view>
	</u-overlay>
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

<style scoped>
	.warp {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 100%;
	}

	.rect {
		width: 120px;
		height: 120px;
		background-color: #fff;
	}
</style>
```

### [#](#遮罩样式) 遮罩样式

-   通过`duration`设置遮罩淡入淡出的时长，单位`ms`

```
<u-overlay :show="show" :duration="400" :z-index ="999" :opacity="0.3"></u-overlay>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/overlay/overlay.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/overlay/overlay.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| show | 是否显示遮罩 | Boolean | false | true |
| zIndex | z-index 层级 | String | Number | 10070 | \- |
| duration | 动画时长，单位毫秒 | String | Number | 300 | \- |
| opacity | 不透明度值，当做rgba的第四个参数 | String | Number | 0.5 | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击遮罩发送此事件 | \- |

### [#](#slot) Slot

| 名称 | 说明 |
| --- | --- |
| default | 默认插槽，用于在遮罩层上方嵌入内容 |

← [Line 线条](https://www.uviewui.com/components/line.html) [NoNetwork 无网络提示](https://www.uviewui.com/components/noNetwork.html) →


