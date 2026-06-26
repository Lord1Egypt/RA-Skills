---
name: "uniModulesSetting"
description: "uView Pro 提供了多种安装方式，本文将介绍如何使用 uni_modules 方式进行配置。. Invoke when user needs to use uniModulesSetting component in their uni-app project."
url: "https://uviewpro.cn/zh/components/uniModulesSetting.html"
---

# uni_modules 安装方式配置

uView Pro 提供了多种安装方式，本文将介绍如何使用 uni_modules 方式进行配置。

## 准备工作

在进行配置之前，请确保您已经根据[安装](/zh/components/install.html)中的步骤对 uView Pro 进行了下载安装，如果没有，请先下载安装。

## 配置步骤

### 1. 引入 uView 主库

在项目根目录中的`main.ts`中，引入并使用 uView Pro 的工具库，注意这两行要放在`import Vue`之后。

```js
// main.ts
import { createSSRApp } from "vue";
import uViewPro from "@/uni_modules/uview-pro";

export function createApp() {
  const app = createSSRApp(App);
  app.use(uViewPro);
  // 其他配置
  return {
    app,
  };
}
```

### 2. 在引入 uView Pro 的全局 SCSS 主题文件

在项目根目录的`uni.scss`中引入此文件。

```css
/* uni.scss */
@import "@/uni_modules/uview-pro/theme.scss";
```

### 3. 引入 uView Pro 基础样式

:::danger 注意！
在`App.vue`中**首行**的位置引入，注意给 style 标签加入 lang="scss"属性
:::

```css
<style lang="scss">
	/* 注意要写在第一行，同时给style标签加入lang="scss"属性 */
	@import "@/uni_modules/uview-pro/index.scss";
</style>
```

## 3. 配置自动引入组件

### 基于 easycom 配置自动引入组件<el-tag type="primary" style="vertical-align: middle;margin-left:8px;" effect="dark" >方案 1</el-tag>

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
    }
  },
  "pages": [
    // ...
  ]
}
```

:::tip 注意

- 1.修改 `easycom` 规则后需重启 HX 或重新编译项目。
- 2.请确保 `pages.json` 中只有一个 easycom 字段，否则请自行合并多个规则。
- 3.一定要放在 `custom` 内，否则无效。
  :::

### 基于 vite 配置自动引入组件<el-tag type="primary" style="vertical-align: middle;margin-left:8px;" effect="dark" >方案 2</el-tag>

如果不熟悉 `easycom`，也可以通过 [@uni-helper/vite-plugin-uni-components](https://github.com/uni-helper/vite-plugin-uni-components) 实现组件的自动引入。

:::tip 提醒

- 推荐使用 `@uni-helper/vite-plugin-uni-components@0.2.1` 及以上版本，因为在 0.2.1 版本开始其内置了 `uView Pro` 的`resolver`。
- 如果使用此方案时控制台打印很多 `Sourcemap for  points to missing source files​` ，可以尝试将 `Vite` 版本升级至 `4.5.x` 以上版本。

:::

::: code-group

```bash [npm]
npm i @uni-helper/vite-plugin-uni-components -D
```

```bash [yarn]
yarn add @uni-helper/vite-plugin-uni-components -D
```

```bash [pnpm]
pnpm add @uni-helper/vite-plugin-uni-components -D
```

:::

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'

import Components from '@uni-helper/vite-plugin-uni-components'
import { uViewProResolver } from '@uni-helper/vite-plugin-uni-components/resolvers'

export default defineConfig({
  plugins: [
    // make sure put it before `Uni()`
    Components({
      resolvers: [uViewProResolver()]
    }),
    uni()
  ]
})
```

如果你使用 `pnpm` ，请在根目录下创建一个 `.npmrc` 文件，参见 [Issue](https://github.com/antfu/unplugin-vue-components/issues/389)。

```text
// .npmrc
public-hoist-pattern[]=@vue*
// or
// shamefully-hoist = true
```

