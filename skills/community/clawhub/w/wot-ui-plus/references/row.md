# Row 栅格布局


## 组件概况

Row 栅格布局组件由 `wd-row` 和 `wd-col` 两个关联组件组成，基于经典的 24 分栏栅格系统，用于快速构建灵活的页面布局。`wd-row` 作为行容器管理列间距与换行行为，`wd-col` 作为列元素控制宽度占比与偏移距离，两者配合使用可实现响应式、高自由度的页面排版。

## 核心功能描述

- **24 分栏系统**：采用 24 分栏设计，`span` 取值范围为 0~24，可灵活组合实现任意宽度比例
- **列间距控制**：通过 `gutter` 属性设置列元素之间的间距，单位为 px
- **列偏移**：通过 `offset` 属性实现列的左侧偏移，偏移量同样基于 24 分栏计算
- **自动换行**：通过 `wrap` 属性控制列元素是否自动换行，适用于动态内容场景
- **Flex 布局**：行容器基于 Flex 布局实现，列元素使用 float 浮动布局
- **数值校验**：组件内置对 `gutter`、`span`、`offset` 的合法性校验，非法值会在控制台输出警告

## 适用业务场景

- **表单布局**：多列表单字段的对齐排版，如两列、三列表单
- **信息卡片排列**：产品列表、新闻卡片等需要等宽或不等宽排列的场景
- **响应式页面结构**：页面主体与侧边栏的组合布局
- **数据看板**：统计面板、数据卡片的网格化展示
- **复杂页面骨架**：作为页面整体结构的布局骨架，嵌套其他业务组件

## API

### wd-row Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| gutter | number | `0` | 否 | 列元素之间的间距（单位为 px），必须大于等于 0 |
| wrap | boolean | `false` | 否 | 是否允许列元素自动换行 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### wd-col Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| span | number | `24` | 否 | 列元素宽度，基于 24 分栏系统，必须大于等于 0 |
| offset | number | `0` | 否 | 列元素左侧偏移距离，基于 24 分栏系统，必须大于等于 0 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### Events

组件不对外暴露任何事件。

### Methods

组件不对外暴露任何方法。

### Slots

#### wd-row Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 默认插槽，用于放置 `wd-col` 列元素 |

#### wd-col Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 默认插槽，用于放置任意内容（文字、图片、其他组件等） |

## 使用示例

### 示例 1：基础用法

展示不同分栏比例的布局效果，通过 `span` 属性控制每列的宽度占比。

```vue
<template>
  <view>
    <!-- 单列占满整行 -->
    <wd-row>
      <wd-col :span="24">
        <view class="bg-dark1">span: 24</view>
      </wd-col>
    </wd-row>

    <!-- 两列等分 -->
    <wd-row>
      <wd-col :span="12">
        <view class="bg-dark">span: 12</view>
      </wd-col>
      <wd-col :span="12">
        <view class="bg-light">span: 12</view>
      </wd-col>
    </wd-row>

    <!-- 三列等分 -->
    <wd-row>
      <wd-col :span="8">
        <view class="bg-dark">span: 8</view>
      </wd-col>
      <wd-col :span="8">
        <view class="bg-light">span: 8</view>
      </wd-col>
      <wd-col :span="8">
        <view class="bg-dark">span: 8</view>
      </wd-col>
    </wd-row>

    <!-- 四列等分 -->
    <wd-row>
      <wd-col :span="6">
        <view class="bg-dark">span: 6</view>
      </wd-col>
      <wd-col :span="6">
        <view class="bg-light">span: 6</view>
      </wd-col>
      <wd-col :span="6">
        <view class="bg-dark">span: 6</view>
      </wd-col>
      <wd-col :span="6">
        <view class="bg-light">span: 6</view>
      </wd-col>
    </wd-row>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .bg-dark1,
  .bg-dark,
  .bg-light {
    border-radius: 4px;
    min-height: 30px;
    text-align: center;
    line-height: 30px;
    font-size: 12px;
    margin-bottom: 10px;
    color: rgba(0, 0, 0, 0.45);
  }
  .bg-dark1 {
    background: #99a9bf;
    color: #fff;
  }
  .bg-dark {
    background: #d3dce6;
  }
  .bg-light {
    background: #e5e9f2;
  }
</style>
```

`span` 属性默认值为 24，表示列元素占满整行宽度。将多个列的 `span` 值相加等于 24 时，它们恰好铺满一行。常见的等分组合有：`12 + 12`（两列）、`8 + 8 + 8`（三列）、`6 + 6 + 6 + 6`（四列）。

### 示例 2：分栏偏移

通过 `offset` 属性实现列的左侧偏移，用于创建不对称布局或居中效果。

```vue
<template>
  <view>
    <!-- 第二列偏移 4 栏 -->
    <wd-row>
      <wd-col :span="4">
        <view class="bg-dark">span: 4</view>
      </wd-col>
      <wd-col :span="8" :offset="4">
        <view class="bg-light">span: 8 offset: 4</view>
      </wd-col>
    </wd-row>

    <!-- 两列分别偏移 4 栏 -->
    <wd-row>
      <wd-col :span="8" :offset="4">
        <view class="bg-dark">span: 8 offset: 4</view>
      </wd-col>
      <wd-col :span="8" :offset="4">
        <view class="bg-light">span: 8 offset: 4</view>
      </wd-col>
    </wd-row>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .bg-dark,
  .bg-light {
    border-radius: 4px;
    min-height: 30px;
    text-align: center;
    line-height: 30px;
    font-size: 12px;
    margin-bottom: 10px;
    color: rgba(0, 0, 0, 0.45);
  }
  .bg-dark {
    background: #d3dce6;
  }
  .bg-light {
    background: #e5e9f2;
  }
</style>
```

`offset` 属性的计算方式与 `span` 相同，均基于 24 分栏系统。例如 `offset="4"` 表示向左偏移 4/24 的宽度。偏移量与 `span` 值之和不应超过 24，否则会导致布局溢出。

### 示例 3：分栏间隔

通过 `gutter` 属性为列元素之间添加间距，使布局更加舒展。

```vue
<template>
  <view>
    <wd-row :gutter="20">
      <wd-col :span="8">
        <view class="bg-dark">span: 8</view>
      </wd-col>
      <wd-col :span="8">
        <view class="bg-light">span: 8</view>
      </wd-col>
      <wd-col :span="8">
        <view class="bg-dark">span: 8</view>
      </wd-col>
    </wd-row>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .bg-dark,
  .bg-light {
    border-radius: 4px;
    min-height: 30px;
    text-align: center;
    line-height: 30px;
    font-size: 12px;
    margin-bottom: 10px;
    color: rgba(0, 0, 0, 0.45);
  }
  .bg-dark {
    background: #d3dce6;
  }
  .bg-light {
    background: #e5e9f2;
  }
</style>
```

设置 `gutter="20"` 后，`wd-row` 会自动在左右两侧各设置 -10px 的外边距（负值），同时每个 `wd-col` 在左右两侧各设置 10px 的内边距，从而实现列与列之间 20px 的间距效果。注意 `gutter` 值必须大于等于 0，否则会输出错误日志。

### 示例 4：混合比例布局

结合实际业务场景，展示不同宽度比例的混合布局。

```vue
<template>
  <view>
    <!-- 主内容区 + 侧边栏（3:1 比例） -->
    <wd-row :gutter="16">
      <wd-col :span="18">
        <view class="content-card">主内容区域</view>
      </wd-col>
      <wd-col :span="6">
        <view class="sidebar-card">侧边栏</view>
      </wd-col>
    </wd-row>

    <!-- 三栏不等宽布局 -->
    <wd-row :gutter="16">
      <wd-col :span="4">
        <view class="nav-card">导航</view>
      </wd-col>
      <wd-col :span="16">
        <view class="content-card">内容区</view>
      </wd-col>
      <wd-col :span="4">
        <view class="tool-card">工具区</view>
      </wd-col>
    </wd-row>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .content-card,
  .sidebar-card,
  .nav-card,
  .tool-card {
    border-radius: 4px;
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.65);
  }
  .content-card {
    background: #d3dce6;
  }
  .sidebar-card {
    background: #e5e9f2;
  }
  .nav-card {
    background: #99a9bf;
    color: #fff;
  }
  .tool-card {
    background: #e5e9f2;
  }
</style>
```

### 示例 5：内容嵌套

在列元素中嵌套任意业务组件或自定义内容。

```vue
<template>
  <view>
    <wd-row :gutter="12">
      <wd-col :span="8">
        <view class="card">
          <view class="card-title">卡片一</view>
          <view class="card-desc">这是栅格布局中的自定义内容</view>
        </view>
      </wd-col>
      <wd-col :span="8">
        <view class="card">
          <view class="card-title">卡片二</view>
          <view class="card-desc">支持嵌套任意组件</view>
        </view>
      </wd-col>
      <wd-col :span="8">
        <view class="card">
          <view class="card-title">卡片三</view>
          <view class="card-desc">灵活的布局方案</view>
        </view>
      </wd-col>
    </wd-row>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .card {
    border-radius: 8px;
    padding: 16px;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
  .card-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }
  .card-desc {
    font-size: 12px;
    color: #999;
  }
</style>
```

## 注意事项

1. **分栏总和规则**：一行内所有列的 `span` 值之和应等于 24，若超过 24 则超出部分会自动换行（需配合 `wrap` 属性）或溢出容器
2. **gutter 必须大于等于 0**：`gutter` 属性值小于 0 时，组件会输出错误日志到控制台，且不会产生预期间距效果
3. **span/offset 必须大于等于 0**：`span` 和 `offset` 属性值小于 0 时，组件会输出错误日志到控制台
4. **gutter 间距实现原理**：设置 `gutter` 后，`wd-row` 会添加左右负外边距（值为 `gutter / 2`），`wd-col` 会添加左右内边距（值为 `gutter / 2`），列内容的 `background-clip` 设为 `content-box`，确保背景色不覆盖间距区域
5. **wrap 属性控制换行**：默认 `wrap` 为 `false`，列元素不会自动换行；设置为 `true` 时，列元素会在超过容器宽度时自动换行，适用于列数不固定的动态场景
6. **默认 span 值为 24**：不设置 `span` 属性时，`wd-col` 默认占满整行宽度（24/24）
7. **float 布局实现**：列元素底层使用 `float: left` 实现浮动布局，行容器使用 Flex 布局，并在行末通过 `::after` 伪元素清除浮动
8. **customStyle 与 customClass 的使用**：通过 `customStyle` 和 `customClass` 可以对 `wd-row` 和 `wd-col` 进行自定义样式扩展，建议在列元素的内容区域设置样式，避免覆盖组件内部的定位逻辑
