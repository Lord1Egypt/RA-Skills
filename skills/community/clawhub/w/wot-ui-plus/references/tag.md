# Tag 标签


## 组件概况

Tag 标签组件是一种轻量级的标记和分类元素，用于对内容进行分类、状态标识或关键词展示。该组件支持多种类型样式（默认、主要、成功、警告、危险），提供幽灵、圆角、标记等多种外观变体，并内置图标集成、自定义颜色、可关闭和动态新增等交互能力，适用于标签云、分类筛选、内容标记等多种业务场景。

标签以行内块元素渲染，支持灵活的尺寸适配和状态切换，能够有效组织信息层级，提升用户对内容分类的识别效率。

## 核心功能描述

- **多种标签类型**：支持 `default`（默认）、`primary`（主要）、`success`（成功）、`warning`（警告）、`danger`（危险）五种类型
- **幽灵样式**：通过 `plain` 属性切换为透明背景、带边框的幽灵标签
- **圆角标签**：通过 `round` 属性将标签切换为全圆角胶囊形状
- **标记标签**：通过 `mark` 属性生成左圆右方的标记样式，适用于侧边标记场景
- **图标支持**：通过 `icon` 属性快速设置左侧图标，或使用 `use-icon-slot` 插槽自定义图标内容
- **自定义颜色**：通过 `color` 和 `bg-color` 属性自定义文字颜色与背景/边框颜色
- **可关闭**：通过 `closable` 属性在圆角标签右侧显示关闭图标，支持点击移除
- **动态新增**：通过 `dynamic` 属性将标签切换为新增模式，点击后可输入新标签内容
- **状态切换**：支持默认、悬浮、点击、聚焦等多种交互状态的视觉反馈

## 适用业务场景

- **内容分类**：文章、商品、话题等内容所属分类的可视化标记
- **状态标识**：订单状态、任务进度、审核结果等业务状态的快速识别
- **标签筛选**：搜索过滤条件、标签云、兴趣标签等可交互筛选元素
- **关键词展示**：搜索热词、话题标签、产品特性关键词等
- **可编辑标签组**：支持动态新增和删除的标签集合，如用户兴趣标签管理
- **消息标记**：消息类型标记、重要程度标识等
- **组合标签**：带图标的标签，如时间标签、位置标签、分类标签等

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| type | 标签类型 | string | default / primary / success / warning / danger | default | - |
| plain | 是否为幽灵标签，透明背景带边框 | boolean | - | false | - |
| round | 是否为圆角标签 | boolean | - | false | - |
| mark | 是否为标记标签，左圆右方样式 | boolean | - | false | - |
| icon | 左侧图标类名 | string | - | '' | - |
| useIconSlot | 是否开启图标插槽，开启后将使用 slot 中的图标而非 icon 属性 | boolean | - | false | - |
| closable | 是否可关闭，仅对圆角标签生效 | boolean | - | false | - |
| dynamic | 是否为新增标签模式 | boolean | - | false | - |
| color | 文字颜色 | string | - | '' | - |
| bgColor | 背景色和边框色 | string | - | '' | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点类名 | string | - | '' | - |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| click | event | 标签点击事件 |
| close | event | 标签关闭事件，`closable` 为 true 时有效 |
| confirm | { value: string } | 新增标签确认事件，`dynamic` 为 true 时有效，返回输入框中的值 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 标签内容，可放置文字或其他组件 |
| icon | - | 自定义图标，需设置 `use-icon-slot` 为 true |
| add | - | 自定义新增按钮内容，需设置 `dynamic` 为 true |

### 外部样式类

| 类名 | 说明 |
|------|------|
| custom-class | 根节点自定义样式类 |
| custom-style | 根节点内联样式 |

## 使用示例

### 示例 1：基本用法

展示不同类型的标签效果，通过 `type` 属性控制标签的主题色。

```vue
<template>
  <view>
    <wd-tag>默认标签</wd-tag>
    <wd-tag type="primary">主要标签</wd-tag>
    <wd-tag type="success">成功标签</wd-tag>
    <wd-tag type="warning">警告标签</wd-tag>
    <wd-tag type="danger">危险标签</wd-tag>
  </view>
</template>
<script lang="ts" setup>
</script>
```

`type` 属性支持 `default`（默认灰色）、`primary`（主要蓝色）、`success`（成功绿色）、`warning`（警告橙色）、`danger`（危险红色）五种类型。默认类型为 `default`，标签以行内块方式排列。

### 示例 2：幽灵标签与圆角标签

展示幽灵样式和圆角样式的标签效果。

```vue
<template>
  <view>
    <!-- 幽灵标签 -->
    <wd-tag plain>默认幽灵</wd-tag>
    <wd-tag type="primary" plain>主要幽灵</wd-tag>
    <wd-tag type="success" plain>成功幽灵</wd-tag>
    <wd-tag type="warning" plain>警告幽灵</wd-tag>
    <wd-tag type="danger" plain>危险幽灵</wd-tag>

    <!-- 圆角标签 -->
    <wd-tag round>默认圆角</wd-tag>
    <wd-tag type="primary" round>主要圆角</wd-tag>
    <wd-tag type="success" round>成功圆角</wd-tag>
    <wd-tag type="warning" round>警告圆角</wd-tag>
    <wd-tag type="danger" round>危险圆角</wd-tag>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `plain` 属性将标签切换为幽灵样式（透明背景，边框和文字颜色与类型一致）。通过 `round` 属性将标签切换为全圆角胶囊形状。两种样式可以组合使用，也可以与 `mark` 属性叠加实现标记标签效果。

### 示例 3：标记标签

展示标记类型的标签，适用于侧边标记、分类标识等场景。

```vue
<template>
  <view>
    <!-- 基础标记 -->
    <wd-tag mark>默认标记</wd-tag>
    <wd-tag type="primary" mark>主要标记</wd-tag>
    <wd-tag type="success" mark>成功标记</wd-tag>
    <wd-tag type="warning" mark>警告标记</wd-tag>
    <wd-tag type="danger" mark>危险标记</wd-tag>

    <!-- 幽灵标记 -->
    <wd-tag mark plain>默认标记</wd-tag>
    <wd-tag type="primary" mark plain>主要标记</wd-tag>
    <wd-tag type="success" mark plain>成功标记</wd-tag>
    <wd-tag type="warning" mark plain>警告标记</wd-tag>
    <wd-tag type="danger" mark plain>危险标记</wd-tag>
  </view>
</template>
<script lang="ts" setup>
</script>
```

`mark` 属性将标签左侧设置为圆角，右侧为直角，形成标记样式。可与 `plain` 属性组合使用实现幽灵标记效果。

### 示例 4：带图标的标签

在标签中集成图标，增强视觉识别性。

```vue
<template>
  <view>
    <!-- 使用 icon 属性设置图标 -->
    <wd-tag icon="clock" mark>时间标签</wd-tag>
    <wd-tag icon="location" type="primary">位置标签</wd-tag>

    <!-- 使用 icon 插槽自定义图标 -->
    <wd-tag use-icon-slot type="success">
      <template #icon>
        <wd-icon name="check" />
      </template>
      成功
    </wd-tag>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `icon` 属性可快速设置左侧图标。若需要更复杂的图标定制（如使用自定义组件），可设置 `use-icon-slot` 为 `true`，然后在 `icon` 插槽中放置自定义内容。图标默认显示在标签文字左侧，间距为 4px。

### 示例 5：自定义颜色

通过 `color` 和 `bg-color` 属性自定义标签的颜色样式。

```vue
<template>
  <view>
    <!-- 自定义文字和背景颜色 -->
    <wd-tag color="#0083ff" bg-color="#d0e8ff">自定义标签</wd-tag>

    <!-- 幽灵样式配合自定义颜色 -->
    <wd-tag color="#FAA21E" bg-color="#FAA21E" plain>幽灵自定义</wd-tag>
  </view>
</template>
<script lang="ts" setup>
</script>
```

`color` 属性控制标签内文字颜色，`bg-color` 属性控制背景色（非幽灵模式）或边框色（幽灵模式）。自定义颜色优先级高于 `type` 属性设置的主题色。

### 示例 6：可关闭标签

展示支持关闭功能的标签，适用于标签移除、筛选条件清除等场景。

```vue
<template>
  <view>
    <wd-tag
      v-for="(tag, index) in tags"
      :key="tag.id"
      :type="tag.type"
      round
      closable
      @click="handleClick(index)"
      @close="handleClose(index)"
    >
      {{ tag.name }}
    </wd-tag>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const tags = ref([
  { id: 1, type: 'primary', name: '标签一' },
  { id: 2, type: 'success', name: '标签二' },
  { id: 3, type: 'warning', name: '标签三' }
])

function handleClick(index: number) {
  console.log('点击标签:', index)
}

function handleClose(index: number) {
  tags.value = tags.value.filter((_, i) => i !== index)
  console.log('关闭标签:', index)
}
</script>
```

`closable` 属性会在圆角标签右侧显示关闭图标，点击关闭图标时触发 `close` 事件，点击标签其他区域时触发 `click` 事件。注意：关闭图标仅在 `round` 为 `true` 时显示。

### 示例 7：动态新增标签

展示支持用户动态新增标签的功能，适用于标签管理、兴趣选择等场景。

```vue
<template>
  <view>
    <!-- 已有标签列表 -->
    <wd-tag
      v-for="(tag, index) in dynamicTags"
      :key="index"
      round
      closable
      @close="handleClose(index)"
    >
      {{ tag }}
    </wd-tag>

    <!-- 新增标签按钮 -->
    <wd-tag round dynamic @confirm="handleConfirm"></wd-tag>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const dynamicTags = ref(['标签一', '标签二'])

function handleClose(index: number) {
  dynamicTags.value = dynamicTags.value.filter((_, i) => i !== index)
}

function handleConfirm({ value }: { value: string }) {
  if (!value) return
  dynamicTags.value = [...dynamicTags.value, value]
}
</script>
```

设置 `dynamic` 属性后，标签会显示为新增模式。点击后切换为输入框，用户输入内容并在确认（失去焦点或按下回车）时触发 `confirm` 事件，返回输入值。输入完成后自动恢复为新增按钮状态。

### 示例 8：自定义新增按钮样式

通过 `add` 插槽自定义新增标签按钮的显示内容。

```vue
<template>
  <view>
    <wd-tag
      v-for="(tag, index) in tags"
      :key="index"
      round
      closable
      @close="handleClose(index)"
    >
      {{ tag }}
    </wd-tag>

    <wd-tag round dynamic @confirm="handleConfirm">
      <template #add>
        <wd-icon name="add" size="16px" />
        <text style="margin-left: 4px">添加标签</text>
      </template>
    </wd-tag>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const tags = ref(['前端', '后端', '全栈'])

function handleClose(index: number) {
  tags.value = tags.value.filter((_, i) => i !== index)
}

function handleConfirm({ value }: { value: string }) {
  if (!value) return
  tags.value = [...tags.value, value]
}
</script>
```

使用 `add` 插槽可以完全自定义新增按钮的显示内容，例如使用不同的图标、文字或布局。插槽内容会替换默认的新增图标和"添加"文字。

## 注意事项

1. **closable 仅对圆角标签生效**：`closable` 属性需要配合 `round` 属性使用，非圆角标签设置 `closable` 不会显示关闭图标。

2. **dynamic 模式交互**：动态新增标签点击后会切换为输入框状态，输入框失去焦点或按下回车时会触发 `confirm` 事件并恢复为按钮状态。空值输入不会触发事件。

3. **颜色优先级**：自定义 `color` 和 `bg-color` 的优先级高于 `type` 属性。设置自定义颜色后，标签类型对应的主题色将不再生效。

4. **图标互斥**：`icon` 属性和 `useIconSlot` 插槽是互斥的。当 `useIconSlot` 为 `true` 时，优先使用插槽中的内容；当仅设置 `icon` 属性时，使用内置的 `wd-icon` 组件渲染图标。

5. **bgColor 样式逻辑**：在非幽灵模式下，`bgColor` 作用于标签背景色；在幽灵模式下，`bgColor` 作用于标签边框色。当 `plain` 为 `true` 且设置了 `bgColor` 时，标签背景保持透明。

6. **行内块渲染**：标签以 `inline-block` 方式渲染，多个标签之间会自动产生间距。如需控制间距，建议通过外部容器或自定义类名设置 margin。

7. **样式定制**：推荐使用 `custom-class` 和 `custom-style` 属性进行样式扩展。避免直接覆盖组件内部类名，以保证样式的可维护性和升级兼容性。

8. **mark 与 round 互斥**：`mark` 和 `round` 属性不建议同时使用，两者会产生样式冲突。标记标签使用左圆右方的特殊形状，圆角标签使用全圆角胶囊形状。
