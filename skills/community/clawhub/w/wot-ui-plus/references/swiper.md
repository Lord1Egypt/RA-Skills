# Swiper 轮播图


## 组件概况

Swiper 轮播图组件用于展示一组可滑动的图片或视频内容，支持自动播放、循环播放、多种指示器样式和自定义指示器位置。组件内置了 `wd-swiper`（轮播容器）和 `wd-swiper-nav`（指示器导航）两个子组件，通过 `indicator` 属性可以灵活配置指示器的类型和行为，满足图片轮播、视频轮播、卡片式轮播等多种业务场景需求。

## 核心功能描述

- **自动播放与循环播放**：支持自动轮播和无限循环播放，间隔时间和切换动画时长均可自定义
- **图片与视频混合轮播**：支持纯图片、纯视频或图片视频混合列表，自动识别资源类型
- **多种指示器类型**：内置 `dots`（点状）、`dots-bar`（点条状）、`fraction`（分式）三种指示器样式
- **指示器位置自定义**：支持 8 种指示器位置：`left`、`top-left`、`top`、`top-right`、`bottom-left`、`bottom`、`bottom-right`、`right`
- **卡片式边距效果**：通过 `previousMargin` 和 `nextMargin` 实现前后边距，配合 `snapToEdge` 实现卡片露边效果
- **多滑块同时展示**：通过 `displayMultipleItems` 支持同时展示多个滑块
- **视频轮播控制**：支持视频自动播放、静音播放、切换停止前一个视频、播放视频时停止自动轮播等高级控制
- **垂直方向滑动**：通过 `direction` 属性支持水平或垂直滑动方向
- **多种缓动动画**：支持 `default`、`linear`、`easeInCubic`、`easeOutCubic`、`easeInOutCubic` 五种切换动画
- **自定义指示器插槽**：通过 `#indicator` 插槽实现完全自定义指示器内容
- **自定义类名**：提供丰富的自定义类名属性，支持对指示器、图片、前后滑块、文字标题等进行样式定制
- **双向绑定**：支持 `v-model:current` 双向绑定当前滑块索引，方便外部控制切换

## 适用业务场景

- **首页 Banner 轮播**：电商平台首页活动 Banner 展示，支持自动播放和点击跳转
- **图片画廊**：相册、商品详情多图展示，支持左右滑动切换
- **视频轮播**：短视频内容推荐，自动播放当前视频并停止上一个视频
- **卡片式轮播**：推荐卡片、热门内容预览，露出前后卡片引导用户滑动
- **引导页**：应用首次启动的新手引导，关闭自动播放和循环，配合控制按钮使用
- **垂直轮播**：公告滚动、垂直切换的内容展示

## API

### Swiper Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| autoplay | boolean | true | 否 | 是否自动播放轮播图 |
| current | number | 0 | 否 | 当前轮播所在项的下标，支持 `v-model:current` 双向绑定 |
| direction | `'horizontal' \| 'vertical'` | `'horizontal'` | 否 | 轮播滑动方向 |
| displayMultipleItems | number | 1 | 否 | 同时显示的滑块数量 |
| duration | number | 300 | 否 | 滑动动画时长，单位为毫秒 |
| easingFunction | `'default' \| 'linear' \| 'easeInCubic' \| 'easeOutCubic' \| 'easeInOutCubic'` | `'default'` | 否 | 切换缓动动画类型 |
| height | number \| string | `'192'` | 否 | 轮播的高度，单位为 px |
| interval | number | 5000 | 否 | 轮播间隔时间，单位为毫秒 |
| list | `SwiperList[] \| string[]` | `[]` | 否 | 轮播数据列表，支持字符串数组或对象数组 |
| loop | boolean | true | 否 | 是否循环播放 |
| videoLoop | boolean | true | 否 | 视频是否循环播放 |
| muted | boolean | true | 否 | 视频是否静音播放 |
| nextMargin | number \| string | `'0'` | 否 | 后边距，用于卡片样式 |
| previousMargin | number \| string | `'0'` | 否 | 前边距，用于卡片样式 |
| snapToEdge | boolean | false | 否 | 是否应用边距到第一个、最后一个元素 |
| indicator | boolean \| `Partial<SwiperNavProps>` | true | 否 | 指示器配置，传 `false` 隐藏指示器，传对象可配置指示器属性 |
| imageMode | string | `'aspectFill'` | 否 | 图片裁剪、缩放的模式 |
| valueKey | string | `'value'` | 否 | 列表对象中资源地址对应的 key |
| textKey | string | `'text'` | 否 | 列表对象中标题文字对应的 key |
| autoplayVideo | boolean | true | 否 | 视频是否自动播放（切换到该滑块时自动播放） |
| stopPreviousVideo | boolean | true | 否 | 切换时是否停止上一个视频的播放 |
| stopAutoplayWhenVideoPlay | boolean | false | 否 | 视频播放时是否停止自动轮播 |
| adjustHeight | `'first' \| 'current' \| 'highest' \| 'none'` | `'highest'` | 否 | 以指定滑块高度为容器高度，仅支付宝小程序支持 |
| adjustVerticalHeight | boolean | false | 否 | vertical 为 true 时强制使 adjustHeight 生效，仅支付宝小程序支持 |
| customIndicatorClass | string | `''` | 否 | 自定义指示器类名 |
| customImageClass | string | `''` | 否 | 自定义图片类名 |
| customPrevImageClass | string | `''` | 否 | 自定义上一个图片类名 |
| customNextImageClass | string | `''` | 否 | 自定义下一个图片类名 |
| customItemClass | string | `''` | 否 | 自定义 swiper 子项类名 |
| customPrevClass | string | `''` | 否 | 自定义上一个子项类名 |
| customNextClass | string | `''` | 否 | 自定义下一个子项类名 |
| customTextClass | string | `''` | 否 | 自定义文字标题类名 |
| customTextStyle | string | `''` | 否 | 自定义文字标题样式 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

#### SwiperList 数据结构

`list` 属性支持两种数据格式：

**字符串数组**（简单场景）：

```ts
const list = [
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/video1.mp4'
]
```

组件会根据 URL 后缀自动识别图片或视频类型。

**对象数组**（复杂场景）：

```ts
const list = [
  { value: 'https://example.com/image1.jpg', type: 'image' },
  { value: 'https://example.com/video1.mp4', type: 'video', poster: 'https://example.com/cover.jpg' },
  { url: 'https://example.com/image2.jpg', title: '图片标题' }  // 配合 valueKey、textKey 使用
]
```

| 字段 | 类型 | 说明 |
|------|------|------|
| value | string | 图片或视频等资源地址（默认 key，可通过 `valueKey` 修改） |
| type | `'image' \| 'video'` | 资源文件类型，不传时自动根据 URL 识别 |
| poster | string | 视频资源的封面图地址 |

### SwiperNav Props (指示器属性)

通过 `indicator` 属性传入对象时，可配置以下指示器属性：

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| type | `'dots' \| 'dots-bar' \| 'fraction'` | `'dots'` | 否 | 指示器类型 |
| current | number | 0 | 否 | 当前轮播项下标（由组件自动传递，无需手动设置） |
| total | number | 0 | 否 | 轮播总项数（由组件自动传递，无需手动设置） |
| direction | `'horizontal' \| 'vertical'` | `'horizontal'` | 否 | 轮播滑动方向（由组件自动传递，无需手动设置） |
| indicatorPosition | `'left' \| 'top-left' \| 'top' \| 'top-right' \| 'bottom-left' \| 'bottom' \| 'bottom-right' \| 'right'` | `'bottom'` | 否 | 指示器展示位置 |
| minShowNum | number | 2 | 否 | 小于该数字时不显示指示器 |
| showControls | boolean | false | 否 | 是否显示两侧的控制按钮 |

### Swiper Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| click | `{ index: number, item: string \| SwiperList }` | 点击滑块时触发 |
| change | `{ current: number, source: string }` | 滑块切换时触发，`source` 为触发来源（`autoplay`、`touch`、`nav` 等） |
| animationfinish | `{ current: number, source: string }` | 滑块动画结束时触发 |
| update:current | `current: number` | `v-model:current` 双向绑定更新时触发 |

### SwiperNav Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | `{ dir: 'prev' \| 'next', source: string }` | 点击控制按钮切换时触发 |

### Swiper Methods

组件不对外暴露任何方法。

### Swiper Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | `{ item: string \| SwiperList, index: number }` | 自定义滑块内容，传入后可完全自定义每个滑块的渲染方式 |
| indicator | `{ current: number, total: number }` | 自定义指示器内容，传入后将替换内置指示器 |

## CSS 变量

组件通过 CSS 变量提供样式定制能力，可通过全局样式或组件父容器覆盖：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `--wot-swiper-radius` | `8px` | swiper 圆角大小 |
| `--wot-swiper-item-padding` | `0` | swiper 子项内边距 |
| `--wot-swiper-item-text-color` | `#ffffff` | swiper 子项文字颜色 |
| `--wot-swiper-item-text-fs` | `$-fs-title` | swiper 子项文字字号 |
| `--wot-swiper-nav-dot-color` | `$-font-white-2` | 指示器圆点默认颜色 |
| `--wot-swiper-nav-dot-active-color` | `$-font-white-1` | 指示器圆点激活颜色 |
| `--wot-swiper-nav-dot-size` | `12rpx` | 指示器圆点大小 |
| `--wot-swiper-nav-dots-bar-active-width` | `40rpx` | 点条状指示器激活态宽度 |
| `--wot-swiper-nav-fraction-color` | `$-font-white-1` | 分式指示器文字颜色 |
| `--wot-swiper-nav-fraction-bg-color` | `$-font-gray-3` | 分式指示器背景颜色 |
| `--wot-swiper-nav-fraction-height` | `48rpx` | 分式指示器高度 |
| `--wot-swiper-nav-fraction-font-size` | `24rpx` | 分式指示器文字大小 |
| `--wot-swiper-nav-btn-color` | `$-font-white-1` | 控制按钮箭头颜色 |
| `--wot-swiper-nav-btn-bg-color` | `$-font-gray-3` | 控制按钮背景颜色 |
| `--wot-swiper-nav-btn-size` | `48rpx` | 控制按钮大小 |

## 使用示例

### 示例 1：基本用法与指示器类型

展示三种内置指示器样式的使用方式。

```vue
<template>
  <view>
    <!-- 点状指示器 -->
    <wd-swiper
      :list="swiperList"
      autoplay
      v-model:current="current1"
      :indicator="{ type: 'dots' }"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>

    <!-- 点条状指示器 -->
    <wd-swiper
      :list="swiperList"
      autoplay
      v-model:current="current2"
      :indicator="{ type: 'dots-bar' }"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>

    <!-- 数字指示器 -->
    <wd-swiper
      :list="swiperList"
      autoplay
      v-model:current="current3"
      :indicator="{ type: 'fraction' }"
      indicator-position="bottom-right"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const swiperList = ref([
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/image3.jpg',
  'https://example.com/image4.jpg'
])

const current1 = ref(0)
const current2 = ref(0)
const current3 = ref(0)

function handleClick(e: { index: number; item: string }) {
  console.log('点击了第', e.index, '项:', e.item)
}

function onChange(e: { current: number; source: string }) {
  console.log('当前切换到第', e.current, '项，来源:', e.source)
}
</script>
```

`indicator` 属性支持三种类型：`dots`（点状，默认）、`dots-bar`（点条状，激活态会拉伸变长）、`fraction`（分式，如 `1/4`）。`indicator` 也可以传 `false` 隐藏指示器，或传 `true`（默认值）使用默认点状指示器。

### 示例 2：视频轮播

展示视频轮播的基础用法以及播放行为控制。

```vue
<template>
  <view>
    <!-- 视频自动轮播 -->
    <wd-swiper
      :list="videoList"
      autoplay
      :indicator="{ type: 'fraction' }"
      indicator-position="top-right"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>

    <!-- 手动播放视频 -->
    <wd-swiper
      :list="videoList"
      autoplay
      :autoplayVideo="false"
      :indicator="{ type: 'fraction' }"
      indicator-position="top-right"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>

    <!-- 播放视频时停止轮播 -->
    <wd-swiper
      :list="videoList"
      autoplay
      stopAutoplayWhenVideoPlay
      :autoplayVideo="false"
      :indicator="{ type: 'fraction' }"
      indicator-position="top-right"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const videoList = ref([
  'https://example.com/video1.mp4',
  'https://example.com/video2.mp4',
  'https://example.com/video3.mp4'
])

function handleClick(e: { index: number; item: string }) {
  console.log('点击了第', e.index, '项')
}

function onChange(e: { current: number; source: string }) {
  console.log('当前项:', e.current)
}
</script>
```

视频相关属性说明：

- `autoplayVideo`：默认为 `true`，切换到视频滑块时自动播放。设置为 `false` 后需要用户手动点击播放
- `stopPreviousVideo`：默认为 `true`，切换滑块时自动停止上一个视频的播放
- `stopAutoplayWhenVideoPlay`：默认为 `false`，设置为 `true` 后视频播放期间暂停自动轮播，暂停后恢复轮播
- `muted`：默认为 `true`，视频静音播放
- `videoLoop`：默认为 `true`，视频循环播放

### 示例 3：卡片样式与多滑块展示

通过前后边距实现卡片露边效果，以及同时展示多个滑块。

```vue
<template>
  <view>
    <!-- 卡片样式 -->
    <view class="card-swiper">
      <wd-swiper
        autoplay
        v-model:current="current1"
        custom-indicator-class="custom-indicator-class"
        custom-image-class="custom-image"
        custom-next-image-class="custom-image-prev"
        custom-prev-image-class="custom-image-prev"
        :indicator="{ type: 'dots' }"
        :list="swiperList"
        previousMargin="24px"
        nextMargin="24px"
      ></wd-swiper>
    </view>

    <!-- 同时展示 2 个滑块 -->
    <view class="card-swiper">
      <wd-swiper
        autoplay
        v-model:current="current2"
        :display-multiple-items="2"
        custom-indicator-class="custom-indicator-class"
        custom-image-class="custom-image"
        custom-next-image-class="custom-image-prev"
        custom-prev-image-class="custom-image-prev"
        :indicator="{ type: 'dots' }"
        :list="swiperList"
        previousMargin="24px"
        nextMargin="24px"
      ></wd-swiper>
    </view>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const swiperList = ref([
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/image3.jpg',
  'https://example.com/image4.jpg',
  'https://example.com/image5.jpg'
])

const current1 = ref(0)
const current2 = ref(0)
</script>
<style lang="scss" scoped>
.card-swiper {
  --wot-swiper-radius: 0;
  --wot-swiper-item-padding: 0 24rpx;
  --wot-swiper-nav-dot-color: #e7e7e7;
  --wot-swiper-nav-dot-active-color: #4d80f0;
  padding-bottom: 24rpx;

  :deep(.custom-indicator-class) {
    bottom: -16px;
  }

  :deep(.custom-image) {
    border-radius: 12rpx;
  }

  :deep(.custom-image-prev) {
    height: 168px !important;
  }
}
</style>
```

卡片效果实现要点：

- `previousMargin` 和 `nextMargin` 分别设置前后滑块的边距，使前后滑块部分可见
- `customPrevImageClass` 和 `customNextImageClass` 用于为前后滑块添加自定义样式（如缩小高度）
- `customImageClass` 为当前滑块添加圆角等样式
- `displayMultipleItems` 控制同时展示的滑块数量
- 通过 CSS 变量可覆盖圆角、内边距等基础样式

### 示例 4：垂直方向与手动切换

展示垂直滑动方向以及带控制按钮的手动切换效果。

```vue
<template>
  <view>
    <!-- 垂直方向 -->
    <wd-swiper
      :list="swiperList"
      direction="vertical"
      indicator-position="right"
      autoplay
      v-model:current="current1"
      :indicator="{ type: 'dots-bar' }"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>

    <!-- 手动切换（带控制按钮） -->
    <wd-swiper
      :list="swiperList"
      :autoplay="false"
      v-model:current="current2"
      :indicator="{ showControls: true }"
      :loop="false"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const swiperList = ref([
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/image3.jpg',
  'https://example.com/image4.jpg'
])

const current1 = ref(0)
const current2 = ref(0)

function handleClick(e: { index: number; item: string }) {
  console.log('点击了第', e.index, '项')
}

function onChange(e: { current: number; source: string }) {
  console.log('当前项:', e.current)
}
</script>
```

垂直轮播通过 `direction="vertical"` 启用，指示器位置建议配合使用 `left` 或 `right`。手动切换场景建议设置 `autoplay="false"` 关闭自动播放，`loop="false"` 关闭循环，`showControls: true` 显示左右切换按钮。

### 示例 5：自定义指示器插槽

通过插槽实现完全自定义的指示器内容。

```vue
<template>
  <view>
    <wd-swiper
      :list="swiperList"
      autoplay
      v-model:current="current"
      @click="handleClick"
      @change="onChange"
    >
      <!-- 自定义指示器 -->
      <template #indicator="{ current, total }">
        <view class="custom-indicator">
          {{ current + 1 }}/{{ total }}
        </view>
      </template>
    </wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const swiperList = ref([
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/image3.jpg'
])

const current = ref(0)

function handleClick(e: { index: number; item: string }) {
  console.log('点击了第', e.index, '项')
}

function onChange(e: { current: number; source: string }) {
  console.log('当前项:', e.current)
}
</script>
<style lang="scss" scoped>
.custom-indicator {
  position: absolute;
  bottom: 24rpx;
  right: 24rpx;
  padding: 0 12rpx;
  height: 48rpx;
  line-height: 48rpx;
  border-radius: 45%;
  background: rgba(0, 0, 0, 0.6);
  color: #ffffff;
  font-size: 24rpx;
}
</style>
```

使用 `#indicator` 插槽后，组件内置的指示器将被替换。插槽作用域中提供 `current`（当前项索引，从 0 开始）和 `total`（总项数）。

### 示例 6：自定义数据字段

通过 `valueKey` 和 `textKey` 适配自定义数据结构。

```vue
<template>
  <view>
    <wd-swiper
      value-key="url"
      text-key="title"
      :list="customSwiperList"
      autoplay
      v-model:current="current"
      @click="handleClick"
      @change="onChange"
    ></wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

// 自定义字段名：url 作为图片地址，title 作为文字标题
const customSwiperList = ref([
  { url: 'https://example.com/image1.jpg', title: '图片标题一' },
  { url: 'https://example.com/image2.jpg', title: '图片标题二' },
  { url: 'https://example.com/image3.jpg', title: '图片标题三' },
  { url: 'https://example.com/image4.jpg', title: '图片标题四' }
])

const current = ref(0)

function handleClick(e: { index: number; item: any }) {
  console.log('点击了第', e.index, '项:', e.item.title)
}

function onChange(e: { current: number; source: string }) {
  console.log('当前项:', e.current)
}
</script>
```

默认情况下，组件期望对象数据中的图片地址字段为 `value`，文字标题字段为 `text`。当后端返回的数据字段名不一致时，可通过 `valueKey` 和 `textKey` 指定对应字段名。文字标题默认显示在右上角，可通过 `customTextClass` 和 `customTextStyle` 自定义样式。

### 示例 7：默认插槽自定义内容

使用默认插槽完全自定义滑块内容。

```vue
<template>
  <view>
    <wd-swiper
      :list="swiperList"
      autoplay
      v-model:current="current"
      :indicator="{ type: 'dots-bar' }"
      @click="handleClick"
      @change="onChange"
    >
      <template #default="{ item, index }">
        <!-- 完全自定义滑块内容 -->
        <view class="custom-slide">
          <image
            :src="item as string"
            mode="aspectFill"
            style="width: 100%; height: 100%"
          />
          <view class="slide-overlay">
            <text>自定义遮罩层 - 第 {{ index + 1 }} 张</text>
          </view>
        </view>
      </template>
    </wd-swiper>
  </view>
</template>
<script lang="ts" setup>
import { ref } from 'vue'

const swiperList = ref([
  'https://example.com/image1.jpg',
  'https://example.com/image2.jpg',
  'https://example.com/image3.jpg'
])

const current = ref(0)

function handleClick(e: { index: number; item: string }) {
  console.log('点击了第', e.index, '项')
}

function onChange(e: { current: number; source: string }) {
  console.log('当前项:', e.current)
}
</script>
<style lang="scss" scoped>
.custom-slide {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24rpx;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  color: #ffffff;
  font-size: 28rpx;
}
</style>
```

使用 `#default` 插槽后，组件将不再渲染内置的 `<image>` 或 `<video>` 元素，完全由插槽内容决定滑块的展示方式。插槽作用域中提供 `item`（当前项数据）和 `index`（当前项索引）。

## 注意事项

1. **指示器优先级**：当使用 `#indicator` 插槽时，内置指示器（包括通过 `indicator` 属性配置的指示器）将被完全替换，`indicator` 属性中的配置对自定义指示器不生效
2. **视频播放行为**：`autoplayVideo` 控制切换到视频滑块时是否自动播放；`stopPreviousVideo` 控制切换时是否停止上一个视频；`stopAutoplayWhenVideoPlay` 控制视频播放期间是否暂停自动轮播。三者配合使用可实现精细的视频播放控制
3. **边距与 snapToEdge**：`previousMargin` 和 `nextMargin` 默认不对第一个和最后一个元素生效，设置 `snapToEdge="true"` 后可使边距对所有元素生效
4. **高度单位**：`height` 属性传入数字时单位为 px，传入字符串时支持 `px`、`rpx`、`vh` 等单位，如 `192` 或 `'192px'` 或 `'384rpx'`
5. **current 越界处理**：当通过 `v-model:current` 或 `current` 属性传入的索引小于 0 时，若 `loop` 为 `true` 则跳转到最后一项，否则跳转到第一项；大于等于列表长度时，若 `loop` 为 `true` 则跳转到第一项，否则跳转到最后一项
6. **list 数据变化**：`list` 数据变化时组件会自动更新，但需要注意 Vue 3 中数组的响应式更新应使用 `ref` 或 `reactive` 包裹
7. **自定义类名使用**：`customPrevImageClass` 和 `customNextImageClass` 仅对前一个和后一个滑块生效（基于当前滑块计算），适用于卡片式轮播中缩小前后滑块的场景
8. **微信小程序 scroll-view 包裹**：在微信小程序平台，swiper 组件会被 `<scroll-view>` 包裹，这是为了解决特定平台问题，不影响正常使用
9. **adjustHeight 平台限制**：`adjustHeight` 和 `adjustVerticalHeight` 属性仅在支付宝小程序中生效，其他平台不支持
