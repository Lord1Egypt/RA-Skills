# SelectPicker 下拉选择器


## 组件概况

SelectPicker 下拉选择器组件是一个基于 ActionSheet 弹出面板的下拉选择组件，用于从预设选项列表中进行单选或多选操作。该组件内部使用 `wd-action-sheet` 作为弹出容器，结合 `wd-radio`/`wd-radio-group`（单选模式）或 `wd-checkbox`/`wd-checkbox-group`（多选模式）实现选项选择功能，同时内置搜索过滤、加载状态、确认前校验等能力。

组件支持单选（radio）和多选（checkbox）两种模式，通过 `type` 属性切换。单选模式下选择后自动确认（可通过 `showConfirm` 控制是否显示确认按钮），多选模式下必须点击确认按钮完成选择。选项数据通过一维数组 `columns` 传入，每项包含 `value` 和 `label` 字段。支持通过 `displayFormat` 自定义展示文案格式，通过 `beforeConfirm` 进行确认前校验，通过 `filterable` 开启本地搜索过滤。

## 核心功能描述

- **单选/多选模式**：通过 `type` 属性切换，`radio` 为单选模式，`checkbox` 为多选模式
- **本地搜索过滤**：通过 `filterable` 开启搜索功能，输入关键字实时过滤选项，匹配文字高亮显示
- **确认按钮控制**：单选模式默认不显示确认按钮（选择即确认），可通过 `showConfirm` 控制显示；多选模式始终显示确认按钮
- **选中项自动滚动**：重新打开弹框时自动滚动到已选中项位置，通过 `scrollIntoView` 控制
- **确认前校验**：通过 `beforeConfirm` 钩子在确认前进行校验，支持异步校验逻辑
- **自定义展示格式**：通过 `displayFormat` 函数自定义选择器外部显示的文案格式
- **可清空**：通过 `clearable` 属性显示清除按钮，点击可清空已选项
- **加载状态**：通过 `loading` 属性展示加载动画，适用于异步加载选项数据的场景
- **禁用/只读**：支持设置组件禁用（disabled）和只读（readonly）状态
- **最小/最大选中数量**：多选模式下支持设置 `min` 和 `max` 限制选中数量范围
- **表单校验集成**：支持 `prop` 和 `rules` 属性与 `wd-form` 组件配合进行表单校验
- **丰富的自定义样式**：支持自定义标签、值、内容区域的样式类名
- **禁用选项**：选项数据中设置 `disabled: true` 可禁用单个选项
- **箭头/清除图标切换**：有内容且可清空时显示清除图标，否则显示箭头图标
- **外部插槽支持**：支持通过默认插槽完全自定义触发器，替代默认的 cell 展示

## 适用业务场景

- **地址选择**：在表单中选择省市区等地址信息，支持单选模式
- **分类筛选**：商品列表页选择商品分类，支持单选快速切换
- **标签多选**：用户兴趣标签选择、文章标签添加等多选场景
- **搜索选择**：选项较多时开启搜索功能，快速定位目标选项
- **异步加载选项**：选项数据需要从接口获取时，展示 loading 加载状态
- **表单必填项**：配合表单组件使用，支持必填标记和表单校验
- **自定义触发器**：使用按钮或其他元素替代默认 cell 作为触发器

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| modelValue | string \| number \| boolean \| Array | - | 是 | 选中项，`type` 为 `checkbox` 时类型为 array；`type` 为 `radio` 时类型为 string/number/boolean，支持 v-model 双向绑定 |
| columns | Record\<string, any\>[] | [] | 否 | 选择器数据，一维数组，每项包含 value（值）和 label（展示文本），支持 disabled 字段 |
| type | 'checkbox' \| 'radio' | 'checkbox' | 否 | 选择器类型，`checkbox` 为多选，`radio` 为单选 |
| label | string | - | 否 | 选择器左侧文案（标题） |
| labelWidth | string | '33%' | 否 | 设置左侧标题宽度 |
| placeholder | string | '请选择'（跟随国际化） | 否 | 选择器占位符，未选择时展示 |
| title | string | '请选择'（跟随国际化） | 否 | 弹出层标题，显示在面板顶部 |
| disabled | boolean | false | 否 | 是否禁用选择器，禁用后不可点击 |
| readonly | boolean | false | 否 | 是否只读，只读状态下不可点击但样式不同于禁用 |
| alignRight | boolean | false | 否 | 选择器的值是否靠右展示 |
| error | boolean | false | 否 | 是否为错误状态，错误状态时右侧内容为红色 |
| required | boolean | false | 否 | 必填样式，在标题前显示必填星号标记 |
| markerSide | 'before' \| 'after' | 'before' | 否 | 必填标记位置，`before` 在标题前，`after` 在标题后 |
| size | string | - | 否 | 选择器大小，可选值：large |
| center | boolean | false | 否 | 是否垂直居中 |
| checkedColor | string | - | 否 | 选中项的颜色（单/复选框） |
| min | number | 0 | 否 | 最小选中数量，仅在复选框类型下生效 |
| max | number | 0 | 否 | 最大选中数量，0 为无限数量，仅在复选框类型下生效 |
| selectSize | string | - | 否 | 设置 picker 内部选项组尺寸大小（单/复选框） |
| loading | boolean | false | 否 | 是否显示加载状态，显示时禁止滚动和选择 |
| loadingColor | string | '#4D80F0' | 否 | 加载状态的颜色，只能使用十六进制色值，且不能使用缩写 |
| valueKey | string | 'value' | 否 | 选项对象中 value 对应的 key |
| labelKey | string | 'label' | 否 | 选项对象中展示文本对应的 key |
| confirmButtonText | string | '确认'（跟随国际化） | 否 | 确认按钮文案 |
| closeOnClickModal | boolean | true | 否 | 点击遮罩是否关闭面板 |
| filterable | boolean | false | 否 | 是否开启搜索功能（目前只支持本地搜索） |
| filterPlaceholder | string | '搜索'（跟随国际化） | 否 | 搜索框占位符 |
| showConfirm | boolean | true | 否 | 是否显示确认按钮（仅 radio 类型生效），默认值为 true |
| scrollIntoView | boolean | true | 否 | 重新打开时是否滚动到选中项 |
| clearable | boolean | false | 否 | 是否显示清空按钮 |
| ellipsis | boolean | false | 否 | 选择器展示文本是否超出隐藏 |
| zIndex | number | 15 | 否 | 弹窗层级 |
| safeAreaInsetBottom | boolean | true | 否 | 弹出面板是否设置底部安全距离（iPhone X 类型的机型） |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） |
| prop | string | - | 否 | 表单域 model 字段名，在使用表单校验功能的情况下该属性是必填的 |
| rules | FormItemRule[] | [] | 否 | 表单验证规则，结合 wd-form 组件使用 |
| displayFormat | SelectPickerDisplayFormat | - | 否 | 自定义展示文案的格式化函数，返回一个字符串 |
| beforeConfirm | SelectPickerBeforeConfirm | - | 否 | 确定前校验函数，接收 `(value, resolve)` 参数，通过 resolve 继续执行 |
| customContentClass | string | '' | 否 | 自定义内容区域样式类名 |
| customLabelClass | string | '' | 否 | 自定义标签样式类名 |
| customValueClass | string | '' | 否 | 自定义值样式类名 |
| useLabelSlot | boolean | false | 否 | 已过时，可以直接使用 label 插槽，无需配置此选项 |
| useDefaultSlot | boolean | false | 否 | 已过时，可以直接使用默认插槽，无需配置此选项 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

| 事件名称 | 触发条件 | 回调参数 | 说明 |
| --- | --- | --- | --- |
| change | 选项发生变化时触发 | `{ value: string \| number \| boolean \| (string \| number \| boolean)[] }` | 单选时 value 为单值；多选时 value 为数组。radio 模式下如果未设置 `showConfirm` 为 false，选择后会自动触发 confirm |
| confirm | 点击确认按钮或单选模式下选择时触发 | `{ value: string \| number \| boolean \| (string \| number \| boolean)[], selectedItems: Record\<string, any\> \| Record\<string, any\>[] }` | value 为选中值；selectedItems 为选中项的完整对象（单选时为单个对象，多选时为对象数组） |
| cancel | 点击遮罩关闭面板时触发（未点击确认） | - | 无参数 |
| close | 面板关闭时触发 | - | 无参数 |
| open | 面板打开时触发 | - | 无参数 |
| clear | 点击清空按钮时触发 | - | 无参数 |
| update:modelValue | 选中值发生变化时触发（v-model 支持） | `value: string \| number \| boolean \| (string \| number \| boolean)[]` | 新的选中值 |

### Methods

通过 `defineExpose` 暴露的实例方法：

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| open | - | void | 打开选择器弹框 |
| close | - | void | 关闭选择器弹框，未确认时数据会还原复位 |

使用方式：通过 ref 获取组件实例后调用。

```ts
import { ref } from 'vue'

const selectPickerRef = ref()

// 打开弹框
selectPickerRef.value.open()

// 关闭弹框
selectPickerRef.value.close()
```

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 自定义触发器内容，替代默认的 wd-cell 展示，可插入按钮、自定义视图等作为打开选择器的触发元素 |
| label | - | 自定义左侧标签内容，替代默认的 label 文字展示 |

## 使用示例

### 示例 1：基础单选用法

效果说明：展示最基本的单选选择器用法。单选模式下点击选项即完成选择并自动关闭面板（`showConfirm` 默认为 true 时显示确认按钮，设置为 false 时选择即确认）。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-select-picker
        label="选择地址"
        v-model="value"
        type="radio"
        :columns="columns"
        :show-confirm="false"
        @confirm="handleConfirm"
      />
    </wd-cell-group>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value = ref<string>('')
const columns = ref<Record<string, any>[]>([
  { value: '101', label: '男装' },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' },
  { value: '104', label: '鞋靴' },
  { value: '105', label: '内衣配饰' }
])

function handleConfirm({ value }: { value: string }) {
  console.log('选中值：', value)
}
</script>
```

### 示例 2：多选模式

效果说明：展示多选选择器用法。多选模式下必须点击确认按钮完成选择，可设置最小/最大选中数量限制。确认时返回选中值数组和选中项完整对象数组。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-select-picker
        label="商品分类"
        v-model="multiValue"
        :columns="columns"
        :min="1"
        :max="3"
        @confirm="handleMultiConfirm"
      />
    </wd-cell-group>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const multiValue = ref<string[]>([])
const columns = ref<Record<string, any>[]>([
  { value: '101', label: '男装' },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' },
  { value: '104', label: '鞋靴' },
  { value: '105', label: '内衣配饰' },
  { value: '106', label: '箱包' }
])

function handleMultiConfirm({ value, selectedItems }: { value: string[], selectedItems: Record<string, any>[] }) {
  console.log('选中值：', value)
  console.log('选中项：', selectedItems)
}
</script>
```

### 示例 3：搜索过滤

效果说明：通过 `filterable` 属性开启本地搜索功能，面板顶部显示搜索输入框，输入关键字实时过滤选项列表，匹配的文字高亮显示。单选和多选模式均支持搜索。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-select-picker
        label="可搜索"
        v-model="searchValue"
        :columns="columns"
        filterable
        filter-placeholder="输入关键词搜索"
        @confirm="handleSearchConfirm"
      />
    </wd-cell-group>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchValue = ref<string[]>([])
const columns = ref<Record<string, any>[]>([
  { value: '101', label: '男装' },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' },
  { value: '104', label: '鞋靴' },
  { value: '105', label: '内衣配饰' },
  { value: '106', label: '箱包' },
  { value: '107', label: '美妆护肤' },
  { value: '108', label: '个性清洁' }
])

function handleSearchConfirm({ value }: { value: string[] }) {
  console.log('选中值：', value)
}
</script>
```

### 示例 4：自定义展示格式与确认前校验

效果说明：通过 `displayFormat` 自定义选择器外部显示的文案格式，通过 `beforeConfirm` 在确认前进行校验，校验不通过时阻止确认。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-select-picker
        label="展示格式化"
        v-model="formatValue"
        :columns="columns"
        :display-format="displayFormat"
        @confirm="handleFormatConfirm"
      />
      <wd-select-picker
        label="确认前校验"
        v-model="validateValue"
        :columns="columns"
        :before-confirm="beforeConfirm"
        @confirm="handleValidateConfirm"
      />
    </wd-cell-group>
    <wd-toast />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { SelectPickerBeforeConfirm, SelectPickerDisplayFormat } from '@/uni_modules/wot-ui-plus/components/wd-select-picker/types'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()
const formatValue = ref<string[]>([])
const validateValue = ref<string[]>([])

const columns = ref<Record<string, any>[]>([
  { value: '101', label: '男装' },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' },
  { value: '104', label: '鞋靴' }
])

// 自定义展示格式
const displayFormat: SelectPickerDisplayFormat = (items, columns) => {
  let showValue = ''
  columns.forEach((column) => {
    ;(items as (string | number | boolean)[]).forEach((item, index) => {
      if (column.value === item) {
        showValue += `${item}: ${column.label} ${index + 1 < (items as (string | number | boolean)[]).length ? '--' : ''} `
      }
    })
  })
  return showValue
}

// 确认前校验
const beforeConfirm: SelectPickerBeforeConfirm = (value, resolve) => {
  if ((value as string[]).length > 0) {
    toast.error('暂时无法选择商品')
    resolve(false)
  } else {
    resolve(true)
  }
}

function handleFormatConfirm({ value }: { value: string[] }) {
  console.log('选中值：', value)
}

function handleValidateConfirm({ value }: { value: string[] }) {
  console.log('选中值：', value)
}
</script>
```

### 示例 5：自定义触发器与禁用状态

效果说明：通过默认插槽自定义触发器，使用按钮替代默认的 cell 作为打开选择器的触发元素。同时展示禁用选项、禁用组件、只读等状态。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 禁用组件 -->
      <wd-select-picker label="禁用" disabled v-model="disabledValue" :columns="columns" />
      <!-- 只读组件 -->
      <wd-select-picker label="只读" readonly v-model="readonlyValue" :columns="columns" />
      <!-- 禁用特定选项 -->
      <wd-select-picker label="禁用选项" v-model="disabledOptionValue" :columns="disabledColumns" />
      <!-- 可清空 -->
      <wd-select-picker
        label="可清空"
        clearable
        type="radio"
        :show-confirm="false"
        v-model="clearableValue"
        :columns="columns"
      />
    </wd-cell-group>

    <!-- 自定义触发器 -->
    <demo-block title="自定义选择器" transparent>
      <view style="margin-left: 15px">
        <view style="margin-bottom: 10px">当前选中项: {{ customShow }}</view>
        <wd-select-picker v-model="customValue" :columns="columns" @confirm="handleCustomConfirm" style="display: inline-block">
          <wd-button>唤起多选</wd-button>
        </wd-select-picker>
      </view>
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const columns = ref<Record<string, any>[]>([
  { value: '101', label: '男装' },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' },
  { value: '104', label: '鞋靴' }
])

const disabledColumns = ref<Record<string, any>[]>([
  { value: '101', label: '男装', disabled: true },
  { value: '102', label: '奢品' },
  { value: '103', label: '女装' }
])

const disabledValue = ref<string[]>(['102'])
const readonlyValue = ref<string[]>(['103'])
const disabledOptionValue = ref<string[]>([])
const clearableValue = ref<string>('101')
const customValue = ref<string[]>(['102'])
const customShow = ref<string>('奢品')

function handleCustomConfirm({ value, selectedItems }: { value: string[], selectedItems: Record<string, any>[] }) {
  customShow.value = selectedItems
    .map((item: any) => item.label)
    .join(', ')
}
</script>
```

### 示例 6：加载状态与表单集成

效果说明：展示 loading 加载状态，适用于选项数据异步加载的场景。同时展示与表单校验的集成用法。

```vue
<template>
  <view>
    <wd-form ref="formRef" :model="formData">
      <wd-cell-group border>
        <wd-select-picker
          label="商品分类"
          v-model="formData.category"
          :columns="columns"
          :loading="isLoading"
          required
          prop="category"
          :rules="[{ required: true, message: '请选择商品分类' }]"
          @confirm="handleFormConfirm"
        />
      </wd-cell-group>
    </wd-form>
    <wd-button type="primary" @click="submitForm">提交</wd-button>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const formRef = ref()
const isLoading = ref(true)
const columns = ref<Record<string, any>[]>([])
const formData = ref({
  category: []
})

// 模拟异步加载选项数据
onMounted(() => {
  setTimeout(() => {
    columns.value = [
      { value: '101', label: '男装' },
      { value: '102', label: '奢品' },
      { value: '103', label: '女装' }
    ]
    isLoading.value = false
  }, 1500)
})

function handleFormConfirm({ value }: { value: string[] }) {
  console.log('选中值：', value)
}

async function submitForm() {
  try {
    await formRef.value.validate()
    console.log('表单校验通过', formData.value)
  } catch (error) {
    console.error('表单校验失败', error)
  }
}
</script>
```

## 注意事项

1. **modelValue 类型差异**：`type` 为 `checkbox` 时，`modelValue` 必须为数组类型；`type` 为 `radio` 时，`modelValue` 为字符串、数字或布尔值。类型不匹配会导致选择异常。

2. **取消时数据还原**：用户在未点击确认的情况下关闭面板（如点击遮罩），已做的选择会还原复位，不会生效。这是为了防止误操作导致的数据变更。

3. **单选模式自动确认**：单选模式下如果 `showConfirm` 为 true（默认），选择后需点击确认按钮；如果 `showConfirm` 设置为 false，选择后立即确认并关闭面板。

4. **搜索高亮实现**：搜索功能通过正则表达式匹配，将匹配到的文字标记为 active 类型并使用 `.wd-select-picker__text-active` 样式类高亮显示。搜索仅支持本地过滤，不支持远程搜索。

5. **beforeConfirm 校验**：`beforeConfirm` 函数接收 `(value, resolve)` 参数，校验通过调用 `resolve(true)`，校验失败调用 `resolve(false)`。适用于需要异步校验或条件判断的场景。

6. **scrollIntoView 滚动逻辑**：重新打开弹框时，组件会自动滚动到第一个已选中项的位置。通过计算滚动视图容器和目标项的位置关系，设置 `scrollTop` 值实现。如果所有选中项都在可视区域内，则不滚动。

7. **loading 状态行为**：设置 `loading` 为 true 时，滚动区域禁止滚动（`scroll-y="!loading"`），底部显示加载动画。适用于选项数据从接口异步加载的场景。

8. **clearable 显示条件**：清除按钮仅在 `clearable` 为 true、非禁用状态、非只读状态且有选中值时显示。显示清除按钮时，右侧箭头图标自动隐藏。

9. **columns 数据格式**：`columns` 为一维数组，每项默认使用 `value` 作为值、`label` 作为展示文本。可通过 `valueKey` 和 `labelKey` 自定义字段名。选项可设置 `disabled: true` 禁用单个选项。

10. **自定义样式类**：`customContentClass` 用于自定义面板内容区域样式类，`customLabelClass` 用于自定义标签样式类，`customValueClass` 用于自定义值样式类，`customHeaderClass` 用于自定义面板头部样式类。

11. **min/max 限制**：多选模式下，`min` 控制最少选中数量，`max` 控制最多选中数量（0 为不限制）。这些限制由 `wd-checkbox-group` 组件内部处理。

12. **表单校验**：通过 `prop` 和 `rules` 属性与 `wd-form` 组件配合使用，`prop` 对应 `form` 模型中的字段名。支持必填校验和其他自定义校验规则。
