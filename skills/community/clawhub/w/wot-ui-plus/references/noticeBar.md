# NoticeBar 通知栏

用于循环播放提示给用户的通知栏组件，支持水平滚动、垂直切换、多文本轮播等能力。

## 何时使用

- 需要向用户展示滚动播报的通知信息时
- 需要在有限空间内展示多条轮播公告时
- 需要支持可关闭、可自定义样式的消息提醒时

## 基本用法

最基本的用法，通过 `text` 传入通知文案，`prefix` 设置左侧图标。

```vue
<template>
  <wd-notice-bar
    text="这是一条消息提示信息，这是一条消息提示信息，这是一条消息提示信息"
    prefix="warn-bold"
  />
</template>
```

## 进阶示例

### 示例一：不同类型

通过 `type` 属性修改通知栏的类型，支持 `warning` | `info` | `danger` 三种类型，每种类型对应不同的背景色和文字颜色。

```vue
<template>
  <wd-notice-bar
    type="danger"
    text="当前网络不可用，请检查你的网络设置"
    prefix="wifi-error"
  />
  <wd-notice-bar
    type="info"
    text="点击查看信息详情，点击查看信息详情，点击查看信息详情"
    prefix="check-outline"
  />
</template>
```

### 示例二：可关闭通知栏

设置 `closable` 属性，通知栏右侧会出现关闭按钮，点击后隐藏通知栏并触发 `close` 事件。

```vue
<template>
  <wd-notice-bar
    text="这是一条消息提示信息，这是一条消息提示信息，这是一条消息提示信息。"
    closable
    prefix="warn-bold"
    @close="handleClose"
  />
</template>

<script setup lang="ts">
function handleClose() {
  console.log('通知栏已关闭')
}
</script>
```

### 示例三：多文本轮播（水平）

将 `text` 设置为字符串数组，组件会自动轮播数组中的每条文本，配合 `next` 事件可监听切换逻辑。

```vue
<template>
  <wd-notice-bar
    :text="textArray"
    prefix="check-outline"
    @next="onNext"
    @click="handleClick"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const textArray = ref([
  '欢迎使用 wot-ui-plus',
  '该组件库基于 uniapp Vue3 TS 构建',
  '项目地址：https://github.com/moonofweisheng/wot-design-uni',
  '我们的目标是打造最强 uniapp 组件库',
  '诚挚邀请大家共同建设'
])

const onNext = (index: number) => {
  console.log('展示下一条，index:', index)
  console.log('文本是：' + textArray.value[index])
}

const handleClick = (result: { index: number; text: string }) => {
  console.log('点击了第', result.index + 1, '条:', result.text)
}
</script>
```

### 示例四：垂直滚动

将 `direction` 设置为 `vertical`，文本会以垂直方向上下切换轮播。可通过 `delay` 调整切换间隔时间（单位：秒）。

```vue
<template>
  <wd-notice-bar
    :text="textArray"
    prefix="warn-bold"
    direction="vertical"
    :delay="3"
    @click="handleClick"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const textArray = ref([
  '欢迎使用 wot-ui-plus',
  '该组件库基于 uniapp Vue3 TS 构建',
  '我们的目标是打造最强 uniapp 组件库'
])

const handleClick = (result: { index: number; text: string }) => {
  console.log(result)
}
</script>
```

### 示例五：自定义颜色

通过 `color` 和 `background-color` 属性自定义文字颜色和背景颜色。

```vue
<template>
  <wd-notice-bar
    text="这是一条消息提示信息，这是一条消息提示信息，这是一条消息提示信息"
    prefix="check-outline"
    color="#34D19D"
    background-color="#f0f9eb"
  />
</template>
```

### 示例六：多行展示

设置 `wrapable` 为 `true` 且 `scrollable` 为 `false` 可实现文本多行换行展示。

```vue
<template>
  <wd-notice-bar
    text="这是一条消息提示信息这是一条消息提示信息这是一条消息提示信息这是一条消息提示信息这是一条消息提示信息这是一条消息提示信息"
    wrapable
    :scrollable="false"
  />
</template>
```

### 示例七：自定义插槽

通过 `prefix` 和 `suffix` 插槽可以自定义左侧和右侧内容。

```vue
<template>
  <wd-notice-bar :scrollable="false">
    <template #prefix>
      <wd-icon name="attention">占位符</wd-icon>
    </template>
    通知被禁或时段内消息屏蔽可能造成消息...
    <template #suffix>
      <view style="color: #4d80f0">查看</view>
    </template>
  </wd-notice-bar>
</template>
```

### 示例八：重置播放动画

通过组件实例的 `reset()` 方法可以手动重置通知栏的播放动画。

```vue
<template>
  <wd-notice-bar
    ref="noticeRef"
    :text="textArray"
    prefix="warn-bold"
    direction="vertical"
    :delay="3"
  />
  <wd-button @click="handleReset">重置播放动画</wd-button>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { NoticeBarInstance } from '@/uni_modules/wot-ui-plus/components/wd-notice-bar/types'

const noticeRef = ref<NoticeBarInstance>()
const textArray = ref([
  '欢迎使用 wot-ui-plus',
  '该组件库基于 uniapp Vue3 TS 构建',
  '我们的目标是打造最强 uniapp 组件库'
])

const handleReset = () => {
  noticeRef.value?.reset()
}
</script>
```

## API

### Props

| 属性名 | 说明 | 类型 | 默认值 |
|--------|------|------|--------|
| text | 通知栏文案，支持字符串或字符串数组 | `string \| string[]` | `''` |
| type | 通知栏类型 | `'warning' \| 'info' \| 'danger' \| ''` | `'warning'` |
| scrollable | 是否可滚动 | `boolean` | `true` |
| delay | 滚动延迟时间（秒） | `number` | `1` |
| speed | 滚动速度（px/s） | `number` | `50` |
| closable | 是否可关闭 | `boolean` | `false` |
| wrapable | 是否换行显示 | `boolean` | `false` |
| prefix | 左侧图标名称（使用 icon 章节中的图标名） | `string` | `-` |
| color | 文字、图标颜色 | `string` | `-` |
| background-color | 背景颜色 | `string` | `-` |
| direction | 滚动方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| custom-style | 自定义根节点样式 | `string` | `-` |
| custom-class | 自定义根节点 class | `string` | `-` |

### Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| close | 关闭按钮点击时触发 | `-` |
| next | 切换下一条通知时触发 | `(index: number): void` |
| click | 点击通知栏内容时触发 | `(result: { index: number; text: string }): void` |

> `click` 事件回调参数说明：
> - `index`: 当前点击文本在数组中的索引（text 为数组时）
> - `text`: 当前点击的文本内容

### Slots

| 插槽名 | 说明 |
|--------|------|
| prefix | 自定义左侧内容，与 `prefix` 属性互斥 |
| suffix | 自定义右侧内容，与 `closable` 属性互斥 |

### Expose

通过 `ref` 可以获取组件实例，调用实例方法。

| 方法名 | 说明 | 类型 |
|--------|------|------|
| reset | 重置通知栏动画 | `() => void` |

## 注意事项

1. 使用垂直滚动（`direction="vertical"`）且 `text` 为数组时，文本会逐条垂直切换轮播；如果数组仅有一条文本则不会滚动。
2. 水平滚动模式下，`scrollable` 为 `true` 时文本会从右往左无限循环滚动；`scrollable` 为 `false` 时超出部分以省略号截断。
3. 组件支持 `keep-alive` 缓存，在组件激活（`onActivated`）时自动恢复动画，失活（`onDeactivated`）时自动停止动画。
4. `prefix` 属性与 `prefix` 插槽互斥：设置了 `prefix` 属性时显示图标，否则显示 `prefix` 插槽内容。
5. `closable` 属性与 `suffix` 插槽互斥：设置了 `closable` 时显示关闭按钮，否则显示 `suffix` 插槽内容。
