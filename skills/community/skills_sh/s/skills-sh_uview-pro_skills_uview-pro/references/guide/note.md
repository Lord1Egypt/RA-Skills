---
name: "note"
description: "什么是`nvue`？见[关于 nvue](/zh/guide/design.html#关于nvue). Invoke when user needs guidance on note."
url: "https://uviewpro.cn/zh/guide/note.html"
triggers: ["note","注意事项"]
---

# 注意事项

## uView Pro 对 nvue 的支持

什么是`nvue`？见[关于 nvue](/zh/guide/design.html#关于nvue)  
目前 uView 是`vue`版本，uView Pro 目前没有兼容 nvue，未来应该也不会兼容

## 技术点要求

1. uView Pro 依赖`SCSS`预处理器，所以您需要给 HBuilder X 安装 “sass/scss 编译” 插件，详见[快速上手](/zh/components/quickstart.html)
2. uView Pro 目前没有兼容 nvue，未来应该也不会兼容
3. uView Pro 基于 VSCode+Vue3 开发，旧版本可能会不兼容
4. uView 要求项目开启 uniapp 的 V3 版本，V3 有很大的优势，详见[V3 版本介绍](https://ask.dcloud.net.cn/article/36599)
5. HX2.5.5 稳定版正式引入`easycom`，建议开发者升级 HX 到 2.5.1 及以上的稳定版，详见[关于 easycom](/zh/components/quickstart.html#_3-配置easycom组件模式)

## 关于 VSCode

uView Pro 基于 VSCode + Vue3 开发，强烈建议使用 VSCode 系列的编辑器，因为 VSCode 的语法提示，代码补全，代码片段，AI 助手等，开发 Vue3 的项目，都是详尽的提示，可以保证你的代码不会出现任何问题。

## 关于 Hbuilder X

uniapp 依赖于 HX，uniapp 经过这两年发展(2018-2020)，势头强劲，茁壮成长。我们目睹了整个过程，陪着 uniapp 一起成长，感慨能有
一家良心企业能扎根技术，埋头苦干，把 APP，H5 还有各家小程序做到大一统，同时也愤慨各家大厂的小程序各自为营，仿佛倒退到多年前
各家[浏览器大战](https://baike.baidu.com/item/%E6%B5%8F%E8%A7%88%E5%99%A8%E5%A4%A7%E6%88%98/8488119?fr=aladdin)的时代，让人唏嘘不已。

uView Pro 也可以使用 HX 作为编辑器：

- 开发者在开发线上项目的时候只使用 HX 的稳定版
- 初学者不要使用 HX 内测版，不然会碰到莫名其妙的问题，会挫败学习信心
- 每当 HX 更新大功能的时候，比如以往的自定义组件模式，近来的 V3 版本，还是目前的 uniCloud，或者以后可能关于 nuve 的大功能，线上项目请过一段时间再使用。
- 建议喜欢尝鲜并熟悉 uniapp 的用户，在电脑分别安装 HX 的稳定版和内测版，尝鲜使用内测版，开发使用稳定版，二者分别更新，互不干扰

## 编译调试

开发的时候，特别是写布局的时候，我们建议使用 chrome 或者 HX 内置的浏览器，需要说明的是，电脑浏览器的预览效果是不精细的，
写完之后，可以手机连上电脑同一局域网的 WiFi，在手机浏览器上再进行细微的调整。  
写完布局再写逻辑的时候，如果还需要兼容小程序和 APP，一定要每写完一个页面，就用 APP 基座和小程序真机进行调试，这能及早发现问题，否则会剪不断理还乱。

## 安全区适配(针对 APP)

在 iPhone X 等机型，底部带有指示条，如果配置了`safearea`则会在底部生成一个原生的白色区块，好处是不会导致
误触，缺点是颜色无法修改，有时候也影响美观。  
uView Pro 在各个可能会受到指示条影响的地方都做了特别处理，比如弹窗，键盘组件等，详见[底部安全区适配](/zh/components/safeAreaInset.html)

## 为什么 uView Pro 的源码中会有那么多的注释？

> uView Pro 和 uView 一样，尽量保持详尽的注释，方便广大开发者使用，也方便开发者维护和升级。

很多开源项目，发布的时候都会刻意去掉注释，这可能是为了干净整洁，也可能是为了减少体积，还可能是出品方认为用户不会，也没必要去阅读源码。  
相反，uView 不这么认为，我们会一直将注释保留在发行的版本中，这些注释不是为了给我们自己看的，而是为了给用户看的。  
我们希望用户在使用的过程中，能通过阅读源码，既能提升工作效率，还能学到知识。因为 uView 的理念是"挣脱束缚，向往自由"，我们也希望您在阅读
源码的过程中，如果发现问题，或者有更好的实现方式和想法，可以反馈给我们，进而构建一个更强健的 UI 框架。
