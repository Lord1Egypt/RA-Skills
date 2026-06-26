# Navbar 导航栏


## 组件概况

Navbar 导航栏组件用于展示页面标题，并提供左右两侧的交互区域（左侧返回按钮、右侧操作按钮），支持自定义胶囊插槽，满足各业务场景下的顶部导航需求。配套提供了 `wd-navbar-capsule` 胶囊按钮组件，用于模拟微信原生胶囊按钮样式，提供返回和返回首页两个快捷操作。

## 核心功能描述

- **标题展示**：支持纯文字标题，最大宽度为 60%，超出时自动省略号显示；也可通过 `title` 插槽自定义标题内容
- **左侧区域**：支持返回箭头（`left-arrow`）和左侧文字（`left-text`），也可通过 `left` 插槽完全自定义
- **右侧区域**：支持右侧文字（`right-text`），也可通过 `right` 插槽完全自定义
- **胶囊插槽**：提供 `capsule` 插槽，可嵌入 `wd-navbar-capsule` 胶囊组件，替代默认的左侧区域
- **固定定位**：通过 `fixed` 属性将导航栏固定在页面顶部，配合 `placeholder` 可生成占位元素避免内容遮挡
- **安全区适配**：通过 `safeAreaInsetTop` 属性自动适配顶部安全区（刘海屏等设备）
- **左右禁用**：通过 `left-disabled` 和 `right-disabled` 分别禁用左右两侧交互区域
- **下边框**：默认显示 0.5px 的下边框，可通过 `bordered` 属性关闭
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **常规页面导航**：页面标题 + 左侧返回按钮的标准导航结构
- **小程序/APP 内页导航**：使用胶囊组件提供返回上级和返回首页的双层导航能力
- **搜索页导航**：将标题区域替换为搜索框，实现内嵌搜索栏的导航效果
- **操作型导航**：在右侧放置操作按钮（如"保存"、"完成"等），提供快捷操作入口
- **沉浸式导航**：结合 `customStyle` 可实现透明背景导航，用于详情页封面图覆盖效果
- **内容编辑页**：左右两侧禁用状态下展示不可操作的导航栏

## API

### wd-navbar Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| title | string | - | 否 | 标题文字 |
| leftText | string | - | 否 | 左侧文案 |
| rightText | string | - | 否 | 右侧文案 |
| leftArrow | boolean | false | 否 | 是否显示左侧箭头 |
| bordered | boolean | true | 否 | 是否显示下边框 |
| fixed | boolean | false | 否 | 是否固定到顶部 |
| placeholder | boolean | false | 否 | 固定在顶部时，是否在标题位置生成一个等高的占位元素 |
| zIndex | number | 500 | 否 | 导航栏 z-index |
| safeAreaInsetTop | boolean | false | 否 | 是否开启顶部安全区适配 |
| leftDisabled | boolean | false | 否 | 是否禁用左侧按钮，禁用时透明度降低，且无法点击 |
| rightDisabled | boolean | false | 否 | 是否禁用右侧按钮，禁用时透明度降低，且无法点击 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### wd-navbar-capsule Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### wd-navbar Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| click-left | - | 点击左侧区域触发，禁用状态下不会触发 |
| click-right | - | 点击右侧区域触发，禁用状态下不会触发 |

### wd-navbar-capsule Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| back | - | 点击胶囊左侧返回图标触发 |
| back-home | - | 点击胶囊右侧首页图标触发 |

### wd-navbar Methods

组件不对外暴露任何方法。

### wd-navbar-capsule Methods

组件不对外暴露任何方法。

### wd-navbar Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| title | - | 自定义标题区域内容，可放置搜索框或其他组件 |
| left | - | 自定义左侧区域内容，优先级高于 `leftText` 和 `leftArrow` |
| right | - | 自定义右侧区域内容，优先级高于 `rightText` |
| capsule | - | 放置胶囊按钮组件，优先级高于默认左侧区域 |

### wd-navbar-capsule Slots

组件不对外暴露任何插槽。

## 使用示例

### 示例 1：基础用法

展示导航栏的基本结构，包含纯标题以及带返回按钮的常见组合。

```vue
<template>
  <view>
    <!-- 仅标题 -->
    <wd-navbar title="标题"></wd-navbar>

    <!-- 标题 + 返回箭头 + 返回文字 -->
    <wd-navbar
      title="标题"
      left-text="返回"
      left-arrow
      @click-left="handleClickLeft"
    ></wd-navbar>

    <!-- 标题 + 返回 + 右侧按钮 -->
    <wd-navbar
      title="标题"
      left-text="返回"
      left-arrow
      right-text="按钮"
      @click-left="handleClickLeft"
      @click-right="handleClickRight"
    ></wd-navbar>
  </view>
</template>
<script lang="ts" setup>
  import { useToast } from '@/uni_modules/wot-ui-plus'
  const { show: showToast } = useToast()

  function handleClickLeft() {
    uni.navigateBack({})
  }

  function handleClickRight() {
    showToast('点击了右侧按钮')
  }
</script>
```

`wd-navbar` 提供了三个核心属性：`title`（标题文字）、`left-text`（左侧文案）和 `left-arrow`（是否显示返回箭头）。`right-text` 可添加右侧操作文字。所有点击事件受对应的 `disabled` 属性控制。

### 示例 2：固定定位与安全区适配

将导航栏固定在页面顶部，并自动适配刘海屏等设备的顶部安全区高度。

```vue
<template>
  <view>
    <!-- 固定顶部导航栏 -->
    <wd-navbar
      fixed
      placeholder
      title="固定导航栏"
      left-arrow
      safeAreaInsetTop
      @click-left="handleClickLeft"
    ></wd-navbar>

    <!-- 页面内容 -->
    <view style="padding: 20rpx">
      <view>页面内容区域</view>
    </view>
  </view>
</template>
<script lang="ts" setup>
  function handleClickLeft() {
    uni.navigateBack({})
  }
</script>
```

通过 `fixed` 属性将导航栏固定在页面顶部（`position: fixed`）。设置 `placeholder` 属性后，导航栏会在自身位置生成一个等高的占位元素，防止页面内容被遮挡。`safeAreaInsetTop` 属性会在导航栏顶部自动添加状态栏高度的 `padding-top`，适配刘海屏等设备的安全区。`fixed` 和 `placeholder` 变化时会自动重新计算占位高度。

### 示例 3：使用插槽自定义

通过插槽完全自定义左侧和右侧内容，实现图标按钮等高级效果。

```vue
<template>
  <view>
    <wd-navbar title="标题" @click-left="handleClickLeft">
      <!-- 自定义左侧 -->
      <template #left>
        <wd-icon name="left" size="24px" class="wd-navbar__arrow" />
      </template>

      <!-- 自定义右侧 -->
      <template #right>
        <wd-icon name="search" size="18" />
      </template>
    </wd-navbar>
  </view>
</template>
<script lang="ts" setup>
  function handleClickLeft() {
    uni.navigateBack({})
  }
</script>
```

当提供了 `left` 插槽时，会忽略 `leftText` 和 `leftArrow` 属性；当提供了 `right` 插槽时，会忽略 `rightText` 属性。插槽内容完全自定义，可以放置任意组件。

### 示例 4：禁用左右按钮

分别禁用左侧和右侧交互区域，适用于不需要用户操作的导航场景。

```vue
<template>
  <view>
    <wd-navbar
      title="标题"
      left-text="返回"
      right-text="按钮"
      left-arrow
      left-disabled
      right-disabled
    ></wd-navbar>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `left-disabled` 和 `right-disabled` 分别禁用左侧和右侧交互区域，禁用时区域透明度降至 0.65，点击事件不会触发。此功能适用于只读展示场景或等待状态下的导航栏。

### 示例 5：胶囊按钮

使用 `capsule` 插槽嵌入胶囊组件，提供返回和返回首页的双层导航能力。

```vue
<template>
  <view>
    <wd-navbar title="标题" left-text="返回" right-text="设置" left-arrow>
      <template #capsule>
        <wd-navbar-capsule
          @back="handleBack"
          @back-home="handleBackHome"
        ></wd-navbar-capsule>
      </template>
    </wd-navbar>
  </view>
</template>
<script lang="ts" setup>
  function handleBack() {
    uni.navigateBack({})
  }

  function handleBackHome() {
    uni.reLaunch({ url: '/pages/index/Index' })
  }
</script>
```

当 `wd-navbar` 的 `capsule` 插槽被填充内容时，会优先使用胶囊区域，隐藏默认的左侧区域。`wd-navbar-capsule` 组件内置左侧返回图标和右侧首页图标，中间用分隔线隔开，整体呈现胶囊形状的圆角边框。点击左侧图标触发 `back` 事件，点击右侧图标触发 `back-home` 事件。

### 示例 6：带搜索栏

将标题区域替换为搜索框，实现搜索页导航效果。

```vue
<template>
  <view>
    <wd-navbar left-text="返回" right-text="设置" left-arrow>
      <template #title>
        <view class="search-box">
          <wd-search
            v-model="keyword"
            hide-cancel
            placeholder-left
          ></wd-search>
        </view>
      </template>
    </wd-navbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const keyword = ref('')
</script>
<style lang="scss" scoped>
  .search-box {
    display: flex;
    height: 100%;
    align-items: center;
    --wot-search-padding: 0;
    --wot-search-side-padding: 0;
    :deep() {
      .wd-search {
        background: transparent;
      }
    }
  }
</style>
```

通过 `title` 插槽将标题区域替换为搜索框组件，配合 CSS 变量和深度选择器调整搜索框样式，使搜索框无缝融入导航栏中。`hide-cancel` 隐藏搜索取消按钮，`placeholder-left` 使占位符居左显示。

## 注意事项

1. **capsule 插槽优先级最高**：当 `capsule` 插槽有内容时，会覆盖默认的左侧区域（包括 `leftText`、`leftArrow` 和 `left` 插槽）
2. **占位高度动态计算**：当使用 `fixed` 和 `placeholder` 组合时，占位高度通过 DOM 查询动态获取，因此在组件挂载后的下一帧计算，首次渲染时可能存在短暂的高度跳动
3. **安全区适配仅控制 padding-top**：`safeAreaInsetTop` 仅影响导航栏的顶部内边距（值为系统状态栏高度），不会改变导航栏自身的高度
4. **标题宽度限制为 60%**：标题区域最大宽度为导航栏宽度的 60%，超出部分自动省略号显示，确保左右两侧区域有足够的空间
5. **右侧区域条件渲染**：右侧区域仅在提供 `right` 插槽或设置了 `rightText` 时才会渲染
6. **z-index 仅在固定模式下生效**：`zIndex` 属性仅在 `fixed` 为 `true` 时才会应用到样式中，默认值为 500
7. **暗色模式自动适配**：组件已内置暗色主题样式，包括背景色、文字颜色、箭头颜色和胶囊边框颜色都会自动调整
8. **边框为 0.5px 细线**：使用 `halfPixelBorder` 技术实现 0.5px 的下边框效果，在高分辨率屏幕上显示更加精致
9. **导航栏高度由 CSS 变量控制**：默认高度通过 `--wot-navbar-height` CSS 变量定义，可通过 `customStyle` 或全局变量覆盖
