---
name: "rate"
description: "Rate 评分 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Rate 评分 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/rate.html"
---

---

## [#](#rate-评分) Rate 评分 [![](https://www.uviewui.com/common/to_api.png)](#api)

该组件一般用于满意度调查，星型评分的场景。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`count`参数设置总共有多少颗星星可选择
-   通过`v-model`双向绑定初始化时默认选中的星星数量

```
<template>
	<u-rate :count="count" v-model="value"></u-rate>
</template>

<script>
	export default {
		data() {
			return {
				count: 4,
				value: 2
			}
		}
	}
</script>
```

### [#](#自定义样式) 自定义样式

-   通过`active-color`设置选中的星星的颜色
-   通过`inactive-color`设置未选中时星星的颜色
-   通过`gutter`设置星星的间距，左右内边距各占`gutter`的一半

```
<u-rate active-color="#FA3534" inactive-color="#b2b2b2" gutter="20"></u-rate>
```

### [#](#自定义图标) 自定义图标

-   通过`active-icon`设置激活的图标
-   通过`inactive-icon`设置未激活的图标

下方示例为使用心形图标替代默认的星星图标：

```
<u-rate activeIcon="heart-fill" inactiveIcon="heart"></u-rate>
```

### [#](#最少选中的数量) 最少选中的数量

```
<u-rate :minCount="5"></u-rate>
```

### [#](#禁用状态) 禁用状态

禁用下，无法点击或者滑动选择，但是可以通过`value`设置默认选中的数量，禁用状态下用来展示分数，允许出现半星

```
<u-rate :value="3.7" disabled></u-rate>
```

### [#](#只读状态) 只读状态

只读下，无法点击或者滑动选择，但是可以通过`value`设置默认选中的数量，禁用状态下用来展示分数，允许出现半星

```
<u-rate :value="3.7" readonly></u-rate>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsA/rate/rate.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsA/rate/rate.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| value | 双向绑定选择星星的数量 | String | Number | 1 | \- |
| count | 最多可选的星星数量 | String | Number | 5 | \- |
| disabled | 是否禁止用户操作 | Boolean | false | true |
| readonly 2.0.30 | 是否只读 | Boolean | false | true |
| size | 星星的大小，单位rpx | String | Number | 18 | \- |
| inactiveColor | 未选中星星的颜色 | String | #b2b2b2 | \- |
| activeColor | 选中的星星颜色 | String | #FA3534 | \- |
| gutter | 星星之间的距离 | String | Number | 4 | \- |
| minCount | 最少选中星星的个数 | String | Number | 1 | \- |
| allowHalf | 是否允许半星选择 | Boolean | false | true |
| activeIcon | 选中时的图标名，只能为uView的内置图标 | String | star-fill | \- |
| inactiveIcon | 未选中时的图标名，只能为uView的内置图标 | String | star | \- |
| touchable | 是否可以通过滑动手势选择评分 | Boolean | true | false |

### [#](#events) Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 选中的星星发生变化时触发 | value：当前选中的星星的数量，如果使用`v-model`双向绑定方式，无需监听此事件 |

← [DatetimePicker 选择器](https://www.uviewui.com/components/datetimePicker.html) [Search 搜索](https://www.uviewui.com/components/search.html) →


