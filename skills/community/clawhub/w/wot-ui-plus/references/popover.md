# Popover 气泡卡片


## 组件概况

Popover 气泡卡片组件是一个功能丰富的弹出式卡片组件，用于在用户交互时展示更复杂的内容信息。与 Tooltip 相比，Popover 支持两种展示模式：普通模式（显示纯文本）和菜单模式（显示可点击的菜单列表），并具备完整的点击事件处理能力。

该组件与 Tooltip 共用 `usePopover` 组合式函数实现定位逻辑，支持 12 种放置位置和箭头指示。在普通模式下，Popover 弹出层采用白色背景配合投影效果，呈现类似卡片的视觉风格；在菜单模式下，弹出层以列表形式展示多个可操作项，支持图标和文字组合展示。

## 核心功能描述

- **双模式展示**：支持 `normal`（普通文本模式）和 `menu`（菜单列表模式），通过 `mode` 属性切换
- **12 种放置位置**：支持 `top` / `top-start` / `top-end` / `bottom` / `bottom-start` / `bottom-end` / `left` / `left-start` / `left-end` / `right` / `right-start` / `right-end`
- **菜单模式**：在 `menu` 模式下，`content` 接收数组类型数据，每项支持 `iconClass`（图标类名）和 `content`（显示文本）字段，点击菜单项触发 `menuclick` 事件
- **箭头指示**：默认显示方向箭头（`visible-arrow: true`），箭头方向自动跟随放置位置调整
- **内容自定义**：通过 `content` 属性传入内容，或使用 `content` 插槽自定义任意内容
- **偏移量控制**：通过 `offset` 属性调整弹出位置的偏移（支持数字类型）
- **关闭按钮**：通过 `show-close` 属性启用内置关闭按钮
- **状态控制**：通过 `v-model` 双向绑定控制显示状态，也可通过 `ref` 调用 `open()` / `close()` 方法
- **禁用状态**：通过 `disabled` 属性禁用交互
- **自动互斥**：同时存在多个 Popover 实例时，打开一个会自动关闭其他实例
- **投影效果**：弹出层采用 `box-shadow: 0px 2px 10px 0px rgba(0, 0, 0, 0.1)` 投影效果，提升视觉层次感
- **过渡动画**：使用 `wd-transition` 组件实现 200ms 的 `fade` 淡入淡出动画

## 适用业务场景

- **操作菜单**：为按钮或图标提供快捷操作菜单（如复制、分享、删除等）
- **信息展示**：在悬停或点击时展示补充说明信息
- **功能入口**：以列表形式提供多个功能入口选项
- **状态切换**：提供多个可选项供用户快速切换
- **消息通知**：展示消息列表或操作建议

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| modelValue / v-model | boolean | false | 否 | Popover 的显示状态，支持双向绑定 |
| content | string / Array | - | 否 | 显示的内容。普通模式下为字符串，菜单模式下为数组（每项包含 `iconClass` 和 `content` 字段）。也可通过 `slot#content` 传入自定义内容 |
| mode | string | 'normal' | 否 | 当前显示模式，可选值：`normal`（普通模式）/ `menu`（菜单模式） |
| placement | string | 'bottom' | 否 | Popover 的放置位置，可选值：`top` / `top-start` / `top-end` / `bottom` / `bottom-start` / `bottom-end` / `left` / `left-start` / `left-end` / `right` / `right-start` / `right-end` |
| visibleArrow | boolean | true | 否 | 是否显示 Popover 箭头 |
| offset | number | 0 | 否 | 出现位置的偏移量，单位为 px |
| useContentSlot | boolean | false | 否 | 是否使用 `content` 插槽传入自定义内容。设置为 `true` 时将忽略 `content` 属性 |
| showClose | boolean | false | 否 | 是否显示 Popover 内部的关闭按钮 |
| disabled | boolean | false | 否 | Popover 是否可用，禁用后点击不会触发显示 |
| customArrow | string | '' | 否 | 自定义箭头的样式类名 |
| customPop | string | '' | 否 | 自定义弹出层容器的样式类名 |
| customStyle | string | '' | 否 | 自定义组件根元素的内联样式 |
| customClass | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| change | `{ show: boolean }` | Popover 显示状态改变时触发，`show` 为当前显示状态 |
| open | - | Popover 打开（显示）时触发 |
| close | - | Popover 关闭（隐藏）时触发 |
| menuclick | `{ item: Record<string, any>, index: number }` | 菜单模式下点击菜单项时触发，返回被点击项的数据和索引 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 默认插槽，用于放置触发 Popover 显示的目标元素（如按钮、图标、文本等） |
| content | - | 内容插槽，当 `use-content-slot` 为 `true` 时使用，可自定义弹出内容的任意样式和结构 |

### Methods

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| open | - | void | 打开 Popover |
| close | - | void | 关闭 Popover |

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-popover | Popover 根节点样式类 |
| wd-popover\_\_pos | 弹出层定位容器样式类 |
| wd-popover\_\_container | 弹出层内容容器样式类 |
| wd-popover\_\_inner | 弹出层文本内容区域样式类（普通模式） |
| wd-popover\_\_menu | 弹出层菜单容器样式类（菜单模式） |
| wd-popover\_\_menu-inner | 弹出层单个菜单项样式类 |
| wd-popover\_\_icon | 菜单项图标样式类 |
| wd-popover\_\_arrow | 箭头元素样式类 |
| wd-popover\_\_close-icon | 关闭按钮图标样式类 |
| wd-popover\_\_target | 触发目标元素容器样式类 |

### CSS 变量

组件支持通过 CSS 变量进行主题定制：

| CSS 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --wot-popover-bg | #ffffff | 弹出层背景色 |
| --wot-popover-color | rgba(0, 0, 0, 0.85) | 弹出层文字颜色 |
| --wot-popover-box-shadow | 0px 2px 10px 0px rgba(0, 0, 0, 0.1) | 弹出层投影效果 |
| --wot-popover-arrow-box-shadow | 0px 2px 10px 0px rgba(0, 0, 0, 0.2) | 箭头投影效果 |
| --wot-popover-border-color | rgba(0, 0, 0, 0.09) | 菜单项边框颜色 |
| --wot-popover-radius | 4px | 弹出层圆角大小 |
| --wot-popover-arrow-size | 6px | 箭头大小 |
| --wot-popover-fs | 14px | 弹出层字号大小 |
| --wot-popover-padding | 15px | 弹出层内边距 |
| --wot-popover-line-height | 18px | 弹出层行高 |
| --wot-popover-z-index | 500 | 弹出层层级 |

## 使用示例

### 示例 1：基本用法 - 普通文本模式

效果说明：展示 Popover 组件的基本使用方式，通过 `v-model` 控制弹出层的显示与隐藏，`content` 属性传入纯文本内容。点击按钮即可弹出气泡卡片。

```vue
<template>
  <view class="center">
    <wd-popover
      v-model="show"
      content="这是一段内容。"
      placement="bottom"
    >
      <wd-button>点击展示</wd-button>
    </wd-popover>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
</script>

<style scoped lang="scss">
.center {
  text-align: center;
}
</style>
```

### 示例 2：动态切换放置位置

效果说明：通过 `radio-group` 组件动态选择 Popover 的放置位置，实时预览不同方向的效果。

```vue
<template>
  <view class="wrapper">
    <!-- 位置选择器 -->
    <wd-radio-group v-model="placement" inline shape="dot">
      <wd-radio value="bottom" custom-class="custom-radio">bottom</wd-radio>
      <wd-radio value="bottom-start" custom-class="custom-radio">bottom-start</wd-radio>
      <wd-radio value="bottom-end" custom-class="custom-radio">bottom-end</wd-radio>
      <wd-radio value="top" custom-class="custom-radio">top</wd-radio>
      <wd-radio value="top-start" custom-class="custom-radio">top-start</wd-radio>
      <wd-radio value="top-end" custom-class="custom-radio">top-end</wd-radio>
      <wd-radio value="left" custom-class="custom-radio">left</wd-radio>
      <wd-radio value="left-start" custom-class="custom-radio">left-start</wd-radio>
      <wd-radio value="left-end" custom-class="custom-radio">left-end</wd-radio>
      <wd-radio value="right" custom-class="custom-radio">right</wd-radio>
      <wd-radio value="right-start" custom-class="custom-radio">right-start</wd-radio>
      <wd-radio value="right-end" custom-class="custom-radio">right-end</wd-radio>
    </wd-radio-group>

    <!-- Popover 组件 -->
    <view class="center">
      <wd-popover
        v-model="show"
        content="这是一段内容。"
        :placement="placement"
      >
        <wd-button>点击展示</wd-button>
      </wd-popover>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { PlacementType } from '@/uni_modules/wot-ui-plus/components/wd-popover/types'

const show = ref<boolean>(false)
const placement = ref<PlacementType>('bottom')
</script>

<style scoped lang="scss">
.center {
  text-align: center;
  padding-bottom: 20px;
}
.wrapper {
  width: 100%;
  height: 100vh;
}
</style>
```

### 示例 3：嵌套自定义内容

效果说明：通过设置 `use-content-slot` 为 `true`，在 `content` 插槽中自定义弹出内容的样式和结构，实现个性化的气泡卡片效果。

```vue
<template>
  <view class="center">
    <wd-popover v-model="show" use-content-slot placement="bottom">
      <template #content>
        <view class="pop-content">这是一段自定义样式的内容。</view>
      </template>
      <wd-button>点击展示</wd-button>
    </wd-popover>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
</script>

<style scoped lang="scss">
.center {
  text-align: center;
}
.pop-content {
  /* 必填 开始 */
  position: relative;
  z-index: 500;
  border-radius: 4px;
  /* 必填 结束 */
  background: #fff;
  color: #8268de;
  font-weight: bolder;
  padding: 10px;
  width: 150px;
}
</style>
```

### 示例 4：菜单列表模式

效果说明：将 `mode` 属性设置为 `menu`，`content` 属性传入菜单数组，每个菜单项可包含 `iconClass`（图标类名）和 `content`（显示文本）。点击菜单项会触发 `menuclick` 事件并自动关闭弹出层。

```vue
<template>
  <view class="center">
    <wd-popover
      v-model="show"
      mode="menu"
      placement="bottom"
      :content="menu"
      @menuclick="handleMenuClick"
    >
      <wd-button>菜单列表</wd-button>
    </wd-popover>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '@/uni_modules/wot-ui-plus'

const show = ref<boolean>(false)
const toast = useToast()

const menu = ref<Array<Record<string, any>>>([
  {
    iconClass: 'read',
    content: '全部标记已读'
  },
  {
    iconClass: 'delete',
    content: '清空最近会话'
  },
  {
    iconClass: 'detection',
    content: '消息订阅设置'
  },
  {
    iconClass: 'subscribe',
    content: '消息异常检测'
  }
])

function handleMenuClick(e: any) {
  toast.show('选择了' + e.item.content)
}
</script>

<style scoped lang="scss">
.center {
  text-align: center;
}
</style>
```

### 示例 5：绑定事件

效果说明：通过监听 `change`、`open`、`close` 事件，在 Popover 显示状态变化时执行自定义逻辑。

```vue
<template>
  <wd-popover
    v-model="show"
    content="事件监听示例"
    placement="bottom"
    @open="handleOpen"
    @close="handleClose"
    @change="handleChange"
  >
    <wd-button>事件监听</wd-button>
  </wd-popover>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)

function handleOpen() {
  console.log('Popover 已显示')
}

function handleClose() {
  console.log('Popover 已关闭')
}

function handleChange(event: { show: boolean }) {
  console.log('状态改变:', event.show)
}
</script>
```

### 示例 6：显示关闭按钮

效果说明：通过 `show-close` 属性启用内置关闭按钮，用户可以点击弹出层右上角的关闭图标来关闭 Popover。

```vue
<template>
  <wd-popover content="显示关闭按钮" placement="right" show-close>
    <wd-button>显示关闭按钮</wd-button>
  </wd-popover>
</template>
```

### 示例 7：禁用状态

效果说明：通过 `disabled` 属性禁用 Popover，点击触发元素不会弹出气泡卡片。

```vue
<template>
  <wd-popover content="禁用状态" placement="right" disabled>
    <wd-button>禁用</wd-button>
  </wd-popover>
</template>
```

### 示例 8：隐藏箭头

效果说明：通过 `visible-arrow` 属性设置为 `false`，隐藏弹出层的方向箭头，使弹出层呈现简洁的矩形卡片样式。

```vue
<template>
  <wd-popover content="不显示箭头" placement="bottom" :visible-arrow="false">
    <wd-button>隐藏箭头</wd-button>
  </wd-popover>
</template>
```

## 注意事项

1. **内容类型校验**：在普通模式（`mode: 'normal'`）下，`content` 属性应为字符串类型。在菜单模式（`mode: 'menu'`）下，`content` 属性应为数组类型。如果类型不匹配，控制台会输出错误提示。

2. **菜单项数据结构**：在菜单模式下，`content` 数组中的每个元素应为对象，支持以下字段：
   - `iconClass`：图标类名，对应 `wd-icon` 组件的 `name` 属性
   - `content`：菜单项显示的文本内容
   
   示例：`[{ iconClass: 'edit', content: '编辑' }, { iconClass: 'delete', content: '删除' }]`

3. **插槽内容样式**：使用 `content` 插槽自定义内容时，必须为插槽内容设置 `position: relative` 和 `z-index` 属性（建议 `z-index: 500`），以确保内容在弹出层中正确显示且不被遮挡。同时建议设置 `border-radius` 保持圆角一致性。

4. **自动互斥机制**：Popover 组件内置了自动互斥逻辑。当页面中存在多个 Popover 实例时，打开一个新的 Popover 会自动关闭其他已打开的 Popover，确保同一时间只有一个 Popover 处于显示状态。

5. **点击外部关闭**：Popover 组件已集成点击外部区域自动关闭的功能，无需额外配置。

6. **菜单点击行为**：在菜单模式下，点击任意菜单项会自动关闭 Popover 弹出层，并触发 `menuclick` 事件。事件回调参数包含 `item`（被点击项的数据）和 `index`（被点击项的索引）。

7. **状态同步**：使用 `v-model` 双向绑定可以保持父组件状态与组件内部状态一致。如果仅需要单向控制，可以使用 `open()` / `close()` 方法而不绑定 `v-model`。

8. **禁用状态行为**：当 `disabled` 属性设置为 `true` 时，点击触发元素不会切换显示状态。但通过 `open()` / `close()` 方法仍可程序化控制显示。

9. **过渡动画**：Popover 使用 `wd-transition` 组件的 `fade` 过渡效果，动画时长为 200ms。在动画进行中，用户仍然可以与页面其他元素交互。

10. **深色模式适配**：组件自动适配深色模式主题。在深色模式下，弹出层背景色为 `rgb(75, 76, 77)`，文字颜色为深色模式主色，边框颜色为 `rgba(255, 255, 255, 0.1)`。

11. **布局溢出处理**：Popover 弹出层使用绝对定位，可能在某些布局中被父容器裁剪。如果弹出层显示不完整，请确保父容器设置了 `overflow: visible` 或使用 `:deep()` 覆盖默认 `overflow` 属性。

12. **z-index 层级**：Popover 弹出层默认 `z-index` 为 500。在规划页面层级时，请确保该值高于需要覆盖的页面内容，低于需要覆盖 Popover 的组件。

13. **投影效果**：普通模式下，弹出层和箭头均带有投影效果（`box-shadow: 0px 2px 10px 0px rgba(0, 0, 0, 0.1)`），增强卡片的立体感。菜单模式下，投影效果同样适用。
