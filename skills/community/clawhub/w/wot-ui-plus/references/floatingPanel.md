# FloatingPanel 浮动面板


## 组件概况

FloatingPanel 浮动面板组件是一个可从页面底部向上拖拽展开或收起的交互面板。用户可以通过拖拽面板头部或内容区域来调整面板高度，面板会自动吸附到预设的锚点位置。该组件适用于需要展示可调节高度内容面板的场景，如地图上的信息面板、底部抽屉式菜单、可展开的操作面板等。

## 核心功能描述

- **基础浮动面板**：通过默认锚点展示浮动面板，面板高度在最小高度（100px）和最大高度（窗口高度的 60%）之间调节
- **拖拽调节高度**：用户可通过拖拽面板头部指示条或内容区域来调整面板高度，拖拽过程带有阻尼效果
- **锚点吸附**：松手后面板会自动吸附到距离当前高度最近的锚点位置，支持自定义多个锚点
- **双锚点模式**：默认使用最小和最大两个锚点，可通过 `anchors` 属性设置多个自定义锚点
- **内容拖拽控制**：可通过 `content-draggable` 属性控制是否允许在内容区域拖拽面板，关闭后仅头部区域可拖拽
- **动画过渡**：高度切换时带有弹性贝塞尔曲线动画过渡效果，动画时长可自定义
- **底部安全距离适配**：支持通过 `safe-area-inset-bottom` 适配 iPhone X 等全面屏机型的底部安全区域
- **滚动条控制**：面板内容区域使用 scroll-view 实现纵向滚动，可控制滚动条显示隐藏

## 适用业务场景

- **地图应用信息面板**：在地图应用中，底部浮动面板用于展示地点详情、路线信息等，用户可根据需要调整面板高度查看更多内容
- **底部操作面板**：用于展示快捷操作菜单或工具栏，平时收起仅露出少量内容，拖拽展开后可完整展示
- **可调节内容展示区**：如音乐播放器的播放列表面板、商品详情的规格选择面板等需要灵活调节展示区域的场景
- **半屏弹窗替代方案**：相比固定高度的弹窗，浮动面板提供更灵活的交互方式，用户可自主控制内容展示区域大小

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| height | number | 0 | 否 | 面板的显示高度，支持 v-model 双向绑定 |
| anchors | `Array<number>` | [100, windowHeight * 0.6] | 否 | 自定义锚点数组，建议至少设置 2 个值，分别表示最小和最大高度 |
| safeAreaInsetBottom | boolean | false | 否 | 是否开启底部安全区域适配 |
| showScrollbar | boolean | true | 否 | 内容区域是否显示滚动条 |
| duration | number / string | 300 | 否 | 动画过渡时长，单位毫秒 |
| contentDraggable | boolean | true | 否 | 是否允许在内容区域拖拽面板，设为 false 时仅头部区域可拖拽 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

| 事件名称 | 参数 | 说明 |
| --- | --- | --- |
| height-change | `{ height: number }` | 面板高度发生变化（松手吸附后）触发，返回当前高度值 |
| update:height | `height: number` | v-model:height 双向绑定更新时触发，返回新高度值 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于放置面板内容，支持任意自定义内容 |

### CSS 变量

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --wot-floating-panel-bg | $-color-white | 面板背景色 |
| --wot-floating-panel-radius | 16px | 面板顶部圆角大小 |
| --wot-floating-panel-z-index | 99 | 面板层级 |
| --wot-floating-panel-header-height | 30px | 面板头部高度 |
| --wot-floating-panel-bar-width | 20px | 头部指示条宽度 |
| --wot-floating-panel-bar-height | 3px | 头部指示条高度 |
| --wot-floating-panel-bar-bg | $-color-gray-5 | 头部指示条背景色 |
| --wot-floating-panel-bar-radius | 4px | 头部指示条圆角 |
| --wot-floating-panel-content-bg | $-color-white | 内容区域背景色 |

## 使用示例

### 示例 1：基础用法

效果说明：展示一个基础的浮动面板，使用默认锚点（最小高度 100px，最大高度为窗口高度的 60%），开启底部安全距离适配。用户可以通过拖拽面板头部或内容区域来调整面板高度，松手后面板会自动吸附到最近的锚点位置。

```vue
<template>
  <wd-floating-panel safeAreaInsetBottom>
    <wd-cell-group border>
      <wd-cell v-for="item in list" :key="item" :title="item" />
    </wd-cell-group>
  </wd-floating-panel>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
</script>
```

### 示例 2：自定义锚点

效果说明：通过 `anchors` 属性设置多个自定义锚点，并在面板高度变化时通过 `height-change` 事件获取当前高度。用户拖拽面板后，面板会自动吸附到设置的锚点位置（100px、窗口高度的 40%、窗口高度的 70%）。面板当前高度通过双向绑定实时更新并在页面中展示。

```vue
<template>
  <wd-floating-panel
    v-model:height="height"
    :anchors="anchors"
    safeAreaInsetBottom
    @height-change="handleHeightChange"
  >
    <view class="panel-content">
      <text>当前锚点：{{ anchors.map(formatUnit) }}</text>
      <text>当前高度：{{ formatUnit(Math.round(height)) }}</text>
    </view>
  </wd-floating-panel>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const height = ref<number>(0)
const anchors = ref<number[]>([])

const formatUnit = (value: number) => `${value}px`

const handleHeightChange = ({ height: newHeight }: { height: number }) => {
  console.log('面板高度已变化:', newHeight)
}

onMounted(() => {
  // 获取窗口高度并设置锚点
  const windowHeight = uni.getSystemInfoSync().windowHeight
  anchors.value = [100, Math.round(0.4 * windowHeight), Math.round(0.7 * windowHeight)]
  // 设置初始高度为中间锚点
  height.value = anchors.value[1]
})
</script>

<style scoped lang="scss">
.panel-content {
  padding: 16px;
  text-align: center;
  font-size: 16px;
  font-weight: bold;
}
</style>
```

### 示例 3：仅头部拖拽

效果说明：通过设置 `content-draggable` 属性为 `false`，禁止在内容区域拖拽面板。此时用户只能通过拖拽面板头部的指示条来调整面板高度。适用于内容区域包含文本选择、滑动组件等可能与拖拽操作冲突的场景。

```vue
<template>
  <wd-floating-panel :contentDraggable="false" safeAreaInsetBottom>
    <view class="panel-content">
      <text>此区域不可拖拽，请拖拽头部指示条来调整面板高度</text>
    </view>
  </wd-floating-panel>
</template>

<script setup lang="ts">
/* 本示例无需额外逻辑。 */
</script>

<style scoped lang="scss">
.panel-content {
  padding: 16px;
  text-align: center;
  font-size: 14px;
  color: #999;
}
</style>
```

### 示例 4：隐藏滚动条

效果说明：通过设置 `show-scrollbar` 属性为 `false` 隐藏内容区域的滚动条，实现更简洁的视觉效果。面板内容超出时仍可滚动，但不显示滚动条指示器。

```vue
<template>
  <wd-floating-panel :showScrollbar="false" safeAreaInsetBottom>
    <wd-cell-group border>
      <wd-cell v-for="(item, index) in list" :key="index" :title="item" :value="'选项 ' + (index + 1)" />
    </wd-cell-group>
  </wd-floating-panel>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const list = ['选项A', '选项B', '选项C', '选项D', '选项E', '选项F', '选项G', '选项H', '选项I', '选项J']
</script>
```

### 示例 5：监听高度变化

效果说明：通过 `@height-change` 事件监听面板高度变化，在用户完成拖拽操作并松手吸附后触发。此事件可用于记录用户偏好的面板高度、保存面板状态等场景。

```vue
<template>
  <wd-floating-panel
    v-model:height="panelHeight"
    :anchors="[100, 300, 500]"
    safeAreaInsetBottom
    @height-change="onHeightChange"
  >
    <view class="panel-content">
      <text>面板当前高度：{{ panelHeight }}px</text>
      <text>最近一次吸附高度：{{ lastHeight }}px</text>
    </view>
  </wd-floating-panel>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const panelHeight = ref<number>(300)
const lastHeight = ref<number>(300)

const onHeightChange = ({ height }: { height: number }) => {
  lastHeight.value = height
  uni.showToast({
    title: `高度: ${height}px`,
    icon: 'none'
  })
}
</script>

<style scoped lang="scss">
.panel-content {
  padding: 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 14px;
}
</style>
```

## 注意事项

- **锚点数量要求**：`anchors` 数组建议至少包含 2 个值，第一个值作为最小高度，最后一个值作为最大高度。如果数组长度不足 2 个，组件会自动使用默认值填充。
- **height 初始值**：`height` 属性默认值为 0，如果不通过 v-model 绑定初始值，面板将默认处于最小高度位置。建议在设置自定义锚点时同时指定初始高度。
- **拖拽阻尼效果**：在拖拽超出锚点范围时，组件会应用阻尼系数（0.2）进行缓动，拖拽越远阻力越大，提供自然的交互反馈。
- **内容区域滚动冲突**：当 `contentDraggable` 为 `true`（默认值）时，在内容区域拖拽会优先触发面板高度调整而非内容滚动。如果内容区域包含长列表需要滚动浏览，建议设置为 `false`。
- **transform 动画性能**：面板高度切换使用 CSS `transform: translateY` 实现动画过渡，配合 `will-change: transform` 优化性能。动画使用弹性贝塞尔曲线 `cubic-bezier(0.18, 0.89, 0.32, 1.28)` 实现回弹效果。
- **伪元素背景延伸**：组件通过 `::after` 伪元素将面板背景色延伸至页面底部，确保面板收起时不会出现背景色断层。
- **触摸事件处理**：组件使用 `.passive` 修饰符绑定触摸事件以优化滚动性能，同时在内容区域的 `touchmove` 上使用 `.stop.prevent` 阻止事件冒泡。
- **窗口高度获取**：最大锚点默认值依赖窗口高度计算，组件在挂载时通过 `getSystemInfo()` 获取窗口高度。横竖屏切换时可能需要手动更新锚点值。
- **层级关系**：面板默认 `z-index` 为 99，如果页面中存在其他浮层组件（如弹窗、下拉菜单等），请注意层级关系避免遮挡。
- **安全区域适配**：开启 `safeAreaInsetBottom` 后会在底部增加安全距离，该设置仅对 iPhone X 等带有底部安全区域的机型生效。
