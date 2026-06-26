# Calendar 日历


## 组件概况

Calendar 日历组件用于选择日期、日期范围、周、月等多种时间维度。该组件由 `wd-calendar`（弹窗选择器）和 `wd-calendar-view`（内联选择器视图）两个关联组件组成。`wd-calendar` 以弹窗形式呈现日历选择面板，支持单选、多选、范围选择等模式；`wd-calendar-view` 直接嵌入页面中使用，实时响应选择变化。组件支持九种日期类型、农历显示、日期格式化、快捷选项、确认前校验等高级功能，广泛应用于预约下单、行程管理、筛选过滤等场景。

## 核心功能描述

- **九种日期类型**：支持 `date`（单选日期）、`dates`（多选日期）、`datetime`（单选日期时间）、`week`（单选周）、`month`（单选月）、`daterange`（日期范围）、`datetimerange`（日期时间范围）、`weekrange`（周范围）、`monthrange`（月范围）
- **类型切换**：通过 `show-type-switch` 属性开启面板内的日/周/月切换功能，支持单日模式（date/week/month）和范围模式（daterange/weekrange/monthrange）间切换
- **范围限制**：通过 `min-date` 和 `max-date` 属性限制可选日期范围，默认范围为当前日期前后各12个月
- **最大范围控制**：通过 `max-range` 属性限制范围选择时的最大天数
- **周起始日自定义**：通过 `first-day-of-week` 属性设置每周起始日（0为周日，1-6为周一至周六）
- **日期格式化**：通过 `formatter` 函数自定义每个日期项的显示内容，支持设置顶部信息、底部信息、颜色、禁用状态等
- **时间精度选择**：`datetime` 和 `datetimerange` 类型支持精确到时分秒的选择，可通过 `hide-second` 隐藏秒选择，通过 `time-filter` 过滤时间选项
- **默认时刻设置**：通过 `default-time` 为选中日期设置默认的时分秒
- **展示文案自定义**：通过 `display-format` 函数自定义单元格中展示的日期文案格式
- **范围面板内部回显**：通过 `inner-display-format` 自定义范围选择时面板内部的日期回显格式
- **快捷选项**：通过 `shortcuts` 和 `on-shortcuts-click` 属性设置快捷日期选项
- **确认前校验**：通过 `before-confirm` 函数在确认前执行异步校验
- **农历显示**：`wd-calendar-view` 支持通过 `show-lunar` 属性显示农历日期
- **月份背景标记**：通过 `show-mark` 属性控制是否显示月份背景标记
- **可清空**：通过 `clearable` 属性显示清除按钮，一键清空已选值
- **表单集成**：支持表单校验功能，通过 `prop` 和 `rules` 属性与 `wd-form` 组件配合使用
- **自定义触发元素**：支持通过默认插槽自定义触发选择器的元素，替代内置的 wd-cell 单元格

## 适用业务场景

- **预约下单**：在预约服务、餐厅预订等场景中让用户选择日期或日期时间
- **行程管理**：在差旅预订、日程安排等场景中选择起止日期
- **筛选过滤**：在订单列表、日志查询等场景中按日期区间进行筛选
- **周报月报**：按周或按月选择，用于生成周报、月报
- **请假申请**：选择请假的起止日期，支持最大天数限制
- **活动时间配置**：在活动配置中设置活动的开始和结束时间
- **嵌入式日期选择**：`wd-calendar-view` 适用于需要在页面中常驻显示日历选择器的场景
- **快捷日期选择**：通过快捷选项快速选择近7天、近30天等常用日期范围

## API

### wd-calendar Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | number / number[] / null | - | 是 | 选中值，为13位时间戳（单选）或时间戳数组（多选或范围选择）或 null（未选择） |
| type | string | 'date' | 否 | 日期类型，可选值：`date`、`dates`、`datetime`、`week`、`month`、`daterange`、`datetimerange`、`weekrange`、`monthrange` |
| minDate | number | 当前日期往前推12个月的当天开始时间 | 否 | 最小可选日期，为13位时间戳 |
| maxDate | number | 当前日期往后推12个月的当月结束时间 | 否 | 最大可选日期，为13位时间戳 |
| firstDayOfWeek | number | 0 | 否 | 周起始天，0表示周日，1-6表示周一至周六 |
| formatter | Function | 无 | 否 | 日期项格式化函数，用于自定义每个日期项的显示内容，详见 CalendarFormatter 类型 |
| maxRange | number | 无 | 否 | 最大日期范围天数，type 为范围选择时有效 |
| rangePrompt | string | 无 | 否 | 选择超出最大日期范围时的错误提示文案 |
| allowSameDay | boolean | false | 否 | 是否允许范围选择时选择同一天 |
| defaultTime | string / string[] | 无 | 否 | 选中日期所使用的当日内具体时刻，单选为字符串，范围选择为字符串数组（起止时间） |
| timeFilter | Function | 无 | 否 | 时间过滤器函数，type 为 'datetime' 或 'datetimerange' 时有效，用于过滤时间选择器的可选值，详见 CalendarTimeFilter 类型 |
| hideSecond | boolean | false | 否 | 是否不展示秒选择，type 为 'datetime' 或 'datetimerange' 时有效 |
| label | string | '' | 否 | 选择器左侧文案（表单项标签） |
| labelWidth | string | '33%' | 否 | 左侧标题宽度 |
| disabled | boolean | false | 否 | 是否禁用选择器 |
| readonly | boolean | false | 否 | 是否只读 |
| placeholder | string | 请选择 | 否 | 选择器占位符文案，未设置时跟随国际化配置 |
| title | string | 请选择日期 | 否 | 弹出层标题 |
| alignRight | boolean | false | 否 | 选中值是否靠右展示 |
| error | boolean | false | 否 | 是否显示为错误状态，错误状态下内容显示为红色 |
| required | boolean | false | 否 | 是否显示必填标记（星号） |
| size | string | '' | 否 | 组件尺寸，可选值：`large` |
| center | boolean | false | 否 | 是否垂直居中 |
| closeOnClickModal | boolean | true | 否 | 点击遮罩层是否关闭弹窗 |
| zIndex | number | 15 | 否 | 弹框层级 |
| showConfirm | boolean | true | 否 | 是否显示确定按钮 |
| confirmText | string | 确认 | 否 | 确定按钮文字，未设置时跟随国际化配置 |
| displayFormat | Function | 默认格式化函数 | 否 | 自定义展示文案的格式化函数，签名为 `(value: number \| number[], type: CalendarType) => string` |
| innerDisplayFormat | Function | 无 | 否 | 自定义范围选择面板内部回显的格式化函数，签名为 `(value: number, rangeType: 'start' \| 'end', type: CalendarType) => string` |
| ellipsis | boolean | false | 否 | 文本溢出时是否显示省略号 |
| showTypeSwitch | boolean | false | 否 | 是否显示类型切换功能（日/周/月切换） |
| shortcuts | Array\<Record\<string, any\>\> | [] | 否 | 快捷选项数组，每项需包含 text 字段 |
| onShortcutsClick | Function | 无 | 否 | 快捷选项点击回调函数，签名为 `(option: { item: Record\<string, any\>, index: number }) => number \| number[]`，需返回选中的日期值 |
| safeAreaInsetBottom | boolean | true | 否 | 是否在底部安全区域内显示（适配 iPhone X 等全面屏机型） |
| beforeConfirm | Function | 无 | 否 | 确认前校验函数，签名为 `(option: { value: number \| number[] \| null, resolve: (isPass: boolean) => void }) => void` |
| prop | string | '' | 否 | 表单域 model 字段名，使用表单校验时必填 |
| rules | Array\<FormItemRule\> | [] | 否 | 表单验证规则，结合 wd-form 组件使用 |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发 change 事件，仅微信小程序和支付宝小程序支持 |
| withCell | boolean | true | 否 | 是否使用内置单元格。默认为 true，使用内置 wd-cell；设为 false 时可配合默认插槽自定义触发元素 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 定位失效问题 |
| markerSide | string | 'before' | 否 | 必填标记位置，可选值：`before`（左侧）、`after`（右侧） |
| clearable | boolean | false | 否 | 是否显示清除按钮 |
| customViewClass | string | '' | 否 | 自定义内部日历视图区域的样式类名 |
| customLabelClass | string | '' | 否 | 自定义 label 区域的样式类名 |
| customValueClass | string | '' | 否 | 自定义 value 显示区域的样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-calendar-view Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | number / number[] / null | - | 是 | 选中值，为13位时间戳（单选）或时间戳数组（多选或范围选择）或 null（未选择） |
| type | string | 'date' | 否 | 日期类型，可选值与 wd-calendar 相同 |
| minDate | number | 当前日期往前推12个月的当天开始时间 | 否 | 最小可选日期，为13位时间戳 |
| maxDate | number | 当前日期往后推12个月的当月结束时间 | 否 | 最大可选日期，为13位时间戳 |
| firstDayOfWeek | number | 1 | 否 | 周起始天，0表示周日，1-6表示周一至周六 |
| formatter | Function | 无 | 否 | 日期项格式化函数，详见 CalendarFormatter 类型 |
| maxRange | number | 无 | 否 | 最大日期范围天数 |
| rangePrompt | string | 无 | 否 | 范围超出提示文案 |
| allowSameDay | boolean | false | 否 | 是否允许选择同一天 |
| showPanelTitle | boolean | true | 否 | 是否显示面板标题（月份标题） |
| defaultTime | string / string[] | '00:00:00' | 否 | 选中日期的具体时刻 |
| panelHeight | number | 378 | 否 | 可滚动面板的高度，单位为 px |
| timeFilter | Function | 无 | 否 | 时间过滤器函数 |
| hideSecond | boolean | false | 否 | 是否隐藏秒选择 |
| immediateChange | boolean | false | 否 | 是否立即触发 change 事件，仅微信小程序和支付宝小程序支持 |
| showLunar | boolean | true | 否 | 是否显示农历 |
| showMark | boolean | true | 否 | 是否显示月份背景标记 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-calendar Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| confirm | 点击确认按钮并完成校验后触发 | `(data: { value: number \| number[] \| null, type: CalendarType })` | `value` 为选中值，`type` 为当前日期类型 |
| cancel | 点击取消按钮或点击遮罩关闭弹窗时触发 | 无 | - |
| open | 弹窗打开时触发 | 无 | - |
| change | 滚动选中项变化时触发 | `(data: { value: number \| number[] \| null })` | `value` 为当前变化的选中值 |
| clear | 点击清除按钮清空选中值时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: number \| number[] \| null)` | 值为确认后的新选中值 |

### wd-calendar-view Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 选中值变化时触发 | `(data: { value: number \| number[] \| null })` | `value` 为更新后的选中值 |
| pickstart | 手指开始触摸滚动时触发 | 无 | - |
| pickend | 手指结束触摸滚动时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: number \| number[] \| null)` | 值为变化后的新选中值 |

### wd-calendar Methods

通过 ref 可以获取 `wd-calendar` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| open | 无 | void | 打开日历选择器弹窗 |
| close | 无 | void | 关闭日历选择器弹窗 |

### wd-calendar-view Methods

通过 ref 可以获取 `wd-calendar-view` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| scrollIntoView | 无 | void | 将当前日期或选中日期滚动到可视区域 |

### wd-calendar Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义触发选择器的元素，需设置 `with-cell` 为 false |
| label | - | 自定义左侧标签区域内容 |
| confirm-left | - | 自定义确认按钮左侧的额外内容 |
| confirm-right | - | 自定义确认按钮右侧的额外内容 |

### wd-calendar-view Slots

`wd-calendar-view` 不提供自定义插槽。

## 使用示例

### 示例一：基础日期选择

最常用的日历选择器用法，支持多种 type 类型切换。

```vue
<template>
  <wd-cell-group border>
    <!-- 单个日期选择 -->
    <wd-calendar
      label="单个日期选择"
      v-model="value1"
      @confirm="handleConfirm"
    />

    <!-- 多个日期选择 -->
    <wd-calendar
      label="多个日期选择"
      type="dates"
      v-model="value2"
      @confirm="handleConfirm"
    />

    <!-- 日期范围选择 -->
    <wd-calendar
      label="日期范围选择"
      type="daterange"
      v-model="value3"
    />

    <!-- 日期时间选择（精确到秒） -->
    <wd-calendar
      label="日期时间选择"
      type="datetime"
      v-model="value4"
    />

    <!-- 日期时间范围选择 -->
    <wd-calendar
      label="日期时间范围选择"
      type="datetimerange"
      v-model="value5"
    />

    <!-- 周选择 -->
    <wd-calendar
      label="周选择"
      type="week"
      v-model="value6"
    />

    <!-- 月选择 -->
    <wd-calendar
      label="月选择"
      type="month"
      :min-date="minDate"
      v-model="value7"
    />

    <!-- 周范围选择（设置周一起始） -->
    <wd-calendar
      label="周范围选择"
      type="weekrange"
      :first-day-of-week="1"
      v-model="value8"
    />

    <!-- 月范围选择 -->
    <wd-calendar
      label="月范围选择"
      type="monthrange"
      v-model="value9"
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const now = new Date()
const minDate = ref<number>(new Date(now.getFullYear() - 20, now.getMonth() - 6, now.getDate()).getTime())

const value1 = ref<number>(Date.now())
const value2 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now()])
const value3 = ref<number[]>([])
const value4 = ref<number>(Date.now())
const value5 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now() - 24 * 60 * 60 * 1000])
const value6 = ref<number>(Date.now())
const value7 = ref<number>(Date.now())
const value8 = ref<number[]>([Date.now() - 14 * 24 * 60 * 60 * 1000, Date.now()])
const value9 = ref<number[]>([Date.now() - 33 * 24 * 60 * 60 * 1000, Date.now()])

function handleConfirm({ value }: any) {
  console.log('选中值:', value)
}
</script>
```

### 示例二：自定义日期格式与快捷选项

通过 `formatter` 函数自定义日历面板中每个日期项的显示内容，通过 `shortcuts` 设置快捷选项，通过 `display-format` 自定义单元格展示文案。

```vue
<template>
  <wd-cell-group border>
    <!-- 日期格式化：标记特殊日期 -->
    <wd-calendar
      label="日期格式化"
      type="daterange"
      v-model="value1"
      :formatter="formatter"
    />

    <!-- 快捷选项：快速选择近N天 -->
    <wd-calendar
      label="快捷选项"
      type="daterange"
      v-model="value2"
      :shortcuts="shortcuts"
      :on-shortcuts-click="onShortcutsClick"
      @confirm="handleConfirm"
    />

    <!-- 自定义展示文案格式 -->
    <wd-calendar
      label="自定义展示"
      type="daterange"
      v-model="value3"
      :display-format="displayFormat"
      :inner-display-format="innerDisplayFormat"
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { dayjs } from '@/uni_modules/wot-ui-plus'
import type {
  CalendarDayItem,
  CalendarFormatter
} from '@/uni_modules/wot-ui-plus/components/wd-calendar-view/types'
import type { CalendarOnShortcutsClickOption } from '@/uni_modules/wot-ui-plus/components/wd-calendar/types'

const value1 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now()])
const value2 = ref<number[]>([])
const value3 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now()])

// 自定义日期项显示
const formatter: CalendarFormatter = (day: CalendarDayItem) => {
  const date = new Date(day.date)
  const now = new Date()

  const year = date.getFullYear()
  const month = date.getMonth()
  const da = date.getDate()
  const nowYear = now.getFullYear()
  const nowMonth = now.getMonth()
  const nowDa = now.getDate()

  // 标记今天
  if (year === nowYear && month === nowMonth && da === nowDa) {
    day.topInfo = '今天'
  }

  // 标记促销活动日
  if (month === 5 && da === 18) {
    day.topInfo = '618大促'
    day.topColor = '#f56c6c'
  }

  // 范围选择时标记开始和结束
  if (day.type === 'start') {
    day.bottomInfo = '开始'
  }
  if (day.type === 'end') {
    day.bottomInfo = '结束'
  }
  if (day.type === 'same') {
    day.bottomInfo = '开始/结束'
  }

  return day
}

// 快捷选项配置
const shortcuts = ref<Record<string, any>[]>([
  { text: '近7天', id: 7 },
  { text: '近15天', id: 15 },
  { text: '近30天', id: 30 }
])

// 快捷选项点击回调
const onShortcutsClick = ({ item }: CalendarOnShortcutsClickOption) => {
  const dayDiff = item.id
  const endDate = Date.now() - 24 * 60 * 60 * 1000
  const startDate = endDate - dayDiff * 24 * 60 * 60 * 1000
  return [startDate, endDate]
}

// 自定义单元格展示文案
const displayFormat = (value: any) => {
  return dayjs(value[0]).format('YYYY年MM月DD日') + ' - ' + dayjs(value[1]).format('YYYY年MM月DD日')
}

// 自定义范围面板内部回显
const innerDisplayFormat = (value: string | number | Date | undefined, rangeType: string) => {
  if (!value) {
    return rangeType === 'start' ? '活动开始时间' : '活动结束时间'
  }
  return dayjs(value).format('YYYY年MM月DD日')
}

function handleConfirm({ value }: any) {
  console.log('确认值:', value)
}
</script>
```

### 示例三：确认前校验、可清空与类型切换

通过 `before-confirm` 进行确认前校验，通过 `clearable` 实现可清空功能，通过 `show-type-switch` 实现日/周/月切换。

```vue
<template>
  <wd-cell-group border>
    <!-- 日/周/月切换 -->
    <wd-calendar
      label="日周月切换"
      :first-day-of-week="1"
      show-type-switch
      v-model="value1"
    />

    <!-- 确认前校验 -->
    <wd-calendar
      label="before-confirm"
      v-model="value2"
      :before-confirm="beforeConfirm"
    />

    <!-- 可清空的单选日期 -->
    <wd-calendar
      label="单个日期（可清空）"
      v-model="value3"
      clearable
      @clear="handleClear"
      @confirm="handleConfirm"
    />

    <!-- 可清空的日期范围 -->
    <wd-calendar
      label="日期范围（可清空）"
      type="daterange"
      v-model="value4"
      clearable
      @clear="handleRangeClear"
      @confirm="handleConfirm"
    />

    <!-- 必填星号在右侧 -->
    <wd-calendar
      label="必填星号在右"
      v-model="value5"
      required
      marker-side="after"
    />

    <!-- 确认按钮区域扩展 -->
    <wd-calendar
      label="拓展区域"
      v-model="value6"
    >
      <template #confirm-right>
        <wd-button
          block
          plain
          custom-style="margin-left: 10px;"
          @click="selectToday"
        >
          今天
        </wd-button>
      </template>
    </wd-calendar>
  </wd-cell-group>

  <wd-toast />
  <wd-message-box />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

const value1 = ref<number>(Date.now())
const value2 = ref<number | null>(null)
const value3 = ref<number | null>(Date.now())
const value4 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now()])
const value5 = ref<number>(Date.now())
const value6 = ref<number>(Date.now())

// 确认前校验：不允许选择未来日期
const beforeConfirm = ({ value, resolve }: any) => {
  if (value !== null && value !== undefined && (Array.isArray(value) ? value[0] : value) > Date.now()) {
    toast.error('该日期暂无数据')
    resolve(false)
  } else {
    resolve(true)
  }
}

function handleClear() {
  console.log('已清空')
}

function handleRangeClear() {
  console.log('区间已清空')
}

function handleConfirm({ value }: any) {
  toast.success('已选择: ' + new Date(value).toLocaleDateString())
}

function selectToday() {
  value6.value = Date.now()
}
</script>
```

### 示例四：自定义触发元素与组件实例调用

通过默认插槽自定义触发选择器的元素，通过 ref 调用组件的 open/close 方法。

```vue
<template>
  <!-- 自定义触发元素 -->
  <view style="margin: 0 15px">
    <view style="margin-bottom: 10px">当前选中日期：{{ formatValue }}</view>
    <wd-calendar v-model="value1" @confirm="handleConfirm">
      <wd-button>选择日期</wd-button>
    </wd-calendar>
  </view>

  <!-- 通过组件实例打开日历 -->
  <view style="margin: 16px 15px">
    <wd-button @click="openCalendar">打开日历</wd-button>
    <wd-calendar
      ref="calendarRef"
      v-model="value2"
      :with-cell="false"
      @confirm="handleConfirm2"
    />
  </view>

  <wd-toast />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { CalendarInstance } from '@/uni_modules/wot-ui-plus/components/wd-calendar/types'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()
const value1 = ref<number | null>(null)
const value2 = ref<number>(Date.now())
const formatValue = ref<string>('')
const calendarRef = ref<CalendarInstance>()

function handleConfirm({ value }: any) {
  formatValue.value = new Date(value).toString()
}

function handleConfirm2({ value }: any) {
  toast.success('已选择: ' + new Date(value).toLocaleDateString())
}

// 通过 ref 打开日历弹窗
function openCalendar() {
  calendarRef.value?.open()
}
</script>
```

### 示例五：内联日历选择器 wd-calendar-view

`wd-calendar-view` 直接嵌入页面中使用，无需弹窗，实时响应选择变化。

```vue
<template>
  <!-- 单个日期选择（支持类型切换） -->
  <view style="margin: 0 15px 10px">
    <view style="margin-bottom: 10px; font-size: 13px">切换类型：</view>
    <wd-radio-group v-model="type1" shape="button">
      <wd-radio value="date">date</wd-radio>
      <wd-radio value="week">week</wd-radio>
      <wd-radio value="month">month</wd-radio>
    </wd-radio-group>
  </view>
  <wd-calendar-view
    :type="type1"
    v-model="value1"
    @change="handleChange1"
  />

  <!-- 多个日期选择 -->
  <wd-calendar-view
    type="dates"
    v-model="value2"
    @change="handleChange2"
  />

  <!-- 日期范围选择（支持类型切换） -->
  <view style="margin: 0 15px 10px">
    <view style="margin-bottom: 10px; font-size: 13px">切换类型：</view>
    <wd-radio-group v-model="type2" shape="button">
      <wd-radio value="daterange">daterange</wd-radio>
      <wd-radio value="weekrange">weekrange</wd-radio>
      <wd-radio value="monthrange">monthrange</wd-radio>
    </wd-radio-group>
  </view>
  <wd-calendar-view
    :type="type2"
    allow-same-day
    v-model="value3"
    @change="handleChange3"
  />

  <!-- 日期时间类型（带时间过滤） -->
  <wd-calendar-view
    type="datetime"
    v-model="value4"
    :time-filter="timeFilter"
  />

  <!-- 日期时间范围类型 -->
  <wd-calendar-view
    type="datetimerange"
    v-model="value5"
  />

  <!-- 限制最大选择范围 -->
  <wd-calendar-view
    type="daterange"
    :max-range="3"
    v-model="value7"
  />

  <!-- 自定义日期显示 -->
  <wd-calendar-view
    type="daterange"
    allow-same-day
    v-model="value6"
    :formatter="formatter"
  />

  <!-- 设置周起始日为周一 -->
  <wd-calendar-view
    :first-day-of-week="1"
    v-model="value8"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { CalendarFormatter } from '@/uni_modules/wot-ui-plus/components/wd-calendar-view/types'

const type1 = ref<string>('date')
const type2 = ref<string>('daterange')
const value1 = ref<number>(Date.now())
const value2 = ref<number[] | null>(null)
const value3 = ref<number[]>([Date.now() - 33 * 24 * 60 * 60 * 1000, Date.now()])
const value4 = ref<number>(Date.now())
const value5 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now() - 24 * 60 * 60 * 1000])
const value6 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now() - 24 * 60 * 60 * 1000])
const value7 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now() - 24 * 60 * 60 * 1000])
const value8 = ref<number[]>([Date.now() - 3 * 24 * 60 * 60 * 1000, Date.now()])

// 时间过滤：分钟只展示整10分钟
const timeFilter = ({ type, values }: any) => {
  if (type === 'minute') {
    return values.filter((item: any) => item.value % 10 === 0)
  }
  return values
}

// 自定义日期项显示
const formatter: CalendarFormatter = (day) => {
  const date = new Date(day.date)
  const now = new Date()

  const year = date.getFullYear()
  const month = date.getMonth()
  const da = date.getDate()
  const nowYear = now.getFullYear()
  const nowMonth = now.getMonth()
  const nowDa = now.getDate()

  if (year === nowYear && month === nowMonth && da === nowDa) {
    day.topInfo = '今天'
  }

  if (month === 5 && da === 18) {
    day.topInfo = '618大促'
  }

  if (month === 10 && da === 11) {
    day.topInfo = '京东双11'
  }

  if (day.type === 'start') {
    day.bottomInfo = '开始'
  }
  if (day.type === 'end') {
    day.bottomInfo = '结束'
  }
  if (day.type === 'same') {
    day.bottomInfo = '开始/结束'
  }

  return day
}

function handleChange1({ value }: any) {
  console.log('单选变化:', value)
}

function handleChange2({ value }: any) {
  console.log('多选变化:', value)
}

function handleChange3({ value }: any) {
  console.log('范围变化:', value)
}
</script>
```

## 注意事项

- **时间戳精度**：所有类型的 `modelValue` 均为毫秒级时间戳。单选模式下为 `number` 类型，多选或范围选择模式下为 `number[]` 类型，未选择时为 `null`。
- **默认日期范围**：`min-date` 默认为当前日期往前推12个月的当天开始时间，`max-date` 默认为当前日期往后推12个月的当月结束时间。如需选择更久远或更未来的日期，请手动设置这两个属性。
- **范围选择确认按钮状态**：范围选择模式下，未选择满起止日期时确认按钮置灰不可点击；多选日期模式下，未选择任何日期时确认按钮同样不可点击。
- **类型切换模式**：开启 `show-type-switch` 后，面板内显示日/周/月三个 Tab。单日模式切换（date/week/month）和范围模式切换（daterange/weekrange/monthrange）根据当前 `type` 是否包含 'range' 关键词自动区分。
- **formatter 与 display-format 的区别**：`formatter` 用于格式化日历面板中每个日期项的显示（如添加顶部标记、底部标记、修改颜色等），作用于面板内部的每一天；`display-format` 用于格式化选中后在表单单元格中展示的文案格式，作用于关闭弹窗后单元格中的显示内容。
- **inner-display-format 的作用**：仅在范围选择模式下生效，用于自定义范围选择面板内部（确认按钮上方）起止日期的回显格式。
- **快捷选项返回类型**：`on-shortcuts-click` 回调函数需要返回一个 `number`（单选）或 `number[]`（范围选择）类型的时间戳值，如果设置了 `show-confirm` 为 false，则点击快捷选项后会自动确认。
- **时间过滤使用场景**：`time-filter` 仅在 `datetime` 或 `datetimerange` 类型下有效，可用于限制可选的小时、分钟、秒选项，例如只允许在工作时间（9:00-18:00）内选择。
- **allow-same-day 含义**：默认情况下，范围选择不允许起止日期为同一天。设置 `allow-same-day` 为 true 后允许选择同一天，适用于请半天假等场景。
- **show-confirm 为 false 的行为**：不显示确认按钮时，选择完成后（单选/多选/范围选满）自动确认并关闭弹窗。此时快捷选项点击后也会自动确认。
- **rootPortal 使用场景**：当日历弹窗在 fixed 定位元素内部无法正常显示时，设置 `root-portal` 为 true。
- **immediateChange 平台限制**：`immediate-change` 属性仅在微信小程序和支付宝小程序中生效。
- **内联面板高度适配**：`wd-calendar` 中 `panel-height` 会根据 `show-confirm` 自动调整（有确认按钮时为 338px，无确认按钮时为 400px）。`wd-calendar-view` 中默认高度为 378px，可通过 `panel-height` 自定义。
- **农历显示**：`wd-calendar-view` 默认显示农历（`show-lunar` 默认为 true），`wd-calendar` 中此属性由内部 `wd-calendar-view` 继承控制。
- **表单校验配合**：使用 `wd-calendar` 进行表单校验时，需设置 `prop` 属性与 `wd-form-item` 对应，并通过 `rules` 传入校验规则。
