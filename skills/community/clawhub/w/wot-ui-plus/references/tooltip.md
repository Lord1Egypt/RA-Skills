# Tooltip 文字提示



## 组件概况

Tooltip 文字提示组件是一个轻量级的弹出提示组件，用于在用户交互时展示简短的说明文字。它通过点击触发目标元素，在目标元素的指定位置弹出半透明的提示气泡，支持 12 种放置位置和箭头指示，帮助用户理解界面元素的功能或含义。

该组件基于 `wd-transition` 实现淡入淡出的过渡动画效果，使用 `usePopover` 组合式函数进行精确的定位计算。组件采用半透明背景配合毛玻璃模糊效果（`backdrop-filter: blur(10px)`），确保在各类背景上都能清晰展示提示内容。

## 核心功能描述

- **12 种放置位置**：支持 `top` / `top-start` / `top-end` / `bottom` / `bottom-start` / `bottom-end` / `left` / `left-start` / `left-end` / `right` / `right-start` / `right-end`，满足各种布局需求
- **箭头指示**：默认显示方向箭头（`visible-arrow: true`），箭头方向自动跟随放置位置调整
- **内容自定义**：通过 `content` 属性传入纯文本，或使用 `content` 插槽自定义任意内容（包括多行文本、图片等）
- **偏移量控制**：通过 `offset` 属性调整弹出位置的偏移，支持数字、数组 `[x, y]` 或对象 `{ x, y }` 格式
- **关闭按钮**：通过 `show-close` 属性启用内置关闭按钮，点击即可关闭提示
- **状态控制**：通过 `v-model` 双向绑定控制显示状态，也可通过 `ref` 调用 `open()` / `close()` 方法
- **禁用状态**：通过 `disabled` 属性禁用交互，点击不会触发显示
- **自动互斥**：同时存在多个 Tooltip 实例时，打开一个会自动关闭其他实例
- **毛玻璃效果**：弹出层采用 `backdrop-filter: blur(10px)` 背景模糊效果，提升视觉层次感
- **过渡动画**：使用 `wd-transition` 组件实现 200ms 的 `fade` 淡入淡出动画

## 适用业务场景

- **功能说明**：为图标、按钮等界面元素提供简短的功能说明
- **操作引导**：在用户首次使用时展示操作提示和说明
- **信息补充**：对表单字段、数据指标等提供补充解释
- **状态提示**：展示当前状态的含义或下一步操作建议
- **多语言提示**：结合国际化方案展示多语言的帮助文案

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| modelValue / v-model | boolean | false | 否 | Tooltip 的显示状态，支持双向绑定 |
| content | string / Array | - | 否 | 显示的内容。支持字符串类型，也可通过 `slot#content` 传入自定义内容 |
| placement | string | 'bottom' | 否 | Tooltip 的出现位置，可选值：`top` / `top-start` / `top-end` / `bottom` / `bottom-start` / `bottom-end` / `left` / `left-start` / `left-end` / `right` / `right-start` / `right-end` |
| visibleArrow | boolean | true | 否 | 是否显示 Tooltip 箭头 |
| offset | number / Array / Object | 0 | 否 | 出现位置的偏移量。支持数字、数组 `[x, y]` 或对象 `{ x, y }` 格式 |
| useContentSlot | boolean | false | 否 | 是否使用 `content` 插槽传入自定义内容。设置为 `true` 时将忽略 `content` 属性 |
| showClose | boolean | false | 否 | 是否显示 Tooltip 内部的关闭按钮 |
| disabled | boolean | false | 否 | Tooltip 是否可用，禁用后点击不会触发显示 |
| customArrow | string | '' | 否 | 自定义箭头的样式类名 |
| customStyle | string | '' | 否 | 自定义组件根元素的内联样式 |
| customClass | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| change | `{ show: boolean }` | Tooltip 显示状态改变时触发，`show` 为当前显示状态 |
| open | - | Tooltip 打开（显示）时触发 |
| close | - | Tooltip 关闭（隐藏）时触发 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 默认插槽，用于放置触发 Tooltip 显示的目标元素（如按钮、图标、文本等） |
| content | - | 内容插槽，当 `use-content-slot` 为 `true` 时使用，可自定义弹出内容的任意样式和结构 |

### Methods

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| open | - | void | 打开 Tooltip |
| close | - | void | 关闭 Tooltip |

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-tooltip | Tooltip 根节点样式类 |
| wd-tooltip\_\_pos | 弹出层定位容器样式类 |
| wd-tooltip\_\_container | 弹出层内容容器样式类 |
| wd-tooltip\_\_inner | 弹出层文本内容区域样式类 |
| wd-tooltip\_\_arrow | 箭头元素样式类 |
| wd-tooltip\_\_close-icon | 关闭按钮图标样式类 |
| wd-tooltip\_\_target | 触发目标元素容器样式类 |

### CSS 变量

组件支持通过 CSS 变量进行主题定制：

| CSS 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --wot-tooltip-bg | rgba(38, 39, 40, 0.8) | 弹出层背景色 |
| --wot-tooltip-color | #ffffff | 弹出层文字颜色 |
| --wot-tooltip-radius | 8px | 弹出层圆角大小 |
| --wot-tooltip-arrow-size | 5px | 箭头大小 |
| --wot-tooltip-fs | 14px | 弹出层字号大小 |
| --wot-tooltip-blur | 10px | 背景高斯模糊效果 |
| --wot-tooltip-padding | 9px 20px | 弹出层内边距 |
| --wot-tooltip-close-size | 6px | 关闭按钮大小 |
| --wot-tooltip-z-index | 500 | 弹出层层级 |
| --wot-tooltip-line-height | 18px | 弹出层行高 |

## 使用示例

### 示例 1：基本用法 - 不同放置位置

效果说明：展示 Tooltip 组件在不同放置位置的效果。通过 `placement` 属性设置弹出位置，支持顶部、底部、左侧、右侧及其变体（start/end）。点击按钮即可切换 Tooltip 的显示与隐藏。

```vue
<template>
  <!-- 底部方向 -->
  <view class="top">
    <wd-tooltip placement="bottom-start" content="bottom-start 提示文字">
      <wd-button :round="false">底部开始</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="bottom" content="bottom 提示文字">
      <wd-button :round="false">底部</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="bottom-end" content="bottom-end 提示文字">
      <wd-button :round="false">底部结束</wd-button>
    </wd-tooltip>
  </view>

  <!-- 右侧方向 -->
  <view class="left">
    <wd-tooltip placement="right-start" content="right-start 提示文字">
      <wd-button :round="false">右侧开始</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="right" content="right 提示文字" customStyle="margin: 20px 0">
      <wd-button :round="false">右侧</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="right-end" content="right-end 提示文字">
      <wd-button :round="false">右侧结束</wd-button>
    </wd-tooltip>
  </view>

  <!-- 左侧方向 -->
  <view class="right">
    <wd-tooltip placement="left-start" content="left-start 提示文字">
      <wd-button :round="false">
        左侧开始
        <wd-icon name="setting" />
      </wd-button>
    </wd-tooltip>
    <wd-tooltip placement="left" content="left 提示文字" customStyle="margin: 20px 0">
      <wd-button :round="false">左侧</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="left-end" content="left-end 提示文字">
      <wd-button :round="false">左侧结束</wd-button>
    </wd-tooltip>
  </view>

  <!-- 顶部方向 -->
  <view class="bottom">
    <wd-tooltip placement="top-start" content="top-start 提示文字">
      <wd-button :round="false">顶部开始</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="top" content="top 提示文字">
      <wd-button :round="false">顶部</wd-button>
    </wd-tooltip>
    <wd-tooltip placement="top-end" content="top-end 提示文字">
      <wd-button :round="false">顶部结束</wd-button>
    </wd-tooltip>
  </view>
</template>

<script setup lang="ts">
// Tooltip 组件会在点击按钮时自动切换显示状态，无需额外绑定 v-model
</script>
```

### 示例 2：多行文本 - 使用内容插槽

效果说明：当需要展示多行文本或自定义内容时，设置 `use-content-slot` 属性为 `true`，并在 `content` 插槽中自定义弹出内容样式。

```vue
<template>
  <wd-tooltip placement="right" use-content-slot>
    <wd-button :round="false">多行文本</wd-button>
    <template #content>
      <view class="lines-content">
        <view>多行文本1</view>
        <view>多行文本2</view>
        <view>多行文本3</view>
      </view>
    </template>
  </wd-tooltip>
</template>

<style scoped lang="scss">
.lines-content {
  color: #fff;
  padding: 5px;
  width: 90px;
}
</style>
```

### 示例 3：显示关闭按钮

效果说明：通过 `show-close` 属性启用内置关闭按钮，用户可点击弹出层右上角的关闭按钮来关闭 Tooltip。

```vue
<template>
  <wd-tooltip content="显示关闭按钮" placement="right" show-close>
    <wd-button :round="false">显示关闭按钮</wd-button>
  </wd-tooltip>
</template>
```

### 示例 4：控制显隐

效果说明：通过 `v-model` 绑定变量控制 Tooltip 的显示与隐藏。也可以使用组件实例的 `open()` / `close()` 方法进行程序化控制。

```vue
<template>
  <view>
    <wd-button plain size="small" @click="control">
      {{ show ? '关闭' : '打开' }}
    </wd-button>
  </view>

  <wd-tooltip placement="top" content="控制显隐" v-model="show">
    <wd-button :round="false">top</wd-button>
  </wd-tooltip>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)

function control() {
  show.value = !show.value
}
</script>
```

### 示例 5：绑定事件

效果说明：通过监听 `change`、`open`、`close` 事件，在 Tooltip 显示状态变化时执行自定义逻辑。

```vue
<template>
  <wd-tooltip
    placement="right-end"
    :content="content"
    @open="onShow"
    @close="onHide"
    @change="handleChange"
  >
    <wd-button :round="false">事件</wd-button>
  </wd-tooltip>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()
const content = ref<string>('显示内容')

function onShow() {
  console.log('Tooltip 已显示')
}

function onHide() {
  toast.show('文字提示已关闭')
}

function handleChange(event: any) {
  console.log('状态改变:', event) // event.detail.show 为当前显示状态
}
</script>
```

### 示例 6：禁用状态

效果说明：通过 `disabled` 属性禁用 Tooltip，点击触发元素不会弹出提示。

```vue
<template>
  <wd-tooltip placement="right-end" content="禁用" disabled>
    <wd-button :round="false">禁用</wd-button>
  </wd-tooltip>
</template>
```

### 示例 7：隐藏箭头

效果说明：通过 `visible-arrow` 属性设置为 `false`，隐藏弹出层的方向箭头，使弹出层呈现简洁的矩形气泡样式。

```vue
<template>
  <wd-tooltip placement="bottom" content="不显示箭头" :visible-arrow="false">
    <wd-button :round="false">隐藏箭头</wd-button>
  </wd-tooltip>
</template>
```

### 示例 8：自定义偏移量

效果说明：通过 `offset` 属性调整弹出层相对于默认位置的偏移。支持三种格式：数字（X/Y 轴统一偏移）、数组 `[x, y]`（分别设置 X/Y 轴偏移）、对象 `{ x, y }`（分别设置 X/Y 轴偏移）。

```vue
<template>
  <!-- 数字偏移 -->
  <wd-tooltip placement="bottom" content="偏移 10px" :offset="10">
    <wd-button :round="false">数字偏移</wd-button>
  </wd-tooltip>

  <!-- 数组偏移 [x, y] -->
  <wd-tooltip placement="bottom" content="X 偏移 20, Y 偏移 30" :offset="[20, 30]">
    <wd-button :round="false">数组偏移</wd-button>
  </wd-tooltip>

  <!-- 对象偏移 { x, y } -->
  <wd-tooltip placement="bottom" content="X 偏移 -10, Y 偏移 15" :offset="{ x: -10, y: 15 }">
    <wd-button :round="false">对象偏移</wd-button>
  </wd-tooltip>
</template>
```

## 注意事项

1. **content 必填**：`content` 属性不能为 `null` 或 `undefined`，否则控制台会输出警告信息。如果使用插槽模式（`use-content-slot: true`），可以不设置 `content` 属性。

2. **插槽内容样式**：使用 `content` 插槽自定义内容时，需要自行设置弹出内容的样式（如文字颜色、背景色、内边距等）。建议确保弹出内容的 `position: relative` 和 `z-index` 正确设置，以免被其他元素遮挡。

3. **placement 动态变化**：当 `placement` 属性值发生变化时，组件会自动重新初始化定位逻辑，更新箭头方向和弹出层位置。

4. **自动互斥机制**：Tooltip 组件内置了自动互斥逻辑。当页面中存在多个 Tooltip 实例时，打开一个新的 Tooltip 会自动关闭其他已打开的 Tooltip，确保同一时间只有一个 Tooltip 处于显示状态。

5. **点击外部关闭**：Tooltip 组件已集成点击外部区域自动关闭的功能，无需额外配置。

6. **偏移量处理逻辑**：`offset` 属性支持数字、数组 `[x, y]` 和对象 `{ x, y }` 三种格式。组件内部会根据放置位置和弹出层/目标元素的尺寸进行智能边界保护计算，确保弹出层不会超出可视区域。

7. **状态同步**：使用 `v-model` 双向绑定可以保持父组件状态与组件内部状态一致。如果仅需要单向控制，可以使用 `open()` / `close()` 方法而不绑定 `v-model`。

8. **禁用状态行为**：当 `disabled` 属性设置为 `true` 时，点击触发元素不会切换显示状态，即使通过 `v-model` 绑定的状态为 `true`，点击也不会关闭。但通过 `open()` / `close()` 方法仍可程序化控制显示。

9. **过渡动画**：Tooltip 使用 `wd-transition` 组件的 `fade` 过渡效果，动画时长为 200ms。在动画进行中，用户仍然可以与页面其他元素交互。

10. **深色模式适配**：组件自动适配深色模式主题。在深色模式下，弹出层背景色为 `rgb(38, 39, 40)`，文字颜色为白色。

11. **自定义箭头样式**：通过 `custom-arrow` 属性可以为箭头元素添加额外的 CSS 类名，实现箭头样式的自定义。

12. **z-index 层级**：Tooltip 弹出层默认 `z-index` 为 500。在规划页面层级时，请确保该值高于需要覆盖的页面内容，低于需要覆盖 Tooltip 的组件。
