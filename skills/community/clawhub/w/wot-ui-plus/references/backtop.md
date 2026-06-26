# Backtop 回到顶部


## 组件概况

Backtop（回到顶部）组件是一个用于长页面滚动场景的导航辅助组件。当用户滚动页面到底部或指定位置时，该组件会以固定定位的方式出现在页面右下角，提供快速返回页面顶部的交互入口。组件采用淡入淡出的过渡动画显示/隐藏，支持圆形和方形两种外观形态，并允许通过插槽自定义内容，适用于需要频繁返回顶部位置的信息流、列表页、文章详情页等场景。

## 核心功能描述

- **滚动监听显示**：通过传入页面的 scrollTop 值，结合 top 阈值属性自动计算是否显示按钮，当滚动距离超过设定值时触发淡入显示
- **平滑返回顶部**：点击按钮后调用 uni.pageScrollTo API 实现平滑滚动至页面顶部，支持自定义滚动动画时长
- **位置自定义**：支持通过 bottom 和 right 属性精确控制按钮距离屏幕底部和右侧的像素距离
- **外观形态切换**：提供 circle（圆形）和 square（方形）两种形状选项，圆形默认圆角 50%，方形圆角 4px
- **内容完全定制**：通过默认插槽可完全替换默认的返回顶部图标，支持传入文字、图片等任意内容
- **层级控制**：通过 zIndex 属性控制组件在页面中的堆叠层级，确保按钮显示在最上层不被遮挡

## 适用业务场景

- **信息流列表页**：在电商商品列表、社交动态流等长页面场景中，用户浏览到底部后可快速返回顶部进行筛选或搜索操作
- **文章/详情页**：在阅读长篇文章、产品详情、帮助文档等页面时，提供便捷的返回顶部入口提升浏览体验
- **数据报表页**：在包含大量数据表格或图表的管理后台页面中，帮助用户快速回到顶部查看表头或操作按钮

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| scrollTop | number | - | 是 | 页面滚动距离，通常由 onPageScroll 事件获取并传入 |
| top | number | 300 | 否 | 距离顶部多少距离时显示按钮，单位为 px |
| duration | number | 100 | 否 | 返回顶部滚动动画的持续时间，单位为 ms |
| zIndex | number | 10 | 否 | 组件的层级堆叠顺序，值越大越靠前 |
| iconStyle | string | '' | 否 | 内部图标的自定义样式，仅在未使用默认插槽时生效 |
| shape | string | 'circle' | 否 | 按钮形状，可选值为 'circle'（圆形）或 'square'（方形） |
| bottom | number | 100 | 否 | 按钮距离屏幕底部的距离，单位为 px |
| right | number | 20 | 否 | 按钮距离屏幕右侧的距离，单位为 px |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Events

当前源码中未显式对外派发自定义事件。

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 用于自定义按钮内容，默认显示返回顶部图标，传入后可完全替换图标展示 |

## 使用示例

### 示例 1：基础用法

效果说明：展示组件的最小接入方式，通过 onPageScroll 监听页面滚动并传入 scrollTop，当滚动超过 300px 时自动显示圆形回到顶部按钮。

```vue
<template>
  <wd-backtop :scrollTop="scrollTop"></wd-backtop>
  <view style="height: 2000px;"></view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onPageScroll } from '@dcloudio/uni-app'

const scrollTop = ref(0)
onPageScroll((e) => {
  scrollTop.value = e.scrollTop
})
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 2：方形按钮与自定义显示距离

效果说明：将按钮形状改为方形，并调整显示阈值为 600px，适合页面较长且不希望过早显示按钮的场景。

```vue
<template>
  <wd-backtop :scrollTop="scrollTop" shape="square" :top="600"></wd-backtop>
  <view style="height: 3000px;"></view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onPageScroll } from '@dcloudio/uni-app'

const scrollTop = ref(0)
onPageScroll((e) => {
  scrollTop.value = e.scrollTop
})
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

### 示例 3：自定义内容与样式

效果说明：通过默认插槽完全替换按钮内容，使用文字 "TOP" 代替默认图标，并通过 customStyle 自定义背景色和文字颜色。

```vue
<template>
  <wd-backtop
    :scrollTop="scrollTop"
    customStyle="background: #007aff; color: white;"
  >
    <text style="color: white;">TOP</text>
  </wd-backtop>
  <view style="height: 2000px;"></view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onPageScroll } from '@dcloudio/uni-app'

const scrollTop = ref(0)
onPageScroll((e) => {
  scrollTop.value = e.scrollTop
})
</script>

<style scoped lang="scss">
/* 本示例无需额外样式。 */
</style>
```

## 注意事项

- **必须传入 scrollTop**：scrollTop 是必填属性，组件依赖该值判断是否显示。请在页面中使用 onPageScroll 钩子实时获取滚动距离并传入，否则按钮将始终隐藏。
- **固定定位布局**：组件使用 fixed 定位，默认距离底部 100px、右侧 20px。如需调整位置，请通过 bottom 和 right 属性设置，避免使用外部 CSS 覆盖定位属性。
- **滚动 API 限制**：组件内部使用 uni.pageScrollTo 实现滚动返回顶部，该 API 在不同平台（H5、小程序、App）的行为可能略有差异，建议在目标平台进行充分测试。
- **插槽使用时机**：当传入默认插槽内容时，内部的 wd-icon 图标组件将完全被替换，此时 iconStyle 属性不再生效，需在插槽内容中自行处理样式。
- **zIndex 层级建议**：默认 zIndex 为 10，若页面中存在其他固定定位元素（如弹窗、导航栏等），请根据实际层级关系调整该值确保按钮可见。
- **性能优化建议**：onPageScroll 事件触发频率较高，建议在滚动回调中直接赋值响应式变量即可，避免在回调中执行额外计算逻辑影响页面滚动性能。
