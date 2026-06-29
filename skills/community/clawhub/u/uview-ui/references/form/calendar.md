---
name: "calendar"
description: "Calendar 日历 -- uView UI uni-app Vue2 组件/工具。Invoke when user needs Calendar 日历 in uni-app Vue 2.x project."
url: "https://www.uviewui.com/components/calendar.html"
---

---

## [#](#calendar-日历) Calendar 日历 [![](https://www.uviewui.com/common/to_api.png)](#api)

此组件用于单个选择日期，范围选择日期等，日历被包裹在底部弹起的容器中。

**注意：** 此组件与[Picker 选择器](https://www.uviewui.com/components/picker.html)的日期选择模式有一定的重合之处，区别在于本组件为更专业的日期选择场景，能选择日期范围等。 另外`Picker`组件的日期模式可以配置更多的参数，如时、分、秒等，可以根据不同的使用场景进行选择。

### [#](#平台差异说明) 平台差异说明

| App（vue） | App（nvue） | H5 | 小程序 |
| --- | --- | --- | --- |
| √ | √ | √ | √ |

### [#](#基本使用) 基本使用

-   通过`show`绑定一个布尔变量用于打开或收起日历弹窗。
-   通过`mode`参数指定选择日期模式，包含单选/多选/范围选择。

```
<template>
	<view>
		<u-calendar :show="show"></u-calendar>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				show: false,
			}
		}
	}
</script>
```

### [#](#日历模式) 日历模式

-   `mode`为`single`只能选择单个日期
-   `mode`为`multiple`可以选择多个日期
-   `mode`为`range`可以选择日期范围

### [#](#单个日期模式) 单个日期模式

选择日期后，需要点击底部的`确定`按钮才能触发回调事件，回调参数为一个数组，有如下属性：

```
["2021-07-01"]
```

示例代码：

```
<template>
	<u-calendar :show="show" :mode="mode" @confirm="confirm"></u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
				mode: 'single'
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			}
		}
	}
</script>
```

### [#](#多个日期模式) 多个日期模式

选择日期后，需要点击底部的`确定`按钮才能触发回调事件，回调参数为一个数组，有如下属性：

```
 ["2021-07-27", "2021-07-29", "2021-07-30"]
```

示例代码：

```
<template>
	<u-calendar :show="show" :mode="mode" @confirm="confirm"></u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
				mode: 'multiple'
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			}
		}
	}
</script>
```

### [#](#日期范围模式) 日期范围模式

此模式用于选择一个日期范围，比如住酒店的入住到离店的日期范围，

此模式的返回参数如下：

```
["2021-07-27", "2021-07-28", "2021-07-29", "2021-07-30", "2021-07-31"]
```

示例代码：

```
<template>
	<u-calendar :show="show" :mode="mode" @confirm="confirm"></u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
				mode: 'range'
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			}
		}
	}
</script>
```

### [#](#自定义主题颜色) 自定义主题颜色

组件可传入`color`参数，更改组件主题色

示例代码：

```
<template>
	<u-calendar :show="show"
    color="#f56c6c" :mode="mode" @confirm="confirm"></u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
				mode: 'range'
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			}
		}
	}
</script>
```

### [#](#自定义文案) 自定义文案

组件可以通过`formatter`以函数的方式定义日期文案

注意：

微信小程序不支持通过`props`传递函数参数，所以组件内部暴露了一个`setFormatter`方法用于设置格式化方法，注意在页面的`onReady`生命周期获取`ref`再操作。

```
<template>
	<u-calendar
        startText="住店"
        endText="离店"
        confirmDisabledText="请选择离店日期"
        :formatter="formatter"
        :show="show"
        :mode="mode"
        @confirm="confirm"
		ref="calendar"
	>
    </u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
				mode: 'range'
			}
		},
		onReady() {

			this.$refs.calendar.setFormatter(this.formatter)
		},
		methods: {
			confirm(e) {
				console.log(e);
			},
			formatter(day) {
				const d = new Date()
				let month = d.getMonth() + 1
				const date = d.getDate()
				if(day.month == month && day.day == date + 3)
				{
					day.bottomInfo = '有优惠'
					day.dot = true
				}
				return day
		    }
		}
	}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```

### [#](#日期最大范围) 日期最大范围

组件可以通过`maxDate`定义日期文案

```
<template>
	<u-calendar
        :maxDate="maxDate"
        :show="show"
        @confirm="confirm">
	</u-calendar>
</template>

<script>
	const d = new Date()
	const year = d.getFullYear()
	let month = d.getMonth() + 1
	month = month < 10 ? `0${month}` : month
	const date = d.getDate()
	export default {
		data() {
			return {
				show: true,
				maxDate: `${year}-${month}-${date + 10}`,
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			},
		}
	}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```

### [#](#是否显示农历) 是否显示农历

组件可以通过`showLunar`定义是否显示农历

```
<template>
	<u-calendar
        showLunar
        :show="show"
        @confirm="confirm">
	</u-calendar>
</template>

<script>
	export default {
		data() {
			return {
				show: true,
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			},
		}
	}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```

### [#](#默认日期) 默认日期

组件可以通过`defaultDate`定义默认日期

```
<template>
	<u-calendar
        :defaultDate="defaultDateMultiple"
        :show="show"
        mode="multiple"
        @confirm="confirm">
	</u-calendar>
</template>

<script>
	const d = new Date()
	const year = d.getFullYear()
	let month = d.getMonth() + 1
	month = month < 10 ? `0${month}` : month
	const date = d.getDate()
	export default {
		data() {
			return {
				show: true,
				defaultDateMultiple: [`${year}-${month}-${date}`, `${year}-${month}-${date + 1}`, `${year}-${month}-${date + 2}`],
			}
		},
		methods: {
			confirm(e) {
				console.log(e);
			},
		}
	}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```

### [#](#此页面源代码地址) 此页面源代码地址

页面源码地址

 [![](https://www.uviewui.com/common/github.svg "github") github](https://github.com/umicro/uView2.0/blob/master/pages/componentsC/calendar/calendar.nvue)  [![](https://www.uviewui.com/common/gitee.svg "github") gitee](https://gitee.com/umicro/uView2.0/blob/master/pages/componentsC/calendar/calendar.nvue)

### [#](#api) API

### [#](#props) Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 |
| --- | --- | --- | --- | --- |
| title | 标题内容 | String | 日期选择 | \- |
| showTitle | 是否显示标题 | Boolean | true | false |
| showSubtitle | 是否显示副标题 | Boolean | true | false |
| mode | 日期类型选择 | String | single | multiple-可以选择多个日期，range-选择日期范围（多个月需配合`monthNum`属性使用） |
| startText | mode=range时，第一个日期底部的提示文字 | String | 开始 | \- |
| endText | mode=range时，最后一个日期底部的提示文字 | String | 结束 | \- |
| customList | 自定义列表 | Array | \[\] | \[\] |
| color | 主题色，对底部按钮和选中日期有效 | String | #3c9cff | \- |
| minDate | 最小的可选日期 | Number | String | 0 | \- |
| maxDate | 最大可选日期 | Number | String | 0 | \- |
| defaultDate | 默认选中的日期，mode为multiple或range是必须为数组格式 | Array | String | Date | null | \- |
| maxCount | mode=multiple时，最多可选多少个日期 | Number | String | Number.MAX\_SAFE\_INTEGER | \- |
| rowHeight | 日期行高 | Number |String | 56 | \- |
| formatter | 日期格式化函数(如需兼容微信小程序，则只能通过`setFormatter`方法) | Function | null | \- |
| showLunar | 是否显示农历 | Boolean | false | true |
| showMark | 是否显示月份背景色 | Boolean | true | false |
| confirmText | 确定按钮的文字 | String | 确定 | \- |
| confirmDisabledText | 确认按钮处于禁用状态时的文字 | String | 确定 | \- |
| show | 是否显示日历弹窗 | Boolean | false | true |
| closeOnClickOverlay | 是否允许点击遮罩关闭日历 （注意：关闭事件需要自行处理，只会在开启closeOnClickOverlay后点击遮罩层执行close回调） | Boolean | false | true |
| readonly | 是否为只读状态，只读状态下禁止选择日期 | Boolean | false | true |
| maxRange | 日期区间最多可选天数，默认无限制，mode = range时有效 | Number | String | 无限制 | \- |
| rangePrompt | 范围选择超过最多可选天数时的提示文案，mode = range时有效 | String | null | 选择天数不能超过 xx 天 | \- |
| showRangePrompt | 范围选择超过最多可选天数时，是否展示提示文案，mode = range时有效 | Boolean | true | false |
| allowSameDay | 是否允许日期范围的起止时间为同一天，mode = range时有效 | Boolean | false | true |
| round | 圆角值，默认无圆角 | String | Number | 0 | \- |
| monthNum 2.0.17 | 最大展示的月份数量 | String | Number | 3 | \- |

### [#](#methods) Methods

| 方法名 | 说明 |
| --- | --- |
| setFormatter | 为兼容微信小程序而暴露的内部方法，见上方说明 |

### [#](#event) Event

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| confirm | 日期选择完成后触发，若`show-confirm`为`true`，则点击确认按钮后触发 | 选择日期相关的返回参数 |
| close | 日历关闭时触发 | 可定义页面关闭时的回调事件 |

← [Form 表单](https://www.uviewui.com/components/form.html) [Keyboard 键盘](https://www.uviewui.com/components/keyboard.html) →


