# LazyLoad 懒加载


## 组件概况

LazyLoad 懒加载组件是一个基于 `IntersectionObserver` API 实现的图片懒加载组件，用于优化长列表、瀑布流等场景下的图片加载性能。当图片进入或即将进入屏幕可视区域时才开始加载真实图片，在此之前显示占位图，从而减少首屏渲染时间和不必要的网络请求。

组件内部通过 `uni.createIntersectionObserver` 监听元素与视口的交叉状态，当满足触发条件时将占位图替换为真实图片，并支持淡入淡出过渡动画和图片加载失败时的错误占位图展示。

## 核心功能描述

- **IntersectionObserver 懒加载**：基于小程序原生 `IntersectionObserver` API 实现，性能优于传统的 scroll 事件监听方案
- **预加载阈值控制**：通过 `threshold` 属性设置图片距离屏幕底部多少像素时提前触发加载，支持正数（未进入屏幕即触发）和负数（部分进入屏幕后触发）
- **淡入淡出动画**：内置 CSS transition 过渡效果，图片加载完成后平滑显示，避免生硬的视觉切换
- **加载状态管理**：自动追踪图片加载状态（lazyed、loaded、error），并通过事件通知父组件
- **错误占位图**：图片加载失败时自动切换为错误占位图，提供友好的失败反馈
- **点击事件区分**：点击事件可区分点击的是占位图、真实图片还是错误图
- **圆角与高度控制**：支持自定义圆角和图片高度，适配各种卡片式布局
- **图片模式支持**：支持 uni-app image 组件的多种裁剪填充模式

## 适用业务场景

- **商品列表**：电商场景中商品列表通常包含大量图片，使用懒加载可显著减少首屏加载时间，提升用户体验
- **瀑布流布局**：结合 `wd-row` 和 `wd-col` 实现多列瀑布流图片展示，图片按需加载避免一次性请求过多资源
- **图片墙/相册**：用户相册、社交媒体动态等包含密集图片的场景，懒加载有效降低内存占用
- **无限滚动列表**：配合 `wd-loadmore` 实现上拉加载更多，每次仅加载可视区域内的图片
- **弱网环境优化**：在网络条件较差的场景下，懒加载避免同时发起大量图片请求导致页面卡顿

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| index | 图片索引标识，用于事件回调中标识具体是哪一张图片 | number / string | - | '' | - |
| image | 要显示的真实图片链接 | string | - | '' | - |
| mode | 图片裁剪和缩放模式 | string | aspectFit / aspectFill / widthFix / top / bottom / center / scaleToFill | widthFix | - |
| loadingImg | 加载中的占位图片路径，支持 base64 或图片 URL | string | - | 内置默认 base64 占位图 | - |
| errorImg | 加载失败的错误占位图路径，支持 base64 或图片 URL | string | - | 内置默认 base64 错误图 | - |
| threshold | 触发懒加载的阈值，单位 rpx。正数表示图片顶部距离屏幕底部多少距离时提前触发；负数表示图片底部超出屏幕底部多少距离后触发 | number / string | - | 100 | - |
| duration | 淡入淡出动画的过渡时间，单位 ms | number / string | - | 300 | - |
| effect | 过渡效果的速度曲线函数 | string | linear / ease / ease-in / ease-out / ease-in-out / cubic-bezier(n,n,n,n) | ease-in-out | - |
| isEffect | 是否启用淡入淡出过渡效果 | boolean | - | true | - |
| round | 图片圆角大小，支持数字和带单位字符串 | number / string | - | 0 | - |
| height | 图片高度，单位 px，支持数字和带单位字符串 | number / string | - | '200' | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Slots

组件未提供具名插槽。

### Methods

组件未通过 `defineExpose` 暴露外部可调用方法。

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| click | 点击图片时触发，区分占位图、真实图片、错误图 | index: 当前图片的索引标识 |
| load | 真实图片加载完成时触发 | index: 当前图片的索引标识 |
| error | 错误占位图加载完成时触发（即真实图片加载失败后显示错误图时） | index: 当前图片的索引标识 |

## 使用示例

### 示例 1：基础用法

效果说明：最基本的懒加载用法，通过 `image` 属性指定图片链接。组件默认显示加载占位图，当图片进入可视区域后开始加载真实图片并展示淡入动画。

```vue
<template>
  <view class="wrap">
    <wd-lazy-load
      :image="imageUrl"
      :index="0"
      @clickImg="clickImg"
      @statusChange="statusChange"
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const imageUrl = ref('https://example.com/product-image.jpg')

function clickImg(index: number | string) {
  console.log('点击了图片，索引:', index)
}

function statusChange(status: string) {
  console.log('图片状态变化:', status)
}
</script>
```

### 示例 2：瀑布流多列布局

效果说明：结合 `wd-row` 和 `wd-col` 实现双列瀑布流布局，图片使用圆角样式，通过 `threshold` 属性设置提前触发加载的距离，配合 `wd-loadmore` 实现上拉加载更多。

```vue
<template>
  <view class="wrap">
    <wd-row :gutter="12" wrap>
      <wd-col :span="12" v-for="(item, index) in list" :key="index">
        <view class="item">
          <wd-lazy-load
            threshold="-450"
            round="10"
            :image="item.src"
            :index="index"
            @statusChange="statusChange"
            @clickImg="clickImg"
          />
        </view>
      </wd-col>
    </wd-row>
    <wd-loadmore :state="loadMoreStatus" @reload="getData" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onReachBottom } from '@dcloudio/uni-app'
import type { LoadMoreState } from '@/uni_modules/wot-ui-plus/components/wd-loadmore/types'

const list = ref<any[]>([])
const loadMoreStatus = ref<LoadMoreState>('loading')
const data = ref([
  { src: 'https://example.com/image1.jpg' },
  { src: 'https://example.com/image2.jpg' },
  { src: 'https://example.com/image3.jpg' },
  { src: 'error.jpg' }, // 此图片会加载失败，显示错误占位图
  { src: 'https://example.com/image4.jpg' }
])

onLoad(() => {
  getData()
  setTimeout(() => {
    loadMoreStatus.value = 'finished'
  }, 1500)
})

// 页面滚动到底部时加载更多
onReachBottom(() => {
  loadMoreStatus.value = 'loading'
  setTimeout(() => {
    getData()
    loadMoreStatus.value = 'finished'
  }, 1000)
})

function statusChange(status: any) {
  console.log(status)
}

function clickImg(img: any) {
  console.log(img)
}

const getData = (): void => {
  for (let i = 0; i < 10; i++) {
    const index = Math.floor(Math.random() * (data.value.length - 1))
    list.value.push({
      src: data.value[index].src
    })
  }
}
</script>

<style lang="scss" scoped>
.item {
  margin-bottom: 20rpx;
  border-radius: 10rpx;
}
</style>
```

### 示例 3：自定义占位图与错误图

效果说明：通过 `loading-img` 和 `error-img` 属性替换默认的占位图和错误图，关闭淡入淡出动画，使用自定义的图片和样式。

```vue
<template>
  <view class="wrap">
    <wd-lazy-load
      height="300"
      round="16"
      :image="imageUrl"
      :index="0"
      loading-img="/static/images/loading-placeholder.png"
      error-img="/static/images/error-placeholder.png"
      :is-effect="false"
      @statusChange="statusChange"
      @clickImg="clickImg"
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const imageUrl = ref('https://example.com/custom-image.jpg')

function statusChange(status: any) {
  console.log('加载状态:', status)
}

function clickImg(index: number | string) {
  console.log('点击了图片索引:', index)
}
</script>
```

### 示例 4：不同图片模式与圆角展示

效果说明：展示 `mode` 属性的不同取值效果和 `round` 圆角属性的使用场景，适用于不同比例的图片和不同风格的 UI 设计。

```vue
<template>
  <view class="demo-wrap">
    <!-- widthFix 模式，宽度固定，高度自适应 -->
    <wd-lazy-load
      height="200"
      round="0"
      mode="widthFix"
      :image="imageUrl"
      :index="0"
    />

    <!-- aspectFill 模式，保持宽高比，填充整个区域，可能裁剪 -->
    <wd-lazy-load
      height="200"
      round="12"
      mode="aspectFill"
      :image="imageUrl"
      :index="1"
    />

    <!-- aspectFit 模式，保持宽高比，完整显示图片 -->
    <wd-lazy-load
      height="200"
      round="12"
      mode="aspectFit"
      :image="imageUrl"
      :index="2"
    />

    <!-- 大圆角卡片 -->
    <wd-lazy-load
      height="250"
      round="24"
      :image="imageUrl"
      :index="3"
      :duration="500"
      effect="ease"
    />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const imageUrl = ref('https://example.com/demo-image.jpg')
</script>

<style lang="scss" scoped>
.demo-wrap > * {
  margin-bottom: 20px;
}
</style>
```

## 注意事项

1. **threshold 阈值计算**：`threshold` 属性单位为 rpx，会自动转换为 px。正数表示图片顶部距离屏幕底部多少距离时提前触发懒加载（图片尚未进入屏幕即开始加载）；负数表示图片底部超出屏幕底部多少距离后才触发（图片部分进入屏幕）。合理设置该值可在视觉流畅度和性能之间取得平衡。

2. **图片路径变化自动重置**：当 `image` 属性发生变化时，组件会自动重置加载状态。如果传入 `null`、空字符串或 `undefined`，组件会自动标记为错误状态并显示错误占位图。

3. **事件回调参数**：所有事件（`click`、`load`、`error`）的回调参数均为传入的 `index` 值，而非事件对象本身。这是为了便于在列表中区分具体是哪一张图片触发的事件。

4. **点击类型区分**：`clickImg` 方法内部会根据当前加载状态区分点击的是哪种图片：`isShow` 为 false 时点击的是占位图（`lazyImg`），`isError` 为 true 时点击的是错误占位图（`errorImg`），否则点击的是真实图片（`realImg`）。

5. **IntersectionObserver 性能优化**：组件在图片加载完成后会自动断开 `IntersectionObserver` 监听，减少不必要的性能消耗。图片一旦显示就不再需要监听其位置变化。

6. **淡入动画原理**：当 `isEffect` 为 true 时，组件先将透明度设置为 0，延时 30ms 后过渡到 1。这 30ms 延时是为了确保在浏览器 H5 环境下过渡效果能正确生效。

7. **rpx 单位支持**：`threshold` 属性使用 rpx 单位，会自动通过 `uni.upx2px` 转换为 px。`round` 和 `height` 属性通过 `addUnit` 工具函数处理，支持纯数字（默认添加 px 单位）和带单位的字符串。

8. **占位图与错误图默认值**：如果未设置 `loadingImg` 和 `errorImg`，组件会使用内置的 base64 编码占位图，无需额外引入图片资源。

9. **onReachBottom 事件广播**：组件在 mounted 阶段会监听全局 `onReachBottom` 事件（通过 `uni.$once`），当页面触底时如果图片尚未加载，则立即显示图片。这使得懒加载组件能与页面的下拉加载更多功能良好配合。