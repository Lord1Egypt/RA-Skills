# Popup 弹出层


## 组件概况

Popup 弹出层组件是一个模态容器组件，用于在页面中弹出一个浮层来展示额外内容或进行交互操作。该组件支持从不同方向（上、下、左、右、居中）弹出，自带过渡动画效果，可配置遮罩层、关闭按钮、滚动锁定等功能，并可结合其他组件构建更复杂的交互界面。

组件内部基于 Overlay 遮罩层和 Transition 过渡动画组件实现，支持通过 `root-portal` 将弹窗从当前 DOM 层级中脱离出来，有效解决固定定位在复杂层级中失效的问题，特别适用于嵌套弹窗、弹窗内使用固定定位等场景。

## 核心功能描述

- **弹出位置**：支持居中、顶部、右侧、底部、左侧五种弹出位置，不同位置对应不同的滑入滑出动画
- **过渡动画**：内置多种过渡动画类型（渐显、滑入、缩放等），支持自定义动画类型和动画持续时间
- **遮罩控制**：支持显示/隐藏遮罩层，可自定义遮罩样式，支持点击遮罩关闭弹窗
- **关闭按钮**：内置关闭按钮，点击即可关闭弹窗，按钮自动定位在弹窗右上角并旋转 45 度呈关闭图标形态
- **滚动锁定**：支持锁定页面滚动，防止弹窗出现时背景内容滚动
- **安全区域**：支持开启底部安全距离适配，自动适配 iPhone X 等带有底部安全区域的机型
- **脱离层级**：通过 `root-portal` 属性将弹窗从页面中脱离，解决固定定位在嵌套结构中失效的问题
- **懒渲染**：默认开启懒渲染，弹窗内容仅在首次展示时才进行渲染，优化性能
- **动画事件**：提供完整的进入/离开生命周期事件，包括进入前、进入中、进入后、离开前、离开中、离开后
- **暗色模式支持**：内置 dark 主题样式，自动适配系统主题切换

## 适用业务场景

- **信息展示**：在居中弹窗中展示详细信息、图片预览、说明文档等
- **操作菜单**：从底部弹出操作菜单，提供多个操作选项供用户选择
- **表单填写**：在弹窗中嵌入表单，用于快速填写信息、搜索筛选等
- **侧边导航**：从左侧或右侧弹出侧边栏，用于导航菜单、筛选面板等
- **嵌套弹窗**：在弹窗中再打开子弹窗，适用于多级确认、详情查看等场景
- **固定定位场景**：弹窗内容需要使用固定定位（如顶部吸顶导航）时，使用 `root-portal` 避免层级问题

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 弹出层是否显示，支持 v-model 双向绑定 | boolean | - | false | - |
| position | 弹出位置 | string | center / top / right / bottom / left | center | - |
| closable | 是否显示关闭按钮 | boolean | - | false | - |
| transition | 自定义动画类型，参见 wd-transition 组件的 name | string | fade / fade-up / fade-down / fade-left / fade-right / slide-up / slide-down / slide-left / slide-right / zoom-in | - | - |
| closeOnClickModal | 点击遮罩时是否关闭弹窗 | boolean | - | true | - |
| duration | 动画持续时间，单位为毫秒 | number / boolean | - | 300 | - |
| modal | 是否显示遮罩层 | boolean | - | true | - |
| zIndex | 弹出层层级 | number | - | 10 | - |
| hideWhenClose | 关闭时是否隐藏弹出层（display: none） | boolean | - | true | - |
| modalStyle | 遮罩层自定义样式 | string | - | '' | - |
| safeAreaInsetBottom | 是否设置底部安全距离（适配 iPhone X 类型机型） | boolean | - | false | - |
| lazyRender | 是否开启懒渲染，触发展示时才渲染内容 | boolean | - | true | - |
| lockScroll | 是否锁定滚动 | boolean | - | true | - |
| rootPortal | 是否从页面中脱离出来，用于解决各种 fixed 失效问题（H5: teleport, APP: renderjs, 小程序: root-portal） | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| update:modelValue | 弹出层显示/隐藏状态变化时触发，用于 v-model 双向绑定 | value: boolean |
| click-modal | 点击遮罩层时触发 | - |
| close | 关闭弹窗时触发（点击关闭按钮或点击遮罩关闭） | - |
| before-enter | 进入动画开始前触发 | - |
| enter | 进入动画开始时触发 | - |
| after-enter | 进入动画完成后触发 | - |
| before-leave | 离开动画开始前触发 | - |
| leave | 离开动画开始时触发 | - |
| after-leave | 离开动画完成后触发 | - |

### Methods

组件未对外暴露可调用的方法。

### Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于放置弹出层的内容 | 任意内容 |

## 使用示例

### 示例 1：基础用法

最基本的弹出层使用方式，通过 `v-model` 控制弹出层的显示与隐藏。

```vue
<template>
  <view>
    <wd-cell-group>
      <wd-cell title="弹出层" is-link @click="handleOpen" />
    </wd-cell-group>

    <wd-popup v-model="show" @close="handleClose" custom-style="border-radius: 32rpx;">
      <view class="popup-content">
        <text class="popup-text">弹弹弹</text>
      </view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const show = ref<boolean>(false)

  function handleOpen() {
    show.value = true
  }

  function handleClose() {
    show.value = false
  }
</script>

<style lang="scss" scoped>
  .popup-content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40rpx;
  }

  .popup-text {
    color: #333;
    font-size: 40rpx;
  }
</style>
```

该示例展示了最基本的弹出层用法。居中弹出，内容区域通过 `custom-style` 设置了圆角效果。点击单元格打开弹窗，点击遮罩层或关闭按钮均可关闭弹窗。

### 示例 2：弹出位置

通过 `position` 属性设置弹出层的位置，支持 `center`（居中）、`top`（顶部）、`right`（右侧）、`bottom`（底部）、`left`（左侧）五种位置。不同位置会自动匹配对应的滑入/滑出动画。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-cell title="顶部弹出" is-link @click="showTop = true" />
      <wd-cell title="右侧弹出" is-link @click="showRight = true" />
      <wd-cell title="底部弹出" is-link @click="showBottom = true" />
      <wd-cell title="左侧弹出" is-link @click="showLeft = true" />
    </wd-cell-group>

    <!-- 顶部弹出 -->
    <wd-popup v-model="showTop" position="top" custom-style="height: 200px;">
      <view class="position-content">顶部内容</view>
    </wd-popup>

    <!-- 右侧弹出 -->
    <wd-popup v-model="showRight" position="right" custom-style="width: 200px;">
      <view class="position-content">右侧内容</view>
    </wd-popup>

    <!-- 底部弹出 -->
    <wd-popup v-model="showBottom" position="bottom" custom-style="height: 200px;">
      <view class="position-content">底部内容</view>
    </wd-popup>

    <!-- 左侧弹出 -->
    <wd-popup v-model="showLeft" position="left" custom-style="width: 200px;">
      <view class="position-content">左侧内容</view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showTop = ref<boolean>(false)
  const showRight = ref<boolean>(false)
  const showBottom = ref<boolean>(false)
  const showLeft = ref<boolean>(false)
</script>

<style lang="scss" scoped>
  .position-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #333;
    font-size: 32rpx;
  }
</style>
```

该示例展示了四种方向的弹出效果：
- `position="top"`：从顶部向下滑入，向上滑出
- `position="right"`：从右侧向左滑入，向右滑出
- `position="bottom"`：从底部向上滑入，向下滑出
- `position="left"`：从左侧向右滑入，向左滑出
- 居中使用默认的 `zoom-in`（缩放）+ `fade`（渐显）组合动画

### 示例 3：关闭按钮与遮罩控制

通过 `closable` 属性显示关闭按钮，通过 `close-on-click-modal` 控制点击遮罩是否关闭，通过 `modal` 控制是否显示遮罩层。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-cell title="显示关闭按钮" is-link @click="showCloseBtn = true" />
      <wd-cell title="禁止点击遮罩关闭" is-link @click="showNoModalClose = true" />
      <wd-cell title="隐藏遮罩层" is-link @click="showNoModal = true" />
    </wd-cell-group>

    <!-- 显示关闭按钮 -->
    <wd-popup
      v-model="showCloseBtn"
      position="bottom"
      closable
      custom-style="height: 200px;"
    >
      <view class="control-content">点击右上角关闭按钮关闭弹窗</view>
    </wd-popup>

    <!-- 禁止点击遮罩关闭 -->
    <wd-popup
      v-model="showNoModalClose"
      position="bottom"
      :close-on-click-modal="false"
      closable
      custom-style="height: 200px;"
    >
      <view class="control-content">只能通过关闭按钮关闭弹窗</view>
    </wd-popup>

    <!-- 隐藏遮罩层 -->
    <wd-popup
      v-model="showNoModal"
      position="bottom"
      :modal="false"
      closable
      custom-style="height: 200px;"
    >
      <view class="control-content">无弹窗遮罩背景</view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showCloseBtn = ref<boolean>(false)
  const showNoModalClose = ref<boolean>(false)
  const showNoModal = ref<boolean>(false)
</script>

<style lang="scss" scoped>
  .control-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #333;
    font-size: 32rpx;
    padding: 0 40rpx;
    text-align: center;
  }
</style>
```

该示例展示了三种遮罩与关闭控制场景：
- `closable`：在弹窗右上角显示关闭按钮（旋转 45 度的加号图标）
- `close-on-click-modal="false"`：点击遮罩层不关闭弹窗，必须通过关闭按钮或其他方式关闭
- `modal="false"`：不显示遮罩层，弹窗直接浮在页面内容上方

### 示例 4：底部安全距离与滚动锁定

通过 `safe-area-inset-bottom` 属性适配 iPhone X 等机型的底部安全区域，通过 `lock-scroll` 锁定页面滚动。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-cell title="开启底部安全距离" is-link @click="showSafeArea = true" />
      <wd-cell title="锁定滚动" is-link @click="showLockScroll = true" />
    </wd-cell-group>

    <!-- 开启底部安全距离 -->
    <wd-popup
      v-model="showSafeArea"
      position="bottom"
      :safe-area-inset-bottom="true"
      custom-style="height: 200px;"
    >
      <view class="safe-content">底部安全距离示例</view>
    </wd-popup>

    <!-- 锁定滚动 -->
    <wd-popup
      v-model="showLockScroll"
      position="bottom"
      lock-scroll
      custom-style="height: 300px;"
    >
      <scroll-view scroll-y style="height: 300px;">
        <view class="scroll-content">
          <view v-for="i in 20" :key="i" class="scroll-item">列表项 {{ i }}</view>
        </view>
      </scroll-view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showSafeArea = ref<boolean>(false)
  const showLockScroll = ref<boolean>(false)
</script>

<style lang="scss" scoped>
  .safe-content {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #333;
    font-size: 32rpx;
  }

  .scroll-content {
    padding: 0 32rpx;
  }

  .scroll-item {
    padding: 24rpx 0;
    border-bottom: 1rpx solid #eee;
    color: #333;
    font-size: 28rpx;
  }
</style>
```

该示例展示了两个实用特性：
- `safe-area-inset-bottom`：自动获取设备底部安全区域高度并添加到弹窗底部 padding，确保内容不会被设备的底部安全区域遮挡。在微信小程序和 H5 中获取方式有所不同。
- `lock-scroll`：锁定页面滚动，防止弹窗打开时背景内容继续滚动。

### 示例 5：嵌套弹窗

在弹窗中再打开子弹窗，子弹窗可以使用 `root-portal` 属性脱离父弹窗的层级，避免 `fixed` 定位失效的问题。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-cell title="嵌套弹窗" is-link @click="showParent = true" />
    </wd-cell-group>

    <!-- 父级弹窗 -->
    <wd-popup
      v-model="showParent"
      position="center"
      custom-style="padding: 20px; border-radius: 16px;"
      @close="handleParentClose"
    >
      <view class="parent-content">
        <text class="parent-title">父弹窗</text>
        <text class="parent-desc">点击下面的按钮打开子弹窗</text>
        <view class="btn-group">
          <wd-button type="primary" size="small" @click="showChild1 = true">
            打开普通子弹窗
          </wd-button>
          <wd-button type="success" size="small" @click="showChild2 = true">
            打开传送子弹窗
          </wd-button>
        </view>
      </view>

      <!-- 普通子弹窗（可能受父弹窗层级影响） -->
      <wd-popup
        v-model="showChild1"
        position="center"
        custom-style="padding: 20px; border-radius: 16px;"
      >
        <view class="child-content">
          <text class="child-title">子弹窗（普通模式）</text>
          <text class="child-desc">这个子弹窗可能会被父弹窗的层级影响</text>
          <wd-button type="primary" size="small" @click="showChild1 = false">关闭</wd-button>
        </view>
      </wd-popup>

      <!-- 传送子弹窗（脱离层级，推荐使用） -->
      <wd-popup
        v-model="showChild2"
        root-portal
        position="center"
        custom-style="padding: 20px; border-radius: 16px;"
      >
        <view class="child-content">
          <text class="child-title">子弹窗（传送模式）</text>
          <text class="child-desc">这个子弹窗使用传送功能，避免了层级问题</text>
          <wd-button type="success" size="small" @click="showChild2 = false">关闭</wd-button>
        </view>
      </wd-popup>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showParent = ref<boolean>(false)
  const showChild1 = ref<boolean>(false)
  const showChild2 = ref<boolean>(false)

  function handleParentClose() {
    // 关闭父弹窗时也关闭子弹窗
    showChild1.value = false
    showChild2.value = false
  }
</script>

<style lang="scss" scoped>
  .parent-content,
  .child-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20rpx;
  }

  .parent-title,
  .child-title {
    color: #333;
    font-size: 36rpx;
    font-weight: bold;
    text-align: center;
  }

  .parent-desc,
  .child-desc {
    color: #666;
    font-size: 28rpx;
    text-align: center;
    line-height: 1.5;
    margin: 10rpx 0;
  }

  .btn-group {
    display: flex;
    gap: 20rpx;
    margin-top: 20rpx;
  }
</style>
```

该示例展示了嵌套弹窗的使用场景：
- 普通子弹窗：直接嵌套在父弹窗内部，在某些平台可能受到 `fixed` 定位层级限制
- 传送子弹窗：通过 `root-portal` 属性将子弹窗传送到页面根节点，有效解决固定定位失效、z-index 层级冲突等问题，**推荐在嵌套弹窗场景中使用**

### 示例 6：自定义动画类型

通过 `transition` 属性自定义过渡动画类型，覆盖默认的动画效果。

```vue
<template>
  <view>
    <wd-cell-group border>
      <wd-cell title="缩放动画" is-link @click="showZoom = true" />
      <wd-cell title="淡入淡出" is-link @click="showFade = true" />
      <wd-cell title="慢速动画" is-link @click="showSlow = true" />
    </wd-cell-group>

    <!-- 自定义缩放动画 -->
    <wd-popup
      v-model="showZoom"
      transition="zoom-in"
      custom-style="padding: 40rpx; border-radius: 24rpx; width: 60%;"
    >
      <view class="anim-content">
        <text class="anim-text">缩放动画效果</text>
      </view>
    </wd-popup>

    <!-- 自定义淡入淡出动画 -->
    <wd-popup
      v-model="showFade"
      position="bottom"
      transition="fade"
      custom-style="height: 200px;"
    >
      <view class="anim-content-bottom">
        <text class="anim-text">淡入淡出效果</text>
      </view>
    </wd-popup>

    <!-- 慢速动画 -->
    <wd-popup
      v-model="showSlow"
      position="bottom"
      :duration="600"
      custom-style="height: 200px;"
    >
      <view class="anim-content-bottom">
        <text class="anim-text">动画持续时间为 600ms</text>
      </view>
    </wd-popup>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showZoom = ref<boolean>(false)
  const showFade = ref<boolean>(false)
  const showSlow = ref<boolean>(false)
</script>

<style lang="scss" scoped>
  .anim-content {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40rpx 0;
  }

  .anim-content-bottom {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .anim-text {
    color: #333;
    font-size: 32rpx;
  }
</style>
```

该示例展示了动画自定义的两种方式：
- `transition`：设置自定义动画类型，可选值包括 `fade`（渐显）、`fade-up`、`fade-down`、`fade-left`、`fade-right`、`slide-up`、`slide-down`、`slide-left`、`slide-right`、`zoom-in`（缩放）。如果不设置 `transition`，组件会根据 `position` 自动匹配动画：居中时使用 `zoom-in` + `fade` 组合，其他位置使用对应的 `slide` 动画。
- `duration`：设置动画持续时间，默认值为 300ms，此处设置为 600ms 实现慢速动画效果。

## 注意事项

1. **双向绑定**：推荐使用 `v-model` 控制弹出层的显示与隐藏。组件内部通过 `update:modelValue` 事件更新状态，手动设置 `modelValue` 为 `false` 即可关闭弹窗。

2. **尺寸设置**：弹出层本身没有固定的宽高，需要通过 `custom-style` 属性设置宽度或高度。居中弹窗通常需要设置固定宽高，底部/顶部弹窗通常需要设置高度，左侧/右侧弹窗通常需要设置宽度。

3. **关闭按钮**：开启 `closable` 后，关闭按钮使用 `wd-icon` 组件，图标名称为 `add`，通过 CSS 旋转 -45 度呈现关闭图标样式，固定在弹窗右上角（`top: 10px; right: 10px`）。

4. **嵌套弹窗层级问题**：在弹窗中再打开子弹窗时，子弹窗的 `fixed` 定位可能受父弹窗影响而失效。此时应为子弹窗设置 `root-portal` 属性，将其传送到页面根节点，脱离当前 DOM 层级。

5. **底部安全距离**：`safe-area-inset-bottom` 仅在 `position="bottom"` 时有效。在微信小程序中通过 `screenHeight - safeArea.bottom` 计算安全距离，在 H5/App 中通过 `safeAreaInsets.bottom` 获取。

6. **懒渲染机制**：默认开启 `lazyRender`，弹窗内容仅在首次展示时渲染。如果弹窗内容需要在关闭时销毁，可以设置 `hide-when-close` 为 `true`（默认值），关闭后 DOM 节点会被移除。

7. **遮罩样式自定义**：通过 `modalStyle` 属性可以自定义遮罩层样式，例如修改遮罩颜色或透明度。遮罩层默认使用 Overlay 组件的样式。

8. **动画事件**：组件提供了完整的动画生命周期事件（`before-enter`、`enter`、`after-enter`、`before-leave`、`leave`、`after-leave`），可用于在动画的不同阶段执行自定义逻辑。

9. **暗色模式**：组件原生支持暗色模式，当父级包含 `wot-theme-dark` 类名时，弹窗背景色会自动切换为暗色主题色，关闭按钮颜色也会同步调整。

10. **滚动穿透处理**：组件通过 `lock-scroll` 属性控制是否锁定滚动。开启后，遮罩层会阻止触摸事件的默认行为，防止弹窗打开时背景页面滚动。
