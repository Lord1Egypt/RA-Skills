# SwipeAction 滑动操作


## 组件概况

SwipeAction 滑动操作组件是一个支持左右滑动手势的容器组件，用于在列表项等场景中隐藏展示操作按钮。用户通过横向滑动内容区域，可滑出左侧或右侧的操作按钮面板，实现删除、编辑、置顶等快捷操作。组件支持单侧或双侧操作按钮、程序化控制展开状态、关闭前拦截钩子、多实例互斥管理以及完整的触摸手势处理（自动区分横向/纵向滑动），适用于消息列表、邮件列表、文件管理等需要隐藏操作入口的场景。

## 核心功能描述

- **左右双侧操作**：通过 `#left` 和 `#right` 插槽分别定义左右两侧操作按钮，可单独使用或同时使用
- **手势滑动**：支持触摸滑动操作，滑动距离超过按钮宽度 30% 阈值时自动展开对应侧按钮，未达阈值则回弹闭合
- **程序化控制**：通过 `v-model` 绑定状态值（`'left'`、`'close'`、`'right'`），可从外部控制展开/收起状态
- **关闭前拦截**：`beforeClose` 钩子函数在每次关闭操作按钮前执行，可接收关闭原因（`click`、`swipe`、`value`）和关闭位置（`left`、`right`、`inside`）
- **多实例互斥**：多个 SwipeAction 实例共存时，展开当前实例会自动收起其他实例，通过队列机制管理
- **横纵手势区分**：内置手势方向识别，纵向滑动时不会拦截页面滚动，仅横向滑动时阻止默认行为和事件冒泡
- **点击关闭**：已展开操作按钮时，点击内容区域会自动收起按钮并触发 `click` 事件，返回关闭位置信息
- **平滑动画**：收起时带有 600ms cubic-bezier(0.18, 0.89, 0.32, 1) 缓动过渡动画，跟随手指滑动时无动画延迟
- **溢出隐藏**：容器使用 `overflow: hidden`，操作按钮在未滑出时完全隐藏
- **暗色模式支持**：通过 `wot-theme-dark` 类名自动适配暗色主题

## 适用业务场景

- **列表项操作**：消息列表、邮件列表、联系人列表中的删除、标记已读、置顶等操作
- **文件管理**：文件列表中的删除、重命名、移动、分享等操作入口
- **购物车操作**：购物车商品项中的删除、收藏、数量修改等操作
- **通知管理**：通知项的删除、免打扰、归档等操作
- **需要隐藏操作的列表**：操作按钮不常使用但需要时可快速触达的场景
- **双侧操作需求**：左侧用于收藏/标记，右侧用于删除/编辑的双向操作场景

## API

### Props

| 属性名称 | 类型 | 默认值 | 是否必填 | 说明 |
|---------|------|--------|---------|------|
| modelValue | `'left' \| 'close' \| 'right'` | `'close'` | 否 | 滑动按钮的状态，支持 `v-model` 双向绑定 |
| disabled | boolean | `false` | 否 | 是否禁用滑动操作 |
| beforeClose | `(reason: SwipeActionReason, position: SwipeActionPosition) => void` | - | 否 | 关闭操作按钮前的钩子函数 |
| customStyle | string | `''` | 否 | 自定义根节点样式 |
| customClass | string | `''` | 否 | 自定义根节点类名 |

#### modelValue 可选值

| 值 | 状态描述 |
|---|---------|
| `left` | 左滑展开，展示左侧操作按钮 |
| `close` | 关闭状态，不展示任何操作按钮 |
| `right` | 右滑展开，展示右侧操作按钮 |

#### beforeClose 回调参数

**reason**（关闭原因）可选值：

| 值 | 触发场景 |
|---|---------|
| `click` | 用户点击内容区域导致关闭 |
| `swipe` | 用户反向滑动导致关闭 |
| `value` | 通过外部修改 `modelValue` 导致关闭 |

**position**（关闭位置）可选值：

| 值 | 说明 |
|---|------|
| `left` | 关闭的是左侧操作按钮 |
| `right` | 关闭的是右侧操作按钮 |
| `inside` | 点击的是内容区域内部（仅 click 原因时返回） |

### Events

| 事件名称 | 回调参数 | 说明 |
|---------|---------|------|
| update:modelValue | `'left' \| 'close' \| 'right'` | 滑动状态变化时触发，传入当前状态值 |
| click | `{ value: 'left' \| 'right' \| 'inside' }` | 点击事件，当操作按钮已展开时点击内容区域触发，`value` 表示点击的位置 |

### Methods

通过 `ref` 获取组件实例后可调用以下方法：

| 方法名称 | 参数 | 说明 |
|---------|------|------|
| close | - | 关闭操作按钮（等效于设置 `modelValue` 为 `'close'`） |

### Slots

| 插槽名称 | 作用域参数 | 使用场景 |
|---------|-----------|---------|
| default | - | 内容区域，通常放置 `wd-cell` 或其他列表项内容 |
| left | - | 左侧操作按钮区域，向左滑动时展示 |
| right | - | 右侧操作按钮区域，向右滑动时展示 |

## 使用示例

### 示例 1：基本用法

展示右侧操作按钮的基础用法，最常见的单侧滑动操作场景。

```vue
<template>
  <view>
    <!-- 仅右侧操作按钮 -->
    <wd-swipe-action>
      <wd-cell title="标题文字" value="内容" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350" @click="handleAction('删除')">删除</view>
          <view class="button" style="background: #f0883a" @click="handleAction('编辑')">编辑</view>
          <view class="button" style="background: #4d80f0" @click="handleAction('更多')">更多</view>
        </view>
      </template>
    </wd-swipe-action>

    <!-- 多个列表项 -->
    <wd-swipe-action>
      <wd-cell title="邮件 1" value="未读" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350">删除</view>
          <view class="button" style="background: #4d80f0">标记已读</view>
        </view>
      </template>
    </wd-swipe-action>

    <wd-swipe-action>
      <wd-cell title="邮件 2" value="已读" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350">删除</view>
          <view class="button" style="background: #4d80f0">置顶</view>
        </view>
      </template>
    </wd-swipe-action>
  </view>
</template>
<script lang="ts" setup>
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const toast = useToast()

  function handleAction(action: string) {
    toast.show('点击了' + action)
  }
</script>
<style lang="scss" scoped>
  .action {
    height: 100%;
    display: flex;
  }
  .button {
    display: inline-block;
    padding: 0 15px;
    height: 100%;
    color: white;
    line-height: 46px;
  }
</style>
```

右侧操作按钮通过 `#right` 插槽定义，内容区域通过默认插槽放置 `wd-cell` 组件。操作按钮区域建议设置 `height: 100%` 使其与内容区域等高。多个 SwipeAction 实例同时存在时，滑动展开一个会自动收起其他已展开的实例。

### 示例 2：左右双侧滑动

同时定义左右两侧操作按钮，支持向左和向右滑动展示不同操作。

```vue
<template>
  <view>
    <wd-swipe-action>
      <!-- 左侧操作按钮 -->
      <template #left>
        <view class="action">
          <view class="button" style="background: #34d19d">置顶</view>
          <view class="button" style="background: #4d80f0">收藏</view>
        </view>
      </template>

      <!-- 内容区域 -->
      <wd-cell title="标题文字" value="内容" />

      <!-- 右侧操作按钮 -->
      <template #right>
        <view class="action">
          <view class="button" style="background: #f0883a">编辑</view>
          <view class="button" style="background: #fa4350">删除</view>
        </view>
      </template>
    </wd-swipe-action>
  </view>
</template>
<script lang="ts" setup>
</script>
<style lang="scss" scoped>
  .action {
    height: 100%;
    display: flex;
  }
  .button {
    display: inline-block;
    padding: 0 15px;
    height: 100%;
    color: white;
    line-height: 46px;
  }
</style>
```

同时使用 `#left` 和 `#right` 插槽可以定义双侧操作。左侧适合放置正向操作（如收藏、置顶、标星），右侧适合放置负向操作（如删除、屏蔽）。滑动时仅能向一侧展开，展开一侧后需先收起才能滑出另一侧。操作按钮数量不受限制，可根据需要自由增减。

### 示例 3：程序化控制状态

通过 `v-model` 绑定状态值，使用外部按钮控制展开/收起。

```vue
<template>
  <view>
    <wd-swipe-action v-model="value">
      <template #left>
        <view class="action">
          <view class="button" style="background: #34d19d">置顶</view>
          <view class="button" style="background: #4d80f0">收藏</view>
          <view class="button" style="background: #fa4350">标记</view>
        </view>
      </template>

      <wd-cell title="标题文字" value="内容" />

      <template #right>
        <view class="action">
          <view class="button" style="background: #f0883a">编辑</view>
          <view class="button" style="background: #4d80f0">分享</view>
          <view class="button" style="background: #fa4350">删除</view>
        </view>
      </template>
    </wd-swipe-action>

    <!-- 外部控制按钮 -->
    <view class="button-group">
      <wd-button size="small" @click="changeState('left')">打开左边</wd-button>
      <wd-button size="small" @click="changeState('close')">关闭所有</wd-button>
      <wd-button size="small" @click="changeState('right')">打开右边</wd-button>
    </view>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import type { SwipeActionStatus } from '@/uni_modules/wot-ui-plus/components/wd-swipe-action/types'

  const value = ref<SwipeActionStatus>('close')

  function changeState(position: SwipeActionStatus) {
    value.value = position
  }
</script>
<style lang="scss" scoped>
  .action {
    height: 100%;
    display: flex;
  }
  .button {
    display: inline-block;
    padding: 0 15px;
    height: 100%;
    color: white;
    line-height: 46px;
  }
  .button-group {
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
  }
</style>
```

通过 `v-model` 绑定 `SwipeActionStatus` 类型的值，可从外部控制组件状态。`'left'` 展开左侧按钮，`'right'` 展开右侧按钮，`'close'` 收起所有按钮。也可以通过 `ref` 获取组件实例后调用 `close()` 方法收起按钮。

### 示例 4：关闭前拦截

使用 `beforeClose` 钩子函数在关闭操作按钮前执行自定义逻辑。

```vue
<template>
  <view>
    <wd-swipe-action v-model="value" :before-close="beforeClose">
      <template #left>
        <view class="action">
          <view class="button" style="background: #34d19d">置顶</view>
          <view class="button" style="background: #4d80f0">收藏</view>
        </view>
      </template>

      <wd-cell title="标题文字" value="内容" />

      <template #right>
        <view class="action">
          <view class="button" style="background: #f0883a">编辑</view>
          <view class="button" style="background: #fa4350">删除</view>
        </view>
      </template>
    </wd-swipe-action>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'
  import type { SwipeActionBeforeClose, SwipeActionStatus } from '@/uni_modules/wot-ui-plus/components/wd-swipe-action/types'

  const toast = useToast()
  const value = ref<SwipeActionStatus>('close')

  const beforeClose: SwipeActionBeforeClose = (reason, position) => {
    if (reason === 'click') {
      toast.show(`点击 ${position} 区域导致滑动按钮关闭`)
    } else {
      toast.show(`${reason} 导致 ${position} 滑动按钮关闭`)
    }
  }
</script>
<style lang="scss" scoped>
  .action {
    height: 100%;
    display: flex;
  }
  .button {
    display: inline-block;
    padding: 0 15px;
    height: 100%;
    color: white;
    line-height: 46px;
  }
</style>
```

`beforeClose` 钩子函数接收两个参数：`reason`（关闭原因）和 `position`（关闭位置）。关闭原因包括 `'click'`（点击关闭）、`'swipe'`（滑动关闭）、`'value'`（通过修改 value 关闭），关闭位置包括 `'left'`、`'right'`、`'inside'`。此钩子适合用于关闭前显示确认提示、记录操作日志等场景。注意：此钩子为同步执行，关闭操作会在此钩子执行完毕后继续进行。

### 示例 5：点击事件与禁用状态

展示点击事件监听以及禁用滑动功能的使用方式。

```vue
<template>
  <view>
    <!-- 点击事件：已展开操作按钮时点击内容区域会触发 -->
    <wd-swipe-action @click="handleClick">
      <wd-cell title="标题文字" value="内容" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350">删除</view>
          <view class="button" style="background: #f0883a">编辑</view>
          <view class="button" style="background: #4d80f0">更多</view>
        </view>
      </template>
    </wd-swipe-action>

    <!-- 禁用状态：无法滑动，操作按钮始终隐藏 -->
    <wd-swipe-action disabled>
      <wd-cell title="此条目已锁定" value="不可操作" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350">删除</view>
          <view class="button" style="background: #f0883a">编辑</view>
        </view>
      </template>
    </wd-swipe-action>

    <!-- 动态禁用 -->
    <wd-swipe-action :disabled="isDisabled">
      <wd-cell title="动态控制" value="根据条件禁用" />
      <template #right>
        <view class="action">
          <view class="button" style="background: #fa4350">删除</view>
        </view>
      </template>
    </wd-swipe-action>
  </view>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { useToast } from '@/uni_modules/wot-ui-plus'

  const toast = useToast()
  const isDisabled = ref<boolean>(false)

  function handleClick({ value }: { value: string }) {
    toast.show(`点击 ${value} 位置关闭操作按钮`)
  }
</script>
<style lang="scss" scoped>
  .action {
    height: 100%;
    display: flex;
  }
  .button {
    display: inline-block;
    padding: 0 15px;
    height: 100%;
    color: white;
    line-height: 46px;
  }
</style>
```

`click` 事件在操作按钮已展开时点击内容区域触发，回调参数中 `value` 为 `'left'`、`'right'` 或 `'inside'`，表示点击位置。事件触发后操作按钮会自动收起。设置 `disabled` 为 `true` 后，组件无法响应滑动手势，操作按钮始终保持隐藏状态，`beforeClose` 和 `click` 事件也不会触发。

## 注意事项

1. **多实例互斥管理**：页面中同时存在多个 SwipeAction 组件时，展开其中一个会自动收起其他已展开的实例，这是通过内部队列机制实现的。如需关闭所有 SwipeAction，可调用 `useQueue().closeOutside()` 方法
2. **滑动阈值**：操作按钮展开的阈值为按钮宽度的 30%（`THRESHOLD = 0.3`），滑动距离超过此比例会自动展开到最大，未达到则回弹收起
3. **横纵向手势区分**：组件内置手势方向识别，当检测到纵向滑动时会放行事件，不阻止页面滚动；仅横向滑动时调用 `preventDefault()` 和 `stopPropagation()` 阻止默认行为和事件冒泡
4. **操作按钮完全展开后锁定**：当操作按钮已完全展开时，继续向同一方向滑动不会生效，组件会模拟一次新的 `startDrag` 事件重置滑动起始点
5. **未存在侧按钮时的行为**：如果某一侧未定义对应插槽（宽度为 0），向该方向滑动时会自动回弹，不会触发任何效果
6. **点击关闭的逻辑**：当操作按钮已展开时，点击内容区域（非操作按钮区域）会自动收起按钮并触发 `click` 事件，`value` 为 `'inside'`；点击左/右操作按钮区域则 `value` 分别为 `'left'` 或 `'right'`
7. **过渡动画条件**：跟随手指滑动时（`touching` 为 `true`）不使用过渡动画以保证跟手性；松手后自动修正位置时使用 600ms cubic-bezier(0.18, 0.89, 0.32, 1) 缓动动画
8. **beforeClose 为同步钩子**：`beforeClose` 是同步执行的函数，不支持返回 Promise 进行异步拦截。如需确认弹窗等异步操作，建议在外部通过 `click` 事件或 `update:modelValue` 事件自行处理
9. **溢出隐藏**：组件根容器使用 `overflow: hidden`，操作按钮在未滑出时完全不可见，确保不会影响页面布局和其他元素
10. **外部控制状态时需处理互斥**：通过 `v-model` 程序化设置展开状态时，同样会触发多实例互斥机制，自动收起其他已展开的 SwipeAction 实例
