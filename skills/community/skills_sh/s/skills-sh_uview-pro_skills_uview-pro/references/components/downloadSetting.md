---
name: "downloadSetting"
description: "uView Pro 依赖 SCSS，您必须要安装此插件，否则无法正常运行。. Invoke when user needs to use downloadSetting component in their uni-app project."
url: "https://uviewpro.cn/zh/components/downloadSetting.html"
---

# 下载安装方式配置

## 关于 SCSS

## 关于 SCSS

uView Pro 依赖 SCSS，您必须要安装此插件，否则无法正常运行。

- 如果您的项目是由`HBuilder X`创建的，相信已经安装 scss 插件，如果没有，请在 HX 菜单的 工具->插件安装中找到"scss/sass 编译"插件进行安装，
  如不生效，重启 HX 即可
- 如果您的项目是由 vue-cli 创建的，请通过以下命令安装对 sass(scss)的支持，如果已安装，请略过。

```bash
# 安装sass
npm i sass -D

# 安装sass-loader
npm i sass-loader -D
```

:::tip 注意
sass、sass-loader 版本过高或过低，导致编译异常，因此推荐统一并锁定依赖版本：

```json
"sass": "1.63.2",
"sass-loader": "10.4.1"
```
:::

## 准备工作

在进行配置之前，请确保您已经根据[安装](install.html)中的步骤对 uView Pro 进行了下载安装，如果没有，请先下载安装。

## 1. 引入 uView Pro 主库

在 `main.ts` 中引入并注册 uView Pro：

```js
// main.ts
import { createSSRApp } from 'vue'
// uni_modules 方式
import uViewPro from '@/uni_modules/uview-pro'

export function createApp() {
  const app = createSSRApp(App)
  app.use(uViewPro)
  return {
    app
  }
}
```

## 2. 引入全局样式

在 `uni.scss` 中引入主题样式：

```scss
// uni_modules 方式
@import '@/uni_modules/uview-pro/theme.scss';
```

在 `App.vue` 首行引入基础样式：

```scss
<style lang="scss">
  // uni_modules 方式
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
      // uni_modules 方式
      "^u-(.*)": "@/uni_modules/uview-pro/components/u-$1/u-$1.vue"
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

## 4. Volar 类型提示支持

如需在 CLI 项目中获得 Volar 的全局类型提示，请在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    // uni_modules 方式
    "types": ["@/uni_modules/uview-pro/types"]
  }
}
```

> HBuilderX 项目暂不支持 tsconfig.json 的 types 配置，CLI 项目推荐配置以获得最佳 TS 体验。

## 5. 组件使用

配置完成后，无需 import 和 components 注册，可直接在 SFC 中使用 uView Pro 组件：

```vue
<template>
  <u-button type="primary">按钮</u-button>
</template>
```
