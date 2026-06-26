---
name: "install"
description: ":::tip 说明. Invoke when user needs to use install component."
url: "https://uviewpro.cn/zh/components/install.html"
triggers: ["install"]
---

# 安装

<demo-model url="/"></demo-model>

:::tip 说明

1. 由于 uView Pro 使用`easycom`模式，让您无需引入组件即可直接使用，但是此功能需要 Hbuilder X 2.5.5 及以上版本才支持，详见[配置自动引入组件](/zh/components/setting.html#_3-配置自动引入组件)。`easycom`打包的时候是**按需引入**的，您可以放心引入 uView Pro 的整个组件库，发布打包时会自动剔除您没有使用的组件(注意：调试时仍然是全部引入的)

2. 请确保您下载的[Hbuilder X](https://www.dcloud.io/hbuilderx.html)为`APP开发版`，而非`标准版`，并且在"工具-插件安装"中安装了"scss/sass 编译"插件

:::

:::tip 注意
sass、sass-loader 版本过高或过低，导致编译异常，因此推荐统一并锁定依赖版本：

```json
"sass": "1.63.2",
"sass-loader": "10.4.1"
```

:::

## 方式一：npm 安装

使用 npm 的方式安装，能更方便进行升级。

**注意：** 项目名称不能有**中文**字符。

如果您的项目是HX创建的，根目录又没有package.json文件的话，请先执行如下命令：

```bash
npm init -y
```
执行安装命令：
::: code-group

```bash [npm]
npm i uview-pro
```

```bash [yarn]
yarn add uview-pro
```

```bash [pnpm]
pnpm add uview-pro
```

:::

## 方式二：下载安装

通过 HBuilderX 插件市场或手动下载，将 uView Pro 放入 `uni_modules` 目录。

[插件市场：https://ext.dcloud.net.cn/plugin?id=24633](https://ext.dcloud.net.cn/plugin?id=24633)

使用下载的方式安装，能更方便阅读源码，但是每次升级都需要重新下载并覆盖 `uview-pro` 文件夹。

- 在 uni-app 插件市场右上角选择 `下载并导入HBuilder X`，会直接导入到项目 `src` 目录的 `uni_modules` 目录中。
- 如果您的项目是由 HBuilder X 创建的标准 uni-app 项目，将下载后的`uview-pro`文件夹，复制到项目`uni_modules`目录。
- 如果您的项目是由[vue-cli](https://uniapp.dcloud.io/quickstart?id=_2-%e9%80%9a%e8%bf%87vue-cli%e5%91%bd%e4%bb%a4%e8%a1%8c)模式创建的，请将下载后的`uview-pro`文件夹放到项目的`src`的 `uni_modules`文件夹中即可。

## 版本查询

- 通过源码查看的形式

可以查阅 uView Pro 的配置文件得知当前版本号，具体位置为 "/uview-pro/package.json" 中的 "version" 字段。

## 示例项目

此方式为整个 uView Pro 演示项目，里面有 uView Pro 核心，组件演示，模板等，建议用户可以下载
此项目运行用于查看 UI 演示效果，复制模板案例，通过里面的示例，可以快速掌握某一个组件的用法。

- 途径一：在 uni-app 插件市场右上角选择`使用 HBuilderX 导入示例项目`或者`下载示例项目ZIP`，然后在 HBuilder X 中运行即可。

  - 插件市场：[https://ext.dcloud.net.cn/plugin?id=24633](https://ext.dcloud.net.cn/plugin?id=24633)

- 途径二：通过 Github 或 Gitee 下载 uView Pro 示例项目，在 VSCode 中运行即可。
  - Github：[https://github.com/anyup/uview-pro](https://github.com/anyup/uview-pro)
  - Gitee：[https://gitee.com/anyup/uview-pro](https://gitee.com/anyup/uview-pro)

```bash

pnpm install

pnpm run dev:h5
```

:::tip 注意
演示项目不适用于直接开发中，它只是演示用的，可以直接运行并查看效果。  
如果在微信开发工具真机预览时，提示分包太大运行的问题，请在`HBuilder X`进行设置：菜单栏 运行 -> 运行到小程序模拟器，在下拉菜单中**勾选**"运行时是否压缩代码"
:::
