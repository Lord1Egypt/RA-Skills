# ColPicker 多列选择器


## 组件概况

ColPicker 组件是一个基于弹窗面板的多列级联选择器。用户通过点击列标题切换不同列的列表，逐列进行选择后确认完成。组件支持异步加载下级数据、自定义展示文案、选择前校验、自动补全列数据等高级功能，并与表单校验系统深度集成。

### 核心功能描述

- **多列级联选择**：支持二维数组数据展示，通过列标题栏切换不同列，逐列递进选择
- **列导航指示器**：顶部列标题带有底部指示线，点击可快速切换列，滑动时自动跟随
- **异步数据加载**：通过 columnChange 回调异步获取下一列数据，加载期间自动显示 loading 状态
- **自动补全**：autoComplete 模式下，当 columns 数据不足时自动触发 columnChange 补齐数据
- **自定义展示文案**：displayFormat 函数可自定义选择结果的展示格式
- **选择前校验**：beforeConfirm 支持在确认前进行异步校验，校验不通过可阻止选择
- **表单集成**：原生支持 wd-form 表单校验，支持 prop 和 rules 属性
- **自定义触发器**：支持通过默认插槽使用自定义组件（如按钮）触发选择器
- **选项禁用与提示**：支持单个选项禁用，支持在选项下方显示提示文案
- **弹窗控制**：支持点击遮罩关闭、zIndex 层级控制、底部安全区域适配

### 适用业务场景

- 省市区/行政区划选择
- 商品多级分类选择
- 组织架构选择（部门-团队-人员）
- 任何需要多级联动的选择场景
- 需要异步加载子级数据的层级选择

---

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| modelValue / v-model | 选中项，数组形式 | Array<string \| number> | - | - | - |
| columns | 选择器数据，二维数组 | Record<string, any>[][] | - | [] | - |
| label | 选择器左侧文案 | string | - | - | - |
| labelWidth | 左侧标题宽度 | string | - | 33% | - |
| useLabelSlot | 是否使用 label 插槽 | boolean | - | false | - |
| useDefaultSlot | 是否使用默认插槽（自定义触发器） | boolean | - | false | - |
| disabled | 是否禁用 | boolean | - | false | - |
| readonly | 是否只读 | boolean | - | false | - |
| placeholder | 选择器占位符 | string | - | - | - |
| title | 弹出层标题 | string | - | - | - |
| columnChange | 列变化回调，用于动态加载下一列数据 | Function | - | - | - |
| displayFormat | 自定义展示文案的格式化函数 | Function | - | - | - |
| beforeConfirm | 确定前校验函数 | Function | - | - | - |
| alignRight | 选择器的值是否靠右展示 | boolean | - | false | - |
| error | 是否为错误状态（值为红色） | boolean | - | false | - |
| required | 是否必填 | boolean | - | false | - |
| size | 选择器大小 | string | large | - | - |
| valueKey | 选项对象中 value 对应的 key | string | - | value | - |
| labelKey | 选项对象中展示文本对应的 key | string | - | label | - |
| tipKey | 选项对象中提示文案对应的 key | string | - | tip | - |
| loadingColor | loading 图标的颜色 | string | - | #4D80F0 | - |
| closeOnClickModal | 点击遮罩是否关闭 | boolean | - | true | - |
| autoComplete | 是否自动触发 columnChange 补全数据 | boolean | - | false | - |
| zIndex | 弹窗层级 | number | - | 15 | - |
| safeAreaInsetBottom | 是否设置底部安全距离 | boolean | - | true | - |
| ellipsis | 是否超出隐藏 | boolean | - | false | - |
| prop | 表单域 model 字段名，用于表单校验 | string | - | - | - |
| rules | 表单验证规则 | FormItemRule[] | - | [] | - |
| lineWidth | 底部条宽度，单位像素 | number \| string | - | - | - |
| lineHeight | 底部条高度，单位像素 | number \| string | - | - | - |
| customViewClass | value 外部自定义样式类 | string | - | '' | - |
| customLabelClass | label 外部自定义样式类 | string | - | '' | - |
| customValueClass | value 外部自定义样式类 | string | - | '' | - |
| rootPortal | 是否从页面中脱离出来 | boolean | - | false | - |
| markerSide | 必填标记位置 | string | before / after | before | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 | 最低版本 |
|--------|------|----------|----------|
| update:modelValue | 绑定值变化时触发 | 选中项的值数组 | - |
| confirm | 点击确定时触发 | { value: 选中值数组, selectedItems: 选中项对象数组 } | - |
| close | 关闭弹框时触发 | - | - |

### Methods

通过组件 ref 可调用以下方法：

| 方法名 | 说明 | 参数 | 返回值 |
|--------|------|------|--------|
| open | 打开选择器弹框 | - | - |
| close | 关闭选择器弹框 | - | - |

### Slots

| 插槽名 | 说明 | 最低版本 |
|--------|------|----------|
| label | 左侧标题插槽，覆盖 label 属性 | - |
| default | 默认插槽，用于自定义触发选择器的元素（需配合 useDefaultSlot） | - |

---

## 使用示例

### 示例一：基本用法

最基础的多列选择器，通过 columnChange 回调动态加载下一列数据。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 基本用法：通过 columnChange 动态加载数据 -->
      <wd-col-picker
        label="选择地址"
        v-model="value1"
        :columns="columns"
        :column-change="columnChange"
        @confirm="handleConfirm"
      />

      <!-- 设置标题 -->
      <wd-col-picker
        label="选择地址"
        v-model="value2"
        title="请选择所在地区"
        :columns="columns"
        :column-change="columnChange"
      />

      <!-- 值靠右展示 -->
      <wd-col-picker
        label="选择地址"
        v-model="value3"
        align-right
        :columns="columns"
        :column-change="columnChange"
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { ColPickerColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-col-picker/types'

// 假设 colPickerData 为省市区数据源
const colPickerData = ref<Record<string, any>[]>([])
const columns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text
  }))
])

const value1 = ref<any[]>([])
const value2 = ref<any[]>([])
const value3 = ref<any[]>([])

// 根据当前选中项动态加载下一列数据
const columnChange: ColPickerColumnChange = ({ selectedItem, resolve, finish }) => {
  // 根据 selectedItem.value 获取子级数据
  const children = getChildrenByValue(selectedItem.value)
  if (children && children.length) {
    resolve(
      children.map((item) => ({
        value: item.value,
        label: item.text
      }))
    )
  } else {
    // 没有子级数据时调用 finish 结束选择
    finish()
  }
}

function getChildrenByValue(value: string): any[] {
  // 实际项目中应从数据源或接口获取
  return []
}

function handleConfirm({ value, selectedItems }: any) {
  console.log('选中值：', value)
  console.log('选中项：', selectedItems)
}
</script>
```

### 示例二：异步加载与自动补全

数据异步获取场景，以及使用 autoComplete 自动补全已选值对应的列数据。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 异步加载数据（带有 loading 状态和失败处理） -->
      <wd-col-picker
        label="选择地址"
        v-model="value1"
        :columns="columns"
        :column-change="asyncColumnChange"
      />

      <!-- 自动补全模式：columns 为空时自动触发 columnChange -->
      <wd-col-picker
        label="初始选项"
        v-model="value2"
        :columns="emptyColumns"
        :column-change="columnChange"
        auto-complete
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import type { ColPickerColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-col-picker/types'

const colPickerData = ref<Record<string, any>[]>([])
const columns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text
  }))
])
const emptyColumns = ref<any[]>([])
const value1 = ref<any[]>([])
const value2 = ref<string[]>([])

onMounted(() => {
  // 设置初始选中值，autoComplete 会自动加载对应列数据
  value2.value = ['150000', '150100', '150121']
})

// 异步加载，模拟接口请求
const asyncColumnChange: ColPickerColumnChange = ({ selectedItem, resolve, finish }) => {
  setTimeout(() => {
    // 模拟随机失败
    if (Math.random() > 0.7) {
      finish(false)
      console.error('数据请求失败，请重试')
      return
    }
    const children = getChildrenByValue(selectedItem.value)
    if (children && children.length) {
      resolve(
        children.map((item) => ({
          value: item.value,
          label: item.text
        }))
      )
    } else {
      finish()
    }
  }, 300)
}

const columnChange: ColPickerColumnChange = async ({ selectedItem, resolve, finish }) => {
  await sleep(0.3)
  const children = getChildrenByValue(selectedItem.value)
  if (children && children.length) {
    resolve(
      children.map((item) => ({
        value: item.value,
        label: item.text
      }))
    )
  } else {
    finish()
  }
}

function getChildrenByValue(value: string): any[] {
  // 实际项目中应从数据源或接口获取
  return []
}

function sleep(second: number = 1) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true)
    }, 1000 * second)
  })
}
</script>
```

### 示例三：禁用状态与选项配置

组件级别禁用、只读状态，以及单个选项的禁用和提示。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 禁用状态 -->
      <wd-col-picker
        label="禁用"
        disabled
        v-model="value1"
        :columns="columns"
        :column-change="columnChange"
      />

      <!-- 只读状态 -->
      <wd-col-picker
        label="只读"
        readonly
        v-model="value2"
        :columns="columns"
        :column-change="columnChange"
      />

      <!-- 禁用特定选项 -->
      <wd-col-picker
        label="禁用选项"
        v-model="value3"
        :columns="disabledColumns"
        :column-change="columnChange"
      />

      <!-- 选项带有提示信息 -->
      <wd-col-picker
        label="选项提示信息"
        v-model="value4"
        :columns="tipColumns"
        :column-change="columnChange"
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { ColPickerColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-col-picker/types'

const colPickerData = ref<Record<string, any>[]>([])
const columns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text
  }))
])

const value1 = ref<any[]>(['130000', '130200', '130204'])
const value2 = ref<any[]>(['130000', '130200', '130204'])
const value3 = ref<any[]>([])
const value4 = ref<any[]>([])

// 带禁用选项的数据
const disabledColumns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text,
    disabled: item.value === '140000'
  }))
])

// 带提示信息的选项数据
const tipColumns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text,
    disabled: item.value === '140000',
    tip:
      item.value === '140000'
        ? '该地区无货暂时无法选择'
        : item.value === '150000'
          ? '该地区配送时间可能较长'
          : ''
  }))
])

const columnChange: ColPickerColumnChange = ({ selectedItem, resolve, finish }) => {
  const children = getChildrenByValue(selectedItem.value)
  if (children && children.length) {
    resolve(
      children.map((item) => ({
        value: item.value,
        label: item.text
      }))
    )
  } else {
    finish()
  }
}

function getChildrenByValue(value: string): any[] {
  return []
}
</script>
```

### 示例四：自定义展示与选择前校验

使用 displayFormat 自定义选中结果的展示文案，以及通过 beforeConfirm 进行确认前校验。

```vue
<template>
  <view>
    <wd-cell-group border>
      <!-- 自定义展示文案格式 -->
      <wd-col-picker
        label="展示格式化"
        v-model="value1"
        :columns="columns"
        :column-change="columnChange"
        :display-format="displayFormat"
      />

      <!-- 确认前校验 -->
      <wd-col-picker
        label="before-confirm"
        v-model="value2"
        :columns="columns"
        :column-change="columnChange"
        :before-confirm="beforeConfirm"
      />

      <!-- 错误状态 -->
      <wd-col-picker
        label="错误"
        error
        v-model="value3"
        :columns="columns"
        :column-change="columnChange"
      />

      <!-- 必填状态 -->
      <wd-col-picker
        label="必填"
        required
        v-model="value4"
        :columns="columns"
        :column-change="columnChange"
      />

      <!-- 必填星号在右侧 -->
      <wd-col-picker
        label="必填星号在右"
        required
        v-model="value5"
        :columns="columns"
        :column-change="columnChange"
        marker-side="after"
      />
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { ColPickerColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-col-picker/types'

const colPickerData = ref<Record<string, any>[]>([])
const columns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text
  }))
])

const value1 = ref<any[]>(['130000', '130200', '130204'])
const value2 = ref<any[]>([])
const value3 = ref<any[]>([])
const value4 = ref<any[]>([])
const value5 = ref<any[]>([])

// 自定义展示文案格式
const displayFormat = (selectedItems: Record<string, any>[]) => {
  // 将倒数第二列和最后一列的值用横线连接展示
  return selectedItems[selectedItems.length - 2].label + '-' + selectedItems[selectedItems.length - 1].label
}

// 确认前校验
const beforeConfirm = (
  value: (string | number)[],
  selectedItems: Record<string, any>[],
  resolve: (isPass: boolean) => void
) => {
  // 校验第三列的值是否大于指定阈值
  if (parseInt(String(value[2])) > 120000) {
    console.error('该地区库存不足')
    resolve(false)
  } else {
    resolve(true)
  }
}

const columnChange: ColPickerColumnChange = ({ selectedItem, resolve, finish }) => {
  const children = getChildrenByValue(selectedItem.value)
  if (children && children.length) {
    resolve(
      children.map((item) => ({
        value: item.value,
        label: item.text
      }))
    )
  } else {
    finish()
  }
}

function getChildrenByValue(value: string): any[] {
  return []
}
</script>
```

### 示例五：自定义触发器与大尺寸样式

使用默认插槽自定义触发选择器的元素，以及大尺寸样式展示。

```vue
<template>
  <view>
    <!-- 大尺寸样式 -->
    <wd-col-picker
      label="选择地址"
      v-model="value1"
      size="large"
      :columns="columns"
      :column-change="columnChange"
    />

    <!-- 不传 label -->
    <wd-col-picker
      v-model="value2"
      :columns="columns"
      :column-change="columnChange"
    />

    <!-- 自定义触发按钮 -->
    <view style="margin-left: 15px">
      <view style="margin-bottom: 10px">当前选中项: {{ displayValue }}</view>

      <wd-col-picker
        v-model="value3"
        use-default-slot
        :columns="columns"
        :column-change="columnChange"
        style="display: inline-block"
        @confirm="handleConfirm"
      >
        <wd-button>选择地址</wd-button>
      </wd-col-picker>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { ColPickerColumnChange } from '@/uni_modules/wot-ui-plus/components/wd-col-picker/types'

const colPickerData = ref<Record<string, any>[]>([])
const columns = ref<any[]>([
  colPickerData.value.map((item) => ({
    value: item.value,
    label: item.text
  }))
])

const value1 = ref<any[]>([])
const value2 = ref<any[]>([])
const value3 = ref<any[]>([])
const displayValue = ref<string>('')

const columnChange: ColPickerColumnChange = ({ selectedItem, resolve, finish }) => {
  const children = getChildrenByValue(selectedItem.value)
  if (children && children.length) {
    resolve(
      children.map((item) => ({
        value: item.value,
        label: item.text
      }))
    )
  } else {
    finish()
  }
}

function handleConfirm({ selectedItems }: any) {
  displayValue.value = selectedItems
    .map((item: any) => item.label)
    .join('')
}

function getChildrenByValue(value: string): any[] {
  return []
}
</script>
```

---

## 注意事项

1. **columns 数据格式**：`columns` 属性必须为二维数组，即 `Record<string, any>[][]`。第一层数组的每个元素代表一列的数据。如果传入的 columns 不是二维数组，组件会在控制台输出错误提示。

2. **columnChange 回调机制**：`columnChange` 是 ColPicker 的核心回调函数。当用户选择某一列的选项时触发，回调参数包含 `selectedItem`（当前选中项对象）、`index`（当前列下标）、`rowIndex`（选中项在该列的下标）、`resolve`（用于传入下一列数据）、`finish`（用于结束选择流程）。必须调用 `resolve` 或 `finish` 来完成数据加载流程。

3. **resolve 与 finish 的使用**：
   - 调用 `resolve(nextColumn)` 传入下一列的数据数组，组件会自动切换到下一列
   - 调用 `finish()` 表示当前已选到最后一列，组件会自动触发确认
   - 调用 `finish(false)` 表示选择流程异常终止（如请求失败），不会触发确认

4. **autoComplete 自动补全**：当 `autoComplete` 为 `true` 且 columns 为空数组或 columns 数组长度小于 modelValue 数组长度时，组件会自动触发 `columnChange` 来补全数据。适用于编辑场景中已保存了选中值但需要动态加载对应列数据的场景。

5. **displayFormat 展示格式化**：`displayFormat` 接收已选中项的对象数组作为参数，返回一个字符串用于在 cell 中展示。如果不设置该函数，组件默认将所有选中项的 labelKey 字段拼接展示。

6. **beforeConfirm 校验时机**：`beforeConfirm` 在选择流程结束（调用 `finish()`）时触发，用于在最终确认前进行校验。校验通过需调用 `resolve(true)`，不通过调用 `resolve(false)`。

7. **选项禁用与提示**：在 columns 数据中，为选项对象设置 `disabled: true` 可禁用该选项。设置 `tip` 字段可在选项 label 下方显示提示文案（对应 tipKey，默认为 `tip`）。

8. **自定义字段名映射**：通过 `valueKey`、`labelKey`、`tipKey` 可以自定义选项对象中 value、label、tip 字段对应的 key 名，默认分别为 `value`、`label`、`tip`。

9. **选择取消回退**：当用户在弹窗中修改选择后关闭弹窗（未点击确认），组件会自动恢复到上一次确认的状态。

10. **自定义触发器**：使用默认插槽时，必须设置 `use-default-slot` 为 `true`，此时组件不会渲染默认的 cell，而是将插槽内容作为触发选择器的元素。

11. **rootPortal 脱离文档流**：当 `rootPortal` 为 `true` 时，弹窗会从页面文档流中脱离出来，用于解决 fixed 定位失效的问题。在 H5 端使用 teleport，在 APP 端使用 renderjs，在小程序端使用 root-portal。

12. **表单校验集成**：使用 `prop` 和 `rules` 属性时，需要将组件放置在 `wd-form` 组件内，以便参与表单校验流程。
