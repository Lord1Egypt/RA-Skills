# Loading 加载


## 组件概况

Loading 加载组件是一个轻量级的视觉加载指示器组件，基于 SVG 动画实现，用于在数据加载、异步操作等场景中向用户提供视觉反馈。该组件支持三种不同的加载动画风格（ring 环形、outline 轮廓、spinner 旋转点阵），并提供颜色、尺寸等自定义配置选项。

组件采用 SVG 图片结合 CSS 旋转动画（`wd-rotate`）的方式实现，通过 `background-image` 将动态生成的 SVG 字符串渲染为加载动画。组件默认以 `inline-block` 方式布局，可灵活嵌入到各种容器中使用。

## 核心功能描述

- **三种动画类型**：内置 ring（默认）、outline、spinner 三种加载指示器样式，适用于不同视觉场景
- **颜色定制**：通过 `color` 属性设置加载指示器的主色调，支持十六进制、rgb/rgba 等 CSS 颜色值
- **尺寸控制**：通过 `size` 属性控制加载指示器的大小，支持带单位的字符串（如 `'30px'`）或纯数字（默认单位为 px）
- **渐变色彩**：ring 类型自动基于主色生成渐变色阶，实现更丰富的视觉效果
- **无限旋转动画**：所有类型均采用匀速无限循环的 360 度旋转动画（`wd-rotate`）
- **自定义样式**：支持通过 `custom-class` 和 `custom-style` 属性进行根节点样式定制

## 适用业务场景

- **数据加载**：在接口请求、数据拉取过程中展示加载状态
- **按钮加载**：在按钮提交操作后展示加载指示，防止重复提交
- **图片预加载**：在图片等资源加载完成前展示占位加载动画
- **模块加载中**：在页面局部模块、列表区域异步加载时作为轻提示
- **页面初始化**：在页面首次渲染数据时展示全局加载状态

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| type | string | 'ring' | 否 | 加载指示器类型，可选值：'ring' / 'outline' / 'spinner' |
| color | string | '#4D80F0' | 否 | 加载指示器颜色，支持 CSS 颜色值、十六进制色值等格式 |
| size | number / string | '' | 否 | 加载指示器大小，支持带单位的字符串（如 `'30px'`）或纯数字（默认单位为 px） |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### Slots

当前组件未定义插槽。

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。

### Events

当前组件未定义对外抛出的事件。

## 使用示例

### 示例 1：基础用法

效果说明：使用默认的 ring 类型加载指示器，采用默认颜色（`#4D80F0`）和默认尺寸。这是最基本的使用方式，适用于大多数常规加载场景。

```vue
<template>
  <view class="flex">
    <wd-loading />
  </view>
</template>

<style lang="scss" scoped>
.flex {
  display: flex;
  align-items: center;
}
</style>
```

### 示例 2：不同加载类型

效果说明：通过 `type` 属性切换三种不同的加载指示器样式。`outline` 类型呈现为渐隐轮廓环，适用于通用模块加载；`spinner` 类型呈现为旋转点阵图标，视觉更突出。

```vue
<template>
  <view class="flex">
    <!-- 默认 ring 类型 -->
    <wd-loading />

    <!-- outline 轮廓类型 -->
    <wd-loading type="outline" />

    <!-- spinner 旋转点阵类型 -->
    <wd-loading type="spinner" />
  </view>
</template>

<style lang="scss" scoped>
.flex {
  display: flex;
  align-items: center;
}
</style>
```

### 示例 3：修改颜色

效果说明：通过 `color` 属性自定义加载指示器颜色。适用于需要与品牌色、主题色保持一致的场景。ring 类型会自动基于主色生成渐变色阶，outline 和 spinner 类型使用纯色渲染。

```vue
<template>
  <view class="flex">
    <!-- ring 类型自定义颜色 -->
    <wd-loading color="#fa34aa" />

    <!-- spinner 类型自定义颜色 -->
    <wd-loading type="spinner" color="#fa34aa" />

    <!-- outline 类型自定义颜色 -->
    <wd-loading type="outline" color="#52c41a" />
  </view>
</template>

<style lang="scss" scoped>
.flex {
  display: flex;
  align-items: center;
}
</style>
```

### 示例 4：修改尺寸

效果说明：通过 `size` 属性控制加载指示器的大小。支持两种格式：纯数字（默认单位为 px）和带单位的字符串。适用于需要适配不同空间大小的场景。

```vue
<template>
  <view class="flex">
    <!-- 使用纯数字，默认单位 px -->
    <wd-loading :size="20" />
    <wd-loading :size="30" />

    <!-- 使用带单位的字符串 -->
    <wd-loading size="50px" />
  </view>

  <view class="flex mt-4">
    <!-- spinner 类型的不同尺寸 -->
    <wd-loading type="spinner" :size="20" />
    <wd-loading type="spinner" :size="30" />
    <wd-loading type="spinner" size="50px" />
  </view>
</template>

<style lang="scss" scoped>
.flex {
  display: flex;
  align-items: center;
}
.mt-4 {
  margin-top: 16px;
}
</style>
```

### 示例 5：组合使用

效果说明：将类型、颜色、尺寸等属性组合使用，实现更丰富的视觉效果。适用于有明确设计规范要求的场景。

```vue
<template>
  <view class="loading-container">
    <!-- 主题色 + 大尺寸 -->
    <wd-loading color="#409eff" :size="40" />

    <!-- 警告色 + outline 类型 -->
    <wd-loading type="outline" color="#e6a23c" :size="35" />

    <!-- 成功色 + spinner 类型 -->
    <wd-loading type="spinner" color="#67c23a" :size="30" />
  </view>
</template>

<style lang="scss" scoped>
.loading-container {
  display: flex;
  align-items: center;
  gap: 20px;
}
</style>
```

## 注意事项

1. **默认类型**：`type` 属性默认值为 `'ring'`，如果不传入 `type` 属性，组件将渲染 ring 类型的环形加载指示器。

2. **颜色渐变机制**：当使用 `ring` 类型时，组件会基于 `color` 属性值自动计算渐变色阶（基于 `#ffffff` 向主色插值生成），实现平滑的色彩过渡效果。`outline` 和 `spinner` 类型不使用渐变，仅使用纯色渲染。

3. **尺寸单位处理**：`size` 属性支持带单位的字符串（如 `'30px'`、`'2rem'`）和纯数字两种格式。当传入纯数字时，默认会添加 `px` 单位。如果传入空字符串（`''`），则使用组件默认尺寸。

4. **动画实现原理**：组件的旋转动画由 CSS 关键帧 `wd-rotate` 实现，从 0 度匀速旋转至 360 度，无限循环。动画应用在 `.wd-loading__body` 容器上，SVG 图片本身静止，通过外层容器旋转实现视觉效果。

5. **布局方式**：组件采用 `inline-block` 布局，默认尺寸继承自全局变量 `$-loading-size`。组件设置了 `font-size: 0` 和 `line-height: 0` 以避免内联元素带来的额外间距。

6. **自定义样式建议**：推荐使用 `custom-class` 和 `custom-style` 属性进行样式定制。如需调整组件间距，建议在外部使用 flex 容器配合 `gap` 属性或 margin 进行控制。

7. **SVG 渲染机制**：组件在 `onBeforeMount` 阶段生成 SVG 字符串并转换为 base64 编码的 data URI，通过 `background-image` 渲染。当 `type` 属性变化时会重新生成 SVG。

8. **虚拟宿主支持**：组件开启了 `virtualHost: true`，在小程序环境下可以正确继承外部样式。同时启用 `addGlobalClass: true` 和 `styleIsolation: 'shared'`，支持全局样式穿透。
