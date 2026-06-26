# Tabbar 标签栏


## 组件概况

Tabbar 标签栏组件用于在应用底部展示多个导航入口，支持通过 `wd-tabbar` 容器组件配合 `wd-tabbar-item` 子项组件共同使用。支持图标、文字、徽标提示等多种展示方式，提供默认和悬浮圆角两种形状，以及自定义颜色、固定定位、底部安全区适配等功能，适用于应用底部主导航等场景。

## 核心功能描述

- **v-model 双向绑定**：支持通过 `v-model` 双向绑定当前激活的标签索引或名称
- **名称匹配**：子项可通过 `name` 属性设置唯一标识符，使用名称代替索引进行匹配
- **图标与文字**：子项支持通过 `icon` 属性设置图标名称，通过 `title` 属性设置文字，也可通过 `icon` 插槽自定义图标内容
- **徽标提示**：支持数字徽标（`value`）、点状徽标（`is-dot`）、徽标最大值（`max`，默认 99）
- **徽标透传**：通过 `badge-props` 属性透传完整配置到内部 Badge 组件
- **两种形状**：`default`（常规底部贴底样式）和 `round`（悬浮圆角卡片样式）
- **颜色定制**：通过 `active-color` 和 `inactive-color` 分别设置激活和未激活状态的文字与图标颜色
- **固定定位**：通过 `fixed` 属性将标签栏固定在页面底部，配合 `placeholder` 可生成占位元素
- **安全区适配**：通过 `safe-area-inset-bottom` 属性自动适配 iPhone X 等机型的底部安全区
- **顶部边框**：默认显示 0.5px 的顶部边框，可通过 `bordered` 属性关闭
- **change 事件监听**：切换标签时触发 `change` 事件，返回当前激活项的标识

## 适用业务场景

- **应用底部主导航**：电商、资讯、社交等应用的核心页面切换入口（首页、分类、购物车、我的等）
- **带数量提示的导航**：购物车商品数、未读消息数、新内容提醒等需要数字徽标的场景
- **新内容提醒**：使用点状徽标标识新功能、新活动等需要用户注意的入口
- **悬浮导航栏**：使用 `round` 形状打造悬浮胶囊效果，适用于沉浸式设计风格的页面
- **固定底部导航**：内容超出屏幕滚动时，使用 `fixed` 属性保持导航始终可见
- **自定义图标导航**：使用自定义图片替代图标字体，实现品牌化图标效果

## API

### wd-tabbar Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | string \| number | 0 | 否 | 选中标签的索引值或者名称，支持 v-model 双向绑定 |
| fixed | boolean | false | 否 | 是否固定在底部 |
| bordered | boolean | true | 否 | 是否显示顶部边框 |
| safeAreaInsetBottom | boolean | false | 否 | 是否设置底部安全距离（iPhone X 类型的机型） |
| shape | `'default' \| 'round'` | `'default'` | 否 | 标签栏的形状 |
| activeColor | string | - | 否 | 激活标签的颜色 |
| inactiveColor | string | - | 否 | 未激活标签的颜色 |
| placeholder | boolean | false | 否 | 固定在底部时，是否在标签位置生成一个等高的占位元素 |
| zIndex | number | 99 | 否 | 自定义组件的层级 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### wd-tabbar-item Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| title | string | - | 否 | 标签页的标题 |
| name | string \| number | - | 否 | 唯一标识符，用于通过名称匹配当前激活项 |
| icon | string | - | 否 | 图标类名 |
| value | string \| number \| null | null | 否 | 徽标显示值 |
| isDot | boolean | undefined | 否 | 是否为点状徽标 |
| max | number | - | 否 | 徽标最大值，超出则显示"最大值+" |
| badgeProps | BadgeProps | - | 否 | 徽标属性，透传给 Badge 组件 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

### wd-tabbar Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| change | `{ value: string \| number }` | 切换标签时触发，返回当前激活项的标识（索引或名称） |

### wd-tabbar-item Events

组件不对外暴露任何事件。

### wd-tabbar Methods

组件不对外暴露任何方法。

### wd-tabbar-item Methods

组件不对外暴露任何方法。

### wd-tabbar Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 放置 wd-tabbar-item 子项组件 |

### wd-tabbar-item Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| icon | `{ active: boolean }` | 自定义图标内容，可根据激活状态展示不同图标或图片 |

## 使用示例

### 示例 1：基础用法

展示底部标签栏的基本结构，包含图标和文字。

```vue
<template>
  <view>
    <wd-tabbar v-model="activeTab" bordered @change="handleChange">
      <wd-tabbar-item title="首页" icon="home"></wd-tabbar-item>
      <wd-tabbar-item title="分类" icon="cart"></wd-tabbar-item>
      <wd-tabbar-item title="我的" icon="user"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log('当前切换至', event)
  }
</script>
```

`wd-tabbar` 作为容器，内部放置多个 `wd-tabbar-item` 子项。通过 `v-model` 绑定当前激活的标签索引（默认从 0 开始）。`icon` 属性设置图标类名，`title` 属性设置文字标签。切换标签时触发 `change` 事件，返回包含当前激活标识的 `{ value }` 对象。

### 示例 2：通过名称匹配

使用 `name` 属性为每个标签设置唯一标识，便于路由跳转等场景使用。

```vue
<template>
  <view>
    <wd-tabbar v-model="activeTab" bordered @change="handleChange">
      <wd-tabbar-item name="home" title="首页" icon="home"></wd-tabbar-item>
      <wd-tabbar-item name="cart" title="分类" icon="cart"></wd-tabbar-item>
      <wd-tabbar-item name="setting" title="设置" icon="setting"></wd-tabbar-item>
      <wd-tabbar-item name="user" title="我的" icon="user"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref('home')

  function handleChange({ value }: { value: string }) {
    console.log('当前切换至', value)
  }
</script>
```

通过为每个 `wd-tabbar-item` 设置 `name` 属性，可以使用语义化的名称（如 `'home'`、`'cart'`）代替数字索引来标识当前激活项。`v-model` 的值和 `change` 事件的回调值均为对应的 `name`。未设置 `name` 时默认使用子项在容器中的索引值。

### 示例 3：徽标提示

展示数字徽标、点状徽标以及徽标最大值的用法。

```vue
<template>
  <view>
    <wd-tabbar v-model="activeTab" @change="handleChange">
      <!-- 点状徽标 -->
      <wd-tabbar-item
        is-dot
        :value="2"
        title="点状"
        icon="home"
      ></wd-tabbar-item>

      <!-- 小数字徽标 -->
      <wd-tabbar-item :value="2" icon="cart" title="分类"></wd-tabbar-item>

      <!-- 普通数字徽标 -->
      <wd-tabbar-item :value="30" title="我的" icon="user"></wd-tabbar-item>

      <!-- 超出最大值的徽标（默认最大值99） -->
      <wd-tabbar-item :value="200" title="最大值" icon="user"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log(event)
  }
</script>
```

`value` 属性设置徽标显示的数字，`is-dot` 属性将徽标显示为小红点。徽标的默认最大值为 99，超过最大值的数字会显示为 `"99+"`。通过 `max` 属性可自定义最大值。`value` 为 `null` 时不显示徽标。

### 示例 4：悬浮标签栏

使用 `round` 形状创建悬浮圆角卡片风格的标签栏。

```vue
<template>
  <view>
    <wd-tabbar
      shape="round"
      v-model="activeTab"
      @change="handleChange"
    >
      <wd-tabbar-item title="首页" icon="home"></wd-tabbar-item>
      <wd-tabbar-item title="分类" icon="cart"></wd-tabbar-item>
      <wd-tabbar-item title="相册" icon="photo"></wd-tabbar-item>
      <wd-tabbar-item title="我的" icon="user"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log(event)
  }
</script>
```

设置 `shape="round"` 后，标签栏呈现为悬浮圆角卡片样式，左右两侧留有 32rpx 边距，底部带有阴影效果。圆角标签栏固定在底部时会自动适配底部安全区，无需额外设置 `safeAreaInsetBottom`。

### 示例 5：自定义图标

通过 `icon` 插槽自定义图标内容，支持使用自定义图片替代图标字体。

```vue
<template>
  <view>
    <wd-tabbar v-model="activeTab" @change="handleChange">
      <wd-tabbar-item :value="2" title="首页" icon="home"></wd-tabbar-item>

      <!-- 自定义图片图标 -->
      <wd-tabbar-item :value="2" icon="cart" title="分类">
        <template #icon>
          <wd-img
            round
            height="40rpx"
            width="40rpx"
            src="https://wot-ui-plus.cn/assets/panda.jpg"
          ></wd-img>
        </template>
      </wd-tabbar-item>

      <wd-tabbar-item :value="3" title="我的" icon="user"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log(event)
  }
</script>
```

当 `wd-tabbar-item` 提供了 `icon` 插槽时，会忽略 `icon` 属性，使用插槽内容作为图标。`icon` 插槽提供 `{ active: boolean }` 作用域参数，可根据激活状态展示不同的图标或样式。

### 示例 6：自定义颜色

通过 `active-color` 和 `inactive-color` 自定义激活和未激活状态的颜色。

```vue
<template>
  <view>
    <wd-tabbar
      v-model="activeTab"
      @change="handleChange"
      active-color="#ee0a24"
      inactive-color="#7d7e80"
    >
      <wd-tabbar-item is-dot :value="2" title="点状" icon="home"></wd-tabbar-item>
      <wd-tabbar-item :value="2" icon="cart" title="分类"></wd-tabbar-item>
      <wd-tabbar-item :value="30" title="我的" icon="user"></wd-tabbar-item>
      <wd-tabbar-item :value="200" title="最大值" icon="photo"></wd-tabbar-item>
      <wd-tabbar-item :value="10" title="客服" icon="chat"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log(event)
  }
</script>
```

`active-color` 和 `inactive-color` 属性作用于 `wd-tabbar` 容器，会自动传递给所有子项。颜色会同时影响图标和文字的显示效果。默认激活颜色为 `#4D80F0`，未激活颜色为 `#7D7E80`。

### 示例 7：固定底部与占位

将标签栏固定在页面底部，并处理内容遮挡问题。

```vue
<template>
  <view>
    <view style="padding: 20rpx">
      <view>页面内容区域，滚动时标签栏保持固定在底部</view>
    </view>

    <wd-tabbar
      fixed
      shape="round"
      v-model="activeTab"
      @change="handleChange"
      bordered
      safeAreaInsetBottom
      placeholder
    >
      <wd-tabbar-item :value="2" is-dot title="首页" icon="home"></wd-tabbar-item>
      <wd-tabbar-item title="分类" icon="cart"></wd-tabbar-item>
      <wd-tabbar-item title="我的" icon="user"></wd-tabbar-item>
      <wd-tabbar-item :value="200" title="相册" icon="photo"></wd-tabbar-item>
      <wd-tabbar-item :value="10" title="客服" icon="chat"></wd-tabbar-item>
    </wd-tabbar>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'

  const activeTab = ref(0)

  function handleChange(event: any) {
    console.log(event)
  }
</script>
```

设置 `fixed` 属性将标签栏固定在页面底部（`position: fixed`）。同时设置 `placeholder` 会在标签栏原始位置生成一个等高的占位元素，防止页面底部内容被遮挡。`safeAreaInsetBottom` 在 iPhone X 等机型上自动添加底部安全距离，避免标签栏被系统手势条遮挡。

## 注意事项

1. **子项必须作为 wd-tabbar 的直接子元素**：`wd-tabbar-item` 必须直接嵌套在 `wd-tabbar` 内部使用，中间不能包裹其他组件或元素，否则父子通信关系无法建立
2. **name 与索引的匹配逻辑**：当子项设置了 `name` 属性时，`v-model` 的值和 `change` 事件的 `value` 使用 `name`；未设置时使用子项在容器中的索引值（从 0 开始）。同一容器内建议统一使用名称或统一使用索引
3. **徽标值为 null 时不显示**：`value` 属性默认值为 `null`，此时不显示徽标；设置为任何非 null 值（包括 0）时显示徽标
4. **徽标最大值默认 99**：内部默认最大值为 99，超过则显示 `"99+"`；可通过 `max` 属性或 `badgeProps` 自定义
5. **badgeProps 属性深度合并**：`badgeProps` 对象会与内部计算出的 `max`、`isDot`、`value` 进行深度合并，允许通过 `badgeProps` 覆盖任何 Badge 组件的属性
6. **圆角形状的安全区自适应**：当 `shape="round"` 且 `fixed` 为 `true` 时，标签栏会自动适配底部安全区，无需额外设置 `safeAreaInsetBottom`
7. **占位高度动态计算**：当使用 `fixed` 和 `placeholder` 组合时，占位高度通过 DOM 查询动态获取，组件挂载后自动计算
8. **颜色通过样式透传**：`activeColor` 和 `inactiveColor` 通过计算属性生成内联样式传递给子项，不会覆盖子项的 `customStyle`
9. **默认顶部边框为 0.5px 细线**：使用 `halfPixelBorder` 技术实现精致的 0.5px 上边框效果，在高分辨率屏幕上显示更加清晰
10. **暗色模式自动适配**：组件已内置暗色主题样式，未激活状态下的文字颜色会自动调整为暗色主题下的灰色系
11. **圆角形状默认无边框**：`shape="round"` 的标签栏不显示顶部边框，`bordered` 属性仅在 `shape="default"` 时生效
