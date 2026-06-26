# Skeleton 骨架屏


## 组件概况

Skeleton 骨架屏组件用于在数据加载过程中展示页面或模块的大致轮廓结构，为用户提供加载中的视觉反馈，避免页面突然跳动或空白。该组件支持 4 种预设主题风格（头像、图片、文本、段落），并提供灵活的 `rowCol` 属性用于自定义任意行列布局。同时支持渐变和闪烁两种加载动画效果，以及通过 `loading` 属性实现骨架屏与真实内容的无缝切换。

组件通过解析 `rowCol` 数组生成行和列的 DOM 结构，每一行对应一个 `wd-skeleton__row`，每列对应一个 `wd-skeleton__col`，并根据传入的配置自动计算样式。

## 核心功能描述

- **四种预设主题**：内置 `text`（文本骨架屏）、`avatar`（头像骨架屏）、`image`（图片骨架屏）、`paragraph`（段落骨架屏）四种主题风格，开箱即用
- **自定义布局（rowCol）**：通过 `rowCol` 属性可精确控制每一行每一列的宽度、高度、间距、形状等，支持三种数据格式：数字（表示列数）、对象（单列配置）、数组（多列配置）
- **三种形状类型**：列元素支持 `text`（文本条，宽度 100%）、`rect`（矩形，带圆角）、`circle`（圆形，固定宽高）三种类型
- **两种加载动画**：支持 `gradient`（渐变加载动画）和 `flashed`（闪烁加载动画）两种效果，值为空时表示无动画
- **加载状态切换**：`loading` 属性控制显示骨架屏还是真实内容，默认值为 `true`。当 `loading` 为 `false` 时渲染插槽中的真实内容
- **丰富的样式配置**：列对象支持 `size`、`width`、`height`、`margin`、`background`、`marginLeft`、`marginRight`、`borderRadius`、`backgroundColor` 等样式属性
- **默认插槽**：通过默认插槽传入加载完成后的真实内容，实现骨架屏与内容的平滑切换
- **自定义样式**：支持通过 `custom-class` 和 `custom-style` 属性进行根节点样式定制
- **暗色模式支持**：内置 dark 主题样式，骨架屏块背景色自动切换为 `$-dark-background4`

## 适用业务场景

- **列表数据加载**：在列表数据请求期间展示列表项的骨架屏占位，提升加载体验
- **卡片模块加载**：在复杂卡片组件的数据加载中展示结构轮廓
- **图文详情加载**：在文章详情、商品详情等图文混合内容加载时展示段落骨架屏
- **宫格布局加载**：在宫格、网格等布局加载时展示对应的方块骨架屏
- **用户信息加载**：在用户资料、评论等头像+文字组合加载时展示头像骨架屏
- **图片组合加载**：在图片画廊、商品图片等场景展示图片占位骨架屏

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| theme | string | 'text' | 否 | 骨架图主题风格，可选值：`text`（文本）、`avatar`（头像）、`image`（图片）、`paragraph`（段落） |
| rowCol | SkeletonRowCol[] | [] | 否 | 用于设置行列数量、宽度、高度、间距等，详见下方类型说明 |
| loading | boolean | true | 否 | 是否为加载状态。`true` 时显示骨架屏，`false` 时显示插槽中的真实内容 |
| animation | string | '' | 否 | 动画效果，可选值：`gradient`（渐变加载动画）、`flashed`（闪烁加载动画），值为空表示无动画 |
| customStyle | CSSProperties | {} | 否 | 自定义组件根元素样式 |
| customClass | string \| array \| object | '' | 否 | 自定义组件根元素类名 |

### SkeletonRowCol 类型

`rowCol` 属性支持数组形式，数组中的每一项可以有以下三种格式：

```ts
// 数字：表示该行有几列，每列为默认文本条样式
type SkeletonRowCol = number | SkeletonRowColObj | Array<SkeletonRowColObj>

interface SkeletonRowColObj {
  type?: 'rect' | 'circle' | 'text'   // 形状类型
  size?: string | number               // 同时设置宽高
  width?: string | number              // 宽度
  height?: string | number             // 高度
  margin?: string | number             // 外边距
  background?: string                  // 背景色
  marginLeft?: string | number         // 左边距
  marginRight?: string | number        // 右边距
  borderRadius?: string | number       // 圆角
  backgroundColor?: string             // 背景色（同 background）
}
```

### 预设主题说明

| 主题名称 | 对应的 rowCol 配置 | 说明 |
| --- | --- | --- |
| `text` | `[1, [{ width: '24%' }, { width: '76%' }]]` | 两行文本，第一行占满宽度，第二行分为 24% 和 76% 两列 |
| `avatar` | `[{ type: 'circle', height: '64px', width: '64px' }]` | 64px 的圆形，适用于头像占位 |
| `image` | `[{ type: 'rect', height: '64px', width: '64px' }]` | 64px 的矩形，适用于图片占位 |
| `paragraph` | `[1, 1, 1, { width: '55%' }]` | 四行文本，前三行占满宽度，第四行宽度为 55%，模拟段落结构 |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| default | - | 加载完成后的真实内容。当 `loading` 为 `false` 时渲染此插槽内容 |

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。

### Events

当前组件未定义对外抛出的事件。

## 使用示例

### 示例 1：预设主题

效果说明：使用内置的四种预设主题，快速生成常见的骨架屏布局。

```vue
<template>
  <view>
    <!-- 头像骨架屏 -->
    <wd-skeleton theme="avatar" />

    <!-- 图片骨架屏 -->
    <wd-skeleton theme="image" />

    <!-- 文本骨架屏 -->
    <wd-skeleton theme="text" />

    <!-- 段落骨架屏 -->
    <wd-skeleton theme="paragraph" />
  </view>
</template>

<script lang="ts" setup>
  // theme 支持 'avatar' | 'image' | 'text' | 'paragraph' 四种预设值
</script>
```

当不传入 `rowCol` 属性时，组件会根据 `theme` 自动渲染对应的预设布局。`theme` 默认值为 `text`。

### 示例 2：宫格骨架屏

效果说明：通过 `rowCol` 数组自定义宫格布局的骨架屏，使用二维数组实现多行多列布局。

```vue
<template>
  <view>
    <wd-skeleton :row-col="grid" />
  </view>
</template>

<script lang="ts" setup>
  import type { SkeletonRowCol } from 'wot-design-uni/components/wd-skeleton/types'

  // 二维数组，外层数组表示行，内层数组表示该行的列
  const grid = [
    [
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' }
    ],
    [
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' }
    ]
  ] as SkeletonRowCol[]
</script>
```

通过二维数组可以精确控制每一行每一列的尺寸。第一行为 5 个 48px 的方块，第二行为 5 个 48px 宽、16px 高的文本条。

### 示例 3：单元格骨架屏

效果说明：通过组合多个 Skeleton 组件实现头像+文字的单元格布局骨架屏，模拟真实列表项结构。

```vue
<template>
  <view>
    <!-- 圆形头像 + 文字 -->
    <view style="display: flex">
      <wd-skeleton :row-col="[{ size: '48px', type: 'circle' }]" />
      <wd-skeleton
        :custom-style="{ width: '100%', marginLeft: '12px' }"
        :row-col="[{ width: '50%' }, { width: '100%' }]"
      />
    </view>

    <!-- 方形图标 + 文字 -->
    <view style="display: flex; margin-top: 20px">
      <wd-skeleton :row-col="[{ size: '48px', type: 'rect' }]" />
      <wd-skeleton
        :custom-style="{ width: '100%', marginLeft: '12px' }"
        :row-col="[{ width: '50%' }, { width: '100%' }]"
      />
    </view>
  </view>
</template>

<script lang="ts" setup>
  // 使用 size 属性可同时设置宽高，type 控制形状为圆形或矩形
</script>
```

通过 flex 布局组合多个 Skeleton 组件，可以轻松实现头像+文字的单元格布局。`size` 属性可同时设置宽高，`type` 控制形状。

### 示例 4：渐变与闪烁动画

效果说明：通过 `animation` 属性为骨架屏添加加载动画，提升用户的等待体验。

```vue
<template>
  <view>
    <!-- 渐变加载动画 -->
    <wd-skeleton animation="gradient" theme="paragraph" />

    <!-- 闪烁加载动画 -->
    <view style="display: flex">
      <wd-skeleton :row-col="[{ size: '48px', type: 'circle' }]" />
      <wd-skeleton
        :custom-style="{ width: '100%', marginLeft: '12px' }"
        animation="flashed"
        theme="paragraph"
      />
    </view>
  </view>
</template>

<script lang="ts" setup>
  // animation 支持 'gradient'（渐变）| 'flashed'（闪烁）| ''（无动画）
</script>
```

`gradient` 动画通过 CSS `::after` 伪元素实现从左到右的光线扫过效果，动画持续 1.5 秒，延迟 2 秒后无限循环。`flashed` 动画通过透明度变化实现闪烁效果，动画持续 2 秒，延迟 2 秒后无限循环。

### 示例 5：图片组合骨架屏

效果说明：使用 `rowCol` 实现图片+文字的组合布局骨架屏，模拟商品卡片或文章卡片的结构。

```vue
<template>
  <view>
    <wd-skeleton :row-col="imageGroup" />
    <wd-skeleton :custom-style="{ marginTop: '20px' }" :row-col="imageGroup" />
  </view>
</template>

<script lang="ts" setup>
  import type { SkeletonRowCol } from 'wot-design-uni/components/wd-skeleton/types'

  // 数组每一项代表一行
  // 第一项：高度 171px 的图片（默认宽度 100%）
  // 第二项：数字 1 表示一行默认文本条
  // 第三项：宽度 107px 的占位
  // 第四项：二维数组，表示一行两列，分别为 93px 和右边距 41px 的 32px 宽度占位
  const imageGroup = [
    { height: '171px' },
    1,
    { width: '107px' },
    [{ width: '93px' }, { width: '32px', marginLeft: '41px' }]
  ] as SkeletonRowCol[]
</script>
```

`rowCol` 数组中的每一项代表一行，数字 1 表示一行默认文本条，对象表示单列配置，二维数组表示多列布局。这种灵活的配置方式可以模拟几乎任意的页面结构。

### 示例 6：加载状态切换

效果说明：通过 `loading` 属性控制骨架屏与真实内容的切换，在数据加载完成后展示真实内容。

```vue
<template>
  <view>
    <view style="margin-bottom: 10px">切换显示</view>
    <wd-switch v-model="showContent" />
    <view style="height: 20px"></view>

    <!-- loading 为 true 时显示骨架屏，为 false 时显示真实内容 -->
    <wd-skeleton :row-col="grid" :loading="showContent">
      <wd-grid>
        <wd-grid-item icon-size="32px" icon="picture" text="文字" />
        <wd-grid-item icon-size="32px" icon="picture" text="文字" />
        <wd-grid-item icon-size="32px" icon="picture" text="文字" />
        <wd-grid-item icon-size="32px" icon="picture" text="文字" />
        <wd-grid-item icon-size="32px" icon="picture" text="文字" />
      </wd-grid>
    </wd-skeleton>
  </view>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'

  const showContent = ref(true)

  const grid = [
    [
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' },
      { width: '48px', height: '48px' }
    ],
    [
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' },
      { width: '48px', height: '16px' }
    ]
  ]
</script>
```

当 `loading` 为 `true` 或未传入时，组件显示骨架屏；当 `loading` 为 `false` 时，组件渲染默认插槽中的真实内容。在实际业务中，通常将接口请求的 loading 状态绑定到此属性上。

## 注意事项

1. **默认主题**：`theme` 属性默认值为 `text`。当不传入 `rowCol` 时，组件会根据 `theme` 渲染对应的预设布局。
2. **rowCol 优先级**：当同时传入 `theme` 和 `rowCol` 时，以 `rowCol` 为准。如果 `rowCol` 为空数组，则回退到 `theme` 的预设布局。
3. **loading 默认值**：`loading` 默认值为 `true`，即默认显示骨架屏。当数据加载完成后需要将 `loading` 设置为 `false` 才能显示真实内容。
4. **loading 为 undefined 的情况**：当 `loading` 未传入（值为 `undefined`）时，组件也会显示骨架屏（内部通过 `loading == undefined || loading === true` 判断）。
5. **animation 空值处理**：`animation` 默认值为空字符串 `''`，表示无动画效果。只有传入 `gradient` 或 `flashed` 时才会启用对应的动画。
6. **rowCol 数据格式**：`rowCol` 数组中的数字项会被转换为默认文本条（`type: 'text'`，宽度 100%）；对象项会被解析为单列布局；二维数组项会被解析为多列布局。
7. **size 属性**：在 `SkeletonRowColObj` 中，`size` 属性会同时设置 `width` 和 `height`，常用于头像、图标等正方形占位。
8. **样式单位**：`rowCol` 对象中的尺寸属性（`width`、`height`、`margin` 等）支持纯数字（默认单位为 `px`）或带单位的字符串（如 `'50%'`、`'2rem'`）。
9. **暗色模式适配**：组件在暗色模式下会自动调整骨架屏块的背景色，无需手动配置。
10. **虚拟宿主支持**：组件开启了 `virtualHost: true`，在小程序环境下可正确继承外部样式。同时启用 `addGlobalClass: true` 和 `styleIsolation: 'shared'`，支持全局样式穿透。
11. **行间距**：每行之间有默认的下边距（`$-skeleton-row-margin-bottom`），最后一行和唯一一行的下边距为 0。
12. **列形状默认样式**：`text` 类型宽度 100%、高度为 `$-skeleton-text-height-default`；`rect` 类型宽度 100%、高度为 `$-skeleton-rect-height-default`；`circle` 类型固定宽高为 `$-skeleton-circle-height-default`。
