---
name: "configProvider"
description: "`u-config-provider` 是 uView Pro 主题系统的唯一入口组件，负责把 `useTheme` 维护的 CSS 变量注入到页面，同时向外抛出主题与暗黑模式变更事件。本文档面向业务开发者，介绍其用法、属性与常见场景。. Invoke when user needs to use configProvider component."
url: "https://uviewpro.cn/zh/components/configProvider.html"
triggers: ["configProvider"]
---

# ConfigProvider 全局配置 <BadgeVersion text="0.4.1" /> <to-api/>

`u-config-provider` 是 uView Pro 主题系统的唯一入口组件，负责把 `useTheme` 维护的 CSS 变量注入到页面，同时向外抛出主题与暗黑模式变更事件。本文档面向业务开发者，介绍其用法、属性与常见场景。

## 监听主题切换

> 需要配合虚拟根组件(`uni-ku-root`) 来做全局共享

### 安装

::: code-group
```bash [npm]
npm i -D @uni-ku/root
```

```bash [yarn]
yarn add -D @uni-ku/root
```

```bash [pnpm]
pnpm add -D @uni-ku/root
```
:::

### 引入

- CLI项目: 直接编辑 根目录下的 vite.config.(js|ts)
- HBuilderX项目: 需要在根目录下 创建 vite.config.(js|ts)

```ts
// vite.config.(js|ts)

import { defineConfig } from 'vite'
import UniKuRoot from '@uni-ku/root'
import Uni from '@dcloudio/vite-plugin-uni'

export default defineConfig({
  plugins: [
    // ...plugins
    UniKuRoot(),
    Uni()
  ]
})
```

:::tip
若存在改变 pages.json 的插件，需要将 UniKuRoot 放置其后
:::

### 使用

1. 创建根组件并处理全局配置组件

- CLI项目: 在 **src** 目录下创建下 App.ku.vue
- HBuilderX项目: 在 **根** 目录下创建 App.ku.vue

:::tip
在 App.ku.vue 中标签 `<KuRootView />` 代表指定视图存放位置
:::

## 基本用法

```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
import { computed } from 'vue';

const { darkMode, themes, currentTheme } = useTheme();

const themeName = computed(() => currentTheme.value?.name);
</script>

<template>
  <u-config-provider :dark-mode="darkMode" :current-theme="themeName" :themes="themes">
    <KuRootView />
  </u-config-provider>
</template>
```
- 建议在应用的最外层（如 `App.ku.vue`）直接包裹整个视图，保证所有子组件都能拿到最新的 CSS 变量。
- `darkMode` 默认是 `Ref<'light' | 'dark' | 'auto'>`，直接透传即可；组件内部会依赖 `useTheme` 自动切换类名 `u-theme-light / u-theme-dark`。

## API

### Props
| Prop | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `themes` | `Theme[]` | `[]` | 可选。用于在运行时（如远程拉取主题）重新初始化主题列表，通常不需要手动传入。 |
| `currentTheme` | `string` | `''` | 可选。强制切换到指定主题名；当你希望父级受控时使用。 |
| `darkMode` | `'light' \| 'dark' \| 'auto'` | `'auto'` | 推荐配合 `useTheme().darkMode`，也可以手动传值。 |
| `customStyle` | `Record<string, any> \| string` | `{}` | 可选。追加到根节点上的样式，会与系统注入的 CSS 变量合并。 |
| `customClass` | `string` | `''` | 可选。自定义外层样式类名。 |

> 当 `themes` 已通过插件初始化后，`u-config-provider` 会跳过重复初始化，仅根据 props 调整当前主题/模式，因此可以安心地多次挂载（例如微前端场景）。

### Events

| 事件 | 回调参数 | 触发时机 |
| --- | --- | --- |
| `theme-change` | `(themeName: string)` | 全局主题被切换时（包括 `setTheme`、外部传入 `currentTheme`）。 |
| `mode-change` | `(mode: 'light' \| 'dark')` | 暗黑渲染状态变化时触发，`auto` 也会根据系统变化回调。 |

示例：
```vue
<u-config-provider
  @theme-change="name => console.log('主题切换到', name)"
  @mode-change="mode => console.log('渲染模式', mode)"
>
  <slot />
</u-config-provider>
```

## 常见场景
- **受控主题面板**：当你的设置页需要根据表单实时切换主题，可在父层直接修改 `currentTheme`，并监听 `theme-change` 做持久化。
- **多应用容器**：如果你的应用存在多个入口，可在每个入口都包裹一个 `u-config-provider`，无需担心初始化冲突。
- **局部覆写样式**：通过 `customStyle` / `customClass` 提供局部布局、背景覆写，同时依旧继承全局 CSS 变量。

## 最佳实践
- 始终通过 `useTheme` 获取 `darkMode` ref，保持单一数据源。
- 不要在业务组件里直接调用 `configProvider` 单例，`u-config-provider` + `useTheme` 已暴露全部能力。
- 若需要在页面层面自定义背景色、遮罩等，请使用 `$u-bg-color`、`rgba(var(--u-mask-color-rgb), .5)` 等变量，避免硬编码。

通过以上方式即可让 `u-config-provider` 在项目中稳定运行，确保主题/暗黑模式与应用保持同步。

