# DatetimePicker 日期时间选择器


## 组件概况

DatetimePicker 日期时间选择器组件用于选择日期、时间或日期时间组合。该组件由 `wd-datetime-picker`（弹窗选择器）和 `wd-datetime-picker-view`（内联选择器视图）两个关联组件组成。`wd-datetime-picker` 以弹窗形式呈现选择面板，支持单选和区间选择两种模式；`wd-datetime-picker-view` 直接嵌入页面中使用，实时响应选择变化。组件支持多种时间类型（datetime、date、year-month、year、time），并提供秒级精度选择、范围限制、选项过滤、文案自定义等高级功能，广泛应用于预约下单、日程管理、筛选过滤等场景。

## 核心功能描述

- **多种时间类型**：支持 `datetime`（日期时间）、`date`（年月日）、`year-month`（年月）、`year`（年）、`time`（时分）五种选择类型
- **秒级精度**：通过 `use-second` 属性启用秒选择，在 datetime 和 time 类型下生效
- **区间选择模式**：当 `modelValue` 传入数组时自动切换为区间选择模式，提供开始/结束时间 Tab 切换面板
- **范围限制**：通过 `min-date` 和 `max-date` 属性限制可选日期范围，区间选择模式下自动禁用超出对方边界值的选项
- **时分范围控制**：time 类型支持 `min-hour` / `max-hour` / `min-minute` / `max-minute` 独立控制可选范围
- **选项过滤**：通过 `filter` 函数自定义过滤每列选项，例如仅展示 5 分钟倍数的分钟选项
- **文案格式化**：通过 `formatter` 函数自定义选项列中的显示文案，如添加"年"、"月"、"日"等后缀
- **展示文案自定义**：通过 `display-format` 函数自定义单元格中展示的最终文案格式
- **区间 Tab 标签格式化**：通过 `display-format-tab-label` 函数自定义区间选择模式下 Tab 标签的显示文案
- **确认前校验**：通过 `before-confirm` 函数在确认前执行异步校验
- **默认日期**：通过 `default-value` 设置打开面板时自动选中的默认日期
- **加载状态**：支持 `loading` 属性和 `setLoading()` 方法控制加载状态
- **可清空**：通过 `clearable` 属性显示清除按钮，一键清空已选值
- **表单集成**：支持表单校验功能，通过 `prop` 和 `rules` 属性与 `wd-form` 组件配合使用

## 适用业务场景

- **预约下单**：在预约服务、餐厅预订等场景中让用户选择日期和时间
- **行程管理**：在差旅预订、日程安排等场景中选择出发时间和到达时间
- **筛选过滤**：在订单列表、日志查询等场景中按日期区间进行筛选
- **表单填写**：在用户信息编辑、活动时间设置等表单场景中快速选择日期
- **时间范围设置**：在活动配置、权限有效期等场景中设置开始和结束时间
- **嵌入式时间选择**：`wd-datetime-picker-view` 适用于需要在页面中常驻显示时间选择器的场景

## API

### wd-datetime-picker Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string / number / Array\<string / number\> | - | 是 | 选中值。当 type 为 time 时为字符串格式（如 '09:30'）；当传入数组时为区间选择模式；否则为时间戳（毫秒） |
| type | string | 'datetime' | 否 | 选择器类型，可选值：`datetime`（日期时间）、`date`（年月日）、`year-month`（年月）、`year`（年）、`time`（时分） |
| label | string | '' | 否 | 选择器左侧文案（表单项标签） |
| placeholder | string | 请选择 | 否 | 选择器未选中时的占位符文案 |
| disabled | boolean | false | 否 | 是否禁用选择器，禁用后无法点击打开弹窗 |
| readonly | boolean | false | 否 | 是否只读，只读状态下不可点击但样式与禁用不同 |
| loading | boolean | false | 否 | 是否显示加载状态 |
| loadingColor | string | '#4D80F0' | 否 | 加载指示器的颜色 |
| title | string | '' | 否 | 弹出层标题，设置后在弹窗顶部中间显示 |
| cancelButtonText | string | 取消 | 否 | 取消按钮文案，未设置时跟随国际化配置 |
| confirmButtonText | string | 确认 | 否 | 确认按钮文案，未设置时跟随国际化配置 |
| required | boolean | false | 否 | 是否显示必填标记（星号） |
| size | string | '' | 否 | 组件尺寸，可选值：`large` |
| labelWidth | string | '33%' | 否 | 左侧标题宽度 |
| error | boolean | false | 否 | 是否显示为错误状态，错误状态下选中内容显示为红色 |
| alignRight | boolean | false | 否 | 选中值是否靠右对齐显示 |
| ellipsis | boolean | false | 否 | 文本溢出时是否显示省略号 |
| clearable | boolean | false | 否 | 是否显示清除按钮 |
| markerSide | string | 'before' | 否 | 必填标记位置，可选值：`before`（左侧）、`after`（右侧） |
| columnsHeight | number | 217 | 否 | 选项滚动区域的总高度，单位为 px |
| valueKey | string | 'value' | 否 | 选项对象中表示值的字段名 |
| labelKey | string | 'label' | 否 | 选项对象中表示显示文本的字段名 |
| minDate | number | 当前年份往前推10年的1月1日 | 否 | 最小可选日期，类型为时间戳（毫秒） |
| maxDate | number | 当前年份往后推10年的12月31日 | 否 | 最大可选日期，类型为时间戳（毫秒） |
| minHour | number | 0 | 否 | 最小可选小时，仅在 time 类型下生效 |
| maxHour | number | 23 | 否 | 最大可选小时，仅在 time 类型下生效 |
| minMinute | number | 0 | 否 | 最小可选分钟，仅在 time 类型下生效 |
| maxMinute | number | 59 | 否 | 最大可选分钟，仅在 time 类型下生效 |
| useSecond | boolean | false | 否 | 是否启用秒选择，仅在 time 和 datetime 类型下生效 |
| minSecond | number | 0 | 否 | 最小可选秒数，仅在 time 和 datetime 类型下生效 |
| maxSecond | number | 59 | 否 | 最大可选秒数，仅在 time 和 datetime 类型下生效 |
| defaultValue | string / number / Array\<string / number\> | 无 | 否 | 默认日期/时间，打开面板时自动选中此值，类型需与 modelValue 保持一致 |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发 change 事件，仅在微信小程序和支付宝小程序中生效 |
| filter | Function | 无 | 否 | 自定义过滤选项的函数，签名为 `(type: string, values: number[]) => number[]`，返回过滤后的选项数组 |
| formatter | Function | 无 | 否 | 自定义选项文案的格式化函数，签名为 `(type: string, value: string) => string`，返回格式化后的文案 |
| displayFormat | Function | 默认格式化函数 | 否 | 自定义展示文案的格式化函数，签名为 `(items: Record\<string, any\>[]) => string`，返回单元格展示的文案 |
| displayFormatTabLabel | Function | 无 | 否 | 区间选择模式下自定义 Tab 标签文案的格式化函数，签名为 `(items: Record\<string, any\>[]) => string` |
| beforeConfirm | Function | 无 | 否 | 确认前校验函数，签名为 `(value: number \| string \| (number \| string)[], resolve: (isPass: boolean) => void, picker: DatetimePickerInstance) => void` |
| closeOnClickModal | boolean | true | 否 | 点击遮罩层是否关闭弹窗 |
| safeAreaInsetBottom | boolean | true | 否 | 是否在底部安全区域内显示（适配 iPhone X 等全面屏机型） |
| zIndex | number | 15 | 否 | 弹出层的层级 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 定位失效问题 |
| prop | string | '' | 否 | 表单域 model 字段名，使用表单校验时必填 |
| rules | Array\<FormItemRule\> | [] | 否 | 表单验证规则，结合 wd-form 组件使用 |
| customCellClass | string | '' | 否 | 自定义 cell 单元格区域的样式类名 |
| customLabelClass | string | '' | 否 | 自定义 label 区域的样式类名 |
| customValueClass | string | '' | 否 | 自定义 value 显示区域的样式类名 |
| customViewClass | string | '' | 否 | 自定义内部 pickerView 视图区域的样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-datetime-picker-view Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string / number | - | 是 | 选中值。当 type 为 time 时为字符串格式（如 '09:30'）；其他类型为时间戳（毫秒） |
| type | string | 'datetime' | 否 | 选择器类型，可选值：`datetime`、`date`、`year-month`、`year`、`time` |
| loading | boolean | false | 否 | 是否显示加载状态 |
| loadingColor | string | '#4D80F0' | 否 | 加载指示器的颜色 |
| columnsHeight | number | 217 | 否 | 选项滚动区域的总高度，单位为 px |
| itemHeight | number | 35 | 否 | 每个选项项的高度，单位为 px |
| valueKey | string | 'value' | 否 | 选项对象中表示值的字段名 |
| labelKey | string | 'label' | 否 | 选项对象中表示显示文本的字段名 |
| minDate | number | 当前年份往前推10年的1月1日 | 否 | 最小可选日期，类型为时间戳（毫秒） |
| maxDate | number | 当前年份往后推10年的12月31日 | 否 | 最大可选日期，类型为时间戳（毫秒） |
| minHour | number | 0 | 否 | 最小可选小时，仅在 time 类型下生效 |
| maxHour | number | 23 | 否 | 最大可选小时，仅在 time 类型下生效 |
| minMinute | number | 0 | 否 | 最小可选分钟，仅在 time 类型下生效 |
| maxMinute | number | 59 | 否 | 最大可选分钟，仅在 time 类型下生效 |
| useSecond | boolean | false | 否 | 是否启用秒选择，仅在 time 和 datetime 类型下生效 |
| minSecond | number | 0 | 否 | 最小可选秒数，仅在 time 和 datetime 类型下生效 |
| maxSecond | number | 59 | 否 | 最大可选秒数，仅在 time 和 datetime 类型下生效 |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发 change 事件，仅在微信小程序和支付宝小程序中生效 |
| filter | Function | 无 | 否 | 自定义过滤选项的函数，签名与 wd-datetime-picker 相同 |
| formatter | Function | 无 | 否 | 自定义选项文案的格式化函数，签名与 wd-datetime-picker 相同 |
| columnFormatter | Function | 无 | 否 | 自定义列的完整格式化函数，签名为 `(picker: DatetimePickerViewExpose) => DatetimePickerViewOption[][]`，用于更精细的列控制（如区间选择模式下的禁用状态处理） |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-datetime-picker Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| confirm | 点击确认按钮并完成校验后触发 | `(data: { value: string \| number \| Array\<string \| number\> })` | `value` 为选中值，区间选择模式下为包含开始和结束时间的数组 |
| cancel | 点击取消按钮或点击遮罩关闭弹窗时触发 | 无 | - |
| open | 弹窗打开时触发 | 无 | - |
| change | 滚动选中项变化时触发 | `(data: { value: string \| number \| Array\<string \| number\> })` | `value` 为当前变化的选中值 |
| toggle | 区间选择模式下切换 Tab 时触发 | `(value: string \| number)` | 切换后当前 Tab 对应的选中值 |
| clear | 点击清除按钮清空选中值时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: string \| number \| Array\<string \| number\>)` | 值为确认后的新选中值 |

### wd-datetime-picker-view Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 滚动选中项变化时触发 | `(data: { value: string \| number; picker: DatetimePickerViewInstance })` | `value` 为更新后的选中值，`picker` 为组件实例 |
| pickstart | 手指开始触摸滚动时触发 | 无 | - |
| pickend | 手指结束触摸滚动时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: string \| number)` | 值为变化后的新选中值 |

### wd-datetime-picker Methods

通过 ref 可以获取 `wd-datetime-picker` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| open | 无 | void | 打开选择器弹出层 |
| close | 无 | void | 关闭选择器弹出层 |
| setLoading | `(loading: boolean)` | void | 设置加载状态，true 为加载中，false 为加载完成 |

### wd-datetime-picker-view Methods

通过 ref 可以获取 `wd-datetime-picker-view` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| updateColumns | 无 | `DatetimePickerViewOption[][]` | 重新计算并返回所有列的数据，基于当前选中值和范围边界 |
| setColumns | `(columnList: DatetimePickerViewOption[][])` | void | 设置完整的列数据 |
| getSelects | 无 | `Record\<string, any\> \| Record\<string, any\>[] \| undefined` | 获取选中项数据，每项包含 label 和 value |
| correctValue | `(value: string \| number)` | `string \| number` | 修正输入值为合法范围内的有效值 |
| getOriginColumns | 无 | `{ type: string; values: number[] }[]` | 获取原始列数据（未经 formatter 处理的纯数值数组） |

### wd-datetime-picker Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义触发选择器的元素，替换默认的 wd-cell 单元格 |
| label | - | 自定义左侧标签区域内容 |

### wd-datetime-picker-view Slots

`wd-datetime-picker-view` 不提供自定义插槽。

## 使用示例

### 示例一：基础日期时间选择

最常用的日期时间选择器用法，支持多种 type 类型切换。

```vue
<template>
  <wd-cell-group border>
    <!-- 完整日期时间（年月日时分） -->
    <wd-datetime-picker
      label="日期时间选择"
      v-model="datetimeValue"
      @confirm="handleDatetimeConfirm"
    />

    <!-- 仅年月日 -->
    <wd-datetime-picker
      label="年月日"
      v-model="dateValue"
      type="date"
      @confirm="handleDateConfirm"
    />

    <!-- 仅年月 -->
    <wd-datetime-picker
      label="年月"
      v-model="yearMonthValue"
      type="year-month"
      @confirm="handleYearMonthConfirm"
    />

    <!-- 仅年份 -->
    <wd-datetime-picker
      label="年份"
      v-model="yearValue"
      type="year"
      @confirm="handleYearConfirm"
    />

    <!-- 时分 -->
    <wd-datetime-picker
      label="时分"
      v-model="timeValue"
      type="time"
      @confirm="handleTimeConfirm"
    />

    <!-- 带秒选择的日期时间 -->
    <wd-datetime-picker
      label="日期时间（带秒）"
      v-model="secondValue"
      use-second
    />

    <!-- 带秒选择的时间 -->
    <wd-datetime-picker
      label="时间（带秒）"
      v-model="timeSecondValue"
      type="time"
      use-second
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const datetimeValue = ref<number>(Date.now())
const dateValue = ref<number>(Date.now())
const yearMonthValue = ref<number>(Date.now())
const yearValue = ref<number>(Date.now())
const timeValue = ref<string>('09:30')
const secondValue = ref<number>(Date.now())
const timeSecondValue = ref<string>('09:30:26')

function handleDatetimeConfirm({ value }: any) {
  console.log('日期时间:', new Date(value))
}

function handleDateConfirm({ value }: any) {
  console.log('日期:', new Date(value))
}

function handleYearMonthConfirm({ value }: any) {
  console.log('年月:', value)
}

function handleYearConfirm({ value }: any) {
  console.log('年份:', new Date(value).getFullYear())
}

function handleTimeConfirm({ value }: any) {
  console.log('时间:', value)
}
</script>
```

### 示例二：自定义文案与过滤选项

通过 `formatter` 函数自定义选项列的显示文案，通过 `filter` 函数过滤可选项，通过 `display-format` 自定义单元格展示的文案格式。

```vue
<template>
  <wd-cell-group border>
    <!-- 自定义选项文案：添加"年"、"月"等后缀 -->
    <wd-datetime-picker
      label="自定义文案"
      v-model="formatterValue"
      :formatter="formatter"
      @confirm="handleConfirm"
    />

    <!-- 过滤分钟选项：仅显示5的倍数 -->
    <wd-datetime-picker
      label="过滤分钟（5分钟间隔）"
      v-model="filterValue"
      :filter="filter"
      @confirm="handleConfirm"
    />

    <!-- 自定义单元格展示文案 -->
    <wd-datetime-picker
      label="自定义展示格式"
      v-model="displayValue"
      :display-format="displayFormat"
      @confirm="handleConfirm"
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {
  DatetimePickerViewFormatter,
  DatetimePickerViewFilter
} from '@/uni_modules/wot-ui-plus/components/wd-datetime-picker-view/types'
import type { DatetimePickerDisplayFormat } from '@/uni_modules/wot-ui-plus/components/wd-datetime-picker/types'

const formatterValue = ref<number>(Date.now())
const filterValue = ref<number>(Date.now())
const displayValue = ref<number>(Date.now())

// 格式化选项文案
const formatter: DatetimePickerViewFormatter = (type, value) => {
  const suffixMap: Record<string, string> = {
    year: '年',
    month: '月',
    date: '日',
    hour: '时',
    minute: '分',
    second: '秒'
  }
  return value + (suffixMap[type] || '')
}

// 过滤分钟选项
const filter: DatetimePickerViewFilter = (type, values) => {
  if (type === 'minute') {
    return values.filter((value) => value % 5 === 0)
  }
  return values
}

// 自定义单元格展示文案
const displayFormat: DatetimePickerDisplayFormat = (items) => {
  return `${items[0].label}年${items[1].label}月${items[2].label}日 ${items[3].label}:${items[4].label}`
}

function handleConfirm({ value }: any) {
  console.log('确认值:', value)
}
</script>
```

### 示例三：区间选择模式

当 `modelValue` 传入数组时，组件自动进入区间选择模式，提供开始时间和结束时间的 Tab 切换面板。在区间选择中，开始时间的可选范围受结束时间限制，反之亦然。

```vue
<template>
  <wd-cell-group border>
    <!-- 日期区间选择 -->
    <wd-datetime-picker
      label="日期区间"
      title="请选择时间区间"
      v-model="rangeValue"
      :display-format-tab-label="displayFormatTabLabel"
      @confirm="handleRangeConfirm"
      @toggle="handleToggle"
    />

    <!-- 时间区间选择（带秒） -->
    <wd-datetime-picker
      label="时间区间"
      v-model="timeRangeValue"
      type="time"
      use-second
      @confirm="handleTimeRangeConfirm"
    />

    <!-- 限制日期范围的区间选择 -->
    <wd-datetime-picker
      label="一年范围内的选择"
      :min-date="minDate"
      :max-date="maxDate"
      v-model="limitedRangeValue"
      @confirm="handleLimitedRangeConfirm"
    />
  </wd-cell-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { DatetimePickerDisplayFormatTabLabel } from '@/uni_modules/wot-ui-plus/components/wd-datetime-picker/types'

// 日期区间
const rangeValue = ref<number[]>([Date.now(), Date.now() + 7 * 24 * 60 * 60 * 1000])

// 时间区间
const timeRangeValue = ref<string[]>(['09:00:00', '18:00:00'])

// 限制范围
const now = new Date()
const minDate = ref<number>(Date.now())
const maxDate = ref<number>(new Date(now.getFullYear() + 1, now.getMonth(), now.getDate()).getTime())
const limitedRangeValue = ref<number[]>([Date.now(), Date.now() + 30 * 24 * 60 * 60 * 1000])

// 自定义 Tab 标签文案
const displayFormatTabLabel: DatetimePickerDisplayFormatTabLabel = (items) => {
  return `${items[0].label}年${items[1].label}月${items[2].label}日`
}

function handleRangeConfirm({ value }: any) {
  console.log('开始时间:', new Date(value[0]))
  console.log('结束时间:', new Date(value[1]))
}

function handleToggle(value: number | string) {
  console.log('切换到:', value)
}

function handleTimeRangeConfirm({ value }: any) {
  console.log('开始时间:', value[0])
  console.log('结束时间:', value[1])
}

function handleLimitedRangeConfirm({ value }: any) {
  console.log('区间:', new Date(value[0]), '~', new Date(value[1]))
}
</script>
```

### 示例四：确认前校验与可清空功能

通过 `before-confirm` 函数在确认前执行异步校验，通过 `clearable` 属性实现可清空功能。

```vue
<template>
  <wd-cell-group border>
    <!-- 确认前校验 -->
    <wd-datetime-picker
      label="校验选择（不能选未来日期）"
      v-model="validateValue"
      :before-confirm="beforeConfirm"
      @confirm="handleConfirm"
    />

    <!-- 可清空的日期选择 -->
    <wd-datetime-picker
      label="日期选择（可清空）"
      v-model="clearableValue"
      clearable
      @clear="handleClear"
      @confirm="handleClearableConfirm"
    />

    <!-- 可清空的区间选择 -->
    <wd-datetime-picker
      label="区间选择（可清空）"
      v-model="rangeClearableValue"
      clearable
      @clear="handleRangeClear"
      @confirm="handleRangeClearableConfirm"
    />
  </wd-cell-group>
  <wd-toast />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'
import type { DatetimePickerInstance } from '@/uni_modules/wot-ui-plus/components/wd-datetime-picker/types'

const toast = useToast()

const validateValue = ref<number>(Date.now())
const clearableValue = ref<number>(Date.now())
const rangeClearableValue = ref<number[]>([Date.now(), Date.now() + 7 * 24 * 60 * 60 * 1000])

// 确认前校验
const beforeConfirm = (value: number | string | (number | string)[], resolve: (isPass: boolean) => void, picker: DatetimePickerInstance) => {
  picker.setLoading(true)
  setTimeout(() => {
    picker.setLoading(false)
    if ((value as number) > Date.now()) {
      resolve(false)
      toast.error('不能选择大于今天的日期')
    } else {
      resolve(true)
    }
  }, 1500)
}

function handleConfirm({ value }: any) {
  console.log('校验通过，确认值:', new Date(value))
}

function handleClear() {
  clearableValue.value = '' as any
  toast.success('已清空')
}

function handleClearableConfirm({ value }: any) {
  console.log('确认值:', value)
}

function handleRangeClear() {
  rangeClearableValue.value = [] as any
  toast.success('区间已清空')
}

function handleRangeClearableConfirm({ value }: any) {
  console.log('区间确认值:', value)
}
</script>
```

### 示例五：内联选择器 wd-datetime-picker-view

`wd-datetime-picker-view` 直接嵌入页面中使用，无需弹窗，实时响应选择变化。

```vue
<template>
  <view class="datetime-picker-view-section">
    <!-- 日期选择 -->
    <view class="view-item">
      <text class="view-title">日期选择</text>
      <wd-datetime-picker-view
        v-model="dateViewValue"
        @change="handleDateViewChange"
      />
      <text class="view-value">选中值: {{ formatDate(dateViewValue) }}</text>
    </view>

    <!-- 年月日选择 -->
    <view class="view-item">
      <text class="view-title">年月日选择</text>
      <wd-datetime-picker-view
        type="date"
        v-model="dateOnlyValue"
        @change="handleDateOnlyChange"
      />
    </view>

    <!-- 时间选择 -->
    <view class="view-item">
      <text class="view-title">时间选择</text>
      <wd-datetime-picker-view
        type="time"
        v-model="timeViewValue"
        @change="handleTimeViewChange"
      />
    </view>

    <!-- 带过滤的内联选择 -->
    <view class="view-item">
      <text class="view-title">自定义过滤（分钟间隔5分钟）</text>
      <wd-datetime-picker-view
        v-model="filterViewValue"
        :filter="filterFn"
        @change="handleFilterViewChange"
      />
    </view>

    <!-- 带自定义格式的内联选择 -->
    <view class="view-item">
      <text class="view-title">自定义选项文案</text>
      <wd-datetime-picker-view
        v-model="formatterViewValue"
        :formatter="formatterFn"
        @change="handleFormatterViewChange"
      />
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type {
  DatetimePickerViewFormatter,
  DatetimePickerViewFilter
} from '@/uni_modules/wot-ui-plus/components/wd-datetime-picker-view/types'

const dateViewValue = ref<number>(Date.now())
const dateOnlyValue = ref<number>(Date.now())
const timeViewValue = ref<string>('11:30')
const filterViewValue = ref<number>(Date.now())
const formatterViewValue = ref<number>(Date.now())

function formatDate(timestamp: number): string {
  const date = new Date(timestamp)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

function handleDateViewChange({ value }: any) {
  console.log('日期变化:', new Date(value))
}

function handleDateOnlyChange({ value }: any) {
  console.log('年月日变化:', new Date(value))
}

function handleTimeViewChange({ value }: any) {
  console.log('时间变化:', value)
}

function handleFilterViewChange({ value }: any) {
  console.log('过滤选择变化:', new Date(value))
}

function handleFormatterViewChange({ value }: any) {
  console.log('格式化选择变化:', new Date(value))
}

// 过滤函数
const filterFn: DatetimePickerViewFilter = (type, values) => {
  if (type === 'minute') {
    return values.filter((value) => value % 5 === 0)
  }
  return values
}

// 格式化函数
const formatterFn: DatetimePickerViewFormatter = (type, value) => {
  const suffixMap: Record<string, string> = {
    year: '年',
    month: '月',
    date: '日',
    hour: '时',
    minute: '分'
  }
  return value + (suffixMap[type] || '')
}
</script>

<style scoped>
.datetime-picker-view-section {
  padding: 16px;
  background: #f5f5f5;
}
.view-item {
  background: #fff;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
}
.view-title {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
  display: block;
}
.view-value {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
  display: block;
}
</style>
```

## 注意事项

- **时间戳精度**：除 `time` 类型外，所有类型的 `modelValue` 均为毫秒级时间戳。如果传入非法时间戳，组件会自动修正到 `min-date` 和 `max-date` 范围内的最接近值。
- **time 类型值格式**：当 `type` 为 `time` 时，`modelValue` 为字符串格式，如 `'09:30'` 或 `'09:30:26'`（启用秒选择时）。
- **区间选择自动识别**：当 `modelValue` 传入数组时，`wd-datetime-picker` 会自动进入区间选择模式，显示开始/结束时间两个 Tab 面板。区间选择时两个面板共享边界约束，开始时间不能晚于结束时间，结束时间不能早于开始时间。
- **区间 Tab 切换**：在区间选择模式下，切换 Tab 时会触发 `toggle` 事件，同时刷新当前面板的列数据以应用最新的边界约束。
- **formatter 与 display-format 的区别**：`formatter` 用于格式化弹出面板中每一列的选项文案（如"2024年"、"3月"），`display-format` 用于格式化选中后在表单单元格中展示的文案。两者作用不同，可以配合使用。
- **columnFormatter 高级用法**：`wd-datetime-picker-view` 提供的 `columnFormatter` 比 `formatter` 更底层，可以完整控制列的每一项（包括 `disabled` 状态），在区间选择模式中用于禁用超出边界值的选项。
- **filter 函数注意事项**：`filter` 函数接收列类型和原始选项数组，返回过滤后的数组。如果过滤后数组为空，可能导致列无法显示选项。
- **边界值自动修正**：区间选择模式下，如果开始时间修改后晚于结束时间，组件会自动将开始时间修正为与结束时间相同；反之亦然。
- **滑动中确认处理**：与 `wd-picker` 类似，快速滚动后立即点击确认按钮时，组件会等待滚动动画结束后再执行确认。
- **默认日期与选中值的关系**：`default-value` 用于设置打开面板时未选中状态下的默认日期，当 `modelValue` 已有值时以 `modelValue` 为准。
- **immediateChange 平台限制**：`immediate-change` 属性仅在微信小程序和支付宝小程序中生效。
- **rootPortal 使用场景**：当选择器弹窗在 fixed 定位元素内部无法正常显示时，设置 `root-portal` 为 true。
- **表单校验配合**：使用 `wd-datetime-picker` 进行表单校验时，需设置 `prop` 属性与 `wd-form-item` 对应，并通过 `rules` 传入校验规则。
- **type 类型校验**：如果传入的 `type` 不是合法的可选值，控制台会输出错误提示。
- **columnsHeight 与 itemHeight**：`wd-datetime-picker-view` 支持通过 `columns-height` 和 `item-height` 分别控制滚动区域总高度和单项高度，调整这两个值可以改变可见选项的数量。
