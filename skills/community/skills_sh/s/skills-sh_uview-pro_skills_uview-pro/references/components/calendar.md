---
name: "calendar"
description: "此组件用于单个选择日期，范围选择日期等，日历被包裹在底部弹起的容器中。. Invoke when user needs to use calendar component."
url: "https://uviewpro.cn/zh/components/calendar.html"
triggers: ["calendar","日历"]
---

# Calendar 日历 <to-api/>

<demo-model url="/pages/componentsA/calendar/index"></demo-model>


此组件用于单个选择日期，范围选择日期等，日历被包裹在底部弹起的容器中。

**注意：** 此组件与[Picker 选择器](/zh/components/picker.html)的日期选择模式有一定的重合之处，区别在于本组件为更专业的日期选择场景，能选择日期范围等。
另外`Picker`组件的日期模式可以配置更多的参数，如时、分、秒等，可以根据不同的使用场景进行选择。


## 平台差异说明

| App | H5 | 微信小程序 | 支付宝小程序 | 百度小程序 | 头条小程序 | QQ小程序 |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| √ | √ | √ | √ | √ | √ | √ |


## 基本使用


- 通过`v-model`绑定一个布尔变量用于打开或收起日历弹窗。
- 通过`mode`参数指定选择单个日期，还是选择日期范围。

```html
<template>
	<view>
		<u-calendar v-model="show" :mode="mode"></u-calendar>
		<u-button @click="show = true">打开</u-button>
	</view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { CalendarMode } from 'uview-pro/types/global'

const show = ref(false)
const mode = ref<CalendarMode>('date')

</script>
```


## 日历模式

- `mode`为`date`只能选择单个日期
- `mode`为`range`可以选择日期范围


## 单个日期模式

选择日期后，需要点击底部的`确定`按钮才能触发回调事件，回调参数为一个对象，有如下属性：

```js
{
	day: 4, // 选择了哪一天
	days: 30, // 这个月份有多少天
	isToday: true, // 选择的日期是否今天
	month: 6, // 选择的月份
	result: "2020-06-04", // 选择的日期整体值
	week: "星期四", // 选择日期所属的星期数
	year: 2020 , // 选择的年份
}
```

示例代码：

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change"></u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('date')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>
```


## 日期范围模式

此模式用于选择一个日期范围，比如住酒店的入住到离店的日期范围，有如下可配置的参数：

- `active-bg-color`参数配置起始/结束日期按钮的背景色
- `active-color`参数配置起始/结束日期按钮的字体颜色
- `range-bg-color`参数配置起始/结束日期之间的区域的背景颜色，默认为`var(--u-type-primary-light)`，为浅蓝色
- `start-text`参数用于设置起始日期底部的提示文字，如"住店"
- `end-text`参数用于设置结束日期底部的提示文字，如"离店"


此模式的返回参数如下：

```js
{
	endDate: "2020-06-04", // 选择的结束日期
	endDay: 4, // 结束日期是哪一天
	endMonth: 6, // 结束日期的月份
	endWeek: "星期四", // 结束日期的星期数
	endYear: 2020, // 结束日期的年份
	startDate: "2020-06-01", // 选择的起始日期
	startDay: 1, // 起始日期是哪一天
	startMonth: 6, // 起始日期的月份
	startWeek: "星期一", // 起始日期的星期数
	startYear: 2020 // 起始日期的年份
}
```

示例代码：

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change"></u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('range')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>
```

## 显示农历模式 <BadgeVersion text="0.2.1" />

支持农历选择和回调，配置的参数：

- `show-lunar`是否显示农历


单个日期模式的返回参数如下：

```js
{
	day: 4, // 选择了哪一天
	days: 30, // 这个月份有多少天
	isToday: true, // 选择的日期是否今天
	month: 6, // 选择的月份
	result: "2020-06-04", // 选择的日期整体值
	week: "星期四", // 选择日期所属的星期数
	year: 2020 , // 选择的年份
	lunar: { 
		dayCn: '十三', // 农历的日
        monthCn: '四月', // 农历的月
		weekCn: "星期四", // 选择日期所属的星期数
        day: '13', // 农历的日
        month: '4', // 农历的月
		week: 4, // 选择日期所属的星期数
        year: 2020 // 农历的年份
	},
}
```

日期范围模式的返回参数如下：

```js
{
	endDate: "2020-06-04", // 选择的结束日期
	endDay: 4, // 结束日期是哪一天
	endMonth: 6, // 结束日期的月份
	endWeek: "星期四", // 结束日期的星期数
	endYear: 2020, // 结束日期的年份
	startDate: "2020-06-01", // 选择的起始日期
	startDay: 1, // 起始日期是哪一天
	startMonth: 6, // 起始日期的月份
	startWeek: "星期一", // 起始日期的星期数
	startYear: 2020, // 起始日期的年份
	startLunar: { 
		dayCn: '初十',
        monthCn: '四月',
		weekCn: "星期一",
        day: '13',
        month: '4',
		week: 1,
        year: 2020
	},
	endLunar: { 
		dayCn: '十三',
        monthCn: '四月',
		weekCn: "星期四",
        day: '13',
        month: '4',
		week: 4,
        year: 2020
	},
}
```

示例代码：

```html
<template>
	<view>
		<u-calendar v-model="show" :mode="mode" :show-lunar="showLunar" @change="change"></u-calendar>
		<view>{{ result }}</view>
		<view>{{ lunarResult }}</view>
	</view>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const result = ref('')
const lunarResult = ref('')
const mode = ref<CalendarMode>('date')
const showLunar = ref(true)


function change(e: CalendarChangeRange | CalendarChangeDate) {
    if (mode.value === 'range') {
        const range = e as CalendarChangeRange;
        result.value = range.startDate + ' - ' + range.endDate;
        if (showLunar.value && range.startLunar && range.endLunar) {
            lunarResult.value = `${range.startLunar.monthCn ?? ''}${range.startLunar.dayCn ?? ''}` + ' - ' + `${range.endLunar.monthCn ?? ''}${range.endLunar.dayCn ?? ''}`;
        } else {
            lunarResult.value = '';
        }
    } else {
        const single = e as CalendarChangeDate;
        result.value = single.result;
        if (showLunar.value && single.lunar) {
            lunarResult.value = `${single.lunar.monthCn ?? ''}${single.lunar.dayCn ?? ''}`;
        } else {
            lunarResult.value = '';
        }
    }
}
</script>
```


## 页面模式 <BadgeVersion text="0.5.17" />

通过`is-page`参数可以将日历直接嵌入页面中显示，而不是以弹窗形式展示。

- `is-page`为`true`时，日历直接嵌入页面，不显示弹窗和确定按钮
- 选择日期后自动触发`change`事件

```html
<template>
	<u-calendar :is-page="true" :mode="mode" @change="change"></u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const mode = ref<CalendarMode>('date')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>
```


## 默认选中日期 <BadgeVersion text="0.5.17" />

支持传入默认选中的日期，组件初始化时会自动选中指定日期。

- `default-date`：单选模式下默认选中的日期，格式：`2024-01-01`
- `start-date`：范围模式下默认选中的开始日期，格式：`2024-01-01`
- `end-date`：范围模式下默认选中的结束日期，格式：`2024-01-01`

```html
<template>
	<!-- 单选模式默认选中 -->
	<u-calendar v-model="show" mode="date" default-date="2024-01-15"></u-calendar>
	
	<!-- 范围模式默认选中 -->
	<u-calendar v-model="show" mode="range" start-date="2024-01-01" end-date="2024-01-07"></u-calendar>
</template>
```


## 只读模式 <BadgeVersion text="0.5.17" />

通过`readonly`参数可以设置日历为只读模式，禁止点击选择日期。

```html
<template>
	<u-calendar :is-page="true" :readonly="true"></u-calendar>
</template>
```


## 打卡签到模式 <BadgeVersion text="0.5.17" />

支持打卡签到功能，可以显示已打卡日期和今日打卡状态。

### 属性说明

- `checked-dates`：已打卡日期列表，格式：`['2024-01-01', '2024-01-02']`
- `today-checked`：今日是否已打卡（优先级高于自动判断）
- `checkin-mode`：是否启用打卡签到模式，未打卡日期显示灰色背景
- `checked-bg-color`：已打卡日期背景色，默认为`var(--u-type-warning)`（橙色）
- `today-checked-bg-color`：今日已打卡背景色，默认为`var(--u-type-success)`（绿色）
- `unchecked-bg-color`：未打卡日期背景色，默认为`var(--u-light-color)`（灰色）

### 显示规则

1. 今日已打卡：绿色圆形背景，显示白色对勾
2. 其他已打卡日期：橙色圆形背景，显示日期
3. 未打卡日期（checkin-mode为true时）：灰色圆形背景

### 示例代码

```html
<template>
	<u-calendar
		:is-page="true"
		:checkin-mode="true"
		:checked-dates="checkedDates"
		:today-checked="todayChecked"
	></u-calendar>
</template>

<script setup>
import { ref } from 'vue'

// 已打卡日期（自动判断今天是否在列表中）
const checkedDates = ref(['2024-01-01', '2024-01-02', '2024-01-03'])

// 手动标记今天已打卡（优先级高于自动判断）
const todayChecked = ref(true)
</script>
```


## 节假日和加班日 <BadgeVersion text="0.5.17" />

支持显示节假日和加班日标记。

### 属性说明

- `holidays`：节假日列表，格式：`['2024-01-01', '2024-01-02']`（标准日期格式 `YYYY-MM-DD`）
- `workdays`：加班日列表，格式：`['2024-01-06', '2024-01-07']`（标准日期格式 `YYYY-MM-DD`）
- `holiday-color`：节假日文字颜色，默认为`var(--u-type-error)`（红色）
- `workday-color`：加班日文字颜色，默认为`var(--u-type-primary)`（蓝色）

### 显示规则

1. 节假日：显示红色"休"字
2. 加班日：显示蓝色"班"字
3. 选中的节假日/加班日：显示白色"休"/"班"字（与选中日期文字颜色一致）
4. 范围选择时：优先显示"开始"/"结束"文案

### 示例代码

```html
<template>
	<u-calendar
		:is-page="true"
		:holidays="holidays"
		:workdays="workdays"
	></u-calendar>
</template>

<script setup>
import { ref } from 'vue'

// 节假日（元旦假期）
const holidays = ref(['2024-01-01', '2024-01-02', '2024-01-03'])

// 加班日（调休上班）
const workdays = ref(['2024-01-06', '2024-01-07'])
</script>
```


## 节日显示 <BadgeVersion text="0.5.17" />

支持显示中国传统节日和自定义节日。

### 属性说明

- `show-festival`：是否显示内置节日（中国传统节日），默认为`false`
- `festivals`：自定义节日配置，格式：`{ '04-04': '清明节', '04-01': '愚人节' }`（支持 `MM-DD` 和 `YYYY-MM-DD` 两种格式）
- `festival-color`：节日文字颜色，默认为`var(--u-type-primary)`（主题色）

### 内置节日

当`show-festival`为`true`时，会自动显示以下中国传统节日：
- 元旦（1月1日）
- 情人节（2月14日）
- 妇女节（3月8日）
- 植树节（3月12日）
- 愚人节（4月1日）
- 劳动节（5月1日）
- 青年节（5月4日）
- 儿童节（6月1日）
- 建党节（7月1日）
- 建军节（8月1日）
- 教师节（9月10日）
- 国庆节（10月1日）
- 光棍节（11月11日）
- 圣诞节（12月25日）

### 自定义节日

可以通过`festivals`属性添加自定义节日，支持两种配置格式：

| 格式 | 示例 | 说明 |
| :- | :- | :- |
| `YYYY-MM-DD` | `'2024-04-04': '清明节'` | 特定年份的节日，只在指定年份显示 |
| `MM-DD` | `'04-04': '清明节'` | 每年的固定节日，每年都显示 |

**格式说明：**
- 使用**标准日期格式**，月份和日期需要**前导零**（如 `04-04` 而不是 `4-4`）
- 所有日期相关配置（节日、节假日、加班日）都使用统一格式

**优先级规则：**
1. 特定年份格式（`年-月-日`）优先级最高
2. 每年固定格式（`月-日`）次之
3. 内置节日优先级最低

**覆盖内置节日：** 传入空字符串可以覆盖内置节日（表示不显示该节日）。

### 示例代码

```html
<template>
	<u-calendar
		:is-page="true"
		:show-festival="true"
		:festivals="customFestivals"
	></u-calendar>
</template>

<script setup>
import { ref } from 'vue'

// 自定义节日（覆盖或补充内置节日）
const customFestivals = ref({
	// 每年固定节日（MM-DD格式）
	'04-04': '清明节', // 每年4月4日都显示
	'05-05': '端午节', // 每年5月5日都显示
	'08-15': '中秋节', // 每年8月15日都显示
	
	// 特定年份节日（YYYY-MM-DD格式）- 优先级更高
	'2025-04-04': '清明节', // 2025年显示，覆盖上面的04-04
	
	// 覆盖内置节日（传入空字符串不显示）
	'02-14': '', // 不显示情人节
})
</script>
```

### 关闭内置节日，完全自定义

```html
<template>
	<u-calendar
		:is-page="true"
		:show-festival="false"
		:festivals="{
			'04-04': '清明节', // 每年4月4日显示
			'10-01': '国庆节', // 每年8月15日显示
		}"
	></u-calendar>
</template>
```


## 自定义日期内容（价格日历）<BadgeVersion text="0.5.17" />

通过`date`插槽可以自定义每个日期的显示内容，常用于电商价格日历等场景。

### 插槽参数

| 属性 | 说明 | 类型 |
| :- | :- | :- |
| date.year | 年份 | Number |
| date.month | 月份 | Number |
| date.day | 日期 | Number |
| date.date | 完整日期字符串 | String |
| date.week | 星期文字 | String |
| date.weekNum | 星期数字 0-6 | Number |
| date.isToday | 是否今天 | Boolean |
| date.isHoliday | 是否节假日 | Boolean |
| date.isWorkday | 是否加班日 | Boolean |
| date.isChecked | 是否已打卡 | Boolean |
| date.isSelected | 是否选中 | Boolean |
| date.isTodayChecked | 今天是否已打卡 | Boolean |
| date.lunar | 农历信息 | Object |

### 注意事项

- 使用自定义日期插槽时，需要设置`use-date-slot="true"`显式声明
- 自定义插槽优先级最高，会覆盖农历、节日等默认显示内容

### 示例代码

```html
<template>
	<u-calendar :is-page="true" :mode="mode" :use-date-slot="true">
		<template #date="{ date }">
			<text :class="getPriceClass(date)">{{ getPrice(date) }}</text>
		</template>
	</u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarMode } from 'uview-pro/types/global'

const mode = ref<CalendarMode>('date')
const priceMap = ref({
	'2024-01-01': 299,
	'2024-01-02': 399,
	// ...
})

function getPrice(date) {
	if (date.isToday) return '今天'
	return '¥' + (priceMap.value[date.date] || '')
}

function getPriceClass(date) {
	if (date.isSelected) return '' // 选中时使用默认白色
	if (date.isToday) return 'price-today'
	return 'price-normal'
}
</script>

<style lang="scss" scoped>
.price-today {
	color: var(--u-type-success);
	font-weight: bold;
}
.price-normal {
	color: var(--u-tips-color);
}
</style>
```


## 默认选中今天 <BadgeVersion text="0.5.17" />

通过`default-select-today`参数控制初始化时是否默认选中今天。

**优先级规则：**
1. 优先级1: `default-date` / `start-date` / `end-date`（显式指定日期）
2. 优先级2: `default-select-today`（默认选中今天，默认值为`true`）
3. 优先级3: 不选中任何日期

```html
<template>
	<!-- 价格日历场景：默认不选中任何日期 -->
	<u-calendar :is-page="true" :default-select-today="false"></u-calendar>
	
	<!-- 普通日历场景：默认选中今天（无需配置，默认值） -->
	<u-calendar :is-page="true"></u-calendar>
</template>
```


## 选中效果控制 <BadgeVersion text="0.5.17" />

通过`is-active-current`参数控制选中日期是否显示选中效果（背景色和文字颜色）。

```html
<template>
	<!-- 价格日历：不显示选中效果，保持价格颜色 -->
	<u-calendar :is-page="true" :is-active-current="false"></u-calendar>
</template>
```


## 自定义内容

组件有一个默认插槽，名为`tooltip`，传入的内容将会显示在键盘的顶部位置，如使用，需要为传入的内容自定义样式。

```html
<template>
	<u-calendar v-model="show" :mode="mode" @change="change">
		<template #tooltip>
			<view class="title">
				请选择住店/离店时间
			</view>
		</template>
	</u-calendar>
</template>

<script setup>
import { ref } from 'vue'
import type { CalendarChangeDate, CalendarChangeRange, CalendarMode } from 'uview-pro/types/global'

const show = ref(true)
const mode = ref<CalendarMode>('range')

function change(e: CalendarChangeRange | CalendarChangeDate) { 
	console.log(e)
}
</script>

<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
		text-align: center;
		padding: 20rpx 0 0 0;
	}
</style>
```



## API

### Props

| 参数 | 说明 | 类型 | 默认值 | 可选值 | 版本 |
| :- | :- | :- | :- | :- | :- |
| mode | 选择日期的模式，date-为单个日期，range-为选择日期范围 | String | date | range | - |
| v-model | 布尔值变量，用于控制日历的弹出与收起 | Boolean | false | true | - |
| safe-area-inset-bottom | 是否开启[底部安全区适配](/zh/components/safeAreaInset.html#关于uview某些组件safe-area-inset参数的说明) | Boolean | false | true | - |
| change-year | 是否显示顶部的切换年份方向的按钮 | Boolean | true | false | - |
| change-month | 是否显示顶部的切换月份方向的按钮 | Boolean | true | false | - |
| max-year | 可切换的最大年份 | Number \| String | 2050 | - | - |
| min-year | 可切换的最小年份 | Number \| String | 1950 | - | - |
| min-date | 最小可选日期 | Number \| String | 1950-01-01 | - | - |
| max-date | 最大可选日期 | Number \| String | 当前日期 | - | - |
| border-radius | 弹窗顶部左右两边的圆角值，单位rpx | Number \| String | 20 | - | - |
| mask-close-able | 是否允许通过点击遮罩关闭日历 | Boolean | true | false | - |
| month-arrow-color | 月份切换按钮箭头颜色 | String | var(--u-content-color) | - | - |
| year-arrow-color | 年份切换按钮箭头颜色 | String | var(--u-tips-color) | - | - |
| color | 日期字体的默认颜色 | String | var(--u-main-color) | - | - |
| active-bg-color | 起始/结束日期按钮的背景色 | String | var(--u-type-primary) | - | - |
| z-index | 弹出时的`z-index`值 | String \| Number | 10075 | - | - |
| active-color | 起始/结束日期按钮的字体颜色 | String | var(--u-white-color) | - | - |
| range-bg-color | 起始/结束日期之间的区域的背景颜色 | String | var(--u-type-primary-light) | - | - |
| range-color | 选择范围内字体颜色 | String | var(--u-type-primary) | - | - |
| start-text | 起始日期底部的提示文字 | String | 开始 | - | - |
| end-text | 结束日期底部的提示文字 | String | 结束 | - | - |
| btn-type | 底部确定按钮的主题 | String | primary | default / success / info / warning / error | - |
| toolTip | 顶部提示文字，如设置名为`tooltip`的`slot`，此参数将失效 | String | 选择日期 | - | - |
| closeable | 是否显示右上角的关闭图标 | Boolean | true | false | - |
| is-change | 切换年月是否触发事件，mode=date时生效 | Boolean | false | true | - |
| show-lunar | 是否显示农历 | Boolean | false | true | 0.2.1 |
| is-page | 是否在页面中直接显示，不使用弹窗 | Boolean | false | true | 0.5.17 |
| default-date | 默认选中的日期，mode=date时生效，格式：2024-01-01 | String | '' | - | 0.5.17 |
| start-date | 默认选中的开始日期，mode=range时生效，格式：2024-01-01 | String | '' | - | 0.5.17 |
| end-date | 默认选中的结束日期，mode=range时生效，格式：2024-01-01 | String | '' | - | 0.5.17 |
| default-select-today | 初始化时是否默认选中今天，优先级低于default-date/start-date/end-date | Boolean | true | false | 0.5.17 |
| is-active-current | 当前选中日期是否带选中效果 | Boolean | true | false | 0.5.17 |
| readonly | 是否只读，只读模式下禁止点击选择日期 | Boolean | false | true | 0.5.17 |
| checked-dates | 已打卡日期列表，格式：['2024-01-01', '2024-01-02'] | Array | [] | - | 0.5.17 |
| today-checked | 今日是否已打卡（优先级高于自动判断） | Boolean | false | true | 0.5.17 |
| checkin-mode | 是否启用打卡签到模式（未打卡日期显示灰色） | Boolean | false | true | 0.5.17 |
| checked-bg-color | 已打卡日期背景色 | String | var(--u-type-warning) | - | 0.5.17 |
| checked-color | 已打卡日期字体颜色 | String | var(--u-white-color) | - | 0.5.17 |
| today-checked-bg-color | 今日已打卡背景色 | String | var(--u-type-success) | - | 0.5.17 |
| unchecked-bg-color | 未打卡日期背景色 | String | var(--u-light-color) | - | 0.5.17 |
| unchecked-color | 未打卡日期字体颜色 | String | var(--u-white-color) | - | 0.5.17 |
| holidays | 节假日列表，格式：['2024-01-01', '2024-01-02'] | Array | [] | - | 0.5.17 |
| workdays | 加班日列表，格式：['2024-01-06', '2024-01-07'] | Array | [] | - | 0.5.17 |
| holiday-color | 节假日文字颜色 | String | var(--u-type-error) | - | 0.5.17 |
| workday-color | 加班日文字颜色 | String | var(--u-type-primary) | - | 0.5.17 |
| show-festival | 是否显示内置节日（中国传统节日） | Boolean | false | true | 0.5.17 |
| festivals | 自定义节日配置，格式：{ '04-04': '清明节' }，支持 `MM-DD` 和 `YYYY-MM-DD` 两种格式 | Object | {} | - | 0.5.17 |
| festival-color | 节日文字颜色 | String | var(--u-type-primary) | - | 0.5.17 |
| use-date-slot | 是否启用自定义日期内容插槽 | Boolean | false | true | 0.5.17 |


### Slots

| 名称 | 说明 | 版本 |
| :- | :- | :- |
| tooltip | 自定义日历顶部的内容 | - |
| date | 自定义日期内容，作用域参数见[自定义日期内容](#自定义日期内容-价格日历) | 0.5.17 |


### Events

| 事件名 | 说明 | 回调参数 |
| :- | :- | :- |
| change | 点击右上角`确定`按钮时触发（弹窗模式）/ 选择日期时触发（页面模式） | 选择日期相关的返回参数 |

<ArticleRecommend :articleLinks="['https://mp.weixin.qq.com/s/Y6pYLiEusiBv5POxcQb4VA']" />
