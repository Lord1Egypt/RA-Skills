# Collapse 折叠面板


## 组件概况

Collapse 折叠面板组件用于对复杂内容进行分区折叠展示，用户可通过点击面板标题展开或收起对应内容区域。该组件由 `wd-collapse`（折叠面板容器）和 `wd-collapse-item`（折叠面板子项）两个关联组件组成，支持普通多面板展开、手风琴模式、查看更多模式以及面板嵌套等多种交互形式。组件内置流畅的展开收起动画，并支持在展开前通过回调函数进行拦截控制。

## 核心功能描述

- **多面板同时展开**：默认模式下多个面板可同时处于展开状态，`modelValue` 为字符串数组类型
- **手风琴模式**：通过 `accordion` 属性开启，同一时间仅允许一个面板展开，`modelValue` 为字符串类型
- **查看更多模式**：通过 `viewmore` 属性开启，将内容以指定行数展示，超出部分通过"展开/收起"按钮控制显示
- **面板嵌套**：支持在 `wd-collapse-item` 的内容区域中嵌套另一个 `wd-collapse`，实现多级折叠效果
- **展开前拦截**：通过 `beforeExpend` 属性在面板展开前执行回调，返回 `false` 可阻止展开，支持异步 `Promise`
- **全部控制**：通过 `toggleAll` 方法实现一键全部展开、全部收起或全部切换，支持跳过禁用面板
- **禁用面板**：通过 `disabled` 属性禁用特定面板的展开/收起交互
- **自定义标题**：通过 `#title` 插槽完全自定义面板标题区域，支持获取展开状态、禁用状态等上下文信息
- **流畅动画**：展开收起过程中使用 CSS transition 动画（0.3s ease-in-out），基于内容高度动态计算
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **帮助与FAQ**：常见问题解答列表，每个问题作为面板标题，答案作为面板内容
- **设置面板**：分组设置项的折叠展示，如通知设置、隐私设置、账号设置等
- **订单详情**：订单列表中折叠展示详细信息（收货地址、商品明细、物流信息等）
- **长文本摘要**：使用 `viewmore` 模式展示长文本摘要，用户点击展开阅读全文
- **多层级分类**：商品分类、组织架构等需要多级折叠展示的场景
- **表单高级选项**：默认收起的高级筛选条件、附加选项等

## API

### wd-collapse Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | `string \| string[] \| boolean` | - | 否 | 绑定值。普通模式下为展开面板的 name 数组 `string[]`；手风琴模式下为当前展开面板的 name `string`；查看更多模式下为是否展开的布尔值 `boolean` |
| accordion | boolean | false | 否 | 是否开启手风琴模式，开启后同一时间只能展开一个面板 |
| viewmore | boolean | false | 否 | 是否开启查看更多模式，将内容以固定行数展示，超出部分可展开 |
| useMoreSlot | boolean | false | 否 | 是否使用自定义展开按钮插槽（`#more`），仅在 `viewmore` 模式下生效 |
| customMoreSlotClass | string | `''` | 否 | 查看更多模式下自定义展开按钮插槽的样式类名 |
| lineNum | number | 2 | 否 | 查看更多模式下，收起时的最大显示行数 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类 |

### wd-collapse-item Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| name | string | - | **是** | 面板的唯一标识符，用于与 `modelValue` 关联 |
| title | string | `''` | 否 | 面板标题文字，也可通过 `#title` 插槽传递自定义内容 |
| disabled | boolean | false | 否 | 是否禁用该面板，禁用后无法点击展开/收起 |
| beforeExpend | `(name: string) => boolean \| Promise<unknown>` | - | 否 | 展开前的回调函数，返回 `false` 可以阻止展开，支持返回 Promise 进行异步控制 |
| customBodyClass | string | `''` | 否 | 自定义折叠内容区域的样式类名 |
| customBodyStyle | string | `''` | 否 | 自定义折叠内容区域的样式 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点样式类 |

### wd-collapse Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | `{ value: string \| string[] \| boolean }` | 面板展开/收起状态变化时触发，`value` 的值类型与 `modelValue` 一致 |
| update:modelValue | `string \| string[] \| boolean` | 面板状态变化时触发更新，用于 `v-model` 双向绑定 |

### wd-collapse Methods

通过 ref 可以获取 `wd-collapse` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| toggleAll | `options?: boolean \| { expanded?: boolean; skipDisabled?: boolean }` | void | 切换所有面板展开状态。不传参为全部切换；传 `true` 为全部展开；传 `false` 为全部收起；传对象时可指定 `expanded`（目标状态）和 `skipDisabled`（是否跳过禁用面板） |

> **注意**：`toggleAll` 方法在手风琴模式（`accordion`）下无效。

### wd-collapse-item Methods

通过 ref 可以获取 `wd-collapse-item` 实例并调用以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
|---------|------|--------|------|
| getExpanded | 无 | `boolean` | 获取当前面板的展开状态 |
| updateExpand | 无 | `Promise<void>` | 更新当前面板的展开状态 |

### wd-collapse Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 折叠面板内容区域，用于放置 `wd-collapse-item` 组件（普通/手风琴模式）或内容文本（查看更多模式） |
| more | - | 自定义查看更多模式下的展开/收起按钮内容，仅在 `viewmore` 和 `useMoreSlot` 同时为 `true` 时生效 |

### wd-collapse-item Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 面板展开后的内容区域 |
| title | `{ expanded: boolean; disabled: boolean; isFirst: boolean }` | 自定义面板标题区域。`expanded` 为当前展开状态，`disabled` 为禁用状态，`isFirst` 是否为第一个面板 |

## 类型定义

### CollapseToggleAllOptions

```ts
type CollapseToggleAllOptions =
  | boolean
  | {
      expanded?: boolean
      skipDisabled?: boolean
    }
```

`toggleAll` 方法的参数类型。传入 `boolean` 时，`true` 表示全部展开，`false` 表示全部收起。传入对象时可精细控制展开行为。

### CollapseInstance

```ts
type CollapseInstance = ComponentPublicInstance<CollapseProps, CollapseExpose>
```

通过 `ref<CollapseInstance>()` 获取折叠面板容器实例的类型定义。

### CollapseItemBeforeExpand

```ts
type CollapseItemBeforeExpand = (name: string) => boolean | Promise<unknown>
```

展开前回调函数类型。接收当前面板的 `name` 作为参数，返回 `false` 可阻止展开，返回 `Promise` 可异步控制展开行为。

## 使用示例

### 示例 1：基本用法

展示普通多面板展开效果，多个面板可同时展开。通过 `v-model` 绑定展开面板的 name 数组，`@change` 事件监听状态变化。

```vue
<template>
  <wd-collapse v-model="activeNames" @change="handleChange">
    <wd-collapse-item
      v-for="item in items"
      :key="item.name"
      :title="item.title"
      :name="item.name"
      :disabled="item.disabled"
    >
      {{ item.content }}
    </wd-collapse-item>
  </wd-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeNames = ref<string[]>(['item1'])

const items = ref([
  {
    title: '标签1',
    name: 'item1',
    content: '这是一条简单的示例文字。这是一条简单的示例文字。这是一条简单的示例文字。'
  },
  {
    title: '标签2',
    name: 'item2',
    content: '这是一条简单的示例文字。',
    disabled: true
  },
  {
    title: '标签3',
    name: 'item3',
    content: '这是一条简单的示例文字。这是一条简单的示例文字。'
  }
])

function handleChange({ value }: { value: string[] }) {
  console.log('当前展开的面板:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

`modelValue` 在普通模式下为字符串数组，包含所有已展开面板的 `name` 值。初始化时可设置默认展开的面板。被禁用的面板不会响应点击事件，但仍然可以通过 `toggleAll` 方法控制（除非设置 `skipDisabled: true`）。

### 示例 2：手风琴模式

开启手风琴模式后，同一时间只允许一个面板处于展开状态，展开新面板会自动收起已展开的面板。

```vue
<template>
  <wd-collapse v-model="activeName" accordion @change="handleChange">
    <wd-collapse-item title="标签1" name="item1">
      这是一条简单的示例文字。
    </wd-collapse-item>
    <wd-collapse-item title="标签2" name="item2">
      这是一条简单的示例文字。这是一条简单的示例文字。这是一条简单的示例文字。
    </wd-collapse-item>
    <wd-collapse-item title="标签3" name="item3">
      这是一条简单的示例文字。
    </wd-collapse-item>
  </wd-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

// 手风琴模式下 modelValue 为 string 类型
const activeName = ref<string>('item1')

function handleChange({ value }: { value: string }) {
  console.log('当前展开的面板:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

手风琴模式下，`accordion` 属性设置为 `true`，此时 `modelValue` 的类型必须是 `string` 而非数组。当用户点击已展开的面板时，该面板会收起（`modelValue` 变为空字符串 `''`）。点击未展开的面板时，已展开的面板自动收起，新面板展开。

### 示例 3：查看更多模式

将长文本内容以指定行数截断展示，用户点击"展开"/"收起"按钮查看完整内容。

```vue
<template>
  <view>
    <!-- 默认显示 2 行 -->
    <wd-collapse viewmore v-model="expanded" @change="handleChange4">
      这是一条简单的示例文字。这是一条简单的示例文字。这是一条简单的示例文字。
      这是一条简单的示例文字。这是一条简单的示例文字。这是一条简单的示例文字。
    </wd-collapse>

    <!-- 自定义显示行数 -->
    <wd-collapse viewmore v-model="expanded2" :line-num="3" @change="handleChange5">
      行数显示设置：这是一条简单的示例文字。这是一条简单的示例文字。
      这是一条简单的示例文字。这是一条简单的示例文字。
    </wd-collapse>

    <!-- 自定义展开按钮 -->
    <wd-collapse
      viewmore
      v-model="expanded3"
      use-more-slot
      custom-more-slot-class="more-slot"
      @change="handleChange6"
    >
      具名插槽：这是一条简单的示例文字。这是一条简单的示例文字。
      这是一条简单的示例文字。这是一条简单的示例文字。这是一条简单的示例文字。
      <template #more>
        <view>显示全部</view>
      </template>
    </wd-collapse>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const expanded = ref<boolean>(false)
const expanded2 = ref<boolean>(false)
const expanded3 = ref<boolean>(false)

function handleChange4({ value }: { value: boolean }) {
  console.log('展开状态:', value)
}

function handleChange5({ value }: { value: boolean }) {
  console.log('展开状态:', value)
}

function handleChange6({ value }: { value: boolean }) {
  console.log('展开状态:', value)
}
</script>

<style lang="scss" scoped>
:deep(.more-slot) {
  color: red;
}
</style>
```

查看更多模式下，`viewmore` 属性设置为 `true`，此时 `modelValue` 为 `boolean` 类型。`lineNum` 控制收起时显示的最大行数，默认值为 2。通过 `useMoreSlot` 和 `#more` 插槽可完全自定义展开/收起按钮的内容和样式。

### 示例 4：自定义标题

通过 `#title` 插槽完全自定义面板标题，可获取展开状态、禁用状态等上下文信息进行动态渲染。

```vue
<template>
  <wd-collapse v-model="activeNames">
    <wd-collapse-item name="item1">
      <template #title="{ expanded }">
        <view class="header">
          <text style="color: red">通过 slot 自定义标题</text>
          <text>{{ expanded ? '我展开了' : '我已收起' }}</text>
        </view>
      </template>
      这是面板内容，标题通过 slot 自定义。
    </wd-collapse-item>

    <wd-collapse-item name="item2" disabled>
      <template #title="{ expanded, disabled }">
        <view class="header">
          <text v-if="disabled">被禁用</text>
          <text style="color: red" v-else>通过 slot 自定义 title</text>
          <text>{{ expanded ? '我展开了' : '我已收起' }}</text>
        </view>
      </template>
      这是一个被禁用的面板。
    </wd-collapse-item>
  </wd-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeNames = ref<string[]>(['item1'])
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
```

`#title` 插槽的作用域参数包含 `expanded`（当前展开状态）、`disabled`（禁用状态）、`isFirst`（是否为第一个面板）。可在标题中放置任意组件和布局，实现复杂的面板标题样式。

### 示例 5：全部控制

通过 `toggleAll` 方法实现一键控制所有面板的展开/收起状态。

```vue
<template>
  <view>
    <wd-button type="info" @click="collapse?.toggleAll()">全部切换</wd-button>
    <wd-button type="success" @click="collapse?.toggleAll(true)">全部展开</wd-button>
    <wd-button type="primary" @click="collapse?.toggleAll(false)">全部收起</wd-button>
    <wd-button type="warning" @click="collapse?.toggleAll({ skipDisabled: true })">
      全部切换（跳过禁用）
    </wd-button>
    <wd-button type="error" @click="collapse?.toggleAll({ expanded: true, skipDisabled: true })">
      全部展开（跳过禁用）
    </wd-button>

    <wd-collapse ref="collapse" v-model="activeNames">
      <wd-collapse-item
        v-for="item in items"
        :key="item.name"
        :title="item.title"
        :name="item.name"
        :disabled="item.disabled"
      >
        {{ item.content }}
      </wd-collapse-item>
    </wd-collapse>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { CollapseInstance } from '@/uni_modules/wot-ui-plus/components/wd-collapse/types'

const collapse = ref<CollapseInstance>()

const activeNames = ref<string[]>(['item1'])

const items = ref([
  { title: '标签1', name: 'item1', content: '内容1', disabled: false },
  { title: '标签2', name: 'item2', content: '内容2', disabled: true },
  { title: '标签3', name: 'item3', content: '内容3', disabled: false },
  { title: '标签4', name: 'item4', content: '内容4', disabled: false },
  { title: '标签5', name: 'item5', content: '内容5', disabled: false }
])
</script>

<style lang="scss" scoped>
:deep(.custom-button) {
  margin-right: 16px;
  margin-bottom: 16px;
}
</style>
```

`toggleAll()` 方法支持三种参数形式：不传参时在展开/收起间切换；传 `true` 全部展开，传 `false` 全部收起；传对象时可指定 `expanded` 目标状态和 `skipDisabled` 是否跳过禁用面板。该方法在手风琴模式下无效。

### 示例 6：展开前拦截

通过 `beforeExpend` 属性在面板展开前执行回调，支持同步返回和异步 Promise，可用于动态加载数据等场景。

```vue
<template>
  <wd-collapse v-model="activeNames">
    <wd-collapse-item
      v-for="item in items"
      :key="item.name"
      :title="item.title"
      :name="item.name"
      :before-expend="item.name === 'item3' ? beforeExpand : undefined"
    >
      {{ item.content }}
    </wd-collapse-item>
  </wd-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()
const activeNames = ref<string[]>(['item1'])

const items = ref([
  { title: '标签1', name: 'item1', content: '内容1' },
  { title: '标签2', name: 'item2', content: '内容2' },
  {
    title: '标签3',
    name: 'item3',
    content: '这是一条简单的示例文字。'
  }
])

/**
 * 展开前回调，返回 Promise 实现异步控制
 */
function beforeExpand(name: string) {
  return new Promise<void>((resolve, reject) => {
    toast.loading('加载中...')
    setTimeout(() => {
      toast.close()
      // 动态更新内容
      const index = items.value.findIndex((item) => item.name === name)
      if (index > -1) {
        items.value[index].content = '这是异步加载后的新内容。'.repeat(5)
      }
      resolve()
    }, 500)
  })
}
</script>

<style lang="scss" scoped>
</style>
```

`beforeExpend` 回调函数接收面板的 `name` 作为参数。若返回 `false` 则阻止面板展开；若返回 `Promise`，则在 Promise resolve 时展开面板，reject 时阻止展开。此功能适用于展开前需要加载数据的场景。

### 示例 7：面板嵌套

在折叠面板内容区域中嵌套另一个折叠面板，实现多级折叠效果。

```vue
<template>
  <wd-collapse v-model="rootActive" @change="handleRootChange">
    <wd-collapse-item
      v-for="i in 5"
      :key="i"
      :title="`一级标签 ${i}`"
      :name="String(i)"
    >
      <!-- 嵌套二级折叠面板 -->
      <wd-collapse v-model="childActive[i - 1]" custom-body-style="padding: 0 0 0 14px">
        <wd-collapse-item
          v-for="item in childItems"
          :key="item.name"
          :title="item.title"
          :name="item.name"
        >
          {{ item.content }}
        </wd-collapse-item>
      </wd-collapse>
    </wd-collapse-item>
  </wd-collapse>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const rootActive = ref<string[]>(['1'])
const childActive = ref<string[][]>([['item1'], ['item2'], ['item3'], ['item4'], ['item5']])

const childItems = ref([
  { title: '二级标签A', name: 'itemA', content: '二级内容A' },
  { title: '二级标签B', name: 'itemB', content: '二级内容B' },
  { title: '二级标签C', name: 'itemC', content: '二级内容C' }
])

function handleRootChange({ value }: { value: string[] }) {
  console.log('一级面板状态:', value)
}
</script>

<style lang="scss" scoped>
</style>
```

通过在 `wd-collapse-item` 的默认插槽中放置另一个 `wd-collapse` 组件，可实现多级嵌套折叠。每个层级的 `wd-collapse` 需要独立维护各自的 `v-model` 状态。使用 `custom-body-style` 可调整内层面板的缩进效果。

## 注意事项

1. **modelValue 类型与模式对应关系**：普通模式下 `modelValue` 必须为 `string[]` 数组类型；手风琴模式下必须为 `string` 字符串类型；查看更多模式下必须为 `boolean` 布尔值。若类型不匹配，组件会在控制台输出错误警告。

2. **name 属性必填**：`wd-collapse-item` 的 `name` 属性为必填项，用于在 `modelValue` 中标识面板。`toggleAll` 方法在收集面板名称时，若没有 `name` 则会使用面板的索引值作为替代。

3. **手风琴模式下 toggleAll 无效**：在 `accordion` 为 `true` 的手风琴模式下，`toggleAll` 方法不会执行任何操作，直接返回。

4. **beforeExpend 拦截机制**：`beforeExpend` 回调仅在面板即将展开时触发（收起时不会触发）。返回 `false` 或 Promise reject 都会阻止展开操作。若 `beforeExpend` 抛出异常，展开也会被阻止。

5. **动画实现原理**：面板展开收起使用 CSS `transition` 动画，通过动态获取内容区域的实际高度（`getRect`）设置 `height` 值，动画时长为 0.3s，缓动函数为 `ease-in-out`。展开完成后 `height` 会被清空（设为 `''`）以适配内容变化。

6. **边框显示**：每个 `wd-collapse-item` 默认带有顶部边框（使用 `halfPixelBorder` 实现 0.5px 细边框）。第一个面板不显示顶部边框。展开的面板标题底部也会显示边框分隔线。

7. **查看更多模式的实现**：`viewmore` 模式下使用 `-webkit-line-clamp` CSS 属性实现文本截断，配合 `lineNum` 属性控制显示行数。展开时通过动态设置 `line-clamp` 为 0 来显示完整内容。

8. **样式隔离与定制**：组件启用了 `virtualHost: true` 和 `styleIsolation: 'shared'`，支持外部样式穿透。可通过 `customBodyClass`、`customBodyStyle` 自定义面板内容区样式，通过 `customClass`、`customStyle` 自定义根节点样式。

9. **暗色模式自动适配**：组件已内置暗色主题样式，当根节点包含 `wot-theme-dark` 类名时，背景色、文字颜色、边框颜色等都会自动切换为暗色主题值。

10. **无障碍交互**：面板标题区域使用 `user-select: none` 防止文字被选中。箭头图标会根据展开状态旋转 180 度，过渡动画时长 0.3s。
