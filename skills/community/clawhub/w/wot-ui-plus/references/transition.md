# Transition 过渡动画


## 组件概况

Transition 过渡动画组件是一个用于控制内容显示/隐藏时动画效果的轻量级容器组件。该组件参考 Vue 的 `<transition>` 设计理念，通过 `name` 属性选择预设的动画类型（如淡入淡出、滑入滑出、缩放等），或通过自定义 CSS 类实现个性化过渡效果。组件内置完整的动画生命周期钩子（`before-enter`、`enter`、`after-enter`、`before-leave`、`leave`、`after-leave`），并提供 `destroy` 属性控制动画结束后是否隐藏子节点，适用于弹窗、提示、下拉菜单等需要过渡动效的交互场景。

## 核心功能描述

- **预设动画类型**：内置 12 种常用过渡动画效果，涵盖 Fade（淡入淡出）、Slide（滑动）、Zoom（缩放）三大类，满足绝大多数业务场景需求
- **动画生命周期**：提供完整的进入/离开动画生命周期钩子，支持在动画的关键阶段执行自定义逻辑
- **独立时长控制**：支持通过 `duration` 属性分别设置进入（enter）和离开（leave）的动画时长，单位为毫秒
- **自定义动画类名**：通过 `enter-class`、`leave-class` 等 6 个类名属性完全自定义 CSS 过渡效果，实现任意复杂动画
- **懒渲染优化**：通过 `lazy-render` 属性控制是否在触发展示时才渲染内容，提升包含大量子节点时的初始渲染性能
- **触摸滚动阻断**：通过 `disable-touch-move` 属性阻止组件区域内的触摸滚动事件，适用于弹窗类场景
- **动画结束后销毁**：`destroy` 属性控制隐藏后是否将内容设置为 `display: none`，平衡性能与可访问性
- **组合动画支持**：`name` 属性支持传入数组，可叠加多种动画效果

## 适用业务场景

- **弹窗显示/隐藏**：为 Dialog、Popup 等弹窗组件添加平滑的淡入或滑入动画
- **下拉刷新/加载**：在列表顶部下拉刷新或底部加载更多时添加过渡效果
- **卡片展开/收起**：实现详情卡片、折叠面板的平滑展开和收起动画
- **提示框/Toast**：为 Toast、NoticeBar 等提示类组件添加淡入淡出效果
- **路由切换动画**：配合页面路由切换实现页面间的过渡动效
- **图片/视频预览**：在图片放大预览时添加缩放过渡效果
- **自定义动画序列**：通过自定义 CSS 类实现品牌特色的专属动效

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| show | boolean | false | 否 | 是否展示组件内容，通过 v-model 或 :show 双向控制显示/隐藏状态 |
| name | string / string[] | 'fade' | 否 | 动画类型，可选值见下方「动画类型」表格，支持传入数组组合多种动画 |
| duration | number / object / boolean | 300 | 否 | 动画时长（毫秒），支持传入数字统一设置、对象分别设置（{ enter: 300, leave: 400 }）、布尔值 |
| destroy | boolean | true | 否 | 是否在动画结束时销毁子节点（设置为 display: none），false 时子节点保持渲染但不可见 |
| lazy-render | boolean | false | 否 | 是否开启懒渲染，开启后触发展示时才渲染插槽内容，适用于渲染开销大的场景 |
| disable-touch-move | boolean | false | 否 | 是否阻止组件区域内的 touchmove 事件，用于防止弹窗内滚动穿透 |
| enter-class | string | '' | 否 | 自定义进入过渡的开始状态 CSS 类名 |
| enter-active-class | string | '' | 否 | 自定义进入过渡的激活状态 CSS 类名 |
| enter-to-class | string | '' | 否 | 自定义进入过渡的结束状态 CSS 类名 |
| leave-class | string | '' | 否 | 自定义离开过渡的开始状态 CSS 类名 |
| leave-active-class | string | '' | 否 | 自定义离开过渡的激活状态 CSS 类名 |
| leave-to-class | string | '' | 否 | 自定义离开过渡的结束状态 CSS 类名 |
| custom-style | string | '' | 否 | 自定义组件根元素的内联样式 |
| custom-class | string | '' | 否 | 自定义组件根元素的样式类名 |

### 动画类型

| 类型值 | 动画效果说明 | 视觉表现 |
| --- | --- | --- |
| fade | 淡入淡出 | 透明度从 0 到 1 渐变 |
| fade-up | 从下方淡入 | 从底部向上滑入同时透明度渐变 |
| fade-down | 从上方淡入 | 从顶部向下滑入同时透明度渐变 |
| fade-left | 从左侧淡入 | 从左侧向右滑入同时透明度渐变 |
| fade-right | 从右侧淡入 | 从右侧向左滑入同时透明度渐变 |
| slide-up | 从下方滑入 | 从底部向上滑入（不改变透明度） |
| slide-down | 从上方滑入 | 从顶部向下滑入（不改变透明度） |
| slide-left | 从左侧滑入 | 从左侧向右滑入（不改变透明度） |
| slide-right | 从右侧滑入 | 从右侧向左滑入（不改变透明度） |
| zoom-in | 缩小淡入 | 从 scale(0.8) 放大到 1 同时淡入 |
| zoom-out | 放大淡入 | 从 scale(1.2) 缩小到 1 同时淡入 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| click | - | 点击组件时触发 |
| before-enter | - | 进入过渡动画开始前触发 |
| enter | - | 进入过渡动画开始时触发（DOM 已插入） |
| after-enter | - | 进入过渡动画完成后触发 |
| before-leave | - | 离开过渡动画开始前触发 |
| leave | - | 离开过渡动画开始时触发 |
| after-leave | - | 离开过渡动画完成后触发（DOM 已隐藏） |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于包裹需要进行过渡动画的内容 |

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-transition | 过渡动画根节点样式类，可用于全局样式覆盖 |

## 使用示例

### 示例 1：基础淡入淡出动画

效果说明：展示 Transition 组件最基础的淡入淡出效果，点击按钮后蓝色方块从透明变为可见，再次点击后渐隐消失。使用默认的 `fade` 动画类型和 300ms 动画时长。

```vue
<template>
  <wd-button type="primary" @click="toggle">切换显示</wd-button>

  <wd-transition :show="show" name="fade" custom-class="demo-block" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)

function toggle() {
  show.value = !show.value
}
</script>

<style scoped lang="scss">
.demo-block {
  position: fixed;
  left: 50%;
  top: 50%;
  margin: -50px 0 0 -50px;
  width: 100px;
  height: 100px;
  background: #0083ff;
  border-radius: 8px;
}
</style>
```

### 示例 2：多种预设动画演示

效果说明：通过切换不同的 `name` 值展示多种内置动画效果。涵盖 Fade 系列（淡入淡出）、Slide 系列（滑动）和 Zoom 系列（缩放）。每种动画可通过 `duration` 属性自定义时长。

```vue
<template>
  <view class="button-group">
    <wd-button @click="playAnimation('fade')">Fade 淡入淡出</wd-button>
    <wd-button @click="playAnimation('fade-up')">向上淡入</wd-button>
    <wd-button @click="playAnimation('slide-up')">向上滑入</wd-button>
    <wd-button @click="playAnimation('zoom-in')">缩小淡入</wd-button>
  </view>

  <wd-transition :show="show" :name="animationName" :duration="500" custom-class="demo-block" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const animationName = ref<string>('fade')

function playAnimation(name: string) {
  animationName.value = name
  show.value = true
  // 动画展示 1.5 秒后自动隐藏
  setTimeout(() => {
    show.value = false
  }, 1500)
}
</script>

<style scoped lang="scss">
.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.demo-block {
  position: fixed;
  left: 50%;
  top: 50%;
  margin: -50px 0 0 -50px;
  width: 100px;
  height: 100px;
  background: #0083ff;
  border-radius: 8px;
}
</style>
```

### 示例 3：分别控制进入和离开时长

效果说明：通过 `duration` 属性传入对象，分别设置进入动画时长为 700ms，离开动画时长为 1000ms。适用于需要快速展示、缓慢退出的交互场景。

```vue
<template>
  <wd-button type="primary" @click="handleShow">快速进入 缓慢退出</wd-button>

  <wd-transition
    :show="show"
    name="fade-up"
    :duration="{ enter: 700, leave: 1000 }"
    custom-class="demo-block"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)

function handleShow() {
  show.value = true
  // 展示 2 秒后自动隐藏，观察缓慢退出效果
  setTimeout(() => {
    show.value = false
  }, 2000)
}
</script>

<style scoped lang="scss">
.demo-block {
  position: fixed;
  left: 50%;
  top: 50%;
  margin: -50px 0 0 -50px;
  width: 100px;
  height: 100px;
  background: #0083ff;
  border-radius: 8px;
}
</style>
```

### 示例 4：完全自定义动画效果

效果说明：通过 6 个自定义 CSS 类属性（`enter-class`、`enter-active-class`、`enter-to-class`、`leave-class`、`leave-active-class`、`leave-to-class`）实现一个包含位移、旋转和背景色变化的复合过渡动画。

```vue
<template>
  <wd-button type="primary" @click="handleCustom">自定义复合动画</wd-button>

  <wd-transition
    :show="customShow"
    :duration="{ enter: 700, leave: 1000 }"
    enter-class="custom-enter"
    enter-active-class="custom-enter-active"
    enter-to-class="custom-enter-to"
    leave-class="custom-leave"
    leave-active-class="custom-leave-active"
    leave-to-class="custom-leave-to"
    custom-class="demo-block"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const customShow = ref<boolean>(false)

function handleCustom() {
  customShow.value = true
  // 动画展示 1.2 秒后自动隐藏
  setTimeout(() => {
    customShow.value = false
  }, 1200)
}
</script>

<style scoped lang="scss">
.demo-block {
  position: fixed;
  left: 50%;
  top: 50%;
  margin: -50px 0 0 -50px;
  width: 100px;
  height: 100px;
  background: #0083ff;
  border-radius: 8px;
}

/* 自定义进入动画：从左上角旋转滑入，红色背景变为蓝色 */
.custom-enter-active {
  transition-property: background, transform;
}

.custom-enter {
  transform: translate3d(-100px, -100px, 0) rotate(-180deg);
  background: #ff0000;
}

.custom-enter-to {
  transform: translate3d(0, 0, 0) rotate(0deg);
  background: #0083ff;
}

/* 自定义离开动画：向右下角旋转滑出，变为红色 */
.custom-leave-active {
  transition-property: background, transform;
}

.custom-leave {
  transform: translate3d(0, 0, 0) rotate(0deg);
  background: #0083ff;
}

.custom-leave-to {
  transform: translate3d(100px, 100px, 0) rotate(180deg);
  background: #ff0000;
}
</style>
```

### 示例 5：监听动画生命周期事件

效果说明：通过监听动画生命周期事件（`before-enter`、`enter`、`after-enter`、`before-leave`、`leave`、`after-leave`）在动画的不同阶段执行自定义逻辑，如显示加载状态、记录动画耗时等。

```vue
<template>
  <wd-button type="primary" @click="toggle">切换并监听生命周期</wd-button>

  <view class="log-panel">
    <text class="log-text" v-for="(log, index) in logs" :key="index">{{ log }}</text>
  </view>

  <wd-transition
    :show="show"
    name="zoom-in"
    :duration="500"
    custom-class="demo-block"
    @before-enter="addLog('before-enter: 进入动画即将开始')"
    @enter="addLog('enter: 进入动画已开始')"
    @after-enter="addLog('after-enter: 进入动画已完成')"
    @before-leave="addLog('before-leave: 离开动画即将开始')"
    @leave="addLog('leave: 离开动画已开始')"
    @after-leave="addLog('after-leave: 离开动画已完成')"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const logs = ref<string[]>([])

function toggle() {
  show.value = !show.value
}

function addLog(message: string) {
  logs.value.push(`${new Date().toLocaleTimeString()} - ${message}`)
  // 仅保留最近 10 条日志
  if (logs.value.length > 10) {
    logs.value.shift()
  }
}
</script>

<style scoped lang="scss">
.demo-block {
  position: fixed;
  left: 50%;
  top: 50%;
  margin: -50px 0 0 -50px;
  width: 100px;
  height: 100px;
  background: #0083ff;
  border-radius: 8px;
}

.log-panel {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.log-text {
  display: block;
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 4px;
}
</style>
```

## 注意事项

1. **show 属性控制**：动画的显示/隐藏完全由 `show` 属性控制，默认值为 `false`（隐藏）。请通过响应式变量绑定并在需要时切换其值。若初始值为 `true`，组件会在 `onBeforeMount` 生命周期中自动执行进入动画。

2. **动画类型默认值**：`name` 属性的默认值为 `'fade'`，即淡入淡出效果。若无需动画效果，可将 `name` 设为空字符串或不设置。

3. **动画时长单位**：`duration` 属性的单位为毫秒（ms），默认值为 300ms。传入对象时可分别控制进入和离开时长，例如 `{ enter: 500, leave: 800 }`。

4. **destroy 属性行为**：`destroy` 默认值为 `true`，表示动画结束后会将内容设置为 `display: none`。设置为 `false` 时内容保持渲染但不可见，适用于需要保持子组件状态（如表单输入值）的场景。

5. **懒渲染性能优化**：当 `lazy-render` 设置为 `true` 时，插槽内容仅在首次显示时渲染，可减少初始渲染开销。适用于包含大量子元素或复杂计算的弹窗场景。

6. **触摸滚动阻断**：`disable-touch-move` 设置为 `true` 时会在根元素上绑定 `@touchmove.stop.prevent` 阻止触摸滚动，仅在使用 `disableTouchMove` 为 true 时生效。适用于需要阻止背景滚动的弹窗场景。

7. **自定义动画类名**：使用自定义动画类名时（`enter-class` 等 6 个属性），需要同时定义 `*-active` 类指定 `transition-property`，否则动画不会生效。可参考示例 4 的实现方式。

8. **动画生命周期执行顺序**：组件内部的动画生命周期通过 `AbortablePromise` 实现顺序控制。当快速切换 `show` 值时，组件会自动取消未完成的 Promise，确保动画状态的准确性。

9. **组合动画支持**：`name` 属性支持传入数组（如 `['fade', 'zoom-in']`），可同时应用多种动画效果，数组中的动画会依次叠加。

10. **虚拟主机配置**：组件内部配置了 `virtualHost: true` 和 `styleIsolation: 'shared'`，在小程序平台组件的根节点样式会直接生效。

11. **CSS 过渡属性**：所有预设动画的 `transition-timing-function` 均设置为 `ease`。通过 `custom-style` 可覆盖默认的过渡时长和缓动函数。
