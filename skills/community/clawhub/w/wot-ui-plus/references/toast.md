# Toast 消息提示



## 组件概况

Toast 消息提示组件是一个轻量级的即时反馈提示组件，用于在用户操作后向用户展示简短的提示信息。该组件支持多种消息类型（成功、错误、警告、常规、加载），可配置图标、位置、布局方向、遮罩层等选项，并通过 `useToast` 组合式 API 实现命令式调用。

组件内部基于 `wd-overlay`（遮罩层）和 `wd-transition`（过渡动画）实现，采用 fade 淡入淡出的过渡动画，支持通过选择器（selector）区分多个 Toast 实例，避免状态冲突。内置 SVG 图标（成功、错误、警告、常规），无需额外引入图标资源。

## 核心功能描述

- **多种消息类型**：通过 `useToast()` 提供的 `show`、`success`、`error`、`warning`、`info`、`loading` 方法，可快速调用不同类型的提示消息，每种类型自带对应图标和默认配置
- **命令式调用**：采用 `useToast` 组合式 API 进行命令式调用，无需在模板中声明组件，调用即用
- **自动关闭**：消息默认在指定时长后自动关闭（`duration`），loading 类型默认不自动关闭（`duration: 0`），需手动调用 `close()` 方法关闭
- **位置控制**：支持四种显示位置：顶部（`top`）、中上（`middle-top`，默认）、居中（`middle`）、底部（`bottom`）
- **布局方向**：支持横向（`horizontal`，默认）和纵向（`vertical`）排列，适用于长文案场景
- **自定义图标**：支持通过 `iconClass` 和 `classPrefix` 使用组件库内置图标或项目自定义图标
- **加载状态**：内置 loading 类型提示，支持 `outline`（轮廓）和 `ring`（环形）两种加载动画，可自定义颜色和尺寸
- **遮罩层支持**：通过 `cover` 属性开启遮罩层，阻止用户操作底层内容（loading 类型默认开启）
- **生命周期回调**：提供 `opened`（完全展示后）和 `closed`（完全关闭后）回调函数，便于执行后续操作
- **多实例支持**：通过 `selector` 参数创建独立的 Toast 实例，不同实例之间互不干扰

## 适用业务场景

- **操作反馈**：用户执行保存、删除、提交等操作后展示成功或失败提示
- **表单验证**：表单校验失败时展示错误提示信息
- **加载状态**：异步请求过程中展示 loading 加载提示，请求结束后关闭
- **网络异常**：网络断开或请求超时时展示错误提示
- **操作引导**：在新手引导或功能提示中展示常规信息提示
- **权限提醒**：用户无权限执行某操作时展示警告提示
- **长文本提示**：使用纵向布局展示较长的提示文案

## API

### Props

以下为通过组件标签方式使用时的 Props。若使用 `useToast` API 调用，可通过 `ToastOptions` 对象传入同名配置项。

| 属性名称 | 数据类型 | 默认值 | 是否必填 | 说明 |
| --- | --- | --- | --- | --- |
| selector | string | '' | 否 | 选择器，用于区分多个 Toast 实例 |
| msg | string | '' | 否 | 提示文案内容 |
| direction | 'vertical' \| 'horizontal' | 'horizontal' | 否 | 内容排列方向，`vertical` 为纵向，`horizontal` 为横向 |
| iconName | 'success' \| 'error' \| 'warning' \| 'loading' \| 'info' | '' | 否 | 内置图标名称，优先级高于 `iconClass` |
| iconSize | number | - | 否 | 图标大小，支持数字（默认单位 px） |
| loadingType | 'outline' \| 'ring' | 'outline' | 否 | 加载动画类型 |
| loadingColor | string | '#4D80F0' | 否 | 加载动画颜色 |
| loadingSize | number | - | 否 | 加载动画大小 |
| iconColor | string | - | 否 | 图标颜色 |
| position | 'top' \| 'middle-top' \| 'middle' \| 'bottom' | 'middle-top' | 否 | 提示框显示位置 |
| zIndex | number | 100 | 否 | 层级堆叠顺序，值越大越靠前 |
| cover | boolean | false | 否 | 是否存在遮罩层，开启后阻止用户操作底层内容 |
| iconClass | string | '' | 否 | 图标类名，用于使用组件库内置图标或自定义图标 |
| classPrefix | string | 'wd-icon' | 否 | 图标类名前缀，用于自定义图标时指定前缀 |
| customStyle | string | '' | 否 | 自定义组件根元素样式 |
| customClass | string | '' | 否 | 自定义组件根元素类名 |

### useToast API

`useToast` 是 Toast 组件的核心调用方式，通过组合式 API 返回一个包含多个方法的对象。

```ts
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()
```

也可传入 `selector` 参数创建指定实例：

```ts
const toast = useToast('#my-toast')
```

返回的 `toast` 对象包含以下方法：

| 方法名称 | 参数 | 返回值 | 说明 |
| --- | --- | --- | --- |
| show | `toastOptions: ToastOptions \| string` | void | 打开 Toast 提示，支持传入配置对象或纯字符串文案 |
| success | `toastOptions: ToastOptions \| string` | void | 成功提示，自动设置 `iconName` 为 `'success'`，默认持续 1500ms |
| error | `toastOptions: ToastOptions \| string` | void | 错误提示，自动设置 `iconName` 为 `'error'`，使用默认持续时长 |
| info | `toastOptions: ToastOptions \| string` | void | 常规提示，自动设置 `iconName` 为 `'info'`，使用默认持续时长 |
| warning | `toastOptions: ToastOptions \| string` | void | 警告提示，自动设置 `iconName` 为 `'warning'`，使用默认持续时长 |
| loading | `toastOptions: ToastOptions \| string` | void | 加载提示，自动设置 `iconName` 为 `'loading'`、`cover` 为 `true`、`duration` 为 `0`（不自动关闭） |
| close | - | void | 关闭当前 Toast 提示，清除自动关闭定时器并隐藏组件 |

### ToastOptions

通过 `useToast` API 调用时，可传入的 `ToastOptions` 对象结构如下：

| 选项名称 | 数据类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| msg | string | - | 提示文案内容 |
| duration | number | 2000 | 自动关闭时长，单位为毫秒；设为 `0` 时不自动关闭 |
| direction | 'vertical' \| 'horizontal' | - | 内容排列方向 |
| iconName | 'success' \| 'error' \| 'warning' \| 'loading' \| 'info' | - | 内置图标名称 |
| iconSize | number | - | 图标大小 |
| loadingType | 'outline' \| 'ring' | - | 加载动画类型 |
| loadingColor | string | - | 加载动画颜色 |
| loadingSize | number | - | 加载动画大小 |
| iconColor | string | - | 图标颜色 |
| position | 'top' \| 'middle-top' \| 'middle' \| 'bottom' | - | 提示框显示位置 |
| cover | boolean | false | 是否存在遮罩层 |
| iconClass | string | - | 图标类名 |
| classPrefix | string | - | 图标类名前缀 |
| opened | () => void | - | 完全展示后的回调函数 |
| closed | () => void | - | 完全关闭时的回调函数 |

### Events

以下为通过组件标签方式使用时的事件。`useToast` API 方式通过 `ToastOptions` 中的 `opened` 和 `closed` 回调实现。

| 事件名称 | 回调参数 | 触发时机 |
| --- | --- | --- |
| opened | - | Toast 动画完全展示后触发 |
| closed | - | Toast 动画完全关闭后触发 |

### Slots

当前组件未定义插槽。

### Methods

当前组件未通过 `defineExpose` 暴露实例方法。所有操作均通过 `useToast` API 完成。

### 外部样式类

| 类名 | 说明 |
| --- | --- |
| wd-toast | Toast 根节点样式类 |
| wd-toast--top | 顶部位置修饰类 |
| wd-toast--middle-top | 中上位置修饰类 |
| wd-toast--middle | 居中位置修饰类 |
| wd-toast--bottom | 底部位置修饰类 |
| wd-toast--with-icon | 带图标时的修饰类 |
| wd-toast--loading | 纯 loading 状态修饰类 |
| wd-toast__icon | 图标样式类 |
| wd-toast__iconWrap | 图标容器样式类 |
| wd-toast__iconBox | 图标盒子样式类 |
| wd-toast__iconSvg | 图标 SVG 样式类 |
| wd-toast__msg | 消息文本样式类 |

## 使用示例

### 示例 1：基础用法

效果说明：展示 Toast 最基础的调用方式。通过 `useToast()` 获取实例后，调用 `show()` 方法并传入字符串文案即可显示提示消息。文案默认在 2000ms 后自动消失。也可直接调用 `success()`、`error()` 等方法展示对应类型的提示。

```vue
<template>
  <wd-button @click="showToast">显示提示</wd-button>
  <wd-button @click="showLongToast">长文案提示</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 基础提示
function showToast() {
  toast.show('提示信息')
}

// 长文案提示（自动换行适配）
function showLongToast() {
  toast.show('这是一段很长很长很长很长很长很长很长很长很长很长的文案')
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

### 示例 2：不同类型提示

效果说明：`useToast` 提供了多种类型的快捷方法，每种类型自动携带对应的内置 SVG 图标。`success` 显示绿色成功图标，`error` 显示红色错误图标，`warning` 显示橙色警告图标，`info` 显示灰色信息图标。不同类型有不同的默认展示时长。

```vue
<template>
  <wd-button @click="showSuccessToast">成功提示</wd-button>
  <wd-button @click="showErrorToast">错误提示</wd-button>
  <wd-button @click="showWarnToast">警告提示</wd-button>
  <wd-button @click="showNormalToast">常规提示</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 成功提示（自动携带成功图标，持续 1500ms）
function showSuccessToast() {
  toast.success('操作成功')
}

// 错误提示（自动携带错误图标）
function showErrorToast() {
  toast.error('错误提示')
}

// 警告提示（自动携带警告图标）
function showWarnToast() {
  toast.warning('提示信息')
}

// 常规提示（自动携带信息图标）
function showNormalToast() {
  toast.info('常规提示')
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

### 示例 3：Loading 加载提示

效果说明：Loading 类型提示默认不自动关闭（`duration: 0`），且默认开启遮罩层（`cover: true`），适用于异步请求等需要手动控制关闭时机的场景。支持两种加载动画类型（`outline` 轮廓和 `ring` 环形），并可自定义加载颜色和尺寸。关闭时需显式调用 `toast.close()` 方法。

```vue
<template>
  <wd-button @click="showLoadingToast">Loading 加载</wd-button>
  <wd-button @click="showLoadingToast2">ring 类型 loading</wd-button>
  <wd-button @click="showLoadingToast3">纵向布局 loading</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 基础 loading（outline 类型，3 秒后手动关闭）
function showLoadingToast() {
  toast.loading('加载中...')
  setTimeout(() => {
    toast.close()
  }, 3000)
}

// ring 类型 loading，自定义颜色
function showLoadingToast2() {
  toast.loading({
    msg: '加载中...',
    loadingType: 'ring',
    loadingColor: '#fff'
  })
  setTimeout(() => {
    toast.close()
  }, 3000)
}

// 纵向布局 loading，适用于长文案
function showLoadingToast3() {
  toast.loading({
    msg: '正在处理，请稍候...',
    direction: 'vertical'
  })
  setTimeout(() => {
    toast.close()
  }, 3000)
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

### 示例 4：自定义提示位置

效果说明：通过 `position` 属性控制 Toast 的显示位置。支持 `top`（顶部）、`middle-top`（中上，默认）、`middle`（居中）、`bottom`（底部）四种位置。同时可以配置图标、回调函数等完整选项。

```vue
<template>
  <wd-button @click="showTopToast">顶部提示</wd-button>
  <wd-button @click="showMiddleToast">居中提示</wd-button>
  <wd-button @click="showBottomToast">底部提示</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 顶部提示
function showTopToast() {
  toast.show({
    position: 'top',
    iconClass: 'star',
    msg: '顶部提示信息',
    opened() {
      console.log('Toast 已完全展示')
    },
    closed() {
      console.log('Toast 已完全关闭')
    }
  })
}

// 居中提示
function showMiddleToast() {
  toast.show({
    position: 'middle',
    iconClass: 'star',
    msg: '居中提示信息',
    opened() {
      console.log('Toast 已完全展示')
    },
    closed() {
      console.log('Toast 已完全关闭')
    }
  })
}

// 底部提示
function showBottomToast() {
  toast.show({
    position: 'bottom',
    msg: '底部提示信息'
  })
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

### 示例 5：使用自定义图标

效果说明：通过 `iconClass` 和 `classPrefix` 属性使用自定义图标。当 `iconClass` 传入图标名称时，组件会查找对应类名的图标。`classPrefix` 默认为 `'wd-icon'`，可自定义为项目图标库的前缀。注意 `iconName` 的优先级高于 `iconClass`，若同时设置 `iconName` 则会使用内置 SVG 图标。

```vue
<template>
  <wd-button @click="showInnerIconToast">使用内置图标库图标</wd-button>
  <wd-button @click="showCustomIconToast">使用自定义图标</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 使用组件库内置图标（如 star 图标）
function showInnerIconToast() {
  toast.show({
    iconClass: 'star',
    msg: '使用组件库内部图标'
  })
}

// 使用项目自定义图标（自定义类名前缀）
function showCustomIconToast() {
  toast.show({
    iconClass: 'kehuishouwu',
    classPrefix: 'fish',
    msg: '使用自定义图标'
  })
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

### 示例 6：排版方向

效果说明：通过 `direction` 属性控制 Toast 内部内容的排列方向。`horizontal`（默认）为图标和文案水平排列，`vertical` 为图标和文案垂直排列。垂直排版适用于较长文案的场景，可使图标居上、文字居下展示。

```vue
<template>
  <wd-button @click="showHorizonToast">横向排版</wd-button>
  <wd-button @click="showVerticalToast">纵向排版</wd-button>
</template>

<script setup lang="ts">
import { useToast } from '@/uni_modules/wot-ui-plus'

const toast = useToast()

// 横向排版（默认）
function showHorizonToast() {
  toast.success('横向排版')
}

// 纵向排版，图标在上方，文字在下方
function showVerticalToast() {
  toast.success({
    msg: '芦叶满汀洲，寒沙带浅流。二十年重过南楼。柳下系船犹未稳，能几日，又中秋。黄鹤断矶头，故人曾到否？旧江山浑是新愁。欲买桂花同载酒，终不似，少年游。',
    direction: 'vertical'
  })
}
</script>

<style scoped lang="scss">
button {
  margin: 0 10px 10px 0;
}
</style>
```

## 注意事项

1. **useToast 调用方式**：Toast 推荐使用 `useToast()` 组合式 API 进行调用，无需在模板中声明 `<wd-toast>` 组件。调用 `useToast()` 后返回的对象包含 `show`、`success`、`error`、`warning`、`info`、`loading`、`close` 方法。

2. **字符串与对象参数**：`show`、`success`、`error`、`warning`、`info`、`loading` 方法均支持传入纯字符串或 `ToastOptions` 对象。传入字符串时自动设置为 `msg` 字段。

3. **自动关闭机制**：Toast 默认持续时长为 2000ms，`success` 类型默认 1500ms。`loading` 类型默认 `duration: 0`，不会自动关闭，需手动调用 `close()` 方法。当 `duration > 0` 时，组件会在指定毫秒数后自动关闭。

4. **定时器管理**：组件内部使用 `Map` 结构（`toastTimerMap`）存储定时器，按 `selector` 区分。同一 `selector` 的多次调用会先清除之前的定时器再重新计时，避免定时器冲突。

5. **图标优先级**：内置图标（通过 `iconName`）的优先级高于自定义图标（通过 `iconClass`）。当同时设置 `iconName` 和 `iconClass` 时，将显示 `iconName` 指定的内置 SVG 图标。

6. **多实例隔离**：通过 `useToast(selector)` 传入不同的 `selector` 值可创建相互独立的 Toast 实例。每个实例拥有独立的状态和定时器，互不影响。若不传入 `selector`，则使用全局默认实例。

7. **遮罩层行为**：`cover` 属性开启后会渲染一个透明的 `wd-overlay` 遮罩层，设置 `pointer-events: auto` 阻止用户点击穿透底层内容。`loading` 类型默认开启遮罩层。

8. **动画实现**：Toast 使用 `wd-transition` 组件实现 `fade` 淡入淡出动画。`opened` 回调在 `@after-enter` 事件时触发，`closed` 回调在 `@after-leave` 事件时触发。

9. **虚拟宿主配置**：组件配置了 `virtualHost: true`、`addGlobalClass: true` 和 `styleIsolation: 'shared'`，在小程序环境下可正确继承外部样式并支持全局样式穿透。

10. **自定义样式**：推荐使用 `custom-class` 和 `custom-style` 属性进行样式定制。也可通过外部样式类（如 `wd-toast__msg`、`wd-toast__icon` 等）进行精细化样式调整。
