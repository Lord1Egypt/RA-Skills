# Gap 间距


## 组件概况

Gap 间距组件是一个用于在页面中创建垂直间隔的空隙组件。该组件通过设置高度和背景颜色，能够在不同内容区域之间提供灵活的间距控制，同时支持底部安全区适配，适用于需要精确控制页面布局间距的场景。

组件采用极简设计，渲染为一个空的 `view` 容器，通过高度属性控制间隔大小，支持背景颜色填充，可作为视觉分隔或布局占位使用。

## 核心功能描述

- **自定义高度**：通过 `height` 属性设置间距高度，默认值为 `15`，支持带单位的字符串（如 `'20px'`、`'30rpx'`）或纯数字（默认单位为 px）
- **背景颜色**：通过 `bg-color` 属性设置背景色，默认为 `transparent`（透明），可设置为任意颜色值用于视觉分隔
- **底部安全区适配**：通过 `safe-area-bottom` 属性开启底部安全区支持，自动适配刘海屏、全面屏等设备的底部安全区域
- **样式定制**：支持通过 `custom-class` 和 `custom-style` 属性进行自定义样式扩展

## 适用业务场景

- **内容分隔**：在不同模块或内容区块之间创建视觉间隔
- **底部占位**：为固定定位的底部导航栏、操作栏预留空间
- **安全区适配**：在全面屏设备底部创建包含安全区域的间距
- **视觉分隔线**：通过设置背景颜色替代传统的分隔线组件
- **弹性布局填充**：在 flex 或 grid 布局中作为灵活的填充元素

## API

### Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| height | 间距高度，支持带单位的字符串或纯数字（默认单位为 px） | number / string | - | 15 | - |
| bgColor | 背景颜色 | string | - | transparent | - |
| safeAreaBottom | 是否开启底部安全区适配 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### Slots

组件未定义插槽。

### Methods

组件未暴露外部可调用的方法。

### Events

组件未定义对外抛出的事件。

## 使用示例

### 基本使用

默认情况下，Gap 组件会使用透明背景和 15px 的高度创建间距。可以通过 `bg-color` 属性设置背景颜色，使其在视觉上更加明显。

```vue
<template>
  <wd-gap bg-color="#FFFFFF"></wd-gap>
</template>
```

### 自定义背景颜色

通过 `bg-color` 属性设置任意背景颜色，可用于创建带颜色的分隔区域。

```vue
<template>
  <wd-gap bg-color="#4D80F0"></wd-gap>
</template>
```

### 自定义高度

通过 `height` 属性自定义间距高度，支持带单位的字符串（如 `rpx`、`px`、`vh` 等）或纯数字。

```vue
<template>
  <wd-gap bg-color="#4D80F0" height="120rpx"></wd-gap>
</template>
```

### 自定义样式

通过 `custom-class` 属性为组件添加自定义样式类，实现更灵活的样式定制。

```vue
<template>
  <wd-gap custom-class="custom-gap"></wd-gap>
</template>

<style lang="scss" scoped>
  :deep(.custom-gap) {
    padding-bottom: 120rpx;
    background: #34d19d !important;
  }
</style>
```

### 底部安全区

在全面屏设备中，通过 `safe-area-bottom` 属性开启底部安全区适配，避免内容被设备底部手势操作区域遮挡。可配合固定定位使用。

```vue
<template>
  <wd-gap bg-color="#333333" safe-area-bottom height="220rpx"></wd-gap>
</template>

<style lang="scss" scoped>
  :deep(.custom-safe-area-bottom) {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
  }
</style>
```

## 注意事项

1. **默认透明背景**：Gap 组件默认背景色为 `transparent`，如果仅需要创建空白间距，无需设置 `bg-color` 属性。

2. **高度单位**：`height` 属性支持纯数字和带单位的字符串。传入纯数字时默认单位为 `px`，如需使用其他单位（如 `rpx`、`vh` 等），请传入带单位的字符串，例如 `"120rpx"`。

3. **底部安全区适配**：开启 `safe-area-bottom` 后，组件会通过 CSS 的 `padding-bottom: env(safe-area-inset-bottom)` 自动适配设备底部安全区域。该功能在需要为固定底部元素预留空间的场景中非常实用。

4. **固定定位配合**：当 Gap 组件用于为固定定位的底部元素预留空间时，建议将组件本身也设置为固定定位，以确保间距始终位于页面底部。

5. **样式定制优先级**：使用 `custom-class` 进行样式定制时，如需覆盖默认背景色，可能需要使用 `!important` 来确保样式生效，因为组件的内联样式优先级较高。

6. **组件定位**：Gap 组件默认采用普通文档流布局，如需特殊定位（如固定定位、绝对定位），请通过 `custom-class` 或 `custom-style` 进行设置。

7. **无内容组件**：Gap 组件不包含任何插槽或子元素，仅作为空白的间隔元素使用。如需在间隔中添加内容，建议使用其他布局组件。

8. **虚拟主机配置**：组件内部配置了 `virtualHost: true`，这意味着组件的根节点样式会直接生效，无需考虑额外的包装元素影响。
