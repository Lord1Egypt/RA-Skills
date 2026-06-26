# Checkbox 复选框


## 组件概况

Checkbox 复选框组件用于在一组选项中进行多选操作，支持独立使用和组合使用两种模式。该组件由 `wd-checkbox`（单个复选框）和 `wd-checkbox-group`（复选框组）两个子组件组成，可以配合使用实现灵活的多选交互。复选框支持圆形、方形、按钮三种形状，提供单元格表单模式和内联排列布局，广泛应用于表单填写、权限配置、批量选择等场景。

## 核心功能描述

- **独立使用**：`wd-checkbox` 可单独使用，通过 `v-model` 绑定布尔值或自定义的 `true-value` / `false-value`
- **组合使用**：`wd-checkbox-group` 包裹多个 `wd-checkbox`，通过 `v-model` 绑定数组统一管理选中项
- **三种形状**：支持 `circle`（圆形）、`square`（方形）、`button`（按钮）三种外观形态
- **半选中状态**：通过 `indeterminate` 属性实现全选/部分选中的中间态展示
- **选中数量控制**：复选框组支持设置 `min`（最小选中数）和 `max`（最大选中数），超出范围自动禁用相关选项
- **表单模式**：通过 `cell` 属性开启单元格样式，适合表单场景中使用
- **内联布局**：通过 `inline` 属性使复选框在同一行排列显示
- **尺寸控制**：支持 `size` 属性调节组件大小，可选值为 `large`
- **自定义颜色**：通过 `checked-color` 属性自定义选中状态的颜色
- **级联禁用**：复选框组设置 `disabled` 后统一禁用所有子项，子项也可通过 `disabled` 属性单独覆盖
- **方法暴露**：`wd-checkbox` 通过 ref 暴露 `toggle()` 方法，支持外部程序化切换选中状态
- **最大宽度限制**：通过 `max-width` 属性控制文案区域的最大宽度，防止文字溢出

## 适用业务场景

- **表单多选**：在注册表单、调查问卷中实现兴趣标签、技能特长等多选题
- **权限配置**：在后台管理系统中配置角色权限、菜单访问权限等多选场景
- **批量操作**：在列表页面中实现批量选中、批量删除、批量修改等功能
- **筛选过滤**：在商品列表、内容列表页面提供多维度筛选条件
- **协议确认**：在注册或支付流程中让用户确认已阅读相关协议条款
- **标签选择**：在内容发布、文章编辑等场景中让用户选择多个分类标签

## API

### wd-checkbox Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string / number / boolean | false | 是 | 复选框绑定的值。独立使用时表示选中状态；在 checkbox-group 中使用时作为该选项的唯一标识符 |
| shape | string | 继承父组件 | 否 | 复选框形状，可选值：`circle` 圆形、`square` 方形、`button` 按钮 |
| checkedColor | string | 继承父组件 | 否 | 选中状态的颜色 |
| disabled | boolean / null | null | 否 | 是否禁用。在 checkbox-group 中设为 null 时会继承父组件的 disabled 状态 |
| trueValue | string / number / boolean | true | 否 | 选中时的值，需与 false-value 配合使用，在 checkbox-group 中无效 |
| falseValue | string / number / boolean | false | 否 | 未选中时的值，需与 true-value 配合使用，在 checkbox-group 中无效 |
| indeterminate | boolean | false | 否 | 是否为半选中（部分选中）状态，此时图标显示为减号 |
| size | string | 继承父组件 | 否 | 组件尺寸，可选值：`large` |
| maxWidth | string | '' | 否 | 文字区域最大宽度，用于控制文案超出时截断显示 |
| customLabelClass | string | '' | 否 | 自定义标签区域的样式类名 |
| customShapeClass | string | '' | 否 | 自定义形状（圆形/方形框）区域的样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-checkbox-group Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | Array\<string / number / boolean\> | [] | 否 | 绑定的选中值数组，数组中不应包含重复值 |
| cell | boolean | false | 否 | 是否开启表单单元格模式 |
| shape | string | 'circle' | 否 | 复选框形状，可选值：`circle` 圆形、`square` 方形、`button` 按钮 |
| checkedColor | string | 继承父组件 | 否 | 选中状态的颜色，会向下传递给所有子项 |
| disabled | boolean | false | 否 | 是否禁用整个复选框组，设为 true 后所有子项将被禁用 |
| min | number | 0 | 否 | 最小选中数量，达到该数量后已选中项将被禁用取消操作 |
| max | number | 0 | 否 | 最大选中数量，0 表示不限制，达到该数量后未选中项将被禁用 |
| inline | boolean | false | 否 | 是否内联排列，设为 true 时所有子项在同一行展示 |
| size | string | '' | 否 | 组件尺寸，可选值：`large`，会向下传递给所有子项 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点样式类 |

### wd-checkbox Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 选中状态切换时触发 | `(data: { value: boolean / string / number / boolean[] })` | 独立使用时 `value` 为新的选中值（trueValue/falseValue）；在组内使用时 `value` 为当前切换后的布尔状态 |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: string / number / boolean)` | 仅在独立使用时触发，值为切换后的新值 |

### wd-checkbox-group Events

| 事件名称 | 触发条件 | 参数类型 | 回调数据说明 |
|---------|---------|---------|-------------|
| change | 子项选中状态变化时触发 | `(data: { value: Array<string / number / boolean> })` | `value` 为更新后的完整选中值数组 |
| update:modelValue | 绑定值更新时触发（v-model 内部使用） | `(value: Array<string / number / boolean>)` | 值为更新后的完整选中数组 |

### wd-checkbox Methods

通过 ref 可以获取 `wd-checkbox` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| toggle | 无 | void | 切换当前复选框的选中/未选中状态 |

### wd-checkbox-group Methods

组件不对外暴露可调用的方法。

### wd-checkbox Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 复选框的文案内容，位于复选框形状右侧 |

### wd-checkbox-group Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 用于放置多个 wd-checkbox 子组件 |

## 使用示例

### 示例 1：基本用法与形状切换

展示 `wd-checkbox` 独立使用的基本方法，以及三种不同形状的切换效果。

```vue
<template>
  <view class="checkbox-section">
    <view class="demo-item">
      <text class="demo-label">默认圆形</text>
      <wd-checkbox v-model="checkCircle">沃特</wd-checkbox>
    </view>

    <view class="demo-item">
      <text class="demo-label">方形复选框</text>
      <wd-checkbox v-model="checkSquare" shape="square">沃特</wd-checkbox>
    </view>

    <view class="demo-item">
      <text class="demo-label">按钮样式</text>
      <wd-checkbox v-model="checkButton" shape="button">沃特</wd-checkbox>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const checkCircle = ref<boolean>(true)
const checkSquare = ref<boolean>(false)
const checkButton = ref<boolean>(true)
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}

.demo-item {
  margin-bottom: 16px;
}

.demo-label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}
</style>
```

该示例展示了三种形状的基本用法。`shape="circle"` 为默认圆形勾选框，`shape="square"` 为方形勾选框，`shape="button"` 为按钮样式——选中时会显示对勾图标和高亮颜色，未选中时呈现常规按钮外观。

### 示例 2：复选框组与数量控制

展示 `wd-checkbox-group` 的基本用法，结合 `min` 和 `max` 属性控制可选数量范围。

```vue
<template>
  <view class="checkbox-section">
    <!-- 基础复选框组 -->
    <view class="demo-item">
      <text class="demo-label">基础复选框组</text>
      <wd-checkbox-group v-model="basicValue">
        <wd-checkbox :modelValue="1">京东</wd-checkbox>
        <wd-checkbox :modelValue="2">沃特</wd-checkbox>
        <wd-checkbox :modelValue="3">商家后台</wd-checkbox>
        <wd-checkbox :modelValue="4">营销中心</wd-checkbox>
      </wd-checkbox-group>
      <text class="demo-tip">当前选中: {{ basicValue }}</text>
    </view>

    <!-- 限制最小/最大选中数量 -->
    <view class="demo-item">
      <text class="demo-label">限制选中数量（最少 1 项，最多 3 项）</text>
      <wd-checkbox-group v-model="rangeValue" :min="1" :max="3" cell>
        <wd-checkbox :modelValue="1">京东</wd-checkbox>
        <wd-checkbox :modelValue="2">沃特</wd-checkbox>
        <wd-checkbox :modelValue="3">商家后台</wd-checkbox>
        <wd-checkbox :modelValue="4">营销中心</wd-checkbox>
      </wd-checkbox-group>
      <text class="demo-tip">当前选中: {{ rangeValue.length }} 项</text>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const basicValue = ref<number[]>([1])
const rangeValue = ref<number[]>([1])
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}

.demo-item {
  margin-bottom: 24px;
}

.demo-label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.demo-tip {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}
</style>
```

在基础复选框组中，`modelValue` 为选中值的数组，每个 `wd-checkbox` 的 `modelValue` 作为该选项的唯一标识。当设置了 `min` 和 `max` 后，达到最小值时已选中项会被禁用（不可取消），达到最大值时未选中项会被禁用（不可再选）。`cell` 属性开启了表单单元格模式，使整体呈现列表样式。

### 示例 3：表单模式与按钮组

展示在表单场景下使用复选框组的完整用法，包括单元格模式下的按钮形状展示。

```vue
<template>
  <view class="checkbox-section">
    <!-- 表单单元格模式 -->
    <view class="demo-item">
      <text class="demo-label">表单模式 - 复选框组</text>
      <wd-checkbox-group v-model="cellValue" cell>
        <wd-checkbox :modelValue="1">沃特</wd-checkbox>
        <wd-checkbox :modelValue="2">商家后台</wd-checkbox>
      </wd-checkbox-group>
    </view>

    <!-- 表单单元格模式 + 按钮形状 -->
    <view class="demo-item">
      <text class="demo-label">表单模式 - 复选框按钮组</text>
      <wd-checkbox-group v-model="buttonValue" cell shape="button">
        <wd-checkbox :modelValue="1" disabled>选项一</wd-checkbox>
        <wd-checkbox :modelValue="2">选项二</wd-checkbox>
        <wd-checkbox :modelValue="3">选项三</wd-checkbox>
        <wd-checkbox :modelValue="4">选项四</wd-checkbox>
      </wd-checkbox-group>
    </view>

    <!-- 禁用状态 -->
    <view class="demo-item">
      <text class="demo-label">整体禁用</text>
      <wd-checkbox-group v-model="disabledValue" disabled>
        <wd-checkbox :modelValue="1">沃特</wd-checkbox>
        <wd-checkbox :modelValue="2" :disabled="false">商家后台（单独启用）</wd-checkbox>
        <wd-checkbox :modelValue="3" shape="square">沃特</wd-checkbox>
        <wd-checkbox :modelValue="4" shape="square">商家后台</wd-checkbox>
      </wd-checkbox-group>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const cellValue = ref<number[]>([1])
const buttonValue = ref<number[]>([1])
const disabledValue = ref<number[]>([1, 3])
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}

.demo-item {
  margin-bottom: 24px;
}

.demo-label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
</style>
```

在 `cell` 模式下，复选框会呈现单元格样式，适合表单布局。结合 `shape="button"` 可实现按钮组的视觉效果。当复选框组设置 `disabled` 为 `true` 时，所有子项统一禁用，但子项可通过设置 `:disabled="false"` 显式覆盖组的禁用状态。

### 示例 4：自定义值与事件处理

展示如何使用 `true-value` 和 `false-value` 自定义选中/未选中时的绑定值，以及监听 `change` 事件。

```vue
<template>
  <view class="checkbox-section">
    <!-- 自定义 true-value 和 false-value -->
    <view class="demo-item">
      <text class="demo-label">自定义选中值</text>
      <wd-checkbox
        v-model="customValue"
        true-value="已同意"
        false-value="未同意"
        @change="handleChange"
      >
        我已阅读并同意用户协议
      </wd-checkbox>
      <text class="demo-tip">当前值: {{ customValue }}</text>
    </view>

    <!-- 半选中状态 -->
    <view class="demo-item">
      <text class="demo-label">半选中状态（全选场景）</text>
      <wd-checkbox
        v-model="indeterminateValue"
        :indeterminate="isIndeterminate"
        @change="handleIndeterminateChange"
      >
        全选（已选 {{ selectedItems.length }}/{{ allItems.length }} 项）
      </wd-checkbox>
      <view class="sub-checkboxes">
        <wd-checkbox
          v-for="item in allItems"
          :key="item.id"
          :modelValue="item.id"
          shape="square"
          @change="handleItemChange(item.id)"
        >
          {{ item.name }}
        </wd-checkbox>
      </view>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'

const customValue = ref<string>('未同意')

function handleChange(e: { value: string | boolean | number }) {
  console.log('选中状态变化:', e.value)
}

// 半选中状态相关
const allItems = ref([
  { id: 1, name: '京东' },
  { id: 2, name: '沃特' },
  { id: 3, name: '商家后台' }
])
const selectedItems = ref<number[]>([])
const indeterminateValue = ref<boolean>(false)

const isIndeterminate = computed(() => {
  return selectedItems.value.length > 0 && selectedItems.value.length < allItems.value.length
})

function handleIndeterminateChange() {
  if (selectedItems.value.length === allItems.value.length) {
    // 全部已选 -> 取消全选
    selectedItems.value = []
  } else {
    // 部分选中或未选中 -> 全选
    selectedItems.value = allItems.value.map((item) => item.id)
  }
}

function handleItemChange(id: number) {
  const index = selectedItems.value.indexOf(id)
  if (index > -1) {
    selectedItems.value.splice(index, 1)
  } else {
    selectedItems.value.push(id)
  }
}
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}

.demo-item {
  margin-bottom: 24px;
}

.demo-label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.demo-tip {
  display: block;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.sub-checkboxes {
  margin-top: 12px;
  padding-left: 24px;
}
</style>
```

`true-value` 和 `false-value` 仅在 `wd-checkbox` 独立使用时生效，用于自定义绑定的具体值。`indeterminate` 属性用于实现全选场景中的半选中状态，此时复选框会显示减号图标而非对勾。

### 示例 5：内联排列与尺寸控制

展示复选框在同一行排列展示的方法，以及不同尺寸的效果。

```vue
<template>
  <view class="checkbox-section">
    <!-- 内联排列 -->
    <view class="demo-item">
      <text class="demo-label">内联排列</text>
      <wd-checkbox-group v-model="inlineValue" inline>
        <wd-checkbox :modelValue="1">沃特</wd-checkbox>
        <wd-checkbox :modelValue="2">商家后台</wd-checkbox>
      </wd-checkbox-group>
    </view>

    <!-- 大尺寸 - 内联 -->
    <view class="demo-item">
      <text class="demo-label">大尺寸（内联）</text>
      <wd-checkbox-group v-model="largeInlineValue" inline size="large">
        <wd-checkbox modelValue="jingmai">沃特</wd-checkbox>
        <wd-checkbox modelValue="shop">商家后台</wd-checkbox>
      </wd-checkbox-group>
    </view>

    <!-- 大尺寸 - 块级 -->
    <view class="demo-item">
      <text class="demo-label">大尺寸（块级）</text>
      <wd-checkbox-group v-model="largeBlockValue" size="large">
        <wd-checkbox modelValue="jingmai">沃特</wd-checkbox>
        <wd-checkbox modelValue="shop">商家后台</wd-checkbox>
      </wd-checkbox-group>
    </view>

    <!-- 自定义选中颜色 -->
    <view class="demo-item">
      <text class="demo-label">自定义选中颜色</text>
      <wd-checkbox v-model="colorValue" checked-color="rgb(52, 209, 157)">沃特</wd-checkbox>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const inlineValue = ref<number[]>([1])
const largeInlineValue = ref<string[]>([])
const largeBlockValue = ref<string[]>([])
const colorValue = ref<boolean>(true)
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}

.demo-item {
  margin-bottom: 20px;
}

.demo-label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
</style>
```

通过 `inline` 属性可以让复选框在同一行水平排列，适合选项较少、空间紧凑的场景。`size="large"` 可增大复选框和文字的尺寸，提升触控区域和可读性。`checked-color` 支持任意 CSS 颜色值格式，包括十六进制、rgb、rgba 等。

### 示例 6：结合 Cell 组件与外部方法调用

展示如何将复选框与单元格组件配合使用，以及通过 ref 调用 `toggle()` 方法实现外部控制。

```vue
<template>
  <view class="checkbox-section">
    <wd-cell-group border>
      <wd-checkbox-group v-model="cellGroupValue" size="large">
        <wd-cell title="点赞" center clickable @click="handleCellClick('checkBox1')">
          <view @click.stop="preventBubble">
            <wd-checkbox modelValue="1" ref="checkBox1" customStyle="margin:0;"></wd-checkbox>
          </view>
        </wd-cell>

        <wd-cell title="投币" center clickable @click="handleCellClick('checkBox2')">
          <view @click.stop="preventBubble">
            <wd-checkbox modelValue="2" ref="checkBox2" customStyle="margin:0;"></wd-checkbox>
          </view>
        </wd-cell>

        <wd-cell title="一键三连" center clickable @click="handleCellClick('checkBox3')">
          <view @click.stop="preventBubble">
            <wd-checkbox modelValue="3" ref="checkBox3" customStyle="margin:0;"></wd-checkbox>
          </view>
        </wd-cell>
      </wd-checkbox-group>
    </wd-cell-group>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { CheckboxInstance } from 'wot-design-uni/components/wd-checkbox/types'

const cellGroupValue = ref<string[]>([])

const checkBox1 = ref<CheckboxInstance>()
const checkBox2 = ref<CheckboxInstance>()
const checkBox3 = ref<CheckboxInstance>()

const checkboxMap: Record<string, ReturnType<typeof ref<CheckboxInstance>>> = {
  checkBox1: checkBox1,
  checkBox2: checkBox2,
  checkBox3: checkBox3
}

function handleCellClick(name: string) {
  const checkboxRef = checkboxMap[name]
  if (checkboxRef.value) {
    checkboxRef.value.toggle()
  }
}

function preventBubble() {
  // 阻止复选框点击事件冒泡到 Cell，避免触发两次
}
</script>

<style lang="scss" scoped>
.checkbox-section {
  padding: 16px;
}
</style>
```

该示例演示了复选框与单元格组件的配合使用。通过 `@click.stop` 阻止复选框点击事件冒泡，避免与 Cell 的点击事件冲突。通过 ref 获取 `wd-checkbox` 实例后，可以调用其暴露的 `toggle()` 方法来程序化地切换选中状态。`customStyle="margin:0;"` 用于消除复选框的默认边距，使其与 Cell 布局更加协调。

## 注意事项

1. **独立使用与组合使用的差异**：`wd-checkbox` 单独使用时 `v-model` 绑定布尔值（或自定义的 `true-value` / `false-value`）；在 `wd-checkbox-group` 中使用时 `modelValue` 作为选项唯一标识，由父组件的 `v-model` 数组统一管理选中状态。

2. **modelValue 必填校验**：`wd-checkbox` 的 `modelValue` 不能为 `null`，组件在挂载前会进行校验并输出错误日志。

3. **checkbox-group 值唯一性**：复选框组的 `modelValue` 数组中不能包含重复值，否则组件会输出错误警告。同一组内各 `wd-checkbox` 的 `modelValue` 也不应相同，否则会产生值冲突。

4. **disabled 优先级**：在复选框组中，禁用状态的计算逻辑为：达到最大选中数且未选中时禁用、达到最小选中数且已选中时禁用、自身设置 `disabled=true` 时禁用、组设置 `disabled=true` 且自身未显式设置 `disabled` 时禁用。子项设置 `disabled=false` 可以覆盖组的禁用状态。

5. **shape 属性校验**：`shape` 的有效值为 `circle`、`square`、`button`，传入其他值会在控制台输出错误提示。`wd-checkbox-group` 设置的 `shape` 会作为子项的默认值，子项可自行覆盖。

6. **button 形状的限制**：当 `shape="button"` 时，组件会隐藏复选框形状图标，仅保留标签文案和选中时的对勾图标。

7. **indeterminate 状态**：设置 `indeterminate` 为 `true` 后，复选框的勾选图标会切换为减号（minus）图标，表示部分选中状态。该属性通常在全选/反选场景中配合子项选中数量计算使用。

8. **min/max 取值范围**：`min` 和 `max` 属性应当为非负整数。`max` 为 `0` 时表示不限制最大选中数量。

9. **customLabelClass 与 customShapeClass**：这两个属性分别用于自定义标签区域和形状区域的样式类名，可实现更精细化的样式定制。在按钮形状下，形状区域会被隐藏，`customShapeClass` 不生效。

10. **样式隔离**：组件启用了 `styleIsolation: 'shared'` 和 `addGlobalClass: true`，支持全局样式和外部样式穿透，可在外部通过自定义类名进行样式覆盖。
