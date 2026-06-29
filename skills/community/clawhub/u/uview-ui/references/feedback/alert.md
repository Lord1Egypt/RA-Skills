---
name: "alert"
description: "Alert 警告提示 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Alert 警告提示 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/alert.html"
---

---

## [#](#alert-警告提示) Alert 警告提示 [![](https://www.uviewui.com/common/to_api.png)](#api)

警告提示，展现需要关注的信息。

### [#](#使用场景) 使用场景

-   当某个页面需要向用户显示警告的信息时。
-   非浮层的静态展现形式，始终展现，不会自动消失，用户可以点击关闭。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`title`和`description`设置组件的标题和描述内容
-   通过`type`设置主题类型，有`primary`,`success`,`error`,`warning`,`info`可选值
-   通过`effect`设置主题浅或深色调，有`light`(浅色 默认),`dark`(深色)可选值

```
<template>
	<view>
		<u-alert :title="title" type = "warning" :description = "description"></u-alert>
		<u-alert :title="title" type = "warning" effect="dark" :description = "description"></u-alert>
	</view>
</template>

<script>
export default {
	data() {
		return {
			title:'uView的目标是成为uni-app生态最优秀的UI框架',
			description:'uView是uni-app生态专用的UI框架'
		};
	},
	onLoad() {},
	methods: {
	}
};
</script>
```

### [#](#图标) 图标

通过`showIcon`设置是否显示图标，作用是让信息类型更加醒目。

**注意**：当前版本图标为uView内置图标，根据`type`参数显示不同的图标，无法自定义。

```
<u-alert type="warning" :show-icon="true"></u-alert>
```

### [#](#可关闭的警告提示) 可关闭的警告提示

显示关闭按钮，点击可关闭警告提示。

-   `closable`参数配置是否可关闭

```
<template>
	<view>
		<u-alert :title="title"  type = "warning" :closable="closable" :description = "description"></u-alert>

	</view>
</template>

<script>
export default {
	data() {
		return {
			title:'uView的目标是成为uni-app生态最优秀的UI框架',
			description:'uView是uni-app生态专用的UI框架',
			closable:true
		};
	},
	onLoad() {},
	methods: {
	}
};
</script>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsB/alert/alert.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsB/alert/alert.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| title | 显示的文字 | String | \- | \- |
| type | 使用预设的颜色 | String | warning | success | primary | error | info |
| description | 辅助性文字，颜色比`title`浅一点，字号也小一点，可选 | String | \- | \- |
| closable | 关闭按钮(默认为叉号icon图标) | Boolean | false | true |
| showIcon | 是否显示左边的辅助图标 | Boolean | false | true |
| effect | 多图时，图片缩放裁剪的模式 | String | light(浅色) | dark(深色) |
| center | 文字是否居中 | Boolean | false | true |
| fontSize | 字体大小 | String | Number | 14 | \- |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击组件时触发 | \- |

← [ActionSheet 操作菜单](https://www.uviewui.com/components/actionSheet.html) [Toast 消息提示](https://www.uviewui.com/components/toast.html) →


