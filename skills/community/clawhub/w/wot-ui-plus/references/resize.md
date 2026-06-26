# Resize 自适应


## 组件概况

Resize 自适应组件是一个用于监听插槽内容尺寸变化的容器组件。其核心原理是利用两个方向相反的 `scroll-view` 容器与超大占位元素，当插槽内容尺寸发生变化时，scroll-view 的滚动条位置会随之改变，进而触发 scroll 事件来捕获尺寸变化。组件通过 `boundingClientRect` API 获取容器的精确位置信息，并将变化结果通过事件通知父组件。

该组件巧妙避免了在某些平台不支持 `ResizeObserver` API 的限制，采用 scroll 事件监听的方式实现了跨平台的尺寸变化检测能力。

## 核心功能描述

- **尺寸变化监听**：实时监测插槽内容的宽高变化，当内容尺寸发生改变时立即触发 `resize` 事件
- **跨平台兼容**：基于 scroll-view 滚动事件实现，兼容 H5、小程序、App 等所有 uni-app 平台
- **位置信息反馈**：除了宽高信息外，还提供 top、bottom、left、right 六个维度的精确位置数据
- **动态高度填充**：组件会自动将父容器的高度设置为当前内容高度，防止父容器因脱离文档流而坍塌
- **初始化回调**：组件挂载完成后会立即触发一次 resize 事件，返回初始容器尺寸信息
- **防抖过滤**：内部对 scroll 事件进行次数过滤，避免初始化阶段和滚动条拉到底部时产生多余触发
- **自定义样式类**：支持为内部 container 元素设置自定义样式类，方便深度样式定制

## 适用业务场景

- **动态内容高度计算**：当子组件内容通过接口异步加载或用户交互动态增加时，父组件需要知道新的容器高度以调整布局
- **吸顶组件配合**：`wd-sticky` 组件内部依赖 `wd-resize` 监听吸顶内容的尺寸变化，确保吸顶位置计算的准确性
- **图表自适应**：ECharts、F2 等图表库在容器尺寸变化时需要重新渲染，通过 resize 事件可以自动触发图表重绘
- **响应式布局调整**：当子组件宽度变化时（如窗口 resize、侧边栏展开收起），父组件根据新尺寸调整自身布局
- **列表动态项**：折叠面板、树形控件等展开收起时高度变化，需要通知外层容器重新计算高度
- **富文本内容**：文章内容、评论列表等长度不确定的内容区域，需要在渲染完成后获取实际占据空间

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |
| customContainerClass | 自定义内部 container 容器的样式类 | string | - | '' | - |

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，需要监听尺寸变化的内容 | 任意内容 |

### Methods

组件未通过 `defineExpose` 暴露外部可调用方法。

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| resize | 容器尺寸发生变化时触发 | `detail: { height: number, width: number, top: number, bottom: number, left: number, right: number }` |

## 使用示例

### 示例 1：基础用法

效果说明：包裹一个背景色为蓝色的方块元素，初始尺寸为 100x100，1.5 秒后通过响应式变量将其改为 100px x 100px。当尺寸变化时，组件会自动触发 `resize` 事件，返回最新的容器尺寸和位置信息。

```vue
<template>
  <page-wraper>
    <demo-block title="基础用法">
      <wd-resize @resize="handleResize">
        <view :style="`background: #4d80f0; width: ${width};height: ${height}`"></view>
      </wd-resize>
      <view class="tip-item">
        <view class="tip-label">width:</view>
        {{ lastWidth }}
        <wd-icon name="arrow-up" custom-class="icon"></wd-icon>
        {{ sizeWidth }}
      </view>
      <view class="tip-item">
        <view class="tip-label">height:</view>
        {{ lastHeight }}
        <wd-icon name="arrow-up" custom-class="icon"></wd-icon>
        {{ sizeHeight }}
      </view>
    </demo-block>
  </page-wraper>
</template>

<script lang="ts" setup>
import { onReady } from '@dcloudio/uni-app'
import { ref } from 'vue'

const width = ref<string>('')
const height = ref<string>('')
const lastWidth = ref<string>('')
const lastHeight = ref<string>('')
const sizeWidth = ref<string>('')
const sizeHeight = ref<string>('')

onReady(() => {
  setTimeout(() => {
    width.value = '100px'
    height.value = '100px'
  }, 1500)
})

function handleResize(detail: Record<string, string | number>) {
  console.log(detail)
  const { height, width } = detail
  lastHeight.value = sizeHeight.value
  lastWidth.value = sizeWidth.value
  sizeHeight.value = height as string
  sizeWidth.value = width as string
}
</script>

<style lang="scss" scoped>
.tip-item {
  margin-top: 15px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 12px;
}

.tip-label {
  display: inline-block;
  width: 70px;
}

:deep(.icon) {
  margin: 0 4px;
  transform: rotate(90deg);
}
</style>
```

### 示例 2：动态内容高度自适应

效果说明：结合 `v-if` 条件渲染，在用户点击按钮时动态插入或删除内容。当内容插入后，容器高度会自动增加，`resize` 事件会触发并返回新的尺寸信息。适用于折叠面板、展开收起等场景。

```vue
<template>
  <view class="demo-wrap">
    <wd-button type="primary" @click="toggleContent" style="margin-bottom: 16px">
      {{ showContent ? '收起内容' : '展开内容' }}
    </wd-button>

    <wd-resize @resize="handleResize">
      <view class="content-box">
        <view>固定内容：这是始终显示的区域</view>
        <view v-if="showContent" class="expand-content">
          <view>动态内容 1：这是一段通过 v-if 控制显示的内容</view>
          <view>动态内容 2：容器高度会根据内容自动调整</view>
          <view>动态内容 3：resize 组件会自动通知父组件尺寸变化</view>
          <view>动态内容 4：适用于折叠面板、展开收起等场景</view>
        </view>
      </view>
    </wd-resize>

    <view class="info">
      当前高度: {{ currentHeight }}px | 当前宽度: {{ currentWidth }}px
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const showContent = ref<boolean>(false)
const currentHeight = ref<number>(0)
const currentWidth = ref<number>(0)

function toggleContent() {
  showContent.value = !showContent.value
}

function handleResize(detail: Record<string, string | number>) {
  currentHeight.value = Number(detail.height.toFixed(2))
  currentWidth.value = Number(detail.width.toFixed(2))
}
</script>

<style lang="scss" scoped>
.demo-wrap {
  padding: 16px;
}

.content-box {
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.expand-content {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e0e0e0;
  color: #666;
  line-height: 1.8;
}

.info {
  margin-top: 16px;
  font-size: 14px;
  color: #999;
}
</style>
```

### 示例 3：六维度位置信息追踪

效果说明：全面展示 `resize` 事件返回的所有位置信息，包括 height、width、top、right、bottom、left 六个维度。当容器尺寸或位置变化时，同时显示变化前后的值，方便开发者理解各维度的含义。

```vue
<template>
  <view class="demo-wrap">
    <wd-resize @resize="handleResize">
      <view :style="boxStyle" class="resize-box">
        尺寸可变的内容区域
      </view>
    </wd-resize>

    <view class="info-panel">
      <view class="info-row">
        <text class="label">height:</text>
        <text class="prev">{{ lastHeight || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeHeight || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">width:</text>
        <text class="prev">{{ lastWidth || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeWidth || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">top:</text>
        <text class="prev">{{ lastTop || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeTop || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">right:</text>
        <text class="prev">{{ lastRight || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeRight || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">bottom:</text>
        <text class="prev">{{ lastBottom || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeBottom || '-' }}</text>
      </view>
      <view class="info-row">
        <text class="label">left:</text>
        <text class="prev">{{ lastLeft || '-' }}</text>
        <text class="arrow">></text>
        <text class="current">{{ sizeLeft || '-' }}</text>
      </view>
    </view>

    <wd-button @click="changeSize" style="margin-top: 16px">
      改变尺寸
    </wd-button>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const boxWidth = ref<number>(100)
const boxHeight = ref<number>(100)

const lastWidth = ref<string>('')
const lastHeight = ref<string>('')
const lastTop = ref<string>('')
const lastRight = ref<string>('')
const lastBottom = ref<string>('')
const lastLeft = ref<string>('')

const sizeWidth = ref<string>('')
const sizeHeight = ref<string>('')
const sizeTop = ref<string>('')
const sizeRight = ref<string>('')
const sizeBottom = ref<string>('')
const sizeLeft = ref<string>('')

const boxStyle = computed(() => {
  return {
    width: `${boxWidth.value}px`,
    height: `${boxHeight.value}px`
  }
})

function handleResize(detail: Record<string, string | number>) {
  console.log('resize detail:', detail)
  const { height, width, top, right, bottom, left } = detail

  // 保存上一次的尺寸信息
  lastHeight.value = sizeHeight.value
  lastWidth.value = sizeWidth.value
  lastTop.value = sizeTop.value
  lastRight.value = sizeRight.value
  lastBottom.value = sizeBottom.value
  lastLeft.value = sizeLeft.value

  // 更新当前尺寸信息
  sizeHeight.value = String(height)
  sizeWidth.value = String(width)
  sizeTop.value = String(top)
  sizeRight.value = String(right)
  sizeBottom.value = String(bottom)
  sizeLeft.value = String(left)
}

function changeSize() {
  boxWidth.value = boxWidth.value + 50
  boxHeight.value = boxHeight.value + 30
}
</script>

<style lang="scss" scoped>
.demo-wrap {
  padding: 16px;
}

.resize-box {
  background: #4d80f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: width 0.3s, height 0.3s;
}

.info-panel {
  margin-top: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  padding: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  padding: 4px 0;
}

.label {
  display: inline-block;
  width: 70px;
}

.prev {
  color: #999;
}

.arrow {
  margin: 0 8px;
  transform: rotate(90deg);
}

.current {
  color: #4d80f0;
  font-weight: bold;
}
</style>
```

### 示例 4：配合自定义容器样式类

效果说明：使用 `custom-container-class` 属性为内部的 container 容器添加自定义样式类，实现特殊的布局需求。同时配合 `custom-style` 为根节点设置样式。

```vue
<template>
  <view class="demo-wrap">
    <wd-resize
      custom-class="my-resize-root"
      custom-container-class="my-resize-container"
      @resize="handleResize"
    >
      <view class="chart-placeholder">
        <view class="chart-title">图表区域</view>
        <view>宽度: {{ chartWidth }}px</view>
        <view>高度: {{ chartHeight }}px</view>
      </view>
    </wd-resize>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const chartWidth = ref<number>(0)
const chartHeight = ref<number>(0)

function handleResize(detail: Record<string, string | number>) {
  chartWidth.value = Number(detail.width.toFixed(2))
  chartHeight.value = Number(detail.height.toFixed(2))
}
</script>

<style lang="scss" scoped>
.demo-wrap {
  padding: 16px;
}

.chart-placeholder {
  width: 100%;
  min-height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 20px;
  color: #fff;
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
}
</style>
```

## 注意事项

1. **scroll-view 监听机制**：组件内部使用了两个 scroll-view 来监听尺寸变化，一个使用 100000px 的超大占位元素监听内容变大，另一个使用 250% 的占位元素监听内容变小。这种设计巧妙利用了 scroll 事件对容器尺寸变化的敏感性，是一种跨平台的兼容方案。

2. **首次事件初始化**：组件在 mounted 时通过 `boundingClientRect` 获取初始尺寸后，第一次 scroll 事件被触发时（`scrollEventCount` 为 0），会立即向父组件发送一次 resize 事件，通知当前的初始容器大小。这是为了确保父组件在挂载后就能获取到准确的尺寸信息。

3. **事件过滤机制**：组件内部使用 `scrollEventCount` 计数器来过滤多余的 scroll 事件。前两次事件被用于初始化通知，当计数器值小于 3 时会直接返回，不触发 resize 事件。这是为了避免滚动条拉到底部时产生多余的触发。

4. **父容器高度维持**：组件会自动将父容器的高度设置为当前内容高度（`height.value = newHeight`），这是为了防止 scroll-view 脱离文档流后父容器高度坍塌。宽度也同样处理。

5. **尺寸变化检测逻辑**：组件分别比较新高度与上次高度、新宽度与上次宽度，只有当至少一个维度发生变化时才触发 resize 事件。当宽高同时改变时，也只会触发一次 resize 事件，避免重复通知。

6. **scrollToBottom 滚动位置计算**：每次触发 resize 事件后，组件会通过 `scrollToBottom` 函数重新设置两个 scroll-view 的滚动位置。expand 方向设置为 `100000 + lastHeight`，shrink 方向设置为 `3 * height + lastHeight`，确保下次尺寸变化时能够正确触发 scroll 事件。

7. **customContainerClass 作用范围**：`custom-container-class` 属性作用于内部的 container 容器元素（`.wd-resize__container`），该容器使用绝对定位。如果需要调整容器内部的布局方式，可以通过该属性添加自定义样式类。

8. **定位方案**：内部 container 容器使用 `position: absolute`，配合 `min-width: 1px` 和 `min-height: 1px` 确保最小尺寸。监听用的两个 scroll-view 使用绝对定位覆盖整个容器区域，并通过 `z-index: -9999`、`overflow: hidden`、`visibility: hidden` 隐藏，不会对用户界面产生影响。

9. **性能建议**：由于 resize 事件会在每次尺寸变化时触发，如果事件处理函数中包含复杂计算或 DOM 操作，建议进行适当的防抖或节流处理。特别是在频繁变化的场景下（如窗口拖动 resize），需要注意性能优化。

10. **组件初始化时机**：resize 组件在 `onMounted` 钩子中执行初始化，使用 `uni.createSelectorQuery` 查询元素布局信息。如果父组件在 mounted 后立即需要尺寸信息，可以通过监听 resize 事件获取，无需额外等待。
