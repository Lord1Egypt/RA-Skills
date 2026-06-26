# Curtain 幕帘


## 组件概况

Curtain 幕帘组件是一个用于在页面中展示营销推广图片的浮层组件，通常用于活动推广、广告弹窗等场景。该组件基于 wd-popup 弹窗组件实现，通过 `zoom-in` 动画从中心放大展示幕帘图片，支持点击遮罩关闭、点击图片跳转链接、自定义关闭按钮位置等功能。

幕帘组件采用透明背景的 Popup 容器，内部包含一张图片（通过 `image` 标签渲染）和一个关闭按钮（默认为 `wd-icon` 图标），支持多种关闭按钮位置预设以及自定义关闭按钮插槽，满足各类推广弹窗的视觉需求。

## 核心功能描述

- **幕帘图片展示**：通过 `src` 属性传入网络图片地址，组件自动按图片原始宽高比进行等比缩放展示
- **宽度控制**：通过 `width` 属性设置幕帘图片宽度（单位 px），高度会根据图片原始比例自动计算
- **点击跳转**：通过 `to` 属性设置点击幕帘图片后的跳转链接地址，点击后自动调用 `uni.navigateTo` 导航
- **关闭按钮**：内置关闭按钮，支持多种位置预设（`inset` / `top` / `bottom` / `top-left` / `top-right` / `bottom-left` / `bottom-right`），默认位于图片内部右上角
- **自定义关闭按钮**：通过 `close` 插槽可完全替换默认的关闭图标，实现自定义样式的关闭按钮
- **点击关闭**：支持点击图片关闭幕帘（`closeOnClick`）、点击遮罩层关闭幕帘（`closeOnClickModal`）两种关闭方式
- **弹窗动画**：基于 wd-popup 的 `zoom-in` 过渡动画，从中心放大展示幕帘
- **层级控制**：通过 `zIndex` 属性控制幕帘的层级堆叠顺序
- **平台兼容**：支持通过 `rootPortal` 属性将幕帘从页面中脱离，解决 H5 / APP / 小程序平台下 fixed 定位失效问题
- **小程序码识别**：通过 `showMenuByLongpress` 属性开启长按图片显示识别小程序码菜单（仅微信小程序平台有效）

## 适用业务场景

- **活动推广弹窗**：在首页展示限时促销、新品上市等营销活动的推广幕帘
- **广告弹窗**：展示品牌广告、合作推广等全屏或半屏广告内容
- **引导浮层**：在用户首次使用时展示功能引导、操作说明等引导幕帘
- **版本更新通知**：展示应用版本更新内容，引导用户跳转更新页面
- **会员推广**：展示会员权益、优惠券领取等营销推广信息

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| modelValue / v-model | boolean | false | 否 | 绑定值，控制幕帘的展示/关闭状态。推荐使用 `v-model` 进行双向绑定 |
| value | boolean | false | 否 | 绑定值，控制幕帘的展示/关闭状态（已废弃，请使用 modelValue） |
| src | string | - | 否 | 幕帘图片地址，必须使用网络地址 |
| to | string | - | 否 | 幕帘图片点击后的跳转链接地址，点击后通过 `uni.navigateTo` 进行页面跳转 |
| width | number | - | 否 | 幕帘图片宽度，单位为 px。设置后高度会根据图片原始比例自动计算 |
| closePosition | string | 'inset' | 否 | 关闭按钮的位置，可选值：`inset` / `top` / `bottom` / `top-left` / `top-right` / `bottom-left` / `bottom-right` |
| closeOnClickModal | boolean | false | 否 | 是否点击遮罩层关闭幕帘 |
| closeOnClick | boolean | true | 否 | 点击图片是否关闭幕帘，默认为 true |
| hideWhenClose | boolean | true | 否 | 关闭时是否将弹出层隐藏（display: none） |
| zIndex | number | 10 | 否 | 幕帘的层级堆叠顺序，值越大越靠前显示 |
| customCloseClass | string | '' | 否 | 自定义关闭按钮的样式类名 |
| customCloseStyle | string | '' | 否 | 自定义关闭按钮的内联样式 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） |
| showMenuByLongpress | boolean | false | 否 | 开启长按图片显示识别小程序码菜单，仅在微信小程序平台有效 |
| customStyle | string | '' | 否 | 自定义组件根元素的内联样式 |
| customClass | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| beforeenter | - | 幕帘进入动画开始前触发 |
| enter | - | 幕帘进入动画进行中触发 |
| afterenter | - | 幕帘进入动画结束后触发 |
| beforeleave | - | 幕帘离开动画开始前触发 |
| leave | - | 幕帘离开动画进行中触发 |
| afterleave | - | 幕帘离开动画结束后触发 |
| close | - | 幕帘关闭时触发 |
| closed | - | 幕帘完全关闭后触发 |
| click-modal | - | 点击遮罩层时触发 |
| click | - | 点击幕帘图片时触发 |
| load | - | 幕帘图片加载成功时触发 |
| error | - | 幕帘图片加载失败时触发 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| close | - | 自定义关闭按钮，用于替换默认的 `wd-icon` 关闭图标 |

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-curtain-wrapper | 幕帘容器根节点样式类 |
| wd-curtain | Popup 组件根节点样式类，可用于设置圆角、透明背景等 |
| wd-curtain\_\_content | 幕帘内容区域样式类 |
| wd-curtain\_\_content-img | 幕帘图片样式类 |
| wd-curtain\_\_content-close | 关闭按钮样式类，可结合位置类名（如 `top-left`、`bottom-right` 等）进行样式覆盖 |

## 使用示例

### 示例 1：基础用法

效果说明：展示幕帘组件的基本使用方式，通过 `v-model` 控制幕帘的显示与隐藏，配置图片地址、跳转链接和图片宽度。关闭按钮默认显示在图片内部右上角（`inset` 模式）。

```vue
<template>
  <wd-button type="primary" @click="show = true">显示幕帘</wd-button>

  <wd-curtain
    v-model="show"
    :src="imageUrl"
    :to="'/pages/activity/index'"
    :width="280"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const imageUrl = ref<string>(
  'https://img20.360buyimg.com/da/jfs/t1/141592/25/8861/261559/5f68d8c1E33ed78ab/698ad655bfcfbaed.png'
)
</script>
```

### 示例 2：自定义关闭按钮位置

效果说明：通过 `closePosition` 属性设置关闭按钮的不同位置。支持 7 种预设位置：`inset`（内部默认）、`top`（顶部居中）、`bottom`（底部居中）、`top-left`（左上角）、`top-right`（右上角）、`bottom-left`（左下角）、`bottom-right`（右下角）。

```vue
<template>
  <view class="btn-group">
    <wd-button @click="openCurtain('top-left')">左上</wd-button>
    <wd-button @click="openCurtain('top')">顶部居中</wd-button>
    <wd-button @click="openCurtain('top-right')">右上</wd-button>
    <wd-button @click="openCurtain('bottom-left')">左下</wd-button>
    <wd-button @click="openCurtain('bottom')">底部居中</wd-button>
    <wd-button @click="openCurtain('bottom-right')">右下</wd-button>
  </view>

  <wd-curtain
    v-model="show"
    :src="imageUrl"
    :to="'/pages/activity/index'"
    :close-position="closePosition"
    :width="240"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ClosePosition } from 'wot-design-uni/components/wd-curtain/types'

const show = ref<boolean>(false)
const closePosition = ref<ClosePosition>('inset')
const imageUrl = ref<string>(
  'https://img20.360buyimg.com/da/jfs/t1/141592/25/8861/261559/5f68d8c1E33ed78ab/698ad655bfcfbaed.png'
)

function openCurtain(position: ClosePosition) {
  closePosition.value = position
  show.value = true
}
</script>

<style scoped lang="scss">
.btn-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
```

### 示例 3：点击遮罩关闭

效果说明：通过设置 `close-on-click-modal` 为 `true`，允许用户点击幕帘图片外的遮罩层区域来关闭幕帘。适用于需要更灵活关闭方式的场景。

```vue
<template>
  <wd-button type="primary" @click="show = true">点击遮罩关闭</wd-button>

  <wd-curtain
    v-model="show"
    :src="imageUrl"
    :to="'/pages/activity/index'"
    :width="240"
    close-position="bottom-right"
    :close-on-click-modal="true"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const imageUrl = ref<string>(
  'https://img20.360buyimg.com/da/jfs/t1/141592/25/8861/261559/5f68d8c1E33ed78ab/698ad655bfcfbaed.png'
)
</script>
```

### 示例 4：自定义关闭按钮

效果说明：通过 `close` 插槽完全替换默认的关闭图标，实现自定义样式的关闭按钮。插槽内容需要自行处理定位和点击关闭逻辑。

```vue
<template>
  <wd-button type="primary" @click="show = true">自定义关闭按钮</wd-button>

  <wd-curtain v-model="show" :src="imageUrl" :width="280">
    <template #close>
      <view class="custom-close" @click="show = false">关闭</view>
    </template>
  </wd-curtain>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref<boolean>(false)
const imageUrl = ref<string>(
  'https://img20.360buyimg.com/da/jfs/t1/141592/25/8861/261559/5f68d8c1E33ed78ab/698ad655bfcfbaed.png'
)
</script>

<style scoped lang="scss">
.custom-close {
  position: absolute;
  top: 10px;
  right: 10px;
  color: #ffffff;
  font-size: 32rpx;
  padding: 6px;
}
</style>
```

## 注意事项

1. **图片地址要求**：`src` 属性必须使用网络图片地址。如果传入本地路径可能导致图片无法正常加载。

2. **宽高比自动计算**：当设置 `width` 属性后，组件会在图片加载成功后根据图片原始宽高比自动计算高度，确保图片不变形。高度计算公式为：`height = width / (原始宽度 / 原始高度)`。

3. **点击行为**：默认情况下，点击幕帘图片会关闭幕帘（`closeOnClick: true`）。如果设置了 `to` 属性，点击后会先执行页面跳转再关闭幕帘。若需要点击图片不关闭，请将 `closeOnClick` 设为 `false`。

4. **关闭按钮位置预设**：`closePosition` 的 7 种预设位置中，`inset` 表示关闭按钮位于图片内部右上角（默认值）。其他 6 种位置均位于图片外部，通过绝对定位实现，需要在图片周围预留足够空间以避免被裁剪。

5. **跳转链接**：`to` 属性配置的跳转地址将通过 `uni.navigateTo` 执行，需确保目标页面已注册在路由配置中。如需其他跳转方式（如 `uni.redirectTo`、`uni.switchTab`），请监听 `click` 事件自行处理。

6. **层级规划**：幕帘默认 `zIndex` 为 10。若页面中存在其他浮层组件（如 Toast、Dialog 等），请合理调整 `zIndex` 值确保幕帘显示在正确层级。

7. **rootPortal 使用**：当幕帘在嵌套滚动容器或特殊布局中显示异常时，可设置 `rootPortal: true` 将幕帘脱离当前 DOM 层级渲染，解决 fixed 定位失效问题。该功能在 H5 平台使用 `teleport`、APP 平台使用 `renderjs`、小程序平台使用 `root-portal` 实现。

8. **小程序码识别**：`showMenuByLongpress` 属性仅在微信小程序平台有效，开启后长按幕帘图片会弹出"识别小程序码"菜单。其他平台此属性不产生效果。

9. **动画事件**：幕帘进入/离开动画提供 6 个生命周期事件（`beforeenter`、`enter`、`afterenter`、`beforeleave`、`leave`、`afterleave`），可用于在动画不同阶段执行自定义逻辑。`close` 事件在幕帘开始关闭时触发，`closed` 事件在幕帘完全关闭后触发。

10. **主题定制**：幕帘组件支持通过 CSS 变量进行主题定制，可用的 CSS 变量包括：
    - `--wot-curtain-content-radius`：内容区域圆角（默认 24px）
    - `--wot-curtain-content-close-color`：关闭按钮颜色（默认白色）
    - `--wot-curtain-content-close-fs`：关闭按钮字体大小（默认 `$-fs-big`）
