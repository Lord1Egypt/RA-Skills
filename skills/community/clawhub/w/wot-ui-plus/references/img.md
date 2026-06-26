# Img 图片


## 组件概况

Img 图片组件是一个增强版的图片展示组件，基于 uni-app 原生 `image` 组件封装。除了基础的图片渲染能力外，还提供了加载状态管理、错误处理、图片预览、圆角/圆形裁剪、懒加载以及自定义占位插槽等丰富功能，适用于各种图片展示场景。

组件内部维护了图片的加载状态（loading、error、success），并根据状态自动切换显示内容，为开发者提供了完整的图片加载生命周期控制能力。

## 核心功能描述

- **图片加载状态管理**：自动追踪图片加载过程，提供 loading、error、success 三种状态
- **自定义插槽**：支持 `loading` 和 `error` 两个具名插槽，允许自定义加载中和加载失败时的显示内容
- **图片预览**：内置图片预览功能，点击即可调用 uni-app 原生图片预览能力
- **尺寸控制**：支持设置宽度、高度，默认单位为 px，也支持其他 CSS 单位
- **填充模式**：支持 uni-app image 组件的所有 mode 值，控制图片裁剪和缩放行为
- **圆角与圆形**：通过 `radius` 属性设置圆角大小，或通过 `round` 属性快速显示为圆形
- **懒加载**：通过 `lazy-load` 属性启用图片懒加载，优化页面性能
- **自定义样式**：支持自定义根节点样式和样式类，满足个性化定制需求

## 适用业务场景

- **商品列表**：电商场景中展示商品缩略图，支持点击预览大图
- **用户头像**：使用圆形头像展示，配合加载失败时的默认占位图
- **图文内容**：文章、帖子中的图片展示，支持懒加载优化首屏性能
- **图片墙/相册**：批量图片展示，结合不同填充模式实现多样化布局
- **加载优化**：网络图片加载时显示加载动画，提升用户体验

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| src | 图片链接 | string | - | - | - |
| previewSrc | 预览图片链接，点击预览时使用该地址 | string | - | - | - |
| round | 是否显示为圆形 | boolean | - | false | - |
| mode | 图片裁剪和缩放模式 | string | scaleToFill / aspectFit / aspectFill / widthFix / heightFix / top / bottom / center / left / right / top left / top right / bottom left / bottom right | scaleToFill | - |
| lazyLoad | 是否开启图片懒加载 | boolean | - | false | - |
| width | 图片宽度，默认单位为 px，支持带单位的字符串或纯数字 | number / string | - | - | - |
| height | 图片高度，默认单位为 px，支持带单位的字符串或纯数字 | number / string | - | - | - |
| radius | 图片圆角大小，默认单位为 px，支持带单位的字符串或纯数字 | number / string | - | - | - |
| enablePreview | 是否允许点击预览图片，仅在图片加载成功后点击生效 | boolean | - | false | - |
| showMenuByLongpress | 是否开启长按图片显示识别小程序码菜单，仅在微信小程序平台有效 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |
| customImage | 自定义 image 元素样式类 | string | - | '' | - |

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| loading | 图片加载中的自定义内容，在 `status` 为 `loading` 时显示 | 任意内容 |
| error | 图片加载失败的自定义内容，在 `status` 为 `error` 时显示 | 任意内容 |

### Methods

组件未暴露外部可调用的方法。

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| click | 点击图片时触发，无论图片是否加载成功都会触发 | event: MouseEvent |
| load | 图片加载成功时触发 | event: Event |
| error | 图片加载失败时触发 | event: Event |

## 使用示例

### 基础用法

最基本的图片展示方式，通过 `src` 属性指定图片链接，通过 `width` 和 `height` 控制图片尺寸。

```vue
<template>
  <wd-img :width="100" :height="100" :src="imageUrl" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const imageUrl = ref('https://example.com/image.jpg')
</script>
```

### 自定义加载状态插槽

通过 `loading` 和 `error` 两个具名插槽，自定义图片加载过程中的显示内容。

```vue
<template>
  <wd-img :width="100" :height="100" src="https://example.com/image.jpg">
    <template #loading>
      <view class="loading-wrap">
        <wd-loading />
      </view>
    </template>
    <template #error>
      <view class="error-wrap">加载失败</view>
    </template>
  </wd-img>
</template>

<style scoped>
.loading-wrap {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-wrap {
  width: 100%;
  height: 100%;
  background-color: rgb(122, 117, 117);
  color: white;
  line-height: 100px;
  text-align: center;
}
</style>
```

### 填充模式

通过 `mode` 属性设置图片的裁剪和缩放模式，适用于不同比例的图片展示场景。

```vue
<template>
  <view class="mode-demo">
    <wd-img width="100%" height="200px" :src="imageUrl" mode="scaleToFill" />
    <view>scaleToFill</view>

    <wd-img width="100%" height="200px" :src="imageUrl" mode="aspectFit" />
    <view>aspectFit</view>

    <wd-img width="100%" height="200px" :src="imageUrl" mode="aspectFill" />
    <view>aspectFill</view>

    <wd-img width="100%" height="200px" :src="imageUrl" mode="top left" />
    <view>top left</view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const imageUrl = ref('https://example.com/image.jpg')
</script>
```

### 圆形与圆角

通过 `round` 属性将图片显示为圆形，或通过 `radius` 属性设置自定义圆角大小。

```vue
<template>
  <!-- 圆形图片 -->
  <wd-img round width="100" height="100" :src="imageUrl" mode="aspectFill" />

  <!-- 圆角图片 -->
  <wd-img :radius="10" width="100" height="100" :src="imageUrl" />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const imageUrl = ref('https://example.com/avatar.jpg')
</script>
```

### 图片预览

通过 `enable-preview` 属性开启点击预览功能。可以使用 `preview-src` 指定预览时使用的高清图片链接。

```vue
<template>
  <!-- 点击预览原图 -->
  <wd-img :width="100" :height="100" :src="imageUrl" :enable-preview="true" />

  <!-- 点击预览指定的高清图 -->
  <wd-img
    :width="100"
    :height="100"
    :src="thumbUrl"
    :preview-src="hdImageUrl"
    :enable-preview="true"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const thumbUrl = ref('https://example.com/thumb.jpg')
const hdImageUrl = ref('https://example.com/hd.jpg')
</script>
```

## 注意事项

1. **加载状态自动管理**：组件内部会自动追踪图片的加载状态。当 `src` 属性发生变化时，状态会自动重置为 `loading`。开发者无需手动管理状态切换。

2. **预览功能限制**：图片预览功能仅在 `enable-preview` 为 `true` 且图片加载成功（`status` 为 `success`）时才会触发。如果图片加载失败，点击不会触发预览。

3. **预览图片优先级**：当同时设置了 `preview-src` 和 `src` 且启用了预览功能时，点击预览会使用 `preview-src` 作为预览图片。若 `preview-src` 未设置，则使用 `src` 进行预览。

4. **插槽显示逻辑**：`loading` 插槽仅在图片加载中时显示，`error` 插槽仅在图片加载失败时显示。两个插槽同时只能显示一个，图片加载成功后插槽内容会被隐藏。

5. **尺寸单位**：`width`、`height`、`radius` 属性支持数字和字符串类型。当传入数字时，默认单位为 px；当传入字符串时，需自行指定单位（如 `'100px'`、`'50%'`、`'2rem'`）。

6. **小程序码菜单**：`show-menu-by-longpress` 属性仅在微信小程序平台有效，其他平台会被忽略。开启后长按图片会显示识别小程序码菜单。

7. **样式定制**：`custom-style` 和 `custom-class` 作用于组件根节点，`custom-image` 作用于内部 image 元素。推荐使用这两个属性进行样式定制，避免直接修改组件内部样式。

8. **懒加载说明**：`lazy-load` 属性开启后，图片会在进入屏幕可视区域后才开始加载，适用于长列表、瀑布流等场景，可有效减少首屏加载时间和带宽消耗。
