# DateStrip 日期条


## 组件概况

DateStrip 日期条组件是一个用于快速选择日期的轻量级横向日期选择器。组件以水平条状方式展示日期，支持周模式（通过 Swiper 滑动切换每周）和平铺模式（通过 ScrollView 横向滚动查看全部日期）。组件支持农历显示、日期禁用、高亮模式切换、自定义样式等功能，适用于需要快速选择单个日期的场景，如日程表、排班系统、预约管理等。

## 核心功能描述

- **周模式**：通过 Swiper 左右滑动切换每周，每周展示 7 天（星期日至星期六），支持自定义周起始日
- **平铺模式**：通过 ScrollView 横向滚动展示日期，一次性展示指定月份范围内的所有日期
- **农历显示**：通过 `show-lunar` 属性在日期下方显示农历信息
- **日期范围限制**：通过 `min-date` 和 `max-date` 限制可选日期范围，默认范围为当前日期前后各一个月
- **自定义禁用日期**：支持通过 `disabled-date` 数组或 `disabled-fun` 函数动态禁用特定日期
- **高亮模式切换**：通过 `active-mode` 控制选中项的高亮样式，支持 `both`（星期和日期同时高亮）、`date`（仅日期高亮）、`text`（仅文本高亮）
- **自定义样式**：支持自定义组件背景色（`bg-color`）、高度（`height`）、圆角（`round`）、每个日期格的宽度（`item-width`）、圆角（`item-round`）、选中框背景色（`active-bg-color`）和选中文字颜色（`active-color`）
- **自定义激活样式**：通过 `active-style` 传入自定义对象，覆盖选中项的默认样式
- **数字补零**：通过 `pad-zero` 控制小于 10 的日期数字是否补零显示
- **自定义格式化**：支持通过 `formatter` 函数自定义每个日期项的数据展示
- **小程序 ref 格式化函数**：在微信小程序中，由于不支持将函数作为 props 传递，组件暴露了 `setFormatter` 方法用于设置格式化函数

## 适用业务场景

- **日程安排**：在日程表中快速选择某一天进行日程查看或编辑
- **排班管理**：在排班系统中选择具体日期查看或排班
- **预约管理**：在预约场景中让用户快速选择预约日期
- **考勤打卡**：在考勤场景中选择日期查看打卡记录
- **日报周报**：选择具体日期撰写日报或查看日报内容
- **天气查询**：在天气应用中选择日期查看历史或未来天气
- **账单查看**：选择日期查看对应日期的收支明细

## API

### DateStrip Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | number | 0 | 否 | 选中的值，为 13 位时间戳 |
| defaultDate | string / number | '' | 否 | 默认选中的日期 |
| mode | string | 'week' | 否 | 切换模式，可选值：`none`（平铺模式）、`week`（按周切换） |
| minDate | number | 0 | 否 | 可选择的最小日期（时间戳），为 0 时使用默认范围 |
| maxDate | number | 0 | 否 | 可选择的最大日期（时间戳），为 0 时使用默认范围 |
| height | string | '55px' | 否 | 组件高度 |
| itemWidth | string | '50px' | 否 | 每格日期宽度 |
| itemRound | string | '6px' | 否 | 每格日期圆角 |
| activeBgColor | string | '#3c9cff' | 否 | 选中框背景色 |
| activeColor | string | '#ffffff' | 否 | 选中框文本颜色 |
| activeStyle | object | {} | 否 | 选中框自定义样式 |
| bgColor | string | '' | 否 | 横条背景色 |
| round | string | '' | 否 | 选中框圆角 |
| firstDayOfWeek | number | 0 | 否 | 第一天从星期几开始，默认 0 = 周日 |
| activeMode | string | 'both' | 否 | 高亮模式，可选值：`both`（星期和日期同时高亮）、`date`（只高亮日期）、`text`（只高亮文本） |
| formatter | Function / null | null | 否 | 日期格式化函数 |
| monthNum | number / string | 1 | 否 | 最多展示月份数量 |
| disabledFun | Function / null | null | 否 | 禁止选择的日期函数，返回 `[boolean, string]` 或 `boolean` |
| disabledDate | Array / string / null | null | 否 | 禁止选择的日期，支持字符串或字符串数组 |
| disabledColor | string | '#c8c9cc' | 否 | 禁用日期的文字颜色 |
| showLunar | boolean | false | 否 | 是否显示农历 |
| padZero | boolean | false | 否 | 是否对小于 10 的数字补 0 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### DateStrip Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 选择日期时触发 | `{ weekday: string, date: string \| number, timestamp: number, lunar?: any }` | `weekday` 为星期几，`date` 为日期数字，`timestamp` 为 13 位时间戳，`lunar` 为农历信息 |
| update:value | 选中值变化时触发（v-model 内部使用） | `(value: number)` | 值为选中日期的 13 位时间戳 |

### DateStrip Methods

通过 ref 可以获取 `wd-date-strip` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| setFormatter | `(formatter: (value: any) => any)` | void | 设置日期格式化函数，用于微信小程序等不支持函数 props 的平台 |

## 使用示例

### 示例一：基础用法

使用默认的周模式展示日期条，通过 `v-model` 绑定选中的日期时间戳。

```vue
<template>
  <wd-date-strip v-model="value1" @change="onChange" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const value1 = ref<number>(dayjs().valueOf())

const onChange = (item: { weekday: string; date: string | number; timestamp: number }) => {
  console.log('选中日期:', item.timestamp)
}
</script>
```

### 示例二：自定义样式与高亮模式

自定义日期条的外观样式和高亮模式，实现不同视觉效果的日期选择。

```vue
<template>
  <!-- 自定义背景与选中框颜色 -->
  <wd-date-strip
    v-model="value7"
    bg-color="#f5f5f5"
    active-bg-color="#ff6b35"
    active-color="#fff"
    round="10px"
  />

  <!-- 圆形选中框 -->
  <wd-date-strip
    v-model="value5"
    active-mode="date"
    height="80px"
    item-width="45px"
    item-round="100px"
  />

  <!-- 文本高亮模式 -->
  <wd-date-strip
    v-model="value6"
    active-mode="text"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const value5 = ref<number>(dayjs().valueOf())
const value6 = ref<number>(dayjs().valueOf())
const value7 = ref<number>(dayjs().valueOf())
</script>
```

### 示例三：平铺模式与日期范围限制

使用平铺模式展示日期，并限制可选日期范围，适用于近期日期选择场景。

```vue
<template>
  <!-- 平铺模式 -->
  <wd-date-strip
    v-model="value3"
    mode="none"
    :min-date="minDate"
    :max-date="maxDate"
  />

  <!-- 限制在最近 7 天 -->
  <wd-date-strip
    v-model="value9"
    :min-date="todayTime"
    :max-date="maxDateLimit"
    mode="none"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const value3 = ref<number>(dayjs().valueOf())
const value9 = ref<number>(dayjs().valueOf())

const minDate = ref<number>(dayjs('2025-06-01').valueOf())
const maxDate = ref<number>(dayjs('2025-10-01').valueOf())
const todayTime = ref<number>(dayjs().valueOf())
const maxDateLimit = ref<number>(dayjs().add(6, 'day').valueOf())
</script>
```

### 示例四：禁用特定日期与农历显示

通过数组或函数禁用特定日期，并展示农历信息。

```vue
<template>
  <!-- 显示农历 -->
  <wd-date-strip
    v-model="value11"
    :show-lunar="true"
    height="70px"
  />

  <!-- 数字补零 -->
  <wd-date-strip
    v-model="value12"
    :pad-zero="true"
    mode="none"
  />

  <!-- 禁用特定日期 -->
  <wd-date-strip
    v-model="value10"
    @change="onChange"
    :disabled-date="disabledDates"
    :disabled-fun="disabledFun"
    mode="none"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

type DisabledResult = [boolean, string] | boolean

const value10 = ref<number>(dayjs().valueOf())
const value11 = ref<number>(dayjs().valueOf())
const value12 = ref<number>(dayjs().valueOf())

const disabledDates = ref<string[]>(['2025-08-09', '2025-08-10', '2025-08-15'])

const disabledFun = (day: { weekday: string }): DisabledResult => {
  if (day.weekday === '二') {
    return [true, '星期二']
  }
  return false
}

const onChange = (item: { timestamp: number }) => {
  console.log('选中日期:', item.timestamp)
}
</script>
```

## 注意事项

- **时间戳精度**：`modelValue` 和事件回调中的 `timestamp` 均为毫秒级时间戳（13 位），使用 `dayjs().valueOf()` 或 `Date.now()` 获取
- **默认日期范围**：未设置 `min-date` 和 `max-date` 时，默认范围为当前日期前后各 1 个月（由 `month-num` 控制）
- **周模式与平铺模式的区别**：周模式使用 Swiper 组件，每次展示一周（7 天），通过左右滑动切换；平铺模式使用 ScrollView，所有日期水平排列，通过横向滚动查看
- **高亮模式**：`active-mode` 为 `both` 时，星期和日期都会显示选中框背景色；为 `date` 时，只有日期数字所在的区域显示背景色；为 `text` 时，不显示背景色，但文字颜色变为选中色
- **禁用日期返回格式**：`disabled-fun` 函数可以返回 `boolean`（仅禁用）或 `[boolean, string]`（禁用并显示底部说明文字），例如 `[true, '星期二']` 会在日期下方显示"星期二"
- **小程序格式化函数**：在微信小程序中，由于不支持将函数作为 props 传递，需要通过 `ref` 调用组件的 `setFormatter` 方法来设置格式化函数
- **农历信息**：开启 `show-lunar` 后，组件使用内置的农历转换算法计算农历日期并展示
- **数字补零**：`pad-zero` 为 `true` 时，1~9 的日期会显示为 `01`~`09`，适用于需要对齐的场景
- **active-style 覆盖行为**：`active-style` 中的样式会覆盖组件默认的选中项样式，建议只设置需要自定义的属性
