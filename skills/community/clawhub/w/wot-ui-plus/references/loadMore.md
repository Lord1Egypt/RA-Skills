# Loadmore 加载更多


## 组件概况

Loadmore 加载更多组件是一个用于列表底部展示加载状态提示的组件，通常与滚动分页加载场景配合使用。该组件通过 `state` 属性切换三种加载状态（`loading` 加载中、`error` 加载失败、`finished` 加载完成），在不同状态下展示对应的 UI 内容和交互元素。

组件内部基于 wd-loading（加载动画）、wd-divider（分割线）、wd-icon（图标）等基础组件组合构建。在 `loading` 状态下展示 loading 旋转动画与加载提示文案；在 `error` 状态下展示错误提示、"点击重试"引导文字及刷新图标，点击组件区域可触发重新加载；在 `finished` 状态下展示分割线与加载完毕提示文案。组件内置多语言支持，各状态的提示文案均有默认值，也可通过属性自定义覆盖。

## 核心功能描述

- **三种状态切换**：通过 `state` 属性控制组件展示 `loading`（加载中）、`error`（加载失败）、`finished`（加载完成）三种状态对应的 UI
- **加载动画**：在 `loading` 状态下渲染 wd-loading 旋转动画组件，配合提示文案告知用户当前正在加载数据
- **错误重试**：在 `error` 状态下展示加载失败提示、点击重试文字和刷新图标，点击组件整体区域触发 `reload` 事件
- **加载完成**：在 `finished` 状态下使用 wd-divider 分割线展示已加载完毕提示，视觉上将列表内容与页面底部自然分隔
- **自定义文案**：通过 `loadingText`、`errorText`、`finishedText` 属性自定义各状态的提示文字，满足业务场景的个性化需求
- **多语言支持**：内置 `useTranslate` 国际化方案，各状态文案有默认中文提示（如"正在努力加载中..."、"加载失败"、"已加载完毕"），未传入自定义文案时自动使用国际化文案
- **loadingProps 透传**：通过 `loadingProps` 属性将配置项传递给内部的 wd-loading 组件，可自定义 loading 动画的颜色、尺寸、类型等
- **自定义样式**：支持通过 `customStyle` 和 `customClass` 属性自定义组件根元素样式

## 适用业务场景

- **列表分页加载**：在长列表或 Feed 流的底部展示加载状态，配合页面触底事件实现分页数据加载
- **下拉刷新/上拉加载**：与滚动组件配合，在用户滚动到底部时展示加载更多状态
- **数据加载失败重试**：在网络异常等场景下展示加载失败提示，提供一键重试能力
- **数据加载完成提示**：当所有数据加载完毕时展示"已加载完毕"提示，给用户明确的反馈
- **图片/视频瀑布流**：在瀑布流布局中配合触底加载实现无限滚动浏览

## API

### Props

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| state | `'loading'` \| `'error'` \| `'finished'` | - | 否 | 加载状态，控制组件展示的 UI 形态。`loading` 表示加载中，`error` 表示加载失败，`finished` 表示加载完成 |
| loadingText | string | - | 否 | 加载中的提示文案。未传入时使用国际化默认值"正在努力加载中..." |
| finishedText | string | - | 否 | 加载完成时的提示文案。未传入时使用国际化默认值"已加载完毕" |
| errorText | string | - | 否 | 加载失败时的提示文案。未传入时使用国际化默认值"加载失败" |
| loadingProps | `Partial<LoadingProps>` | - | 否 | 传递给内部 wd-loading 组件的属性配置，可自定义 loading 动画的颜色、尺寸、类型等 |
| customStyle | string | '' | 否 | 自定义组件根元素的内联样式 |
| customClass | string | '' | 否 | 自定义组件根元素的样式类名 |

### Events

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| reload | - | 仅在 `state` 为 `error` 状态下，点击组件区域时触发，用于通知父组件重新加载数据 |

### Slots

当前组件未定义插槽。

### Methods

当前源码中未通过 `defineExpose` 暴露实例方法。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-loadmore | 组件根节点样式类，可设置整体宽高、文字颜色等 |
| wd-loadmore\_\_loading | 内部 wd-loading 组件的样式类，可自定义 loading 动画样式 |
| wd-loadmore\_\_text | 提示文字样式类，应用于各状态的文本元素 |
| wd-loadmore\_\_text.is-light | 错误状态下"点击重试"文字的浅色高亮样式类 |
| wd-loadmore\_\_refresh | 错误状态下刷新图标的样式类 |

## 使用示例

### 示例 1：基础分页加载

效果说明：最常见的列表分页加载场景。通过监听页面触底事件（`onReachBottom`），根据 `state` 状态切换实现加载中、加载失败、加载完成三种状态的展示。配合模拟数据加载流程演示完整的分页加载生命周期。

```vue
<template>
  <view class="container">
    <!-- 列表数据 -->
    <view v-for="item in list" :key="item.id" class="list-item">
      <text>{{ item.title }}</text>
    </view>

    <!-- 加载更多组件 -->
    <wd-loadmore :state="state" @reload="handleReload" />
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onReachBottom } from '@dcloudio/uni-app'
import type { LoadMoreState } from 'wot-design-uni/components/wd-loadmore/types'

const list = ref<Array<{ id: number; title: string }>>([])
const state = ref<LoadMoreState>('loading')
const currentPage = ref<number>(1)
const maxPage = ref<number>(5)

// 初始化加载
onMounted(() => {
  loadData()
})

// 监听页面触底
onReachBottom(() => {
  if (state.value === 'error') {
    // 错误状态下由用户手动点击重试
    return
  }
  if (currentPage.value >= maxPage.value) {
    state.value = 'finished'
    return
  }
  loadData()
})

// 加载数据
function loadData() {
  state.value = 'loading'
  // 模拟异步请求
  setTimeout(() => {
    const newItems = Array.from({ length: 10 }, (_, i) => ({
      id: (currentPage.value - 1) * 10 + i + 1,
      title: `列表项 ${(currentPage.value - 1) * 10 + i + 1}`
    }))
    list.value = [...list.value, ...newItems]
    currentPage.value++

    // 模拟第 3 页加载失败
    if (currentPage.value === 3) {
      state.value = 'error'
    } else if (currentPage.value > maxPage.value) {
      state.value = 'finished'
    } else {
      state.value = 'loading'
    }
  }, 1000)
}

// 点击重试
function handleReload() {
  // 回退页码后重新加载
  currentPage.value--
  loadData()
}
</script>

<style scoped lang="scss">
.container {
  padding: 0 16px;
}

.list-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

### 示例 2：自定义提示文案

效果说明：通过 `loadingText`、`errorText`、`finishedText` 属性自定义各状态下的提示文字，使用更贴近业务场景的文案表达。

```vue
<template>
  <view class="container">
    <view v-for="item in list" :key="item.id" class="list-item">
      <text>{{ item.title }}</text>
    </view>

    <wd-loadmore
      :state="state"
      loading-text="数据加载中，请稍候..."
      error-text="网络异常，请检查网络后重试"
      finished-text="没有更多内容了"
      @reload="handleReload"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onReachBottom } from '@dcloudio/uni-app'
import type { LoadMoreState } from 'wot-design-uni/components/wd-loadmore/types'

const list = ref<Array<{ id: number; title: string }>>([])
const state = ref<LoadMoreState>('loading')
const currentPage = ref<number>(1)

onMounted(() => {
  loadData()
})

onReachBottom(() => {
  if (state.value === 'loading' || state.value === 'error') return
  loadData()
})

function loadData() {
  state.value = 'loading'
  setTimeout(() => {
    const newItems = Array.from({ length: 10 }, (_, i) => ({
      id: (currentPage.value - 1) * 10 + i + 1,
      title: `资讯 ${(currentPage.value - 1) * 10 + i + 1}`
    }))
    list.value = [...list.value, ...newItems]
    currentPage.value++

    if (currentPage.value > 3) {
      state.value = 'finished'
    }
  }, 800)
}

function handleReload() {
  currentPage.value--
  loadData()
}
</script>

<style scoped lang="scss">
.container {
  padding: 0 16px;
}

.list-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

### 示例 3：自定义 Loading 动画样式

效果说明：通过 `loadingProps` 属性向内部 wd-loading 组件传递配置，自定义 loading 动画的颜色和尺寸，使其与页面主题风格保持一致。

```vue
<template>
  <view class="container">
    <view v-for="item in list" :key="item.id" class="list-item">
      <text>{{ item.title }}</text>
    </view>

    <wd-loadmore
      :state="state"
      :loading-props="{
        color: '#409eff',
        size: '24px'
      }"
      @reload="handleReload"
    />
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onReachBottom } from '@dcloudio/uni-app'
import type { LoadMoreState } from 'wot-design-uni/components/wd-loadmore/types'

const list = ref<Array<{ id: number; title: string }>>([])
const state = ref<LoadMoreState>('loading')
const currentPage = ref<number>(1)

onMounted(() => {
  loadData()
})

onReachBottom(() => {
  if (state.value === 'loading') return
  loadData()
})

function loadData() {
  state.value = 'loading'
  setTimeout(() => {
    const newItems = Array.from({ length: 10 }, (_, i) => ({
      id: (currentPage.value - 1) * 10 + i + 1,
      title: `动态 ${(currentPage.value - 1) * 10 + i + 1}`
    }))
    list.value = [...list.value, ...newItems]
    currentPage.value++

    if (currentPage.value > 3) {
      state.value = 'finished'
    }
  }, 1200)
}

function handleReload() {
  currentPage.value--
  loadData()
}
</script>

<style scoped lang="scss">
.container {
  padding: 0 16px;
}

.list-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

### 示例 4：单独展示各状态

效果说明：通过按钮手动切换 `state` 属性值，直观展示 loading、error、finished 三种状态下的 UI 表现，适用于调试和演示场景。

```vue
<template>
  <view class="state-switcher">
    <wd-button
      v-for="s in states"
      :key="s.value"
      :type="state === s.value ? 'primary' : 'default'"
      size="small"
      @click="state = s.value"
    >
      {{ s.label }}
    </wd-button>
  </view>

  <view class="demo-list">
    <view v-for="i in 10" :key="i" class="demo-item">
      <text>列表项 {{ i }}</text>
    </view>
  </view>

  <wd-loadmore
    :state="state"
    loading-text="正在加载..."
    error-text="加载出错"
    finished-text="全部加载完成"
    @reload="handleReload"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { LoadMoreState } from 'wot-design-uni/components/wd-loadmore/types'

const state = ref<LoadMoreState>('loading')
const states = [
  { label: '加载中', value: 'loading' as LoadMoreState },
  { label: '加载失败', value: 'error' as LoadMoreState },
  { label: '加载完成', value: 'finished' as LoadMoreState }
]

function handleReload() {
  // 模拟重试后恢复为 loading 状态
  state.value = 'loading'
  setTimeout(() => {
    state.value = 'finished'
  }, 1500)
}
</script>

<style scoped lang="scss">
.state-switcher {
  display: flex;
  gap: 12px;
  padding: 16px;
}

.demo-list {
  padding: 0 16px;
}

.demo-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

## 注意事项

1. **state 状态必填**：`state` 属性为控制组件 UI 形态的核心属性，不传值时组件不会展示任何内容。请根据实际加载阶段正确切换 `loading` / `error` / `finished` 三种状态。

2. **错误状态交互**：仅在 `state` 为 `error` 时，点击组件才会触发 `reload` 事件。在 `loading` 和 `finished` 状态下点击组件不会触发任何事件。

3. **国际化文案**：组件内置 `useTranslate('loadmore')` 国际化方案，当未传入 `loadingText`、`errorText`、`finishedText` 时，自动使用对应语言的默认文案（中文："正在努力加载中..."、"加载失败"、"已加载完毕"、"点击重试"）。

4. **状态切换时机**：建议在发起数据请求前将状态设为 `loading`，请求成功且还有更多数据时保持或恢复为 `loading`，请求成功且无更多数据时设为 `finished`，请求失败时设为 `error`。

5. **错误重试机制**：在 `error` 状态下触发 `reload` 事件后，父组件应在重新发起请求前将 `state` 重置为 `loading`，以保证用户能立即看到加载中的视觉反馈。

6. **loadingProps 透传**：`loadingProps` 属性接受 `Partial<LoadingProps>` 类型对象，支持传递 wd-loading 组件的所有属性（如 `color`、`size`、`type` 等）。组件内部会自动为 `customClass` 添加 `wd-loadmore__loading` 前缀类名，请勿手动覆盖该类名。

7. **与滚动容器配合**：在 H5 平台可配合页面的 `onReachBottom` 生命周期事件触发加载。在自定义滚动容器（如 `scroll-view`）中，需监听容器自身的滚动触底事件来切换状态。

8. **主题定制**：Loadmore 组件支持通过 CSS 变量进行主题定制，可用的 CSS 变量包括：
   - `--wot-loadmore-height`：组件高度（默认 48px）
   - `--wot-loadmore-color`：文字颜色（默认 rgba(0, 0, 0, 0.45)）
   - `--wot-loadmore-fs`：文字字号（默认 14px）
   - `--wot-loadmore-error-color`：错误状态重试文字颜色（默认主题色）
   - `--wot-loadmore-refresh-fs`：刷新图标字号（默认 16px）
   - `--wot-loadmore-loading-size`：loading 动画尺寸（默认 16px）

9. **暗色主题**：组件内置暗色主题适配，在 `.wot-theme-dark` 容器下文字颜色会自动切换为 `--wot-dark-color` 变量值。

10. **分割线展示**：`finished` 状态下使用 `wd-divider` 分割线组件承载提示文案，视觉上呈现为一条带文字的水平分割线，将列表内容与页面底部自然分隔。
