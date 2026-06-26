---
name: "customTheme"
description: ":::tip 说明. Invoke when user needs guidance on customTheme."
url: "https://uviewpro.cn/zh/guide/customTheme.html"
triggers: ["customTheme","自定义主题"]
---

# 多主题与暗黑模式 <BadgeVersion text="0.4.1" />

:::tip 说明
本文适用于 uView Pro 版本 0.4.1 及以上，支持单主题、多主题、暗黑模式等。
:::

本文面向 uView Pro 组件库使用者，帮助你在 Uni-app 项目中完整启用 uView Pro 的多主题与暗黑模式能力，重点围绕 `useTheme` 的 API 和最佳实践展开。

## 核心能力
- **一次性初始化**：在应用入口通过 `initTheme` 注入自定义主题，支持多套配置并自动生成暗黑色板。
- **响应式主题状态**：`useTheme` 暴露 `currentTheme`、`themes`、`darkMode`、`cssVars` 等 ref，可直接用于模板。
- **暗黑模式策略**：支持 `auto` 跟随系统、`light`、`dark` 三种模式，且可在运行时主动切换。
- **颜色获取**：CSS 场景使用 `$u-*` SCSS 变量，内联样式使用 `$u.color.xxx` 或 `useTheme().cssVars` / `useColor()` 返回值，确保实时响应。

## 生成主题

通过【[`主题配置工具ThemeGenerate`](/zh/guide/themeGenerate.html)】生成主题文件 `uview-pro.theme.ts`

- 生成后复制到 `src/uview-pro.theme.ts`，默认导出一个数组，每个元素描述一套主题：

```ts
export default [
  {
    name: 'midnight-black',
    label: '午夜黑',
    color: {
      primary: '#ff7a18',
      // ... 亮色色板
    },
    darkColor: {
      primaryLight: '#ffb066'
      // 留空的暗色会由系统智能生成
    }
  },
  // 其他主题...
];
```
- 只提供 `color` 也可以，缺失的 `darkColor` 会自动按规则补齐；若部分暗色需要自定义，只需在 `darkColor` 中填写对应键，其余仍会自动生成。

## 注册主题

### 基础使用

在 `unis.scss`中引入`uview-pro/theme.scss`

```scss
@import 'uview-pro/theme.scss';
```

在 `main.ts` 中注册 uView Pro

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import themes from '@/uview-pro.theme';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, { theme: themes }); // 只需传入一次
  return { app };
}
```
- `install` 内部会调用 `useTheme().initTheme`，无需手动再次初始化，确保主题数据全局唯一。

### 使用系统单主题

如果你是使用系统单主题，且需要修改主题色，可以进行如下配置：

:::tip 注意
仅使用系统单主题不可自定义暗黑色值的主题色
:::

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, {
      theme: {
          primary: '#000000',
          // ...
      }
  });
  return { app };
}
```

### 自定义单/多主题

如果你是多主题并在初始化时设置默认主题和暗黑模式，可以进行如下配置：

:::tip 注意
版本支持<BadgeVersion text="0.4.13" align="middle" />
:::

```ts
import { createSSRApp } from 'vue';
import App from './App.vue';
import themes from '@/uview-pro.theme';
import uViewPro from '@/uni_modules/uview-pro';

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro, {
      theme: {
          themes: themes,
          defaultTheme: 'purple', // 默认主题名称
          defaultDarkMode: 'auto' // 默认暗黑模式：auto、light、dark
      }
  });
  return { app };
}
```


## 监听主题切换

> 需要配合虚拟根组件([uni-ku-root](https://github.com/uni-ku/root)) 来做全局共享

如果你不想使用`uni-ku-root`虚拟根组件，也可以自己定义一个全局根组件，但是必须要使用 `u-config-provider` 组件来包裹内部所有页面！

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

在全局根组件包裹 `u-config-provider`

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
- `u-config-provider` 负责把 CSS 变量注入到页面，同时监听主题/模式切换事件，具体 API 见 [u-config-provider 文档](/zh/components/configProvider.html)。


## 在项目中使用

> 以上配置完成后需重新编译项目即可生效使用

在 scss 中使用：

```html
<style lang="scss" scoped>
	.title{
		color: $u-type-primary;
    /* 或使用 css 变量 */
    color: var(--u-type-primary);
	}
</style>

```

在 vue/ts 中使用：

```js
import { ref, onMounted } from 'vue';
import {$u} from 'uview-pro'
const color = ref('');

onMounted(() => {
  color.value = uni.$u.color['primary'];
  // 或
  color.value = $u.color['primary'];
});
```

## `useTheme` API

```ts
const {
  currentTheme, // Ref<Theme | null>
  themes,       // Ref<Theme[]>
  darkMode,     // Ref<'light' | 'dark' | 'auto'>
  cssVars,      // Ref<Record<string, string>>
  setTheme,
  getCurrentTheme,
  getAvailableThemes,
  initTheme,
  getDarkMode,
  setDarkMode,
  isInDarkMode,
  toggleDarkMode
} = useTheme();
```
- **currentTheme / themes**：直接在模板中使用，例如 `currentTheme?.name`、`themes.map(...)`。
- **cssVars**：包含诸如 `--u-type-primary`, `--u-bg-color` 等变量，可配合 `v-bind` 绑定到行内样式。
- **setTheme(name)**：切换到指定主题，内部会持久化到 `Storage`，下次启动自动恢复。
- **initTheme(list, defaultName?)**：大多数场景无需手动调用；只有当你在运行时动态获取主题列表时，需要显式调用一次。
- **getDarkMode / setDarkMode**：读写当前暗黑策略；`setDarkMode('auto')` 会立即跟随系统主题。
- **toggleDarkMode()**：在 `light` 与 `dark` 间快速切换，常用于快捷开关。
- **isInDarkMode()**：返回布尔值，表示当前是否处于暗黑渲染状态（`auto` 时会考虑系统设置）。

## 响应式颜色
- **SCSS / CSS**：继续使用 `$u-xxx` 变量，例如
```scss
.card {
  background-color: $u-bg-white;
  border-color: $u-border-color;
}
```
- **模板行内样式**：使用 `$u.color.xxx` 或 `useTheme().cssVars`
```vue
<view :style="{ color: $u.color.primary }">按钮</view>
<view :style="{ backgroundColor: `rgba(var(--u-type-primary-rgb), 0.15)` }" />
<view :style="{ backgroundColor: `var(--u-type-primary)` }" />
```
- **组合式 API**：`useColor()`（可选）提供 `getColor(name)`，在脚本逻辑中获取实时颜色值。

## 构建主题切换 UI 示例
```vue
<script setup lang="ts">
import { useTheme } from 'uview-pro';
const { themes, currentTheme, setTheme, darkMode, setDarkMode, toggleDarkMode } = useTheme();
</script>

<template>
  <picker :range="themes" range-key="label" @change="e => setTheme(themes[e.detail.value].name)">
    <view>当前主题：{{ currentTheme?.label }}</view>
  </picker>
  <u-switch :checked="darkMode === 'dark'" @change="toggleDarkMode" />
  <u-button @click="setDarkMode('auto')">跟随系统</u-button>
</template>
```

## 系统暗黑模式与持久化
- 首次进入应用时，如果 `darkMode` 设置为 `auto`，库会读取 `uni.getSystemInfoSync().theme` 并立即同步。
- 随后通过 `uni.onThemeChange`/`window.matchMedia` 监听系统变化，保持与系统一致。
- 主题、暗黑模式均存储在本地 Storage，实现跨页面、重启仍然生效。

## 常见问题
- **Q: 为什么动态写入 style 的颜色没有更新？**  
  A: 确保使用 `$u.color.xxx` 或 `useTheme().cssVars`，而不是硬编码十六进制。
- **Q: 只传入了一个主题对象是否可行？**  
  A: 可以。传递 `options.theme` 时会与默认主题合并，仍具备暗黑模式。
- **Q: 如何为特定主题手动定制暗黑色？**  
  A: 在 `darkColor` 中写入需要覆盖的键（例如 `primaryLight`），其余键仍由系统生成，保证一致性。

完成以上步骤即可获得统一、响应式、可扩展的主题与暗黑体验。若需更复杂的用例，可结合 `useTheme` 返回的 `cssVars` 做自定义动画或渐变效果。

<ArticleRecommend :articleLinks="['https://mp.weixin.qq.com/s/aH9IiLsHXaqSA9FyALhESg']" />
