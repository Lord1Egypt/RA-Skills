# Divider 分割线


## 组件概况

Divider 分割线组件用于在页面或内容区块之间创建视觉分隔，帮助用户区分不同的内容模块。该组件支持水平和垂直两种方向，提供实线与虚线样式选择，并支持在分割线中插入文字或图标等自定义内容，可灵活控制内容位置与颜色，适用于多种布局场景，是构建清晰信息层级不可或缺的界面元素。

## 核心功能描述

- **方向切换**：支持水平分割线（默认）与垂直分割线，适配不同布局需求
- **实线与虚线**：默认显示实线，通过 `dashed` 属性可切换为虚线样式
- **Hairline 细线**：默认显示 0.5px 的细线效果，提升视觉精致度
- **内容展示**：支持在分割线中间插入文字、图标等自定义内容
- **内容位置控制**：水平分割线可设置内容居左、居中或居右对齐
- **自定义颜色**：支持自定义文字和线条颜色
- **暗色模式支持**：内置 dark 主题样式，自动跟随系统主题切换

## 适用业务场景

- **内容分隔**：在列表项、段落或功能模块之间添加分割线，区分不同内容区域
- **信息层级划分**：在详情页中使用分割线划分基本信息、详细描述、评论等不同层级
- **垂直元素分隔**：在导航栏、工具栏等水平排列的元素之间使用垂直分割线进行视觉区分
- **数据分组展示**：在表格或卡片列表中使用分割线对数据进行分组展示

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| color | string | - | 否 | 自定义分割线及内容颜色 |
| contentPosition | string | 'center' | 否 | 内容位置，可选值为 `left`、`center`、`right` |
| dashed | boolean | false | 否 | 是否显示为虚线 |
| vertical | boolean | false | 否 | 是否为垂直分割线 |
| hairline | boolean | true | 否 | 是否显示为 0.5px 的细线 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### Events

组件不对外暴露任何事件。

### Methods

组件不对外暴露任何方法。

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 自定义分割线中间的内容，可插入文字、图标或其他组件。仅在水平分割线（`vertical` 为 `false`）时生效 |

## 使用示例

### 示例 1：基础用法

最基础的分割线用法，展示实线细线效果。

```vue
<template>
  <view>
    <wd-divider></wd-divider>
    <wd-divider :hairline="false"></wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

第一条分割线默认开启 `hairline` 属性，显示为 0.5px 的细线；第二条分割线关闭 `hairline`，显示为常规宽度的分割线。

### 示例 2：展示文本

在分割线中间插入文字内容，默认居中显示。

```vue
<template>
  <view>
    <wd-divider>展示文本</wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过默认插槽插入文本内容，文本两侧会自动延伸出分割线，形成内容居中的分割效果。

### 示例 3：自定义渲染内容

在分割线中间插入图标等自定义内容。

```vue
<template>
  <view>
    <wd-divider>
      <wd-icon name="down" size="20" />
    </wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

该示例在分割线中间插入了一个向下箭头图标，适用于需要引导用户注意力的场景，如展开更多内容提示等。

### 示例 4：内容位置

控制分割线中文字或内容的对齐位置。

```vue
<template>
  <view>
    <wd-divider>中间</wd-divider>
    <wd-divider content-position="left">左侧</wd-divider>
    <wd-divider content-position="right">右侧</wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `contentPosition` 属性可以控制内容的位置，可选值为 `left`（左侧）、`center`（居中，默认值）、`right`（右侧）。内容位置的设置仅在水平分割线且存在插槽内容时生效。

### 示例 5：虚线分割

展示虚线样式的分割线效果。

```vue
<template>
  <view>
    <wd-divider dashed></wd-divider>
    <wd-divider dashed>虚线分割</wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `dashed` 属性可将分割线设置为虚线样式，适用于需要弱化分隔感或表示可选/非强制内容的场景。

### 示例 6：自定义颜色

自定义分割线及文字的颜色。

```vue
<template>
  <view>
    <wd-divider color="#4D80F0">自定义颜色</wd-divider>
  </view>
</template>
<script lang="ts" setup>
</script>
```

通过 `color` 属性可同时修改分割线和文字的颜色，适用于需要与主题色保持一致或强调特定分隔区域的场景。

### 示例 7：垂直分割线

在水平排列的元素之间使用垂直分割线进行视觉分隔。

```vue
<template>
  <view>
    <view class="content">
      <text>文本</text>
      <wd-divider vertical />
      <text>文本</text>
      <wd-divider vertical dashed />
      <text>文本</text>
      <wd-divider vertical :hairline="false" />
      <text>文本</text>
      <wd-divider vertical color="#1989fa" />
      <text>文本</text>
    </view>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .content {
    padding: 12rpx 15px;
  }
</style>
```

垂直分割线通过 `vertical` 属性开启，适用于工具栏、导航菜单等水平排列元素的视觉分隔。垂直模式下支持虚线、细线、自定义颜色等所有基础属性，但不支持插入内容插槽。

## 注意事项

1. **垂直分割线不支持内容插槽**：当 `vertical` 设置为 `true` 时，默认插槽内容不会渲染，垂直分割线仅作为纯分割线使用
2. **内容位置仅水平模式生效**：`contentPosition` 属性仅在水平分割线（`vertical` 为 `false`）且存在插槽内容时生效
3. **hairline 默认开启**：默认情况下分割线显示为 0.5px 的细线效果，如需常规宽度线条需显式设置 `hairline` 为 `false`
4. **customStyle 优先级**：通过 `customStyle` 设置的样式会与组件内部样式合并，优先级高于默认样式
5. **暗色模式适配**：组件已内置暗色主题样式，颜色值会自动适配系统主题，无需额外配置
6. **垂直分割线对齐方式**：垂直分割线使用 `display: inline-block` 和 `vertical-align: middle`，与相邻文本元素自然居中对齐
