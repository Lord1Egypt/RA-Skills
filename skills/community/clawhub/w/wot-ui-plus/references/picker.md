# Picker 选择器


## 组件概况

Picker 选择器组件用于在预设的选项列表中进行单选或多选操作。该组件由 `wd-picker`（弹窗选择器）和 `wd-picker-view`（内联选择器视图）两个关联组件组成。`wd-picker` 以弹窗形式呈现，适用于表单填写场景；`wd-picker-view` 直接嵌入页面中，适用于需要常驻显示的选择器场景。两者共享相同的数据格式和列操作能力，支持单列选择、多列选择和多级联动选择，广泛应用于省市区选择、分类筛选、表单选项等场景。

## 核心功能描述

- **弹窗选择模式**：`wd-picker` 内置底部弹出层，点击表单单元格后弹出选择面板，支持取消和确认操作
- **内联嵌入模式**：`wd-picker-view` 直接嵌入页面布局中，实时响应选择变化，无需弹窗交互
- **单列选择**：支持一维数组数据源，适用于简单的单选场景
- **多列选择**：支持二维数组数据源，每一列独立滚动选择，适用于多字段组合选择
- **多级联动**：通过 `column-change` 回调函数，在列切换时动态更新后续列的数据源，实现省市区三级联动等场景
- **自定义展示文案**：通过 `display-format` 函数自定义单元格中显示的选中值文案格式
- **确认前校验**：通过 `before-confirm` 函数在点击确认按钮时执行异步校验，校验不通过可阻止确认
- **禁用选项**：选项对象支持 `disabled` 属性，被禁用的选项无法选中，自动选择距离最近的可用选项
- **立即变更模式**：通过 `immediate-change` 属性控制是否在手指松开时立即触发 change 事件
- **加载状态**：支持 `loading` 属性显示加载动画，`wd-picker` 还提供 `setLoading()` 方法供外部控制
- **可清空**：通过 `clearable` 属性显示清除按钮，一键清空已选值
- **表单集成**：支持表单校验功能，通过 `prop` 和 `rules` 属性与 `wd-form` 组件配合使用
- **丰富的方法暴露**：`wd-picker-view` 暴露了获取选中项、设置列数据、重置列数据等完整的方法集

## 适用业务场景

- **省市区选择**：通过多级联动功能实现省/市/区三级联动选择
- **分类筛选**：在商品列表、内容列表页面提供分类、品牌等多维度筛选条件
- **表单选项**：在注册表单、信息填写页面提供下拉式选项选择，如学历、行业、职位等
- **多字段组合选择**：如学校+专业、品牌+型号等多字段组合场景
- **时间/日期自定义选择**：当内置的日期选择器不满足需求时，可自定义日期选项列表
- **嵌入式选择器**：`wd-picker-view` 适用于需要在页面中常驻显示选择器的场景，如设置页面、筛选面板

## API

### wd-picker Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string / number / Array\<string / number\> | '' | 否 | 选中项的值。单列选择时为字符串或数字，多列选择时为数组 |
| columns | Array\<string / number / ColumnItem / Array\<string / number / ColumnItem\>\> | [] | 否 | 选择器数据源，可以为字符串数组、对象数组（ColumnItem），二维数组表示多列选择器 |
| label | string | '' | 否 | 选择器左侧文案（表单项标签） |
| placeholder | string | 请选择 | 否 | 选择器未选中时的占位符文案 |
| disabled | boolean | false | 否 | 是否禁用选择器，禁用后无法点击打开弹窗 |
| readonly | boolean | false | 否 | 是否只读，只读状态下不可点击但样式与禁用不同 |
| loading | boolean | false | 否 | 是否显示加载状态 |
| loadingColor | string | '#4D80F0' | 否 | 加载指示器的颜色 |
| title | string | '' | 否 | 弹出层标题，设置后在弹窗顶部中间显示 |
| cancelButtonText | string | 取消 | 否 | 取消按钮文案，未设置时跟随国际化配置 |
| confirmButtonText | string | 完成 | 否 | 确认按钮文案，未设置时跟随国际化配置 |
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
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发 change 事件，仅在微信小程序和支付宝小程序中生效 |
| displayFormat | Function | 默认格式化函数 | 否 | 自定义展示文案的格式化函数，签名为 `(items: ColumnItem \| ColumnItem[], vl: { valueKey: string; labelKey: string }) => string`，返回一个字符串 |
| beforeConfirm | Function | 无 | 否 | 确认前校验函数，签名为 `(value: string \| number \| boolean \| string[] \| number[] \| boolean[], resolve: (isPass: boolean) => void, picker: PickerInstance) => void` |
| columnChange | Function | 无 | 否 | 列切换回调函数，签名为 `(pickerView: PickerViewInstance, selects: Record\<string, any\> \| Record\<string, any\>[], index: number, resolve: () => void) => void`，用于多级联动场景 |
| closeOnClickModal | boolean | true | 否 | 点击遮罩层是否关闭弹窗 |
| safeAreaInsetBottom | boolean | true | 否 | 是否在底部安全区域内显示（适配 iPhone X 等全面屏机型） |
| zIndex | number | 15 | 否 | 弹出层的层级 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 定位失效问题 |
| prop | string | '' | 否 | 表单域 model 字段名，使用表单校验时必填 |
| rules | Array\<FormItemRule\> | [] | 否 | 表单验证规则，结合 wd-form 组件使用 |
| customLabelClass | string | '' | 否 | 自定义 label 区域的样式类名 |
| customValueClass | string | '' | 否 | 自定义 value 显示区域的样式类名 |
| customViewClass | string | '' | 否 | 自定义内部 pickerView 视图区域的样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-picker-view Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string / number / boolean / Array\<number\> / Array\<string\> / Array\<boolean\> | '' | 是 | 选中项的值，类型需要与 columns 中的 value 类型保持一致 |
| columns | Array\<string / number / ColumnItem / Array\<number\> / Array\<string\> / Array\<ColumnItem\>\> | [] | 否 | 选择器数据源，格式与 wd-picker 一致 |
| loading | boolean | false | 否 | 是否显示加载状态 |
| loadingColor | string | '#4D80F0' | 否 | 加载指示器的颜色 |
| columnsHeight | number | 217 | 否 | 选项滚动区域的总高度，单位为 px |
| itemHeight | number | 35 | 否 | 每个选项项的高度，单位为 px |
| valueKey | string | 'value' | 否 | 选项对象中表示值的字段名 |
| labelKey | string | 'label' | 否 | 选项对象中表示显示文本的字段名 |
| immediateChange | boolean | false | 否 | 是否在手指松开时立即触发 change 事件，仅在微信小程序和支付宝小程序中生效 |
| columnChange | Function | 无 | 否 | 列切换回调函数，签名与 wd-picker 相同，用于多级联动场景 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### ColumnItem 数据结构

| 字段名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| value | string / number / boolean | - | 选项的值 |
| label | string | - | 选项的显示文本 |
| disabled | boolean | false | 是否禁用该选项 |

### wd-picker Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| confirm | 点击确认按钮并完成校验后触发 | `(data: { value: string \| number \| Array\<string \| number\>; selectedItems: ColumnItem \| ColumnItem[] })` | `value` 为选中项的值数组，`selectedItems` 为选中项的完整数据对象 |
| cancel | 点击取消按钮或点击遮罩关闭弹窗时触发 | 无 | - |
| open | 弹窗打开时触发 | 无 | - |
| clear | 点击清除按钮清空选中值时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: string \| number \| Array\<string \| number\>)` | 值为确认后的新选中值 |

### wd-picker-view Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 选择器滚动选中项变化时触发 | `(data: { picker: PickerViewInstance; value: string \| number \| Array\<string \| number\>; index: number })` | `picker` 为 pickerView 实例，`value` 为当前选中值，`index` 为变化列的下标（单列时为行下标） |
| pickstart | 手指开始触摸滚动时触发 | 无 | - |
| pickend | 手指结束触摸滚动时触发 | 无 | - |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: string \| number \| Array\<string \| number\>)` | 值为变化后的新选中值 |

### wd-picker Methods

通过 ref 可以获取 `wd-picker` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| open | 无 | void | 打开选择器弹出层 |
| close | 无 | void | 关闭选择器弹出层 |
| setLoading | `(loading: boolean)` | void | 设置加载状态，true 为加载中，false 为加载完成 |

### wd-picker-view Methods

通过 ref 可以获取 `wd-picker-view` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| getSelects | 无 | `Record\<string, any\> \| Record\<string, any\>[]` | 获取所有列的选中项数据对象，单列时返回单个对象，多列时返回对象数组 |
| getValues | 无 | `string \| number \| Array\<string \| number\>` | 获取所有列的选中值，单列时返回单个值，多列时返回数组 |
| getLabels | 无 | `string[]` | 获取所有列选中项的 label 文本数组 |
| getSelectedIndex | 无 | `number[]` | 获取所有列选中项的索引数组 |
| getColumnIndex | `(columnIndex: number)` | `number` | 获取指定列的选中项索引 |
| getColumnData | `(columnIndex: number)` | `Record\<string, string\>[]` | 获取指定列的选项数据 |
| getColumnsData | 无 | `Record\<string, string\>[][]` | 获取所有列的选项数据 |
| setColumnData | `(columnIndex: number, data: Array\<string \| number \| ColumnItem\>, rowIndex?: number)` | void | 设置指定列的数据源，rowIndex 为设置后的默认选中行下标，默认为 0 |
| resetColumns | `(columns: Array\<string \| number \| ColumnItem \| string[] \| number[] \| ColumnItem[]\>)` | void | 重置所有列的数据为指定数据 |

### wd-picker Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义触发选择器的元素，替换默认的 wd-cell 单元格 |
| label | - | 自定义左侧标签区域内容 |

### wd-picker-view Slots

`wd-picker-view` 不提供自定义插槽。

## 使用示例

### 示例一：单列选择器

最基础的选择器用法，传入一维数组作为数据源，支持字符串数组和对象数组两种格式。

```vue
<template>
  <wd-picker
    label="单列选项"
    v-model="value"
    :columns="columns"
    @confirm="handleConfirm"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')

const columns = ref([
  { label: '选项一', value: '1' },
  { label: '选项二', value: '2' },
  { label: '选项三', value: '3' },
  { label: '选项四', value: '4' },
  { label: '选项五', value: '5' }
])

function handleConfirm({ value, selectedItems }: any) {
  console.log('选中值:', value)
  console.log('选中项:', selectedItems)
}
</script>
```

简洁写法，直接传入字符串数组（此时 value 和 label 均为字符串本身）：

```vue
<template>
  <wd-picker label="单列选项" v-model="value" :columns="columns" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref('')
const columns = ref(['选项一', '选项二', '选项三', '选项四', '选项五'])
</script>
```

### 示例二：多级联动选择器

通过 `column-change` 回调函数实现省市区三级联动，当某一列切换时动态更新后续列的数据源。

```vue
<template>
  <wd-picker
    label="省市区选择"
    v-model="value"
    :columns="columns"
    :column-change="onChangeDistrict"
    @confirm="handleConfirm"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { PickerViewColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-picker-view/types'

const value = ref(['110000', '110100', '110102'])

// 模拟省市区数据
const district: Record<string, Array<{ label: string; value: string }>> = {
  0: [
    { label: '北京市', value: '110000' },
    { label: '广东省', value: '440000' }
  ],
  110000: [{ label: '北京市', value: '110100' }],
  440000: [
    { label: '广州市', value: '440100' },
    { label: '深圳市', value: '440300' },
    { label: '珠海市', value: '440400' }
  ],
  110100: [
    { label: '东城区', value: '110101' },
    { label: '西城区', value: '110102' },
    { label: '朝阳区', value: '110105' }
  ],
  440100: [
    { label: '荔湾区', value: '440103' },
    { label: '越秀区', value: '440104' },
    { label: '海珠区', value: '440105' }
  ],
  440300: [
    { label: '罗湖区', value: '440303' },
    { label: '福田区', value: '440304' }
  ],
  440400: [
    { label: '香洲区', value: '440402' },
    { label: '斗门区', value: '440403' }
  ]
}

// 初始化数据源
const columns = ref([
  district[0],
  district[district[0][0].value],
  district[district[district[0][0].value][0].value]
])

const onChangeDistrict: PickerViewColumnChange = (pickerView, selects, columnIndex, resolve) => {
  const item = (selects as Record<string, any>[])[columnIndex]
  if (columnIndex === 0) {
    // 第一列变化，更新第二列和第三列
    pickerView.setColumnData(1, district[item.value])
    pickerView.setColumnData(2, district[district[item.value][0].value])
  } else if (columnIndex === 1) {
    // 第二列变化，更新第三列
    pickerView.setColumnData(2, district[item.value])
  }
  resolve()
}

function handleConfirm({ value }: any) {
  console.log('选中值:', value)
}
</script>
```

### 示例三：多列选择器

传入二维数组实现多列独立选择，每列可独立滚动选中。

```vue
<template>
  <wd-picker
    label="学校与专业"
    v-model="value"
    :columns="columns"
    :display-format="displayFormat"
    @confirm="handleConfirm"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { PickerDisplayFormat } from '@/uni_modules/wot-ui-plus/components/wd-picker/types'
import type { ColumnItem } from '@/uni_modules/wot-ui-plus/components/wd-picker-view/types'

const value = ref(['中山大学', '软件工程'])

const columns = ref([
  ['中山大学', '中南大学', '华南理工大学'],
  ['计算机科学与技术', '软件工程', '通信工程', '法学', '经济学']
])

// 自定义展示格式
const displayFormat: PickerDisplayFormat = (items) => {
  return (items as ColumnItem[])
    .map((item) => item.label)
    .join(' - ')
}

function handleConfirm({ value }: any) {
  console.log('选中值:', value)
}
</script>
```

### 示例四：确认前校验

通过 `before-confirm` 函数在确认前执行异步校验，校验不通过时阻止确认并显示提示。

```vue
<template>
  <wd-picker
    label="需要校验的选择"
    v-model="value"
    :columns="columns"
    :before-confirm="beforeConfirm"
    @confirm="handleConfirm"
  />
  <wd-toast />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'
import type { PickerBeforeConfirm } from '@/uni_modules/wot-ui-plus/components/wd-picker/types'

const toast = useToast()
const value = ref('')

const columns = ref(['选项一', '选项二', '选项三', '选项四', '选项五'])

const beforeConfirm: PickerBeforeConfirm = (value, resolve, picker) => {
  // 设置加载状态
  picker.setLoading(true)
  setTimeout(() => {
    picker.setLoading(false)
    // 模拟校验逻辑
    if (value === '选项二' || value === '选项三') {
      resolve(false)
      toast.error('校验不通过，请重新选择')
    } else {
      resolve(true)
    }
  }, 1000)
}

function handleConfirm({ value }: any) {
  console.log('确认选中:', value)
}
</script>
```

### 示例五：内联选择器 wd-picker-view 与可清空功能

`wd-picker-view` 直接嵌入页面中使用，实时响应变化，同时展示 `wd-picker` 的 `clearable` 可清空功能。

```vue
<template>
  <!-- wd-picker-view 内联使用 -->
  <view class="picker-view-wrapper">
    <wd-picker-view
      v-model="pickerViewValue"
      :columns="pickerViewColumns"
      @change="handleChange"
    />
    <text>当前选中值: {{ pickerViewValue }}</text>
  </view>

  <!-- wd-picker 可清空功能 -->
  <wd-picker
    label="可清空选择"
    v-model="clearableValue"
    :columns="clearableColumns"
    clearable
    @clear="handleClear"
    @confirm="handleConfirm"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// wd-picker-view 示例
const pickerViewValue = ref('选项一')
const pickerViewColumns = ref([
  { label: '选项一', value: '1' },
  { label: '选项二', value: '2' },
  { label: '选项三（禁用）', value: '3', disabled: true },
  { label: '选项四', value: '4' },
  { label: '选项五', value: '5' }
])

function handleChange({ value }: any) {
  console.log('picker-view 值变化:', value)
}

// wd-picker 可清空示例
const clearableValue = ref('选项二')
const clearableColumns = ref(['选项一', '选项二', '选项三', '选项四'])

function handleClear() {
  clearableValue.value = ''
  toast.success('已清空')
}

function handleConfirm({ value }: any) {
  console.log('确认选中:', value)
}
</script>

<style scoped>
.picker-view-wrapper {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
}
</style>
```

## 注意事项

- **数据源格式**：`columns` 支持一维数组（单列）和二维数组（多列），数组元素可以是字符串、数字或 `ColumnItem` 对象（包含 `value`、`label`、`disabled` 字段）。不能混用原始值和对象类型，否则会抛出异常。
- **多级联动异步处理**：`column-change` 回调函数支持同步和异步两种模式。如果函数参数少于 4 个则为同步调用；如果参数为 4 个（包含 `resolve`），则需要在异步操作完成后调用 `resolve()` 通知组件更新完成。
- **禁用选项的自动修正**：当选中项被标记为 `disabled` 时，组件会自动寻找距离最近的未禁用选项进行替代。如果该列全部禁用，则保持当前位置不变。
- **滑动中确认处理**：当用户快速滚动后立即点击确认按钮，组件会等待滚动动画结束后再执行确认操作，确保获取到最终的选中值。
- **取消时的数据回滚**：点击取消按钮后，`wd-picker` 会将数据源回滚到弹窗打开前的状态，避免多级联动场景下数据源不一致。
- **displayFormat 类型校验**：`displayFormat` 必须是函数类型，否则会在控制台输出错误提示。
- **immediateChange 平台限制**：`immediate-change` 属性仅在微信小程序和支付宝小程序中生效，其他平台会在滚动动画结束后触发 change 事件。
- **rootPortal 使用场景**：当选择器弹窗在 fixed 定位元素内部或某些特殊布局中无法正常显示时，可以设置 `root-portal` 为 true，将弹窗从当前 DOM 层级中脱离出来。
- **wd-picker-view 必须传入 modelValue**：`wd-picker-view` 的 `modelValue` 是必填属性，即使初始值可以为空字符串或空数组也必须显式绑定。
- **columns 为空时的处理**：当 `columns` 被设置为空数组时，组件会自动清空 `pickerValue` 和 `showValue`，避免显示异常。
- **自定义 key 名映射**：当数据源的字段名不是默认的 `value` 和 `label` 时，可以通过 `valueKey` 和 `labelKey` 属性进行自定义映射。
- **表单校验配合**：使用 `wd-picker` 进行表单校验时，必须设置 `prop` 属性与 `wd-form-item` 的 `prop` 对应，同时通过 `rules` 属性传入校验规则。
