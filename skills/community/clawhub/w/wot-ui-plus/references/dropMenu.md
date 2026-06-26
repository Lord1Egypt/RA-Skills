# DropMenu 下拉菜单


## 组件概况

DropMenu 下拉菜单组件用于在导航栏或工具栏中展示可展开的下拉筛选菜单，用户点击菜单项后弹出选项列表进行选择。该组件由 `wd-drop-menu`（下拉菜单容器）和 `wd-drop-menu-item`（下拉菜单子项）两个关联组件组成，支持向下和向上两种弹出方向，内置遮罩层管理和多菜单互斥关闭机制。每个菜单项可配置选项列表或完全自定义内容区域，适用于各类筛选、排序、分类导航等交互场景。

## 核心功能描述

- **多菜单并列**：在 `wd-drop-menu` 中可放置多个 `wd-drop-menu-item`，菜单标题栏自动等分宽度
- **互斥展开**：点击某一菜单项时，自动关闭其他已打开的菜单，确保同一时间只有一个下拉菜单处于展开状态
- **弹出方向**：通过 `direction` 属性控制菜单弹出方向，`down`（向下弹出，默认）或 `up`（向上弹出）
- **选项列表**：通过 `options` 属性传入选项数组，支持自定义 `value`、`label`、`tip` 等字段的 key 映射
- **自定义内容**：通过 `wd-drop-menu-item` 的默认插槽可完全自定义下拉面板内容，如滑块、表单、按钮组合等
- **异步拦截**：通过 `beforeToggle` 属性在菜单打开/关闭前执行回调，可异步控制是否允许操作
- **遮罩层管理**：自动显示/隐藏遮罩层，支持配置是否展示遮罩层以及是否点击遮罩层关闭菜单
- **动画控制**：通过 `duration` 属性控制菜单展开收起动画时长（单位 ms，默认 200ms）
- **菜单禁用**：通过 `disabled` 属性禁用特定菜单项的点击交互
- **自定义图标**：支持自定义菜单标题区域的图标和图标大小
- **脱离页面渲染**：通过 `rootPortal` 属性将下拉面板从当前组件树中脱离出来，解决 fixed 定位失效问题
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **商品筛选**：电商列表页的商品分类、品牌、价格区间等多维度筛选
- **排序功能**：综合排序、销量排序、上架时间排序等列表排序入口
- **地图筛选**：地图应用中按类型、距离等条件筛选 POI 点
- **自定义筛选面板**：需要嵌入滑块、多选、日期范围等复杂交互条件的筛选场景
- **底部工具栏**：使用向上弹出模式，在页面底部工具栏中展示操作菜单
- **复合导航**：与自定义按钮（如 SortButton）组合使用，形成混合风格的导航筛选栏

## API

### wd-drop-menu Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| direction | `'up' \| 'down'` | `'down'` | 否 | 菜单展开方向，`down` 表示向下弹出，`up` 表示向上弹出 |
| zIndex | number | 12 | 否 | 弹框层级 |
| modal | boolean | true | 否 | 是否展示遮罩层（蒙层） |
| closeOnClickModal | boolean | true | 否 | 是否点击遮罩层时关闭菜单 |
| duration | number | 200 | 否 | 菜单展开收起动画时间，单位毫秒（ms） |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类 |

### wd-drop-menu-item Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | `string \| number` | - | 否 | 当前选中项对应的 value 值，支持 `v-model` 双向绑定 |
| options | `Record<string, any>[]` | `[]` | 否 | 选项列表数据，默认数据结构 `[{label: '标题', value: '0', tip: '提示文字'}]` |
| disabled | boolean | false | 否 | 是否禁用该菜单项 |
| title | string | - | 否 | 菜单标题文字。若未设置，则自动根据当前选中项的 label 显示 |
| icon | string | `'arrow-down'` | 否 | 菜单项右侧图标名称（可选图标见 `wd-icon` 组件） |
| iconSize | `string \| number` | - | 否 | 菜单项右侧图标大小 |
| iconName | string | `'check'` | 否 | 选项列表中选中标项的图标名称 |
| valueKey | string | `'value'` | 否 | 选项对象中表示值的字段 key |
| labelKey | string | `'label'` | 否 | 选项对象中表示展示文本的字段 key |
| tipKey | string | `'tip'` | 否 | 选项对象中表示选项说明的字段 key |
| beforeToggle | `(option: { status: boolean; resolve: (isPass: boolean) => void }) => void` | - | 否 | 展开/关闭前的回调，通过 `resolve(true)` 允许操作，`resolve(false)` 阻止操作 |
| popupHeight | string | `''` | 否 | 自定义下拉弹出层高度，默认最大高度为 80% |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 定位失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） |
| customTitle | string | `''` | 否 | 菜单项左侧文字的自定义样式类名 |
| customIcon | string | `''` | 否 | 菜单项右侧图标的自定义样式类名 |
| customPopupClass | string | `''` | 否 | 自定义下拉弹出层的样式类名 |
| customPopupStyle | string | `''` | 否 | 自定义下拉弹出层的内联样式 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类 |

### wd-drop-menu-item Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | `{ value: string \| number; selectedItem: Record<string, any> }` | 选项被选中时触发，返回选中的 value 值和完整选中项数据 |
| open | - | 下拉菜单开始打开（弹出层进入动画前） |
| opened | - | 下拉菜单打开完成（弹出层进入动画后） |
| close | - | 下拉菜单开始关闭（弹出层离开动画前） |
| closed | - | 下拉菜单关闭完成（弹出层离开动画后） |
| update:modelValue | `string \| number` | 选项值变化时触发，用于 `v-model` 双向绑定 |

### wd-drop-menu Methods

组件不对外暴露方法。

### wd-drop-menu-item Methods

通过 ref 可以获取 `wd-drop-menu-item` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| getShowPop | 无 | `boolean` | 获取当前下拉面板的显示状态 |
| open | 无 | void | 打开下拉面板 |
| close | 无 | void | 关闭下拉面板 |
| toggle | 无 | void | 切换下拉面板的打开/关闭状态 |

### wd-drop-menu Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 下拉菜单内容区域，用于放置 `wd-drop-menu-item` 组件 |

### wd-drop-menu-item Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义下拉面板内容。当不传入 `options` 或需要通过插槽完全自定义面板内容时使用 |

## 类型定义

### DropMenuItemBeforeToggleOption

```ts
type DropMenuItemBeforeToggleOption = {
  // 操作状态：true 打开下拉菜单，false 关闭下拉菜单
  status: boolean
  // 回调函数，用于控制是否允许打开或关闭下拉菜单
  // 调用 resolve(true) 允许操作，resolve(false) 阻止操作
  resolve: (isPass: boolean) => void
}
```

`beforeToggle` 回调的参数类型。通过 `status` 判断当前是打开还是关闭操作，通过调用 `resolve` 控制是否放行。

### DropMenuItemBeforeToggle

```ts
type DropMenuItemBeforeToggle = (option: DropMenuItemBeforeToggleOption) => void
```

展开/关闭前拦截函数的类型定义。

### DropMenuItemInstance

```ts
type DropMenuItemInstance = ComponentPublicInstance<DropMenuItemProps, DropMenuItemExpose>
```

通过 `ref<DropMenuItemInstance>()` 获取下拉菜单项实例的类型定义。

## 使用示例

### 示例 1：基本用法

展示最基础的下拉菜单使用方式，通过 `v-model` 绑定选中值，`options` 传入选项列表。

```vue
<template>
  <wd-drop-menu>
    <wd-drop-menu-item v-model="value1" :options="options1" @change="handleChange1" />
    <wd-drop-menu-item v-model="value2" :options="options2" @change="handleChange2" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)
const value2 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部商品', value: 0 },
  { label: '新款商品', value: 1 },
  { label: '活动商品', value: 2 }
])

const options2 = ref<Record<string, any>[]>([
  { label: '综合排序', value: 0 },
  { label: '销量排序', value: 1 },
  { label: '上架时间', value: 2 }
])

function handleChange1({ value }: { value: number | string }) {
  console.log('筛选值:', value)
  // 此处可触发列表查询
}

function handleChange2({ value }: { value: number | string }) {
  console.log('排序值:', value)
  // 此处可触发列表查询
}
</script>

<style lang="scss" scoped>
</style>
```

多个 `wd-drop-menu-item` 在 `wd-drop-menu` 中会自动均分宽度。点击菜单项标题打开下拉面板，选择选项后自动关闭面板并触发 `change` 事件。`options` 数组中每一项默认识别 `label` 作为展示文本、`value` 作为选中值。

### 示例 2：自定义菜单内容

在 `wd-drop-menu-item` 中不使用 `options`，而是通过插槽自定义下拉面板内容，可嵌入滑块、表单、按钮等任意组件。

```vue
<template>
  <wd-drop-menu>
    <wd-drop-menu-item v-model="value1" :options="options1" @change="handleChange1" />
    <wd-drop-menu-item ref="customItemRef" title="筛选" @opened="handleOpened">
      <view>
        <wd-slider v-model="sliderValue" />
        <wd-cell title="价格区间" :value="`¥${sliderValue}`" />
        <view style="padding: 0 10px 20px; box-sizing: border-box">
          <wd-button block size="large" @click="handleConfirm">确定</wd-button>
        </view>
      </view>
    </wd-drop-menu-item>
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { DropMenuItemInstance } from '@/uni_modules/wot-ui-plus/components/wd-drop-menu-item/types'

const value1 = ref<number>(0)
const sliderValue = ref<number>(50)
const customItemRef = ref<DropMenuItemInstance>()

const options1 = ref<Record<string, any>[]>([
  { label: '全部商品', value: 0 },
  { label: '新款商品', value: 1 }
])

/**
 * 下拉面板打开完成后初始化 slider
 */
function handleOpened() {
  // 可在此处执行需要面板可见后才能进行的初始化操作
}

function handleChange1({ value }: { value: number | string }) {
  console.log('筛选值:', value)
}

/**
 * 确认筛选，关闭面板
 */
function handleConfirm() {
  customItemRef.value?.close()
  // 此处可根据 sliderValue 触发列表查询
}
</script>

<style lang="scss" scoped>
</style>
```

当 `wd-drop-menu-item` 不使用 `options` 属性时，其默认插槽内容将直接渲染在下拉面板中。通过 ref 获取组件实例后可调用 `close()` 方法关闭面板。`@opened` 事件在面板打开动画完成后触发，可在此处执行需要面板可见后才能初始化的组件（如 slider 需要重新计算尺寸）。

### 示例 3：向上弹出

通过 `direction` 属性设置菜单向上弹出，适用于页面底部工具栏中的下拉菜单。

```vue
<template>
  <wd-drop-menu direction="up">
    <wd-drop-menu-item v-model="value1" :options="options1" @change="handleChange1" />
    <wd-drop-menu-item v-model="value2" :options="options2" @change="handleChange2" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)
const value2 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部区域', value: 0 },
  { label: '附近 1km', value: 1 },
  { label: '附近 3km', value: 2 },
  { label: '附近 5km', value: 3 }
])

const options2 = ref<Record<string, any>[]>([
  { label: '默认排序', value: 0 },
  { label: '距离最近', value: 1 },
  { label: '评分最高', value: 2 }
])

function handleChange1({ value }: { value: number | string }) {
  console.log('区域筛选:', value)
}

function handleChange2({ value }: { value: number | string }) {
  console.log('排序方式:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

设置 `direction="up"` 后，菜单面板会从菜单栏下方向上弹出，遮罩层也相适配覆盖菜单栏上方区域。常用于地图筛选、底部操作栏等场景。

### 示例 4：选项说明文字

在选项列表中使用 `tip` 字段为选项添加补充说明文字。

```vue
<template>
  <wd-drop-menu>
    <wd-drop-menu-item v-model="value1" :options="options1" @change="handleChange1" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部商品', value: 0 },
  { label: '新款商品', value: 1, tip: 'NEW' },
  { label: '特价商品', value: 2, tip: 'HOT' }
])

function handleChange1({ value }: { value: number | string }) {
  console.log('选中值:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

选项数据中添加 `tip` 字段后，在选项列表中会展示在 label 文字右侧，以较小的灰色文字显示，适用于"NEW"、"HOT"、"限时"等标签提示。`tip` 字段名可通过 `tipKey` 属性自定义。

### 示例 5：异步打开 / 关闭

通过 `beforeToggle` 属性在菜单打开或关闭前进行拦截确认，支持异步操作。

```vue
<template>
  <wd-drop-menu>
    <wd-drop-menu-item
      v-model="value1"
      :options="options1"
      :before-toggle="handleBeforeToggle"
      @change="handleChange1"
    />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useMessage } from '@/uni_modules/wot-ui-plus'
import type { DropMenuItemBeforeToggle } from '@/uni_modules/wot-ui-plus/components/wd-drop-menu-item/types'

const value1 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部商品', value: 0 },
  { label: '新款商品', value: 1 },
  { label: '活动商品', value: 2 }
])

const messageBox = useMessage()

const handleBeforeToggle: DropMenuItemBeforeToggle = ({ status, resolve }) => {
  messageBox
    .confirm({
      title: status ? '确认打开' : '确认关闭',
      msg: status ? '确定要打开下拉菜单吗？' : '确定要关闭下拉菜单吗？'
    })
    .then(() => {
      resolve(true)
    })
    .catch(() => {
      resolve(false)
    })
}

function handleChange1({ value }: { value: number | string }) {
  console.log('选中值:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

`beforeToggle` 回调接收 `{ status, resolve }` 参数，`status` 为 `true` 表示打开操作，`false` 表示关闭操作。调用 `resolve(true)` 允许操作继续，`resolve(false)` 阻止操作。可在回调中调用异步方法（如弹窗确认、接口请求等），根据异步结果决定放行或拦截。

### 示例 6：自定义菜单图标

通过 `icon` 和 `iconSize` 属性自定义菜单标题区域的图标。

```vue
<template>
  <wd-drop-menu>
    <!-- 自定义图标和大小 -->
    <wd-drop-menu-item title="地图" icon="location" icon-size="14px" />
    <!-- 使用默认箭头图标 -->
    <wd-drop-menu-item v-model="value1" :options="options1" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部', value: 0 },
  { label: '选项A', value: 1 },
  { label: '选项B', value: 2 }
])
</script>

<style lang="scss" scoped>
</style>
```

`icon` 属性设置菜单标题右侧的图标名称（参考 `wd-icon` 组件支持的图标列表），`iconSize` 控制图标大小。当不使用 `options` 且仅展示图标时，可用于实现地图切换、视图切换等功能入口。

### 示例 7：禁用状态

通过 `disabled` 属性禁用菜单项，禁用后点击不会打开下拉面板。

```vue
<template>
  <wd-drop-menu direction="up">
    <wd-drop-menu-item v-model="value1" disabled :options="options1" @change="handleChange1" />
    <wd-drop-menu-item v-model="value2" :options="options2" @change="handleChange2" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)
const value2 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '选项A', value: 0 },
  { label: '选项B', value: 1 }
])

const options2 = ref<Record<string, any>[]>([
  { label: '排序1', value: 0 },
  { label: '排序2', value: 1 }
])

function handleChange1({ value }: { value: number | string }) {
  console.log('value1:', value)
}

function handleChange2({ value }: { value: number | string }) {
  console.log('value2:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

设置 `disabled` 为 `true` 后，该菜单项呈现禁用样式（灰色文字），点击时不会打开下拉面板，也不会触发互斥关闭其他菜单。适用于条件不满足时需要禁用筛选项的场景。

### 示例 8：自定义字段映射

通过 `valueKey`、`labelKey`、`tipKey` 自定义选项数据的字段名称映射。

```vue
<template>
  <wd-drop-menu>
    <wd-drop-menu-item
      v-model="selectedCategory"
      :options="categoryList"
      value-key="id"
      label-key="name"
      tip-key="desc"
      @change="handleCategoryChange"
    />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedCategory = ref<number>(1)

const categoryList = ref([
  { id: 1, name: '电子产品', desc: '手机、电脑等' },
  { id: 2, name: '服装鞋帽', desc: '服饰、箱包等' },
  { id: 3, name: '食品饮料', desc: '零食、饮品等' }
])

function handleCategoryChange({ value, selectedItem }: { value: number | string; selectedItem: Record<string, any> }) {
  console.log('选中分类:', value, selectedItem)
}
</script>

<style lang="scss" scoped>
</style>
```

当接口返回的数据结构与组件默认字段名不一致时，可通过 `valueKey`（默认 `value`）、`labelKey`（默认 `label`）、`tipKey`（默认 `tip`）进行映射配置，避免额外转换数据。

### 示例 9：自定义标题样式

通过 `customTitle` 和 `customIcon` 自定义菜单标题文字和图标的样式类名。

```vue
<template>
  <wd-drop-menu direction="up">
    <wd-drop-menu-item
      v-model="value1"
      :options="options1"
      custom-title="red-title"
      custom-icon="red-icon"
      @change="handleChange1"
    />
    <wd-drop-menu-item v-model="value2" :options="options2" @change="handleChange2" />
  </wd-drop-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(0)
const value2 = ref<number>(0)

const options1 = ref<Record<string, any>[]>([
  { label: '全部', value: 0 },
  { label: '选项A', value: 1 }
])

const options2 = ref<Record<string, any>[]>([
  { label: '综合', value: 0 },
  { label: '最新', value: 1 }
])

function handleChange1({ value }: { value: number | string }) {
  console.log('value1:', value)
}

function handleChange2({ value }: { value: number | string }) {
  console.log('value2:', value)
}
</script>

<style lang="scss" scoped>
:deep(.red-title) {
  color: red;
}
:deep(.red-icon) {
  color: red;
}
</style>
```

`customTitle` 和 `customIcon` 分别用于为菜单标题文字和图标添加自定义 CSS 类名，配合 `:deep()` 选择器可在外部修改组件内部样式。

## 注意事项

1. **互斥关闭机制**：组件内部使用队列机制管理多个下拉菜单。点击某一菜单项时，会自动关闭其他已打开的菜单，确保同一时间最多只有一个下拉面板处于展开状态。点击遮罩层也会关闭所有已打开的菜单。

2. **遮罩层延迟关闭**：遮罩层使用延迟关闭策略（16ms），避免快速切换菜单时遮罩层闪烁。小程序中即使先 fold 再 closeOther 也会有闪烁问题，已通过延迟关闭处理。

3. **title 优先级**：若设置了 `title` 属性，则菜单标题始终显示为 `title` 的值。若未设置 `title`，则自动根据当前选中项在 `options` 中对应的 `label` 值作为标题显示。如果当前 `modelValue` 在 `options` 中找不到匹配项，会在控制台输出警告。

4. **beforeToggle 异步控制**：`beforeToggle` 回调中必须调用 `resolve` 函数才能继续操作，不调用则操作会一直处于等待状态。`resolve(true)` 放行，`resolve(false)` 阻止。

5. **方向值校验**：`direction` 属性仅支持 `'up'` 和 `'down'` 两个值。若传入其他值，组件会在控制台输出错误警告。

6. **modelValue 类型**：`modelValue` 应为 `number` 或 `string` 类型。若传入其他类型，组件会在控制台输出警告信息。

7. **rootPortal 使用场景**：在复杂嵌套场景中（如嵌套在 fixed 定位的容器内、嵌套在 transform 元素内等），下拉面板的 `position: fixed` 可能失效。设置 `rootPortal` 为 `true` 可将面板渲染到页面顶层容器（H5 使用 teleport，小程序使用 root-portal），脱离当前组件树层级限制。

8. **popupHeight 自定义高度**：默认下拉面板最大高度为 `80%`（相对于视口）。通过 `popupHeight` 可设置固定高度值，如 `"300px"`。设置后 `scroll-view` 容器高度也会同步，支持滚动浏览超出内容。

9. **自定义内容与 options 互斥**：当传入 `options` 时，下拉面板渲染为选项列表；当不传 `options` 或 `options` 为空数组时，下拉面板渲染默认插槽内容。两者不可同时使用。

10. **选中图标与状态**：选项列表中被选中的项会显示右侧勾选图标（默认 `check` 图标，可通过 `iconName` 自定义），同时文字颜色变为激活态颜色。激活态还会在菜单标题下方显示一条短横线标识。

11. **样式隔离**：组件启用了 `virtualHost: true` 和 `styleIsolation: 'shared'`，支持全局样式和外部样式穿透。菜单项激活态的下划线、箭头旋转等样式可通过 `:deep()` 选择器在外部覆盖。

12. **暗色模式自动适配**：组件已内置暗色主题样式，当根节点包含 `wot-theme-dark` 类名时，菜单文字颜色、背景色、禁用态颜色等都会自动切换为暗色主题值。
