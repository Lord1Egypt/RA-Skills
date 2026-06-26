# Watermark 水印


## 组件概况

Watermark 水印组件是一个基于 Canvas 绘制的水印生成工具，可在页面或指定容器内生成平铺重复的文字或图片水印。该组件通过 Canvas 2D API 将水印内容绘制为图片，并将其作为背景图重复平铺在容器上，广泛应用于内容版权保护、信息安全溯源、企业内部系统防泄露等场景。

组件支持全屏和局部两种水印模式，提供文字水印和图片水印两种渲染方式，支持自定义字体样式、倾斜角度、透明度、间距等配置，并且针对不同平台（H5、微信小程序、钉钉小程序等）自动适配 Canvas 实现方案。

## 核心功能描述

- **文字水印**：通过 content 属性设置文字内容，支持自定义字体颜色、大小、样式、粗细、字体系列
- **图片水印**：通过 image 属性设置图片地址（支持网络图片和 Base64 格式），配合 imageWidth 和 imageHeight 控制图片尺寸
- **全屏/局部模式**：通过 fullScreen 属性切换全屏水印（fixed 定位）或局部水印（absolute 定位，覆盖父容器）
- **平铺重复**：水印以 Canvas 绘制的单元格为单位，通过 background-repeat: repeat 实现无缝平铺覆盖
- **倾斜旋转**：支持通过 rotate 属性调整水印倾斜角度，默认 -25 度倾斜
- **间距控制**：通过 gutterX 和 gutterY 分别控制水印单元格在 X 轴和 Y 轴方向上的间距
- **透明度控制**：通过 opacity 属性控制整体水印层的透明度，取值范围 0~1
- **平台适配**：在 H5 平台使用 document.createElement 创建 Canvas，在微信小程序平台优先使用离屏 Canvas（createOffscreenCanvas），不支持离屏 Canvas 时使用普通 Canvas 方案
- **响应式更新**：通过 watch 深度监听所有 props 变化，属性改变时自动重新生成水印

## 适用业务场景

- **内容版权保护**：在文章、图片、视频等内容展示页添加水印，标识版权归属
- **企业内部防泄露**：在企业后台管理系统、文档预览系统中添加员工信息水印，追踪泄露来源
- **数据敏感页面**：在展示敏感数据（如用户信息、财务数据）的页面添加水印，提升安全意识
- **图片防盗用**：在图片展示区域添加图片水印，防止未经授权的下载和使用
- **品牌标识**：在特定展示区域添加品牌 Logo 或文字标识，强化品牌形象
- **文档预览水印**：在文档预览服务中添加"草稿"、"机密"等水印标识

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| content | 水印显示的文字内容 | string | - | '' | - |
| image | 水印图片的地址，支持网络图片和 Base64（钉钉小程序仅支持网络图片） | string | - | '' | - |
| imageWidth | 水印图片的宽度，单位 px | number | - | 100 | - |
| imageHeight | 水印图片的高度，单位 px | number | - | 100 | - |
| gutterX | 水印单元格在 X 轴方向上的间距，单位 px | number | - | 0 | - |
| gutterY | 水印单元格在 Y 轴方向上的间距，单位 px | number | - | 0 | - |
| width | Canvas 画布宽度（单个水印单元格的宽度），单位 px | number | - | 100 | - |
| height | Canvas 画布高度（单个水印单元格的高度），单位 px | number | - | 100 | - |
| fullScreen | 是否为全屏水印。true 时使用 fixed 定位覆盖整个视口；false 时使用 absolute 定位覆盖父容器 | boolean | - | true | - |
| color | 水印字体颜色（文字水印时生效） | string | - | '#8c8c8c' | - |
| size | 水印字体大小（文字水印时生效），单位 px | number | - | 14 | - |
| fontStyle | 水印字体样式（仅微信和 H5 平台支持） | string | normal / italic / oblique | normal | - |
| fontWeight | 水印字体粗细（仅微信和 H5 平台支持） | number / string | - | 'normal' | - |
| fontFamily | 水印字体系列（仅微信和 H5 平台支持） | string | - | 'PingFang SC' | - |
| rotate | 水印旋转角度，正值顺时针旋转，负值逆时针旋转 | number | - | -25 | - |
| zIndex | 水印层的自定义层级 | number | - | 1100 | - |
| opacity | 水印层的透明度，取值范围 0~1 | number | 0 ~ 1 | 0.5 | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Slots

组件未提供插槽。

### Methods

组件未通过 defineExpose 对外暴露方法。

### Events

组件未定义对外抛出的事件。

### 外部样式类

| 类名 | 说明 |
|------|------|
| wd-watermark | 水印根节点样式类，可用于全局样式覆盖 |
| is-fullscreen | 全屏水印模式下的附加类名（当 fullScreen 为 true 时添加） |

## 使用示例

### 示例 1：基础文字水印

效果说明：在页面中生成全屏平铺的文字水印。默认使用灰色文字、-25 度倾斜、50% 透明度，覆盖整个视口区域。

```vue
<template>
  <!-- 全屏文字水印 -->
  <wd-watermark content="wot-ui-plus"></wd-watermark>

  <!-- 页面其他内容，水印会覆盖在上方 -->
  <view class="content">
    <text>这里是页面内容</text>
  </view>
</template>

<script setup lang="ts">
// 本示例无需额外脚本
</script>

<style scoped lang="scss">
.content {
  padding: 20px;
}
</style>
```

### 示例 2：图片水印与文字水印切换

效果说明：通过 image 属性控制是否显示图片水印。当 image 为空字符串时使用文字水印（由 content 属性定义），当 image 为有效图片地址时使用图片水印。示例支持通过按钮动态切换两种水印模式。

```vue
<template>
  <view class="controls">
    <wd-button @click="toggleImage(false)" plain>文字水印</wd-button>
    <wd-button @click="toggleImage(true)" plain>图片水印</wd-button>
  </view>

  <wd-watermark
    :image="watermarkImage"
    :width="130"
    :height="140"
    :image-width="38"
    :image-height="38"
    content="wot-ui-plus"
    :opacity="0.5"
  ></wd-watermark>

  <view class="content">
    <text>这里是页面内容，水印覆盖在上方</text>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const showImage = ref(false)

const watermarkImage = computed(() => {
  return showImage.value ? 'https://wot-ui-plus.cn/logo.png' : ''
})

function toggleImage(show: boolean) {
  showImage.value = show
}
</script>

<style scoped lang="scss">
.controls {
  display: flex;
  gap: 10px;
  padding: 16px;
}

.content {
  padding: 20px;
}
</style>
```

### 示例 3：局部水印

效果说明：通过设置 fullScreen="false" 将水印限定在特定容器内（使用 absolute 定位），而非覆盖整个页面。局部水印适用于只需要在特定区域（如文档预览区域、图片展示区域）添加水印的场景。

```vue
<template>
  <view class="watermark-container">
    <!-- 局部水印，仅覆盖当前容器 -->
    <wd-watermark
      :opacity="0.8"
      image="https://wot-ui-plus.cn/logo.png"
      :image-width="38"
      :image-height="38"
      :full-screen="false"
    ></wd-watermark>

    <!-- 容器内的内容 -->
    <wd-cell-group border>
      <wd-cell size="large" title="标题文字" value="内容" />
      <wd-cell title="标题文字" value="内容" size="large" icon="setting" is-link />
      <wd-cell size="large" title="标题文字" label="描述信息" value="内容" />
      <wd-cell size="large" title="标题文字" value="内容" />
      <wd-cell title="标题文字" value="内容" size="large" icon="setting" is-link />
      <wd-cell size="large" title="标题文字" label="描述信息" value="内容" />
    </wd-cell-group>
  </view>
</template>

<script setup lang="ts">
// 本示例无需额外脚本
</script>

<style scoped lang="scss">
.watermark-container {
  position: relative;
  min-height: 300px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}
</style>
```

### 示例 4：自定义水印样式

效果说明：通过调整颜色、大小、间距、旋转角度、透明度等参数，实现不同风格的文字水印效果。示例演示了如何配置一个更大、更透明、间距更宽的水印。

```vue
<template>
  <!-- 自定义样式的文字水印 -->
  <wd-watermark
    content="机密文件"
    :width="200"
    :height="200"
    :size="20"
    color="rgba(255, 0, 0, 0.3)"
    :rotate="-30"
    :opacity="0.6"
    :gutter-x="20"
    :gutter-y="20"
    font-weight="bold"
  ></wd-watermark>

  <view class="content">
    <text>这是带有自定义样式水印的页面内容</text>
  </view>
</template>

<script setup lang="ts">
// 本示例无需额外脚本
</script>

<style scoped lang="scss">
.content {
  padding: 20px;
}
</style>
```

### 示例 5：带间距控制的图文水印

效果说明：通过 width、height、gutterX、gutterY 属性精确控制水印单元格的尺寸和间距。较大的间距使水印更稀疏，较小的间距使水印更密集。适用于需要调整水印密度的场景。

```vue
<template>
  <!-- 稀疏水印 -->
  <wd-watermark
    content="DRAFT"
    :width="300"
    :height="300"
    :size="28"
    color="rgba(0, 0, 255, 0.15)"
    :rotate="-45"
    :gutter-x="50"
    :gutter-y="50"
  ></wd-watermark>

  <view class="content">
    <text>这是一个带有稀疏水印的页面</text>
  </view>
</template>

<script setup lang="ts">
// 本示例无需额外脚本
</script>

<style scoped lang="scss">
.content {
  padding: 20px;
}
</style>
```

## 注意事项

1. **全屏与局部模式**：fullScreen 属性决定水印的定位方式。设置为 true 时使用 `position: fixed` 覆盖整个浏览器视口；设置为 false 时使用 `position: absolute` 覆盖最近的定位父容器，因此父容器需要设置 `position: relative`。

2. **图片水印优先级**：当同时设置 image 和 content 时，image 属性优先生效。仅当 image 为空字符串时才会使用 content 渲染文字水印。

3. **图片格式支持**：image 属性支持网络图片 URL 和 Base64 格式的数据。钉钉小程序平台仅支持网络图片，不支持 Base64 格式。

4. **跨域图片处理**：使用网络图片时，组件会自动设置 `crossOrigin = 'anonymous'` 和 `referrerPolicy = 'no-referrer'`，以避免跨域问题。如果图片服务器不允许跨域访问，水印可能无法正确生成。

5. **平台差异**：
   - **H5 平台**：使用 `document.createElement('canvas')` 创建画布，不渲染 canvas 标签到 DOM 中
   - **微信小程序**：优先使用 `uni.createOffscreenCanvas()` 创建离屏画布；不支持时使用 `uni.createCanvasContext()` 传统方案
   - **钉钉小程序**：使用传统 Canvas 方案，通过 `toTempFilePath` 接口获取图片路径
   - 字体样式（fontStyle）、字体粗细（fontWeight）、字体系列（fontFamily）仅在微信和 H5 平台支持

6. **响应式重绘**：组件通过 watch 深度监听所有 props，当任何一个属性发生变化时会自动重新生成水印。无需手动调用刷新方法。

7. **像素比适配**：组件内部会根据设备的 pixelRatio 自动调整 Canvas 画布的实际尺寸，确保在不同分辨率的设备下水印清晰度一致。

8. **不可交互**：水印层通过 `pointer-events: none` 设置为不可交互状态，不会阻挡用户的点击、滑动等操作。

9. **Canvas 隐藏**：生成水印图片后，canvas 元素的 visibility 会被设置为 hidden（非 H5 平台且不支持离屏 Canvas 时），Canvas 标签仍然存在于 DOM 中但不显示。

10. **性能考虑**：频繁修改水印属性会导致 Canvas 反复重绘，建议在初始化时确定水印配置，避免在运行时频繁修改。对于大尺寸水印单元格或复杂的图片水印，生成过程可能需要一定时间。

11. **层级规划**：水印默认 zIndex 为 1100，确保覆盖大部分页面内容。若页面中存在更高层级的元素（如弹窗），可根据需要调整 zIndex 值。
