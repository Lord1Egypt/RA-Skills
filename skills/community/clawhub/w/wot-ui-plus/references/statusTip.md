# StatusTip 状态提示


## 组件概况

StatusTip 状态提示组件是一个用于展示页面缺省状态的视觉反馈组件，通常用于空页面、网络异常、搜索无结果、支付失败等场景。该组件内置了 7 种常见的预设图片类型，支持自定义图片 URL、图片尺寸、裁剪模式以及自定义提示文案，并提供了 `image` 和 `bottom` 两个插槽用于高度自定义内容。

组件采用 flex 列式布局，图片与提示文案垂直居中对齐，结构简洁且易于扩展。

## 核心功能描述

- **预设图片类型**：内置 7 种常见场景图片：`search`（搜索无结果）、`network`（网络异常）、`content`（页面无内容）、`collect`（我的收藏为空）、`comment`（我的评论为空）、`halo`（支付失败）、`message`（消息订阅）
- **自定义图片 URL**：`image` 属性可直接传入完整的图片网络地址，覆盖预设类型
- **图片尺寸控制**：`imageSize` 属性支持数字、字符串或 `ImageSize` 对象（包含 `width` 和 `height`），灵活控制图片大小，默认尺寸为 160px x 160px
- **图片裁剪模式**：`imageMode` 属性支持设置图片的裁剪、缩放模式，默认值为 `aspectFill`
- **路径前缀配置**：`urlPrefix` 属性用于设置图片路径前缀，默认指向 `./../../static/images/`，推荐将图片部署到自己的服务器并通过此属性配置
- **自定义提示文案**：`tip` 属性用于设置图片下方的提示文字，支持多行文字自动换行
- **image 插槽**：通过 `#image` 插槽完全自定义图片区域内容，可渲染任意组件（如 `wd-icon`）
- **bottom 插槽**：通过 `#bottom` 插槽在提示文案下方插入操作区域（如按钮、链接等）
- **自定义样式**：支持通过 `custom-class` 和 `custom-style` 属性进行根节点样式定制
- **暗色模式支持**：内置 dark 主题样式，文字颜色自动切换为 `$-dark-color3`

## 适用业务场景

- **搜索无结果**：当用户搜索关键词但未匹配到任何结果时，展示搜索无结果的缺省页
- **网络异常**：当网络请求失败或网络不可用时，展示网络异常的提示页面
- **空数据页面**：当列表、收藏、评论等数据为空时，展示对应的缺省提示
- **操作失败**：如支付失败、订单取消等场景，展示操作结果的提示页面
- **自定义业务场景**：通过自定义图片 URL 或插槽，适配任何业务需要的缺省状态

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| image | string | 'network' | 否 | 缺省图片类型，支持传入图片 URL。可选值：`search`、`network`、`content`、`collect`、`comment`、`halo`、`message` |
| imageSize | string \| number \| ImageSize | '' | 否 | 图片大小。传入数字或字符串时宽高相等；传入对象时可分别设置 `width` 和 `height`，单位为 `px`（默认） |
| tip | string | '' | 否 | 提示文案，显示在图片下方 |
| imageMode | string | 'aspectFill' | 否 | 图片裁剪、缩放的模式，可选值参考小程序 image 组件的 mode 属性 |
| urlPrefix | string | './../../static/images/' | 否 | 图片路径前缀，用于拼接预设图片的 URL。推荐将图片放到自己的服务器上并设置此属性 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### ImageSize 类型

```ts
type ImageSize = {
  width: number | string
  height: number | string
}
```

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
| --- | --- | --- |
| image | - | 自定义图片区域内容，当传入此插槽时将替代内部的图片渲染逻辑 |
| bottom | - | 自定义底部操作区域内容，渲染在提示文案下方 |

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。

### Events

当前组件未定义对外抛出的事件。

## 使用示例

### 示例 1：基础用法

效果说明：使用预设的图片类型和提示文案，展示常见的缺省状态。以下为多种业务场景的用法：

```vue
<template>
  <view>
    <!-- 搜索无结果 -->
    <wd-status-tip image="search" tip="当前搜索无结果" />

    <!-- 网络异常 -->
    <wd-status-tip image="network" tip="当前网络不可用，请检查你的网络设置" />

    <!-- 页面无内容 -->
    <wd-status-tip image="content" tip="暂无内容" />

    <!-- 我的收藏为空 -->
    <wd-status-tip image="collect" tip="暂无收藏" />

    <!-- 我的评论为空 -->
    <wd-status-tip image="comment" tip="暂无评论" />

    <!-- 支付失败 -->
    <wd-status-tip image="halo" tip="支付失败，请重新订购" />

    <!-- 消息订阅 -->
    <wd-status-tip image="message" tip="已订阅全部消息" />
  </view>
</template>

<script lang="ts" setup>
  // 无需额外逻辑，image 属性使用预设类型名称即可
</script>
```

`image` 属性支持 7 种预设值：`search`、`network`、`content`、`collect`、`comment`、`halo`、`message`。组件会根据 `urlPrefix` 自动拼接图片 URL，如 `urlPrefix + 'search.png'`。默认 `image` 值为 `network`，即网络异常图片。

### 示例 2：自定义图片尺寸

效果说明：通过 `imageSize` 属性自定义图片的宽高。支持传入数字、字符串或对象。

```vue
<template>
  <view>
    <!-- 传入对象，分别设置宽高 -->
    <wd-status-tip
      image="search"
      tip="当前搜索无结果"
      :image-size="{
        width: 300,
        height: 200
      }"
    />

    <!-- 传入字符串，宽高相等 -->
    <wd-status-tip image="search" tip="当前搜索无结果" image-size="120px" />
  </view>
</template>

<script lang="ts" setup>
  // 无需额外逻辑
</script>
```

当 `imageSize` 传入对象时，可分别设置 `width` 和 `height`；当传入数字或字符串时，宽高会设置为相同的值。默认图片尺寸为 160px x 160px。

### 示例 3：自定义图片 URL

效果说明：`image` 属性可直接传入完整的图片网络地址，用于展示自定义的图片内容。

```vue
<template>
  <view>
    <wd-status-tip
      image="https://example.com/avatar.jpg"
      tip="查看我的头像"
    />
  </view>
</template>

<script lang="ts" setup>
  // image 传入完整 URL 时，不会与 urlPrefix 拼接
</script>
```

当 `image` 的值不是 7 种预设类型之一时，组件会直接将其作为完整的图片 URL 使用，不会与 `urlPrefix` 进行拼接。

### 示例 4：使用 image 插槽自定义图片

效果说明：通过 `#image` 插槽完全自定义图片区域的内容，可以渲染图标、组件等任意内容。

```vue
<template>
  <view>
    <wd-status-tip tip="使用插槽自定义图片内容">
      <template #image>
        <wd-icon name="logo-tw" size="100px"></wd-icon>
      </template>
    </wd-status-tip>
  </view>
</template>

<script lang="ts" setup>
  // 当传入 #image 插槽时，内置的图片渲染逻辑将被完全替代
</script>
```

当传入 `#image` 插槽内容时，组件会优先渲染插槽内容，不再渲染内部的 `wd-img` 组件。这为自定义图片区域提供了最大的灵活性。

### 示例 5：使用 bottom 插槽添加操作按钮

效果说明：通过 `#bottom` 插槽在提示文案下方添加操作区域，如重新加载按钮、跳转链接等。

```vue
<template>
  <view>
    <wd-status-tip image="content" tip="当前搜索无结果">
      <template #bottom>
        <view class="bottom-actions">
          <wd-button type="info">重新加载</wd-button>
        </view>
      </template>
    </wd-status-tip>
  </view>
</template>

<script lang="ts" setup>
  // 无需额外逻辑
</script>

<style lang="scss" scoped>
.bottom-actions {
  margin-top: var(--wot-statustip-bottom-margin-top, 20px);
  display: flex;
  justify-content: center;
  width: 100%;
}
</style>
```

`#bottom` 插槽渲染在提示文案下方，适合放置操作按钮、跳转链接等交互元素。默认提示文案与底部插槽之间没有额外间距，可通过 CSS 变量 `--wot-statustip-bottom-margin-top` 或自定义样式控制间距。

## 注意事项

1. **图片类型匹配**：当 `image` 属性的值为 7 种预设类型之一（`search`、`network`、`content`、`collect`、`comment`、`halo`、`message`）时，组件会将其与 `urlPrefix` 拼接为完整 URL（如 `urlPrefix + 'search.png'`）。其他值则直接作为图片 URL 使用。
2. **urlPrefix 默认值**：`urlPrefix` 默认值为 `./../../static/images/`，指向项目本地静态资源目录。建议将预设图片部署到自己的 CDN 或服务器，并通过此属性配置路径，以减少小程序包体积。
3. **imageSize 单位**：`imageSize` 传入数字时默认单位为 `px`。传入对象时，`width` 和 `height` 也支持数字或字符串。空字符串表示不设置自定义尺寸，使用默认 160px x 160px。
4. **插槽优先级**：当传入 `#image` 插槽时，内置的 `wd-img` 组件将被完全替代。如果未传入 `#image` 插槽且 `imgUrl` 计算结果为空字符串，则图片区域不会渲染。
5. **imageMode 默认值**：图片裁剪模式默认值为 `aspectFill`，表示保持纵横比缩放图片，完全覆盖显示区域并可能裁剪。可根据需要设置为 `aspectFit`、`widthFix` 等模式。
6. **暗色模式适配**：组件在暗色模式下会自动调整文字颜色，无需手动配置。背景色由外部容器控制。
7. **文本换行**：提示文案使用 `overflow-wrap: break-word` 实现长文本自动换行，确保超长文案不会溢出容器。
8. **布局结构**：组件采用 `flex` 列式布局，图片与文案垂直居中对齐。根容器设置了 `width: 100%` 和 `margin: 0 auto`，默认宽度撑满父容器。
9. **虚拟宿主支持**：组件开启了 `virtualHost: true`，在小程序环境下可正确继承外部样式。同时启用 `addGlobalClass: true` 和 `styleIsolation: 'shared'`，支持全局样式穿透。
10. **图片加载**：内置图片使用 `wd-img` 组件渲染，继承了 `wd-img` 的图片加载能力和模式支持。自定义 URL 图片需要确保网络可达。
