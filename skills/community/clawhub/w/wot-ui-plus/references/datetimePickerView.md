# DatetimePickerView 日期时间选择器视图


## 组件概况

### 组件概述
DatetimePickerView 是一个日期时间选择器视图组件，基于 picker-view 实现，支持多种选择类型（日期、年月、时间、日期时间、年份），可自定义格式、范围和样式，常用于表单中的日期时间选择场景。

### 详细功能描述
- 支持多种选择类型：日期（date）、年月（year-month）、时间（time）、日期时间（datetime）、年份（year）
- 支持自定义日期范围（最小日期和最大日期）
- 支持自定义时间范围（最小/最大小时、分钟、秒）
- 支持显示秒选择（useSecond 属性）
- 支持自定义格式化选项文案
- 支持自定义过滤选项
- 支持自定义列格式化
- 支持加载状态
- 支持自定义滚动高度和选项高度
- 支持立即触发 change 事件（immediateChange 属性）
- 支持联动更新，如选择年份后自动更新月份，选择月份后自动更新日期

### 适用业务场景
- 表单中的日期时间选择
- 预约系统的时间选择
- 生日选择器
- 事件日历的日期选择
- 数据筛选的时间范围选择
- 活动报名的截止时间选择

## 完整API参考

### Props
| 名称 | 类型 | 默认值 | 必填 | 描述 |
| --- | --- | --- | --- | --- |
| modelValue | string / number | - | 是 | 选中项，当 type 为 time 时，类型为字符串（如 "12:30"），否则为时间戳 |
| type | string | datetime | 否 | 选择器类型，可选值：date / year-month / time / datetime / year |
| loading | boolean | false | 否 | 加载中状态 |
| loadingColor | string | #4D80F0 | 否 | 加载的颜色，只能使用十六进制的色值写法，且不能使用缩写 |
| columnsHeight | number | 217 | 否 | picker内部滚筒高度 |
| itemHeight | number | 35 | 否 | picker item的高度 |
| valueKey | string | value | 否 | 选项的key |
| labelKey | string | label | 否 | 选项的label |
| filter | function | - | 否 | 自定义过滤选项的函数，返回列的选项数组 |
| formatter | function | - | 否 | 自定义弹出层选项文案的格式化函数，返回一个字符串 |
| columnFormatter | function | - | 否 | 自定义列的格式化函数 |
| minDate | number | 当前年份-10年的1月1日 | 否 | 最小日期（时间戳） |
| maxDate | number | 当前年份+10年的12月31日 | 否 | 最大日期（时间戳） |
| minHour | number | 0 | 否 | 最小小时，time类型时生效 |
| maxHour | number | 23 | 否 | 最大小时，time类型时生效 |
| minMinute | number | 0 | 否 | 最小分钟，time类型时生效 |
| maxMinute | number | 59 | 否 | 最大分钟，time类型时生效 |
| useSecond | boolean | false | 否 | 是否显示秒选择，仅在 time 和 datetime 类型下生效 |
| minSecond | number | 0 | 否 | 最小秒数，仅在 time 和 datetime 类型下生效 |
| maxSecond | number | 59 | 否 | 最大秒数，仅在 time 和 datetime 类型下生效 |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发picker-view的 change 事件 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### Events
| 事件名 | 触发条件 | 参数说明 |
| --- | --- | --- |
| change | 选中值变化时触发 | { value: string/number, picker: object } - 选中的值和选择器实例 |
| pickstart | 开始滚动时触发 | - |
| pickend | 滚动结束时触发 | - |
| update:modelValue | 选中值变化时触发 | value: string/number - 选中的值 |

### Methods
| 方法名 | 参数 | 返回值 | 功能说明 |
| --- | --- | --- | --- |
| updateColumns | - | DatetimePickerViewOption[][] | 更新选项列数据 |
| setColumns | columnList: DatetimePickerViewOption[][] | - | 设置选项列数据 |
| getSelects | - | Record<string, any>[] | 获取当前选中的数据 |
| correctValue | value: string/number | string/number | 修正时间值，确保在有效范围内 |
| getOriginColumns | - | { type: string, values: number[] }[] | 获取原始的选项列数据 |

### Slots
| 插槽名 | 作用域变量 | 使用说明 |
| --- | --- | --- |

## 多场景使用示例代码

### 基础用法
```vue
<template>
  <view>
    <!-- 基础日期时间选择器视图 -->
    <wd-datetime-picker-view v-model="datetime" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const datetime = ref<number>(Date.now())
</script>
```

### 时间类型选择器
```vue
<template>
  <view>
    <!-- 时间类型选择器 -->
    <wd-datetime-picker-view 
      v-model="time" 
      type="time" 
      use-second
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const time = ref<string>("12:30:45")
</script>
```

### 日期类型选择器
```vue
<template>
  <view>
    <!-- 日期类型选择器 -->
    <wd-datetime-picker-view 
      v-model="date" 
      type="date"
      :min-date="minDate"
      :max-date="maxDate"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import dayjs from 'dayjs'

const date = ref<number>(Date.now())
const minDate = computed(() => dayjs().subtract(1, 'year').valueOf())
const maxDate = computed(() => dayjs().add(1, 'year').valueOf())
</script>
```

### 年月类型选择器
```vue
<template>
  <view>
    <!-- 年月类型选择器 -->
    <wd-datetime-picker-view 
      v-model="yearMonth" 
      type="year-month"
      :formatter="formatter"
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const yearMonth = ref<number>(Date.now())

// 自定义格式化函数
const formatter = (type: string, value: string) => {
  if (type === 'year') {
    return `${value}年`
  }
  if (type === 'month') {
    return `${value}月`
  }
  return value
}
</script>
```

### 年份类型选择器
```vue
<template>
  <view>
    <!-- 年份类型选择器 -->
    <wd-datetime-picker-view 
      v-model="year" 
      type="year"
      :min-date="minDate"
      :max-date="maxDate"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import dayjs from 'dayjs'

const year = ref<number>(Date.now())
const minDate = computed(() => dayjs().subtract(5, 'year').valueOf())
const maxDate = computed(() => dayjs().add(5, 'year').valueOf())
</script>
```

### 自定义样式和加载状态
```vue
<template>
  <view>
    <!-- 自定义样式和加载状态 -->
    <wd-datetime-picker-view 
      v-model="datetime"
      :loading="loading"
      loading-color="#ff6b6b"
      columns-height="300"
      item-height="45"
      custom-style="border: 1px solid #eee; border-radius: 8px;"
    />
    <wd-button @click="toggleLoading">
      {{ loading ? '关闭加载' : '开启加载' }}
    </wd-button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const datetime = ref<number>(Date.now())
const loading = ref<boolean>(false)

const toggleLoading = () => {
  loading.value = !loading.value
}
</script>
```

## 样式定制指南

### customStyle 用法
使用 `customStyle` 属性可以直接为选择器视图添加内联样式：
```vue
<wd-datetime-picker-view 
  custom-style="border: 1px solid #eee; border-radius: 8px; padding: 10px;"
/>
```

### customClass 用法
通过 `customClass` 属性可以为组件添加自定义CSS类：
```vue
<wd-datetime-picker-view custom-class="custom-picker" />

<style>
.custom-picker {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 10px;
  background-color: #f8f9fa;
}
</style>
```

### 滚动高度和选项高度
可以通过 `columnsHeight` 和 `itemHeight` 属性调整选择器的滚动高度和选项高度：
```vue
<wd-datetime-picker-view 
  columns-height="300"
  item-height="45"
/>
```

## 注意事项

1. **数据类型**: 当 `type` 为 `time` 时，`modelValue` 应为字符串格式（如 "12:30" 或 "12:30:45"）；其他类型时应为时间戳。
2. **联动更新**: 对于日期和日期时间类型，选择年份后会自动更新月份，选择月份后会自动更新日期，确保日期的有效性。
3. **加载状态**: `loading` 属性控制加载状态，`loadingColor` 属性控制加载动画的颜色，仅支持十六进制完整色值。
4. **格式化函数**: `formatter` 函数用于格式化选项文案，`columnFormatter` 函数用于自定义整个列的格式化。
5. **过滤函数**: `filter` 函数用于过滤选项，可以根据需要自定义显示的选项。
6. **秒选择**: 只有 `type` 为 `time` 或 `datetime` 时，`useSecond` 属性才有效。
7. **立即触发**: `immediateChange` 属性控制是否在手指松开时立即触发 `change` 事件，仅微信小程序和支付宝小程序支持。
8. **性能优化**: 当选择范围较大时，建议合理设置 `minDate` 和 `maxDate` 属性，避免生成过多选项导致性能问题。
9. **样式隔离**: 组件使用 `styleIsolation: 'shared'`，确保自定义样式能正常生效。
