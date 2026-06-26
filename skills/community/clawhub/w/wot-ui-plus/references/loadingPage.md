# LoadingPage 页面加载


## 组件概况

LoadingPage 页面加载组件是一个全屏页面级别的加载指示器组件，用于在页面数据加载、初始化或其他耗时操作期间向用户展示加载状态。该组件基于 `wd-transition` 过渡动画实现，通过 fixed 定位覆盖整个页面区域，内置加载动画图标和提示文字，支持自定义图片、动画类型、背景色、字体颜色等选项，为用户提供明确的加载状态反馈。

组件内部使用 `wd-loading` 组件展示加载动画，支持 `outline`（圆形）和 `ring`（半圆形）两种加载动画模式，同时支持使用自定义图片替代默认加载动画。通过 `v-model` 或 `loading` 属性控制加载状态的显示与隐藏，并带有平滑的过渡动画效果。

## 核心功能描述

- **全屏覆盖加载**：使用 fixed 定位覆盖整个页面区域，阻止用户操作底层内容
- **两种加载动画**：支持 `outline`（圆形）和 `ring`（半圆形）两种内置加载动画模式
- **自定义图片**：支持传入自定义图片替代默认加载动画，适用于品牌定制化场景
- **平滑过渡动画**：基于 `wd-transition` 实现淡入淡出的过渡动画，显示和隐藏时过渡自然
- **背景色自定义**：支持设置全屏背景色，默认白色，可设置为半透明遮罩效果
- **提示文案自定义**：支持自定义加载提示文字内容、字体大小和颜色
- **加载图标尺寸**：支持自定义加载动画图标的大小
- **加载图标颜色**：支持自定义加载动画的颜色
- **层级控制**：通过 `zIndex` 属性控制加载层的堆叠顺序
- **默认插槽**：支持通过默认插槽完全自定义加载内容区域

## 适用业务场景

- **页面初始化**：应用启动或页面首次加载时展示全屏加载动画，数据加载完成后隐藏
- **数据请求**：页面发起异步数据请求时展示加载状态，请求完成后隐藏
- **长时操作**：执行数据同步、文件上传下载等耗时操作时展示加载提示
- **品牌定制**：使用自定义图片展示品牌 Logo 加载动画，提升品牌识别度
- **半透明遮罩**：设置半透明背景色，在展示加载状态的同时隐约显示底层页面内容
- **全屏操作锁定**：在关键操作进行中时防止用户误触其他操作区域

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| text | string | '加载中' | 否 | 提示内容，显示在加载动画下方 |
| image | string | '' | 否 | 自定义加载图标，传入图片地址时使用图片替代默认加载动画 |
| type | 'outline' \| 'ring' | 'ring' | 否 | 加载动画模式，`outline` 为圆形，`ring` 为半圆形 |
| loading | boolean | false | 否 | 是否显示加载动画，控制组件的显示与隐藏 |
| bgColor | string | '#ffffff' | 否 | 页面背景颜色，默认为白色 |
| color | string | '#C8C8C8' | 否 | 提示文字字体颜色 |
| fontSize | number \| string | 19 | 否 | 提示文字字体大小，支持数字（默认 px）或带单位的字符串 |
| iconSize | number \| string | 28 | 否 | 自定义加载图标大小，支持数字（默认 px）或带单位的字符串 |
| loadingColor | string | '#C8C8C8' | 否 | 加载动画颜色，仅对内置动画有效 |
| zIndex | number \| string | 10 | 否 | 加载动画层级（z-index） |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

当前组件未定义自定义事件。组件的显示与隐藏通过 `loading` 属性控制。

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 自定义加载内容区域，替代默认的加载动画和提示文字组合，可插入自定义加载组件或图文组合 |

## 使用示例

### 示例 1：基本用法

效果说明：最基础的页面加载用法。通过 `loading` 属性控制显示与隐藏，使用默认的半圆形加载动画和"加载中"提示文字。点击按钮显示加载状态，1 秒后自动隐藏。

```vue
<template>
  <page-wraper>
    <view class="container">
      <demo-block title="基本用法">
        <wd-button type="primary" @click="showLoading">显示加载</wd-button>
      </demo-block>
      <wd-loading-page :loading="show" />
    </view>
  </page-wraper>
</template>

<script setup lang="ts">
import wdLoadingPage from '@/uni_modules/wot-ui-plus/components/wd-loading-page/wd-loading-page.vue'
import { ref } from 'vue'

const show = ref(false)

function showLoading() {
  show.value = true
  setTimeout(() => {
    show.value = false
  }, 1000)
}
</script>
```

### 示例 2：自定义加载动画模式和文字

效果说明：展示自定义加载动画模式、文字内容、文字颜色和动画颜色。通过 `loadingMode` 设置动画类型，通过 `loadingText` 设置提示文字。

```vue
<template>
  <page-wraper>
    <view class="container">
      <demo-block title="自定义加载动画模式">
        <wd-button type="primary" @click="showCustomMode">显示加载</wd-button>
      </demo-block>
      <wd-loading-page :loading="show" :text="loadingText" :type="loadingMode" :color="textColor" :loading-color="loadingColor" />
    </view>
  </page-wraper>
</template>

<script setup lang="ts">
import wdLoadingPage from '@/uni_modules/wot-ui-plus/components/wd-loading-page/wd-loading-page.vue'
import { ref } from 'vue'
import type { LoadingType } from '@/uni_modules/wot-ui-plus/components/wd-loading-page/types'

const show = ref(false)
const loadingText = ref('Hello Wot')
const loadingMode = ref<LoadingType>('semicircle')
const textColor = ref('#C8C8C8')
const loadingColor = ref('#C8C8C8')

function showCustomMode() {
  loadingText.value = 'Hello Wot'
  loadingMode.value = 'semicircle'
  textColor.value = '#C8C8C8'
  loadingColor.value = '#C8C8C8'
  show.value = true
  setTimeout(() => {
    show.value = false
  }, 1000)
}
</script>
```

### 示例 3：自定义图片

效果说明：使用自定义图片替代默认加载动画，适用于品牌定制化场景。通过 `image` 属性传入图片地址，同时可自定义图标尺寸和提示文字。

```vue
<template>
  <page-wraper>
    <view class="container">
      <demo-block title="自定义图片">
        <wd-button type="primary" @click="showWithImage">显示加载</wd-button>
      </demo-block>
      <wd-loading-page
        :loading="show"
        :image="customImage"
        :icon-size="iconSize"
        :text="loadingText"
        :color="textColor"
      />
    </view>
  </page-wraper>
</template>

<script setup lang="ts">
import wdLoadingPage from '@/uni_modules/wot-ui-plus/components/wd-loading-page/wd-loading-page.vue'
import { ref } from 'vue'

const show = ref(false)
const customImage = ref('../../static/icon/app.png')
const iconSize = ref(40)
const loadingText = ref('Wot UI Plus')
const textColor = ref('#C8C8C8')

function showWithImage() {
  customImage.value = '../../static/icon/app.png'
  iconSize.value = 40
  loadingText.value = 'Wot UI Plus'
  textColor.value = '#C8C8C8'
  show.value = true
  setTimeout(() => {
    show.value = false
  }, 1000)
}
</script>
```

### 示例 4：自定义背景色

效果说明：通过 `bgColor` 属性设置半透明背景色，在展示加载状态的同时隐约显示底层页面内容。适用于需要保留页面可见性的加载场景。

```vue
<template>
  <page-wraper>
    <view class="container">
      <demo-block title="自定义背景色">
        <wd-button type="primary" @click="showWithBgColor">显示加载</wd-button>
      </demo-block>
      <wd-loading-page
        :loading="show"
        :bg-color="bgColor"
        :type="loadingMode"
        :text="loadingText"
        :color="textColor"
        :loading-color="loadingColor"
      />
    </view>
  </page-wraper>
</template>

<script setup lang="ts">
import wdLoadingPage from '@/uni_modules/wot-ui-plus/components/wd-loading-page/wd-loading-page.vue'
import { ref } from 'vue'
import type { LoadingType } from '@/uni_modules/wot-ui-plus/components/wd-loading-page/types'

const show = ref(false)
const bgColor = ref('rgba(0, 0, 0, 0.3)')
const loadingMode = ref<LoadingType>('outline')
const loadingText = ref('Wot UI Plus')
const textColor = ref('#eee')
const loadingColor = ref('#ddd')

function showWithBgColor() {
  bgColor.value = 'rgba(0, 0, 0, 0.3)'
  loadingMode.value = 'outline'
  loadingText.value = 'Wot UI Plus'
  textColor.value = '#eee'
  loadingColor.value = '#ddd'
  show.value = true
  setTimeout(() => {
    show.value = false
  }, 1000)
}
</script>
```

### 示例 5：在异步请求中使用

效果说明：在实际业务场景中，页面加载组件通常配合异步请求使用。在请求发起时显示加载状态，请求完成后隐藏。

```vue
<template>
  <page-wraper>
    <view class="container">
      <demo-block title="异步请求加载">
        <wd-button type="primary" @click="fetchData">获取数据</wd-button>
      </demo-block>
      <wd-loading-page
        :loading="isLoading"
        text="数据加载中..."
        type="ring"
        :bg-color="'rgba(255, 255, 255, 0.9)'"
      />
      <view v-if="dataList.length > 0">
        <view v-for="item in dataList" :key="item.id">{{ item.name }}</view>
      </view>
    </view>
  </page-wraper>
</template>

<script setup lang="ts">
import wdLoadingPage from '@/uni_modules/wot-ui-plus/components/wd-loading-page/wd-loading-page.vue'
import { ref } from 'vue'

const isLoading = ref(false)
const dataList = ref<any[]>([])

async function fetchData() {
  isLoading.value = true
  try {
    // 模拟异步请求
    await new Promise((resolve) => setTimeout(resolve, 2000))
    dataList.value = [
      { id: 1, name: '数据项1' },
      { id: 2, name: '数据项2' },
      { id: 3, name: '数据项3' }
    ]
  } catch (error) {
    console.error('数据加载失败', error)
  } finally {
    isLoading.value = false
  }
}
</script>
```

## 注意事项

1. **loading 属性控制显隐**：组件的显示与隐藏完全由 `loading` 属性控制，设置为 `true` 时显示加载层并带有淡入动画，设置为 `false` 时隐藏加载层并带有淡出动画。

2. **image 优先级高于 type**：当同时设置 `image` 和 `type` 时，如果 `image` 不为空，则优先使用自定义图片，`type` 属性不生效。

3. **全屏 fixed 定位**：组件使用 fixed 定位覆盖整个视口区域（top: 0, left: 0, right: 0, bottom: 0），确保加载层始终覆盖全屏。在小程序等平台上，如遇到 fixed 定位异常，可考虑使用 `rootPortal` 方案。

4. **过渡动画实现**：组件内部使用 `wd-transition` 的 fade 淡入淡出动画实现显示和隐藏的过渡效果，动画时长由 `wd-transition` 默认控制。

5. **背景色半透明效果**：当使用半透明背景色（如 `rgba(0, 0, 0, 0.3)`）时，用户仍可隐约看到底层页面内容，适用于需要保留页面上下文的加载场景。

6. **图标尺寸单位**：`fontSize` 和 `iconSize` 属性支持传入数字（默认 px）或带单位的字符串（如 `'20px'`、`'1.2rem'`），组件内部使用 `addUnit` 函数进行单位处理。

7. **加载颜色限制**：`loadingColor` 属性仅对内置的 `wd-loading` 组件有效，传入自定义图片时无效。加载颜色使用十六进制色值。

8. **自定义插槽内容**：使用默认插槽时，会完全替代默认的加载动画和提示文字组合，此时 `image`、`text`、`type`、`loadingColor` 等属性不再生效，需自行实现加载内容。

9. **层级设置**：`zIndex` 默认值为 10，如有多个浮层组件同时存在，需合理设置各组件的 `zIndex` 值确保加载层显示在最上层。

10. **性能考虑**：加载层在 `loading` 为 `false` 时虽然不可见，但组件仍然存在于 DOM 中。如需在隐藏时完全销毁组件，可使用 `v-if` 替代 `loading` 属性控制。
