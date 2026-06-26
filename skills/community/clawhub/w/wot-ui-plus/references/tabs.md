# Tabs 标签页


## 组件概况

Tabs 标签页组件是一组用于内容分类和切换的导航控件，由 `wd-tabs`（容器组件）和 `wd-tab`（子项组件）共同构成。该组件允许用户在同一页面内通过点击标签或手势滑动来切换不同的内容面板，有效减少页面跳转，提升信息浏览效率。

导航栏区域采用水平排列的标签布局，支持超出屏幕时自动横向滚动，并配备动态下划线指示器标识当前激活项。内容区域默认隐藏非激活面板，支持懒加载渲染和切换动画过渡效果。

## 核心功能描述

- **双向绑定**：通过 `v-model` 绑定当前激活的标签索引或名称，支持数字索引和字符串名称两种匹配方式
- **滑动导航**：标签数量超过阈值时自动开启横向滚动，选中项自动滚动到可视区域居中位置
- **手势滑动**：开启 `swipeable` 后支持左右滑动手势切换标签内容（需配合 `animated` 使用）
- **切换动画**：通过 `animated` 属性开启内容面板左右滑动过渡效果，可自定义动画时长
- **粘性吸顶**：通过 `sticky` 属性将导航栏固定在页面顶部，支持自定义吸顶位置 `offsetTop`
- **导航地图**：标签数量超过阈值时自动弹出导航地图面板，提供全屏选项列表快速跳转
- **底部条定制**：支持自定义底部指示条的宽度和高度，可自动匹配标签文字宽度
- **徽标提示**：每个标签支持通过 `badgeProps` 添加徽标，用于展示未读数量或状态提示
- **懒加载**：默认开启懒加载，tab 内容仅在首次被激活时渲染，优化性能
- **禁用状态**：支持禁用特定标签，点击被禁用标签时触发 `disabled` 事件
- **颜色定制**：支持自定义激活状态和非激活状态的标签文字颜色

## 适用业务场景

- **内容分类浏览**：新闻分类、商品分类、文档分类等需要多类别切换的场景
- **表单分组**：多步骤表单或复杂表单中按功能模块分组展示
- **数据看板**：不同维度的数据展示切换，如今日/本周/本月数据
- **订单管理**：按订单状态（全部/待付款/待发货/已完成）筛选展示
- **设置页面**：将设置项按类别分组，通过标签页切换不同设置面板
- **弹窗内导航**：在弹窗组件内部使用标签页组织多层级内容

## API

### wd-tabs Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| modelValue | 绑定值，当前激活标签的索引或名称 | number / string | - | 0 | - |
| slidableNum | 标签数量超过此值时可滑动 | number | - | 6 | - |
| mapNum | 标签数量超过此值时显示导航地图 | number | - | 10 | - |
| mapTitle | 导航地图的标题文字 | string | - | 全部 | - |
| sticky | 是否开启粘性布局（导航栏吸顶） | boolean | - | false | - |
| offsetTop | 粘性布局吸顶时的距离顶部偏移量，单位 px | number | - | 0 | - |
| swipeable | 是否开启手势滑动切换内容 | boolean | - | false | - |
| autoLineWidth | 是否自动调整底部条宽度以匹配标签文字宽度（设置 lineWidth 后无效） | boolean | - | false | - |
| lineWidth | 底部指示条宽度，单位 px | number / string | - | - | - |
| lineHeight | 底部指示条高度，单位 px | number / string | - | - | - |
| color | 激活状态标签文字颜色 | string | - | '' | - |
| inactiveColor | 非激活状态标签文字颜色 | string | - | '' | - |
| animated | 是否开启内容面板切换过渡动画 | boolean | - | false | - |
| duration | 切换动画过渡时间，单位 ms | number | - | 300 | - |
| slidable | 标签可滑动模式 | string | auto / always | auto | - |
| showScrollbar | 标签可滑动时是否显示滚动条 | boolean | - | false | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

#### slidable 属性说明

- `auto`：默认模式，仅当标签数量超过 `slidableNum` 时才开启横向滚动
- `always`：始终开启横向滚动模式，无论标签数量多少

### wd-tab Props

| 属性名 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|--------|------|------|--------|--------|----------|
| name | 标签唯一标识符，用于字符串匹配方式 | number / string | - | - | - |
| title | 标签显示的标题文字 | string | - | - | - |
| disabled | 是否禁用该标签，禁用后无法点击切换 | boolean | - | false | - |
| lazy | 是否懒加载，切换到该标签时才渲染内容 | boolean | - | true | - |
| badgeProps | 徽标属性配置，透传给 Badge 组件 | object | - | - | - |
| customStyle | 自定义根节点样式 | string | - | '' | - |
| customClass | 自定义根节点样式类 | string | - | '' | - |

### wd-tabs Events

| 事件名称 | 回调参数 | 说明 |
|----------|----------|------|
| change | `{ index: number, name: number \| string }` | 激活标签切换时触发（值改变时触发） |
| click | `{ index: number, name: number \| string }` | 点击标签时触发（无论是否禁用都会触发） |
| disabled | `{ index: number, name: number \| string }` | 点击被禁用的标签时触发 |

> 注意：`click` 事件在点击任何标签时都会触发，包括被禁用的标签。若需要区分正常点击和禁用点击，可同时监听 `click` 和 `disabled` 事件。

### wd-tab Events

组件未定义对外抛出的事件。

### wd-tabs Methods

组件实例暴露的方法，可通过 ref 调用：

| 方法名 | 说明 | 参数 |
|--------|------|------|
| setActive | 设置激活的标签项 | `value: number \| string, init?: boolean, setScroll?: boolean` |
| scrollIntoView | 使当前选中项滚动到可视区域 | - |
| updateLineStyle | 更新底部指示条样式 | `animation?: boolean`（是否开启动画，默认开启） |

### wd-tab Methods

组件未暴露外部可调用的方法。

### wd-tabs Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于放置 `wd-tab` 子组件 | `wd-tab` 组件 |

### wd-tab Slots

| 插槽名 | 说明 | 子节点内容 |
|--------|------|------------|
| default | 默认插槽，用于放置当前标签页的内容 | 任意内容 |

## 使用示例

### 基础用法

最基本的标签页使用方式，通过 `v-model` 绑定当前激活的标签索引，在 `wd-tabs` 内部放置多个 `wd-tab` 子组件。

```vue
<template>
  <wd-tabs v-model="activeTab" @change="handleChange">
    <wd-tab title="标签一">
      <view class="content">内容一</view>
    </wd-tab>
    <wd-tab title="标签二">
      <view class="content">内容二</view>
    </wd-tab>
    <wd-tab title="标签三">
      <view class="content">内容三</view>
    </wd-tab>
    <wd-tab title="标签四">
      <view class="content">内容四</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeTab = ref<number>(0)

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### name 字符串匹配

通过为每个 `wd-tab` 设置 `name` 属性，可以使用字符串而不是数字索引来标识和切换标签。这种方式在标签顺序可能变化的场景下更加灵活。

```vue
<template>
  <wd-tabs v-model="activeTab" @change="handleChange">
    <wd-tab title="今日" name="today">
      <view class="content">今日内容</view>
    </wd-tab>
    <wd-tab title="本周" name="week">
      <view class="content">本周内容</view>
    </wd-tab>
    <wd-tab title="本月" name="month">
      <view class="content">本月内容</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

// 使用字符串名称绑定，初始激活 "today"
const activeTab = ref<string>('today')

function handleChange(event: any) {
  console.log('当前标签', event.name, '索引', event.index)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 粘性吸顶布局

通过设置 `sticky` 属性，标签导航栏会在滚动时固定在页面顶部，适用于长页面内容浏览场景。可通过 `offsetTop` 属性设置吸顶位置距离顶部的距离。

```vue
<template>
  <wd-tabs v-model="activeTab" sticky :offsetTop="10" @change="handleChange">
    <wd-tab v-for="item in 4" :key="item" :title="`标签${item}`">
      <view class="large-content">
        标签页内容{{ item }}，向下滚动可看到导航栏吸顶效果
      </view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeTab = ref<number>(0)

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.large-content {
  min-height: 320px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 手势滑动切换

开启 `swipeable` 和 `animated` 属性后，用户可以通过左右滑动手势切换标签内容，同时底部指示条会同步平滑过渡。

```vue
<template>
  <wd-tabs v-model="activeTab" swipeable animated :duration="300" @change="handleChange">
    <wd-tab v-for="item in 4" :key="item" :title="`标签${item}`">
      <view class="content">内容{{ item }}</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeTab = ref<number>(0)

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 徽标提示

通过 `wd-tab` 的 `badgeProps` 属性为标签添加徽标提示，适用于消息通知、待办数量等场景。`badgeProps` 属性会透传给 Badge 组件。

```vue
<template>
  <wd-tabs v-model="activeTab" @change="handleChange">
    <wd-tab
      v-for="(item, index) in tabsWithBadge"
      :key="index"
      :title="item.title"
      :badge-props="item.badgeProps"
    >
      <view class="content">{{ item.title }}</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'

const activeTab = ref<number>(0)

const tabsWithBadge = computed(() => [
  {
    title: '消息',
    badgeProps: {
      modelValue: 10,
      right: '-8px'
    }
  },
  {
    title: '通知',
    badgeProps: {
      modelValue: 100,
      max: 99,
      right: '-8px'
    }
  },
  {
    title: '动态',
    badgeProps: {
      isDot: true,
      right: '-8px',
      showZero: true
    }
  }
])

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 自动调整底部条宽度

通过 `auto-line-width` 属性，底部指示条的宽度会自动匹配当前激活标签的文字宽度，适用于标签文字长度差异较大的场景。

```vue
<template>
  <wd-tabs v-model="activeTab" auto-line-width @change="handleChange">
    <wd-tab title="推荐" name="recommend">
      <view class="content">推荐内容</view>
    </wd-tab>
    <wd-tab title="热门活动" name="hot">
      <view class="content">热门活动内容</view>
    </wd-tab>
    <wd-tab title="最新" name="newest">
      <view class="content">最新内容</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeTab = ref<string>('recommend')

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 在弹窗中使用

在 `wd-popup` 等弹出层组件中使用 Tabs 时，需要在弹窗展开后手动调用 `updateLineStyle` 方法更新底部指示条样式，因为弹窗渲染时机可能导致指示条位置计算不准确。

```vue
<template>
  <wd-button @click="showPopup = true">打开弹窗</wd-button>

  <wd-popup
    v-model="showPopup"
    position="bottom"
    safe-area-inset-bottom
    @after-enter="handlePopupShow"
    closable
    custom-style="padding: 0 24rpx;"
  >
    <view class="title">弹窗中的标签页</view>
    <wd-tabs v-model="activeTab" ref="tabsRef">
      <wd-tab v-for="item in tabs" :key="item" :title="item" :name="item">
        <view class="content">内容 {{ item }}</view>
      </wd-tab>
    </wd-tabs>
  </wd-popup>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import type { TabsInstance } from '@/uni_modules/wot-ui-plus/components/wd-tabs/types'

const showPopup = ref(false)
const activeTab = ref<number>(0)
const tabsRef = ref<TabsInstance>()
const tabs = ['选项一', '选项二', '选项三']

/**
 * 弹窗打开后更新底部指示条样式
 */
function handlePopupShow() {
  tabsRef.value?.updateLineStyle(false)
}
</script>

<style lang="scss" scoped>
.title {
  display: flex;
  font-size: 32rpx;
  align-items: center;
  justify-content: center;
  padding: 24rpx 0;
}
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

### 禁用标签与点击事件

通过设置 `disabled` 属性可以禁用特定标签，被禁用的标签无法切换。同时可以监听 `click` 和 `disabled` 事件分别处理普通点击和禁用标签点击。

```vue
<template>
  <wd-tabs v-model="activeTab" @click="handleClick" @disabled="handleDisabled" @change="handleChange">
    <wd-tab v-for="item in 4" :key="item" :title="`标签${item}`" :disabled="item === 2">
      <view class="content">内容{{ item }}</view>
    </wd-tab>
  </wd-tabs>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const activeTab = ref<number>(0)

function handleClick({ index, name }: any) {
  console.log('点击了标签', { index, name })
}

function handleDisabled({ index, name }: any) {
  console.log('点击了禁用标签', { index, name })
}

function handleChange(event: any) {
  console.log('切换标签', event)
}
</script>

<style lang="scss" scoped>
.content {
  height: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
```

## 注意事项

1. **组件配对使用**：`wd-tab` 必须作为 `wd-tabs` 的直接子组件使用，脱离 `wd-tabs` 容器单独使用无法正常工作。

2. **modelValue 类型校验**：`modelValue` 的值类型必须为 number 或 string。传入空字符串、null 或 undefined 会在控制台输出错误信息。当使用数字类型时，值不能为负数。

3. **name 唯一性**：当使用 `name` 属性进行字符串匹配时，确保每个 `wd-tab` 的 `name` 值唯一。重复的 `name` 值会在控制台输出警告信息。

4. **索引越界兜底**：当 `modelValue` 设置的数字索引超出 `wd-tab` 子组件数量范围时，组件会自动将索引重置为 0。

5. **弹窗中更新指示条**：在 `wd-popup` 等弹出层组件中使用 Tabs 时，由于弹窗内容在打开后才渲染，底部指示条的位置可能计算不准确。必须在弹窗完全展开后（如 `@after-enter` 事件回调中）调用 `updateLineStyle()` 方法重新计算指示条位置。

6. **手势滑动依赖动画**：开启 `swipeable` 手势滑动功能时，建议同时开启 `animated` 属性以获得流畅的切换体验。手势滑动的最小触发滑动距离为 50px。

7. **导航地图自动触发**：当标签数量超过 `mapNum`（默认 10）时，导航栏右侧会自动出现导航地图按钮。点击按钮可以展开全屏选项列表，方便快速跳转。导航地图的标题可通过 `mapTitle` 属性自定义。

8. **懒加载渲染**：`wd-tab` 默认开启 `lazy` 懒加载模式，tab 内容仅在首次被激活时才进行渲染。如果需要在初始化时就渲染所有 tab 内容，可将 `lazy` 设置为 `false`。

9. **指示条样式优先级**：当同时设置了 `lineWidth` 和 `autoLineWidth` 时，`lineWidth` 的优先级更高，`autoLineWidth` 将不会生效。

10. **滚动导航模式**：`slidable="always"` 模式下无论标签数量多少都开启横向滚动，适用于标签文字较长或需要始终支持滚动的场景。`slidable="auto"` 模式下只有标签数量超过 `slidableNum`（默认 6）时才开启滚动。
