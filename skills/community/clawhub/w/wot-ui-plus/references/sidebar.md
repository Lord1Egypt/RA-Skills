# Sidebar 侧边栏


## 组件概况

Sidebar 侧边栏组件是一组用于垂直导航分类的控件，由 `wd-sidebar`（容器组件）和 `wd-sidebar-item`（子项组件）共同构成。该组件通常以垂直列表形式展示一组导航选项，通过高亮标识当前选中项，适用于左右分栏布局中的左侧分类导航。

侧边栏采用纵向排列的选项列表，选中项通过背景色和文字颜色变化进行视觉区分，同时相邻选项会产生圆角过渡效果，使选中状态更加醒目。每个选项支持配置图标、徽标提示、禁用状态等丰富功能。

## 核心功能描述

- **双向绑定**：通过 `v-model` 绑定当前选中的侧边栏项的值，支持数字和字符串类型的唯一标识
- **异步切换控制**：通过 `beforeChange` 钩子函数在切换前执行异步操作（如加载数据），根据操作结果决定是否切换
- **图标支持**：每个选项支持配置内置图标名称，通过 `icon` 属性设置；也支持通过具名插槽自定义图标内容
- **徽标提示**：通过 `badge` 属性或 `badgeProps` 配置为选项添加徽标，支持数值徽标、点状徽标、自定义徽标属性
- **禁用状态**：通过 `disabled` 属性禁用特定选项，被禁用的选项无法点击切换
- **圆角过渡**：自动识别选中项的上下相邻项，为相邻项添加圆角过渡样式，增强选中状态的视觉层次
- **值唯一标识**：每个 `wd-sidebar-item` 通过 `value` 属性绑定唯一标识，支持数字和字符串类型

## 适用业务场景

- **分类导航**：电商平台的商品分类导航，左侧分类列表配合右侧商品内容展示
- **设置菜单**：设置页面左侧功能分类列表，点击后右侧展示对应设置项
- **消息列表**：消息应用的会话分类导航，如全部消息、私信通知、系统通知等
- **文件管理**：文件管理器中的文件夹树形导航或分类筛选
- **后台管理系统**：管理后台左侧功能模块导航菜单
- **锚点导航**：配合滚动区域实现页面内锚点定位导航

## API

### wd-sidebar Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 当前选中项的值 | number / string | - | 0 | - |
| beforeChange | 切换前执行的钩子函数，用于异步控制切换行为 | SidebarBeforeChange | - | - | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-sidebar-item Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| label | 当前选项的标题文字 | string | - | - | - |
| value | 当前选项的唯一标识值 | number / string | - | - | - |
| badge | 徽标显示值 | string / number / null | - | null | - |
| badgeProps | 徽标属性配置，透传给 Badge 组件 | object | - | - | - |
| icon | 图标名称 | string | - | - | - |
| isDot | 是否显示为点状徽标 | boolean | - | undefined | - |
| max | 徽标最大值，超过后显示 `{max}+` | number | - | 99 | - |
| disabled | 是否禁用该选项 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-sidebar Events

| 事件名称 | 回调参数 | 说明 |
|----------|----------|------|
| change | `{ value: number \| string, label: string }` | 选项切换时触发 |

### wd-sidebar-item Events

组件未定义对外抛出的事件。

### wd-sidebar Methods

组件未暴露外部可调用的方法。

### wd-sidebar-item Methods

组件未暴露外部可调用的方法。

### wd-sidebar Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于放置 `wd-sidebar-item` 子组件 | `wd-sidebar-item` 组件 |

### wd-sidebar-item Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| icon | 自定义图标插槽，覆盖 `icon` 属性设置的图标 | 自定义图标内容 |
| default | 默认插槽内容已由 `label` 属性渲染，通常不需要使用 | 任意内容 |

### beforeChange 类型定义

```ts
type SidebarBeforeChange = (option: SidebarBeforeChangeOption) => void

interface SidebarBeforeChangeOption {
  value: number | string        // 目标选项的值
  resolve: (pass: boolean) => void  // 调用 resolve(true) 允许切换，resolve(false) 阻止切换
}
```

## 使用示例

### 基础用法

最基本的侧边栏使用方式，通过 `v-model` 绑定当前选中的值，在 `wd-sidebar` 内部放置多个 `wd-sidebar-item` 子组件。每个选项通过 `value` 设置唯一标识，`label` 设置显示文字。

```vue
<template>
  <view class="sidebar-container">
    <wd-sidebar v-model="active">
      <wd-sidebar-item :value="0" label="分类一" />
      <wd-sidebar-item :value="1" label="分类二" />
      <wd-sidebar-item :value="2" label="分类三" />
    </wd-sidebar>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref<number>(0)
</script>

<style lang="scss" scoped>
.sidebar-container {
  width: 100%;
}
</style>
```

### 徽标提示

通过 `badge` 属性为选项添加数值徽标，`is-dot` 属性添加点状徽标，`badge-props` 配置更详细的徽标属性（如主题色、最大值等）。

```vue
<template>
  <view class="sidebar-container">
    <wd-sidebar v-model="active">
      <!-- 点状徽标 -->
      <wd-sidebar-item :value="0" label="新消息" is-dot />
      <!-- 数值徽标 -->
      <wd-sidebar-item :value="1" label="待处理" badge="5" />
      <!-- 自定义徽标属性 -->
      <wd-sidebar-item
        :value="2"
        label="预警"
        badge="120"
        :badge-props="{ type: 'warning', max: 99 }"
      />
      <wd-sidebar-item :value="3" label="已完成" />
    </wd-sidebar>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref<number>(0)
</script>

<style lang="scss" scoped>
.sidebar-container {
  width: 100%;
}
</style>
```

### 异步切换控制

通过 `beforeChange` 钩子函数在选项切换前执行异步操作（如显示加载提示、请求数据等），操作完成后再决定是否允许切换。

```vue
<template>
  <view class="sidebar-container">
    <wd-sidebar v-model="active" :before-change="beforeChange">
      <wd-sidebar-item :value="0" label="首页" />
      <wd-sidebar-item :value="1" label="分类" />
      <wd-sidebar-item :value="2" label="我的" />
    </wd-sidebar>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { SidebarBeforeChange } from '@/uni_modules/wot-ui-plus/components/wd-sidebar/types'

const active = ref<number>(0)

const beforeChange: SidebarBeforeChange = ({ value, resolve }) => {
  // 显示加载提示
  uni.showLoading({ title: '加载中...' })

  // 模拟异步操作
  setTimeout(() => {
    uni.hideLoading()
    // 允许切换
    resolve(true)
  }, 1000)
}
</script>

<style lang="scss" scoped>
.sidebar-container {
  width: 100%;
}
</style>
```

### 锚点联动导航

侧边栏与右侧滚动区域联动，点击侧边栏选项时滚动到对应内容区域，滚动内容区域时自动高亮对应的侧边栏选项。

```vue
<template>
  <view class="wraper">
    <wd-sidebar v-model="active" @change="handleChange">
      <wd-sidebar-item
        v-for="(item, index) in categories"
        :key="index"
        :value="index"
        :label="item.label"
      />
    </wd-sidebar>
    <scroll-view
      class="content"
      scroll-y
      scroll-with-animation
      :scroll-top="scrollTop"
      :throttle="false"
      @scroll="onScroll"
    >
      <view v-for="(item, index) in categories" :key="index" class="category">
        <wd-cell-group :title="item.title" border>
          <wd-cell
            v-for="(cell, cellIndex) in item.items"
            :key="cellIndex"
            :title="cell.title"
            :label="cell.label"
          />
        </wd-cell-group>
      </view>
    </scroll-view>
  </view>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from 'vue'
import { getRect } from '@/uni_modules/wot-ui-plus/components/common/util'

interface CategoryItem {
  title: string
  label: string
}

interface Category {
  label: string
  title: string
  items: CategoryItem[]
}

const active = ref<number>(0)
const scrollTop = ref<number>(0)
const itemScrollTop = ref<number[]>([])

const subCategories = computed<CategoryItem[]>(() =>
  new Array(20).fill({ title: '标题文字', label: '这是描述内容' }, 0, 20)
)

const categories = computed<Category[]>(() => [
  { label: '分类一', title: '标题一', items: subCategories.value },
  { label: '分类二', title: '标题二', items: subCategories.value },
  { label: '分类三', title: '标题三', items: subCategories.value.slice(0, 15) },
  { label: '分类四', title: '标题四', items: subCategories.value.slice(0, 18) },
  { label: '分类五', title: '标题五', items: subCategories.value }
])

onMounted(() => {
  getRect('.category', true).then((rects) => {
    itemScrollTop.value = rects.map((item) => item.top || 0)
    scrollTop.value = rects[active.value].top || 0
  })
})

function handleChange({ value }: any) {
  active.value = value
  scrollTop.value = itemScrollTop.value[value]
}

function onScroll(e: any) {
  const { scrollTop: currentScrollTop } = e.detail
  const threshold = 50 // 下一个标题与顶部的距离
  if (currentScrollTop < threshold) {
    active.value = 0
    return
  }
  const index = itemScrollTop.value.findIndex(
    (top) => top > currentScrollTop && top - currentScrollTop <= threshold
  )
  if (index > -1) {
    active.value = index
  }
}
</script>

<style lang="scss" scoped>
.wraper {
  display: flex;
  height: calc(100vh - var(--window-top));
  height: calc(100vh - var(--window-top) - constant(safe-area-inset-bottom));
  height: calc(100vh - var(--window-top) - env(safe-area-inset-bottom));
}
.content {
  flex: 1;
  background: #fff;
}
</style>
```

### 自定义图标

通过 `icon` 属性为选项设置内置图标，也可以通过 `icon` 插槽完全自定义图标内容。

```vue
<template>
  <view class="sidebar-container">
    <wd-sidebar v-model="active" @change="handleChange">
      <wd-sidebar-item
        v-for="(item, index) in categories"
        :key="index"
        :value="index"
        :label="item.label"
        :icon="item.icon"
        :disabled="item.disabled"
      />
    </wd-sidebar>
  </view>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'

const active = ref<number>(0)

const categories = computed(() => [
  { label: '推荐', icon: 'thumb-up', disabled: false },
  { label: '二维码', icon: 'qrcode', disabled: false },
  { label: '位置', icon: 'location', disabled: false },
  { label: '浏览器', icon: 'chrome', disabled: false },
  { label: 'Android', icon: 'android', disabled: true }
])

function handleChange({ value }: any) {
  console.log('选中项', value)
}
</script>

<style lang="scss" scoped>
.sidebar-container {
  width: 100%;
}
</style>
```

### 禁用选项

通过 `disabled` 属性可以禁用特定选项，被禁用的选项无法点击切换。

```vue
<template>
  <view class="sidebar-container">
    <wd-sidebar v-model="active">
      <wd-sidebar-item :value="0" label="可用选项一" />
      <wd-sidebar-item :value="1" label="可用选项二" />
      <wd-sidebar-item :value="2" label="禁用选项" disabled />
      <wd-sidebar-item :value="3" label="可用选项三" />
    </wd-sidebar>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const active = ref<number>(0)
</script>

<style lang="scss" scoped>
.sidebar-container {
  width: 100%;
}
</style>
```

### 多侧边栏布局

在同一页面中使用多个侧边栏组件，每个侧边栏独立管理自己的选中状态。

```vue
<template>
  <view class="multi-sidebar">
    <!-- 第一组侧边栏 -->
    <view class="sidebar-group">
      <view class="group-title">业务分类</view>
      <wd-sidebar v-model="businessActive">
        <wd-sidebar-item :value="0" label="订单" />
        <wd-sidebar-item :value="1" label="商品" />
        <wd-sidebar-item :value="2" label="用户" />
      </wd-sidebar>
    </view>

    <!-- 第二组侧边栏 -->
    <view class="sidebar-group">
      <view class="group-title">消息分类</view>
      <wd-sidebar v-model="messageActive">
        <wd-sidebar-item :value="0" label="通知" is-dot />
        <wd-sidebar-item :value="1" label="私信" badge="3" />
        <wd-sidebar-item :value="2" label="系统" />
      </wd-sidebar>
    </view>
  </view>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const businessActive = ref<number>(0)
const messageActive = ref<number>(0)
</script>

<style lang="scss" scoped>
.multi-sidebar {
  display: flex;
  justify-content: space-around;
}
.sidebar-group {
  width: 45%;
}
.group-title {
  font-size: 28rpx;
  font-weight: bold;
  margin-bottom: 16rpx;
}
</style>
```

## 注意事项

1. **组件配对使用**：`wd-sidebar-item` 必须作为 `wd-sidebar` 的直接子组件使用，脱离容器单独使用无法获取上下文信息，选中状态将不会正常显示。

2. **value 唯一性**：每个 `wd-sidebar-item` 的 `value` 属性值必须唯一，用于标识和匹配当前选中项。如果多个选项使用相同的 `value`，将导致选中状态混乱。

3. **beforeChange 必须调用 resolve**：使用 `beforeChange` 钩子时，必须在异步操作完成后调用 `resolve(true)` 或 `resolve(false)` 来允许或阻止切换。如果不调用 `resolve`，切换操作将永远处于等待状态。

4. **徽标默认最大值**：当未显式设置 `max` 属性时，徽标的默认最大值为 99。超过最大值的数字会显示为 `99+` 格式。`badgeProps` 中也可以覆盖此设置。

5. **图标插槽优先级**：当同时使用 `icon` 属性和 `icon` 插槽时，插槽内容的优先级更高，`icon` 属性设置的图标将不会显示。

6. **圆角过渡样式**：组件会自动计算选中项的上下相邻项，为相邻项添加对应的圆角样式（`wd-sidebar-item--prefix` 和 `wd-sidebar-item--suffix`）。这些样式类由组件内部自动处理，无需手动配置。

7. **左右分栏布局**：侧边栏组件本身不控制布局宽度，通常需要配合外层容器使用 flex 布局实现左右分栏效果。左侧固定侧边栏宽度，右侧内容区域使用 `flex: 1` 自适应剩余空间。

8. **徽标属性合并**：`badgeProps` 属性会与 `badge`、`isDot`、`max` 等独立属性进行合并，`badgeProps` 中的配置优先级更高。如果 `badgeProps` 中未设置 `max`，则使用独立的 `max` 属性值。

9. **切换事件时机**：`change` 事件在选中项实际变更后触发，回调参数包含选中项的 `value`（值）和 `label`（标题文字），可用于根据选中项加载对应的内容数据。
