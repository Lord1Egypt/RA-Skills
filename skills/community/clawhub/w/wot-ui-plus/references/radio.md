# Radio 单选框


## 组件概况

Radio 单选框组件是一组用于在多个互斥选项中进行单项选择的表单控件。该组件由 `wd-radio`（单个单选框）和 `wd-radio-group`（单选框组）两部分组成，通常配合使用以实现完整的单选交互功能。

单选框支持多种视觉形态（对勾、圆点、按钮），并提供单元格模式、内联布局、尺寸调节、颜色定制等丰富的配置选项，能够灵活适配各类业务场景中的单选需求。

## 核心功能描述

- **多种形状**：支持 `check`（对勾）、`dot`（圆点）、`button`（按钮）三种单选框样式
- **双向绑定**：通过 `v-model` 在 `wd-radio-group` 上实现选中值的双向数据绑定
- **表单模式**：开启 `cell` 属性后以单元格形式展示，适合表单页面中的选项组
- **内联布局**：通过 `inline` 属性实现单选框横向排列
- **图标位置**：支持通过 `iconPlacement` 属性调整图标在左侧、右侧或自动布局
- **层级优先级**：`wd-radio` 自身的属性优先级高于 `wd-radio-group` 传递的属性，支持局部覆盖
- **尺寸调节**：支持通过 `size` 属性设置 `large` 等大尺寸
- **颜色定制**：通过 `checkedColor` 属性自定义选中状态的颜色
- **禁用控制**：支持在组级别或单个单选框级别设置禁用状态
- **事件通知**：选中值变化时触发 `change` 事件，返回当前选中值

## 适用业务场景

- **支付方式选择**：用户在微信、支付宝、银行卡等支付方式中单选一种
- **性别/身份选择**：表单中性别、身份类型等互斥选项的选择
- **评分/评价**：单项满意度评价、等级选择等场景
- **设置选项**：系统设置中的单选开关项，如通知方式、语言选择等
- **筛选条件**：列表筛选中的单选条件，如排序方式、分类选择等

## API

### wd-radio-group Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 选中项的值，会自动选中对应的单选框 | string / number / boolean | - | - | - |
| shape | 单选框形状 | string | check / dot / button | check | - |
| checkedColor | 选中状态的颜色 | string | - | #4D80F0 | - |
| disabled | 是否禁用组内所有单选框 | boolean | - | false | - |
| cell | 是否启用表单单元格模式 | boolean | - | false | - |
| size | 单选框尺寸 | string | large / '' | '' | - |
| inline | 是否同行展示 | boolean | - | false | - |
| iconPlacement | 图标位置 | string | left / right / auto | auto | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-radio Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| value | 当前单选框的值，必填 | string / number / boolean | - | - | - |
| shape | 单选框形状（覆盖组级别配置） | string | check / dot / button | - | - |
| checkedColor | 选中状态的颜色（覆盖组级别配置） | string | - | - | - |
| disabled | 是否禁用当前单选框（覆盖组级别配置） | boolean / null | - | null | - |
| cell | 是否启用单元格模式（覆盖组级别配置） | boolean / null | - | null | - |
| size | 单选框尺寸（覆盖组级别配置） | string | large / '' | - | - |
| inline | 是否同行展示（覆盖组级别配置） | boolean / null | - | null | - |
| maxWidth | 标签区域最大宽度 | string | - | - | - |
| iconPlacement | 图标位置（覆盖组级别配置） | string | left / right / auto | - | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Events

#### wd-radio-group Events

| 事件名 | 说明 | 参数 |
|--------|------|------|
| change | 选中值发生变化时触发 | `{ value: string \| number \| boolean }` |

#### wd-radio Events

wd-radio 组件未单独对外抛出事件，点击操作由 wd-radio-group 统一处理。

### Methods

组件未暴露外部可调用的方法。

### Slots

#### wd-radio-group Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽 | wd-radio 组件列表 |

#### wd-radio Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于显示单选框的标签文本 | 文本或任意内容 |

## 使用示例

### 基础用法

最基本的单选框组使用方式，通过 `v-model` 绑定选中值，在 `wd-radio-group` 内放置多个 `wd-radio` 组件。

```vue
<template>
  <wd-radio-group v-model="value" @change="handleChange">
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<number>(1)

function handleChange(e: { value: number }) {
  console.log('选中值:', e.value)
}
</script>
```

### 修改形状

通过 `shape` 属性可以切换单选框的视觉形态，支持 `check`（默认对勾）、`dot`（圆点）、`button`（按钮）三种样式。

```vue
<template>
  <!-- 按钮样式 -->
  <wd-radio-group v-model="value1" shape="button">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>

  <!-- 圆点样式 -->
  <wd-radio-group v-model="value2" shape="dot">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
</script>
```

### 表单单元格模式

开启 `cell` 属性后，单选框将以表单单元格样式展示，选项之间带有分隔线，适合表单页面的选项组场景。结合 `shape="button"` 可实现按钮样式的表单单选组。

```vue
<template>
  <!-- 单元格样式 -->
  <wd-radio-group v-model="value3" cell>
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>

  <!-- 单元格按钮样式 -->
  <wd-radio-group v-model="value4" cell shape="button">
    <wd-radio :value="1">选项一</wd-radio>
    <wd-radio :value="2">选项二</wd-radio>
    <wd-radio :value="3">选项三</wd-radio>
    <wd-radio :value="4">选项四</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value3 = ref<number>(1)
const value4 = ref<number>(1)
</script>
```

### 同行展示

通过 `inline` 属性使单选框横向排列，适用于空间有限或需要紧凑布局的场景。可配合 `iconPlacement` 调整图标位置。

```vue
<template>
  <!-- 默认图标在左侧 -->
  <wd-radio-group v-model="value5" inline>
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>

  <!-- 圆点样式 + 同行展示 -->
  <wd-radio-group v-model="value6" inline shape="dot">
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>

  <!-- 图标在右侧 -->
  <wd-radio-group v-model="value7" inline shape="dot" icon-placement="right">
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value5 = ref<number>(1)
const value6 = ref<number>(1)
const value7 = ref<number>(1)
</script>
```

### 自定义选中颜色

通过 `checkedColor` 属性自定义单选框选中状态的颜色。

```vue
<template>
  <wd-radio-group v-model="value1" checked-color="#fa4350">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>

  <wd-radio-group v-model="value2" shape="dot" checked-color="#fa4350">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
</script>
```

### 禁用状态

支持在 `wd-radio-group` 上设置 `disabled` 禁用整个单选框组，也可以单独对某个 `wd-radio` 设置禁用。

```vue
<template>
  <!-- 圆点样式禁用 -->
  <wd-radio-group v-model="value1" disabled shape="dot">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>

  <!-- 默认样式禁用 -->
  <wd-radio-group v-model="value2" disabled>
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>

  <!-- 按钮样式禁用 -->
  <wd-radio-group v-model="value3" disabled shape="button">
    <wd-radio :value="1">选项1</wd-radio>
    <wd-radio :value="2">选项2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
const value3 = ref<number>(1)
</script>
```

### 大尺寸

通过 `size` 属性设置 `large` 可以放大单选框尺寸，适合需要增强视觉点击区域的场景。

```vue
<template>
  <!-- 大尺寸 - 默认样式 -->
  <wd-radio-group v-model="value1" size="large">
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>

  <!-- 大尺寸 - 圆点样式 -->
  <wd-radio-group v-model="value2" size="large" shape="dot">
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>

  <!-- 大尺寸 - 内联展示 -->
  <wd-radio-group v-model="value3" size="large" inline>
    <wd-radio :value="1">单选框1</wd-radio>
    <wd-radio :value="2">单选框2</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(1)
const value2 = ref<number>(1)
const value3 = ref<number>(1)
</script>
```

### 单个 Radio 属性覆盖组级别配置

`wd-radio` 自身的属性优先级高于 `wd-radio-group` 传递的属性。当需要为某个选项设置不同样式时，可直接在 `wd-radio` 上覆盖配置。

```vue
<template>
  <wd-radio-group v-model="value" shape="button" disabled checked-color="#fa4350">
    <!-- 此选项覆盖禁用状态和选中颜色 -->
    <wd-radio :value="1" checked-color="#000" :disabled="false">选项1</wd-radio>
    <!-- 此选项仅覆盖禁用状态 -->
    <wd-radio :value="2" :disabled="false">选项2</wd-radio>
    <!-- 此选项使用组级别配置 -->
    <wd-radio :value="3">选项3</wd-radio>
  </wd-radio-group>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<number>(1)
</script>
```

## 注意事项

1. **必须配合使用**：`wd-radio` 需要放置在 `wd-radio-group` 内部才能正常工作。单独使用 `wd-radio` 无法完成选中状态的管理和值变更。

2. **value 必填**：每个 `wd-radio` 组件的 `value` 属性为必填项，且值类型必须为 `string`、`number` 或 `boolean`。`wd-radio-group` 的 `modelValue` 类型需与 `wd-radio` 的 `value` 类型保持一致。

3. **属性优先级**：`wd-radio` 自身设置的属性优先级高于 `wd-radio-group` 传递的属性。例如在组级别设置 `disabled` 后，仍可通过在单个 `wd-radio` 上设置 `:disabled="false"` 来取消该选项的禁用状态。

4. **shape 校验**：`shape` 属性仅接受 `check`、`dot`、`button` 三个值，传入其他值会在控制台输出错误提示。

5. **单元格模式建议**：单选框组件基本使用未对高度进行扩展，建议在表单场景中优先使用 `cell` 属性启用单元格模式，以获得更好的视觉效果和用户体验。

6. **使用场景建议**：当选项在 3 项以内且有重要信息备选时，可使用圆形单选框。但需注意圆形单选框与圆形复选框容易混淆，可能造成表单页面结构不统一，一般情况建议使用表单单选组（`cell` 模式）。

7. **图标位置**：`iconPlacement` 默认为 `auto`，在单元格模式下图标默认在右侧，非单元格模式下图标默认在左侧。可显式设置为 `left` 或 `right` 进行统一控制。

8. **样式定制**：推荐使用 `customStyle` 和 `customClass` 属性进行组件样式定制。`wd-radio-group` 的样式属性作用于容器，`wd-radio` 的样式属性作用于单个选项。
