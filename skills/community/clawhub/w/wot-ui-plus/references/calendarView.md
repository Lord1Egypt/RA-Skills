# CalendarView 日历视图


## 组件概况

### 组件概述
CalendarView 日历视图组件是一个功能强大的日历展示和选择组件，支持多种日历类型和视图模式。它提供了灵活的配置选项，允许开发者根据不同业务需求定制日历的外观和行为，支持从简单的日期选择到复杂的日期范围选择等多种场景。

### 详细功能描述
- 支持多种日历类型：日期单选、日期多选、日期时间、周选择、月选择以及各种范围选择
- 提供月视图和年视图两种面板，根据选择类型自动切换
- 支持农历日期显示
- 支持自定义日期格式化和样式
- 支持日期范围限制
- 支持时间选择过滤
- 支持自定义面板高度
- 提供滚动到可视区域的方法
- 支持范围选择的最大天数限制
- 支持自定义周起始日
- 支持显示/隐藏秒选择
- 支持立即触发change事件

### 适用业务场景
- 预约系统中的日期时间选择
- 考勤系统中的排班日期选择
- 报表系统中的日期范围筛选
- 活动报名中的日期选择
- 日历应用中的日期查看和标记
- 酒店预订系统中的入住离店日期选择
- 会议系统中的会议时间选择

## 完整API参考

### Props属性

| 名称 | 类型 | 默认值 | 必填 | 描述 |
|------|------|--------|------|------|
| modelValue | number \| number[] \| null | - | 是 | 选中值，单选时为时间戳，多选或范围选择时为时间戳数组 |
| type | string | date | 否 | 日历类型，可选值：date、dates、datetime、week、month、daterange、datetimerange、weekrange、monthrange |
| minDate | number | 当前日期往前12个月 | 否 | 最小可选日期，时间戳 |
| maxDate | number | 当前日期往后12个月 | 否 | 最大可选日期，时间戳 |
| firstDayOfWeek | number | 1 | 否 | 周起始天，0表示周日，1-6表示周一至周六 |
| showLunar | boolean | true | 否 | 是否显示农历日期 |
| showMark | boolean | true | 否 | 是否显示月份背景 |
| formatter | function | - | 否 | 日期格式化函数，用于自定义日期项的显示和样式 |
| maxRange | number | - | 否 | 最大日期范围，type为范围选择时有效 |
| rangePrompt | string | - | 否 | 范围超出提示文案 |
| allowSameDay | boolean | false | 否 | 是否允许选择同一天，type为范围选择时有效 |
| showPanelTitle | boolean | true | 否 | 是否展示面板标题 |
| defaultTime | string \| string[] | 00:00:00 | 否 | 选中日期的具体时刻，单选时为字符串，范围选择时为数组 |
| panelHeight | number | 378 | 否 | 可滚动面板的高度 |
| timeFilter | function | - | 否 | 时间选择器过滤器，用于过滤时间选择器的可选数据 |
| hideSecond | boolean | false | 否 | 是否隐藏秒修改 |
| immediateChange | boolean | false | 否 | 是否立即触发change事件，仅微信小程序和支付宝小程序支持 |
| customStyle | string | - | 否 | 自定义根节点样式 |
| customClass | string | - | 否 | 自定义根节点样式类 |

### Events事件

| 事件名 | 触发条件 | 参数说明 |
|--------|----------|----------|
| change | 选中值发生变化时 | { value: number \| number[] \| null } - 选中的值 |
| pickstart | 开始选择范围时 | 无 |
| pickend | 结束选择范围时 | 无 |

### Methods方法

| 方法名 | 参数 | 返回值 | 功能说明 |
|--------|------|--------|----------|
| scrollIntoView | 无 | 无 | 使当前日期或者选中日期滚动到可视区域 |

### Slots插槽

该组件没有定义任何插槽。

## 多场景使用示例代码

### 1. 基础日期选择

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">基础日期选择</view>
    <wd-calendar-view v-model="date" type="date" />
    <view class="demo-result">选中日期：{{ formatDate(date) }}</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 基础日期选择
const date = ref<number | null>(dayjs().valueOf())

// 格式化日期
const formatDate = (timestamp: number | null) => {
  if (!timestamp) return ''
  return dayjs(timestamp).format('YYYY-MM-DD')
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
```

### 2. 日期范围选择

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">日期范围选择</view>
    <wd-calendar-view 
      v-model="dateRange" 
      type="daterange" 
      :max-range="7"
      range-prompt="最多选择7天"
      allow-same-day
    />
    <view class="demo-result">
      开始日期：{{ formatDate(dateRange?.[0]) }}<br>
      结束日期：{{ formatDate(dateRange?.[1]) }}
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 日期范围选择
const dateRange = ref<number[] | null>([
  dayjs().valueOf(),
  dayjs().add(3, 'day').valueOf()
])

// 格式化日期
const formatDate = (timestamp: number | undefined) => {
  if (!timestamp) return ''
  return dayjs(timestamp).format('YYYY-MM-DD')
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
  line-height: 48rpx;
}
</style>
```

### 3. 日期时间选择

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">日期时间选择</view>
    <wd-calendar-view 
      v-model="datetime" 
      type="datetime" 
      :hide-second="true"
      default-time="14:30:00"
    />
    <view class="demo-result">选中日期时间：{{ formatDatetime(datetime) }}</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 日期时间选择
const datetime = ref<number | null>(dayjs().valueOf())

// 格式化日期时间
const formatDatetime = (timestamp: number | null) => {
  if (!timestamp) return ''
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
```

### 4. 月份选择

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">月份选择</view>
    <wd-calendar-view v-model="month" type="month" />
    <view class="demo-result">选中月份：{{ formatMonth(month) }}</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 月份选择
const month = ref<number | null>(dayjs().valueOf())

// 格式化月份
const formatMonth = (timestamp: number | null) => {
  if (!timestamp) return ''
  return dayjs(timestamp).format('YYYY-MM')
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
```

### 5. 自定义日期格式化

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">自定义日期格式化</view>
    <wd-calendar-view 
      v-model="date" 
      type="date" 
      :formatter="formatter"
    />
    <view class="demo-result">选中日期：{{ formatDate(date) }}</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 自定义日期格式化
const date = ref<number | null>(dayjs().valueOf())

// 格式化日期
const formatDate = (timestamp: number | null) => {
  if (!timestamp) return ''
  return dayjs(timestamp).format('YYYY-MM-DD')
}

// 自定义日期项格式化函数
const formatter = (day: any) => {
  // 标记今天
  if (dayjs(day.date).format('YYYY-MM-DD') === dayjs().format('YYYY-MM-DD')) {
    day.topInfo = '今天'
    day.topColor = '#ff4d4f'
  }
  
  // 标记周末
  const dayOfWeek = dayjs(day.date).day()
  if (dayOfWeek === 0 || dayOfWeek === 6) {
    day.bottomColor = '#1890ff'
  }
  
  // 禁用特定日期
  if (dayjs(day.date).format('YYYY-MM-DD') === '2025-12-25') {
    day.disabled = true
    day.bottomInfo = '不可选'
    day.bottomColor = '#ff4d4f'
  }
  
  return day
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}
</style>
```

### 6. 多日期选择

```vue
<template>
  <view class="calendar-view-demo">
    <view class="demo-title">多日期选择</view>
    <wd-calendar-view v-model="dates" type="dates" />
    <view class="demo-result">
      <view>选中日期：</view>
      <view v-for="(date, index) in dates" :key="index" class="date-item">
        {{ formatDate(date) }}
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

// 多日期选择
const dates = ref<number[] | null>([
  dayjs().valueOf(),
  dayjs().add(1, 'day').valueOf(),
  dayjs().add(3, 'day').valueOf()
])

// 格式化日期
const formatDate = (timestamp: number) => {
  return dayjs(timestamp).format('YYYY-MM-DD')
}
</script>

<style scoped>
.calendar-view-demo {
  padding: 20rpx;
}

.demo-title {
  font-size: 28rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.demo-result {
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}

.date-item {
  margin-top: 10rpx;
  padding: 10rpx;
  background-color: #f0f0f0;
  border-radius: 4rpx;
  display: inline-block;
  margin-right: 10rpx;
  margin-bottom: 10rpx;
}
</style>
```

## 样式定制指南

### 1. 使用customStyle自定义样式

```vue
<template>
  <wd-calendar-view 
    v-model="date" 
    type="date" 
    customStyle="background-color: #f5f7fa; border-radius: 12rpx; padding: 20rpx;"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const date = ref<number | null>(dayjs().valueOf())
</script>
```

### 2. 使用customClass自定义类名

```vue
<template>
  <wd-calendar-view 
    v-model="date" 
    type="date" 
    customClass="my-calendar-view"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const date = ref<number | null>(dayjs().valueOf())
</script>

<style scoped>
/* 注意：需要使用 ::v-deep 或 /deep/ 穿透 scoped 样式 */
:deep(.my-calendar-view) {
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8rpx;
  padding: 10rpx;
}

:deep(.my-calendar-view .wd-calendar-view__title) {
  color: #0284c7;
  font-weight: bold;
}
</style>
```

### 3. 自定义面板高度

```vue
<template>
  <wd-calendar-view 
    v-model="date" 
    type="date" 
    :panel-height="500"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import dayjs from 'dayjs'

const date = ref<number | null>(dayjs().valueOf())
</script>
```

## 注意事项

1. **类型选择**：根据业务需求选择合适的calendar type，不同类型对应不同的选择模式和UI展示

2. **日期格式**：组件内部使用13位时间戳，外部使用时需要注意时间格式转换

3. **范围选择**：使用range类型时，可以通过maxRange属性限制最大选择范围，并通过rangePrompt设置超出范围的提示信息

4. **自定义格式化**：formatter函数可以自定义日期项的显示，包括顶部信息、底部信息、颜色等

5. **月份视图和年份视图**：根据type属性自动切换，month和monthrange类型使用年份视图，其他类型使用月份视图

6. **时间选择**：datetime和datetimerange类型支持时间选择，可以通过hideSecond属性隐藏秒选择，通过defaultTime设置默认时间

7. **滚动定位**：可以通过scrollIntoView方法将当前日期或选中日期滚动到可视区域

8. **性能优化**：对于大量日期数据的场景，建议合理设置minDate和maxDate，避免渲染过多日期

9. **周起始日**：可以通过firstDayOfWeek属性设置周起始日，默认为周一（1）

10. **农历显示**：可以通过showLunar属性控制是否显示农历日期，默认为true

11. **立即触发change事件**：immediateChange属性仅在微信小程序和支付宝小程序中生效

12. **双向绑定**：使用v-model指令可以实现数据的双向绑定，简化状态管理

13. **事件监听**：可以监听change、pickstart和pickend事件，实现复杂的交互逻辑

14. **组件实例**：通过ref可以获取组件实例，调用scrollIntoView方法

15. **样式定制**：可以通过customStyle和customClass属性自定义组件样式，需要注意使用::v-deep或/deep/穿透scoped样式

16. **跨端兼容**：组件在iOS、Android、H5和主流小程序平台上都能正常工作，无需特殊处理

17. **类型安全**：组件使用TypeScript开发，提供了完整的类型定义，使用时可以获得良好的类型提示