# Rate 评分


## 组件概况

`wd-rate` 是一个评分组件，用于展示和收集用户对某一事物的评分反馈。组件支持点击和滑动选择评分、半星选择、只读/禁用状态、自定义图标和颜色等功能。通过 `v-model` 实现评分值的双向数据绑定。

## 核心功能描述

- **点击/滑动评分**：支持点击单个图标进行评分，也支持在组件上滑动来快速选择评分值。滑动评分通过 `touchmove` 事件监听触摸位置，自动计算覆盖的评分项索引
- **半选支持**：通过 `allow-half` 属性开启半选功能，点击图标的左半部分可选择半星评分值
- **自定义图标**：通过 `icon` 和 `active-icon` 属性可自定义未选中和已选中状态的图标名称
- **颜色自定义**：`active-color` 支持传入单个颜色值或颜色数组，颜色数组可实现分段颜色效果（如评分值低于 60% 使用第一种颜色，高于 60% 使用第二种颜色）
- **只读与禁用**：支持 `readonly`（只读）和 `disabled`（禁用）两种状态
- **可清空评分**：通过 `clearable` 属性，当评分值为最小值（`allow-half` 时为 0.5，否则为 1）时再次点击可清空为 0
- **v-model 双向绑定**：通过 `modelValue` 属性实现评分值的双向绑定

## 适用业务场景

- 商品评价/服务评价评分
- 内容质量评分（文章、视频、音乐等）
- 应用评分/满意度调查
- 星级等级展示（如酒店星级、会员等级）

## 使用示例

### 示例一：基本用法

最基础的评分组件，通过 `v-model` 绑定当前评分值，支持点击清空。

```vue
<template>
  <wd-rate v-model="value" clearable @change="handleChange" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<number>(5)

function handleChange({ value }: { value: number }) {
  console.log('当前评分:', value)
}
</script>
```

### 示例二：只读与禁用状态

通过 `readonly` 和 `disabled` 属性控制组件的交互状态。只读状态下用户无法修改评分，禁用状态下组件呈现灰色不可用状态。

```vue
<template>
  <!-- 只读状态，用户无法修改评分 -->
  <wd-rate v-model="readonlyValue" readonly />

  <!-- 禁用状态，组件呈现不可用状态 -->
  <wd-rate v-model="disabledValue" disabled />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const readonlyValue = ref<number>(3)
const disabledValue = ref<number>(2)
</script>
```

### 示例三：自定义颜色

通过 `active-color` 属性修改选中状态的颜色，支持传入颜色数组实现分段颜色效果。

```vue
<template>
  <!-- 单一选中颜色 -->
  <wd-rate
    v-model="value1"
    active-color="linear-gradient(180deg, rgba(255,238,0,1) 0%,rgba(250,176,21,1) 100%)"
    @change="handleChange"
  />

  <!-- 分段颜色：评分值 <= 60% 使用第一种颜色，> 60% 使用第二种颜色 -->
  <wd-rate
    v-model="value2"
    :active-color="[
      'linear-gradient(180deg, rgba(255,238,0,1) 0%,rgba(250,176,21,1) 100%)',
      'linear-gradient(315deg, rgba(245,34,34,1) 0%,rgba(255,117,102,1) 100%)'
    ]"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(3)
const value2 = ref<number>(4)

function handleChange({ value }: { value: number }) {
  console.log('当前评分:', value)
}
</script>
```

### 示例四：自定义图标和尺寸

通过 `icon`、`active-icon`、`size`、`space` 等属性自定义图标和布局。

```vue
<template>
  <!-- 自定义图标 -->
  <wd-rate v-model="value1" icon="dong" active-icon="dong" active-color="#4D80F0" />

  <!-- 自定义图标大小和间距 -->
  <wd-rate v-model="value2" space="10px" size="30px" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<number>(3)
const value2 = ref<number>(5)
</script>
```

### 示例五：半选和可清空

通过 `allow-half` 属性开启半选功能，通过 `clearable` 属性支持再次点击最小值时清空评分。

```vue
<template>
  <!-- 允许半选 -->
  <wd-rate v-model="halfValue" allow-half />

  <!-- 允许清空评分（不含半选） -->
  <wd-rate v-model="clearValue" clearable />

  <!-- 允许清空评分（含半选） -->
  <wd-rate v-model="clearHalfValue" clearable allow-half />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const halfValue = ref<number>(2.5)
const clearValue = ref<number>(3)
const clearHalfValue = ref<number>(3.5)
</script>
```

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| v-model / modelValue | 当前分数，使用 v-model 进行双向绑定 | string \| number \| null | - | null | - |
| num | 评分最大值 | number | - | 5 | - |
| size | 图标大小 | string | - | '16px' | - |
| space | 图标间距 | string | - | '4px' | - |
| color | 未选中的图标颜色 | string | - | '#E8E8E8' | - |
| active-color | 选中的图标颜色，支持传颜色数组用于分段颜色 | `string \| Array<string>` | - | 'linear-gradient(180deg, rgba(255,238,0,1) 0%,rgba(250,176,21,1) 100%)' | - |
| icon | 未选中的图标类名 | string | - | 'star-filled' | - |
| active-icon | 选中的图标类名 | string | - | 'star-filled' | - |
| disabled | 是否禁用 | boolean | - | false | - |
| disabled-color | 禁用的图标颜色 | string | - | 'linear-gradient(315deg, rgba(177,177,177,1) 0%,rgba(199,199,199,1) 100%)' | - |
| readonly | 是否只读 | boolean | - | false | - |
| allow-half | 是否允许半选 | boolean | - | false | - |
| clearable | 当 clearable 属性设置为 true，再次点击相同的值时（最小值），可以将值重置为 0 | boolean | - | false | - |
| custom-style | 根节点自定义样式 | string | - | - | - |
| custom-class | 根节点自定义类名 | string | - | - | - |

### Events

| 事件名 | 说明 | 参数 |
|--------|------|------|
| change | 评分值改变时触发 | `{ value: number }` - 当前评分值 |

### Slots

该组件不提供插槽。

## 注意事项

1. **modelValue 类型校验**：组件要求 `modelValue` 必须为 `number` 类型。如果传入非 number 类型，控制台会输出错误信息 `[wot ui] error(wd-rate): the value of wd-rate should be a number`。

2. **active-color 数组校验**：当 `active-color` 传入数组时，数组不能为空。如果传入空数组，控制台会输出错误信息 `activeColor cannot be an empty array`。

3. **分段颜色计算逻辑**：当 `active-color` 为数组且长度大于 0 时，组件会根据当前评分值与最大评分值的比例来决定使用哪种颜色。如果评分值小于等于最大值的 60%，使用数组第一个元素的颜色；否则使用数组第二个元素的颜色。如果数组没有第二个元素，则始终使用第一个元素的颜色。

4. **半选实现原理**：半选功能通过在每个评分图标上覆盖一个宽度为 50% 的透明层（`.wd-rate__item-half`）实现。点击该透明层时，触发半选逻辑，评分值为当前索引加 0.5。半选层的点击事件会阻止事件冒泡（`@click.stop`）。

5. **滑动评分**：组件通过监听 `touchmove` 事件实现滑动选择评分。滑动时获取所有评分项的位置信息，根据触摸点的 `clientX` 坐标判断覆盖的评分项索引，再根据是否开启半选以及触摸点在评分项中的具体位置来计算半选/全选的评分值。在只读或禁用状态下，滑动评分功能不生效。

6. **clearable 清空逻辑**：当 `clearable` 为 `true` 时，如果点击的评分值与当前 `modelValue` 相等且等于最小值（开启 `allow-half` 时为 0.5，否则为 1），则将评分值重置为 0。

7. **选中颜色通过背景色实现**：组件通过 wd-icon 的 `custom-style` 设置 `background` 属性来实现颜色效果，配合 `-webkit-background-clip: text` 和 `color: transparent` 实现文字/图标的渐变色填充效果。

8. **禁用状态颜色**：当组件处于禁用状态时，已选中图标会使用 `disabled-color` 属性指定的颜色，而不是 `active-color`。
