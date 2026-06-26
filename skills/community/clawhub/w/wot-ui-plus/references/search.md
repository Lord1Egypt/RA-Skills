# Search 搜索框


## 组件概述

搜索框是用于用户输入搜索关键词的核心输入组件。组件内置搜索图标、输入框、清除按钮以及可选的取消按钮，支持占位符配置、禁用状态、自动聚焦等丰富功能，适用于各类搜索场景。

## 核心功能

- **双向绑定**：通过 `v-model` 实现搜索值的双向绑定
- **搜索图标**：内置搜索图标，支持占位符模式和左侧显示模式
- **快捷清除**：输入内容后显示清除图标，一键清空输入
- **取消操作**：右侧可显示取消按钮，支持自定义文案和插槽
- **主题切换**：支持默认深色和亮色（白色）两种主题风格
- **自动聚焦**：支持初始化自动聚焦和清除后自动聚焦
- **前缀扩展**：支持通过 `prefix` 插槽在左侧插入自定义内容（如搜索类型选择器）
- **国际化**：内置多语言支持，占位符和取消按钮文本自动适配

## 适用业务场景

- 商品/订单/内容搜索入口
- 通讯录、消息列表快速查找
- 配合下拉菜单实现多维度搜索（如搜索类型切换）
- 导航栏集成搜索功能

## API

### Props

| 参数 | 说明 | 类型 | 可选值 | 默认值 | 最低版本 |
|------|------|------|--------|--------|----------|
| model-value / v-model | 绑定值 | string | - | '' | - |
| placeholder | 占位文本 | string | - | 国际化默认文案 | - |
| cancel-txt | 取消按钮文案 | string | - | 国际化默认文案 | - |
| light | 是否使用亮色（白色）主题 | boolean | - | false | - |
| hide-cancel | 是否隐藏取消按钮 | boolean | - | false | - |
| disabled | 是否禁用 | boolean | - | false | - |
| maxlength | 输入最大字符数 | number \| string | - | -1 | - |
| placeholder-left | 占位符是否靠左显示 | boolean | - | false | - |
| focus | 是否自动聚焦 | boolean | - | false | 0.1.63 |
| focus-when-clear | 清除时是否自动聚焦 | boolean | - | false | 0.1.63 |
| placeholder-style | 原生属性，指定 placeholder 的样式（仅支持 color、font-size、font-weight） | string | - | - | - |
| placeholder-class | 原生属性，指定 placeholder 的样式类 | string | - | '' | - |
| custom-input-class | 自定义输入框 class | string | - | '' | - |
| custom-style | 自定义根节点样式 | string | - | '' | - |
| custom-class | 自定义根节点样式类 | string | - | '' | - |

### Events

| 事件名称 | 说明 | 参数 |
|----------|------|------|
| change | 输入值变化时触发 | `{ value: string }` 当前输入值 |
| search | 点击确认/搜索按钮时触发 | `{ value: string }` 当前输入值 |
| clear | 点击清除按钮时触发 | - |
| focus | 输入框聚焦时触发 | `{ value: string }` 当前输入值 |
| blur | 输入框失焦时触发 | `{ value: string }` 当前输入值 |
| cancel | 点击取消按钮时触发 | `{ value: string }` 当前输入值 |
| click | 点击搜索框区域时触发（仅在 disabled 状态下生效） | - |

### Slots

| 插槽名称 | 说明 |
|----------|------|
| prefix | 前缀插槽，位于搜索图标左侧，常用于放置搜索类型选择器等自定义内容 |
| suffix | 后缀插槽，替代默认取消按钮，需配合 `hide-cancel=false` 使用 |

## 使用示例

### 示例一：基础搜索框

最基本的搜索框用法，隐藏取消按钮，禁用清除功能。

```vue
<template>
  <wd-search
    v-model="value1"
    hide-cancel
    :clearabled="false"
    @search="handleSearch"
    @change="handleChange"
    @cancel="handleCancel"
    @clear="handleClear"
  />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value1 = ref<string>('')

function handleSearch(e: any) {
  uni.showToast({ title: '搜索: ' + e.value })
}

function handleChange(e: any) {
  console.log('输入变化:', e.value)
}

function handleCancel() {
  uni.showToast({ title: '取消' })
}

function handleClear() {
  uni.showToast({ title: '已清空' })
}
</script>
```

### 示例二：亮色主题搜索框

使用 `light` 属性开启白色输入框样式，适合浅色背景场景。自定义取消按钮文案。

```vue
<template>
  <wd-search light cancel-txt="搜索" placeholder="请输入关键词" />
</template>

<script lang="ts" setup>
// 无需额外逻辑，组件内部管理状态
</script>
```

### 示例三：占位符靠左

通过 `placeholder-left` 属性使搜索图标和占位符靠左对齐显示。

```vue
<template>
  <wd-search placeholder-left placeholder="请输入搜索内容" />
</template>

<script lang="ts" setup>
// 无需额外逻辑
</script>
```

### 示例四：自定义前缀插槽

在前缀插槽中嵌入搜索类型选择器，支持多维度搜索切换。

```vue
<template>
  <wd-search v-model="searchValue">
    <template #prefix>
      <wd-popover mode="menu" :content="menuList" @menuclick="changeSearchType">
        <view class="search-type">
          <text>{{ currentSearchType }}</text>
          <wd-icon class="icon-arrow" name="down-box-filled" />
        </view>
      </wd-popover>
    </template>
  </wd-search>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'

const searchValue = ref<string>('')
const currentSearchType = ref<string>('全部')

const menuList = computed(() => {
  return [
    { content: '全部' },
    { content: '订单号' },
    { content: '退款单号' }
  ]
})

function changeSearchType({ item, index }: any) {
  currentSearchType.value = item.content
}
</script>

<style lang="scss" scoped>
.search-type {
  position: relative;
  height: 30px;
  line-height: 30px;
  padding: 0 8px 0 16px;
  color: rgba(0, 0, 0, 0.45);
}

.search-type::after {
  position: absolute;
  content: '';
  width: 1px;
  right: 0;
  top: 5px;
  bottom: 5px;
  background: rgba(0, 0, 0, 0.25);
  transform: scaleX(0.5);
}

.search-type .icon-arrow {
  margin-left: 4px;
  display: inline-block;
  font-size: 18px;
  vertical-align: middle;
  color: rgba(0, 0, 0, 0.65);
}
</style>
```

### 示例五：清除后自动聚焦

清除输入内容后自动聚焦到输入框，方便用户快速重新输入。

```vue
<template>
  <wd-search v-model="value" focus-when-clear />
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const value = ref<string>('')
</script>
```

### 示例六：禁用状态

禁用搜索框交互，点击时可通过 `click` 事件进行提示。

```vue
<template>
  <wd-search disabled hide-cancel @click="handleDisabledClick" />
</template>

<script lang="ts" setup>
function handleDisabledClick() {
  uni.showToast({ title: '搜索框已禁用' })
}
</script>
```

## 注意事项

1. **聚焦机制**：组件内部使用 `showInput` 和 `isFocused` 两个响应式变量配合异步延迟实现聚焦效果。当 `focus` 为 true 或用户点击搜索框时，会先隐藏占位覆盖层，再延迟设置输入框显示和聚焦状态。

2. **清除逻辑**：清除操作会触发表达式重新计算，如果开启 `focus-when-clear`，会在清除后重新聚焦输入框。组件内部使用 `clearing` 标记位避免 blur 事件与清除操作冲突。

3. **Blur 延迟处理**：`handleBlur` 方法中使用了 150ms 延迟等待清除操作完成，防止清除和失焦同时触发导致状态异常。

4. **占位覆盖层**：当未启用 `placeholder-left` 时，组件使用一个覆盖层（`wd-search__cover`）展示搜索图标和占位文本，点击后才会显示真实输入框。这是一种优化首屏渲染和交互体验的设计。

5. **disabled 状态点击**：当搜索框被禁用时，点击搜索框区域会触发 `click` 事件，可用于向用户展示禁用原因的提示。

6. **国际化支持**：组件通过 `useTranslate` composable 实现国际化，占位符和取消按钮文案在未传入时会使用翻译函数获取默认值。

7. **输入确认类型**：输入框的 `confirm-type` 固定为 `search`，确保软键盘回车键显示为搜索图标。

8. **废弃属性**：`useSuffixSlot` 属性已被标记为 `@deprecated`，将在下一个 minor 版本中移除，请直接使用 `suffix` 插槽。

9. **自定义样式**：可通过 `custom-input-class` 单独定制输入框样式，通过 `custom-style` 和 `custom-class` 定制根节点样式。

10. **虚拟主机**：组件启用了 `virtualHost: true`，在小程序环境中样式穿透需要注意使用 `addGlobalClass: true` 和 `styleIsolation: 'shared'` 配置。
