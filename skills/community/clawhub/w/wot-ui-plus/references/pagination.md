# Pagination 分页


## 组件概况

Pagination 分页组件是一个用于长数据列表或表格场景的页码导航组件。该组件提供上一页/下一页按钮、当前页码与总页数显示、以及可选的分页信息展示功能。支持文字和图标两种导航按钮样式，支持 v-model 双向绑定当前页码，并在页码切换时触发 change 事件。当总页数只有一页时，可选择隐藏整个组件。适用于需要分页展示数据的各种业务场景。

## 核心功能描述

- **页码切换导航**：提供上一页和下一页按钮，当前页码为第一页时上一页按钮禁用，当前页码为最后一页时下一页按钮禁用
- **页码信息展示**：居中显示当前页码与总页数的比例关系，格式为 "当前页 / 总页数"
- **图标模式**：通过 `show-icon` 属性切换为图标导航模式，使用箭头图标替代文字 "上一页 / 下一页"
- **分页信息提示**：通过 `show-message` 属性展示分页详细信息，包括当前页码、总条数和每页条数，信息通过国际化翻译系统输出
- **自动页数计算**：当传入 `total`（总条数）和 `pageSize`（每页条数）时，组件自动通过 `Math.ceil(total / pageSize)` 计算总页数，优先于 `totalPage` 属性
- **单页隐藏**：通过 `hide-if-one-page` 属性控制在总页数只有一页时是否隐藏整个分页组件，减少不必要的 UI 元素
- **自定义按钮文案**：通过 `prev-text` 和 `next-text` 属性自定义上一页和下一页按钮的显示文字，未设置时使用国际化默认值
- **按钮样式联动**：可点击状态的按钮使用实心样式（plain 为 false），禁用状态的按钮使用线框样式（plain 为 true）

## 适用业务场景

- **数据列表分页**：在商品列表、用户列表、订单列表等数据展示场景中，将大量数据分页展示，提升页面加载性能和用户体验
- **表格分页导航**：在管理后台的数据表格底部放置分页组件，配合每页显示条数设置，方便用户浏览和管理大批量数据
- **搜索结果分页**：在搜索结果页中展示分页导航，让用户能够逐页浏览搜索结果
- **信息流分页加载**：在需要控制单次加载数据量的场景中，通过分页组件替代无限滚动，提供更明确的浏览进度感知

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| v-model / modelValue | number | - | 是 | 当前页码，支持双向绑定 |
| totalPage | number | 1 | 否 | 总页数，如果同时传入了 total 则优先使用 total 和 pageSize 计算 |
| total | number | 0 | 否 | 数据总条数，组件会自动根据 total 和 pageSize 计算总页数 |
| pageSize | number | 10 | 否 | 每页显示的数据条数，与 total 配合使用计算总页数 |
| showIcon | boolean | false | 否 | 是否使用图标模式显示上一页/下一页按钮，默认显示文字 |
| showMessage | boolean | false | 否 | 是否展示分页信息提示，包括当前页、总条数和每页条数 |
| hideIfOnePage | boolean | true | 否 | 当总页数只有一页时是否隐藏整个组件 |
| prevText | string | - | 否 | 上一页按钮的自定义文字，未设置时使用国际化默认值 "上一页" |
| nextText | string | - | 否 | 下一页按钮的自定义文字，未设置时使用国际化默认值 "下一页" |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

| 事件名称 | 回调参数 | 说明 |
| --- | --- | --- |
| change | { value: number } | 页码切换时触发，返回切换后的目标页码值 |
| update:modelValue | number | 页码值更新时触发，用于 v-model 双向绑定 |

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### Slots

当前源码中未提供自定义插槽。

## 使用示例

### 示例 1：基础用法

效果说明：展示分页组件的最小接入方式，通过 v-model 绑定当前页码，传入 total 总条数后组件自动计算总页数，点击上一页/下一页按钮切换页码。

```vue
<template>
  <wd-pagination v-model="page" :total="total" @change="handleChange"></wd-pagination>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const page = ref<number>(1)
const total = ref<number>(190)

function handleChange({ value }: { value: number }) {
  console.log('当前切换到第', value, '页')
  // 在此处根据 value 请求对应页的数据
}
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 2：图标模式

效果说明：通过 `show-icon` 属性启用图标导航模式，上一页和下一页按钮显示为箭头图标而非文字，适用于空间紧凑的场景或偏好图形化交互的设计。

```vue
<template>
  <wd-pagination
    v-model="page"
    :total="total"
    show-icon
    @change="handleChange"
  ></wd-pagination>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const page = ref<number>(1)
const total = ref<number>(19)

function handleChange({ value }: { value: number }) {
  console.log('当前切换到第', value, '页')
  // 在此处根据 value 请求对应页的数据
}
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 3：展示分页信息提示

效果说明：同时开启 `show-icon` 和 `show-message` 属性，按钮显示为图标的同时，组件底部展示详细的分页信息，包括当前所在页、数据总条数以及每页显示的条数，帮助用户了解当前浏览位置和数据总量。

```vue
<template>
  <wd-pagination
    v-model="page"
    :total="total"
    :page-size="pageSize"
    show-icon
    show-message
    @change="handleChange"
  ></wd-pagination>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const page = ref<number>(1)
const total = ref<number>(160)
const pageSize = ref<number>(20)

function handleChange({ value }: { value: number }) {
  console.log('当前切换到第', value, '页')
  // 在此处根据 value 请求对应页的数据
}
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 4：自定义按钮文字

效果说明：通过 `prev-text` 和 `next-text` 属性自定义上下页按钮的显示文案，适用于需要非默认文字描述的场景，如使用 "前一篇 / 后一篇" 等特殊文案。

```vue
<template>
  <wd-pagination
    v-model="page"
    :total-page="10"
    prev-text="前一篇"
    next-text="后一篇"
    @change="handleChange"
  ></wd-pagination>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const page = ref<number>(1)

function handleChange({ value }: { value: number }) {
  console.log('当前切换到第', value, '页')
}
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

## 注意事项

- **必须绑定 modelValue**：`modelValue` 是必填属性，请通过 v-model 或 :model-value 绑定当前页码。当前页码小于等于 1 时上一页按钮禁用，大于等于总页数时下一页按钮禁用。
- **总页数计算优先级**：当同时传入 `total` 和 `totalPage` 时，组件优先使用 `total` 除以 `pageSize` 计算总页数。建议根据实际业务情况选择传入方式：有数据总量时传入 `total`，直接知道页数时传入 `totalPage`。
- **单页自动隐藏**：`hide-if-one-page` 默认值为 true，即总页数只有一页时整个组件不会渲染。如需在单页时仍然显示分页组件，请将此属性设为 false。
- **国际化文案**：未设置 `prev-text` 和 `next-text` 时，按钮文字来自组件库的国际化系统，默认文案为 "上一页" 和 "下一页"。分页信息提示中的文案（如 "第 x 页"、"共 x 条"、"每页 x 条"）同样由国际化系统提供。
- **按钮状态联动**：按钮的 `plain` 属性与可点击状态联动，可点击时为实心按钮，禁用时为线框样式，同时按钮会设置 `disabled` 属性阻止点击。请勿通过外部 CSS 覆盖按钮的禁用状态。
- **页数变更重新计算**：当 `total` 属性发生变化时，组件会自动重新计算总页数。请确保传入的 `pageSize` 值始终大于 0，否则可能导致计算异常（除以零）。
- **页码边界保护**：点击上一页按钮时，如果当前页码小于 2 则不触发切换；点击下一页按钮时，如果当前页码大于等于总页数减 1 则不触发切换，防止越界。
- **暗色主题适配**：组件内置了对 wot-theme-dark 暗色主题的样式适配，在暗色模式下背景色和文字颜色会自动切换，无需额外配置。
