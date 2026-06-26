# Grid 网格


## 组件概况

Grid 网格组件由 `Grid`（容器组件）和 `GridItem`（子项组件）两个关联组件组成，用于创建网格布局。`Grid` 组件负责控制整体布局参数（列数、间距、边框、背景色等），`GridItem` 组件负责展示具体内容（图标、文字、徽标等），并支持点击跳转和自定义内容。两者配合使用，可以快速实现等分布局、响应式布局、正方形网格等多种网格效果。

## 核心功能描述

- **自定义列数**：通过 `column` 属性控制网格列数，支持等宽分配
- **间距控制**：通过 `gutter` 属性设置网格项之间的间距，默认为 px 单位
- **正方形网格**：通过 `square` 属性将网格项固定为正方形，适用于图标展示等场景
- **边框显示**：通过 `border` 属性控制是否显示网格边框，支持圆角和直角边框样式
- **点击反馈**：通过 `clickable` 属性开启点击反馈效果，支持自定义 hover 样式
- **路由跳转**：GridItem 支持配置 `url` 和 `linkType` 实现点击自动跳转，支持 navigateTo、switchTab、reLaunch、redirectTo 四种跳转方式
- **徽标支持**：GridItem 内置 Badge 徽标组件，支持显示小红点、数字徽标、类型徽标等
- **自定义背景色**：通过 `bgColor` 属性设置网格项背景色
- **插槽定制**：支持自定义图标插槽（icon）、文字插槽（text）和默认插槽

## 适用业务场景

- 首页功能入口网格导航
- 商品分类列表展示
- 图标导航菜单
- 数据卡片网格布局
- 响应式内容展示
- 快捷操作面板

## 完整API

### Grid Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| clickable | boolean | false | 否 | 是否开启格子点击反馈效果 |
| square | boolean | false | 否 | 是否将格子固定为正方形 |
| column | number | - | 否 | 网格列数，必须大于 0 |
| border | boolean | false | 否 | 是否显示网格边框 |
| bgColor | string | '' | 否 | 网格项背景颜色 |
| gutter | number | - | 否 | 格子之间的间距，默认单位为 px |
| hoverClass | string | - | 否 | 自定义内容区域 hover-class，需配合 clickable 使用 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### GridItem Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| icon | string | '' | 否 | 图标名称，可选值参考 wd-icon 组件 |
| iconSize | string | '26px' | 否 | 图标大小 |
| text | string | - | 否 | 网格项下方显示的文字 |
| url | string | - | 否 | 点击后跳转的链接地址 |
| linkType | LinkType | 'navigateTo' | 否 | 页面跳转方式，可选值：navigateTo / switchTab / reLaunch / redirectTo |
| isDot | boolean | false | 否 | 是否显示图标右上角小红点 |
| type | BadgeType | - | 否 | 图标右上角 badge 类型，可选值：primary / success / warning / danger / info |
| value | number / string | - | 否 | 图标右上角 badge 显示值 |
| max | number | - | 否 | 图标右上角 badge 最大值，超过最大值会显示 '{max}+'，要求 value 是 Number 类型 |
| badgeProps | `Partial<BadgeProps>` | - | 否 | 徽标属性配置，透传给 Badge 组件 |
| customText | string | '' | 否 | 自定义下方文字样式类名 |
| customIcon | string | '' | 否 | 自定义上方图标样式类名 |
| customStyle | string | '' | 否 | 自定义根节点样式 |
| customClass | string | '' | 否 | 自定义根节点类名 |

### GridItem Events

| 事件名称 | 说明 | 回调参数 |
|---------|------|---------|
| itemclick | 点击网格项时触发 | - |

### Grid Slots

| 插槽名称 | 说明 |
|---------|------|
| default | 用于放置 GridItem 子组件 |

### GridItem Slots

| 插槽名称 | 说明 |
|---------|------|
| default | 自定义网格项完整内容，覆盖默认的图标+文字布局 |
| icon | 自定义图标内容 |
| text | 自定义文字内容 |

## 使用示例

### 基础用法

```vue
<template>
  <wd-grid :column="4" :border="true">
    <wd-grid-item v-for="item in 8" :key="item" :text="`功能${item}`" />
  </wd-grid>
</template>
```

### 带图标的网格

```vue
<template>
  <wd-grid :column="4" :gutter="10">
    <wd-grid-item 
      v-for="item in gridData" 
      :key="item.name" 
      :icon="item.icon" 
      :text="item.name"
    />
  </wd-grid>
</template>

<script setup lang="ts">
const gridData = [
  { name: '首页', icon: 'home' },
  { name: '分类', icon: 'category' },
  { name: '购物车', icon: 'cart' },
  { name: '我的', icon: 'user' },
  { name: '订单', icon: 'order' },
  { name: '收藏', icon: 'star' },
  { name: '优惠券', icon: 'coupon' },
  { name: '客服', icon: 'service' }
]
</script>
```

### 正方形网格

```vue
<template>
  <wd-grid :column="3" square :border="true">
    <wd-grid-item 
      v-for="item in 6" 
      :key="item" 
      :icon="`icon-${item}`" 
      :text="`选项${item}`"
    />
  </wd-grid>
</template>
```

### 自定义背景色和间距

```vue
<template>
  <wd-grid :column="2" :gutter="20" bg-color="#f5f7fa" :border="true">
    <wd-grid-item 
      v-for="item in 4" 
      :key="item" 
      :text="`卡片${item}`"
      :custom-style="{ padding: '20px' }"
    >
      <template #icon>
        <wd-icon name="star" size="32px" />
      </template>
    </wd-grid-item>
  </wd-grid>
</template>
```

### 带徽标的网格

```vue
<template>
  <wd-grid :column="4">
    <wd-grid-item 
      icon="message" 
      text="消息" 
      :value="99" 
      :max="99"
    />
    <wd-grid-item 
      icon="cart" 
      text="购物车" 
      :value="3"
    />
    <wd-grid-item 
      icon="comment" 
      text="评论" 
      is-dot
    />
    <wd-grid-item 
      icon="warning" 
      text="告警" 
      type="danger"
      :value="5"
    />
  </wd-grid>
</template>
```

### 带路由跳转的网格

```vue
<template>
  <wd-grid :column="4" clickable>
    <wd-grid-item 
      icon="home" 
      text="首页" 
      url="/pages/home/index" 
      link-type="switchTab"
    />
    <wd-grid-item 
      icon="order" 
      text="订单" 
      url="/pages/order/index" 
      link-type="navigateTo"
      @itemclick="handleItemClick"
    />
    <wd-grid-item 
      icon="user" 
      text="我的" 
      url="/pages/user/index" 
      link-type="switchTab"
    />
    <wd-grid-item 
      icon="setting" 
      text="设置" 
      url="/pages/setting/index" 
      link-type="navigateTo"
    />
  </wd-grid>
</template>

<script setup lang="ts">
const handleItemClick = () => {
  console.log('点击了订单入口')
}
</script>
```

### 自定义内容网格

```vue
<template>
  <wd-grid :column="2" :gutter="16">
    <wd-grid-item v-for="item in 4" :key="item">
      <view class="custom-card">
        <wd-icon name="chart" size="40px" />
        <view class="custom-card__title">数据统计</view>
        <view class="custom-card__desc">查看详情数据</view>
      </view>
    </wd-grid-item>
  </wd-grid>
</template>

<style scoped>
.custom-card {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  text-align: center;
}

.custom-card__title {
  margin-top: 12px;
  font-size: 16px;
  font-weight: bold;
}

.custom-card__desc {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}
</style>
```

### 无边框网格

```vue
<template>
  <wd-grid :column="4">
    <wd-grid-item 
      v-for="item in 8" 
      :key="item" 
      :icon="`icon-${item}`" 
      :text="`功能${item}`"
    />
  </wd-grid>
</template>
```

## 注意事项

1. **列数设置**：`column` 属性值必须大于 0，不建议使用过大的值，否则会导致网格项显示异常。

2. **间距与边框**：当设置了 `gutter` 时，边框会自动调整为圆角边框样式；当未设置 `gutter` 时，边框显示为直角样式。

3. **正方形网格**：启用 `square` 属性后，网格项的宽高会根据宽度百分比计算保持高度一致，适用于图标展示场景。

4. **点击反馈**：`hoverClass` 属性仅在 `clickable` 为 `true` 时生效。如果未自定义 `hoverClass`，则使用默认的点击反馈样式。

5. **路由跳转**：GridItem 的 `url` 属性需配合 `clickable` 属性使用才能生效。`linkType` 的四种跳转方式需参考微信小程序路由文档，确保目标页面路径正确。

6. **组件嵌套**：Grid 组件建议仅包含 GridItem 子组件，不建议混入其他类型的子组件。

7. **性能优化**：在包含大量网格项时，建议使用合理的列数配置，避免过多的 DOM 元素渲染影响性能。

8. **徽标配置**：通过 `badgeProps` 可以透传更多 Badge 组件的配置项，实现更丰富的徽标展示效果。
