# SortButton 排序按钮


## 组件概况

SortButton 排序按钮组件是一个用于列表排序操作的交互组件，通过点击按钮在升序、降序和无排序三种状态之间切换。组件由左侧标题文字和右侧上下箭头图标组成，每次点击按照预设的顺序循环切换排序状态。支持双箭头（上下两个箭头）和填充箭头样式，可自定义下划线、箭头颜色、切换顺序等选项，适用于商品列表、数据表格等需要排序功能的场景。

组件内部通过 `modelValue` 属性表示当前排序状态：`1` 表示升序，`-1` 表示降序，`0` 表示无排序（默认/重置状态）。点击按钮时根据当前状态和配置属性自动计算下一个状态，并通过 `change` 事件和 `update:modelValue` 事件通知外部组件。

## 核心功能描述

- **三态切换**：支持升序（1）、降序（-1）、无排序（0）三种状态的循环切换
- **双箭头展示**：同时展示上箭头和下箭头，当前激活的箭头高亮显示
- **填充箭头样式**：通过 `filled` 属性切换为填充风格的箭头图标，视觉更加醒目
- **升序优先/降序优先**：通过 `descFirst` 属性控制首次点击切换为升序还是降序，默认优先升序
- **重置控制**：通过 `allowReset` 属性控制是否允许从降序状态回到无排序状态（0），默认不允许重置
- **下划线指示**：激活状态时标题文字下方显示下划线，可通过 `line` 属性控制是否显示，通过 `lineColor` 自定义颜色
- **自定义标题**：通过 `title` 属性设置按钮展示的文案，如"价格"、"销量"等
- **v-model 支持**：支持 v-model 双向绑定排序状态值，方便与外部状态管理同步
- **轻量级组件**：组件实现简洁，无外部依赖（除 wd-icon 图标组件外），性能优秀

## 适用业务场景

- **商品列表排序**：电商商品列表页提供价格、销量、好评度等排序按钮
- **数据表格排序**：后台管理系统数据表格的列头排序功能
- **内容列表排序**：资讯、视频等内容列表按发布时间、热度等排序
- **多维度排序组合**：多个 SortButton 组合使用，实现多字段排序（如同时按价格和销量排序）
- **移动端筛选栏**：移动端筛选栏中的排序操作入口

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| modelValue | number | 0 | 否 | 当前排序状态值，`1` 表示升序，`-1` 表示降序，`0` 表示无排序，支持 v-model 双向绑定 |
| title | string | '' | 否 | 排序按钮展示的文案，如"价格"、"销量"等 |
| filled | boolean | false | 否 | 是否展示填充风格的箭头图标，设置为 true 时箭头图标为填充样式 |
| allowReset | boolean | false | 否 | 是否允许重置按钮，即是否允许从降序状态回到无排序状态（0） |
| descFirst | boolean | false | 否 | 是否优先切换为降序，默认优先切换为升序 |
| line | boolean | true | 否 | 是否展示下划线，当只有一个排序按钮时通常不展示下划线 |
| lineColor | string | '$-sort-button-line-color'（跟随主题变量） | 否 | 自定义下划线颜色 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

| 事件名称 | 触发条件 | 回调参数 | 说明 |
| --- | --- | --- | --- |
| change | 点击按钮排序状态发生变化时触发 | `{ value: number }` | value 为新的排序状态值：1（升序）、-1（降序）、0（无排序） |
| update:modelValue | 排序状态发生变化时触发（v-model 支持） | `value: number` | 新的排序状态值 |

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。

### Slots

当前组件未定义插槽。

## 使用示例

### 示例 1：基础用法

效果说明：最基础的排序按钮用法，点击按钮在升序、降序之间循环切换（默认不允许重置为无排序状态）。首次点击切换为升序，再次点击切换为降序，第三次点击回到升序，以此循环。

```vue
<template>
  <view>
    <demo-block title="基础用法">
      <wd-sort-button v-model="value1" title="价格" @change="handleChange" />
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value1 = ref<number>(0)

function handleChange({ value }: { value: number }) {
  console.log('排序值：', value)
  // value: 1 升序, -1 降序, 0 无排序
}
</script>
```

### 示例 2：填充箭头样式

效果说明：通过 `filled` 属性启用填充风格的箭头图标，视觉更加醒目。当前激活的箭头会显示为填充样式，未激活的箭头为轮廓样式。

```vue
<template>
  <view>
    <demo-block title="填充箭头样式">
      <wd-sort-button v-model="value1" filled title="价格" @change="handleChange" />
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value1 = ref<number>(0)

function handleChange({ value }: { value: number }) {
  console.log('排序值：', value)
}
</script>
```

### 示例 3：允许重置

效果说明：通过 `allowReset` 属性允许从降序状态回到无排序状态。设置后点击顺序为：升序（1） -> 降序（-1） -> 无排序（0） -> 升序（1），形成完整循环。适用于需要清除排序的场景。

```vue
<template>
  <view>
    <demo-block title="允许重置">
      <wd-sort-button v-model="value3" title="价格" allow-reset @change="handleChange" />
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value3 = ref<number>(0)

function handleChange({ value }: { value: number }) {
  console.log('排序值：', value)
  if (value === 0) {
    console.log('已清除排序')
  } else if (value === 1) {
    console.log('升序排列')
  } else {
    console.log('降序排列')
  }
}
</script>
```

### 示例 4：降序优先切换

效果说明：通过 `descFirst` 属性设置首次点击切换为降序。设置后点击顺序为：降序（-1） -> 升序（1） -> 降序（-1）。如果同时设置 `allowReset`，则循环为：降序（-1） -> 升序（1） -> 无排序（0） -> 降序（-1）。

```vue
<template>
  <view>
    <demo-block title="降序优先">
      <wd-sort-button v-model="value4" title="价格" desc-first @change="handleChange" />
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value4 = ref<number>(0)

function handleChange({ value }: { value: number }) {
  console.log('排序值：', value)
}
</script>
```

### 示例 5：自定义下划线颜色

效果说明：通过 `lineColor` 属性自定义激活状态下划线颜色，通过 `line` 属性控制是否显示下划线。当页面中只有一个排序按钮时，通常设置 `line` 为 false 不展示下划线以保持简洁。

```vue
<template>
  <view>
    <!-- 自定义下划线颜色 -->
    <demo-block title="自定义下划线颜色">
      <wd-sort-button v-model="value2" line-color="red" title="价格" @change="handleChange" />
    </demo-block>

    <!-- 不展示下划线 -->
    <demo-block title="不展示下划线">
      <wd-sort-button v-model="value5" title="价格" :line="false" @change="handleChange" />
    </demo-block>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const value2 = ref<number>(0)
const value5 = ref<number>(0)

function handleChange({ value }: { value: number }) {
  console.log('排序值：', value)
}
</script>
```

### 示例 6：多字段排序组合

效果说明：在实际业务中，通常会组合使用多个 SortButton 组件实现多字段排序。每个按钮独立维护自己的排序状态，点击某个按钮时可将其他按钮的排序状态重置。

```vue
<template>
  <view>
    <view class="sort-bar">
      <wd-sort-button v-model="priceSort" title="价格" :line="false" @change="handlePriceChange" />
      <wd-sort-button v-model="salesSort" title="销量" :line="false" @change="handleSalesChange" />
      <wd-sort-button v-model="timeSort" title="时间" :line="false" @change="handleTimeChange" />
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const priceSort = ref<number>(0)
const salesSort = ref<number>(0)
const timeSort = ref<number>(0)

function handlePriceChange({ value }: { value: number }) {
  // 点击价格排序时，重置其他排序
  if (value !== 0) {
    salesSort.value = 0
    timeSort.value = 0
  }
  console.log('价格排序：', value)
  doSort('price', value)
}

function handleSalesChange({ value }: { value: number }) {
  if (value !== 0) {
    priceSort.value = 0
    timeSort.value = 0
  }
  console.log('销量排序：', value)
  doSort('sales', value)
}

function handleTimeChange({ value }: { value: number }) {
  if (value !== 0) {
    priceSort.value = 0
    salesSort.value = 0
  }
  console.log('时间排序：', value)
  doSort('time', value)
}

function doSort(field: string, sortType: number) {
  // 发起排序请求
  console.log(`按 ${field} ${sortType === 1 ? '升序' : sortType === -1 ? '降序' : '默认排序'}`)
}
</script>

<style scoped lang="scss">
.sort-bar {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  background-color: #fff;
}
</style>
```

## 注意事项

1. **状态值含义**：`modelValue` 的三个状态值分别表示：`1`（升序）、`-1`（降序）、`0`（无排序/默认状态）。使用时需根据实际业务逻辑处理这三个状态值。

2. **切换顺序逻辑**：
   - 默认情况（`descFirst: false`，`allowReset: false`）：0 -> 1 -> -1 -> 1（循环）
   - 降序优先（`descFirst: true`，`allowReset: false`）：0 -> -1 -> 1 -> -1（循环）
   - 允许重置 + 默认（`descFirst: false`，`allowReset: true`）：0 -> 1 -> -1 -> 0（循环）
   - 允许重置 + 降序优先（`descFirst: true`，`allowReset: true`）：0 -> -1 -> 1 -> 0（循环）

3. **下划线使用场景**：当页面中只有一个排序按钮时，建议设置 `line` 为 `false` 不展示下划线。当有多个排序按钮组合使用时，建议保持 `line` 为 `true` 以增强激活状态的视觉辨识度。

4. **箭头图标切换**：升序状态（1）时，上箭头激活、下箭头非激活；降序状态（-1）时，下箭头激活、上箭头非激活；无排序状态（0）时，两个箭头均非激活。

5. **样式自定义**：推荐使用 `customStyle` 和 `customClass` 属性进行组件根元素样式定制。下划线颜色通过 `lineColor` 属性自定义，支持 CSS 颜色值和 CSS 变量。

6. **active 状态样式**：当排序状态不为 0 时，标题文字和箭头图标都会添加 `is-active` 类名，可通过该类名自定义激活状态的样式（如文字颜色变化）。

7. **v-model 双向绑定**：推荐使用 v-model 绑定排序状态值，这样组件会自动更新状态。也可以在 `change` 事件中根据业务逻辑手动修改 `modelValue` 的值。

8. **多按钮互斥**：在多个排序按钮组合使用时，通常需要在某个按钮激活时将其他按钮重置为 0（无排序）状态，以保证同一时间只有一个排序字段生效。

9. **与后端排序对接**：将 `change` 事件返回的 `value` 值转换为后端排序参数（如 `1` 对应 `asc`，`-1` 对应 `desc`），传递给后端接口实现数据排序。

10. **虚拟宿主配置**：组件配置了 `virtualHost: true`、`addGlobalClass: true` 和 `styleIsolation: 'shared'`，在小程序环境下可正确继承外部样式并支持全局样式穿透。
