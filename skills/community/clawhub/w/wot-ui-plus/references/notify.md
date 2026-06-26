# Notify 通知


## 组件概况

Notify 通知组件是一种轻量级的页面级反馈提示组件，用于在页面顶部或底部向用户展示简短的通知消息。该组件基于 `wd-popup` 弹窗组件实现，采用从顶部或底部滑入的过渡动画，支持多种主题类型（主要、成功、危险、警告），并提供命令式调用和组件标签两种使用方式。

组件内部使用 Popup 弹窗的 top/bottom 位置模式实现滑入滑出效果，支持自定义背景颜色、字体颜色、展示时长、弹出位置等配置，并通过 `useNotify` 组合式 API 实现便捷的命令式调用。

## 核心功能描述

- **多种通知类型**：内置 primary（主要）、success（成功）、danger（危险）、warning（警告）四种预设主题色，满足不同场景的视觉反馈需求
- **命令式调用**：采用 `useNotify` 组合式 API 进行命令式调用，无需在模板中声明组件，调用即用
- **组件标签使用**：支持通过 `<wd-notify>` 标签在模板中使用，配合 `v-model:visible` 控制显隐
- **自动关闭**：通知默认在 3000ms 后自动关闭，支持自定义展示时长；设置为 0 时不会自动消失
- **位置控制**：支持顶部（`top`，默认）和底部（`bottom`）两种弹出位置
- **安全区域适配**：顶部弹出时支持通过 `safeHeight` 属性配置安全高度，适配刘海屏等特殊屏幕
- **自定义样式**：支持自定义字体颜色（`color`）和背景颜色（`background`），实现个性化视觉风格
- **换行支持**：消息内容支持通过 `\n` 实现换行，适用于多行文案展示
- **插槽定制**：提供默认插槽，支持完全自定义通知内容（如图标 + 文字组合）
- **生命周期回调**：提供 `onClick`、`onClosed`、`onOpened` 回调函数，便于执行交互逻辑
- **多实例支持**：通过 `selector` 参数创建独立的 Notify 实例，不同实例之间互不干扰
- **Root Portal 支持**：通过 `rootPortal` 属性将组件从页面中脱离出来，解决各种 fixed 定位失效问题（H5: teleport, APP: renderjs, 小程序: root-portal）

## 适用业务场景

- **操作反馈**：用户执行保存、提交、删除等操作后展示成功或失败通知
- **表单验证**：表单校验失败时展示错误提示信息
- **系统通知**：展示系统级别的通知消息，如版本更新、维护公告等
- **状态提醒**：网络断开、权限不足等异常状态提醒
- **操作引导**：在新手引导或功能提示中展示常规信息通知
- **多场景提示**：根据操作结果展示不同类型的通知（成功/失败/警告）

## API

### Props

以下为通过组件标签方式使用时的 Props。若使用 `useNotify` API 调用，可通过配置对象传入同名属性。

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| visible | boolean | false | 否 | 是否显示通知，支持 v-model 双向绑定 |
| type | 'primary' \| 'success' \| 'danger' \| 'warning' | 'danger' | 否 | 通知类型，对应不同的预设背景色 |
| message | string / number | '' | 否 | 展示文案，支持通过 `\n` 换行 |
| color | string | '' | 否 | 自定义字体颜色 |
| background | string | '' | 否 | 自定义背景颜色 |
| duration | number | 3000 | 否 | 展示时长，单位为毫秒；值为 0 时不会自动消失 |
| position | 'top' \| 'bottom' | 'top' | 否 | 弹出位置 |
| zIndex | number | 99 | 否 | 将组件的 z-index 层级设置为一个固定值 |
| safeHeight | number | - | 否 | 顶部安全高度，用于适配特殊屏幕 |
| selector | string | '' | 否 | 指定唯一标识，用于区分多个 Notify 实例 |
| rootPortal | boolean | false | 否 | 是否从页面中脱离出来，用于解决各种 fixed 失效问题 |

### useNotify API

`useNotify` 是 Notify 组件的核心调用方式，通过组合式 API 返回一个包含多个方法的对象。

```ts
import { useNotify } from '@/uni_modules/wot-ui-plus'

const notify = useNotify()
```

也可传入 `selector` 参数创建指定实例：

```ts
const notify = useNotify('#my-notify')
```

返回的 `notify` 对象包含以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| showNotify | `option: NotifyProps \| string` | void | 打开通知提示，支持传入配置对象或纯字符串文案 |
| closeNotify | - | void | 关闭当前通知，清除自动关闭定时器并隐藏组件 |

### 全局配置方法

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| setNotifyDefaultOptions | `options: NotifyProps` | void | 设置全局默认配置选项 |
| resetNotifyDefaultOptions | - | void | 重置全局默认配置为初始值 |

### NotifyProps 配置对象

通过 `useNotify` API 调用时，可传入的配置对象结构如下：

| 选项名称 | 数据类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | 'primary' \| 'success' \| 'danger' \| 'warning' | 'danger' | 通知类型 |
| message | string / number | - | 展示文案，支持通过 `\n` 换行 |
| color | string | - | 自定义字体颜色 |
| background | string | - | 自定义背景颜色 |
| duration | number | 3000 | 展示时长（ms），值为 0 时不自动关闭 |
| position | 'top' \| 'bottom' | 'top' | 弹出位置 |
| zIndex | number | 99 | z-index 层级 |
| safeHeight | number | - | 顶部安全高度 |
| onClick | (event: MouseEvent) => void | - | 点击通知时的回调函数 |
| onClosed | () => void | - | 通知完全关闭后的回调函数 |
| onOpened | () => void | - | 通知完全展示后的回调函数 |

### Events

以下为通过组件标签方式使用时的事件。`useNotify` API 方式通过配置对象中的 `onClick`、`onClosed`、`onOpened` 回调实现。

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| update:visible | value: boolean | 通知显隐状态变化时触发，用于 v-model 双向绑定 |
| click | event: MouseEvent | 点击通知时触发 |
| closed | - | 通知动画完全关闭后触发 |
| opened | - | 通知动画完全展示后触发 |

### Slots

| 插槽名 | 说明 | 子节点内容 |
| --- | --- | --- |
| default | 默认插槽，用于自定义通知内容（如图标 + 文字组合） | 任意内容，不传入时显示 `message` 属性内容 |

### Methods

组件未通过 `defineExpose` 暴露外部可调用的实例方法。所有操作均通过 `useNotify` API 完成。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-notify | Notify 根节点样式类 |
| wd-notify--primary | 主要类型修饰类 |
| wd-notify--success | 成功类型修饰类 |
| wd-notify--danger | 危险类型修饰类 |
| wd-notify--warning | 警告类型修饰类 |

### Notify 主题变量

组件提供以下 CSS 变量用于主题定制：

| 变量名 | 说明 | 默认值 |
| --- | --- | --- |
| --wot-notify-text-color | 通知文字颜色 | #ffffff（白色） |
| --wot-notify-padding | 通知内边距 | 8px 16px |
| --wot-notify-font-size | 通知字号 | 14px（$-fs-content） |
| --wot-notify-line-height | 通知行高 | 20px |
| --wot-notify-primary-background | 通知主要背景颜色 | $-color-theme（主题色） |
| --wot-notify-success-background | 通知成功背景颜色 | $-color-success（成功色） |
| --wot-notify-danger-background | 通知危险背景颜色 | $-color-danger（危险色） |
| --wot-notify-warning-background | 通知警告背景颜色 | $-color-warning（警告色） |

## 使用示例

### 示例 1：基础用法

效果说明：展示 Notify 最基础的调用方式。通过 `useNotify()` 获取实例后，调用 `showNotify()` 方法并传入字符串文案即可显示通知消息。文案默认在 3000ms 后自动消失。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="基础用法" is-link @click="showBasicNotify" />
  </wd-cell-group>
</template>

<script setup lang="ts">
import { useNotify } from '@/uni_modules/wot-ui-plus'

const { showNotify } = useNotify()

// 基础通知提示
function showBasicNotify() {
  showNotify('测试通知')
}
</script>
```

### 示例 2：不同类型的通知

效果说明：`useNotify` 支持四种预设通知类型，每种类型自动应用对应的背景色。`primary` 显示主题色背景，`success` 显示绿色背景，`danger` 显示红色背景，`warning` 显示橙色背景。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="主要通知" is-link @click="showType('primary')" />
    <wd-cell title="成功通知" is-link @click="showType('success')" />
    <wd-cell title="危险通知" is-link @click="showType('danger')" />
    <wd-cell title="警告通知" is-link @click="showType('warning')" />
  </wd-cell-group>
</template>

<script setup lang="ts">
import { useNotify } from '@/uni_modules/wot-ui-plus'
import type { NotifyType } from '@/uni_modules/wot-ui-plus/components/wd-notify/types'

const { showNotify } = useNotify()

function showType(type: NotifyType) {
  showNotify({
    message: '通知内容',
    type
  })
}
</script>
```

### 示例 3：自定义颜色和背景

效果说明：通过 `color` 和 `background` 属性自定义通知的字体颜色和背景颜色，实现个性化的视觉风格，适用于需要与品牌色或特定场景匹配的场景。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="自定义颜色" is-link @click="showCustomColor" />
  </wd-cell-group>
</template>

<script setup lang="ts">
import { useNotify } from '@/uni_modules/wot-ui-plus'

const { showNotify } = useNotify()

function showCustomColor() {
  showNotify({
    color: '#ad0000',
    message: '自定义颜色通知',
    background: '#ffe1e1'
  })
}
</script>
```

### 示例 4：自定义弹出位置

效果说明：通过 `position` 属性控制通知的弹出位置。支持 `top`（顶部，默认）和 `bottom`（底部）两种位置。顶部弹出时会自动适配安全区域高度。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="自定义位置" is-link @click="showCustomPosition" />
  </wd-cell-group>
</template>

<script setup lang="ts">
import { useNotify } from '@/uni_modules/wot-ui-plus'

const { showNotify } = useNotify()

function showCustomPosition() {
  showNotify({
    message: '自定义位置通知',
    position: 'bottom'
  })
}
</script>
```

### 示例 5：自定义展示时长

效果说明：通过 `duration` 属性控制通知的展示时长，单位为毫秒。默认值为 3000ms。设置为 0 时通知不会自动消失，需要手动调用 `closeNotify()` 方法关闭。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="自定义时长" is-link @click="showCustomDuration" />
  </wd-cell-group>
</template>

<script setup lang="ts">
import { useNotify } from '@/uni_modules/wot-ui-plus'

const { showNotify } = useNotify()

function showCustomDuration() {
  showNotify({
    message: '自定义时长通知',
    duration: 1000
  })
}
</script>
```

### 示例 6：使用 Notify 组件标签

效果说明：通过 `<wd-notify>` 组件标签在模板中使用，配合 `v-model:visible` 控制显隐状态。支持通过默认插槽自定义内容，如图标与文字组合展示。

```vue
<template>
  <wd-cell-group>
    <wd-cell title="使用 Notify 组件" is-link @click="showNotifyComponent" />
  </wd-cell-group>

  <wd-notify v-model:visible="visible" type="success">
    <wd-icon name="check-circle" size="inherit" color="inherit" />
    成功通知
  </wd-notify>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const visible = ref(false)
let timer: ReturnType<typeof setTimeout>

function showNotifyComponent() {
  visible.value = true
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => {
    visible.value = false
  }, 2000)
}
</script>
```

## 注意事项

1. **两种调用方式**：Notify 支持 `useNotify()` 命令式调用和 `<wd-notify>` 组件标签两种方式。推荐使用命令式调用，无需在模板中声明组件，调用即用。

2. **字符串与对象参数**：`showNotify` 方法支持传入纯字符串或配置对象。传入字符串时自动设置为 `message` 字段。

3. **自动关闭机制**：通知默认持续时长为 3000ms。当 `duration > 0` 时，组件会在指定毫秒数后自动关闭；当 `duration` 为 0 时，通知不会自动消失，需手动调用 `closeNotify()` 方法关闭。

4. **定时器管理**：组件内部使用单一变量存储定时器，同一实例的多次调用会先清除之前的定时器再重新计时，避免定时器冲突。

5. **多实例隔离**：通过 `useNotify(selector)` 传入不同的 `selector` 值可创建相互独立的 Notify 实例。每个实例拥有独立的状态，互不影响。若不传入 `selector`，则使用全局默认实例。

6. **位置与安全高度**：当 `position` 为 `top` 时，可通过 `safeHeight` 属性配置顶部安全高度，组件会自动计算 `top: calc(var(--window-top) + safeHeight)` 的偏移量，适配刘海屏等特殊屏幕。当 `position` 为 `bottom` 时，自动设置为 `bottom: var(--window-bottom)`。

7. **动画实现**：Notify 基于 `wd-popup` 组件实现，使用 250ms 的过渡动画。`opened` 回调在 `@enter` 事件时触发，`closed` 回调在 `@leave` 事件时触发。

8. **换行支持**：`message` 属性支持通过 `\n` 实现换行。组件内部设置了 `white-space: pre-wrap` 和 `word-wrap: break-word`，确保长文案和多行文本正确展示。

9. **插槽优先级**：当使用 `<wd-notify>` 组件标签并提供默认插槽内容时，插槽内容会覆盖 `message` 属性的展示。推荐通过插槽实现图标 + 文字等自定义内容组合。

10. **Root Portal 模式**：当遇到 fixed 定位失效问题（如被某些容器遮挡）时，可设置 `rootPortal: true` 将组件从当前页面结构中脱离出来。在不同平台会采用不同的实现方式：H5 使用 teleport，APP 使用 renderjs，小程序使用 root-portal。

11. **全局配置**：通过 `setNotifyDefaultOptions()` 可设置全局默认配置选项，通过 `resetNotifyDefaultOptions()` 可重置为初始值。这些配置会影响所有未显式指定配置的 Notify 实例。

12. **虚拟宿主配置**：组件配置了 `virtualHost: true`、`addGlobalClass: true` 和 `styleIsolation: 'shared'`，在小程序环境下可正确继承外部样式并支持全局样式穿透。

13. **自定义样式**：推荐使用 CSS 变量进行主题定制。也可通过外部样式类（如 `wd-notify--primary`、`wd-notify--success` 等）进行样式调整。
