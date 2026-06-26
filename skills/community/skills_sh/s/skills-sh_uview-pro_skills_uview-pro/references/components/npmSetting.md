---
name: "npmSetting"
description: "uView Pro 依赖 SCSS，您必须要安装此插件，否则无法正常运行。. Invoke when user needs to use npmSetting component."
url: "https://uviewpro.cn/zh/components/npmSetting.html"
triggers: ["npmSetting"]
---

# npm 安装方式配置

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

在进行配置之前，请确保您已经根据[安装](install.html)中的步骤对 uView Pro 进行了 npm 安装，如果没有，请先执行安装：

## 1. 引入 uView Pro 主库

在 `main.ts` 中引入并注册 uView Pro：

```js
// main.ts
import { createSSRApp } from 'vue'
// npm 方式
import uViewPro from 'uview-pro'

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
/* uni.scss */
// npm 方式
@import 'uview-pro/theme.scss';
```

在 `App.vue` 首行引入基础样式：

```scss
<style lang="scss">
  // npm 方式
  @import "uview-pro/index.scss";
</style>
```

## 3. 配置 easycom 自动引入组件

在 `pages.json` 中配置 easycom 规则，实现组件自动引入：

```json
// pages.json
{
  "easycom": {
    "autoscan": true,
    "custom": {
      // npm 方式
      "^u-(.*)": "uview-pro/components/u-$1/u-$1.vue"
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

## 4. Volar 类型提示支持

如需在 CLI 项目中获得 Volar 的全局类型提示，请在 `tsconfig.json` 中添加：

```json
{
  "compilerOptions": {
    // npm 方式
    "types": ["uview-pro/types"]
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
